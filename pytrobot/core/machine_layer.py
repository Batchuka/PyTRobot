# pytrobot/core/machine.py
from pytrobot.core.states.starter_state import _StarterState
from pytrobot.core.states.base_state import BaseState

class StateTransitionError(Exception):
    pass

class TrueTable:
    def __init__(self):
        self._transitions = {}  # Dicionário para armazenar as transições

    def add_transition(self, current_state, next_state_on_success, next_state_on_failure):
        self._transitions[current_state] = {'1': next_state_on_success, '0': next_state_on_failure}

    def evaluate_next_state(self, current_state, status):

        if not isinstance(status, bool):
            raise ValueError(f"'status' deve ser um valor booleano, recebido: {type(status)}")

        if current_state in self._transitions:
            return self._transitions[current_state][str(int(status))]
        return None

class StateMachine:
    def __init__(self, access_dataset_layer, access_object_layer, access_machine_layer):
        self.access_dataset_layer = access_dataset_layer
        self.access_object_layer = access_object_layer
        self.access_machine_layer = access_machine_layer
        self.current_state: BaseState = _StarterState()

    def get_next_state(self) -> BaseState:
        status = self.current_state._status
        next_state_name = self.access_machine_layer.evaluate_next_state(self.current_state.__class__.__name__, status)
        if not next_state_name:
            raise StateTransitionError(f"Não foi possível determinar o próximo estado a partir de {self.current_state.__class__.__name__} com status {status}")
        next_state_class = self.access_object_layer._get(next_state_name)["object"]
        if not next_state_class:
            raise StateTransitionError(f"Não foi possível encontrar a classe do estado {next_state_name}")
        next_state_instance = next_state_class(self.access_dataset_layer, self.access_object_layer)
        return next_state_instance

    def reset_current_state(self):
        current_state_name = self.current_state.__class__.__name__
        current_state_class = self.access_object_layer._get(current_state_name)["object"]
        if not current_state_class:
            raise StateTransitionError(f"Não foi possível encontrar a classe do estado {current_state_name} para reiniciar")
        self.current_state = current_state_class(self.access_dataset_layer, self.access_object_layer)
        self.current_state._on_entry()

    """ NOTE
    This is the state machine. Be careful when changing things here.
    """
    def run(self):

        while self.current_state is not None:

            try:
                self.current_state._on_entry()
                self.current_state._execute()
                self.current_state._on_exit()
            except Exception as e:
                self.current_state._on_error(e)
                if self.current_state.reset:
                    continue
            
            self.current_state = self.access_machine_layer.get_next_state()

class AccessMachineLayer:
    def __init__(self, pytrobot_instance):
        self.pytrobot_instance = pytrobot_instance
    
    def get_current_state(self):
        return self.pytrobot_instance.current_state

    def add_transition(self, current_state, next_state_on_success, next_state_on_failure):
        self.pytrobot_instance.true_table.add_transition(current_state, next_state_on_success, next_state_on_failure)

    def evaluate_next_state(self, current_state_name, status):
        return self.pytrobot_instance.true_table.evaluate_next_state(current_state_name, status)
    
    def get_next_state(self):
        return self.pytrobot_instance.state_machine.get_next_state()

    def reset_current_state(self):
        return self.pytrobot_instance.state_machine.reset_current_state()