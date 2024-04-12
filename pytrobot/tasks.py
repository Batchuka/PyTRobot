# Conteúdo de tasks.py
import os
import re
import sys
import shutil
import subprocess

from invoke import task, context, Collection, Program #type:ignore

scaffold_dir = os.path.join(os.path.dirname(__file__), "scaffold")
templates = {
    'state': 'src/sample_state.py',
    'testState': 'tests/test_state.py'
}


@task
def testState(c, path="."):
    template_file = templates['testState']
    shutil.copy(os.path.join(scaffold_dir, template_file), path)
    print(f"New testState created at: {os.path.join(path, template_file)}")

@task
def state(c, path="."):
    template_file = templates['state']
    shutil.copy(os.path.join(scaffold_dir, template_file), path)
    print(f"New state created at: {os.path.join(path, template_file)}")

@task
def new(c, path="."):
    # Pergunta o nome do projeto ao usuário
    project_name = input("Por favor, insira o nome do novo projeto PyTRobot: ")

    # Se 'path' é '.', usa o diretório atual, caso contrário, o caminho fornecido.
    project_path = os.path.join(path if path != "." else os.getcwd(), project_name)

    # Verifica se o diretório do projeto já existe
    if os.path.exists(project_path):
        print(f"O diretório '{project_path}' já existe. Por favor, escolha um nome diferente ou remova o diretório existente.")
        return

    # Caminho para o diretório de scaffold/template
    template_path = os.path.join(os.path.dirname(__file__), 'scaffold')

    # Copia o scaffold para o novo diretório do projeto
    shutil.copytree(template_path, project_path)
    
    # Cria um arquivo requirements.txt vazio
    requirements_path = os.path.join(project_path, 'requirements.txt')
    with open(requirements_path, 'w') as requirements_file:
        requirements_file.write("# Adicione aqui suas dependências\n")

    # Cria um ambiente virtual dentro do diretório do projeto
    subprocess.run([sys.executable, '-m', 'venv', os.path.join(project_path, 'venv')])

    print(f"Projeto '{project_name}' criado com sucesso em: {project_path}")
    print(f"Para ativar o ambiente virtual, navegue até '{project_path}' e execute:")
    print(f"'source venv/bin/activate' no Unix ou macOS, ou 'venv\\Scripts\\activate' no Windows.")




# Substitua as variáveis a seguir pelos valores apropriados
AWS_ACCOUNT_ID = ''
AWS_DEFAULT_REGION = ''
CODEARTIFACT_DOMAIN = ''
CODEARTIFACT_REPOSITORY = ''
CODEARTIFACT_TOKEN = ''

@task
def build_docker(ctx, browser):

    pip_index_url = f"https://aws:{CODEARTIFACT_TOKEN}@{CODEARTIFACT_DOMAIN}-{AWS_ACCOUNT_ID}.d.codeartifact.{AWS_DEFAULT_REGION}.amazonaws.com/pypi/{CODEARTIFACT_REPOSITORY}/simple/"

    print('\n========== Buildando o container')
    if browser.lower() == 'firefox':
        ctx.run(
            f"docker build -t wmt-bot005-emitir-certidoes-due-diligence-firefox -f Dockerfile.deploy-firefox --build-arg PIP_INDEX_URL={pip_index_url} .", echo=True)
    elif browser.lower() == 'chrome':
        ctx.run(
            f"docker build -t wmt-bot005-emitir-certidoes-due-diligence-chrome -f Dockerfile.deploy-chrome --build-arg PIP_INDEX_URL={pip_index_url} .", echo=True)
    else:
        print("Navegador não suportado. Use 'firefox' ou 'chrome'.")
    print('\nFeito!')


@task
def spec_package(ctx):
    pass


@task
def test(ctx):
    ctx.run("pytest tests/")
    ctx.run("pytest --docker tests/")


@task
def clean(ctx):
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)




# @task
# def build(c, path=None):

#     user_dir = path or os.getcwd()
#     project_name = os.path.basename(user_dir)
#     trt_dir = os.path.join(user_dir, ".trt", project_name)
#     version = input("Enter Version: ")

#     # Step 1: Clean previous build and create new
#     remove_previous_build(user_dir)
#     os.makedirs(trt_dir)

#     # Step 2: Copy all logic
#     copy_user_logic_to_build(user_dir, trt_dir)
#     copy_core_logic_to_build(trt_dir)

#     # Step 3: Adjust import in all files
#     adjust_imports_to_build(trt_dir, project_name)

#     # Step 4: Build the package
#     create_setup_py(trt_dir, project_name, version)
#     build_package(trt_dir)

#     print(f"Build successful for {project_name} version {version}")

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
# from setuptools import setup, find_packages

# setup(
#     name='{project_name}',
#     version='{version}',
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires={requirements},
#     entry_points={{
#         'console_scripts': [
#             'trt-run={project_name}.__main__:entrypoint'
#         ]
#     }}
# )
# """)

# def build_package(trt_dir):
#     parent_dir = os.path.dirname(trt_dir)
#     python_executable = shutil.which("python") or shutil.which("python3")
#     if python_executable is None:
#         raise SystemError("No Known Python executable found.")
#     subprocess.run([python_executable, '-m', 'build', parent_dir], check=True)


# if __name__ == '__main__':
#     c = context.Context()
#     build(c,'/home/seluser/user/bot1')
