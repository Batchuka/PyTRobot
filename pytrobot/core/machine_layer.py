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

class StateMachine:
    def __init__(self, access_object_layer, access_machine_layer):
        self.access_object_layer = access_object_layer
        self.access_machine_layer = access_machine_layer
        self.current_state: BaseState = _StarterState()

    def get_next_state(self) -> BaseState:
        status = self.current_state._status
        state_name = self.access_machine_layer.evaluate_next_state(self.current_state.__class__.__name__, status)

        if not state_name:
            raise StateTransitionError(f"Não foi possível determinar o próximo estado a partir de {self.current_state.__class__.__name__} com status {status}")

        next_state_class = self.access_object_layer.get(state_name)
        if not next_state_class:
            raise StateTransitionError(f"Não foi possível encontrar a classe do estado {state_name}")

        # Criar a nova instância do estado
        next_state = next_state_class(self.access_object_layer, self.access_machine_layer)
        return next_state

    def run(self):
        while self.current_state is not None:
            self.current_state.on_entry()

            try:
                self.current_state.execute()
                self.current_state.on_exit()
            except:
                self.current_state.on_error()

            self.current_state = self.get_next_state()

class AccessMachineLayer:
    def __init__(self, pytrobot_instance):
        self.pytrobot_instance = pytrobot_instance
    
    def get_current_state(self):
        return self.pytrobot_instance.current_state

    def add_transition(self, current_state, next_state_on_success, next_state_on_failure):
        self.pytrobot_instance.true_table.add_transition(current_state, next_state_on_success, next_state_on_failure)

    def evaluate_next_state(self, current_state_name, status):
        return self.pytrobot_instance.true_table.evaluate_next_state(current_state_name, status)