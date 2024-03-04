from abc import ABC, abstractmethod

class BaseTool(ABC):

    def __str__(self) -> str:
        return f"Tool {self.__class__.__name__}"

    def __init__(self, access_dataset_layer):
        self.access_dataset_layer = access_dataset_layer
        self._data = None
        self._status = None
        self.initialize()
    
    def get_asset(self, asset_name):
        return self.access_dataset_layer.get_asset(asset_name)

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
    def initialize():
        """
        Use este método para inicializar a classe. Não utilize o '__init__'
        """
        pass