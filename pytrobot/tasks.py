# Conteúdo de tasks.py
import os
import re
import sys
import yaml
import shutil
import subprocess
import glob
import pathlib
import pkg_resources
from pathlib import Path
from cookiecutter.main import cookiecutter


from invoke import task, context, Collection, Program  # type:ignore

def get_project_config(project_path):
    """
    Carrega as configurações do projeto a partir de um arquivo YAML na raiz do diretório especificado.

    :param project_path: Caminho para a raiz do diretório do projeto.
    :return: Um dicionário com as configurações do projeto.
    """
    yaml_file_path = os.path.join(project_path, 'project.yaml')
    try:
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)
            if config is None:
                raise ValueError(
                    "The project.yaml file is empty or has incorrect content.")
            return config
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The project.yaml file was not found at {yaml_file_path}.")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(
            f"An error occurred while parsing the YAML file at {yaml_file_path}: {e}")
    except Exception as e:
        raise Exception(
            f"An unexpected error occurred while loading the project configuration: {e}")



BLUE                    = '\033[94m'
RESET                   = '\033[0m'
IMPORT_PATTERN          = re.compile(r'^\s*(?:import (\S+)|from (\S+?) import)')

CORE_PATH               = os.path.join(os.path.dirname(__file__), "core")
SCAFFOLD_PATH           = os.path.join(os.path.dirname(__file__), 'scaffold')
SAMPLE_STATE_PATH       = os.path.join(SCAFFOLD_PATH, '{{cookiecutter.project_name}}', '{{cookiecutter.project_name}}', 'src', 'sample_state.py')
TEST_SAMPLE_STATE_PATH  = os.path.join(SCAFFOLD_PATH, '{{cookiecutter.project_name}}', 'tests', 'test_sample_state.py')

################### SCAFFOLDS ###################

@task
def testState(c, output_path="."):
    # Converte o caminho relativo em absoluto se necessário
    output_path = os.path.abspath(output_path)
    test_state_path = os.path.join(output_path, 'test_state.py')

    shutil.copy(TEST_SAMPLE_STATE_PATH, test_state_path)
    print(f"New testState created at: {test_state_path}")

@task
def state(c, output_path="."):
    # Converte o caminho relativo em absoluto se necessário
    output_path = os.path.abspath(output_path)
    sample_state_path = os.path.join(output_path, 'sample_state.py')

    shutil.copy(SAMPLE_STATE_PATH, sample_state_path)
    print(f"New state created at: {sample_state_path}")

@task
def new(c, name="", output_path='.'):
    project_name = name if name else input(
        "Please enter the new PyTRobot project name: ")
    version = input(
        "Please enter the new project version (default is 0.1.0): ") or "0.1.0"

    # Converte o caminho relativo em absoluto se necessário
    if output_path == '.':
        output_path = os.getcwd()
    else:
        output_path = os.path.abspath(output_path)

    # Supondo que a criação do projeto ocorra aqui com cookiecutter
    try:
        cookiecutter(
            template=SCAFFOLD_PATH,
            extra_context={'project_name': project_name, 'version': version},
            no_input=True,
            output_dir=output_path
        )

        # Chamada para criar o arquivo YAML após a criação do projeto
        create_project_yaml(output_path, project_name, version)
        print(
            f"Project '{project_name}' created successfully in '{output_path}'.")
    except Exception as e:
        print(f"An error occurred while creating the project: {e}")


################### FILE GENERATION FUNCIONTS ###################

def create_project_yaml(output_dir, PROJECT_NAME, PROJECT_VERSION):

    print(f"{BLUE}========== Creating 'project.yaml' =========={RESET}")
    
    # Construindo os caminhos dinamicamente com base no projeto recém-criado
    project_dir = os.path.join(output_dir, f"{PROJECT_NAME}")
    yaml_content = {
        'project_name': PROJECT_NAME,
        'version': PROJECT_VERSION,
        'project_path': project_dir,
        'package_path': os.path.join(project_dir, PROJECT_NAME),
        'build_path': os.path.join(project_dir, "dist"),
        'aws':{
            'default_region':'replace >> your_default_region',
            'account_id':'replace >> your_account_id',
            'codeartifact_domain':'replace >> your_codeartifact_domain',
            'codeartifact_repository':'replace >> your_codeartifact_repository'
        }
    }


    # Escrevendo o conteúdo no arquivo YAML
    yaml_file_path = os.path.join(project_dir, "project.yaml")
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_content, yaml_file, default_flow_style=False)

    print(f"YAML configuration file created at: {yaml_file_path}")

