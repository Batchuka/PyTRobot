# exemplo → from make_database import MySQL

"""
"""
from framework.robot import Robot, State
from framework.config import Config
from framework.transaction import Transaction
from framework.utils import *


@apply_decorator_to_all_methods(handle_exceptions)
@apply_decorator_to_all_methods(with_logging)
class Starter(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.STARTER

    def on_entry(self):

        result = MySQL.select('classificao_email', "id_status='2'")

    def execute(self):

        # Instalação do certificado
        pass

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER
