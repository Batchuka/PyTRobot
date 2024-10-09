# pytrobot/scaffold/celery/project/pizzeria_bot/src/make_pizza_task.py

from pytrobot.core.strategy.sqs.base_task import BaseTask
from pytrobot.core.decortador.sqs import SQS

from .pizzeria import Pizzeria

@SQS()
class MakePizzaTask(BaseTask):
    """
    Task to make a pizza and pass it to the next task for delivery.
    """

    def on_entry(self):
        self.logger.info("Entering MakePizzaTask...")

    def execute(self, *args, **kwargs):
        # Inicializa a pizzaria para receber o pedido
        pizzeria = Pizzeria()
        flavor = kwargs.get('flavor')
        slices = kwargs.get('slices')

        # Faz o pedido da pizza com os argumentos fornecidos
        pizza = pizzeria.order(flavor, slices)

        self.logger.info(f"Done a pizza flavor {pizza.flavor} and {pizza.total_slices} slices.")
