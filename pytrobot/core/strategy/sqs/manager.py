# pytrobot\core\strategy\sqs\manager.py
import time
import json
import threading
from queue import Queue, Empty
import boto3

from pytrobot.core.utility.log import LogManager
from pytrobot.core.strategy.sqs.registry import SQSRegistry
from pytrobot.core.strategy.sqs.message_builder import SQSMessage

class SQSManager:
    def __init__(self, task_registry: SQSRegistry, region_name=None, queue_url=None, max_messages=None, wait_time=60):
        """
        Inicializa o QueueManager com o registro de tasks e configurações para SQS.
        """
        self.task_registry = task_registry
        self.logger = LogManager().get_logger('SQS')
        self.local_queue = Queue()
        self.region_name = region_name
        self.queue_url = queue_url
        self.max_messages = max_messages
        self.wait_time = wait_time

        # Conecta ao cliente SQS
        self.sqs_client = boto3.client('sqs', region_name=self.region_name)
        # self.sqs_queue = self.sqs_client.get_queue_by_name(QueueName='wmt-rpa-teste')
        
        # Inicia o processo de consumo da fila
        self.start()

        # Flag para controle do loop de polling
        self.keep_polling = True

    def start(self):
        """
        Inicia o processo de consumo da fila SQS e processamento da fila local.
        """
        self.logger.info("Iniciando consumo da fila SQS...")
        # Cria uma thread para consumo e processamento de mensagens
        polling_thread = threading.Thread(target=self._poll_and_process_messages, daemon=True)
        polling_thread.start()

    def _poll_and_process_messages(self):
        """
        Puxa mensagens da fila SQS e as processa na fila local.
        """
        while self.keep_polling:
            # Puxa mensagens da fila SQS
            messages = self.pull_messages()
            
            # Se houver mensagens, as adiciona à fila local
            if messages:
                for message in messages:
                    self.local_queue.put(message)
                    self.logger.info(f"Mensagem {message['MessageId']} adicionada à fila local.")

            # Processa mensagens da fila local
            self.process_queue()

            # Pausa antes do próximo polling
            time.sleep(self.wait_time)

    def pull_messages(self):
        """
        Busca mensagens da fila SQS e as retorna.
        """
        try:
            response = self.sqs_client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=self.max_messages,  # Certifique-se de que self.max_messages <= 10
                WaitTimeSeconds=self.wait_time  # Long Polling
            )
            messages = response.get('Messages', [])
            
            # Loga o tamanho das mensagens recebidas para debug
            self.logger.info(f"Número de mensagens recebidas: {len(messages)}")
            return messages

        except Exception as e:
            self.logger.error(f"Erro ao buscar mensagens da fila SQS: {e}")
            return []

    def process_queue(self):
        """
        Consome a fila local e processa os itens, identificando e executando as tasks associadas.
        """
        while not self.local_queue.empty():
            try:
                message = self.local_queue.get(timeout=1)  # Tenta obter uma mensagem da fila local
                self.logger.info(f"Processando mensagem: {message['MessageId']}")
                self.handle_message(message)
                self.local_queue.task_done()
            except Empty:
                break

    def handle_message(self, message):
        """
        Processa uma mensagem específica do SQS. Identifica se a mensagem é para uma Task.
        """
        body = self.parse_message_body(message)
        
        # Identifica qual task deve ser executada com base na mensagem
        task_name = body.get('task_name')
        task_kwargs = body.get('kwargs', {})

        if task_name:
            # Verifica se a task está registrada
            if task_name in self.task_registry.get_all():
                self.logger.warning("Não tem essa atividade")
                success = self.execute_task(task_name, **task_kwargs)
                if success:
                    self.delete_message(message)
            else:
                self.logger.warning(f"Tarefa '{task_name}' não registrada. Mensagem ID: {message['MessageId']}")
        else:
            self.logger.warning(f"Mensagem inválida ou sem task associada: {message['MessageId']}")

    def parse_message_body(self, message):
        """
        Converte a mensagem SQS para um dicionário utilizável.
        Isso assume que o corpo da mensagem é JSON, mas verifica antes.
        """
        body = message['Body']

        # Verifica se o 'body' já está em formato de dicionário
        if isinstance(body, str):
            try:
                # Se for uma string, tenta fazer o load como JSON
                body = body.replace("'", '"')
                return json.loads(body)
            except json.JSONDecodeError as e:
                self.logger.error(f"Erro ao decodificar JSON da mensagem: {e}")
                return {}
        elif isinstance(body, dict):
            # Se já for um dicionário, apenas retorna
            return body
        else:
            # Se não for nem string nem dicionário, retorna vazio com erro
            self.logger.error("Formato inesperado no campo 'Body' da mensagem.")
            return {}

    def execute_task(self, task_name, **kwargs):
        """
        Executa a task a partir do nome fornecido. Cria uma nova thread para a execução se necessário.
        """
        task_cls = self.task_registry.get_all().get(task_name)
        if task_cls:
            # Determina se deve executar em uma nova thread ou na principal
            if hasattr(task_cls, 'run_in_thread') and task_cls.run_in_thread:
                thread = threading.Thread(target=self.run_task, args=(task_cls, kwargs), daemon=True)
                thread.start()
                self.logger.info(f"Task {task_name} executada em nova thread.")
            else:
                # Executa na thread principal
                self.logger.info(f"Task {task_name} sendo executada na thread principal.")
                self.run_task(task_cls, kwargs)

            return True
        else:
            self.logger.error(f"Tarefa {task_name} não encontrada no registro.")
            return False

    def run_task(self, task_cls, kwargs):
        """
        Executa a lógica da task dentro de uma thread.
        """
        try:
            task_instance = task_cls()
            task_instance.run(**kwargs)
            self.logger.info(f"Tarefa {task_cls.__name__} executada com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao executar a tarefa {task_cls.__name__}: {e}")

    def send_message(self, message: SQSMessage) -> bool:
        """
        Envia uma mensagem para a fila SQS.
        
        :param message: Instância de SQSMessage a ser enviada.
        :return: True se a mensagem foi enviada com sucesso, False caso contrário.
        """
        try:
            # Publica a mensagem na fila SQS
            self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                # MessageBody=message.to_dict()['MessageBody']
                MessageBody=str(message.to_dict())
            )
            self.logger.info(f"Mensagem enviada para a fila SQS")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao enviar mensagem para a fila SQS: {e}")
            return False

    def delete_message(self, message):
        """
        Exclui uma mensagem da fila SQS.
        """
        try:
            self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            self.logger.info(f"Mensagem {message['MessageId']} excluída da fila SQS.")
        except Exception as e:
            self.logger.error(f"Erro ao excluir mensagem {message['MessageId']}: {e}")

