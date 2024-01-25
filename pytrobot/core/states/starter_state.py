from pytrobot.core.states.base_state import BaseState

class _StarterState(BaseState):
    
    def __init__(self):
        self._status = None

    def execute(self):
        pass

    def on_entry(self):
        pass

    def on_exit(self):
        pass

    def on_error(self):
        pass
