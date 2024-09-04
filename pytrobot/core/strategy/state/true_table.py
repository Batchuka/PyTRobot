# pytrobot/core/strategy/state/true_table.py

from pytrobot.core.singleton import Singleton
from pytrobot.core.strategy.state.private_states import _StarterState, _FinisherState

class TrueTable(metaclass=Singleton):
    #TODO: não seria interessante colocar TrueTable em um arquivo a parte?
    
    def __init__(self):
        self._states = {}
        self._first_state_name = None
        self._register_core_states()

    def _register_core_states(self):

        # _StarterState
        if self._first_state_name:
            self.add_transition(_StarterState, self._first_state_name, '_FinisherState')
        else:
            self.add_transition(_StarterState, '_FinisherState', '_FinisherState')
        
        # _FinisherState
        self.add_transition(_FinisherState,'_FinisherState', '_FinisherState')

    def add_transition(self, current_state, next_state_on_success, next_state_on_failure, operator=None):
        # Assegura que as instâncias dos estados são criadas com acesso ao operador
        self._states[current_state.__name__] = {
            'instance': current_state(operator),
            'success_state': next_state_on_success,
            'failure_state': next_state_on_failure
        }

    def get_state_info(self, state_name):
         return self._states.get(state_name)
