from pytrobot import BaseState

class _FinisherState(BaseState):

    def execute(self):
        pass

    def on_entry(self):
        pass

    def on_exit(self):
        
        import threading

        # Imprime a contagem de threads ativas antes de sair
        print(f'Active threads count: {threading.active_count()}')
        print('Active threads:', threading.enumerate())

        exit()

    def on_error(self):

        import os
        os._exit(0)
