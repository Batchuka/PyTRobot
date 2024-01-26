from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    Classe abstrata base para todas as ferramentas no PyTRobot.
    """
    def __init__(self):
        self._data = None
        self._status = None

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
    def use(self):
        """
        Método para usar a ferramenta.
        """
        pass