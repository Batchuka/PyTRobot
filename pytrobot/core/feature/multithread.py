# pytrobot/core/feature/multithread.py

import threading
import logging
from pytrobot.core.singleton import Singleton

class MultithreadManager(metaclass=Singleton):
    def __init__(self):
        self.threads = {}
        self.logger = logging.getLogger('PyTRobot')

    def new_thread(self, func, join=False):
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
            self.logger.info(f"The thread for {full_invocation} is already running.")
            return
        else:
            self.logger.info(f"Starting new thread for {full_invocation}.")
            thread = threading.Thread(target=func, daemon=True)
            self.threads[full_invocation] = thread
            thread.start()
            if join:thread.join() # Se join for True, aguarde o término da thread
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
                self.logger.info(f"Ending the {full_invocation} .")
                # Python não suporta finalização direta de threads, você precisará de lógica específica para cada thread
                # para verificar um flag e terminar a execução de forma limpa.
                # Aqui você pode setar um flag e deixar a thread verificar esse flag para terminar.
            else:
                self.logger.warning(f"Thread {full_invocation} is no longer active.")
        else:
            self.logger.warning(f"No threads found for {full_invocation}.")
    
    def list_active_threads(self):
        """
        Lista todas as threads ativas gerenciadas pelo MultithreadManager.
        """
        active_threads = {name: thread for name, thread in self.threads.items() if thread.is_alive()}
        self.logger.info(f"Active threads count: {len(active_threads)}")
        for name, thread in active_threads.items():
            self.logger.info(f"Thread name: {name}, Thread id: {thread.ident}")

    def get_number_active_threads(self) -> int:
        """
        Retorna o número de threads ativas gerenciadas pelo MultithreadManager.
        """
        active_threads = {name: thread for name, thread in self.threads.items() if thread.is_alive()}
        return len(active_threads)
            