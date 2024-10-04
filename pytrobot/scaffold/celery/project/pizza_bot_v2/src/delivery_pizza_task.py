# pytrobot/scaffold/celery/project/pizzeria_bot/src/delivery_pizza_task.py

from pytrobot.core.strategy.celery.base_task import BaseTask
from pytrobot.core.decortador.celery import Task

from .make_pizza_task import MakePizzaTask

@Task
class DeliveryPizzaTask(BaseTask):
    """
    Task to deliver a pizza by scheduling its preparation first.
    """

    def on_entry(self):
        print("Entering DeliveryPizzaTask...")

    def execute(self, *args, **kwargs):
        # Recebe os detalhes da pizza do pedido
        flavor = kwargs.get('flavor')
        slices = kwargs.get('slices')

        print(f"Received order for a {flavor} pizza with {slices} slices.")

        # Aciona a task de preparação da pizza
        MakePizzaTask().apply_async(kwargs={'flavor': flavor, 'slices': slices})