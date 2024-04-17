# pytrobot/__init__.py
import builtins
import warnings
from pytrobot.core.dataset_layer import ConfigData, TransactionData
from pytrobot.core.machine_layer import StateMachine, TrueTable
from pytrobot.core.utils import print_pytrobot_banner, pytrobot_print
from abc import ABC, abstractmethod


RED     = '\033[91m'
GREEN   = '\033[92m'
YELLOW  = '\033[93m'
RESET   = '\033[0m'
BLUE    = '\033[94m'


class PyTRobotNotInitializedException(Exception):
    """Exceção para ser levantada quando o PyTRobot não está instanciado."""
    pass

class PyTRobot:
    """Classe principal do pytrobot, implementada como um Singleton."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PyTRobot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._first_state_name: str = ''
        self._resources: str = ''
        if not hasattr(self, '_initialized'):
            self._initialize()
            
    def _initialize(self):
        print_pytrobot_banner()
        builtins.print = pytrobot_print

        # Inicializa os novos atributos
        self.config_data = ConfigData()
        self.state_machine = StateMachine(true_table = TrueTable())
        self._initialized = True

    def _register_core_states(self):
        from pytrobot.scaffold.src.starter_state import _StarterState
        from pytrobot.scaffold.src.finisher_state import _FinisherState
        State(_StarterState)
        if self._first_state_name:
            State(self._first_state_name, '_FinisherState')(_StarterState)
        else:
            State('_FinisherState', '_FinisherState')(_StarterState)
        State(_FinisherState)
        State('_FinisherState', '_FinisherState')(_FinisherState)

    def start(self):
        self.state_machine.run()

    # Métodos de acesso para os decoradores

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise PyTRobotNotInitializedException("PyTRobot object is not initialized.")
        return cls._instance

    @classmethod
    def set_first_state(cls, state_name):
        try:
            instance = cls.get_instance()
            instance._first_state_name = state_name
        except PyTRobotNotInitializedException as e:
            warnings.warn(str(f"{e} : Your objects will not be registered"), RuntimeWarning)

    # @classmethod
    # def add_transition_on_true_table(cls, current_state_name, next_state_on_success_name, next_state_on_failure_name):
    #     try:
    #         instance = cls.get_instance()
    #         instance.state_machine._true_table.add_transition(current_state_name, next_state_on_success_name, next_state_on_failure_name)
    #         return instance.state_machine._true_table
    #     except PyTRobotNotInitializedException as e:
    #         warnings.warn(str(f"{e} : Your objects will not be registered"), RuntimeWarning)

class BaseState(ABC):

    def __str__(self) -> str:
        return f"State {self.__class__.__name__}"

    def __init__(self, state_machine_operator):
        self.state_machine_operator = state_machine_operator
        self._status = None
        self.retry_counter = 0
        self.reset = False


    def transition(self, current_state, next_state_on_success=True, next_state_on_failure=False):
        """
        Update transition on time.
        
        :param current_state: Current state.
        :param next_state_on_success: Next state on success.
        :param next_state_on_failure: Next state on failure.
        """
        current_state_name = self.__class__.__name__
        self.state_machine_operator(
            current_state=current_state_name,
            next_state_on_success=next_state_on_success,
            next_state_on_failure=next_state_on_failure
        )

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def on_entry(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass

    @abstractmethod
    def on_error(self, error):
        pass

    def _execute(self):
        print(f"{BLUE} ========== Running 'execute' ===== {self.__class__.__name__} {RESET}")
        method = getattr(self, 'execute', None)
        if method:
            method()
        else:
            raise NotImplementedError("The 'execute' method must be implemented by the subclass.")

    def _on_entry(self):

        print(f"{BLUE} ========== Starting state ====== {self.__class__.__name__} {RESET}")
        method = getattr(self, 'on_entry', None)
        if method:
            method()
        else:
            raise NotImplementedError("The 'on_entry' method must be implemented by the subclass.")

    def _on_exit(self):
        self._status = True
        print(f"{BLUE} ========== 'execute' goes right ======== {self.__class__.__name__} {RESET}")
        method = getattr(self, 'on_exit', None)
        if method:
            method()
        else:
            self._status = False
            raise NotImplementedError("The 'on_exit' method must be implemented by the subclass.")

    def _on_error(self, error):
        self._status = False
        print(f"{RED} ========== Something failed ========== {self.__class__.__name__} \n {error}{RESET} ")
        method = getattr(self, 'on_error', None)
        if method:
            if self.retry_counter > 0:
                self.retry_counter -= 1
                print(f"Attempt failed. {self.retry_counter} attempts remaining.")
                self.reset = True
            else:
                print("Maximum number of attempts reached.")
                self.reset = False
            return method(error)
        else:
            raise NotImplementedError(f"The 'on_error' method must be implemented by the subclass. Error: {error}")

# Decoradores

def State(next_state_on_success=None, next_state_on_failure=None):
    def decorator(cls):
        try:
            instance = PyTRobot.get_instance()
            st = instance.state_machine
            st.add_state_transition(cls, next_state_on_success, next_state_on_failure)
        except PyTRobotNotInitializedException as e:
            warnings.warn(str(f"{e} : Your objects will not be registered"), RuntimeWarning)
        return cls
    return decorator

def First(cls):
    PyTRobot.set_first_state(cls.__name__)
    return cls
