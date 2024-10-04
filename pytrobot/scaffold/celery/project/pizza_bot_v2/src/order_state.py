from pytrobot.core.decortador.state import State
from pytrobot.core.strategy.state.base_state import BaseState

from .delivery_pizza_task import DeliveryPizzaTask

@State('EatingState', 'DeadState')
class OrderState(BaseState):
    """The robot orders pizza and prepares for the pizza delivery."""

    def on_entry(self):
        print("I'll order a pizza...")

    def execute(self):
        # Coleta dados para a tarefa de entrega
        flavor = input("What flavor of pizza would you like? ")
        slices = int(input("How many slices should the pizza have? (Enter a number): "))

        # Enfileira a tarefa de entrega da pizza com os argumentos necessários
        self.delivery = DeliveryPizzaTask.apply_async(kwargs={"flavor": flavor, "slices": slices})

        print(f"Order placed for a {flavor} pizza with {slices} slices.")

    def on_exit(self):
        print("Pizza order sent to the delivery task.")

    def on_error(self, e):
        print(f"An error occurred while ordering the pizza: {e}")

