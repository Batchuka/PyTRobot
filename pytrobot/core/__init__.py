# pytrobot/__init__.py
import builtins
from pytrobot.core.dataset_layer import DatasetLayer
from pytrobot.core.object_layer import ObjectLayer
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
        PyTRobot.object_layer = ObjectLayer()
        PyTRobot.machine_layer = MachineLayer(self.object_layer, self.dataset_layer)
        self._initialized = True

    def _register_core_states(self):
        from pytrobot.core.states.starter_state import _StarterState
        from pytrobot.core.states.finisher_state import _FinisherState
        State(_StarterState)
        if PyTRobot._first_state_name:
            Transition('_StarterState', PyTRobot._first_state_name, '_FinisherState')(_StarterState)
        else:
            # Transição padrão se nenhum estado inicial foi definido
            Transition('_StarterState', '_FinisherState', '_FinisherState')(_StarterState)
        State(_FinisherState)
        Transition('_FinisherState', '_FinisherState', '_FinisherState')(_FinisherState)

    def start(self):
        self.machine_layer.run()

    # Métodos de acesso para os decoradores

    @staticmethod
    def get_object_layer():
        if PyTRobot.object_layer is None:
            raise Exception("PyTRobot não foi inicializado corretamente.")
        return PyTRobot.object_layer
    
    @staticmethod
    def get_machine_layer():
        if PyTRobot.machine_layer is None:
            raise Exception("PyTRobot não foi inicializado corretamente.")
        return PyTRobot.machine_layer

    @classmethod
    def set_first_state(cls, state_name):
        cls._first_state_name = state_name

# Decoradores

def State(cls):
    if PyTRobot.object_layer is None:
        raise Exception("PyTRobot não foi inicializado corretamente. A camada de objetos está inacessível.")
    object_layer = PyTRobot.get_object_layer()
    object_layer.register_state(cls)
    return cls

def Tool(cls):
    if PyTRobot.object_layer is None:
        raise Exception("PyTRobot não foi inicializado corretamente. A camada de objetos está inacessível.")
    object_layer = PyTRobot.get_object_layer()
    object_layer.register_tool(cls)
    return cls

def Action(cls):
    if PyTRobot.object_layer is None:
        raise Exception("PyTRobot não foi inicializado corretamente. A camada de objetos está inacessível.")
    object_layer = PyTRobot.get_object_layer()
    object_layer.register_action(cls)
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

def First(cls):
    PyTRobot.set_first_state(cls.__name__)
    return cls