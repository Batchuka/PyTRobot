# pytrobot/core/objects.py

class ObjectsRegister:
    def __init__(self):
        self._registry = {}

    def register(self, name, obj):
        if name in self._registry:
            raise ValueError(f"Objeto com nome '{name}' já registrado.")
        self._registry[name] = obj

    def get(self, name):
        return self._registry.get(name, None)

    def is_registered(self, name):
        return name in self._registry


class AccessObjectLayer:
    def __init__(self, pytrobot_instance):
        self.pytrobot_instance = pytrobot_instance

    def register(self, object_cls):
        self.pytrobot_instance.objects_register.register(object_cls.__name__, object_cls)
        return object_cls

    def get(self, name):
        return self.pytrobot_instance.objects_register.get(name)

    def is_registered(self, name):
        return name in self.pytrobot_instance.objects_register._registry
