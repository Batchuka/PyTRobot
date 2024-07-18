# pytrobot/core/strategy/orchestrator_strategy.py
from pytrobot.core.strategy.robot_strategy import RobotStrategy
from pytrobot.core.strategy.orchestrator.celery_manager import CeleryManager

class CeleryStrategy(RobotStrategy):
    
    def __init__(self):
        self.celery_layer : CeleryManager

    def initialize(self):
        self.celery_layer = CeleryManager()

    def start(self):
        self.celery_layer.run()