# pytrobot/__init__.py
import builtins
import warnings
from pytrobot.core.dataset_layer import ConfigData, TransactionData, TransactionItem
from pytrobot.core.machine_layer import StateMachine, TrueTable
from pytrobot.core.singleton import Singleton
from pytrobot.core.utils import print_pytrobot_banner, pytrobot_print
from abc import abstractmethod

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'


class PyTRobotNotInitializedException(Exception):
    """Exceção para ser levantada quando o PyTRobot não está instanciado."""
    pass


class PyTRobot(metaclass=Singleton):
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
        self.state_machine = StateMachine(true_table=TrueTable())
        self._initialized = True

    def _register_core_states(self):

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
            raise PyTRobotNotInitializedException(
                "PyTRobot object is not initialized.")
        return cls._instance

    @classmethod
    def set_first_state(cls, state_name):
        try:
            instance = cls.get_instance()
            instance._first_state_name = state_name
        except PyTRobotNotInitializedException as e:
            warnings.warn(
                str(f"{e} : Your objects will not be registered"), RuntimeWarning)


class BaseState(metaclass=Singleton):
    """
    Base class for all states within the state management system.
    Each state is a Singleton, ensuring that only one instance of each specific state is created and necessary.
    They don't restart, so think about that!

    Attributes:
        state_machine_operator (callable): Is a function that allows some State manipulate the transition on StateMachine Object.
        _status (bool or None): The status of the last running process, True was successful.
        retry_counter (int): Counter for attempting to execute the state.
        reset (bool): Flag to indicate whether the state should be reset after an error — 

    Abstract methods:
        execute: Defines a main state execution logic.
        on_entry: Executed when the state is activated.
        on_exit: Executed when the state completes successfully.
        on_error: Executed when an error occurs during state execution.
    """

    def __str__(self) -> str:
        return f"State {self.__class__.__name__}"

    def __init__(self, state_machine_operator):
        self.state_machine_operator = state_machine_operator
        self._status = None
        self.retry_counter = 3
        self.reset = False

    def transition(self, on_success=None, on_failure=None):
        """
        Allows state instances to programmatically update their transition paths.

        :param on_success: Class name of the next state on success.
        :param on_failure: Class name of the next state on failure.
        """
        # Uses the operator to update the transitions based on provided state names.
        self.state_machine_operator(
            on_success=on_success, on_failure=on_failure)

    @abstractmethod
    def execute(self):
        """
        Define a main logic that the state must execute.
        This method must be implemented by all subclasses.
        """
        pass

    @abstractmethod
    def on_entry(self):
        """
        State preparation logic. It is necessary to consider that this logic can run multiple times.
        This method must be implemented by all subclasses.
        """
        pass

    @abstractmethod
    def on_exit(self):
        """
        Logic that must run every time the state ends successfully.
        This method must be implemented by all subclasses.
        """
        pass

    @abstractmethod
    def on_error(self, error):
        """
        Logic that must be executed to handle the state when an error occurs.
        This method must be implemented by all subclasses.

        Args:
            error (Exception): The exception that was raised.
        """
        pass

    def _execute(self):
        print(
            f"{BLUE} ========== Running 'execute' ========== {self.__class__.__name__} {RESET}")
        method = getattr(self, 'execute', None)
        if method:
            method()
        else:
            raise NotImplementedError(
                "The 'execute' method must be implemented by the subclass.")

    def _on_entry(self):

        print(f"{BLUE} =========== Starting state ============ {self.__class__.__name__} {RESET}")
        method = getattr(self, 'on_entry', None)
        if method:
            method()
        else:
            raise NotImplementedError(
                "The 'on_entry' method must be implemented by the subclass.")

    def _on_exit(self):
        self._status = True
        print(
            f"{BLUE} ============== Success ================ {self.__class__.__name__}  {RESET}")
        method = getattr(self, 'on_exit', None)
        if method:
            method()
        else:
            self._status = False
            raise NotImplementedError(
                "The 'on_exit' method must be implemented by the subclass.")

    def _on_error(self, error):
        self._status = False
        print(f"{RED} ========== Something failed  ========== {self.__class__.__name__} \n {error}{RESET} ")
        method = getattr(self, 'on_error', None)
        if method:
            if self.retry_counter > 0:
                self.retry_counter -= 1
                print(
                    f"Attempt failed. {self.retry_counter} attempts remaining.")
                self.transition(on_failure=self.__class__.__name__)
            else:
                print("Maximum number of attempts reached.")
            return method(error)
        else:
            raise NotImplementedError(
                f"The 'on_error' method must be implemented by the subclass. Error: {error}")


# Decoradores

def State(next_state_on_success=None, next_state_on_failure=None):
    def decorator(cls):
        try:
            instance = PyTRobot.get_instance()
            st = instance.state_machine
            st.add_state_transition(
                cls, next_state_on_success, next_state_on_failure)
        except PyTRobotNotInitializedException as e:
            warnings.warn(
                str(f"{e} : Your objects will not be registered"), RuntimeWarning)
        return cls
    return decorator


def First(cls):
    PyTRobot.set_first_state(cls.__name__)
    return cls


class _FinisherState(BaseState):

    def execute(self):
        pass

    def on_entry(self):
        pass

    def on_exit(self):

        import threading

        # Imprime a contagem de threads ativas antes de sair
        print(f'Active threads count: {threading.active_count()}')
        print('Active threads:', threading.enumerate())

        exit()

    def on_error(self):

        import os
        os._exit(0)


class _StarterState(BaseState):

    def execute(self):
        pass

    def on_entry(self):
        pass

    def on_exit(self):
        pass

    def on_error(self):
        pass
