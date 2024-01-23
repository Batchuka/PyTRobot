# pytrobot/core/objects.py

class ObjectsLayer:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise ValueError("ObjectsLayer já foi instanciada!")
        self._registry = {}

    def register_state(self, cls):
        self._registry[cls.__name__] = cls
        return cls

    def register_tool(self, cls):
        self._registry[cls.__name__] = cls
        return cls
    
    def register_action(self, cls):
        self._registry[cls.__name__] = cls
        return cls
