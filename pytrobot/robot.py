from typing import List
from .state import Enum
"""
"""
# __all__ = ["Robot", "go_next_state", "create_instance_for_state"]


class Robot:
    transaction_number: int = 0
    transaction_item: dict = {}
    transaction_data: List[dict] = []
    """
    Essa classe implementa a estrutura do estado. Ela controla e separa as lógicas 
    e os diversos estados do robô. O controle desses estados é baseado no retorno 'robot.status()'. 
    """

    def __init__(self):
        self._status = False
        self._current_state = None
        self._next_state = None

    def __repr__(self) -> str:
        return f'Robot.{self._current_state}'

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, bool):
            self._status = value
        else:
            raise ValueError(
                "The status value must be a Boolean (True or False).")

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, value):
        from .state import State
        if isinstance(value, State):
            self._current_state = value
        else:
            raise ValueError(
                "The current_state value must be a member of the State enumeration.")

    @property
    def next_state(self):
        return self._next_state

    @next_state.setter
    def next_state(self, value):
        from .state import State
        if isinstance(value, State):
            self._next_state = value
        else:
            raise ValueError(
                "The next_state value must be a member of the State enumeration.")

    # def set_next_state(self, next_state):
    #     """
    #     Esse método faz parte da tentativa de implementar uma forma mais elegante
    #     de interagir com os 'state'.
    #     """

    #     if next_state is None:
    #         print("Escolha um estado válido:")
    #         for estado in State:
    #             print(f"- {estado.name}: {estado.value}")
    #     elif isinstance(next_state, State):
    #         self.next_state = next_state
    #     else:
    #         raise ValueError("O estado deve ser do tipo State Enum.")

    def execute(self):
        """
        Executa a lógica principal do estado atual do robô. Deve ser implementado em cada subclasse.

        :return: Retorna o estado do robô após a execução da lógica.
        """
        pass

    def on_error(self):
        """
        Método invocado quando a execução do estado atual retorna 'False', indicando um erro.
        Deve implementar as tratativas de erro adequadas.

        :return: Retorna o próximo estado planejado após o tratamento de erro.
        """
        pass

    def on_exit(self):
        """
        Método invocado quando a execução do estado atual retorna 'True', indicando sucesso.
        Pode implementar ações de limpeza ou transição para o próximo estado.

        :return: Retorna o próximo estado planejado após a conclusão com sucesso.
        """
        pass

    def on_entry(self):
        """
        Primeiro método invocado ao entrar em qualquer estado. Pode ser usado para inicializações e acessos ao config.

        :return: Retorna o estado do robô após a inicialização.
        """
        pass


# class State(Enum):
#     DEFAULT = None
#     STARTER = 'Starter'
#     HANDLER = 'Handler'
#     DISPATCHER = 'Dispatcher'
#     PERFORMER = 'Performer'
#     FINISHER = 'Finisher'

# def create_instance_for_state(state):

#     from .starter import Starter
#     from .handler import Handler
#     from .dispatcher import Dispatcher
#     from .performer import Performer
#     from .finisher import Finisher


#     if state == State.STARTER:
#         return Starter()
#     elif state == State.HANDLER:
#         return Handler()
#     elif state == State.DISPATCHER:
#         return Dispatcher()
#     elif state == State.PERFORMER:
#         return Performer()
#     elif state == State.FINISHER:
#         return Finisher()
#     else:
#         raise ValueError("Invalid state.")

# def go_next_state(next_state):
#     if next_state:
#         instance = create_instance_for_state(next_state)
#         # Aqui você pode fazer algo com a instância criada
#         return instance
#     else:
#         raise ValueError("Next state is not set.")
