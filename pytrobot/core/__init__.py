# pytrobot/__init__.py
import builtins
from pytrobot.core.dataset_layer import DatasetLayer
from pytrobot.core.object_layer import ObjectsLayer
from pytrobot.core.machine_layer import MachineLayer
from pytrobot.core.utils import print_pytrobot_banner, pytrobot_print


class PyTRobot:
    """Classe principal do pytrobot, implementada como um Singleton."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PyTRobot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialize()

    def _initialize(self):
        print_pytrobot_banner()
        builtins.print = pytrobot_print
        PyTRobot.dataset_layer = DatasetLayer()
        PyTRobot.objects_layer = ObjectsLayer()
        PyTRobot.machine_layer = MachineLayer(self.objects_layer, self.dataset_layer)
        self._initialized = True
    
    @staticmethod
    def get_objects_layer():
        if PyTRobot.objects_layer is None:
            raise Exception("PyTRobot não foi inicializado corretamente.")
        return PyTRobot.objects_layer
    
    @staticmethod
    def get_machine_layer():
        if PyTRobot.machine_layer is None:
            raise Exception("PyTRobot não foi inicializado corretamente.")
        return PyTRobot.machine_layer

    def start(self):
        self.machine_layer.run()

def State(cls):
    if PyTRobot.objects_layer is None:
        raise Exception("PyTRobot não foi inicializado corretamente. A camada de objetos está inacessível.")
    objects_layer = PyTRobot.get_objects_layer()
    objects_layer.register_state(cls)
    return cls

def Tool(cls):
    if PyTRobot.objects_layer is None:
        raise Exception("PyTRobot não foi inicializado corretamente. A camada de objetos está inacessível.")
    objects_layer = PyTRobot.get_objects_layer()
    objects_layer.register_tool(cls)
    return cls

def Action(cls):
    if PyTRobot.objects_layer is None:
        raise Exception("PyTRobot não foi inicializado corretamente. A camada de objetos está inacessível.")
    objects_layer = PyTRobot.get_objects_layer()
    objects_layer.register_action(cls)
    return cls

def Transition(current_state_name, next_state_on_success_name, next_state_on_failure_name):
    def decorator(cls):
        if current_state_name is None:
            raise ValueError("O nome do estado atual não pode ser None.")
        if next_state_on_success_name is None:
            raise ValueError("O nome do próximo estado para sucesso não pode ser None.")
        if next_state_on_failure_name is None:
            raise ValueError("O nome do próximo estado para falha não pode ser None.")

        machine_layer = PyTRobot.get_machine_layer()
        if machine_layer is None:
            raise Exception("A camada da máquina não foi inicializada corretamente.")

        machine_layer.create_transition(current_state_name, next_state_on_success_name, next_state_on_failure_name)
        return cls
    return decorator

