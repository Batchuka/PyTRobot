import os
import configparser

import boto3

class Assets:

    @staticmethod
    def load_properties_from_ssm(path=None, env=None):

        # Initialize the AWS Systems Manager Parameter Store client
        ssm_client = boto3.client('ssm')

        # Use the dir() function to get all attributes of the Assets class
        Assets.load_properties_from_file(path, env)

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
    def load_properties_from_file(cls, path=None, env=None):
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
            raise FileNotFoundError("No root directory provided")

        # Procurar o primeiro arquivo .properties no diretório
        for file_name in os.listdir(path):
            if file_name.endswith(".properties"):
                Assets_file = path+".properties" # type:ignore
                break
        else:
            raise FileNotFoundError(".properties file Not found in project root directory.")

        # Ler o arquivo .properties e carregar os atributos da classe Assets
        Assets_parser = configparser.ConfigParser()
        Assets_parser.read(Assets_file)


        for section in Assets_parser.sections():
            for key, value in Assets_parser.items(section):
                # Defina os atributos da classe Assets dinamicamente
                if section == env: setattr(cls, key.lower(), value)
                # else: 
                #     raise ValueError(f"Valor desconhecido para PYTROBOT_ENV: {pytrobot_env}. Deve ser 'DEV' ou 'OPS'.")

    # def encontrar_arquivo():

        # pytrobot_prop = os.getenv("PYTROBOT_PROP")
        # pytrobot_env = os.getenv("PYTROBOT_ENV")

        # if pytrobot_prop == "LOCAL":
        #     # Lógica para ambiente de desenvolvimento
        #     Assets.load_properties_from_file(self.user_dir, pytrobot_env)
        # elif pytrobot_prop == "SSM":
        #     # Lógica para ambiente de operações
        #     Assets.load_properties_from_ssm(self.user_dir, pytrobot_env)
        # else:
        #     raise ValueError(f"Valor desconhecido para PYTROBOT_PROP: {pytrobot_prop}. Deve ser 'LOCAL' ou 'SSM'.")

    #     try:
    #             # Adiciona o caminho à variável de ambiente sys.path
    #             sys.path.insert(0, self.user_dir)

    #             # Obtém o nome do projeto a partir do último componente do caminho
    #             project_name = os.path.basename(self.user_dir)
    #             project_name = project_name.replace("-", "_")  # Substitua caracteres especiais conforme necessário

    #             # Carrega o módulo principal do projeto
    #             user_module = __import__(project_name)

    #         except Exception as e:
    #             print(f"Erro ao carregar o projeto do usuário: {e}")

    #         finally:
    #             # Remove o caminho adicionado para evitar impacto em outros módulos
    #             sys.path.pop(0)

# def find_calling_directory():
#     # Obtém a pilha de chamadas
#     pilha_frames = inspect.stack()[3:]

#     # Itera sobre os frames na pilha
#     for frame in pilha_frames:
        
#         if frame.code_context:
#             import_package = frame.code_context[0]

#         # Verifica se o caminho do arquivo é válido e não é especial
#         if import_package.startswith('from pytrobot import'): #type:ignore
#             # Retorna o diretório do arquivo
#             return os.path.dirname(frame.filename)

#     return None
