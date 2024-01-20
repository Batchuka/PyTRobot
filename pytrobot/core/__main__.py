import sys
import os

from pytrobot.core.states import *
from pytrobot.core.true_table import get_next_state

user = os.path.join(os.getcwd(), 'user')


def run(dir=user):
    state = Starter(dir)

    while True:
        state.on_entry()

        if state.status == True:
            state.execute()

        # Se o status for False ou após executar
        if state.status == True:
            state.on_exit()
        else:
            state.on_error()

        # Determinar o próximo estado com base na lógica de transições
        state = get_next_state(state)


def entrypoint() -> None:
    if len(sys.argv) != 3:
        print("Usage: trt <command> <directory>")
    else:
        command = sys.argv[1]
        if command == 'run':
            run(sys.argv[2])
        else:
            print(f"Unknown command: {command}")

if __name__ == '__main__':
    entrypoint()
    
