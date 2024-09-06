# pytrobot/core/strategy/state/base_state.py
from abc import abstractmethod
from pytrobot.core.singleton import Singleton
from pytrobot.core.feature.logging import TerminalColor

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
            f"{TerminalColor.BLUE.value} ========== Running 'execute' ========== {self.__class__.__name__} {TerminalColor.RESET.value}")
        method = getattr(self, 'execute', None)
        if method:
            method()
        else:
            raise NotImplementedError(
                "The 'execute' method must be implemented by the subclass.")

    def _on_entry(self):

        print(f"{TerminalColor.BLUE.value} =========== Starting state ============ {self.__class__.__name__} {TerminalColor.RESET.value}")
        method = getattr(self, 'on_entry', None)
        if method:
            method()
        else:
            raise NotImplementedError(
                "The 'on_entry' method must be implemented by the subclass.")

    def _on_exit(self):
        self._status = True
        print(
            f"{TerminalColor.BLUE.value} ============== Success ================ {self.__class__.__name__}  {TerminalColor.RESET.value}")
        method = getattr(self, 'on_exit', None)
        if method:
            method()
        else:
            self._status = False
            raise NotImplementedError(
                "The 'on_exit' method must be implemented by the subclass.")

    def _on_error(self, error):
        self._status = False
        print(f"{TerminalColor.RED.value} ========== Something failed  ========== {self.__class__.__name__} \n {error}{TerminalColor.RESET.value} ")
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
