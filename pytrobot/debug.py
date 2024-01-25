import os
import re
import sys
import pathlib
from pytrobot.core.__main__ import entrypoint

def debug_entrypoint(command='run', directory=None):
    """
    Proxy function to trigger the main entrypoint of the framework.
    This function is specifically designed for debugging purposes.
    """
    sys.argv = ['trt', command, directory or os.getcwd()]
    entrypoint()


def auto_import_classes(directory):
    """
    Scan the actions, tools and states directories within src_directory,
    and automatically writes the necessary imports to the __init__.py files
    corresponding.
    """
    for subdir in ['actions', 'tools', 'states']:
        init_file_path = pathlib.Path(directory) / 'src' / subdir / '__init__.py'
        with open(init_file_path, 'w') as init_file:
            py_files = [f for f in os.listdir(pathlib.Path(directory) / 'src' / subdir) if f.endswith('.py') and f != '__init__.py']
            for py_file in py_files:
                file_path = pathlib.Path(directory) / 'src' / subdir / py_file
                with open(file_path, 'r') as file:
                    content = file.read()
                    # Encontra a definição da classe
                    match = re.search(r'class (\w+)', content)
                    if match:
                        class_name = match.group(1)  # Pega o nome da classe
                        import_statement = f"from src.{subdir}.{py_file[:-3]} import {class_name}\n"
                        init_file.write(import_statement)