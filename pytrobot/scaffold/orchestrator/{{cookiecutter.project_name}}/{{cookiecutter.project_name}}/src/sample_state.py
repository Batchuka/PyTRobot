from pytrobot import State, First, BaseState, TransactionData

# @First            → Will set this state as the first in StateMachine
# TransactionData() → This class will save the transaction data


@State('StateOnSucess', 'StateOnFailure')
class SampleState(BaseState):
    """
    Read docstrings
    """

    def on_entry(self):

        pass

    def execute(self):

        pass

    def on_exit(self):

        pass

    def on_error(self, error):

        pass
