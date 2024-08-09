# pytrobot/core/decortador/state.py
from pytrobot.core.strategy.state.state_machine import TrueTable

def State(next_state_on_success, next_state_on_failure='_FinisherState'):
    """
    Decorator that registers the class as a state
    """
    def decorator(cls):
        TrueTable().add_transition(cls, next_state_on_success, next_state_on_failure)
        return cls
    return decorator

def First(cls):
    """
    Decorator that sets state to first.
    """
    TrueTable()._first_state_name = cls.__name__
    return cls
