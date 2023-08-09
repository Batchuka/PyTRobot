from enum import Enum
from .robot import Robot
from .inventory import Inventory
from .starter import Starter
from .controller import Controller
from .dispatcher import Dispatcher
from .performer import Performer
from .finisher import Finisher


class Environment(Enum):
    DEV = 'DEV.properties'
    HML = 'HML.properties'
    OPS = 'OPS.properties'


class State(Enum):
    DEFAULT = None
    STARTER = 'Starter'
    CONTROLLER = 'Controller'
    DISPATCHER = 'Dispatcher'
    PERFORMER = 'Performer'
    FINISHER = 'Finisher'
