# Conteúdo de tasks.py
import os
import re
import sys
import tomllib
import tomli_w
import shutil
import subprocess
import glob
import pkg_resources
from pathlib import Path
from setuptools_scm import get_version
from cookiecutter.main import cookiecutter


from invoke import task, context, Collection, Program  # type:ignore

def get_project_config(project_path):
    """
    Carrega as configurações do projeto a partir de um arquivo TOML na raiz do diretório especificado.

    :param project_path: Caminho para a raiz do diretório do projeto.
    :return: Um dicionário com as configurações do projeto.
    :raises FileNotFoundError: Se o arquivo pyproject.toml não for encontrado.
    :raises tomllib.TOMLDecodeError: Se o arquivo pyproject.toml não puder ser decodificado.
    """
    pyproject_file_path = os.path.join(project_path, 'pyproject.toml')
    
    if not os.path.exists(pyproject_file_path):
        raise FileNotFoundError(f"pyproject.toml not found in {project_path}")

    with open(pyproject_file_path, 'rb') as pyproject_file:
        try:
            pyproject_content = tomllib.load(pyproject_file)
        except tomllib.TOMLDecodeError as e:
            raise tomllib.TOMLDecodeError(f"Failed to decode pyproject.toml: {e}")
    
    # Obter versão usando setuptools_scm
    scm_version = get_version(root=project_path, relative_to=__file__)

    project_config = {
        'project_name': pyproject_content['project']['name'],
        'project_path': project_path,
        'package_path': os.path.join(project_path, pyproject_content['project']['name']),
        'venv_path': os.path.join(project_path, 'venv'),
        'version': scm_version
    }
    
    return project_config



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

    # Verifica se a versão do Python é 3.12 ou superior
    if sys.version_info < (3, 11):
        print("Python 3.11 or higher is required to create a new project.")
        return

    project_name = name if name else input("Please enter the new PyTRobot project name: ")
    version = input("Please enter the new project version (default is 0.1.0): ") or "0.1.0"

    # Converte o caminho relativo em absoluto se necessário
    output_path = os.path.abspath(output_path) if output_path != '.' else os.getcwd()

    # Supondo que a criação do projeto ocorra aqui com cookiecutter
    try:
        print(f"{BLUE}========== Copying scaffold =========={RESET}")
        cookiecutter(
            template=SCAFFOLD_PATH,
            extra_context={'project_name': project_name, 'version': version},
            no_input=True,
            output_dir=output_path
        )

        project_dir = Path(output_path) / project_name
        venv_dir = project_dir / 'venv'

        print(f"{BLUE}========== Creating 'venv' enviroment =========={RESET}")
        # Criação do ambiente virtual
        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)])

        # Chamada para criar o arquivo pyproject.toml após a criação do projeto
        create_pyproject_toml(project_dir, project_name, version)

        # Instalação do pacote em modo editável
        if sys.platform == 'win32':
            activate_cmd = f"{venv_dir / 'Scripts' / 'activate'} && pip install -e ."
        else:
            activate_cmd = f". {venv_dir / 'bin' / 'activate'} && pip install -e ."

        # print(f"{BLUE}========== Installing project on editable mode =========={RESET}")

        # subprocess.run(activate_cmd, shell=True, cwd=project_dir, executable="/bin/bash")

        print(f"Project '{project_name}' created successfully in '{output_path}'.")
        
    except Exception as e:
        print(f"An error occurred while creating the project: {e}")


################### FILE GENERATION FUNCIONTS ###################

