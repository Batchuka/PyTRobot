from typing import Any
from enum import Enum


class State(Enum):
    DEFAULT = None
    STARTER = 'Starter'
    CONTROLLER = 'Controller'
    DISPATCHER = 'Dispatcher'
    PERFORMER = 'Performer'
    FINISHER = 'Finisher'


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
        self.next_state = None

    def __repr__(self) -> str:
        return f'Robot.{self.current_state}'

    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, value):
        if isinstance(value, bool):
            self.status = value
        else:
            raise ValueError(
                "O valor do status deve ser um booleano (True ou False).")

    @property
    def current_state(self):
        return self.current_state

    @current_state.setter
    def current_state(self, value):
        if isinstance(value, State):
            self.current_state = value
        else:
            raise ValueError(
                "O valor do current_state deve ser um membro da enumeração State.")

    @property
    def next_state(self):
        return self.next_state

    @next_state.setter
    def next_state(self, value):
        if isinstance(value, State):
            self.next_state = value
        else:
            raise ValueError(
                "O valor do current_state deve ser um membro da enumeração State.")

    def execute(self):
        """
        Aqui, a lógica principal do estado deve ser executada. Logo, esse método
        reserva espaço para chamar e tratar as lógicas principais.

        - args : <dict>config
        - return : <bool>robot_state
        """
        pass

    def on_error(self):
        """
        Este método é invocado quando robot_state retorna 'False', indicando que o
        Robot.execute() em questão não executou como previsto. Esse método deve
        implementar as tratativas de erro adequadas. Este método invoca 'handle()' e
        somente retorna o que 'handle()' retornar.

        - args : <str>robot_state or <bool>robot_state
        - return : <RobotState>robot — que é o retorno do 'handle()'
        """
        pass

    def on_exit(self):
        """
        Este método é invocado quando robot_state retorna 'True' — ou as strings
        mapeadas para cada estado —, indicando que o Robot.execute() em questão
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
