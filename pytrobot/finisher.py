from .robot import Robot
from .state import State
from .common import *
"""
imports do framework  ↑
imports do usuário    ↓
"""


@apply_decorator_to_all_methods(handle_exceptions)
class Finisher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.FINISHER

    def on_entry(self):
        Logger.log(
            "Imagine a instancia de algo usado para finalização da execução")

    def execute(self):
        Logger.log("Imagine o uso instancia para finalizar a execução")
        delete_all_temp_files()

    def on_exit(self):
        Logger.log("I'll be back!", level=logging.DEBUG)
        exit()

    def on_error(self):
        Logger.log("I shit myself!", level=logging.DEBUG)
        exit()
