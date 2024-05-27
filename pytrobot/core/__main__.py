# pytrobot/__main__.py
import os
import sys
import importlib
from pytrobot.core import PyTRobot


def get_base_package(src_path):
    """
    Extracts the base package name from the given src path.
    Assumes the base package is the directory name just before 'src'.
    """
    parts = src_path.split(os.sep)
    if 'src' in parts:
        return parts[parts.index('src') - 1]
    raise ValueError("Invalid src path: 'src' directory not found in path")

def import_all_states(src_path):
    """
    Imports all Python modules in the specified directory.
    """
    base_package = get_base_package(src_path)
    for file in os.listdir(src_path):
        if file.endswith(".py") and file not in ["__init__.py", "__main__.py"]:
            module_name = file[:-3]  # Remove .py
            importlib.import_module(f'{base_package}.src.{module_name}')

def entrypoint():
    """
    For the pytrobot package to work properly, user modules must be imported.
    Thus, the @State decorators will be invoked and with this, the class registration 
    logic will occur in the 'TrueTable' of pytrobot's 'StateMachine'.

    Much of the logic of the 'entrypoint' method is aimed at ensuring that the user's package path is
    imported before 'robot.start()', so that user states are recorded.
    """

    if len(sys.argv) != 1:
        print(sys.argv)
        print("Usage: <directory>")
        print("You must enter the project directory")
        sys.exit(1)
    

    directory       = sys.argv[0]
    src_path        = os.path.join(directory, 'src')

    robot = PyTRobot()

    sys.path.insert(0, str(src_path))

    # Checks if the src directory exists and tries to import its __init__.py
    if os.path.exists(src_path):
        # Usar a nova função de importação
        import_all_states(src_path)
    else:
        raise FileNotFoundError("'src' directory not found.")

    robot._register_core_states()
    robot.start()
