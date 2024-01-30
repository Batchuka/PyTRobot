# pytrobot/core/machine.py
from pytrobot.core.states.starter_state import _StarterState
from pytrobot.core.states.base_state import BaseState

class StateTransitionError(Exception):
    """Exceção personalizada para erros na transição de estados."""
    pass

class TrueTable:
    def __init__(self):
        self._transitions = {}  # Dicionário para armazenar as transições

    def add_transition(self, current_state, next_state_on_success, next_state_on_failure):
        self._transitions[current_state] = {'1': next_state_on_success, '0': next_state_on_failure}

    def evaluate_next_state(self, current_state, status):
        # Retorna o próximo estado com base no status atual
        if current_state in self._transitions:
            return self._transitions[current_state][str(int(status))]
        return None

class MachineLayer:
    def __init__(self, object_layer, dataset_layer):
        self.object_layer = object_layer
        self.dataset_layer = dataset_layer
        self.true_table = TrueTable()
        self.current_state: BaseState = _StarterState()

    def get_next_state(self, current_state: BaseState) -> BaseState:
        status = self.current_state._status
        state_name = self.true_table.evaluate_next_state(current_state.__class__.__name__, status)

        if not state_name:
            raise StateTransitionError(f"Não foi possível determinar o próximo estado a partir de {current_state.__class__.__name__} com status {status}")

        #TODO: Não existe o método 'create_object' em object_layer
        next_state = self.object_layer.create_object(state_name)
        if not next_state:
            raise StateTransitionError(f"Não foi possível criar o estado {state_name}")

        return next_state
    
    def create_transition(self, current_state_name, next_state_on_success_name, next_state_on_failure_name):
        self.true_table.add_transition(current_state_name, next_state_on_success_name, next_state_on_failure_name)

    def run(self):

        while self.current_state is not None:

            self.current_state.on_entry()

            try:
                self.current_state.execute() 
                self.current_state.on_exit() 

            except:
                self.current_state.on_error()

            self.current_state = self.get_next_state(self.current_state)
