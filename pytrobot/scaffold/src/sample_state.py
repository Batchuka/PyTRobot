from pytrobot import State, BaseState

# @State
# @Transition('SampleState', 'StateOnSucess', 'StateOnError')
class SampleState(BaseState):
    """
    Um estado inicial de exemplo que pode ser usado como ponto de partida.
    """

    def on_entry(self):
        pass

    def execute(self):
        pass

    def on_exit(self):
        pass

    def on_error(self, error):
        pass