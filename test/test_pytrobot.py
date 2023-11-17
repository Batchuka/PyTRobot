# teste framework
from framework import *


def test_framework():

    Config.load_config()
    Config.set_config()

    # Exemplo de uso
    items_to_process = [{"item_id": 1}, {"item_id": 2}, {"item_id": 3}]
    Transaction.start_transaction(items_to_process)

    while not Transaction.is_last_transaction():
        Transaction.process_item()
