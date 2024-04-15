# pytrobot/core/objects_layer.py


class ObjectsRegister:
    def __init__(self):
        self._registry = {}

    def register(self, name, object_cls, instance=None, is_instance=False):
        """
        Registra ou atualiza uma referência à classe no registro.
        'is_instance' é usado para indicar se a referência é uma instância ou uma classe.
        Os objetos são registrados como referências de classe por padrão (is_instance=False).
        Se um objeto com o mesmo nome já estiver registrado, o registro é atualizado.
        """
        # Verifica se o objeto já está registrado e decide se deve atualizar ou criar um novo registro
        if name in self._registry:
            # Atualiza apenas 'instance' e 'is_instance', mantendo 'object' como está
            self._registry[name]["instance"] = instance
            self._registry[name]["is_instance"] = is_instance
            print(f"Registro para '{name}' atualizado com nova instância.")
        else:
            # Cria um novo registro
            self._registry[name] = {"object": object_cls, "instance": instance, "is_instance": is_instance}

    """ NOTE
    Nunca altere esse método, ele é ativamente utilizado pela máquina de estados.
    """
    def _get(self, name):
        entry = self._registry.get(name)
        # if entry and not entry["is_instance"]:
        #     return entry
        # return None
        if not entry:
            raise ValueError("This object is not registered")
        return entry

