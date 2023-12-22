import importlib.util

from pytrobot.robot import Robot
from pytrobot.state import State
from pytrobot.utils import *
from pytrobot.assets import Assets
from pytrobot.user_functions import FunctionRegistry

@apply_decorator_to_all_methods(handle_exceptions)
class Starter(Robot):

    def __init__(self, dir):
        super().__init__()
        self.current_state = State.STARTER
        self.user_dir = dir

    def on_entry(self):

        pytrobot_prop = os.getenv("PYTROBOT_PROP")
        pytrobot_env = os.getenv("PYTROBOT_ENV")
        if pytrobot_prop == "LOCAL":
            # Lógica para ambiente de desenvolvimento
            Assets.load_properties_from_file(self.user_dir, pytrobot_env)
        elif pytrobot_prop == "SSM":
            # Lógica para ambiente de operações
            Assets.load_properties_from_ssm(self.user_dir, pytrobot_env)
        else:
            raise ValueError(f"Valor desconhecido para PYTROBOT_PROP: {pytrobot_prop}. Deve ser 'LOCAL' ou 'SSM'.")

    def execute(self):
        self.user_dir
        pass
        # module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(module)



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

