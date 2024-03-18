# pytrobot/core/dataset_layer/dataset.py
import os
import importlib.util
import boto3


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


"""TODO
É possível limpar bastante essa classe usando getter e setter no 'row' e 'column'
"""

class TransactionData:
    def __init__(self, name, columns):
        if not columns:
            raise ValueError("A lista de colunas não pode estar vazia.")
        self.__name = name
        self.columns = columns
        self.data = {column: [] for column in self.columns}

    def __iter__(self):
        num_rows = len(self.data[self.columns[0]])
        for i in range(num_rows):
            yield self.get_row(i)

    def add_column(self, column_name):
        if column_name in self.data:
            raise ValueError(f"A coluna '{column_name}' já existe.")
        self.data[column_name] = []

    def add_row(self, **kwargs):
        # Verifica se o valor na primeira coluna já existe
        first_column_values = self.data[self.columns[0]]
        if kwargs[self.columns[0]] in first_column_values:
            print(f"Aviso: Valor '{kwargs[self.columns[0]]}' na coluna '{self.columns[0]}' já existe e será ignorado.")
            return

        for column in self.columns:
            self.data[column].append(kwargs.get(column, None))

    def get_column(self, column_name):
        if column_name not in self.data:
            raise ValueError(f"A coluna '{column_name}' não existe.")
        return self.data[column_name]

    def get_row(self, index):
        if index >= len(self.data[self.columns[0]]):
            raise IndexError("O índice está fora do alcance dos dados existentes.")
        return {column: self.data[column][index] for column in self.columns}

    def update_row(self, find_by_column, find_value, **kwargs):
        if find_by_column not in self.columns:
            raise ValueError(f"A coluna '{find_by_column}' não existe.")

        try:
            row_index = self.data[find_by_column].index(find_value)
        except ValueError:
            print(f"Valor {find_value} não encontrado na coluna '{find_by_column}'.")
            return

        for column_name, value in kwargs.items():
            if column_name in self.data:
                self.data[column_name][row_index] = value
            else:
                print(f"A coluna '{column_name}' não existe.")

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
            print(f"TransactionData com o nome '{name}' não existe.")
            return None