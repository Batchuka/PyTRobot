from abc import ABC, abstractmethod


class BaseState(ABC):

    def __str__(self) -> str:
        return f"State {self.__class__.__name__}"

    def __init__(self, access_dataset_layer, access_object_layer):
        self.access_dataset_layer = access_dataset_layer
        self.access_object_layer = access_object_layer
        self._status = None

    def get_action(self, action_class):
        action = self.access_object_layer.get(action_class)
        action = action(self.access_dataset_layer, self.access_object_layer)
        return action

    def get_tool(self, tool_class):
        tool = self.access_object_layer.get(tool_class)
        tool = tool(self.access_object_layer, self.access_dataset_layer)
        return tool

    def get_tool_i(self, tool_instance):
        tool = self.access_object_layer.get_instance(tool_instance)
        # tool = tool(self.access_object_layer, self.access_dataset_layer)
        return tool

    def register_tool_i(self, tool_instance):
        self.access_object_layer.register_instance(tool_instance)
        return tool_instance
    
    def get_asset(self, asset_name):
        return self.access_dataset_layer.get_asset(asset_name)

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
        print(f"=====> Executando : {self.__class__.__name__}")
        method = getattr(self, 'execute', None)
        if method:
            method()
        else:
            raise NotImplementedError("O método 'execute' deve ser implementado pela subclasse.")

    def _on_entry(self):
        print(f"=====> Iniciando : {self.__class__.__name__}")
        method = getattr(self, 'on_entry', None)
        if method:
            method()
        else:
            raise NotImplementedError("O método 'on_entry' deve ser implementado pela subclasse.")

    def _on_exit(self):
        self._status = True
        print(f"=====> Sucesso no : {self.__class__.__name__}")
        method = getattr(self, 'on_exit', None)
        if method:
            method()
        else:
            self._status = False
            raise NotImplementedError("O método 'on_exit' deve ser implementado pela subclasse.")

    def _on_error(self, error):
        self._status = False
        print(f"=====> Falha no : {self.__class__.__name__}")
        method = getattr(self, 'on_error', None)
        if method:
            method(error)
        else:
            raise NotImplementedError(f"O método 'on_error' deve ser implementado pela subclasse. Erro: {error}")