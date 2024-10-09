from pytrobot.core.decortador.state import State
from pytrobot.core.strategy.state.base_state import BaseState

from pytrobot.core.strategy.sqs.message_builder import SQSMessageBuilder
from pytrobot.core.strategy.sqs.strategy import SQSStrategy

@State('EatingState', 'DeadState')
class OrderState(BaseState):
    """The robot orders pizza and prepares for the pizza delivery."""

    def on_entry(self):
        self.logger.info("I'll order a pizza...")

    def execute(self):
        # Coleta dados para a tarefa de entrega
        # flavor = input("What flavor of pizza would you like? ")
        # slices = int(input("How many slices should the pizza have? (Enter a number): "))
        flavor = 'frango'
        slices = 6

        # Cria uma mensagem SQS para a tarefa de entrega da pizza
        if flavor and slices:
            message = (
            SQSMessageBuilder(task_name='DeliveryPizzaTask')
            .add_kwargs(flavor=flavor, slices=slices)
            .build()
            )

        # Inicializa o SQSStrategy e seleciona a fila correta
        sqs_strategy = SQSStrategy()
        queue_manager = sqs_strategy.select_queue("wmt-rpa-teste") 

        # Publica a mensagem na fila
        queue_manager.send_message(message)

        self.logger.info(f"Order placed for a {flavor} pizza with {slices} slices.")

    def on_exit(self):
        self.logger.info("Pizza order sent to the delivery task.")

    def on_error(self, e):
        self.logger.error(f"An error occurred while ordering the pizza: {e}")

