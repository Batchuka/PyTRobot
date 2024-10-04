# pytrobot/core/strategy/celery/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.utility.config import Value
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.queue.queue_manager import QueueManager
from pytrobot.core.strategy.queue.task_registry import TaskRegistry

class CeleryStrategy(ApplicationStrategy, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.queue_manager: QueueManager

    def initialize(self):
        task_registry = TaskRegistry()
        self.queue_manager = QueueManager(task_registry)

    def start(self):

        self.multithread_manager.new_thread(self.queue_manager.start)

    def stop(self):

        self.multithread_manager.stop_thread(self.queue_manager.start)