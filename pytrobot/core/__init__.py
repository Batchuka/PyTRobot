# pytrobot/__init__.py
import builtins
import warnings
from pytrobot.core.singleton import Singleton

from pytrobot.core.strategy.state.machine import StateMachine, TrueTable
from pytrobot.core.feature.multithread import MultithreadManager
from pytrobot.core.feature.subprocess import SubprocessManager
from pytrobot.core.feature.logging import print_pytrobot_banner, pytrobot_print



class PyTRobotNotInitializedException(Exception):
    """Exceção para ser levantada quando o PyTRobot não está instanciado."""
    pass

class PyTRobot(metaclass=Singleton):
    """Classe principal do pytrobot, implementada como um Singleton."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PyTRobot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._first_state_name: str = ''
        self._resources: str = ''
        print_pytrobot_banner()
        builtins.print = pytrobot_print
        if not hasattr(self, '_initialized'):
            self._initialize()
