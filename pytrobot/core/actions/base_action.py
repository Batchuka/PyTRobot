

from abc import ABC, abstractmethod


class BaseAction(ABC):
    """
    Classe abstrata base para todas as ações no PyTRobot.
    """
    def __init__(self, objects_layer, dataset_layer):
        self.objects_layer = objects_layer
        self.dataset_layer = dataset_layer

    def get_tool(self, tool_class):
        return self.objects_layer.get_tool(tool_class)
    
    def get_config_asset(self, asset_name):
        return self.dataset_layer.config_data.get_asset(asset_name)

    @abstractmethod
    def perform(self):
        """
        Método para executar a ação.
        """
        pass

    @abstractmethod
    def on_success(self):
        """
        Método chamado se a ação for bem-sucedida.
        """
        pass

    @abstractmethod
    def on_failure(self, error):
        """
        Método chamado se a ação falhar.
        """
        pass