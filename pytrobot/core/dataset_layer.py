# pytrobot/core/dataset_layer/dataset.py
from pytrobot.core.data.config_data import ConfigData
from pytrobot.core.data.transaction_data import TransactionData

class DatasetLayer:
    def __init__(self):
        self.data = {}

    def load_data(self, source):
        # Lógica para carregar dados
        pass

    def get_data(self, key):
        # Lógica para acessar os dados
        return self.data.get(key)