# pytrobot/core/strategy/state/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.state.manager import StateManager, StateRegistry


class StateStrategy(ApplicationStrategy, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.state_manager : StateManager

    def initialize(self):
        state_registry = StateRegistry()
        self.state_manager = StateManager(
            state_registry      = state_registry
        )

    def start(self):

        self.multithread_manager.new_thread(self.state_manager.run)

    def stop(self):

        self.multithread_manager.stop_thread(self.state_manager.run)