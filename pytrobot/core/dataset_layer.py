# pytrobot/core/dataset_layer/dataset.py

import os
import importlib.util
import boto3
from pytrobot.core.singleton import Singleton
from typing import List

class ConfigData(metaclass=Singleton):
    def __init__(self):
        self.config = {}

    def load_config(self, resources_path):
        """Carrega as configurações do arquivo 'config.py' localizado no diretório 'resources' especificado."""
        config_path = os.path.join(resources_path, 'config.py')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Arquivo de configuração não encontrado em: {config_path}")

        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec) # type: ignore
        spec.loader.exec_module(config) # type: ignore

        # Carrega as configurações do módulo 'config' para o dicionário 'config'
        for attr in dir(config):
            if attr.isupper():
                self.config[attr] = getattr(config, attr)

    def load_assets_from_config(self, config_module_path, env):
        try:
            config_module = __import__(config_module_path, fromlist=[env])
            env_config = getattr(config_module, env, {})
            for key, value in env_config.items():
                self.config[key.lower()] = value
        except ModuleNotFoundError:
            raise FileNotFoundError(f"Configuration module '{config_module_path}' not found.")
        except AttributeError:
            raise ValueError(f"Environment '{env}' not found in the configuration module.")

    def load_assets_from_ssm(self):
        
        ssm_client = boto3.client('ssm')
        for key in self.config:
            parameter_name = key.replace("_", "/")
            try:
                response = ssm_client.get_parameter(
                    Name=parameter_name,
                    WithDecryption=True
                )
                parameter_value = response['Parameter']['Value']
                self.config[key] = parameter_value
                print(f"The value of parameter {parameter_name} is: {parameter_value}")

            except ssm_client.exceptions.ParameterNotFound:
                print(f"The parameter {parameter_name} was not found.")
            except Exception as e:
                print(f"An error occurred while fetching parameter {parameter_name}: {str(e)}")

    def get_asset(self, name):
        return self.config.get(name, None)

    def set_asset(self, name, value):

        if name in self.config:
            print(f"The value of '{name}' has been updated in the config.")
        else:
            print(f"The name '{name}' was modified in the config.")
        self.config[name] = value

class TransactionItem:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getitem__(self, key):
        """Permite o acesso a atributos usando item['key']"""
        return getattr(self, key, None)

    def __setitem__(self, key, value):
        """Permite a modificação de atributos usando item['key'] = value"""
        setattr(self, key, value)

    def update(self, **kwargs):
        """Método para atualizar os valores das colunas."""
        for key, value in kwargs.items():
            self[key] = value  # Usando __setitem__ internamente

    def __repr__(self):
        """Método para representar o objeto como string (útil para depuração)."""
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

class TransactionData(metaclass=Singleton):

    def __init__(self, columns):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.columns = columns
            self.items : List[TransactionItem] = []
            self.transaction_number = 0
            self.transaction_item = None

    def __iter__(self):
        return iter(self.items)

    def add_item(self, **kwargs):
        if any(item[self.columns[0]] == kwargs.get(self.columns[0], None) for item in self.items):
            raise ValueError(f"An item with the same {self.columns[0]} already exists.")
        item = TransactionItem(**kwargs)
        self.items.append(item)
        if self.transaction_item is None:
            self.transaction_item = item

    def get_item(self, id):
        for item in self.items:
            if item[self.columns[0]] == id:
                return item
        return None

    def update_item(self, id, **kwargs):
        item = self.get_item(id)
        if item is not None:
            item.update(**kwargs)
        else:
            raise ValueError(f"Item with {self.columns[0]} '{id}' not found.")

    def get_next_item(self):

        self.transaction_number += 1
        if self.transaction_number <= len(self.items):
            self.transaction_item = self.items[self.transaction_number - 1]
            return self.transaction_item
        else:
            self.transaction_number = 0
            self.transaction_item = None
            return None

