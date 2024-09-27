from pytrobot.core.decortador.state import State, First
from pytrobot.core.strategy.state.base_state import BaseState

from .pizza import Pizza


@First
@State('PedirPizza', 'Morto')
class Hungry(BaseState):
    """Estado inicial: o robô está com fome e quer pizza."""
    def on_entry(self):
        print("Estou com fome! Preciso de pizza.")
    
    def execute(self):
        # Checa se está faminto (tempo limite atingido)
        if pizza_context.is_starved():
            self.transition('Morto')
        else:
            self.transition('PedirPizza')

    def on_exit(self):
        print("Hora de resolver essa fome...")