from enum import Enum
import importlib
import logging
import configparser
import inspect
import os


class Environment(Enum):
    DEV = 'DEV.properties'
    HML = 'HML.properties'
    OPS = 'OPS.properties'


class Config:
    GLOBALS = None
    PACKAGES = None

    @staticmethod
    def load_config():
        """
        Carrega e filtra as configurações de um arquivo .properties.

        O método procura um arquivo .properties no diretório do arquivo .py que o invocou
        e lê as configurações relevantes para as seções correspondentes no arquivo.
        Ele retorna dicionários com as configurações filtradas.

        :return: Dicionários contendo as configurações para cada seção.
        :raises FileNotFoundError: Se nenhum arquivo .properties for encontrado no diretório.
        :raises ValueError: Se uma seção no arquivo .properties não corresponder a nenhum dicionário na classe Config.
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

        # Carregar os pacotes do arquivo .properties
        Config.PACKAGES = config.sections()

        # Carregar as configurações globais da seção [global]
        if "global" in config:
            Config.GLOBALS = {}
            for key, value in config["global"].items():
                Config.GLOBALS[key] = value

    @staticmethod
    def set_config():
        """
        Configura os atributos das classes de configuração dos pacotes com base nas configurações globais e de pacotes.

        O método itera sobre os pacotes definidos em Config.PACKAGES e configura as classes de configuração
        de cada pacote com os valores correspondentes nas configurações globais e nos pacotes.
        """

        if Config.GLOBALS is None:
            raise ValueError(
                "GLOBALS is not loaded. Call load_config() first.")

        for package_name in Config.PACKAGES:
            try:
                package_module = importlib.import_module(package_name)
                package_config_class = getattr(
                    package_module, f"{package_name.capitalize()}Config")

                # Configurar atributos globais
                for key, value in Config.GLOBALS.items():
                    if hasattr(package_config_class, key):
                        setattr(package_config_class, key, value)
                    else:
                        print(
                            f"Attribute '{key}' not found in '{package_config_class.__name__}'. Skipping...")

                # Configurar atributos do pacote
                if package_name in Config.__dict__:
                    package_config = Config.__dict__[package_name]
                    for key, value in package_config.items():
                        if hasattr(package_config_class, key):
                            setattr(package_config_class, key, value)
                        else:
                            print(
                                f"Attribute '{key}' not found in '{package_config_class.__name__}'. Skipping...")
                else:
                    raise AttributeError(
                        f"{package_name} not found in Config.")

            except ModuleNotFoundError:
                print(f"Package '{package_name}' not found.")

        # Configuração básica do logging
        logging.basicConfig(level=logging.INFO)

        if Config.config['debugger_mode']:

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

    Config.load_config()
    Config.set_config()
