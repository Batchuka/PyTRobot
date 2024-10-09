from pytrobot.core.decortador.state import State
from pytrobot.core.strategy.state.base_state import BaseState

@State()
class DeadState(BaseState):
    """The robot died of hunger."""

    def on_entry(self):
        self.logger.info("It was a long wait without pizza...")

    def execute(self):
        self.logger.info('The robot died of hunger.')

    def on_exit(self):
        # Nothing happens after this state, the robot is dead
        pass

    def on_error(self, e):
        # Nothing happens after this state, the robot is dead
        pass