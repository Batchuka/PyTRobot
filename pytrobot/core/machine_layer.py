# pytrobot/core/machine.py

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

    def update_transition(self, current_state, next_state_on_success=None, next_state_on_failure=None):

        if current_state not in self._transitions:
            self._transitions[current_state] = {'1': '_FinisherState', '0': '_FinisherState'}
            print("The state informed doesn't exist. Default '_FinisherState' assigned for success and failure.")
        
        if next_state_on_success is not None:
            self._transitions[current_state]['1'] = next_state_on_success
        
        if next_state_on_failure is not None:
            self._transitions[current_state]['0'] = next_state_on_failure

class StateMachine:

    def __init__(self, access_dataset_layer, access_objects_layer, access_machine_layer):
        from pytrobot.core import BaseState
        from pytrobot.scaffold.src.starter_state import _StarterState
        self.access_dataset_layer = access_dataset_layer
        self.access_objects_layer = access_objects_layer
        self.access_machine_layer = access_machine_layer
        self.current_state : BaseState = _StarterState()

    def get_next_state(self):
        status = self.current_state._status
        next_state_name = self.access_machine_layer.evaluate_next_state(self.current_state.__class__.__name__, status)
        
        if not next_state_name:
            raise StateTransitionError(f"Não foi possível determinar o próximo estado a partir de {self.current_state.__class__.__name__} com status {status}")
        
        next_state_class = self.access_objects_layer._get(next_state_name)["object"]
        
        if not next_state_class:
            raise StateTransitionError(f"Não foi possível encontrar a classe do estado {next_state_name}")

        next_state_instance = next_state_class(self.access_dataset_layer, self.access_objects_layer, self.access_machine_layer)
        return next_state_instance

    def reset_current_state(self):
        current_state_name = self.current_state.__class__.__name__
        current_state_class = self.access_objects_layer._get(current_state_name)["object"]
        if not current_state_class:
            raise StateTransitionError(f"Não foi possível encontrar a classe do estado {current_state_name} para reiniciar")
        self.current_state = current_state_class(self.access_dataset_layer, self.access_objects_layer)
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
