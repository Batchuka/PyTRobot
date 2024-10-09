# pytrobot/core/decortador/sqs.py

from typing import Any, Type
from pytrobot.core.strategy.sqs.registry import SQSRegistry


def SQS(thread: bool = False):
    """
    Decorator that registers the class as a worker for SQS with an option
    to execute in a new thread or not.

    :param thread: Boolean indicating if the task should run in a separate thread.
    """
    def decorator(cls: Type[Any]) -> Any:
        task_name = f'{cls.__module__}.{cls.__name__}'
        task_registry = SQSRegistry()  # Obtém a instância do TaskRegistry (singleton)

        # Store thread preference as a class attribute
        cls.run_in_thread = thread
        
        # Registra a task no TaskRegistry
        task_registry.register(task_name, cls)  # Registra o nome da task e a classe

        return cls  # Retorna a classe sem modificá-la

    return decorator