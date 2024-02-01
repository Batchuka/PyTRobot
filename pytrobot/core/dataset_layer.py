# pytrobot/core/dataset_layer/dataset.py
import os
import configparser
import boto3
from pandas import DataFrame


class ConfigData:
    def __init__(self):
        self.config = {}

    def load_config(self, path, env):
        self._load_properties_from_file(path, env)
        self._load_properties_from_ssm()

    def _load_properties_from_file(self, path, env):
        config_file = os.path.join(path, '.config')
        if not os.path.exists(config_file):
            raise FileNotFoundError(f".config file not found in {path}")

        parser = configparser.ConfigParser()
        parser.read(config_file)

        for section in parser.sections():
            if section == env:
                for key, value in parser.items(section):
                    self.config[key.lower()] = value

    def _load_properties_from_ssm(self):
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