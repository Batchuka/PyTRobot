from abc import ABC, abstractmethod


class BaseState(ABC):
    def __init__(self, objects_layer):
        self._status = None,
        self.objects_layer = objects_layer

    def get_action(self, action_class):
        return self.objects_layer.get_action(action_class)

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
