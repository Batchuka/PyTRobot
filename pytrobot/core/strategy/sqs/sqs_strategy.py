# pytrobot/core/strategy/celery/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.utility.config import Value
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.sqs.sqs_manager import SQSManager
from pytrobot.core.strategy.sqs.sqs_registry import SQSRegistry

class SQSStrategy(ApplicationStrategy, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.queue_manager: SQSManager

    def initialize(self, region_name=None, queue_url=None, max_messages=None, wait_time=None):
        task_registry = SQSRegistry()
        self.queue_manager = SQSManager(
            task_registry  = task_registry,
            region_name    = region_name     or Value("aws.region_name"),
            queue_url      = queue_url       or Value("aws.queue_url"),
            max_messages   = max_messages    or Value("aws.max_messages"),
            wait_time      = wait_time       or Value("aws.wait_time")
        )


    def start(self):

        self.multithread_manager.new_thread(self.queue_manager.start)

    def stop(self):

        self.multithread_manager.stop_thread(self.queue_manager.start)