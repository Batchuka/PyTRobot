# pytrobot/__main__.py
import sys
from pytrobot import PyTRobot

def entrypoint():
    """
    Entry point for the PyTRobot application.
    """
    if len(sys.argv) != 1:
        print("Usage: <project_directory>")
        print("You must enter the project directory")
        sys.exit(1)

    directory = sys.argv[0]

    # Initialize the PyTRobot application
    pytrobot = PyTRobot(directory)
    pytrobot.initialize_application()
    pytrobot.start_application()

if __name__ == '__main__':
    entrypoint()
