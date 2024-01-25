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

        src_path = pathlib.Path(directory)

        sys.path.insert(0, str(src_path))

        print(sys.path)

        if src_path.exists():
            init_file = src_path / "src" / "__init__.py"
            if init_file.exists():
                importlib.import_module("src")
            else:
                raise ImportError("O arquivo __init__.py é obrigatório no diretório src.")
        else:
            raise FileNotFoundError("Diretório src não encontrado.")
        robot._register_core_states()
        robot.start()
    else:
        print(f"Unknown command: {command}")