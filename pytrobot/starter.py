from .robot import Robot
from .state import State
from .utils import *
from .user_functions import FunctionRegistry
import importlib.util

@apply_decorator_to_all_methods(handle_exceptions)
class Starter(Robot):

    def __init__(self, dir):
        super().__init__()
        self.current_state = State.STARTER
        self.user_dir = dir

    def load_user_functions(self):
        spec = importlib.util.spec_from_file_location("user_dir", self.user_dir)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    def on_entry(self):
        pass



        # if str(self) == "Robot.State.STARTER":
        #     func = FunctionRegistry.get(State.STARTER, 'on_entry')
        #     value = func[0]()
        #     return value
        # else:
        #     FunctionRegistry.register(State.STARTER, 'on_entry', self)

    def execute(self):
        pass



        # if str(self) == "Robot.State.STARTER":
        #     func = FunctionRegistry.get(State.STARTER, 'execute')
        #     value = func[0]()
        #     return value
        # else:
        #     FunctionRegistry.register(State.STARTER, 'execute', self)

    def on_exit(self):
        Robot.next_state = State.HANDLER



        # if str(self) == "Robot.State.STARTER":
        #     func = FunctionRegistry.get(State.STARTER, 'on_exit')
        #     func[0]()
        #     Robot.next_state = State.HANDLER
        # else:
        #     FunctionRegistry.register(State.STARTER, 'on_exit', self)

    def on_error(self):
        Robot.next_state = State.FINISHER



        # if str(self) == "Robot.State.STARTER":
        #     func = FunctionRegistry.get(State.STARTER, 'on_error')
        #     func[0]()
        #     Robot.next_state = State.FINISHER
        # else:
        #     FunctionRegistry.register(State.STARTER, 'on_error', self)