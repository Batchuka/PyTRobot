# pytrobot/core/decortador/state.py

# from pytrobot.core.strategy.state.true_table import TrueTable
from pytrobot.core.strategy.state.registry import StateRegistry

def State(next_state_on_success='_FinisherState', next_state_on_failure='_FinisherState'):
    """
    Decorator that registers the class as a state
    """
    def decorator(cls):
        StateRegistry().register(cls, next_state_on_success, next_state_on_failure)
        return cls
    return decorator

def First(cls):
    """
    Decorator that sets state to first.
    """
    state_registry = StateRegistry()
    state_registry.first_state_name = cls.__name__  # Use o setter para definir o primeiro estado
    return cls
