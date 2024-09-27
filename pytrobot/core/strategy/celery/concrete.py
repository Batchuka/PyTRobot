# pytrobot/core/strategy/celery/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.utility.config import Value
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.celery.celery_manager import CeleryManager
from pytrobot.core.strategy.celery.task_registry import TaskRegistry

class CeleryStrategy(ApplicationStrategy, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.celery_manager: CeleryManager

    def initialize(self, region_name=None, role_arn=None, queue_url=None, queue_name=None, visibility_timeout=None, polling_interval=None):
        task_registry = TaskRegistry()
        self.celery_manager = CeleryManager(
            task_registry       = task_registry,
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