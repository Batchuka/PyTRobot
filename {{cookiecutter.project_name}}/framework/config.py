from enum import Enum
import importlib
import logging
import json
import inspect
import os


class Environment(Enum):
    DEV = 'DEV.properties'
    HML = 'HML.properties'
    OPS = 'OPS.properties'


class Config:
    PARAMS = {}
    CONSTANTS = {}
    ASSETS = {}

    @staticmethod
    def load_config():
        """
        Carrega e filtra as configurações de um arquivo .config.

        O método procura um arquivo .config no diretório do arquivo .py que o invocou
        e lê as configurações relevantes para as seções correspondentes no arquivo.
        Ele carrega as configurações em um dicionário chamado Config.ASSETS.

        :return: None
        :raises FileNotFoundError: Se nenhum arquivo .config for encontrado no diretório.
        """

        # Obter o diretório do arquivo .py que invocou a função
        calling_directory = inspect.stack()[2].filename
        calling_directory = os.path.dirname(calling_directory)

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

    @staticmethod
    def set_assets():
        """
        Configura os atributos das classes de configuração dos pacotes com base nas configurações globais e de pacotes.

        O método itera sobre as configurações carregadas em Config.ASSETS e configura as classes de configuração
        de cada pacote com os valores correspondentes nas configurações globais e nos pacotes.

        :raises ValueError: Se Config.ASSETS não estiver carregado. Chame load_config() primeiro.
        """

        if Config.ASSETS is None:
            raise ValueError("ASSETS is not loaded. Call load_config() first.")

        for package_name, package_data in Config.ASSETS.items():
            try:
                package_module = importlib.import_module(package_name)
                components = package_name.split('_')
                camel_case = ''.join(x.title() for x in components)
                package_config_class = getattr(
                    package_module, camel_case, None)

                if package_config_class:
                    # Configurar atributos globais
                    for key, value in Config.ASSETS["globals"].items():
                        if hasattr(package_config_class, key):
                            setattr(package_config_class, key, value)
                        else:
                            print(
                                f"Attribute '{key}' not found in '{package_config_class.__name__}'. Skipping...")

                    # Configurar atributos do pacote
                    for key, value in package_data.items():
                        if hasattr(package_config_class, key):
                            setattr(package_config_class, key, value)
                        else:
                            print(
                                f"Attribute '{key}' not found in '{package_config_class.__name__}'. Skipping...")
                else:
                    print(
                        f"Class {camel_case} not found in module {package_name}. Skipping...")

            except ModuleNotFoundError:
                print(f"Module {package_name} not found. Skipping...")

    @staticmethod
    def set_config():

        # Configuração básica do logging
        logging.basicConfig(level=logging.INFO)

        if Config.ASSETS['globals']['debug_mode']:

            # Salvar log e trazer level DEBUG
            # logging.basicConfig(filename='temp/robot.log',level=logging.DEBUG)
            logging.basicConfig(level=logging.DEBUG)
            print("On debug mode.")

        # Criar um objeto de formatação de log personalizado
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)

        # Definir o formato de data e hora para exibir apenas hora e minutos
        formatter.datefmt = '%H:%M'

        # Aplicar o formato de log personalizado ao logger padrão
        logging.getLogger().handlers[0].setFormatter(formatter)


if __name__ == '__main__':

    Config.load_config()
    Config.set_config()
