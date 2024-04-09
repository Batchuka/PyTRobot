from abc import ABC, abstractmethod
from pytrobot.core.dataset_layer import AccessDatasetLayer
from pytrobot.core.object_layer import AccessObjectLayer
from pytrobot.core.machine_layer import AccessMachineLayer

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'

class BaseState(ABC):

    access_dataset_layer : AccessDatasetLayer
    access_object_layer : AccessObjectLayer
    access_machine_layer : AccessMachineLayer

    def __str__(self) -> str:
        return f"State {self.__class__.__name__}"

    def __init__(self, access_dataset_layer, access_object_layer, access_machine_layer):
        self.access_dataset_layer = access_dataset_layer
        self.access_object_layer = access_object_layer
        self.access_machine_layer = access_machine_layer
        self._status = None
        self.retry_counter = 0
        self.reset = False
    
    def create_tdata(self, name, columns, data=None):
        return self.access_dataset_layer.create_transaction_data(name, columns)

    def get_tool(self, class_name):
        entry = self.access_object_layer._get(class_name)

        if entry is None:
            raise ValueError(f"Tool {class_name} not registered.")

        if not entry["is_instance"]:
            object = entry["object"]
            instance = object(self.access_dataset_layer) 
            self.access_object_layer.register(class_name, instance, is_instance=True)
            return instance
        else:
            return entry["instance"]
    
    def get_tdata(self, transaction_data_name):
        tdata = self.access_dataset_layer.get_transaction_data(transaction_data_name)
        return tdata

    def get_asset(self, asset_name):
        return self.access_dataset_layer.get_asset(asset_name)

    def set_asset(self, asset_name, asset_value):
        return self.access_dataset_layer.set_asset(asset_name, asset_value)

    def transition(self, current_state, next_state_on_success=None, next_state_on_failure=None):
        """
        Update transition in TrueTable.
        
        :param current_state: Current state.
        :param next_state_on_success: Next state on success.
        :param next_state_on_failure: Next state on failure.
        """
        current_state_name = self.__class__.__name__
        self.access_machine_layer.transition(
            current_state=current_state_name,
            next_state_on_success=next_state_on_success,
            next_state_on_failure=next_state_on_failure
        )

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def on_entry(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass

    @abstractmethod
    def on_error(self, error):
        pass

    def _execute(self):
        print(f"{BLUE} ===== Executando ===== {self.__class__.__name__} {RESET}")
        method = getattr(self, 'execute', None)
        if method:
            method()
        else:
            raise NotImplementedError("O método 'execute' deve ser implementado pela subclasse.")

    def _on_entry(self):
        print(f"{BLUE} ===== Iniciando ====== {self.__class__.__name__} {RESET}")
        method = getattr(self, 'on_entry', None)
        if method:
            method()
        else:
            raise NotImplementedError("O método 'on_entry' deve ser implementado pela subclasse.")

    def _on_exit(self):
        self._status = True
        print(f"{BLUE} ===== Sucesso ======== {self.__class__.__name__} {RESET}")
        method = getattr(self, 'on_exit', None)
        if method:
            method()
        else:
            self._status = False
            raise NotImplementedError("O método 'on_exit' deve ser implementado pela subclasse.")

    def _on_error(self, error):
        self._status = False
        print(f"{RED} ===== Falha ========== {self.__class__.__name__} \n {error}{RESET} ")
        method = getattr(self, 'on_error', None)
        if method:
            if self.retry_counter > 0:
                self.retry_counter -= 1
                print(f"Tentativa falhou. Restam {self.retry_counter} tentativas.")
                self.reset = True
            else:
                print("Número máximo de tentativas alcançado.")
                self.reset = False
            return method(error)
        else:
            raise NotImplementedError(f"O método 'on_error' deve ser implementado pela subclasse. Erro: {error}")