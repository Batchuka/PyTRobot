from pytrobot.core.strategy.orchestrator.base_worker import BaseWorker



class NewState(BaseWorker):
    """
    Read docstrings of BaseWorker
    """

    def on_entry(self):

        pass

    def execute(self, *args, **kwargs):
        raise NotImplementedError

