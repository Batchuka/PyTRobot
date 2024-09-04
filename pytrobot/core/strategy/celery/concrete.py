# pytrobot/core/strategy/celery/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.utility.config import Value
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.celery.celery_manager import CeleryManager

class CeleryStrategy(ApplicationStrategy, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.celery_manager: CeleryManager

    def initialize(self, region_name=None, role_arn=None, queue_url=None, queue_name=None, visibility_timeout=None, polling_interval=None):
        """Permite passar os valores diretamente ou usar o Value para pegar os valores do arquivo de configuração."""
        self.celery_manager = CeleryManager(
            region_name         = region_name           or Value("aws.region_name"),
            role_arn            = role_arn              or Value("aws.role_arn"),
            queue_url           = queue_url             or Value("aws.queue_url"),
            queue_name          = queue_name            or Value("aws.queue_name"),
            visibility_timeout  = visibility_timeout    or Value("general.visibility_timeout"),
            polling_interval    = polling_interval      or Value("general.polling_interval")
        )

    def start(self):

        self.multithread_manager.new_thread(self.celery_manager.run)

    def stop(self):

        self.multithread_manager.stop_thread(self.celery_manager.run)

if __name__ == "__main__":
    
    import time

    # Testando passando argumentos diretamente
    cs_obj = CeleryStrategy()
    cs_obj.initialize(
        region_name          = "us-east-1",
        role_arn             = "arn:aws:iam::435062120355:role/wmt-service-robot-role",
        queue_url            = "https://sqs.us-east-1.amazonaws.com/435062120355/wmt-declaracao-importacao-queue",
        queue_name           = "wmt-declaracao-importacao-queue",
        visibility_timeout   = 3600,
        polling_interval     = 10
    )
    cs_obj.start()
    cs_obj.multithread_manager.list_active_threads()
    while True:
        print("aqui é a principal")
        time.sleep(10)
