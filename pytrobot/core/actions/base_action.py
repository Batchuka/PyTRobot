
from abc import ABC, abstractmethod

class BaseAction(ABC):

    def __str__(self) -> str:
        return f"Action {self.__class__.__name__}"

    def __init__(self, access_object_layer, access_dataset_layer):
        self.access_object_layer = access_object_layer
        self.access_dataset_layer = access_dataset_layer

    def get_tool(self, tool_class):
        tool = self.access_object_layer.get(tool_class)
        tool = tool(self.access_object_layer, self.access_dataset_layer)
        return tool
    
    def get_asset(self, asset_name):
        return self.access_dataset_layer.config_data.get_asset(asset_name)

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def on_success(self):
        pass

    @abstractmethod
    def on_failure(self, error):
        pass