# pytrobot/core/strategy/celery/task_registry.py
from pytrobot.core.singleton import Singleton

class TaskRegistry(metaclass=Singleton):
    def __init__(self):
        self._tasks = {}  # Dicionário para armazenar tasks {task_name: task_class}

    def register(self, task_name, task_cls):
        """Adiciona uma task ao registro."""
        self._tasks[task_name] = task_cls
        print(f"Task {task_name} registrada.")

    def get_all_tasks(self):
        """Retorna todas as tasks registradas."""
        return self._tasks
