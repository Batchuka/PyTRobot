from .robot import Robot
from .state import State
from .common import *
"""
imports do framework  ↑
imports do usuário    ↓
"""
from make_database import MysqlDB


@apply_decorator_to_all_methods(handle_exceptions)
class Handler(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.HANDLER
        self.go_handler: bool = False
        self.go_dispatcher: bool = False
        self.go_performer: bool = False

    def on_entry(self):
        # Inicia tudo que precisará para executar a tarefa do Controller
        Logger.log("imagine a instancia de algo para ETL do dataset")

    def execute(self):

        # Inicia o dataset da transação se não estiver iniciado
        if Robot.transaction_number == 0:
            self.get_transaction_data(
                data=[{"ID": 1, "IMPORTANCIA": 300}, {"ID": 2, "IMPORTANCIA": 400}])
            # se o dataset precisar de algum enriquecimento, use 'Dispatcher'
            self.go_dispatcher = True
            return

        # Lógica de obtenção do novo item da transação
        if (Robot.transaction_number <= len(Robot.transaction_data)):
            self.get_transaction_item()
            self.go_performer = True

    def get_transaction_data(self, data):
        """
        Starts the transaction variables of static Robot with the provided list of items. 
        Use this method to make ETL of data to process and set the proper structure for transaction. 
        Note: use 'dispatcher' State do enrich the 'transaction_data' if necessery.

        :param data: some untyped dataset representing the items to be processed in the job.
        """
        Robot.transaction_data = data
        Robot.transaction_number = 1
        Robot.transaction_item = {}

    def get_transaction_item(self):
        """
        Processes the next item in the transaction.
        Updates the item counter and the currently processed item.
        Logs messages to indicate the processing status.

        :return: The dictionary representing the processed item or None if no item is being processed.
        """
        if Robot.transaction_data:
            number = len(Robot.transaction_data) - Robot.transaction_number
            Robot.transaction_item = Robot.transaction_data[number]
            Logger.log(
                f"Transaction {Robot.transaction_number} | Item {Robot.transaction_item}")
            Robot.transaction_number += 1
        else:
            raise ValueError('No items to process.')

    def on_exit(self):
        # utilize as variávels para configurar qual estado seguir
        if self.go_handler:
            self.next_state = State.HANDLER
        elif self.go_performer:
            self.next_state = State.PERFORMER
        elif self.go_dispatcher:
            self.next_state = State.DISPATCHER
        else:
            self.next_state = State.FINISHER

    def on_error(self):
        self.next_state = State.FINISHER
