from abc import ABC, abstractmethod

class BaseTool(ABC):

    def __str__(self) -> str:
        return f"Tool {self.__class__.__name__}"

    def __init__(self, *args, **kwargs):
        self.initialize(*args, **kwargs)
    
    @abstractmethod
    def initialize(self, *args, **kwargs):
        """
        Use este método para inicializar a classe. Não utilize o '__init__'
        Passe qualquer argumento necessário para a classe aqui.
        """
        pass