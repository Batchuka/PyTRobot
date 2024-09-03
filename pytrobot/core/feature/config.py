#pytrobot/core/feature/config.py
import os
import json
from pytrobot.core.singleton import Singleton

class ConfigManager(metaclass=Singleton):
    """
    Classe responsável por carregar e armazenar configurações da aplicação.
    """

    def __init__(self):
        self._config_data = {}

    def load_config(self, directory: str, config_name: str = 'app.json'):
        """
        Carrega as configurações a partir de um arquivo na pasta rsc.
        """
        config_path = os.path.join(directory, 'rsc', config_name)

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file '{config_name}' not found in the rsc directory.")

        with open(config_path, 'r', encoding='utf-8') as config_file:
            self._config_data = json.load(config_file)

    def get_config(self, key: str, default=None):
        keys = key.split('.')
        value = self._config_data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default

        if isinstance(value, dict):
            print(f"Config key '{key}' resolved to a dictionary, expected a value. Returning default.")
            return default

        return value

    def get_all_configs(self):
        return self._config_data
