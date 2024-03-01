# pytrobot/core/dataset_layer/dataset.py
import os
import importlib.util
import boto3
from pandas import DataFrame


class ConfigData:
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


class TransactionData:
    def __init__(self, name, columns):
        self.__name = name
        self.columns = ['ID'] + columns  # ID é a primeira coluna
        self.data = {column: [] for column in self.columns}  # Dicionário de listas para cada coluna
        self.next_id = 1  # Autoincremento para o ID

    def add_column(self, column_name):
        if column_name in self.data:
            raise ValueError(f"A coluna '{column_name}' já existe.")
        self.data[column_name] = []

    def add_row(self, **kwargs):
        for column in self.columns:
            if column == 'ID':
                self.data[column].append(self.next_id)
                continue
            self.data[column].append(kwargs.get(column, None))
        self.next_id += 1

    def get_column(self, column_name):
        if column_name not in self.data:
            raise ValueError(f"A coluna '{column_name}' não existe.")
        return self.data[column_name]

    def set_column_value(self, column_name, index, value):
        if column_name not in self.data:
            raise ValueError(f"A coluna '{column_name}' não existe.")
        if index >= len(self.data['ID']):
            raise IndexError("O índice está fora do alcance dos dados existentes.")
        self.data[column_name][index] = value

    def get_row(self, index):
        if index >= self.next_id:
            raise IndexError("O índice está fora do alcance dos dados existentes.")
        return {column: self.data[column][index] for column in self.columns}

class AccessDatasetLayer:

    def __init__(self, pytrobot_instance):
        self.pytrobot_instance = pytrobot_instance
        self.tdata_reg = {}

    def get_asset(self, name):
        return self.pytrobot_instance.config_data.get_asset(name)

    def get_config_data(self):
        return self.pytrobot_instance.config_data

    def create_transaction_data(self, name, columns):
        if name in self.tdata_reg:
            raise ValueError(f"TransactionData com o nome '{name}' já existe.")
        tdata = TransactionData(name=name, columns=columns)
        self.tdata_reg[name] = tdata
        return tdata

    def get_transaction_data(self, name):
        if name in self.tdata_reg:
            return self.tdata_reg[name]
        else:
            raise KeyError(f"TransactionData com o nome '{name}' não existe.")