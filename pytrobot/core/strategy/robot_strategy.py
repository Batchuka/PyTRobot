# pytrobot/core/strategy/robot_strategy.py
from abc import ABC, abstractmethod

class RobotStrategy(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def start(self):
        pass