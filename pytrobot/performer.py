from .robot import Robot
from .state import State
from .common import *
from functools import wraps

@apply_decorator_to_all_methods(handle_exceptions)
class Performer(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.PERFORMER

    @staticmethod
    def on_entry(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print(f"Executing on_entry for function {func.__name__}")
            return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def execute(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print(f"Executing execute for function {func.__name__}")
            return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def on_exit(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print(f"Executing on_exit for function {func.__name__}")
            self.next_state = State.HANDLER
            return func(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def on_error(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print(f"Executing on_error for function {func.__name__}")
            self.next_state = State.FINISHER
            return func(self, *args, **kwargs)
        return wrapper
