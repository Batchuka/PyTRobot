# pytrobot/core/strategy/state/concrete.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.strategy.application_strategy import ApplicationStrategy
from pytrobot.core.strategy.state.state_manager import StateManager, TrueTable


class StateStrategy(ApplicationStrategy, metaclass=Singleton):
    # TODO: Talvez seja o caso de desvinciliar a máquina de estados do 'StateManager'
    def __init__(self):
        super().__init__()
        self._first_state_name = None
        self.state_manager : StateManager

    def initialize(self):

        self.state_manager = StateManager(true_table=TrueTable())

    def start(self):

        self.multithread_manager.new_thread(self.state_manager.run)

    def stop(self):

        self.multithread_manager.stop_thread(self.state_manager.run)


if __name__ == "__main__":

    import time

    # Testando passando argumentos diretamente
    ss_obj = StateStrategy()
    ss_obj.initialize()
    ss_obj.start()
    ss_obj.multithread_manager.list_active_threads()
    while True:
        print("aqui é a principal")
        time.sleep(10)
