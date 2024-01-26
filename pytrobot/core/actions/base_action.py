

from abc import ABC, abstractmethod

class BaseAction(ABC):
    """
    Classe abstrata base para todas as ações no PyTRobot.
    """
    def __init__(self, objects_layer):
        self.objects_layer = objects_layer

    def get_tool(self, tool_class):
        return self.objects_layer.get_tool(tool_class)

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