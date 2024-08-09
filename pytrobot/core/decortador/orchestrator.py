# pytrobot/core/decortador/orchestrator.py
from pytrobot.core.strategy.orchestrator.celery_manager import CeleryManager

def Worker(cls):
    """
    Decorator that registers the class as a worker
    """
    task_name = f'{cls.__module__}.{cls.__name__}.run'
    celery_manager = CeleryManager() #type:ignore
    task = celery_manager.celery_app.task(name=task_name)(cls().run)
    return task