def create_requirements_txt(output_dir, PROJECT_NAME):

    print(f"{BLUE}========== Creating package 'requirements.txt'  =========={RESET}")

    def is_standard_library(name):
        """
        Retorna True se o módulo for uma biblioteca padrão do Python.
        
        Levanta uma exceção se o Python em uso for anterior à versão 3.10,
        pois sys.stdlib_module_names só está disponível a partir do Python 3.10.
        """
        # Primeiro, verifique a versão do Python em execução
        if sys.version_info < (3, 10):
            raise RuntimeError("Pytrobot requires Python 3.10 or higher")
        
        # Se a versão for 3.10 ou superior, prossiga com a verificação
        return name in sys.stdlib_module_names #type:ignore

    # Dicionário para armazenar bibliotecas
    libraries = {}

    # Caminho completo para o diretório do projeto
    project_dir = Path(output_dir)

    # Percorre os arquivos do diretório do projeto
    for file in project_dir.rglob('*.py'):
        if 'venv' in file.parts:
            continue  # Ignora arquivos dentro de 'venv'
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

def create_pyproject_toml(output_dir, project_name, project_version):

    print(f"{BLUE}========== Creating 'pyproject.toml' =========={RESET}")

    # É necessário informar que a ferramenta é poetry mesmo?

    pyproject_content = f"""
[build-system]
requires = [
    "setuptools>=69","wheel>=0.34.2","setuptools_scm[toml]>=8.1.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "{project_version}"
description = "A short description of the project"
authors = [
    {{ name = "Your Name", email = "your.email@example.com" }}
]
dependencies = [
    "pytrobot==3.0.5",
    "boto3==1.26.141",
    "invoke==2.2.0",
    "cookiecutter==2.5.0"
]
readme = "README.md"
requires-python = ">=3.11"

[project.scripts]
{project_name}-run = "{project_name}.__main__:main"

[tool.setuptools_scm]
version_scheme = "post-release"
local_scheme = "dirty-tag"
    """

    pyproject_file_path = os.path.join(output_dir, "pyproject.toml")
    with open(pyproject_file_path, 'w') as pyproject_file:
        pyproject_file.write(pyproject_content)
    
    print(f"pyproject.toml file created at: {pyproject_file_path}")

def filter_stable_versions(dependencies):
    """
    Filtra as dependências para remover sufixos 'dirty' e 'post'.

    :param dependencies: Lista de dependências no formato 'nome==versão'.
    :return: Lista de dependências com apenas versões estáveis.
    """
    stable_dependencies = []
    for dep in dependencies:
        name, version = dep.split('==')
        if 'dirty' not in version and 'post' not in version:
            stable_dependencies.append(dep)
    return stable_dependencies

def update_pyproject_toml(project_path):
    """
    Atualiza o pyproject.toml com as dependências usadas no ambiente virtual especificado.

    :param project_path: Caminho para a raiz do diretório do projeto.
    """
    create_requirements_txt(project_path, Path(project_path).name)

    requirements_path = os.path.join(project_path, 'requirements.txt')
    with open(requirements_path, 'r') as req_file:
        dependencies = req_file.read().splitlines()

    # Filtrar apenas as versões estáveis
    stable_dependencies = filter_stable_versions(dependencies)

    # Formatar dependências para o formato necessário
    formatted_dependencies = [dep.split('==')[0] + '==' + dep.split('==')[1] for dep in stable_dependencies]

    pyproject_file_path = os.path.join(project_path, 'pyproject.toml')
    
    if not os.path.exists(pyproject_file_path):
        raise FileNotFoundError(f"pyproject.toml not found in {project_path}")

    # Ler o arquivo pyproject.toml existente
    with open(pyproject_file_path, 'rb') as pyproject_file:
        pyproject_content = tomllib.load(pyproject_file)

    # Atualizar a seção de dependências no dicionário
    pyproject_content['project']['dependencies'] = formatted_dependencies

    with open(pyproject_file_path, 'wb') as pyproject_file:
        tomli_w.dump(pyproject_content, pyproject_file)

    print(f"pyproject.toml updated with current dependencies of project")

################### AWS ###################


