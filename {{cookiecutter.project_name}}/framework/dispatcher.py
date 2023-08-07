from framework.robot import *
from framework.config import *
from framework.utils import *


@apply_decorator_to_all_methods(with_logging)
@apply_decorator_to_all_methods(handle_exceptions)
class Dispatcher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.DISPATCHER

    def on_entry(self):

        pass

    def execute(self):

        pass

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER
