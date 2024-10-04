import threading
from queue import Queue
from pytrobot.core.utility.log import LogManager
from pytrobot.core.strategy.queue.task_registry import TaskRegistry

class QueueManager:
    def __init__(self, task_registry: TaskRegistry, config=None):
        """
        Inicializa o QueueManager com um registro de tasks e configurações opcionais.
        """
        self.task_registry = task_registry
        self.logger = LogManager().get_logger('Queue')
        self.local_queue = Queue()  # Fila local para armazenar itens
        self.config = config or {}

    def pull_from_external_queue(self):
        """
        Simula a extração de itens de uma fila externa. Esta função deve ser
        personalizada para qualquer tecnologia de fila que for usada.
        """
        # Lógica personalizada para integração com filas como SQS, RabbitMQ, etc.
        # Exemplo: connection.get_message() para adicionar itens à `local_queue`.
        pass

    def add_item(self, item):
        """
        Adiciona um item na fila local. O item pode ter diferentes tipos ou destinos.
        """
        self.local_queue.put(item)
        self.logger.info(f"Item adicionado à fila local: {item}")

    def process_queue(self):
        """
        Consome a fila local e processa os itens.
        """
        while True:
            item = self.local_queue.get()
            self.logger.info(f"Processando item da fila: {item}")
            self.handle_item(item)

    def handle_item(self, item):
        """
        Processa um item específico. Identifica se o item é uma task e executa a task.
        """
        # Exemplo de identificação de item (isso deve ser personalizado):
        task_name = item.get('task_name')
        task_kwargs = item.get('kwargs', {})

        if task_name:
            self.execute_task(task_name, **task_kwargs)
        else:
            self.logger.warning(f"Item inválido ou desconhecido: {item}")

    def execute_task(self, task_name, **kwargs):
        """
        Executa a task a partir do nome fornecido. Cria uma nova thread para a execução.
        """
        task_cls = self.task_registry.get(task_name)
        if task_cls:
            thread = threading.Thread(target=self.run_task, args=(task_cls, kwargs), daemon=True)
            thread.start()
            self.logger.info(f"Task {task_name} executada em nova thread.")
        else:
            self.logger.error(f"Tarefa {task_name} não encontrada no registro.")

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

    def start(self):
        """
        Inicia o processo de consumo de fila.
        """
        consumer_thread = threading.Thread(target=self.process_queue, daemon=True)
        consumer_thread.start()
        self.logger.info("Iniciado o consumo da fila local.")
