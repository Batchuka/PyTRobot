# pytrobot/core/strategy/state/state_registry.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.strategy.base_registry import BaseRegistry
from pytrobot.core.strategy.state.private_states import _StarterState, _FinisherState

class StateRegistry(BaseRegistry, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self._states = {}
        self._first_state_name = None
        self._register_core_states()

    def _register_core_states(self):
        # _StarterState
        if self._first_state_name:
            self.register(_StarterState, self._first_state_name, '_FinisherState')
        else:
            self.register(_StarterState, '_FinisherState', '_FinisherState')

        # _FinisherState
        self.register(_FinisherState, '_FinisherState', '_FinisherState')

    def register(self, current_state, next_state_on_success, next_state_on_failure, operator=None):
        """Adiciona um estado ao registro."""
        self._states[current_state.__name__] = {
            'instance': current_state(operator),
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
