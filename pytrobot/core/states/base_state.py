from abc import ABC, abstractmethod


class BaseState(ABC):
    def __init__(self):
        self._status = None

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def on_entry(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass

    @abstractmethod
    def on_error(self):
        pass
