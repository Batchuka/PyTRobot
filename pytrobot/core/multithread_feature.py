# multithread_feature.py

import threading
from functools import wraps
from pytrobot.core.singleton import Singleton

class MultithreadManager(metaclass=Singleton):
    def __init__(self):
        self.threads = {}

    def thread(self, func):
        """
        Decorador para executar a função decorada em uma nova thread e gerenciar a thread.
        Garante que a função não crie múltiplas threads simultaneamente.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            instance = args[0]  # A primeira arg é a instância de `self`
            thread_name = f"_{func.__name__}_thread"
            
            if thread_name in self.threads and self.threads[thread_name].is_alive():
                print(f"The thread for {func.__name__} is already running.")
                return
            else:
                print(f"Starting new thread for {func.__name__}.")
                thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
                self.threads[thread_name] = thread
                thread.start()
                return thread
        return wrapper

    def stop_thread(self, func_name):
        """
        Finaliza a thread associada à função fornecida.
        """
        thread_name = f"_{func_name}_thread"
        if thread_name in self.threads:
            thread = self.threads[thread_name]
            if thread.is_alive():
                print(f"Ending the {func_name} thread.")
                # Python não suporta finalização direta de threads, você precisará de lógica específica para cada thread
                # para verificar um flag e terminar a execução de forma limpa.
                # Aqui você pode setar um flag e deixar a thread verificar esse flag para terminar.
            else:
                print(f"Thread {func_name} is no longer active.")
        else:
            print(f"No threads found for {func_name}.")
    
    def list_active_threads(self):
        """
        Lista todas as threads ativas gerenciadas pelo MultithreadManager.
        """
        active_threads = {name: thread for name, thread in self.threads.items() if thread.is_alive()}
        print(f"Active threads count: {len(active_threads)}")
        for name, thread in active_threads.items():
            print(f"Thread name: {name}, Thread id: {thread.ident}")