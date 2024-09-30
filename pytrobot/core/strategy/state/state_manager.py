# pytrobot/core/strategy/state/state_manager.py

from pytrobot.core.strategy.state.state_registry import StateRegistry
from pytrobot.core.strategy.state.base_state import BaseState

class StateTransitionError(Exception):
    pass


class StateManager():

    def __init__(self, state_registry: StateRegistry):

        # Atualiza a referência do operador no StateRegistry
        self._state_registry: StateRegistry = state_registry
        self._state_registry.update_state_operator(self.state_machine_operator)
        
        # Define o estado inicial corretamente, usando o StateRegistry
        starter_state_info = self._state_registry.get_state_info('_StarterState')
        self._current_state = starter_state_info['instance'] if starter_state_info else None

        self._next_state_on_success: BaseState
        self._next_state_on_failure: BaseState

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

    def evaluate_next_state(self):

        if self._current_state is None:
            raise StateTransitionError("There is no current state defined.")

        current_state_name = self._current_state.__class__.__name__
        state_info = self._state_registry.get_state_info(current_state_name)
        
        if not state_info:
            raise StateTransitionError(f"No registration defined for state {current_state_name}")
        elif not state_info['success_state']:
            raise StateTransitionError(f"No 'success_state' defined for state {current_state_name}")
        elif not state_info['failure_state']:
            raise StateTransitionError(f"No 'failure_state' defined for state {current_state_name}")
        
        # Obtém diretamente as instâncias dos estados de sucesso e falha usando os nomes armazenados
        success_state_name = state_info['success_state']
        failure_state_name = state_info['failure_state']

        success_state_info = self._state_registry.get_state_info(success_state_name)
        if success_state_info is None: raise StateTransitionError(f"Success {success_state_name} state not found.")

        failure_state_info = self._state_registry.get_state_info(failure_state_name)
        if failure_state_info is None: raise StateTransitionError(f"Failure {failure_state_name} state not found.")

        if success_state_info and failure_state_info:
            self._next_state_on_success = success_state_info['instance']
            self._next_state_on_failure = failure_state_info['instance']
        else:
            raise StateTransitionError("Success or failure state instance not found.")

    def state_machine_operator(self, on_success=None, on_failure=None):

        if on_success:
            success_state_info = self._state_registry.get_state_info(on_success)
            if success_state_info:
                self._next_state_on_success = success_state_info['instance']
            else:
                raise StateTransitionError(f"State information for '{on_success}' not found in TrueTable for success transition.")

        if on_failure:
            failure_state_info = self._state_registry.get_state_info(on_failure)
            if failure_state_info:
                self._next_state_on_failure = failure_state_info['instance']
            else:
                raise StateTransitionError(f"State information for '{on_failure}' not found in TrueTable for failure transition.")
    
    """ NOTE
    This is the state machine. Be careful when changing things here.
    """

    def run(self):

        while self.current_state is not None:
            
            self.evaluate_next_state()

            try:
                self.current_state._on_entry()
                self.current_state._execute()
                self.current_state._on_exit()
                self._current_state = self.next_state_on_success
            except Exception as e:
                # TODO : Implementar o retry
                self.current_state._on_error(e)
                self._current_state = self.next_state_on_failure
