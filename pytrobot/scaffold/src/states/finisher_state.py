from pytrobot.core.states.base_state import BaseState

class _FinisherState(BaseState):

    def execute(self):
        pass

    def on_entry(self):
        pass

    def on_exit(self):
        exit()

    def on_error(self):
        exit()
