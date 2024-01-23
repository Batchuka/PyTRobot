from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    Classe abstrata base para todas as ferramentas no PyTRobot.
    """

    @abstractmethod
    def use(self):
        """
        Método para usar a ferramenta.
        """
        pass