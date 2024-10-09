# pytrobot/scaffold/celery/project/pizzeria_bot/src/delivery_pizza_task.py

from pytrobot.core.strategy.sqs.base_task import BaseTask
from pytrobot.core.decortador.sqs import SQS

@SQS()
class DeliveryPizzaTask(BaseTask):
    """
    Task to deliver a pizza by scheduling its preparation first.
    """

    def on_entry(self):
        self.logger.info("Entering DeliveryPizzaTask...")

    def execute(self, *args, **kwargs):
        # Recebe os detalhes da pizza do pedido
        flavor = kwargs.get('flavor')
        slices = kwargs.get('slices')

        self.logger.info(f"Received order for a {flavor} pizza with {slices} slices.")