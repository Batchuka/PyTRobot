# Conteúdo de tasks.py
import os
import shutil
from invoke import task, context, Collection, Program #type:ignore
import autopep8

@task
def construct_user_project(c, user_dir):

    project_name = input("Enter Project Name:")
    version = input("Enter Version:")

    remove_all_trt(c, user_dir)
    copy_pytrobot_logic(c, user_dir, project_name)
    copy_user_logic(c, user_dir, project_name)
    update_imports(c, user_dir)
    create_setup_py(c, user_dir, project_name, version)

@task
def remove_all_trt(c, user_dir):
    target_user_dir = os.path.join(user_dir, ".trt")
    if os.path.exists(target_user_dir):
        shutil.rmtree(target_user_dir)

@task
def copy_pytrobot_logic(c, user_dir, project_name):
    pytrobot_source_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pytrobot")
    pytrobot_target_dir = os.path.join(user_dir, ".trt", project_name)
    shutil.copytree(src=pytrobot_source_dir, dst=pytrobot_target_dir, ignore=shutil.ignore_patterns("__pycache__"))

@task
def copy_user_logic(c, user_dir, project_name):
    target_user_dir = os.path.join(user_dir, ".trt", project_name, "user")
    
    def ignore_func(dir, files):
        return [f for f in files if f == '.trt' or f == '__pycache__']

    shutil.copytree(src=user_dir, dst=target_user_dir, ignore=ignore_func)

@task
def update_imports(c, user_dir):
    user_files = get_python_files(c, user_dir+"/.trt")

    for file_path in user_files:
        with open(file_path, "r") as file:
            content = file.read()

        updated_content = autopep8.fix_code(content)

        with open(file_path, "w") as file:
            file.write(updated_content)

@task
def get_python_files(c, directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

@task
def create_setup_py(c, user_dir, project_name, version):
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

    
# if __name__ == '__main__':
#     c = context.Context()
#     remove_all_trt(c,'/home/seluser/wmt-bot005-emitir-certidoes-due-diligence/wmt_bot005_emitir_certidoes_due_diligence')
#     copy_pytrobot_logic(c,'/home/seluser/wmt-bot005-emitir-certidoes-due-diligence/wmt_bot005_emitir_certidoes_due_diligence')
#     copy_user_logic(c,'/home/seluser/wmt-bot005-emitir-certidoes-due-diligence/wmt_bot005_emitir_certidoes_due_diligence')
#     update_imports(c,'/home/seluser/wmt-bot005-emitir-certidoes-due-diligence/wmt_bot005_emitir_certidoes_due_diligence')
#     create_setup_py(c,'/home/seluser/wmt-bot005-emitir-certidoes-due-diligence/wmt_bot005_emitir_certidoes_due_diligence')