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

def get_from_yaml(value):

    project_file = os.path.join(user_dir, '_bot.yml')
    print(project_file)
    with open(project_file, 'r') as stream:
        config = yaml.safe_load(stream)
    
    return config['project_name'], config['version']

SCAFFOLD_PATH           = os.path.join(os.path.dirname(__file__), 'scaffold/')
SAMPLE_STATE_PATH       = os.path.join(SCAFFOLD_PATH, '{{cookiecutter.project_name}}_proj/{{cookiecutter.project_name}}/src/sample_state.py')
TEST_SAMPLE_STATE_PATH  = os.path.join(SCAFFOLD_PATH, '{{cookiecutter.project_name}}_proj/tests/test_state.py')

CORE_DIR    = get_from_yaml('cor_path')
USER_DIR    = get_from_yaml('user_path')
TRT_DIR     = get_from_yaml('trt_path')

PROJECT_NAME    = get_from_yaml('project_name')
PROJECT_VERSION = get_from_yaml('version')


################### SCAFFOLDS ###################

@task
def testState(c, path="."):
    shutil.copy(TEST_SAMPLE_STATE_PATH, path)
    print(f"New testState created at: {os.path.join(path, 'test_state.py')}")

@task
def state(c, path="."):
    shutil.copy(SAMPLE_STATE_PATH, path)
    print(f"New state created at: {os.path.join(path, 'sample_state.py')}")

@task
def new(c, name=""):
    project_name = name if name else input("Please enter the new PyTRobot project name: ")
    version = input("Please enter the new project version (default is 0.1.0): ") or "0.1.0"
    output_dir = os.getcwd()

    # Supondo que a criação do projeto ocorra aqui com cookiecutter
    try:
        cookiecutter(
            template=SCAFFOLD_PATH,
            extra_context={'project_name': project_name},
            no_input=True,
            output_dir=output_dir
        )

        # Chamada para criar o arquivo YAML após a criação do projeto
        create_project_yaml(output_dir, project_name, version)
        print(f"Project '{project_name}' created successfully in '{output_dir}'.")
    except Exception as e:
        print(f"An error occurred while creating the project: {e}")

def create_project_yaml(output_dir, project_name, version):
    
    # Construindo os caminhos dinamicamente com base no projeto recém-criado
    core_dir = os.path.join(os.path.dirname(__file__), "core")
    user_dir = Path(output_dir) / f"{project_name}_bot"
    trt_dir = user_dir / ".trt"

    yaml_content = {
        'project_name': project_name,
        'version': version,
        'aws': {
            'account_id': '',
            'default_region': '',
            'codeartifact_domain': '',
            'codeartifact_token': '',
            'codeartifact_repository': '',
        },
        'trt_cli': {
            'core_path': str(core_dir),
            'user_path': str(user_dir),
            'trt_path': str(trt_dir)
        }
    }

    # Escrevendo o conteúdo no arquivo YAML
    yaml_file_path = user_dir / f"{project_name}.yaml"
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_content, yaml_file, default_flow_style=False)

    print(f"YAML configuration file created at: {yaml_file_path}")

################### BUILD ###################

@task
def build(ctx):

    trt_dir = os.path.join(TRT_DIR, PROJECT_NAME)

    # Step 1: Clean previous build and create new
    remove_previous_build()
    os.makedirs(trt_dir)

    # Step 2: Copy all logic
    copy_user_logic_to_build()
    copy_core_logic_to_build()

    # Step 3: Adjust import in all files
    adjust_imports_to_build()

    # Step 4: Build the package
    create_setup_py()
    build_package()

    print(f"Build successful for {PROJECT_NAME} version {PROJECT_VERSION}")

@task
def build_docker(ctx):

    pip_index_url = f"https://aws:{CODEARTIFACT_TOKEN}@{CODEARTIFACT_DOMAIN}-{AWS_ACCOUNT_ID}.d.codeartifact.{AWS_DEFAULT_REGION}.amazonaws.com/pypi/{CODEARTIFACT_REPOSITORY}/simple/"
    print('\n========== Buildando o container')
    ctx.run(f"docker build -t {PROJECT_NAME} --build-arg PIP_INDEX_URL={pip_index_url} .", echo=True)

    # colocar comando para fazer tags

    print('\nFeito!')

# Funções atualizadas
def remove_previous_build():
    if os.path.exists(TRT_DIR):
        shutil.rmtree(TRT_DIR)

def copy_user_logic_to_build():
    # Copia os diretórios 'src' e 'resources' para o diretório .trt
    for subdir in ['src', 'resources']:
        src_subdir = os.path.join(USER_DIR, subdir)
        if os.path.exists(src_subdir):
            dest_subdir = os.path.join(TRT_DIR, subdir)
            shutil.copytree(src_subdir, dest_subdir)

    # Copia o arquivo 'requirements.txt'
    requirements_src = os.path.join(USER_DIR, "requirements.txt")
    requirements_dest = os.path.join(TRT_DIR, "requirements.txt")
    shutil.copy(requirements_src, requirements_dest)

def copy_core_logic_to_build():
    # Copia os arquivos do diretório 'core' para o diretório de build .trt
    for item in os.listdir(CORE_DIR):
        item_path = os.path.join(CORE_DIR, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, TRT_DIR)

