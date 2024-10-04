# pytrobot/scaffold/celery/project/pizzeria_bot/src/make_pizza_task.py

from pytrobot.core.strategy.celery.base_task import BaseTask
from pytrobot.core.decortador.celery import Task

from .pizzeria import Pizzeria

@Task
class MakePizzaTask(BaseTask):
    """
    Task to make a pizza and pass it to the next task for delivery.
    """

    def on_entry(self):
        print("Entering MakePizzaTask...")

    def execute(self, *args, **kwargs):
        # Inicializa a pizzaria para receber o pedido
        pizzeria = Pizzeria()
        flavor = kwargs.get('flavor')
        slices = kwargs.get('slices')

        # Faz o pedido da pizza com os argumentos fornecidos
        pizza = pizzeria.order(flavor, slices)

        print(f"Making pizza with flavor {pizza.flavor} and {pizza.total_slices} slices.")
        
        # Envia a tarefa para a entrega, passando a pizza feita
        from .delivery_pizza_task import DeliveryPizzaTask
        DeliveryPizzaTask().apply_async(kwargs={'pizza': pizza.__dict__})

        print("Pizza is ready to be delivered!")