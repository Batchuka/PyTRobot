from abc import ABC, abstractmethod
from enum import Enum

from decorators import apply_decorator_to_all_methods, handle_exceptions

class State(Enum):
    STARTER = 1
    HANDLER = 2
    DISPATCHER = 3
    PERFORMER = 4
    FINISHER = 5

class StateBase(ABC):
    def __init__(self):
        self._status = None

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
    def on_error(self):
        pass

@apply_decorator_to_all_methods(handle_exceptions)
class Starter(StateBase):

    def __init__(self, dir):
        super().__init__()
        self.user_dir = dir

    def on_entry(self):
        pass

    def execute(self):
        pass

    def on_exit(self):
        pass

    def on_error(self):
        pass


@apply_decorator_to_all_methods(handle_exceptions)
class Handler(StateBase):

    def __init__(self):
        super().__init__()


    def on_entry(self):
        pass

    def execute(self):
        pass
        
    def on_exit(self):
        pass

    def on_error(self):
        pass


@apply_decorator_to_all_methods(handle_exceptions)
class Dispatcher(StateBase):

    def __init__(self):
        super().__init__()

    def on_entry(self):
        pass

    def execute(self):
        pass

    def on_exit(self):
        pass

    def on_error(self):
        pass


@apply_decorator_to_all_methods(handle_exceptions)
class Performer(StateBase):

    def __init__(self):
        super().__init__()

    def on_entry(self):
        pass

    def execute(self):
        pass

    def on_exit(self):
        pass


    def on_error(self):
        pass


@apply_decorator_to_all_methods(handle_exceptions)
class Finisher(StateBase):

    def __init__(self):
        super().__init__()
    
    def on_entry(self):
        pass

    def execute(self):
        pass

    def on_exit(self):
        print("I'll be back!")
        exit()

    def on_error(self):
        print("I shit myself!")
        exit()