def adjust_imports_to_build():
    # Atualiza os imports nos arquivos Python dentro do diretório .trt
    for root, _, files in os.walk(TRT_DIR):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                content = re.sub(r'pytrobot\.', f'{PROJECT_NAME}.', content)
                with open(file_path, 'w') as f:
                    f.write(content)

def create_setup_py():
    # Cria um arquivo setup.py no diretório .trt com a configuração do pacote
    setup_path = os.path.join(TRT_DIR, "setup.py")
    requirements_path = os.path.join(TRT_DIR, "requirements.txt")
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

def build_package():
    
    # Constrói o pacote usando a ferramenta de build do Python
    subprocess.run([sys.executable, '-m', 'build', TRT_DIR], check=True)

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

# ###################################

# def remove_previous_build(user_dir):
#     trt_dir = os.path.join(user_dir, ".trt")
#     if os.path.exists(trt_dir):
#         shutil.rmtree(trt_dir)

# def copy_user_logic_to_build(user_dir, trt_dir):
#     resources_dir = os.path.join(user_dir, "resources")
#     shutil.copytree(resources_dir, os.path.join(trt_dir, "resources"))
#     src_dir = os.path.join(user_dir, "src")
#     for subdir in ['tools', 'states']:
#         src_subdir = os.path.join(src_dir, subdir)
#         if os.path.exists(src_subdir):
#             dest_subdir = os.path.join(trt_dir, subdir)
#             shutil.copytree(src_subdir, dest_subdir)
    
#     # Copia o arquivo 'requirements.txt'
#     requirements_src = os.path.join(user_dir, "requirements.txt")
#     requirements_dest = os.path.join(user_dir, ".trt", "requirements.txt")
#     if os.path.exists(requirements_src):
#         shutil.copy(requirements_src, requirements_dest)
#     else:
#         raise FileNotFoundError("O arquivo 'requirements.txt' não foi encontrado no diretório do usuário.")

# def copy_core_logic_to_build(trt_dir):

#     core_dir = os.path.join(os.path.dirname(__file__), "core")
    
#     # Lista de subdiretórios conhecidos para serem copiados como pacotes
#     known_subdirs = ['states', 'data']
    
#     # Primeiro, copie os subdiretórios conhecidos
#     for subdir in known_subdirs:
#         core_subdir = os.path.join(core_dir, subdir)
#         if os.path.exists(core_subdir):
#             dest_subdir = os.path.join(trt_dir, subdir)
#             # Copie os arquivos base se o diretório já não foi copiado antes
#             if not os.path.exists(dest_subdir):
#                 shutil.copytree(core_subdir, dest_subdir)
#             else:
#                 # Copia apenas os arquivos .py (e possivelmente outros) para o diretório existente
#                 for file in os.listdir(core_subdir):
#                     if file.endswith('.py'):
#                         shutil.copy(os.path.join(core_subdir, file), dest_subdir)
    
#     # Depois, copie os arquivos restantes diretamente para o diretório raiz do projeto
#     for item in os.listdir(core_dir):
#         item_path = os.path.join(core_dir, item)
#         if os.path.isfile(item_path) and item_path.endswith('.py') and item not in known_subdirs:
#             shutil.copy(item_path, trt_dir)

# def adjust_imports_to_build(trt_dir, project_name):
    
#     for root, _, files in os.walk(trt_dir):
#         for file in files:
#             if file.endswith('.py'):
#                 file_path = os.path.join(root, file)
#                 with open(file_path, 'r') as f:
#                     content = f.read()

#                 # Ajusta os imports que iniciam com 'pytrobot.core'
#                 content = re.sub(r'pytrobot\.core', f'{project_name}', content)

#                 content = re.sub(r'from pytrobot import State,', 
#                                  f'from {project_name} import State\nfrom {project_name}.states.base_state import', content)
#                 content = re.sub(r'from pytrobot import Tool,', 
#                                  f'from {project_name} import Tool\nfrom {project_name}.tools.base_tool import', content)

#                 # Escreve o conteúdo ajustado de volta no arquivo
#                 with open(file_path, 'w') as f:
#                     f.write(content)

# def create_setup_py(trt_dir, project_name, version):

#     parent_dir = os.path.dirname(trt_dir)
#     setup_path = os.path.join(parent_dir, "setup.py")
#     requirements_path = os.path.join(parent_dir, "requirements.txt")
    

#     with open(requirements_path, 'r') as req_file:
#         requirements = req_file.readlines()
#         requirements = [req.strip() for req in requirements]


#     with open(setup_path, 'w') as setup_file:
#         setup_file.write(f"""
#             from setuptools import setup, find_packages

#             setup(
#                 name='{project_name}',
#                 version='{version}',
#                 packages=find_packages(),
#                 include_package_data=True,
#                 install_requires={requirements},
#                 entry_points={{
#                     'console_scripts': [
#                         'trt-run={project_name}.__main__:entrypoint'
#                     ]
#                 }}
#             )
#             """
#     )

# def build_package(trt_dir):
#     parent_dir = os.path.dirname(trt_dir)
#     python_executable = shutil.which("python") or shutil.which("python3")
#     if python_executable is None:
#         raise SystemError("No Known Python executable found.")
#     subprocess.run([python_executable, '-m', 'build', parent_dir], check=True)


if __name__ == '__main__':
    c = context.Context()
    new(c)
    # state(c)

