# pytrobot/__init__.py

from .starter import Starter
from .dispatcher import Dispatcher
from .performer import Performer
from .handler import Handler
from .finisher import Finisher
from .transaction import Transaction

from .__main__ import run

__all__ = ['Assets','Starter', 'Dispatcher', 'Performer', 'Handler', 'Finisher', 'Transaction']





def print_pytrobot():
    print("  _____        _______          _")
    print(" |  __ \__   _|__   __|        | |     o   _")
    print(" | |__) \ \ / /  | |_ ___  ___ | |__  _|_ | |__")
    print(" |  ___/ \   /   | | V __|/ _ \|  _ \/   \|  __|")
    print(" | |      | |    | |  /  | |_| | |_)( * * ) |")
    print(" |_|      |_|    |_|__|   \___/|____/\---/|_|")
    print(" ____________________________________________")
    print("|____________________________________________|")
    print("  -- Transactional State Robot for Python --")
    print("               Copyright © 2023")
    print("\n\n")

print_pytrobot()

import logging
import builtins

class Logger:
    handle = None

    @staticmethod
    def setup():
        if Logger.handle is None:
            Logger.handle = logging.getLogger('pytrobot')
            Logger.handle.setLevel(
                logging.DEBUG if Assets.debug_mode else logging.INFO) #type:ignore

            formatter = logging.Formatter(
                "%(asctime)s  %(levelname)s  %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            Logger.handle.addHandler(handler)

    @staticmethod
    def log(message, level=logging.INFO):
        Logger.setup()
        Logger.handle.log(level, message)  # type: ignore

def pytrobot_print(*args, **kwargs):
    message = " ".join(map(str, args))
    Logger.log(message, level=kwargs.get('level', logging.INFO))

# Substituir a função print padrão
builtins.print = pytrobot_print




import boto3
import os
import inspect
import configparser

def find_calling_directory():
    # Obtém a pilha de chamadas
    pilha_frames = inspect.stack()[3:]

    # Itera sobre os frames na pilha
    for frame in pilha_frames:
        
        if frame.code_context:
            import_package = frame.code_context[0]

        # Verifica se o caminho do arquivo é válido e não é especial
        if import_package.startswith('from pytrobot import'): #type:ignore
            # Retorna o diretório do arquivo
            return os.path.dirname(frame.filename)

    return None



class Assets:

    @staticmethod
    def load_properties_from_ssm():

        # Initialize the AWS Systems Manager Parameter Store client
        ssm_client = boto3.client('ssm')

        # Use the dir() function to get all attributes of the Assets class
        Assets.load_properties_from_file()

        attributes = vars(Assets)

        for attribute in attributes:
           
            if not attribute.startswith('__') or not isinstance(getattr(Assets, attribute), str):
                continue
            
            
            parameter_name = f'{attribute.replace("_","/")}'

            try:
                # Use the get_parameter method to fetch the parameter's value
                response = ssm_client.get_parameter(
                    Name=parameter_name,
                    WithDecryption=True  # Set to True if the parameter is encrypted and needs decryption
                )

                # The response contains the parameter's value
                parameter_value = response['Parameter']['Value']

                # Set the value as a static class attribute
                setattr(Assets, attribute, parameter_value)
                print(
                    f'The value of parameter {parameter_name} is: {parameter_value}')

            except ssm_client.exceptions.ParameterNotFound:
                print(f'The parameter {parameter_name} was not found.')
            except Exception as e:
                print(
                    f'An error occurred while fetching parameter {parameter_name}: {str(e)}')

    @classmethod
    def load_properties_from_file(cls, path=None):
        """
        Carrega e filtra as Assetsurações de um arquivo .properties.

        O método procura um arquivo .properties no diretório do arquivo .py que o invocou
        e lê as Assetsurações relevantes para os atributos da classe Assets.

        :param path: Caminho opcional para o diretório.
        :return: None
        :raises FileNotFoundError: Se nenhum arquivo .properties for encontrado no diretório.
        """

        # Obter o diretório do arquivo .py que invocou a função
        if path is None:
            calling_directory = find_calling_directory()
        else:
            calling_directory = path

        # Procurar o primeiro arquivo .properties no diretório
        for file_name in os.listdir(calling_directory):
            if file_name.endswith(".properties"):
                Assets_file = os.path.join(calling_directory, file_name) # type:ignore
                break
        else:
            raise FileNotFoundError(
                "Nenhum arquivo .properties encontrado no diretório raiz do projeto.")

        # Ler o arquivo .properties e carregar os atributos da classe Assets
        Assets_parser = configparser.ConfigParser()
        Assets_parser.read(Assets_file)


        for section in Assets_parser.sections():
            for key, value in Assets_parser.items(section):
                # Defina os atributos da classe Assets dinamicamente
                if section == pytrobot_env: setattr(cls, key.lower(), value)
                # else: 
                #     raise ValueError(f"Valor desconhecido para PYTROBOT_ENV: {pytrobot_env}. Deve ser 'DEV' ou 'OPS'.")



pytrobot_prop = os.getenv("PYTROBOT_PROP")
pytrobot_env = os.getenv("PYTROBOT_ENV")
if pytrobot_prop == "LOCAL":
    # Lógica para ambiente de desenvolvimento
    Assets.load_properties_from_file()
elif pytrobot_prop == "SSM":
    # Lógica para ambiente de operações
    Assets.load_properties_from_ssm()
else:
    raise ValueError(f"Valor desconhecido para PYTROBOT_PROP: {pytrobot_prop}. Deve ser 'LOCAL' ou 'SSM'.")
