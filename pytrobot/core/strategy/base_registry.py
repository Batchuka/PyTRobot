from abc import ABC, abstractmethod

class BaseRegistry(ABC):
    """
    Classe base para todos os registries. Define a interface padrão.
    """

    def __init__(self):
        self._items = []

    @abstractmethod
    def register(self, item):
        """Registra um item no registry."""
        pass

    @abstractmethod
    def get_all(self):
        """Retorna todos os itens registrados."""
        pass

    @abstractmethod
    def has_items(self) -> bool:
        """Verifica se há itens registrados."""
        return len(self._items) > 0
