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