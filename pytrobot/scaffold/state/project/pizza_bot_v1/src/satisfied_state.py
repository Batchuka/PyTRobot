from pytrobot.core.decortador.state import State
from pytrobot.core.strategy.state.base_state import BaseState

@State()
class SatisfiedState(BaseState):
    """The robot is satisfied after eating pizza."""

    def on_entry(self):
        self.logger.info("I'm satisfied now. This pizza was delicious!")

    def execute(self):
        self.logger.info("I'm going to take a nap now")

    def on_exit(self):
        self.logger.info("Bye")

    def on_error(self, e):
        self.logger.warning(f"It didn't go down well, I think I'm going to vomit: {e}")