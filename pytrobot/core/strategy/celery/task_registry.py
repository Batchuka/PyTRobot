# pytrobot/core/strategy/celery/task_registry.py
from pytrobot.core.singleton import Singleton
from pytrobot.core.strategy.base_registry import BaseRegistry

class TaskRegistry(BaseRegistry, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self._tasks = {}  # Dicionário para armazenar tasks {task_name: task_class}

    def register(self, task_name, task_cls):
        """Adiciona uma task ao registro."""
        self._tasks[task_name] = task_cls
        print(f"Task {task_name} registrada.")

    def get_all(self):
        """Retorna todas as tasks registradas."""
        return self._tasks

    def has_items(self) -> bool:
        """Verifica se há tasks registradas."""
        return len(self._tasks) > 0
