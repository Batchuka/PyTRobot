from config import *
import json
import os
import re
import boto3


def from_environment():

    assets = {}

    # Obter as informações de configuração do ambiente (os.environ)
    assets['<nome do asset>'] = os.environ.get('<nome da variável>')

    return assets


def from_json(file):

    _dict = {}

    # Carregar as informações de configuração de um arquivo JSON
    with open(file, 'r') as f:
        _dict = json.load(f)
        return _dict


def look_for_projects():

    # username = os.getlogin()  # Obtém o nome de usuário atual

    # Cria o caminho completo usando o nome de usuário
    pass


def get_list_projects():
    project_list = []
    pattern = r'^wmt-bot'
    _path_of_projects = str(Bag.assets['path_of_projects'])

    for root, dirs, _ in os.walk(_path_of_projects):
        for dir_name in dirs:
            if re.match(pattern, dir_name):
                project_path = os.path.join(root, dir_name)
                main_path = os.path.join(project_path, "main.py")
                venv_path = os.path.join(project_path, "venv", "bin", "python")

                if os.path.isfile(main_path) and os.path.isfile(venv_path):
                    project_info = {
                        'project_name': dir_name,
                        'main_path': main_path,
                        'venv_path': venv_path
                    }
                    project_list.append(project_info)

    Bag.list_of_projects = project_list


def set_aws_profile():
    Bag.aws_session = boto3.Session(profile_name=Bag.assets['aws_session'])
