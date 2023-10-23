from .robot import Robot
from .state import State
from .common import *
"""
imports do framework  ↑
imports do usuário    ↓
"""


@apply_decorator_to_all_methods(handle_exceptions)
class Dispatcher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.DISPATCHER

    def on_entry(self):
        Logger.log(
            "imagine a instancia de algo usado para enriquecimento do dataset")

    def execute(self):
        # lógicas alvo do dispatcher
        Logger.log("imagine uma lógica para enriquecer de fato")
        if Robot.transaction_data is None:
            raise ValueError("There is not Transaction Data")
        self.update()

    def update(self):
        for item in Robot.transaction_data:
            item["LOG"] = "teste"

    def on_exit(self):
        self.next_state = State.HANDLER

    def on_error(self):
        self.next_state = State.FINISHER
