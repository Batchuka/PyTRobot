from .robot import Robot
from .state import State
from .common import *

class StateFunctionsRegistry:
    _functions = {state: {'on_entry': [], 'execute': [], 'on_exit': [], 'on_error': []} for state in State}

    @classmethod
    def register_function(cls, state, function_type, func):
        cls._functions[state][function_type].append(func)

    @classmethod
    def get_functions(cls, state, function_type):
        return cls._functions[state][function_type]

@apply_decorator_to_all_methods(handle_exceptions)
class Starter(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.STARTER

    @staticmethod
    def on_entry(func):
        StateFunctionsRegistry.register_function(State.STARTER, 'on_entry', func)
        return func

    @staticmethod
    def execute(func):
        StateFunctionsRegistry.register_function(State.STARTER, 'execute', func)
        return func

    @staticmethod
    def on_exit(func):
        StateFunctionsRegistry.register_function(State.STARTER, 'on_exit', func)
        Robot.next_state = State.HANDLER

    @staticmethod
    def on_error(func):
        StateFunctionsRegistry.register_function(State.STARTER, 'on_error', func)
        Robot.next_state = State.FINISHER