# pytrobot/core/machine.py

class StateTransitionError(Exception):
    pass

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class TrueTable(metaclass=Singleton):
    
    def __init__(self):
        self._states = {}

    def add_transition(self, current_state, next_state_on_success, next_state_on_failure, operator=None):
        # Assegura que as instâncias dos estados são criadas com acesso ao operador
        self._states[current_state.__name__] = {
            'instance': current_state(operator),
            'success_state': next_state_on_success,
            'failure_state': next_state_on_failure
        }

    def get_state_info(self, state_name):
        return self._states.get(state_name)

class StateMachine(metaclass=Singleton):

    def __init__(self, true_table):
        from pytrobot.core import BaseState
        from pytrobot.scaffold.src.starter_state import _StarterState

        self._true_table : TrueTable = true_table
        self._current_state : BaseState = _StarterState(self.state_machine_operator)
        self._next_state_on_success : BaseState
        self._next_state_on_failure : BaseState

    def evaluate_next_state(self):

        if self._current_state is None:
            raise StateTransitionError("There is no current state defined.")

        current_state_name = self._current_state.__class__.__name__
        state_info = self._true_table.get_state_info(current_state_name)
        
        if not state_info:
            raise StateTransitionError(f"No registration defined for state {current_state_name}")
        elif not state_info['success_state']:
            raise StateTransitionError(f"No 'success_state' defined for state {current_state_name}")
        elif not state_info['failure_state']:
            raise StateTransitionError(f"No 'failure_state' defined for state {current_state_name}")
        
        success_state_name = state_info['success_state']
        failure_state_name = state_info['failure_state']

        success_info = self._true_table.get_state_info(success_state_name)
        failure_info = self._true_table.get_state_info(failure_state_name)

        self._next_state_on_success = success_info['instance']
        self._next_state_on_failure = failure_info['instance']

    def state_machine_operator(self, state, on_success=False, on_failure=False):
        if on_success:self.next_state_on_success = state
        if on_failure:self.next_state_on_failure = state

    def add_state_transition(self, current_state, next_state_on_success, next_state_on_failure):
        # Quando adicionar estados, passa o operador
        self._true_table.add_transition(current_state, next_state_on_success, next_state_on_failure, self.state_machine_operator)

    @property
    def current_state(self):
        return self._current_state

    @property
    def next_state_on_success(self):
        return self._next_state_on_success

    @next_state_on_success.setter
    def next_state_on_success(self, value):
        self._next_state_on_success = value

    @property
    def next_state_on_failure(self):
        return self._next_state_on_failure

    @next_state_on_failure.setter
    def next_state_on_failure(self, value):
        self._next_state_on_failure = value

    # def set_next_state_on_success(self, state):
    #     self._next_state_on_success = state

    # def set_next_state_on_failure(self, state):
    #     self._next_state_on_failure = state

    """ NOTE
    This is the state machine. Be careful when changing things here.
    """

    def run(self):

        self.evaluate_next_state()

        while self.current_state is not None:

            try:
                self.current_state._on_entry()
                self.current_state._execute()
                self.current_state._on_exit()
                self._current_state = self.next_state_on_success
            except Exception as e:
                self.current_state._on_error(e)
                self._current_state = self.next_state_on_failure
