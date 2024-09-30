# WARNING : NOT CHANGE THIS
import os
import sys

def main():

    from pytrobot.core.__main__ import entrypoint

    # Defines the current directory as an argument for the entrypoint
    sys.argv = [os.path.abspath(os.path.dirname(__file__)), "orchestrator"]

    # Invoke probot entrypoint
    entrypoint()

if __name__ == '__main__':
    main()