def create_main_py(output_dir):

    print(f"{BLUE}========== Creating package '__main__.py' =========={RESET}")

    main_content = """
import os
import sys

def main():

    from pytrobot.core.__main__ import entrypoint

    # Defines the current directory as an argument for the entrypoint
    sys.argv = [os.path.abspath(os.path.dirname(__file__))]

    # Invoke probot entrypoint
    entrypoint()

if __name__ == '__main__':
    main()

"""

    # Caminho completo onde o arquivo __main__.py será criado
    main_py_path = os.path.join(output_dir, '__main__.py')

    # Escreve o conteúdo no arquivo __main__.py
    with open(main_py_path, 'w') as main_file:
        main_file.write(main_content)

    print(f"__main__.py file created at: {main_py_path}")

    pass

def create_setup_py(output_dir, PROJECT_NAME, PROJECT_VERSION):

    print(f"{BLUE}========== Creating package 'setup.py' =========={RESET}")

    # Cria um arquivo setup.py do projeto com a configuração do pacote
    setup_path = os.path.join(output_dir, "setup.py")
    requirements_path = os.path.join(output_dir, "requirements.txt")
    with open(setup_path, 'w') as setup_file:
        setup_file.write(
            f"""
from setuptools import setup, find_packages

setup(
    name='{PROJECT_NAME}',
    version='{PROJECT_VERSION}',
    packages=find_packages(),
    include_package_data=True,
    install_requires={open(requirements_path).readlines()},
    entry_points={{
        'console_scripts': [
            '{PROJECT_NAME}-run={PROJECT_NAME}.__main__:main'
        ]
    }},
)
        """
        )
    print(f"setup.py file created in: {setup_path}")

def create_requirements_txt(output_dir, PROJECT_NAME):

    print(f"{BLUE}========== Creating package 'requirements.txt'  =========={RESET}")

    def is_standard_library(name):
        # Retorna True se o módulo for uma biblioteca padrão do Python
        return name in sys.stdlib_module_names

    # Dicionário para armazenar bibliotecas
    libraries = {}

    # Caminho completo para o diretório do projeto
    project_dir = Path(output_dir)

    # Percorre os arquivos do diretório do projeto
    for file in project_dir.rglob('*.py'):
        with open(file, 'r') as f:
            for line in f:
                if line.strip().startswith('#') or not line.strip():
                    continue

                match = IMPORT_PATTERN.search(line)
                if match:
                    lib = match.group(1) or match.group(2)
                    if '.' in lib:
                        lib = lib.split('.')[1]
                    if is_standard_library(lib) or lib == PROJECT_NAME:
                        continue

                    try:
                        version = pkg_resources.get_distribution(lib).version
                        libraries[lib] = version
                    except Exception:
                        print(f"Could not find version for library: {lib}")

    # Escreve as bibliotecas e suas versões no requirements.txt
    requirements_path = project_dir / 'requirements.txt'
    with open(requirements_path, 'w') as req_file:
        for lib, version in libraries.items():
            req_file.write(f"{lib}=={version}\n")

    print(f"requirements.txt file created in: {requirements_path}")

################### AWS ###################

def get_codeartifact_url(ctx, project_path='.'):
    
    try:
        # Carrega as configurações do projeto
        project_config = get_project_config(project_path)

        AWS_ACCOUNT_ID = project_config['aws']['account_id']
        AWS_DEFAULT_REGION = project_config['aws']['default_region']
        CODEARTIFACT_DOMAIN = project_config['aws']['codeartifact_domain']
        CODEARTIFACT_REPOSITORY = project_config['aws']['codeartifact_repository']

        codeartifact_token = get_codeartifact_token(ctx, CODEARTIFACT_DOMAIN, AWS_ACCOUNT_ID)

        # Constrói a URL do CodeArtifact
        pip_index_url = f"https://aws:{codeartifact_token}@{CODEARTIFACT_DOMAIN}-{AWS_ACCOUNT_ID}.d.codeartifact.{AWS_DEFAULT_REGION}.amazonaws.com/pypi/{CODEARTIFACT_REPOSITORY}/simple/"

        return pip_index_url

    except KeyError as e:
        print(f"Missing configuration for CodeArtifact: {e}")
        raise
    except Exception as e:
        print(f"Error retrieving CodeArtifact URL: {e}")
        raise

def get_codeartifact_token(ctx, CODEARTIFACT_DOMAIN, AWS_ACCOUNT_ID):
    """
    Função busca o token de autorização do Code-Artifact
    """
    print(f'\n {BLUE}========== Obtendo Token do CodeArtifact =========={RESET}')
    code_artifact_token = ctx.run(
        f"aws codeartifact get-authorization-token --domain {CODEARTIFACT_DOMAIN} --domain-owner {AWS_ACCOUNT_ID} --query authorizationToken --output text", hide=True).stdout.strip()
    print('\n Feito!')
    return code_artifact_token

################### BUILD ###################