# if __name__ == "__main__":
#     from pytrobot.core.strategy.sqs.registry import SQSRegistry
#     from pytrobot.core.strategy.sqs.message_builder import SQSMessageBuilder

#     # Simulação dos valores necessários para SQS
#     region_name = 'us-east-1'
#     queue_url = 'https://sqs.us-east-1.amazonaws.com/435062120355/wmt-rpa-teste'
#     max_messages = 10
#     wait_time = 20

#     # Cria uma instância de SQSRegistry para registrar tasks simuladas
#     task_registry = SQSRegistry()

#     # # Simulação de uma task para registrar no registry
#     # class DummyTask:
#     #     def run(self, **kwargs):
#     #         print(f"Executando DummyTask com args: {kwargs}")

#     # # Registrar a task DummyTask
#     # task_registry.register('DummyTask', DummyTask)

#     # Inicializa o SQSManager com task_registry
#     sqs_manager = SQSManager(
#         task_registry=task_registry,
#         region_name=region_name,
#         queue_url=queue_url,
#         max_messages=max_messages,
#         wait_time=wait_time
#     )

#     # # Simula a criação de uma mensagem com o builder
#     # message = SQSMessageBuilder(task_name='DummyTask').add_kwargs(param1='value1', param2='value2').build()

#     # # Enviar a mensagem para a fila SQS
#     # sqs_manager.send_message(message)

#     # Inicia o processo de polling e processamento (não irá parar, então limite o tempo no teste)
#     try:
#         sqs_manager.start()
#         while True:
#             time.sleep(10)
#     except KeyboardInterrupt:
#         print("Encerrando o processo.")
