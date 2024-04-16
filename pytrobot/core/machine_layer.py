# pytrobot/core/machine.py

class StateTransitionError(Exception):
    pass

class TrueTable:
    
    def __init__(self):
        self._transitions = {} 

    def add_transition(self, current_state, next_state_on_success, next_state_on_failure):
        self._transitions[current_state] = {'1': next_state_on_success, '0': next_state_on_failure}

    def update_transition(self, current_state, next_state_on_success=None, next_state_on_failure=None):

        if current_state not in self._transitions:
            self._transitions[current_state] = {'1': '_FinisherState', '0': '_FinisherState'}
            print("The state informed doesn't exist. Default '_FinisherState' assigned for success and failure.")
        
        if next_state_on_success is not None:
            self._transitions[current_state]['1'] = next_state_on_success
        
        if next_state_on_failure is not None:
            self._transitions[current_state]['0'] = next_state_on_failure

class StateMachine:

    def __init__(self, true_table):
        from pytrobot.core import BaseState
        from pytrobot.scaffold.src.starter_state import _StarterState

        self._true_table = true_table
        self._current_state : BaseState = _StarterState()
        self._next_state_on_success = None
        self._next_state_on_failure = None

    def evaluate_next_state(self):
        # Acessa a tabela de transições para o estado atual
        if self._current_state is None:
            raise StateTransitionError("Não há estado atual definido.")
        
        current_state_name = self._current_state.__class__.__name__
        transition = self._true_table._transitions.get(current_state_name)

        if not transition:
            raise StateTransitionError(f"Nenhuma transição definida para o estado {current_state_name}")

        # Acessa o nome das classes dos próximos estados de sucesso e falha
        success_state_name = transition['1']
        failure_state_name = transition['0']

        # Converte os nomes dos estados em instâncias de classe do estado
        # Supõe-se que exista alguma função 'get_state_class_by_name' para fazer isso
        self._next_state_on_success = self.get_state_class_by_name(success_state_name)
        self._next_state_on_failure = self.get_state_class_by_name(failure_state_name)

    def get_state_class_by_name(self, state_name):
        # Essa função precisa acessar um registro de classes de estado ou usar alguma lógica para converter nomes em classes
        # Pode-se usar um dicionário mapeando nomes para classes ou importar dinamicamente
        try:
            module = __import__('pytrobot.states', fromlist=[state_name])
            state_class = getattr(module, state_name)
            return state_class()
        except (ImportError, AttributeError) as e:
            raise StateTransitionError(f"Erro ao carregar a classe de estado '{state_name}': {str(e)}")

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

    def set_next_state_on_success(self, state):
        self._next_state_on_success = state

    def set_next_state_on_failure(self, state):
        self._next_state_on_failure = state

    """ NOTE
    This is the state machine. Be careful when changing things here.
    """

    def state_machine_operator(self, state, on_success=False, on_failure=False):
        if on_success: self.set_next_state_on_success(state)
        if on_failure: self.set_next_state_on_failure(state)




    def run(self):

        self.evaluate_next_state()

        while self.current_state is not None:

            try:
                self.current_state._on_entry()
                self.current_state._execute()
                self.current_state._on_exit()
                state = self.next_state_on_success
                self._current_state = state(self)
            except Exception as e:
                self.current_state._on_error(e)
                state = self.next_state_on_failure
                self._current_state = state(self)
