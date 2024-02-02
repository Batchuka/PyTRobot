from abc import ABC, abstractmethod


class BaseState(ABC):

    def __str__(self) -> str:
        return f"State {self.__class__.__name__}"

    def __init__(self, access_object_layer, access_dataset_layer):
        self.access_object_layer = access_object_layer
        self.access_dataset_layer = access_dataset_layer
        self._status = None

    def get_action(self, action_class):
        action = self.access_object_layer.get(action_class)
        action = action(self.access_object_layer, self.access_dataset_layer)
        return action
    
    def get_config_asset(self, asset_name):
        return self.access_dataset_layer.config_data.get_asset(asset_name)

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
    def on_error(self, error):
        pass
