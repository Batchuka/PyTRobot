from pytrobot.core.decortador.state import State
from pytrobot.core.strategy.state.base_state import BaseState

from .pizza import Pizza

@State('ComendoPizza', 'Satisfeito')
class OrderPizza(BaseState):
    """O robô pede pizza e se prepara para comer."""
    def on_entry(self):
        print("Vou pedir uma pizza...")
        pizza_context.eat_pizza()
    
    def execute(self):
        print(f"Comi um pedaço de pizza. Total comido: {pizza_context.pizza_count}")
        time.sleep(1)  # Simula o tempo de comer pizza

        # Checa se está satisfeito
        if pizza_context.is_satisfied():
            self.transition('Satisfeito')
        else:
            self.transition('ComendoPizza')

    def on_exit(self):
