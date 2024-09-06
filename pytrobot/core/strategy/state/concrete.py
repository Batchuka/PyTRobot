# pytrobot/core/strategy/state/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.state.state_machine import StateMachine, TrueTable


class StateStrategy(ApplicationStrategy, metaclass=Singleton):
    # TODO: Talvez seja o caso de desvinciliar a máquina de estados do 'StateManager'
    def __init__(self):
        super().__init__()
        self._first_state_name = None
        self.state_manager : StateMachine

    def initialize(self):

        true_table = TrueTable()
        self.state_manager = StateMachine(true_table=true_table)

    def start(self):

        self.multithread_manager.new_thread(self.state_manager.run)

    def stop(self):

        self.multithread_manager.stop_thread(self.state_manager.run)