def update_pip_conf():
    """
    TODO : atualizar o pip para ter dois url
    """

    # Obtém o token de autorização do CodeArtifact
    command = [
        'aws', 'codeartifact', 'get-authorization-token',
        '--domain', 'wmt-libraries',
        '--domain-owner', '435062120355',
        '--query', 'authorizationToken',
        '--output', 'text',
        '--region', 'us-east-1'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    token = result.stdout.strip()

    # Caminho para o arquivo pip.conf
    pip_conf_path = os.path.expanduser('~/.config/pip/pip.conf')

    # Conteúdo do pip.conf
    pip_conf_content = f"""
[global]
index-url = https://pypi.org/simple
extra-index-url = https://aws:{token}@wmt-libraries-435062120355.d.codeartifact.us-east-1.amazonaws.com/pypi/wmt-python-repository/simple/
trusted-host =
    pypi.org
    pypi.python.org
    files.pythonhosted.org
    wmt-libraries-435062120355.d.codeartifact.us-east-1.amazonaws.com
"""

    # Escreve o conteúdo no pip.conf
    with open(pip_conf_path, 'w') as pip_conf_file:
        pip_conf_file.write(pip_conf_content)

    print(f"pip.conf atualizado com sucesso em {pip_conf_path}")

def source_aws_sh(output_path="."):
    """
    TODO : o source precisa ser feito para o terminal que está usando essas funções da aws
    """

    print(f"{BLUE}========== Sourcing o 'aws.sh' =========={RESET}")
    output_path = os.path.abspath(output_path)
    aws_sh_path = os.path.abspath(os.path.join(output_path, "aws.sh"))
    if os.path.exists(aws_sh_path):
        command = f'source {aws_sh_path} && env'
        proc = os.popen(command)
        for line in proc:
            (key, _, value) = line.partition('=')
            os.environ[key.strip()] = value.strip()
        proc.close()
    else:
        raise FileNotFoundError(f"aws.sh not found at {aws_sh_path}")

def get_codeartifact_url(ctx):
    try:
        # # Source the aws.sh file to set environment variables
        # source_aws_sh()

        AWS_ACCOUNT_ID = os.environ['AWS_ACCOUNT_ID']
        AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
        CODEARTIFACT_DOMAIN = os.environ['CODEARTIFACT_DOMAIN']
        CODEARTIFACT_REPOSITORY = os.environ['CODEARTIFACT_REPOSITORY']

        codeartifact_token = get_codeartifact_token(ctx, CODEARTIFACT_DOMAIN, AWS_ACCOUNT_ID)

        trusted_host = f"https://aws:{codeartifact_token}@{CODEARTIFACT_DOMAIN}-{AWS_ACCOUNT_ID}.d.codeartifact.{AWS_DEFAULT_REGION}.amazonaws.com/pypi/{CODEARTIFACT_REPOSITORY}/simple/"

        return trusted_host

    except KeyError as e:
        print(f"Missing environment variable for CodeArtifact: {e}")
        raise
    except Exception as e:
        print(f"Error retrieving CodeArtifact URL: {e}")
        raise

def get_codeartifact_token(ctx, CODEARTIFACT_DOMAIN, AWS_ACCOUNT_ID):
    print(f'{BLUE}========== Obtendo Token do CodeArtifact =========={RESET}')
    code_artifact_token = ctx.run(f"aws codeartifact get-authorization-token --domain {CODEARTIFACT_DOMAIN} --domain-owner {AWS_ACCOUNT_ID} --query authorizationToken --output text", hide=True).stdout.strip()
    print('Successfully obtained codeartifact token')
    return code_artifact_token

@task
def aws(ctx, output_path='.'):
    output_path = os.path.abspath(output_path)
    tasks_dir = os.path.dirname(__file__)
    cli_dir = os.path.join(tasks_dir, 'cli')
    project_config = get_project_config(output_path)
    output_path = project_config['project_path']
    with ctx.cd(cli_dir):
        ctx.run(f'python aws_env_setup.py --output-path {output_path}', echo=True)

################### DEPLOY ###################

def get_latest_version_tag():
    # Função para obter a última versão tag do git
    result = os.popen('git describe --tags --abbrev=0').read().strip()
    return result

def increment_version(version):
    # Incrementa a versão (presumindo versão semântica)
    major, minor, patch = map(int, version.split('.'))
    return f"{major}.{minor}.{patch + 1}"

@task
def publish(ctx, project_path='.'):
    print(f"{BLUE} =========== Publishing Package on CodeArtifact ============ {RESET}")

    try:
        project_path = os.path.abspath(project_path)

        # Commit, tag e push
        summary = input("Enter commit summary: ")
        description = input("Enter commit description: ")

        latest_version = get_latest_version_tag()
        suggested_version = increment_version(latest_version.strip('v'))
        new_version = input(f"Enter new version (suggested: {suggested_version}): ") or suggested_version

        branch = os.popen('git branch --show-current').read().strip()

        os.system("git add .")
        os.system(f"git commit -m 'Summary: {summary} | Description: {description}'")
        os.system(f"git tag -a v{new_version} -m 'Release version {new_version}'")
        os.system(f"git push origin {branch} v{new_version}")

        # Build
        build(ctx, project_path='.')

        project_config = get_project_config(project_path)

        PROJECT_NAME    = project_config['project_name']
        PROJECT_VERSION = project_config['version']

        # Autenticar no CodeArtifact para client twine
        ctx.run(f"aws codeartifact login --tool twine --repository wmt-python-repository --domain wmt-libraries --domain-owner 435062120355 --region us-east-1", echo=True)

        # Publicar o pacote no CodeArtifact usando twine
        ctx.run(f"twine upload --repository codeartifact dist/*", echo=True)

        print(f"Package {PROJECT_NAME} was successfuly published on version {PROJECT_VERSION}")

    except Exception as e:
        print(f"Error during publishing process: {e}")

@task
def build(ctx, project_path='.'):

    # Determina o diretório base do projeto
    project_path = os.path.abspath(project_path)
    print(f"Building project in: {project_path}")

    try:
        # Obtém as configurações do projeto a partir do pyproject.toml
        project_config = get_project_config(project_path)

        PROJECT_NAME    = project_config['project_name']
        PROJECT_PATH    = project_config['project_path']
        PROJECT_VERSION = project_config['version']

        # Remover pastas de build do python
        remove_previous_build(PROJECT_PATH)

        # Criação do requirements para injetar as dependências adequadas
        create_requirements_txt(PROJECT_PATH, PROJECT_NAME)

        # Atualização do pyproject.toml para conter todos os pacotes utilizados TODO : Não testei
        update_pyproject_toml(PROJECT_PATH)

        # Obtém o URL do CodeArtifact
        pip_index_url = get_codeartifact_url(ctx)

        # Passa o caminho do BUILD e o pip_index_url para a função de construção do pacote
        build_package(PROJECT_PATH, pip_index_url)

        print(f"Build successful for {PROJECT_NAME} version {PROJECT_VERSION}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except tomllib.TOMLDecodeError as e:
        print(f"Error: {e}")
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
    env['PIP_EXTRA_INDEX_URL'] = pip_index_url

    # Constrói o pacote usando a ferramenta de build do Python com o índice de pacotes personalizado
    subprocess.run([sys.executable, '-m', 'build', BUILD_PATH], env=env, check=True)


################### UTILS ###################


if __name__ == '__main__':
    c = context.Context()
    # new(c, output_path='E:\\Projetos')
    # new(c, output_path='/home/seluser/wmt_registro_di_bot')
    # state(c, output_path='/home/seluser/wmt_registro_di_bot/wmt_registro_di_bot/src')
    # testState(c, output_path='/home/seluser/teste_proj/sample_bot/tests')
    # build(c, project_path='/home/seluser/wmt-busca-info-cct-bot')
    # create_requirements_txt(output_dir='/app/wmt_upload_ged_bot', PROJECT_NAME='wmt_upload_ged_bot')
    # update_pyproject_toml('/app/wmt_upload_ged_bot')
