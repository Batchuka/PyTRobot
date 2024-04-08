# pytrobot/__init__.py
import builtins
import warnings
from pytrobot.core.dataset_layer import ConfigData, TransactionData, AccessDatasetLayer
from pytrobot.core.machine_layer import StateMachine, TrueTable, AccessMachineLayer
from pytrobot.core.object_layer import ObjectsRegister, AccessObjectLayer
from pytrobot.core.utils import print_pytrobot_banner, pytrobot_print


class PyTRobotNotInitializedException(Exception):
    """Exceção para ser levantada quando o PyTRobot não está instanciado."""
    pass

class PyTRobot:
    """Classe principal do pytrobot, implementada como um Singleton."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PyTRobot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._first_state_name: str = ''
        self._resources: str = ''
        if not hasattr(self, '_initialized'):
            self._initialize()
            
    def _initialize(self):
        print_pytrobot_banner()
        builtins.print = pytrobot_print
        access_dataset_layer = self.create_access_dataset_layer()
        access_object_layer = self.create_access_object_layer()
        access_machine_layer = self.create_access_machine_layer()

        # Inicializa os novos atributos
        self.config_data = ConfigData()
        self.true_table = TrueTable()
        self.state_machine = StateMachine(access_dataset_layer, access_object_layer, access_machine_layer)
        self.objects_register = ObjectsRegister()
        self._initialized = True

    def _register_core_states(self):
        from pytrobot.core.states.starter_state import _StarterState
        from pytrobot.core.states.finisher_state import _FinisherState
        State(_StarterState)
        if self._first_state_name:
            Transition('_StarterState', self._first_state_name, '_FinisherState')(_StarterState)
        else:
            Transition('_StarterState', '_FinisherState', '_FinisherState')(_StarterState)
        State(_FinisherState)
        Transition('_FinisherState', '_FinisherState', '_FinisherState')(_FinisherState)

    def start(self):
        self.state_machine.run()

    def create_access_dataset_layer(self):
        return AccessDatasetLayer(self)

    def create_access_object_layer(self):
        return AccessObjectLayer(self)

    def create_access_machine_layer(self):
        return AccessMachineLayer(self)

    # Métodos de acesso para os decoradores

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise PyTRobotNotInitializedException("PyTRobot object is not initialized.")
        return cls._instance

    @classmethod
    def add_object_on_registry(cls, registry_cls):
        try:
            instance = cls.get_instance()
            instance.objects_register.register(registry_cls.__name__, registry_cls)
            return instance.objects_register
        except PyTRobotNotInitializedException as e:
            warnings.warn(str(f"{e} : Your objects will not be registered"), RuntimeWarning)
    
    @classmethod
    def update_transition(cls, current_state, next_state_on_success=None, next_state_on_failure=None):
        try:
            instance = cls.get_instance()
            instance.true_table.update_transition(current_state, next_state_on_success, next_state_on_failure)
        except PyTRobotNotInitializedException as e:
            warnings.warn(str(f"{e} : Your objects will not be registered"), RuntimeWarning)

    @classmethod
    def add_transition_on_true_table(cls, current_state_name, next_state_on_success_name, next_state_on_failure_name):
        try:
            instance = cls.get_instance()
            instance.true_table.add_transition(current_state_name, next_state_on_success_name, next_state_on_failure_name)
            return instance.true_table
        except PyTRobotNotInitializedException as e:
            warnings.warn(str(f"{e} : Your objects will not be registered"), RuntimeWarning)

    @classmethod
    def set_first_state(cls, state_name):
        try:
            instance = cls.get_instance()
            instance._first_state_name = state_name
        except PyTRobotNotInitializedException as e:
            warnings.warn(str(f"{e} : Your objects will not be registered"), RuntimeWarning)

# Decoradores

def State(cls):
    PyTRobot.add_object_on_registry(cls)
    return cls

def Tool(cls):
    PyTRobot.add_object_on_registry(cls)
    return cls

def First(cls):
    PyTRobot.set_first_state(cls.__name__)
    return cls

def Transition(current_state_name, next_state_on_success_name, next_state_on_failure_name):
    def decorator(cls):
        if current_state_name is None:
            raise ValueError("O nome do estado atual não pode ser None.")
        if next_state_on_success_name is None:
            raise ValueError("O nome do próximo estado para sucesso não pode ser None.")
        if next_state_on_failure_name is None:
            raise ValueError("O nome do próximo estado para falha não pode ser None.")

        # Adiciona a transição usando o método de classe do PyTRobot
        PyTRobot.add_transition_on_true_table(current_state_name, next_state_on_success_name, next_state_on_failure_name)
        return cls
    return decorator