from enum import Enum
"""
"""


class State(Enum):
    DEFAULT = None
    STARTER = 'Starter'
    HANDLER = 'Handler'
    DISPATCHER = 'Dispatcher'
    PERFORMER = 'Performer'
    FINISHER = 'Finisher'


def create_instance_for_state(state):

    from .starter import Starter
    from .handler import Handler
    from .dispatcher import Dispatcher
    from .performer import Performer
    from .finisher import Finisher

    if state == State.STARTER:
        return Starter()
    elif state == State.HANDLER:
        return Handler()
    elif state == State.DISPATCHER:
        return Dispatcher()
    elif state == State.PERFORMER:
        return Performer()
    elif state == State.FINISHER:
        return Finisher()
    else:
        raise ValueError("Invalid state.")


def go_next_state(next_state):
    if next_state:
        instance = create_instance_for_state(next_state)
        # Aqui você pode fazer algo com a instância criada
        return instance
    else:
        raise ValueError("Next state is not set.")