@task
def image(ctx, project_path='.'):
    print(f"{BLUE} =========== Build Docker Image ============ {RESET}")


    try:

        # Determina o diretório base do projeto
        project_path = os.path.abspath(project_path)
        print(f"Building project in: {project_path}")

        project_config = get_project_config(project_path)
        PROJECT_NAME = project_config('project_name')
        PROJECT_VERSION = project_config('project_version')

        # Obtém a URL do CodeArtifact
        pip_index_url = get_codeartifact_url(ctx, project_path)

        # Comando para construir a imagem Docker
        ctx.run(f"docker build -t {PROJECT_NAME} --build-arg PIP_INDEX_URL={pip_index_url} .", echo=True)

        # Colocar comando para fazer tags
        pass

        print('\nFeito!')

    except Exception as e:
        print(f"Error during image generation process: {e}")

@task
def build(ctx, project_path='.'):

    # Determina o diretório base do projeto
    project_path = os.path.abspath(project_path)
    print(f"Building project in: {project_path}")

    try:
        # Supondo que esta função agora recebe o diretório base do projeto
        project_config = get_project_config(project_path)

        PROJECT_NAME    = project_config['project_name']
        PROJECT_PATH    = project_config['project_path']
        PACKAGE_PATH    = project_config['package_path']
        PROJECT_VERSION = project_config['version']

        # Remover pastas de build do python
        remove_previous_build(PROJECT_PATH)

        # Criação do requirements para injetar as dependências adequadas
        create_requirements_txt(PROJECT_PATH, PROJECT_NAME)

        #BUG : Adicionar o auto_import do usuário.
        auto_import_states(PACKAGE_PATH)

        # Criação do setup.py para configurar pacote
        create_setup_py(PROJECT_PATH, PROJECT_NAME, PROJECT_VERSION)

        # Obtém o URL do CodeArtifact
        pip_index_url = get_codeartifact_url(ctx, project_path)

        # Passa o caminho do BUILD e o pip_index_url para a função de construção do pacote
        build_package(PROJECT_PATH, pip_index_url)

        print(f"Build successful for {PROJECT_NAME} version {PROJECT_VERSION}")

    except Exception as e:
        print(f"Error during build process: {e}")

def remove_previous_build(PROJECT_PATH):

    print(f"{BLUE}========== Cleaning up artifacts from old builds =========={RESET}")


    # Files do remove
    files_to_remove = ['requirements.txt', 'setup.py']
    for file_name in files_to_remove:
        file_path = os.path.join(PROJECT_PATH, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed: {file_path}")

    # Folders to remove
    folders_to_remove = ['dist', '*.egg-info']
    for folder_pattern in folders_to_remove:
        # Usando glob para encontrar todos os diretórios que correspondem ao padrão
        for folder in glob.glob(os.path.join(PROJECT_PATH, folder_pattern)):
            if os.path.isdir(folder):
                shutil.rmtree(folder)
                print(f"Removed directory: {folder}")

def build_package(BUILD_PATH, pip_index_url):

    print(f"{BLUE}========== Build package =========={RESET}")

    # Define a variável de ambiente para o índice de pacotes
    env = os.environ.copy()
    env['PIP_INDEX_URL'] = pip_index_url

    # Constrói o pacote usando a ferramenta de build do Python com o índice de pacotes personalizado
    subprocess.run([sys.executable, '-m', 'build', BUILD_PATH], env=env, check=True)


################### UTILS ###################

def auto_import_states(directory):
    """
    Scan the directory for Python files, and automatically writes the necessary imports to the __init__.py file
    for classes decorated with @State.
    """
    src_file_path = pathlib.Path(directory) / 'src'
    init_file_path = pathlib.Path(directory) / 'src' / '__init__.py'

    with open(init_file_path, 'w') as init_file:
        py_files = [f for f in os.listdir(src_file_path) if f.endswith('.py') and f != '__init__.py']
        for py_file in py_files:
            file_path = pathlib.Path(src_file_path) / py_file
            with open(file_path, 'r') as file:
                content = file.readlines()
                for index, line in enumerate(content):
                    if re.match(r'@State', line.strip()):
                        # Find the next class definition after the decorator
                        for class_line in content[index:]:
                            class_match = re.search(r'class (\w+)', class_line)
                            if class_match:
                                class_name = class_match.group(1)  # Capture the class name
                                import_statement = f"from .{py_file[:-3]} import {class_name}\n"
                                init_file.write(import_statement)
                                break  # Exit the inner loop after finding the decorated class
                        break  # Exit the outer loop after processing the current file


if __name__ == '__main__':
    c = context.Context()
    # new(c, output_path='E:\\Projetos')
    # state(c, output_path='/home/seluser/teste_proj/sample_bot/sample/src')
    # testState(c, output_path='/home/seluser/teste_proj/sample_bot/tests')
    build(c, project_path='E:\\Projetos\\wmt_registro_di_bot')
