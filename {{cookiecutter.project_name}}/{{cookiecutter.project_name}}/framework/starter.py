from .robot import Robot
from .state import State
from .common import *
"""
imports do framework  ↑
imports do usuário    ↓
"""


@apply_decorator_to_all_methods(handle_exceptions)
class Starter(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.STARTER

    def on_entry(self):
        # instancia conexão com banco RPA
        pass

    def execute(self):
        # registra o id_job e guarda em config
        Config.job = self.mysql_rpa.execute_stored_procedure(
            'NEW_JOB', ['wmt-bot011-registro-di'])  # type: ignore

    def on_error(self):
        self.next_state = State.FINISHER

    def on_exit(self):
        self.next_state = State.HANDLER
