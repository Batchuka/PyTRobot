# pytrobot/core/objects.py

class ObjectsRegister:
    def __init__(self):
        self._registry = {}

    def register(self, name, obj, is_instance=False):
        if name in self._registry:
            raise ValueError(f"Objeto com nome '{name}' já registrado.")
        self._registry[name] = {"object": obj, "is_instance": is_instance}

    def register_instance(self, name, obj, is_instance=True):
        if name in self._registry:
            raise ValueError(f"Objeto com nome '{name}' já registrado.")
        self._registry[name] = {"object": obj, "is_instance": is_instance}

    def get(self, name):
        entry = self._registry.get(name)
        if entry and not entry["is_instance"]:
            return entry["object"]
        return None

    def get_instance(self, name):
        entry = self._registry.get(name)
        if entry and entry["is_instance"]:
            return entry["object"]
        return None

    def is_registered(self, name):
        return name in self._registry
    
    def is_instance(self, name):
        entry = self._registry.get(name, None)
        if entry is not None:
            return entry["is_instance"]
        return False


class AccessObjectLayer:
    def __init__(self, pytrobot_instance):
        self.pytrobot_instance = pytrobot_instance

    def register(self, object_cls):
        name = object_cls.__class__.__name__
        self.pytrobot_instance.objects_register.register(name, object_cls)
        return object_cls

    def register_instance(self, object__instance):
        name = object__instance.__class__.__name__ + "_instance"
        self.pytrobot_instance.objects_register.register_instance(name, object__instance)
        return object__instance

    
    def get(self, name):
        return self.pytrobot_instance.objects_register.get(name)

    def get_instance(self, name):
        return self.pytrobot_instance.objects_register.get_instance(name)

    def is_registered(self, name):
        return name in self.pytrobot_instance.objects_register._registry
