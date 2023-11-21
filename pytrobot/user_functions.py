try:
    from .state import State
except ImportError:
    from state import State

class FunctionRegistry:
    _functions = {state: {'on_entry': [], 'execute': [], 'on_exit': [], 'on_error': []} for state in State}

    @classmethod
    def register(cls, state, function_type, func):
        cls._functions[state][function_type].append(func)

    @classmethod
    def get(cls, state, function_type):
        return cls._functions[state][function_type]