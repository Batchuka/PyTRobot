# pytrobot/__main__.py

import sys
import importlib
import pathlib
from pytrobot.core import PyTRobot

def entrypoint():
    if len(sys.argv) != 3:
        print("Usage: trt <command> <directory>")
        sys.exit(1)
    
    command = sys.argv[1]
    directory = sys.argv[2]

    if command == 'run':

        robot = PyTRobot()
        base_path = pathlib.Path(directory)

        src_path = base_path
        resources_path = base_path / "resources"

        # Adiciona o caminho do diretório src ao sys.path para importação dos módulos do usuário
        sys.path.insert(0, str(src_path))

        # Verifica se o diretório src existe e tenta importar o __init__.py dele
        if src_path.exists():
            init_file = src_path / "src" / "__init__.py"
            if init_file.exists():
                importlib.import_module("src")
            else:
                raise ImportError("The __init__.py file is mandatory in the src directory.")
        else:
            raise FileNotFoundError("'src' directory not found.")
        
        # Verifica se o diretório resources existe e o adiciona no PyTRobot
        if resources_path.exists():
            robot._resources = resources_path.as_posix()
            robot.config_data.load_config(resources_path.as_posix())
        else:
            raise FileNotFoundError("'resources' directory not found or not specified correctly.")
        
        robot._register_core_states()
        robot.start()

    else:
        print(f"Unknown command: {command}")

