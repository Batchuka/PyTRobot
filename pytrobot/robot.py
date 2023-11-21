try:
    from .state import Enum
    from .state import State
except ImportError:
    from state import Enum
    from state import State

from typing import List
from pandas import DataFrame


class Robot:
    transaction_number: int = 0
    transaction_item: dict = {}
    transaction_data: DataFrame = DataFrame()
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

    @staticmethod
    def set_transaction_data(data):
        """
        Starts the transaction variables of static Robot with the provided list of items. 
        Use this method to make ETL of data to process and set the proper structure for transaction. 
        Note: use 'dispatcher' State do enrich the 'transaction_data' if necessery.

        :param data: some untyped dataset representing the items to be processed in the job.
        """
        Robot.transaction_data = data
        Robot.transaction_number = 1
        Robot.transaction_item = {}

    @staticmethod
    def get_transaction_item():
        """
        Processes the next item in the transaction.
        Updates the item counter and the currently processed item.
        Logs messages to indicate the processing status.

        :return: The dictionary representing the processed item or None if no item is being processed.
        """
        if not Robot.transaction_data.empty:
            number = len(Robot.transaction_data) - Robot.transaction_number
            Robot.transaction_item = Robot.transaction_data.iloc[number].to_dict()
            print(f"Transaction {Robot.transaction_number} | Item {Robot.transaction_item}")
            Robot.transaction_number += 1
            return Robot.transaction_item
        else:
            raise ValueError('No items to process.')    


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
        if isinstance(value, State):
            self._next_state = value
        else:
            raise ValueError(
                "The next_state value must be a member of the State enumeration.")

    def register(self):
        """
        Permite ao usuário definir qual função ele quer que seja executada.

        :return: Retorna o estado do robô após a execução da lógica.
        """
        pass


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
