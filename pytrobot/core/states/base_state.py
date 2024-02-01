from abc import ABC, abstractmethod


class BaseState(ABC):
    def __init__(self, access_object_layer, access_dataset_layer):
        self._status = None,
        self.access_object_layer = access_object_layer
        self.access_dataset_layer = access_dataset_layer

    def get_action(self, action_class):
        return self.access_object_layer.get(action_class)
    
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
    def on_error(self):
        pass
