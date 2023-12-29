# Conteúdo de tasks.py
import os
import re
import sys
import shutil
import subprocess

from invoke import task, context, Collection, Program #type:ignore

@task
def build(c, user_dir):

    try:

        project_name = input("Enter Project Name:")
        version = input("Enter Version:")

        construct_user_project(user_dir, project_name, version)

        # Encontrar o executável do Python
        python_executable = shutil.which("python") or shutil.which("python3")

        if python_executable is None:
            raise SystemError("No Known Python executable found.")

        # Obtém o diretório atual
        current_directory = os.getcwd()

        # Muda para o diretório '.trt/'
        os.chdir(".trt")

        # Executa o comando 'python -m build .'
        os.system(f"{python_executable} -m build .")

        # Volta para o diretório original
        os.chdir(current_directory)

    except Exception as e:

        print(f"Error on build : {e}")
        handle_error(user_dir)
    


def construct_user_project(user_dir, project_name, version):

    remove_all_trt(user_dir)

    copy_pytrobot_logic(user_dir, project_name)
    copy_user_logic(user_dir, project_name)

    extract_imports(user_dir)
    create_setup_py(user_dir, project_name, version)

def handle_error(user_dir):

    c = context.Context()
    remove_all_trt(user_dir)
    sys.exit(1)  # Encerra o programa com código de saída 1 em caso de erro

def get_python_files(directory):
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def remove_all_trt(user_dir):
    target_user_dir = os.path.join(user_dir, ".trt")
    if os.path.exists(target_user_dir):
        shutil.rmtree(target_user_dir)

def copy_pytrobot_logic(user_dir, project_name):

    pytrobot_source_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "framework")
    pytrobot_target_dir = os.path.join(user_dir, ".trt", project_name)

    # Copiar a estrutura do diretório
    shutil.copytree(src=pytrobot_source_dir, dst=pytrobot_target_dir, ignore=shutil.ignore_patterns("__pycache__"))

    # Regex para encontrar os imports que seguem o padrão "from pytrobot <qualquer import> import "
    import_regex = re.compile(r"from pytrobot\.framework\.(\w+)")

    # Percorrer todos os arquivos no diretório
    for root, _, files in os.walk(pytrobot_target_dir):
        for file in files:
            file_path = os.path.join(root, file)

            # Ler o conteúdo do arquivo
            with open(file_path, 'r') as f:
                content = f.read()

            # Substituir os imports no conteúdo
            adjusted_content = import_regex.sub(fr"from {project_name}", content)

            # Escrever o conteúdo ajustado de volta ao arquivo
            with open(file_path, 'w') as f:
                f.write(adjusted_content)

def copy_user_logic(user_dir, project_name):
    target_user_dir = os.path.join(user_dir, ".trt", project_name, "user")

    # Copiar a estrutura do diretório
    shutil.copytree(src=user_dir, dst=target_user_dir, ignore=ignore_func)

    # Regex para encontrar os imports que seguem o padrão "from <base_from> <qualquer import> import "
    base_from = os.path.basename(os.path.normpath(user_dir))
    last_regex = re.compile(fr"from {re.escape(base_from)}(\S*)[^\n]*import [^\n]*")
    import_regex_1 = re.compile(fr"from {re.escape(base_from)}\.(\w+)")
    import_regex_2 = re.compile(r"from pytrobot\.framework")

    # Percorrer todos os arquivos no diretório
    for root, _, files in os.walk(target_user_dir):
        for file in files:
            file_path = os.path.join(root, file)

            # Ler o conteúdo do arquivo
            with open(file_path, 'r') as f:
                content = f.read()

            # Encontrar o último componente do import
            last_match = last_regex.search(content)
            last_component = last_match.group(1) if last_match else None

            # Substituir os imports no conteúdo
            adjusted_content = import_regex_1.sub(fr"from {project_name}.user{last_component}", content)
            adjusted_content = import_regex_2.sub(fr"from {project_name}", adjusted_content)

            # Escrever o conteúdo ajustado de volta ao arquivo
            with open(file_path, 'w') as f:
                f.write(adjusted_content)
    
def ignore_func(dir, files):
    return [f for f in files if f == '.trt' or f == '__pycache__']

def extract_imports(user_dir):
    user_files = get_python_files(os.path.join(user_dir, ".trt"))
    
    # Etapa 2: Identificar todos os imports feitos pelo usuário
    unique_imports = set()
    for file_path in user_files:
        with open(file_path, "r") as file:
            content = file.read()

        lines = content.split("\n")
        for line in lines:
            if line.startswith("import ") or line.startswith("from "):
                parts = line.split()
                library_name = parts[1] if len(parts) > 1 else ""
                library_name = library_name.split(".")[0]
                unique_imports.add(library_name)

    # Etapa 3: Descartar valores repetidos
    unique_imports = list(unique_imports)

    # Etapa 4 e 5: Verificar a versão e criar requirements.txt
    dependencies = {}
    for library_name in unique_imports:
        try:
            __import__(library_name)
            version = subprocess.check_output(
                ["pip", "show", library_name], universal_newlines=True
            )
            version = version.split("\n")[1].split(":")[1].strip()
            dependencies[library_name] = version
        except ImportError as e:
            print(f"Ignorando import de objeto específico: {library_name} — {e}")
        except subprocess.CalledProcessError:
            print(f"Ignorando pacote sem versão especificada: {library_name}")

    # Adicionar dependências ao requirements.txt
    requirements_path = os.path.join(user_dir, ".trt", "requirements.txt")
    with open(requirements_path, "w") as requirements_file:
        for library, version in sorted(dependencies.items()):
            requirements_file.write(f"{library}=={version}\n")

def create_setup_py(user_dir, project_name, version):
    setup_py_path = os.path.join(user_dir, ".trt", "setup.py")
    requirements_txt_path = os.path.join(user_dir, ".trt", "requirements.txt")

    with open(requirements_txt_path, "r") as requirements_file:
        requirements_content = requirements_file.read().strip().splitlines()

    with open(setup_py_path, "w") as setup_file:
        setup_file.write(
            f"from setuptools import setup, find_packages\n\n"
            f"setup(\n"
            f"    name='{project_name}',\n"
            f"    version='{version}',\n"
            f"    packages=find_packages(),\n"
            f"    entry_points={{\n"
            f"        'console_scripts': [\n"
            f"            'trt-run={project_name}.__main__:run'\n"
            f"        ]\n"
            f"    }},\n"
            f"    install_requires={requirements_content},\n"  # Inclui as dependências do requirements.txt
            f")\n"
        )


if __name__ == '__main__':
    c = context.Context()
    build(c,'/home/seluser/wmt-bot005-emitir-certidoes-due-diligence/wmt_bot005_emitir_certidoes_due_diligence')
