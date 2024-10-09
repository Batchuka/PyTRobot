import time
from pytrobot.core.decortador.state import State
from pytrobot.core.strategy.state.base_state import BaseState

from .pizza import Pizza

@State('SatisfiedState', 'DeadState')
class EatingState(BaseState):
    """The robot is eating the pizza."""

    def on_entry(self):
        self.logger.info("Finally the pizza arrived. Time to eat!")
        self.pizza = Pizza()

    def execute(self):
        # Comer pizza até que todas as fatias sejam consumidas
        while self.pizza.total_slices != self.pizza.slices_eaten:
            self.pizza.eat_slice()
            self.logger.info(f"I ate a slice of pizza. Total slices eaten: {self.pizza.slices_eaten}")
            time.sleep(1)  # Simula o tempo gasto para comer cada fatia

    def on_exit(self):

        if self.pizza.slices_eaten == 8:
            self.transition(on_success='SatisfiedState')

        elif self.pizza.slices_eaten > 8:
            self.logger.info("I ate too much pizza.")
            self.transition(on_success='DeadState')

        elif self.pizza.slices_eaten < 8:
            self.logger.info("I ran out of pizza but I'm still hungry.")
            self.transition(on_success='DeadState')
        else:
            raise Exception


    def on_error(self, e):
        self.logger.error(f"I choked while eating: {e}")