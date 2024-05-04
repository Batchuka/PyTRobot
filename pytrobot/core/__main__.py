# pytrobot/__main__.py
import os
import sys
import importlib
from pytrobot.core import PyTRobot

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
    src_path        = os.path.join(directory)
    resources_path  = os.path.join(directory, 'resources')

    robot = PyTRobot()

    sys.path.insert(0, str(src_path))

    # Checks if the src directory exists and tries to import its __init__.py
    if os.path.exists(src_path):
        init_file = os.path.join(src_path, "src", "__init__.py")
        if os.path.exists(init_file):
            importlib.import_module("src")
        else:
            raise ImportError("The __init__.py file is mandatory in the src directory.")
    else:
        raise FileNotFoundError("'src' directory not found.")
    

    # Checks if the resources directory exists and adds it to PyTRobot
    if os.path.exists(resources_path):
        robot._resources = resources_path
        robot.config_data.load_config(resources_path)
    else:
        raise FileNotFoundError("'resources' directory not found or not specified correctly.")
    

    robot._register_core_states()
    robot.start()
