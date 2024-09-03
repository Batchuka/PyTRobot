# pytrobot/core/decortador/multithread.py

from pytrobot.core.feature.multithread import MultithreadManager

def Thread(func):
    """
    Proxy para o decorador @Thread do PyTRobot.
    """
    multithread_manager = MultithreadManager()
    return multithread_manager.thread(func)