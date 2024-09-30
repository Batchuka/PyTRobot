# pytrobot/core/decortador/multithread.py

from pytrobot.core.feature.multithread import MultithreadManager

# def Thread(func):
#     """
#     Proxy para o decorador @Thread do PyTRobot.
#     """
#     multithread_manager = MultithreadManager()
#     return multithread_manager.new_thread(func)

def Thread(func):
    """
    Proxy para o decorador @Thread do PyTRobot.
    """
    multithread_manager = MultithreadManager()
    
    def wrapper(*args, **kwargs):
        # A função decorada é passada para a execução da thread
        thread = multithread_manager.new_thread(lambda: func(*args, **kwargs))
        return thread

    return wrapper