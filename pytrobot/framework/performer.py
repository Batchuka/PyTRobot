from pytrobot.framework.robot import Robot
from pytrobot.framework.state import State
from pytrobot.framework.utils import *
from pytrobot.framework.user_functions import FunctionRegistry

@apply_decorator_to_all_methods(handle_exceptions)
class Performer(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.PERFORMER

    def on_entry(self):
        if str(self) == "Robot.State.PERFORMER":
            func = FunctionRegistry.get(State.PERFORMER, 'on_entry')
            value = func[0]()
            return value
        else:
            FunctionRegistry.register(State.PERFORMER, 'on_entry', self)

    def execute(self):
        if str(self) == "Robot.State.PERFORMER":
            func = FunctionRegistry.get(State.PERFORMER, 'execute')
            value = func[0]()
            return value
        else:
            FunctionRegistry.register(State.PERFORMER, 'execute', self)

    def on_exit(self):
        Robot.next_state = State.HANDLER
        # if str(self) == "Robot.State.PERFORMER":
        #     func = FunctionRegistry.get(State.PERFORMER, 'on_exit')
        #     func[0]()
        #     Robot.next_state = State.HANDLER
        # else:
        #     FunctionRegistry.register(State.PERFORMER, 'on_exit', self)

    def on_error(self):
        Robot.next_state = State.FINISHER
        # if str(self) == "Robot.State.PERFORMER":
        #     func = FunctionRegistry.get(State.PERFORMER, 'on_error')
        #     func[0]()
        #     Robot.next_state = State.FINISHER
        # else:
        #     FunctionRegistry.register(State.PERFORMER, 'on_error', self)