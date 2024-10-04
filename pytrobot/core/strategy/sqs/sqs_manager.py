import time
import threading
from queue import Queue
from pytrobot.core.utility.log import LogManager
from pytrobot.core.strategy.sqs.sqs_registry import SQSRegistry
import boto3

class SQSManager:
    def __init__(self, task_registry: SQSRegistry, region_name=None, queue_url=None, max_messages=None, wait_time=60):
        """
        Inicializa o QueueManager com o registro de tasks e configurações para SQS.
        """
        self.task_registry = task_registry
        self.logger = LogManager().get_logger('SQS')
        self.local_queue = Queue()  # Fila local para armazenar itens
        self.region_name = region_name
        self.queue_url = queue_url
        self.max_messages = max_messages
        self.wait_time = wait_time

        # Conecta ao cliente SQS
        self.sqs_client = boto3.client('sqs', region_name=self.region_name)
        
        # Inicia o processo de consumo da fila
        self.start()

    def start(self):
        """
        Inicia o processo de consumo da fila SQS.
        """
        while True:
            # Busca mensagens da fila SQS
            self.logger.info("Buscando mensagens da fila SQS...")
            messages = self.pull_messages()
            
            if messages:
                # Adiciona mensagens à fila local para processamento
                for message in messages:
                    self.local_queue.put(message)
                    self.logger.info(f"Mensagem {message['MessageId']} adicionada à fila local.")

                # Processa a fila local
                self.process_queue()

            # Pausa entre polls se não houver mensagens
            if self.local_queue.empty():
                self.logger.info("Nenhuma mensagem encontrada. Esperando antes do próximo polling...")
                time.sleep(self.wait_time)
                continue

    def pull_messages(self):
        """
        Busca mensagens da fila SQS e as retorna.
        """
        response = self.sqs_client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=self.max_messages,
            WaitTimeSeconds=self.wait_time
        )
        return response.get('Messages', [])

    def process_queue(self):
        """
        Consome a fila local e processa os itens, identificando e executando as tasks associadas.
        """
        while True:
            message = self.local_queue.get()
            self.logger.info(f"Processando mensagem: {message['MessageId']}")
            self.handle_message(message)

    def handle_message(self, message):
        """
        Processa uma mensagem específica do SQS. Identifica se a mensagem é para uma Task.
        """
        body = self.parse_message_body(message)
        
        # Identifica qual task deve ser executada com base na mensagem
        task_name = body.get('task_name')
        task_kwargs = body.get('kwargs', {})

        if task_name:
            self.execute_task(task_name, **task_kwargs)
        else:
            self.logger.warning(f"Mensagem inválida ou sem task associada: {message['MessageId']}")

    def parse_message_body(self, message):
        """
        Converte a mensagem SQS para um dicionário utilizável. 
        Isso assume que o corpo da mensagem é JSON, pode ajustar conforme necessário.
        """
        import json
        return json.loads(message['Body'])

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