from enum import Enum
import inspect

########################## CLASSES DE CONFIGURAÇÔES ###########################


class State(Enum):
    DEFAULT = None
    STARTER = 'Starter'
    CONTROLLER = 'Controller'
    DISPATCHER = 'Dispatcher'
    PERFORMER = 'Performer'
    FINISHER = 'Finisher'


class Environment(Enum):
    DEFAULT = None
    DEV = 'data/DEV-assets.json'
    HML = None
    OPS = 'data/OPS-assets.json'


class Bag:
    assets = None
    transaction_item = {}
    list_of_projects = None
    sqs_client = None
    aws_session = None
    flask_server = None
    debugger_mode = False
    Environment = Environment.DEV
    xvfb = True

########################## SUPER CLASSE ROBOT #################################


class Robot:
    """
    Essa classe implementa a estrutura do estado. Temos cinco métodos, que servem
    para controlar e separar as lógicas e os diversos estados do robô. O controle
    desses estados é baseado no retorno 'robot.status()'. Além disso, temos o dicionário
    config que guarda variáveis de execução desse robô — você pode acessa-las e modifica-
    las em qualquer estados, caso precise.
    """

    def __init__(self):
        self.status = False
        self.current_state = State.DEFAULT
        self.next_state = State.DEFAULT
        if Bag.debugger_mode:
            self.debugger_mode = True
        else:
            self.debugger_mode = False

    def execute(self):
        """
        Aqui, a lógica principal do estado deve ser executada. Logo, esse método
        reserva espaço para chamar e tratar as lógicas principais.
        (1) Start: lógicas de verificação do ambiente;
        (2) Idle: lógicas de Stand-By e comunicação com Orquestrador e Agênte;
        (3) Dispatcher: lógicas de extração, validação e formatação dos dados para o caso de uso;
        (4) Performer: lógicas de execução do caso de uso e;
        (5) Finish: lógicas de finalização do robô no ambiente.

        - args : <dict>config
        - return : <bool>robot_state
        """
        pass

    def handle(self):
        """
        Este método é o responsável por controlar o próximo estado baseado nas variáveis
        internas do contexto.

        - args : <str>robot_state or <bool>robot_state
        - return : <RobotState>robot
        """
        pass

    def on_error(self):
        """
        Este método é invocado quando robot_state retorna 'False', indicando que o
        RobotState.execute() em questão não executou como previsto. Esse método deve
        implementar as tratativas de erro adequadas. Este método invoca 'handle()' e
        somente retorna o que 'handle()' retornar.

        - args : <str>robot_state or <bool>robot_state
        - return : <RobotState>robot — que é o retorno do 'handle()'
        """
        pass

    def on_exit(self):
        """
        Este método é invocado quando robot_state retorna 'True' — ou as strings
        mapeadas para cada estado —, indicando que o RobotState.execute() em questão
        executou como previsto. Este método invoca 'handle()' e somente retorna o que
        'handle()' retornar.

        - args : <str>robot_state or <bool>robot_state
        - return : <RobotState>robot — que é o retorno do 'handle()'
        """
        pass

    def on_entry(self):
        """
        É o primeiro método invocado de qualquer estado e serve para implementar
        lógicas de inicialização do estado. É tipicamente aqui que acessos ao
        config do robô ocorrem.

        - args : <dict>config, <str>robot_state or <bool>robot_state
        - return : <bool>robot_state
        """
        pass

########################## DECORADORES ########################################


def handle(func):

    def wrapper(self, *args, **kwargs):
        try:
            if self.debugger_mode == True:
                print(f"* {self.current_state} > {func.__name__}")
            func(self, *args, **kwargs)
            self.status = True
        except Exception as e:
            print(
                f"Error in '{func.__name__}' of the {self.current_state}: {str(e)}")
            self.status = False

    return wrapper


def fill_arguments_from_bag(func):

    def wrapper(*args, **kwargs):
        # Obtém a assinatura da função
        signature = inspect.signature(func)
        filled_args = []
        filled_kwargs = {}

        # Mapeia os valores posicionais da função original
        for i, param in enumerate(signature.parameters.values()):
            if i < len(args):
                filled_args.append(args[i])
            elif param.name in kwargs:
                filled_kwargs[param.name] = kwargs[param.name]
            else:
                # Verifica se o argumento é None e preenche com valores de Bag.params e Bag.assets
                filled_kwargs[param.name] = kwargs.get(param.name) or Bag.assets.get(
                    param.name) or Bag.assets.get(param.name)

        # Chama a função original com os argumentos preenchidos
        return func(*filled_args, **filled_kwargs)

    return wrapper


def apply_decorator_to_all_methods(decorator):

    def class_decorator(cls):
        for name, value in vars(cls).items():
            if callable(value) and not name.startswith("__"):
                setattr(cls, name, decorator(value))
        return cls

    return class_decorator
