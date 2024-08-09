# pytrobot/core/strategy/application_strategy.py
from abc import ABC, abstractmethod
from pytrobot.core.feature.multithread import MultithreadManager
from pytrobot.core.feature.subprocess import SubprocessManager

class ApplicationStrategy(ABC):
    def __init__(self):
        self.multithread_manager = MultithreadManager()
        self.subprocess_manager = SubprocessManager()
        
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def start(self):
        pass