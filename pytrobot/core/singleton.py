# pytrobot\core\singleton.py

from abc import ABCMeta

class Singleton(ABCMeta):
    """Metaclass to create a Singleton class.
    Singleton instances ensure that only one instance of the class is created.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
