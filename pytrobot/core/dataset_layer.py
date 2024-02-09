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
        return self.config.get(name.lower(), None)



class TransactionData:
    def __init__(self, columns):
        self.data = DataFrame(columns=columns)
        self.current_index = 0

    def add_row(self, row_values):
        if len(row_values) != len(self.data.columns):
            raise ValueError("Número de valores não corresponde ao número de colunas.")

        self.data.iloc[self.current_index] = row_values
        self.current_index += 1

    def current(self):
        if self.current_index < len(self.data):
            return self.data.iloc[self.current_index]
        else:
            raise IndexError("Index out of range")

    def update(self, updated_item):
        if self.current_index < len(self.data):
            self.data.iloc[self.current_index] = updated_item
        else:
            raise IndexError("Index out of range")

    def next_item(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
        else:
            raise IndexError("No more items in transaction")

    def reset(self):
        self.current_index = 0


class AccessDatasetLayer:
    def __init__(self, pytrobot_instance):
        self.pytrobot_instance = pytrobot_instance

    def get_asset(self, name):
        return self.pytrobot_instance.config_data.get_asset(name)

    def get_config_data(self):
        return self.pytrobot_instance.config_data

    def get_transaction_data(self):
        return self.pytrobot_instance.transaction_data

    def update_transaction_data(self, data):
        self.get_transaction_data().set_data(data)

    def process_next_transaction_item(self):
        return self.get_transaction_data().get_item()

    def update_transaction_item(self, item):
        self.get_transaction_data().update(item)