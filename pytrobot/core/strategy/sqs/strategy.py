# pytrobot/core/strategy/sqs/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.utility.config import Value
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.sqs.manager import SQSManager
from pytrobot.core.strategy.sqs.registry import SQSRegistry

class SQSStrategy(ApplicationStrategy, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.sqs_managers = {}

    def initialize(self, queue_name=None, region_name=None, queue_url=None, max_messages=None, wait_time=None):
        """
        Inicializa uma instância do SQSManager para uma fila específica.
        
        :param queue_name: Chave única para identificar a fila.
        :param region_name: Região AWS para a fila SQS.
        :param queue_url: URL da fila SQS.
        :param max_messages: Número máximo de mensagens a serem puxadas.
        :param wait_time: Tempo de espera para polling da fila.
        """
        for sqs_config in Value("aws.sqs"):
            task_registry = SQSRegistry()
            queue_name = sqs_config.get("queue_name")
            
            self.sqs_managers[queue_name] = SQSManager(
                task_registry  = task_registry,
                region_name    = sqs_config.get("region_name"),
                queue_url      = sqs_config.get("queue_url"),
                max_messages   = int(sqs_config.get("max_messages")),
                wait_time      = int(sqs_config.get("wait_time"))
            )

    def start(self):
        """
        Inicia o consumo da fila para todos os SQSManagers registrados.
        """
        for manager in self.sqs_managers.values():
            self.multithread_manager.new_thread(manager.start)

    def stop(self):
        """
        Para o consumo da fila para todos os SQSManagers registrados.
        """
        for manager in self.sqs_managers.values():
            self.multithread_manager.stop_thread(manager.start)

    def select_queue(self, queue_key: str) -> SQSManager:
        """
        Seleciona uma fila para envio de mensagens e retorna a instância do SQSManager.
        
        :param queue_key: A chave da fila a ser selecionada.
        :return: A instância de SQSManager correspondente à fila.
        """
        if queue_key in self.sqs_managers:
            return self.sqs_managers[queue_key]
        else:
            raise ValueError(f"Fila '{queue_key}' não encontrada.")