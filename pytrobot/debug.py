import os
import sys
from pytrobot.core.__main__ import entrypoint

def debug_entrypoint(directory=None):
    """
    Proxy function to trigger the main entrypoint of the framework.
    This function is specifically designed for debugging purposes.
    """
    sys.argv = [directory or os.getcwd()]
    entrypoint()