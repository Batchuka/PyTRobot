from framework.robot import *
from framework.config import *
from framework.utils import *


@apply_decorator_to_all_methods(with_logging)
@apply_decorator_to_all_methods(handle_exceptions)
class Starter(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.STARTER

    def on_entry(self):

        # inicie seu dicionário de assets caso não exista
        print("...")

    def execute(self):

        # para garantir a limpeza de arquivos residuais
        print(...)

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER
