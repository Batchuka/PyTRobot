import importlib.util
import sys

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
        if self.user_dir:
            try:
                # Adiciona o caminho à variável de ambiente sys.path
                sys.path.insert(0, self.user_dir)

                # Obtém o nome do projeto a partir do último componente do caminho
                project_name = os.path.basename(self.user_dir)
                project_name = project_name.replace("-", "_")  # Substitua caracteres especiais conforme necessário

                # Carrega o módulo principal do projeto
                user_module = __import__(project_name)

            except Exception as e:
                print(f"Erro ao carregar o projeto do usuário: {e}")

            finally:
                # Remove o caminho adicionado para evitar impacto em outros módulos
                sys.path.pop(0)


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

