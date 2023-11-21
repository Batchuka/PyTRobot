from .robot import Robot
from .state import State
from .utils import *
from .user_functions import FunctionRegistry

@apply_decorator_to_all_methods(handle_exceptions)
class Dispatcher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.DISPATCHER

    def on_entry(self):
        if str(self) == "Robot.State.DISPATCHER":
            func = FunctionRegistry.get(State.DISPATCHER, 'on_entry')
            value = func[0]()
            return value
        else:
            FunctionRegistry.register(State.DISPATCHER, 'on_entry', self)

    def execute(self):
        if str(self) == "Robot.State.DISPATCHER":
            func = FunctionRegistry.get(State.DISPATCHER, 'execute')
            value = func[0]()
            return value
        else:
            FunctionRegistry.register(State.DISPATCHER, 'execute', self)

    def on_exit(self):
        Robot.next_state = State.HANDLER
        # if str(self) == "Robot.State.DISPATCHER":
        #     func = FunctionRegistry.get(State.DISPATCHER, 'on_exit')
        #     func[0]()
        #     Robot.next_state = State.HANDLER
        # else:
        #     FunctionRegistry.register(State.DISPATCHER, 'on_exit', self)

    def on_error(self):
        Robot.next_state = State.FINISHER
        # if str(self) == "Robot.State.DISPATCHER":
        #     func = FunctionRegistry.get(State.DISPATCHER, 'on_error')
        #     func[0]()
        #     Robot.next_state = State.FINISHER
        # else:
        #     FunctionRegistry.register(State.DISPATCHER, 'on_error', self)