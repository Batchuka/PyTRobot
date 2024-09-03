# pytrobot/core/strategy/celery/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.utility.config import Value
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.celery.celery_manager import CeleryManager

class CeleryStrategy(ApplicationStrategy, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.celery_layer: CeleryManager

    def initialize(self):
        self.celery_layer = CeleryManager(
            region_name=Value("aws.region_name"),
            role_arn=Value("aws.role_arn"),
            queue_url=Value("aws.queue_url"),
            queue_name=Value("aws.queue_name"),
            visibility_timeout=Value("general.visibility_timeout"),
            polling_interval=Value("general.polling_interval")
        )

    def start(self):
        self.multithread_manager.thread(self.celery_layer.run())

    def stop(self):
        self.multithread_manager.stop_thread('start')