from .robot import Robot
from .state import State
from .utils import *
from .user_functions import FunctionRegistry

@apply_decorator_to_all_methods(handle_exceptions)
class Handler(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.HANDLER
        self.go_handler: bool = False
        self.go_dispatcher: bool = False
        self.go_performer: bool = False

    def on_entry(self):
        if str(self) == "Robot.State.HANDLER":
            func = FunctionRegistry.get(State.HANDLER, 'on_entry')
            value = func[0]()
            return value
        else:
            FunctionRegistry.register(State.HANDLER, 'on_entry', self)

    def execute(self):

        if str(self) == "Robot.State.HANDLER":
            func = FunctionRegistry.get(State.HANDLER, 'execute')
            value = func[0]()

            # Inicia o dataset da transação se não estiver iniciado
            if Robot.transaction_number == 0:
                Robot.set_transaction_data(value)
                # se o dataset precisar de algum enriquecimento, use 'Dispatcher'
                self.go_dispatcher = True
                return

            # Lógica de obtenção do novo item da transação
            if (Robot.transaction_number <= len(Robot.transaction_data)):
                Robot.get_transaction_item()
                self.go_performer = True

        else:
            FunctionRegistry.register(State.HANDLER, 'execute', self)
        
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
