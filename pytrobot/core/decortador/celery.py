# pytrobot/core/decortador/celery.py

from typing import Any, Type
from pytrobot.core.strategy.celery.task_registry import TaskRegistry


def Task(cls: Type[Any]) -> Any:
    """
    Decorator that registers the class as a worker
    """
    task_name = f'{cls.__module__}.{cls.__name__}'
    task_registry = TaskRegistry()  # Obtém a instância do TaskRegistry (singleton)
    
    # Registra a task no TaskRegistry
    task_registry.register(task_name, cls)  # Registra o nome da task e a classe

    return cls  # Retorna a classe sem modificá-la


