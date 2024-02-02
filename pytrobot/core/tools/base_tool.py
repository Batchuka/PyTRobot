from abc import ABC, abstractmethod

class BaseTool(ABC):

    def __str__(self) -> str:
        return f"Tool {self.__class__.__name__}"

    def __init__(self, access_object_layer, access_dataset_layer):
        self.access_object_layer = access_object_layer
        self.access_dataset_layer = access_dataset_layer
        self._data = None
        self._status = None
        self.create()
    
    def get_asset(self, asset_name):
        return self.access_dataset_layer.config_data.get_asset(asset_name)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
    
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def use(self):
        pass