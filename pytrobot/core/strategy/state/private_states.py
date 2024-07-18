# pytrobot/core/strategy/state/private_states.py
from pytrobot.core.strategy.state.base_state import BaseState
from pytrobot.core.feature.multithread import MultithreadManager
from pytrobot.core.feature.subprocess import SubprocessManager


class _FinisherState(BaseState):

    def execute(self):
        pass

    def on_entry(self):
        self.multithread_manager = MultithreadManager()
        self.subprocess_manager = SubprocessManager()

    def on_exit(self):
        import sys
        # Lista as threads ativas antes de sair
        self.multithread_manager.list_active_threads()
        self.subprocess_manager.list_active_processes()
        sys.exit()

    def on_error(self):
        import os
        os._exit(0)

class _StarterState(BaseState):

    def execute(self):
        pass

    def on_entry(self):
        pass

    def on_exit(self):
        pass

    def on_error(self):
        pass