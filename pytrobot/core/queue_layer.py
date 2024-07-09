# pytrobot/core/queue_layer.py

import time
from queue import Queue
from pytrobot.core.singleton import Singleton
import boto3

class QueueLink(metaclass=Singleton):

    def __init__(self, queue_type='FIFO'):
        """
        Inicializa o QueueManager, associando-se a uma fila remota específica no SQS.
        """
        self.local_queue = Queue()
        self.running = True
        self.worker_threads = []
        self.sqs = boto3.client('sqs', region_name='us-east-1')  # Configure sua região
        self.remote_queue_url = 'YOUR_SQS_QUEUE_URL'  # Defina a URL da sua fila SQS

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

    def update_item(self, item_id, new_data):
        """
        Atualiza um item na fila de QueueManager.
        """
        temp_queue = Queue()
        while not self.local_queue.empty():
            item = self.local_queue.get()
            if item.get('id') == item_id:
                item.update(new_data)
            temp_queue.put(item)
        self.local_queue = temp_queue

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
            'body': message['Body']
        }
        return item

    def stop(self):
        """
        Finaliza a execução do QueueManager.
        """
        self.running = False
        for thread in self.worker_threads:
            thread.join()


class QueueMachine(metaclass=Singleton):

    def __init__(self, max_items=100, interval=5):
        self.local_queue = QueueLink()
        self.running = True
        self.max_items = max_items
        self.interval = interval
        self.routines = {}

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
        self.local_queue.stop()

    def sync_with_remote(self):
        """
        Sincroniza a fila local com a fila remota se houver espaço na fila local.
        """
        if self.local_queue.local_queue.qsize() < self.max_items:
            self.local_queue.fetch_from_sqs(max_messages=self.max_items - self.local_queue.local_queue.qsize())

    def manage_routines(self):
        """
        Verifica se existem itens na fila local sem threads ativas e inicia as threads das rotinas associadas.
        """
        for item in list(self.local_queue.local_queue.queue):
            item_id = item.get('id')
            routine_class = self.routines.get(item.get('routine'))
            if routine_class and not routine_class.is_thread_active(item_id):
                if routine_class.condition(item):
                    routine_class.setup(item)
                    routine_class.start_thread(item)

    def register_routine(self, routine_class):
        """
        Registra uma rotina associada a um identificador específico.
        """
        routine_instance = routine_class(self.local_queue)
        self.routines[routine_class.identifier] = routine_instance