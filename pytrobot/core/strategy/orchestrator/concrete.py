# pytrobot/core/strategy/orchestrator/concrete.py
import warnings
from pytrobot.core.singleton import Singleton
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.state.state_machine import StateMachine, TrueTable


class StateStrategy(ApplicationStrategy, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self._first_state_name = None
        self.state_machine : StateMachine

    def initialize(self):
        self.state_machine = StateMachine(true_table=TrueTable())

    def start(self):
        self.state_machine.run()