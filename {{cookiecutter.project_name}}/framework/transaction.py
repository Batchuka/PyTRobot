from typing import List, Optional
import logging
"""
"""
from .config import Config


class Transaction:
    item: dict = {}
    data: List[dict] = []
    number: int = 0

    @staticmethod
    def start_transaction(items: List[dict]):
        """
        Inicia uma nova transação com a lista de itens fornecida.

        :param items: Uma lista de dicionários representando os itens a serem processados na transação.
        """
        Transaction.data = items
        Transaction.number = len(items)
        Transaction.item = {}

    @staticmethod
    def process_item():
        """
        Processa o próximo item na transação.

        Atualiza o contador de itens e o item atual sendo processado.
        Imprime mensagens para indicar o status do processamento.
        """
        if Transaction.number > 0:
            Transaction.number -= 1
            if Transaction.data:
                Transaction.item = Transaction.data.pop(0)
                logging.info("Item processado: %s", Transaction.item)
                if Transaction.number == 0:
                    logging.info("Todos os itens foram processados.")
            else:
                logging.info("Todos os itens foram processados.")
        else:
            logging.info("Nenhum item para processar.")

    @staticmethod
    def get_current_item() -> Optional[dict]:
        """
        Obtém o item atual sendo processado.

        :return: O dicionário representando o item atual ou None se nenhum item estiver sendo processado.
        """
        return Transaction.item if Transaction.item else None

    @staticmethod
    def is_last_transaction() -> bool:
        """
        Verifica se esta é a última transação.

        :return: True se todos os itens foram processados e não há mais itens na fila, False caso contrário.
        """
        return Transaction.number == 0 and not Transaction.data


if __name__ == '__main__':

    Config.load_configuration()
    Config.set_assets()

    # Exemplo de uso
    items_to_process = [{"item_id": 1}, {"item_id": 2}, {"item_id": 3}]
    Transaction.start_transaction(items_to_process)

    while not Transaction.is_last_transaction():
        Transaction.process_item()
