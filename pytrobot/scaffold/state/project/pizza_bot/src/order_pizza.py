from pytrobot.core.decortador.state import State
from pytrobot.core.strategy.state.base_state import BaseState

# from pytrobot.scaffold.state.project.pizza_bot.src.pizzeria import Pizzeria

from .pizzeria import Pizzeria

@State('EatingPizza', 'Dead')
class OrderPizza(BaseState):
    """The robot orders pizza and gets ready to eat."""

    def on_entry(self):
        print("I'll get the number of the pizzeria...")
        self.pizzaria = Pizzeria()
    
    def execute(self):
        # This method return a 'Pizza' object that is a singleton
        pizza = self.pizzaria.order()

    def on_exit(self):
        pass

    def on_error(self, e):
        pass

