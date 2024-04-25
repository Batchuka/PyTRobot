# Conteúdo de tasks.py
import os
import re
import sys
import yaml
import shutil
import subprocess
from pathlib import Path
from cookiecutter.main import cookiecutter


from invoke import task, context, Collection, Program #type:ignore

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
                raise ValueError("The project.yaml file is empty or has incorrect content.")
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"The project.yaml file was not found at {yaml_file_path}.")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"An error occurred while parsing the YAML file at {yaml_file_path}: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while loading the project configuration: {e}")

CORE_PATH               = os.path.join(os.path.dirname(__file__), "core")
SCAFFOLD_PATH           = os.path.join(os.path.dirname(__file__), 'scaffold')
SAMPLE_STATE_PATH       = os.path.join(SCAFFOLD_PATH, '{{cookiecutter.project_name}}_bot/{{cookiecutter.project_name}}/src/sample_state.py')
TEST_SAMPLE_STATE_PATH  = os.path.join(SCAFFOLD_PATH, '{{cookiecutter.project_name}}_bot/tests/test_state.py')


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
    project_name = name if name else input("Please enter the new PyTRobot project name: ")
    version = input("Please enter the new project version (default is 0.1.0): ") or "0.1.0"

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
        print(f"Project '{project_name}' created successfully in '{output_path}'.")
    except Exception as e:
        print(f"An error occurred while creating the project: {e}")

def create_project_yaml(output_dir, project_name, version):
    # Construindo os caminhos dinamicamente com base no projeto recém-criado
    project_dir = os.path.join(output_dir, f"{project_name}_bot")
    yaml_content = {
        'project_name': project_name,
        'version': version,
        'project_path': project_dir,
        'package_path': os.path.join(project_dir, project_name),
        'build_path': os.path.join(project_dir, ".trt")
    }

    # Escrevendo o conteúdo no arquivo YAML
    yaml_file_path = os.path.join(project_dir, "project.yaml")
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_content, yaml_file, default_flow_style=False)

    print(f"YAML configuration file created at: {yaml_file_path}")

################### BUILD ###################

@task
def image(ctx, project_path='.'):

    # Determina o diretório base do projeto
    project_path = os.path.abspath(project_path)
    print(f"Building project in: {project_path}")

    try:
        project_config = get_project_config(project_path)  # Supondo que esta função agora recebe o diretório base do projeto

        PROJECT_NAME            = project_config('project_name')
        AWS_ACCOUNT_ID          = project_config('account_id')
        AWS_DEFAULT_REGION      = project_config('default_region')
        CODEARTIFACT_TOKEN      = project_config('codeartifact_token')
        CODEARTIFACT_DOMAIN     = project_config('codeartifact_domain')
        CODEARTIFACT_REPOSITORY = project_config('codeartifact_repository')

        pip_index_url = f"https://aws:{CODEARTIFACT_TOKEN}@{CODEARTIFACT_DOMAIN}-{AWS_ACCOUNT_ID}.d.codeartifact.{AWS_DEFAULT_REGION}.amazonaws.com/pypi/{CODEARTIFACT_REPOSITORY}/simple/"
        print('\n========== Buildando o container')
        ctx.run(f"docker build -t {PROJECT_NAME} --build-arg PIP_INDEX_URL={pip_index_url} .", echo=True)

        # colocar comando para fazer tags
        print('\nFeito!')
    except Exception as e:
        print(f"Error during image generation process: {e}")

@task
def build(ctx, project_path='.'):

    # Determina o diretório base do projeto
    project_path = os.path.abspath(project_path)
    print(f"Building project in: {project_path}")

    try:
        project_config = get_project_config(project_path)  # Supondo que esta função agora recebe o diretório base do projeto

        BUILD_PATH      = project_config['build_path']
        PACKAGE_PATH    = project_config['package_path']
        PROJECT_NAME    = project_config['project_name']
        PROJECT_VERSION = project_config['version']

        # Passa o TRT_DIR para as funções
        remove_previous_build(BUILD_PATH)
        os.makedirs(BUILD_PATH)

        copy_user_logic_to_build(PACKAGE_PATH, BUILD_PATH, PROJECT_NAME)
        copy_core_logic_to_build(CORE_PATH, BUILD_PATH, PROJECT_NAME)

        adjust_imports_to_build(BUILD_PATH, PROJECT_NAME)

        create_setup_py(BUILD_PATH, PROJECT_NAME, PROJECT_VERSION)
        build_package(BUILD_PATH)

        print(f"Build successful for {PROJECT_NAME} version {PROJECT_VERSION}")
    
    except Exception as e:
        print(f"Error during build process: {e}")

# Funções de build
def remove_previous_build(BUILD_PATH):
    if os.path.exists(BUILD_PATH):
        shutil.rmtree(BUILD_PATH)

def copy_user_logic_to_build(PACKAGE_PATH, BUILD_PATH, PROJECT_NAME):

    # Copia os diretórios 'src' e 'resources' para o diretório .trt
    for subdir in ['src', 'resources']:
        src_subdir = os.path.join(PACKAGE_PATH, subdir)
        if os.path.exists(src_subdir):
            dest_subdir = os.path.join(BUILD_PATH, PROJECT_NAME, subdir)
            shutil.copytree(src_subdir, dest_subdir)

    # Copia o arquivo 'requirements.txt'
    requirements_src = os.path.join(PACKAGE_PATH, "requirements.txt")
    requirements_dest = os.path.join(BUILD_PATH, "requirements.txt")
    shutil.copy(requirements_src, requirements_dest)

def copy_core_logic_to_build(CORE_DIR, BUILD_PATH, PROJECT_NAME):
    
    # Copia os arquivos do diretório 'core' para o diretório de build .trt
    for item in os.listdir(CORE_DIR):
        item_path = os.path.join(CORE_DIR, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, f'{BUILD_PATH}/{PROJECT_NAME}')

def adjust_imports_to_build(BUILD_PATH, PROJECT_NAME):
    # Atualiza os imports nos arquivos Python dentro do diretório .trt
    for root, _, files in os.walk(BUILD_PATH):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                content = re.sub(r'pytrobot.core\.', f'{PROJECT_NAME}.', content)
                with open(file_path, 'w') as f:
                    f.write(content)

def create_setup_py(BUILD_PATH, PROJECT_NAME, PROJECT_VERSION):

    # Cria um arquivo setup.py no diretório .trt com a configuração do pacote
    setup_path = os.path.join(BUILD_PATH, "setup.py")
    requirements_path = os.path.join(BUILD_PATH, "requirements.txt")
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
            '{PROJECT_NAME}-run={PROJECT_NAME}.__main__:entrypoint'
        ]
    }},
)
        """
        )

def build_package(BUILD_PATH):
    
    # Constrói o pacote usando a ferramenta de build do Python
    subprocess.run([sys.executable, '-m', 'build', BUILD_PATH], check=True)


################### UTILS ###################

@task
def test(ctx):
    ctx.run("pytest tests/")
    ctx.run("pytest --docker tests/")

@task
def clean(ctx):
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)

@task
def spec_package(ctx):
    pass

@task
def auto_import(ctx):
    pass



if __name__ == '__main__':
    c = context.Context()
    # new(c, output_path='/home/seluser/teste_proj')
    # state(c, output_path='/home/seluser/teste_proj/sample_bot/sample/src')
    # testState(c, output_path='/home/seluser/teste_proj/sample_bot/tests')
    build(c, project_path='/home/seluser/teste_proj/sample_bot')
