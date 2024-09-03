# pytrobot/core/strategy/state/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.state.state_manager import StateManager, TrueTable


class StateStrategy(ApplicationStrategy, metaclass=Singleton):
    # TODO: Talvez seja o caso de desvinciliar a máquina de estados do 'StateManager'
    def __init__(self):
        super().__init__()
        self._first_state_name = None
        self.state_machine : StateManager

    def initialize(self):
        self.state_machine = StateManager(true_table=TrueTable())

    def start(self):
        self.state_machine.run()