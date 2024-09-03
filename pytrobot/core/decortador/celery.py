# pytrobot/core/decortador/orchestrator.py
from typing import Any, Type
from pytrobot.core.strategy.orchestrator.celery_manager import CeleryManager

def Worker(cls: Type[Any]) -> Any:
    """
    Decorator that registers the class as a worker
    """
    task_name = f'{cls.__module__}.{cls.__name__}.run'
    celery_manager = CeleryManager()
    task = celery_manager.celery_app.task(name=task_name)(cls().run)
    return task


