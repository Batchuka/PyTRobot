# pytrobot/core/strategy/state_strategy.py
from pytrobot.core.strategy.robot_strategy import RobotStrategy
from pytrobot.core.strategy.state.machine import StateMachine, TrueTable
from pytrobot.core.feature.multithread import MultithreadManager
from pytrobot.core.feature.subprocess import SubprocessManager

class StateStrategy(RobotStrategy):

    def __init__(self):
        self.state_machine : StateMachine
        self.multithread_manager = None
        self.subprocess_manager = None

    def initialize(self):
        self.state_machine = StateMachine(true_table=TrueTable())
        self.multithread_manager = MultithreadManager()
        self.subprocess_manager = SubprocessManager()

    def _initialize(self):
        self.state_machine = StateMachine(true_table=TrueTable())
        self.multithread_manager = MultithreadManager()
        self.subprocess_manager = SubprocessManager()
        self._initialized = True

    def _register_core_states(self):

        State(_StarterState)
        if self._first_state_name:
            State(self._first_state_name, '_FinisherState')(_StarterState)
        else:
            State('_FinisherState', '_FinisherState')(_StarterState)
        State(_FinisherState)
        State('_FinisherState', '_FinisherState')(_FinisherState)

    def start(self):
        self.state_machine.run()

    # Métodos de acesso para os decoradores

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise PyTRobotNotInitializedException("PyTRobot object is not initialized.")
        return cls._instance

    # Função proxy para o decorador @First
    @classmethod
    def set_first_state(cls, state_name):
        try:
            instance = cls.get_instance()
            instance._first_state_name = state_name
        except PyTRobotNotInitializedException as e:
            warnings.warn(
                str(f"{e} : Your objects will not be registered"), RuntimeWarning)

    @classmethod
    def set_thread(cls, func):
        def wrapper(*args, **kwargs):
            try:
                instance = cls.get_instance()
                thread_decorator = instance.multithread_manager.thread(func)
                return thread_decorator(*args, **kwargs)
            except PyTRobotNotInitializedException as e:
                warnings.warn(str(e), RuntimeWarning)
                return None
        return wrapper

    @classmethod
    def set_subprocess(cls, comando, captura_saida=True, captura_erro=True):
        if not isinstance(comando, list):
            raise ValueError("O comando deve ser uma lista de strings.")
        return cls().subprocess_manager.executar_subprocesso(comando, captura_saida, captura_erro)

