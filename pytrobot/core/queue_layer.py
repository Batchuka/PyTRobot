# pytrobot/core/queue_layer.py

import time
from queue import Queue
from pytrobot.core.singleton import Singleton
import boto3
from datetime import datetime

class QueueLink(metaclass=Singleton):

    def __init__(self, role_arn, remote_queue_url, region_name='us-east-1', session_duration=3600, queue_type='FIFO'):
        """
        Inicializa o QueueManager, associando-se a uma fila remota específica no SQS.
        """
        self.local_queue = Queue()
        self.role_arn = role_arn
        self.remote_queue_url = remote_queue_url
        self.region_name = region_name
        self.session_duration = session_duration
        self.sqs = self.assume_role_and_get_sqs_client()

    def assume_role_and_get_sqs_client(self):
        """
        Assume a role do IAM e retorna um cliente SQS com credenciais temporárias.
        """
        sts_client = boto3.client('sts')
        session_name = f"AssumeRoleSession_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        assumed_role_object = sts_client.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=session_name,
            DurationSeconds=self.session_duration
        )
        credentials = assumed_role_object['Credentials']

        sqs_client = boto3.client(
            'sqs',
            region_name=self.region_name,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )

        return sqs_client

    def add_item(self, item):
        """
        Adiciona um item à fila de QueueManager.
        """
        self.local_queue.put(item)

    def get_item(self):
        """
        Pega um item da fila de QueueManager.
        """
        if not self.local_queue.empty():
            return self.local_queue.get()
        return None

    def fetch_from_sqs(self, max_messages=10):
        """
        Busca mensagens da fila SQS e adiciona à fila local.
        """
        response = self.sqs.receive_message(
            QueueUrl=self.remote_queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=10
        )

        messages = response.get('Messages', [])
        for message in messages:
            item = self.process_message(message)
            self.add_item(item)
            self.sqs.delete_message(
                QueueUrl=self.remote_queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )

    def process_message(self, message):
        """
        Processa a mensagem recebida do SQS.
        """
        # Implementar lógica para processar a mensagem e extrair o item
        item = {
            'id': message['MessageId'],
            'body': message['Body'],
            'retry_count': 0
        }
        return item

    def handle_processing_failure(self, item):
        """
        Lida com falhas no processamento do item.
        """
        item['retry_count'] += 1
        max_retries = 3
        if item['retry_count'] > max_retries:
            # Mover para a DLQ
            self.move_to_dlq(item)
        else:
            # Re-enfileirar para nova tentativa
            self.add_item(item)

    def move_to_dlq(self, item):
        """
        Move um item para a Dead-Letter Queue.
        """
        dlq_url = 'YOUR_DLQ_URL'  # Defina a URL da sua DLQ
        self.sqs.send_message(
            QueueUrl=dlq_url,
            MessageBody=item['body']
        )


class QueueMachine(metaclass=Singleton):

    def __init__(self, role_arn, remote_queue_url, max_items=100, interval=5, region_name='us-east-1', session_duration=3600):
        self.queue_link = QueueLink(role_arn, remote_queue_url, region_name, session_duration)
        self.running = True
        self.max_items = max_items
        self.interval = interval

    def start(self):
        """
        Inicia a máquina de filas, mantendo o loop principal para sincronização e verificação de threads.
        """
        while self.running:
            # Sincronizar a fila local com a fila remota
            self.sync_with_remote()
            # Verificar e iniciar threads para rotinas associadas a itens na fila
            self.manage_routines()
            # Pausar por um intervalo antes da próxima iteração
            time.sleep(self.interval)

    def stop(self):
        """
        Lógicas para o encerramento gracioso do robô.
        """
        self.running = False
        self.queue_link.stop()

    def sync_with_remote(self):
        """
        Sincroniza a fila local com a fila remota se houver espaço na fila local.
        """
        if self.queue_link.local_queue.qsize() < self.max_items:
            self.queue_link.fetch_from_sqs(max_messages=self.max_items - self.queue_link.local_queue.qsize())

    def manage_routines(self):
        """
        Verifica se existem itens na fila local sem threads ativas e inicia as threads das rotinas associadas.
        """
        for routine_name, routine_instance in self.queue_link.routines.items():
            if not routine_instance.is_thread_active():
                for item in list(self.queue_link.local_queue.queue):
                    if routine_instance.condition(item):
                        routine_instance.start(item)
                        break  # Inicia apenas uma thread por iteração

    def register_routine(self, routine_class):
        """
        Registra uma rotina associada a um identificador específico.
        """
        self.queue_link.register_routine(routine_class)

### Códigos que sairão daqui

import threading

class BaseRoutine(metaclass=Singleton):

    def __init__(self, local_queue):
        self.thread = None
        self.itens = []
        self.local_queue = local_queue

    def _condition(self):
        """
        Verifica se há itens na fila com o id_routine correto.
        """
        self.itens = [item for item in self.local_queue.queue if item.get('id_routine') == self.__class__.identifier]
        return bool(self.itens)

    def setup(self):
        """
        O usuário deve implementar lógica para configurar a rotina.
        """
        raise NotImplementedError("O método 'setup' deve ser implementado pela classe derivada.")

    def routine(self):
        """
        O usuário deve implementar lógica que ficará em loop na thread enquanto houverem self.itens.
        """
        raise NotImplementedError("O método 'routine' deve ser implementado pela classe derivada.")

    def _routine(self):
        """
        Wrapper de routine que faz o while enquanto houver itens. Se não houver exceção, 
        o item deve ser retirado da lista 'self.itens' e da fila também.
        """
        self.setup()
        while self._condition():
            try:
                self.routine()
                if self.itens:
                    item = self.itens.pop(0)
                    self.local_queue.task_done(item)
            except Exception as e:
                print(f"Erro na rotina: {e}")

    def is_thread_active(self):
        """
        Verifica se a thread está ativa e, se não estiver, verifica a condição e inicia a thread novamente.
        """
        if not (self.thread and self.thread.is_alive()):
            if self._condition():
                self.thread = threading.Thread(target=self._routine)
                self.thread.start()


def Routine(cls, id_routine):
    """
    Decorador para registrar a rotina na QueueLink da QueueMachine.
    """
    queue_machine = QueueMachine()
    queue_machine.register_routine(cls)
    return cls



if __name__ == "__main__":

    # Inicializar a QueueMachine com parâmetros necessários
    role_arn = "arn:aws:iam::123456789012:role/wmt-service-robot-role"
    remote_queue_url = "YOUR_SQS_QUEUE_URL"
    queue_machine = QueueMachine(role_arn, remote_queue_url, max_items=100, interval=5)

    pass

    @Routine('printar_valores')
    class PrintarValoresRoutine(BaseRoutine):

        def condition(self, itens):
            # Implementar a lógica para validar a condição
            return True

        def setup(self):
            # Implementar a lógica de setup
            pass

        def routine(self):
            # Implementar a lógica da rotina
            while True:
                # Loop da rotina
                pass

    @Routine
    class AcessarSiteRoutine(BaseRoutine):

        def condition(self, item):
            # Implementar a lógica para validar a condição
            return True

        def setup(self, item):
            # Implementar a lógica de setup
            pass

        def routine(self):
            # Implementar a lógica da rotina
            while True:
                # Loop da rotina
                pass

    # Iniciar a máquina de filas
    queue_machine.start()