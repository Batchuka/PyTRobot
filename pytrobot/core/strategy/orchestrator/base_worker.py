# pytrobot/core/strategy/orchestrator/base_worker.py

from celery import Task


class BaseWorker(Task):
    abstract = True

    def run(self, *args, **kwargs):
        raise NotImplementedError("O método 'run' deve ser implementado pelo worker.")


# Orchestrator Decorators

def Worker(self, cls):
    task_name = f'{cls.__module__}.{cls.__name__}.run'
    task = self.celery_app.task(name=task_name, base=BaseWorker)(cls().run)
    return task