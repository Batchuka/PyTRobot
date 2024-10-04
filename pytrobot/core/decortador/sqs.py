# pytrobot/core/decortador/queue.py

from typing import Any, Type
from pytrobot.core.strategy.sqs.sqs_registry import SQSRegistry


def SQS(cls: Type[Any]) -> Any:
    """
    Decorator that registers the class as a worker
    """
    task_name = f'{cls.__module__}.{cls.__name__}'
    task_registry = SQSRegistry()  # Obtém a instância do TaskRegistry (singleton)
    
    # Registra a task no TaskRegistry
    task_registry.register(task_name, cls)  # Registra o nome da task e a classe

    return cls  # Retorna a classe sem modificá-la