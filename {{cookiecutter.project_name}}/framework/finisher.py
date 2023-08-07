from framework.robot import *
from framework.config import *
from framework.utils import *


@apply_decorator_to_all_methods(with_logging)
@apply_decorator_to_all_methods(handle_exceptions)
class Finisher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.FINISHER

    def on_entry(self):

        # se prepare para desligar: salve algo se precisar
        pass

    def execute(self):

        # Feche todas as aplicações, limpe sua bagunça e mande um Log
        pass

    def on_error(self):

        delete_all_temp_files()
        logging.debug("I shit myself!")
        exit()

    def on_exit(self):

        delete_all_temp_files()
        logging.debug("I'll be back!")
        exit()
