from enum import Enum
from typing import List, Optional
import logging
import configparser
import inspect
import os


class Environment(Enum):
    DEV = 'DEV.properties'
    HML = 'HML.properties'
    OPS = 'OPS.properties'


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
                print("Item processado:", Transaction.item)
                if Transaction.number == 0:
                    print("Todos os itens foram processados.")
            else:
                print("Todos os itens foram processados.")
        else:
            print("Nenhum item para processar.")

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


class Inventory:
    config: dict = {}

    @staticmethod
    def load_config():
        """
        Carrega e filtra as configurações de um arquivo .properties.

        O método procura um arquivo .properties no diretório do arquivo .py que o invocou
        e lê as configurações relevantes para a seção 'robot' do arquivo. Ele retorna um
        dicionário com as configurações filtradas.

        :return: Um dicionário contendo as configurações relevantes para a seção 'robot'.
        :raises FileNotFoundError: Se nenhum arquivo .properties for encontrado no diretório.
        """

        # Obter o diretório do arquivo .py que invocou a função
        calling_directory = inspect.stack()[2].filename
        calling_directory = os.path.dirname(calling_directory)

        # Procurar o primeiro arquivo .properties no diretório
        for file_name in os.listdir(calling_directory):
            if file_name.endswith(".properties"):
                config_file = os.path.join(calling_directory, file_name)
                break
        else:
            raise FileNotFoundError(
                "Nenhum arquivo .properties encontrado no diretório do arquivo .py.")

        config = configparser.ConfigParser()
        config.read(config_file)

        # Filtrar as configurações relevantes para make_database
        filtered_config = {}
        boolean_mapping = {"true": True, "false": False}
        for key in config['robot']:
            value = config.get('robot', key)
            value_lower = value.lower()
            if value_lower in boolean_mapping:
                # Corrigir: uso de "=" em vez de ":"
                filtered_config[key] = boolean_mapping[value_lower]
            else:
                # Corrigir: uso de "=" em vez de ":"
                filtered_config[key] = value

        Inventory.config = filtered_config

    @staticmethod
    def set_config():
        """
        Configura as opções de logging com base nas configurações fornecidas.

        O método configura o nível de logging para INFO e o formato padrão. Se a opção
        'debugger_mode' estiver definida como True nas configurações fornecidas, o método
        também configura o nível de logging para DEBUG e salva logs em 'temp/robot.log'.

        :param config: Um dicionário contendo as configurações, incluindo 'debugger_mode'.
        """

        # Configuração básica do logging
        logging.basicConfig(level=logging.INFO)

        if Inventory.config['debugger_mode']:

            # Salvar log e trazer level DEBUG
            logging.basicConfig(filename='temp/robot.log', level=logging.DEBUG)

        # Criar um objeto de formatação de log personalizado
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)

        # Definir o formato de data e hora para exibir apenas hora e minutos
        formatter.datefmt = '%H:%M'

        # Aplicar o formato de log personalizado ao logger padrão
        logging.getLogger().handlers[0].setFormatter(formatter)


if __name__ == '__main__':

    Inventory.load_config()
    Inventory.set_config()

    # Exemplo de uso
    items_to_process = [{"item_id": 1}, {"item_id": 2}, {"item_id": 3}]
    Transaction.start_transaction(items_to_process)

    while not Transaction.is_last_transaction():
        Transaction.process_item()
        # logging.INFO(Transaction.get_current_item())
