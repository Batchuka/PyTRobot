from pytrobot.framework.robot import Robot
from pytrobot.framework.state import State
from pytrobot.framework.utils import *
from pytrobot.framework.user_functions import FunctionRegistry

@apply_decorator_to_all_methods(handle_exceptions)
class Finisher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.FINISHER
    
    def on_entry(self):
        pass
        # if str(self) == "Robot.State.FINISHER":
        #     func = FunctionRegistry.get(State.FINISHER, 'on_entry')
        #     value = func[0]()
        #     return value
        # else:
        #     FunctionRegistry.register(State.FINISHER, 'on_entry', self)

    def execute(self):
        delete_all_temp_files()
        # if str(self) == "Robot.State.FINISHER":
        #     func = FunctionRegistry.get(State.FINISHER, 'execute')
        #     func[0]()
        #     delete_all_temp_files()
        # else:
        #     FunctionRegistry.register(State.FINISHER, 'execute', self)

    def on_exit(self):
        print("I'll be back!")
        exit()

    def on_error(self):
        print("I shit myself!")
        exit()