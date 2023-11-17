import logging
import inspect
import boto3
import json
import os


class Logger:
    handle = None

    @staticmethod
    def setup():

        if Logger.handle is None:
            Logger.handle = logging.getLogger('framework')
            Logger.handle.setLevel(
                logging.DEBUG if Config.debug_mode else logging.INFO)

            # Configura o formato do log
            formatter = logging.Formatter(
                "%(asctime)s  %(levelname)s  %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            Logger.handle.addHandler(handler)

    @staticmethod
    def log(message, level=logging.INFO):
        Logger.handle.log(level, message)  # type: ignore


class Config:
    debug_mode = True
    retry_attempts = 3
    log_level = "info"
    sleep = {
        "medium": "5",
        "large": "10"
    }
    mysql_rpa = ("192.168.1.9", "rpa", "H3ll0_w0R1d", "rpa")

    @staticmethod
    def init_all_settings():
        # Initialize the AWS Systems Manager Parameter Store client
        ssm_client = boto3.client('ssm')

        # Specify the folder in SSM where the parameters are located
        ssm_folder = '/path/to/your/folder/'

        # Use the dir() function to get all attributes of the Config class
        attributes = dir(Config)

        for attribute in attributes:
            # Check if the attribute starts with '__' (internal attributes) or is not a string
            if attribute.startswith('__') or not isinstance(getattr(Config, attribute), str):
                continue

            # Build the full name of the parameter in SSM
            parameter_name = f'{ssm_folder}{attribute}'

            try:
                # Use the get_parameter method to fetch the parameter's value
                response = ssm_client.get_parameter(
                    Name=parameter_name,
                    WithDecryption=True  # Set to True if the parameter is encrypted and needs decryption
                )

                # The response contains the parameter's value
                parameter_value = response['Parameter']['Value']

                # Set the value as a static class attribute
                setattr(Config, attribute, parameter_value)
                print(
                    f'The value of parameter {parameter_name} is: {parameter_value}')

            except ssm_client.exceptions.ParameterNotFound:
                print(f'The parameter {parameter_name} was not found.')
            except Exception as e:
                print(
                    f'An error occurred while fetching parameter {parameter_name}: {str(e)}')

    @staticmethod
    def init_all_settings_local(path=None):
        """
        Carrega e filtra as configurações de um arquivo .config.

        O método procura um arquivo .config no diretório do arquivo .py que o invocou
        e lê as configurações relevantes para as seções correspondentes no arquivo.
        Ele carrega as configurações em um dicionário chamado Config.ASSETS.

        :return: None
        :raises FileNotFoundError: Se nenhum arquivo .config for encontrado no diretório.
        """

        # Obter o diretório do arquivo .py que invocou a função
        if path is None:
            calling_directory = inspect.stack()[2].filename
            calling_directory = os.path.dirname(calling_directory)
        else:
            calling_directory = path

        # Procurar o primeiro arquivo .properties no diretório
        for file_name in os.listdir(calling_directory):
            if file_name.endswith(".config"):
                config_file = os.path.join(calling_directory, file_name)
                break
        else:
            raise FileNotFoundError(
                "Nenhum arquivo .config encontrado no diretório raiz do projeto.")

        # Ler o arquivo e carrega-lo no atributo Config.ASSETS
        with open(config_file, "r") as f:
            config_data = json.load(f)
        Config.ASSETS = config_data


def handle_exceptions(func):
    """
    Um decorator que envolve a função fornecida com tratamento de exceções genéricas.
    Se a função for executada com sucesso, atualiza o status do robô para True. Se ocorrer
    uma exceção, registra um erro e atualiza o status do robô para False.

    :param func: A função a ser decorada.
    """

    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
            self.status = True
        except Exception as e:
            Logger.log(
                f"Error in '{func.__name__}' of the {self.current_state}: {str(e)}", logging.ERROR)
            self.status = False

    return wrapper


def with_logging(func):
    """
    Um decorator que registra a chamada de uma função com informações de depuração.

    :param func: A função a ser decorada.
    """

    def wrapper(self, *args, **kwargs):
        Logger.log(f"{self.current_state}.{func.__name__}", logging.DEBUG)
        func(self, *args, **kwargs)
    return wrapper


def apply_decorator_to_all_methods(decorator):
    """
    Um decorator de classe que aplica um decorator fornecido a todos os métodos da classe.

    :param decorator: O decorator a ser aplicado.
    """

    def class_decorator(cls):
        for name, value in vars(cls).items():
            if callable(value) and not name.startswith("__"):
                setattr(cls, name, decorator(value))
        return cls

    return class_decorator


def delete_all_temp_files():
    """
    Exclui todos os arquivos no diretório temporário, exceto 'placeholder.txt'.
    """

    temp_directory = '/home/seluser/temp'

    # Verifica se o diretório temporário existe
    if os.path.exists(temp_directory) and os.path.isdir(temp_directory):
        # Obtém a lista de arquivos no diretório temporário
        files = os.listdir(temp_directory)

        for file in files:
            # Verifica se o arquivo é diferente de 'placeholder.txt'
            if file != 'placeholder.txt':
                file_path = os.path.join(temp_directory, file)
                # Verifica se o caminho é um arquivo
                if os.path.isfile(file_path):
                    # Exclui o arquivo
                    os.remove(file_path)
                    Logger.log(f"Deleted file: {file_path}")
    else:
        Logger.log(f"Temporary directory '{temp_directory}' not found")
