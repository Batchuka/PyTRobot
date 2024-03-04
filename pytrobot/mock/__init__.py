# mock.py
import pathlib
from pytrobot import PyTRobot

__all__ = ['Mock']

# Supondo que PyTRobot já tenha sido importado e esteja disponível

class Mock:
    def __init__(self, tool_class, dir):
        # Cria uma instância do PyTRobot (ou obtém a instância única, se for um Singleton)
        pytrobot_instance = PyTRobot()

        base_path = pathlib.Path(dir)
        resources_path = base_path / "resources"

        # Verifica se o diretório resources existe e o adiciona no PyTRobot
        if resources_path.exists():
            pytrobot_instance._resources = resources_path.as_posix()
            pytrobot_instance.config_data.load_config(resources_path.as_posix())
        else:
            raise FileNotFoundError("Diretório resources não encontrado ou não especificado corretamente.")
        
    
        # Usa os métodos do PyTRobot para criar as camadas necessárias
        access_dataset_layer = pytrobot_instance.create_access_dataset_layer()
        #access_object_layer = pytrobot_instance.create_access_object_layer()
        #access_machine_layer = pytrobot_instance.create_access_machine_layer()

        # Inicializa a tool_class com as instâncias criadas
        self.tool_instance =  tool_class(access_dataset_layer)