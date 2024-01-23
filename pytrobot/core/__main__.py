# pytrobot/__main__.py
import sys
from pytrobot.core import PyTRobot

def entrypoint():
    if len(sys.argv) != 3:
        print("Usage: trt <command> <directory>")
        sys.exit(1)
    
    command = sys.argv[1]
    directory = sys.argv[2]
    if command == 'run':
        robot = PyTRobot()
        robot.start()
    else:
        print(f"Unknown command: {command}")

if __name__ == '__main__':
    entrypoint()