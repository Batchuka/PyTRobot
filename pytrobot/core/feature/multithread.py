# pytrobot/core/feature/multithread.py

import threading
from pytrobot.core.singleton import Singleton

class MultithreadManager(metaclass=Singleton):
    def __init__(self):
        self.threads = {}

    def new_thread(self, func):
        """
        Executa a função em uma nova thread e gerencia a thread.
        Garante que a função não crie múltiplas threads simultaneamente.
        """
        # Captura o nome do módulo onde a função foi definida
        module_name = func.__module__
        
        # Captura o nome da função
        func_name = func.__name__
        
        # Monta a linha de invocação completa
        full_invocation = f"{module_name}.{func_name}_thread"

        if full_invocation in self.threads and self.threads[full_invocation].is_alive():
            print(f"The thread for {full_invocation} is already running.")
            return
        else:
            print(f"Starting new thread for {full_invocation}.")
            thread = threading.Thread(target=func, daemon=True)
            self.threads[full_invocation] = thread
            thread.start()
            return thread

    def stop_thread(self, func):
        """
        Finaliza a thread associada à função fornecida.
        """

        # Captura o nome do módulo onde a função foi definida
        module_name = func.__module__
        
        # Captura o nome da função
        func_name = func.__name__
        
        # Monta a linha de invocação completa
        full_invocation = f"{module_name}.{func_name}_thread"

        if full_invocation in self.threads:
            thread = self.threads[full_invocation]
            if thread.is_alive():
                print(f"Ending the {full_invocation} .")
                # Python não suporta finalização direta de threads, você precisará de lógica específica para cada thread
                # para verificar um flag e terminar a execução de forma limpa.
                # Aqui você pode setar um flag e deixar a thread verificar esse flag para terminar.
            else:
                print(f"Thread {full_invocation} is no longer active.")
        else:
            print(f"No threads found for {full_invocation}.")
    
    def list_active_threads(self):
        """
        Lista todas as threads ativas gerenciadas pelo MultithreadManager.
        """
        active_threads = {name: thread for name, thread in self.threads.items() if thread.is_alive()}
        print(f"Active threads count: {len(active_threads)}")
        for name, thread in active_threads.items():
            print(f"Thread name: {name}, Thread id: {thread.ident}")