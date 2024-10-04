# pytrobot/core/strategy/state/state_registry.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.strategy.base_registry import BaseRegistry
from pytrobot.core.strategy.state.private_states import _StarterState, _FinisherState

class FirstStateNotDefinedException(Exception):
    """Exceção lançada quando o primeiro estado não está definido."""
    def __init__(self, message="The first state name is not defined in the state registry."):
        super().__init__(message)

class StateRegistry(BaseRegistry, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self._states = {}
        self._first_state_name = None
        self._state_machine_operator = None # Inicialmente, define como None. Isso será alterado depois por StateManager

    @property
    def first_state_name(self):
        return self._first_state_name

    @first_state_name.setter
    def first_state_name(self, state_name):
        self._first_state_name = state_name
        self._register_core_states()

    def update_state_operator(self, operator_func):
        """Atualiza o operador de todos os estados registrados."""
        for state_info in self._states.values():
            state_info['instance'].state_machine_operator = operator_func

    def _register_core_states(self):
        # _StarterState
        if self._first_state_name:
            self.register(_StarterState, self._first_state_name, '_FinisherState')
        else:
            raise FirstStateNotDefinedException()

        # _FinisherState
        self.register(_FinisherState, '_FinisherState', '_FinisherState')

    def register(self, current_state, next_state_on_success, next_state_on_failure):
        """Adiciona um estado ao registro."""
        self._states[current_state.__name__] = {
            'instance': current_state(self._state_machine_operator), # Após instancia de StateManager, essa função passa a retornar o operador corretamente
            'success_state': next_state_on_success,
            'failure_state': next_state_on_failure
        }

    def get_all(self):
        """Retorna todos os estados registrados."""
        return self._states

    def get_state_info(self, state_name):
        """Recupera informações de um estado pelo nome."""
        return self._states.get(state_name)

    def has_items(self) -> bool:
        """Verifica se há estados registrados."""
        return len(self._states) > 0
