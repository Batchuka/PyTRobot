import sys
import os

from pytrobot.starter import Starter
from pytrobot.state import go_next_state

user = os.path.join(os.getcwd(), 'user')

def run(dir=user):

    robot = Starter(dir)

    while True:

        robot.on_entry()

        if robot.status == True:

            robot.execute()

            if robot.status == True:

                # Se NÂO HOUVER exceções "on_exit" define o "next_state"
                robot.on_exit()
                # Método da super classe para atualizar a instância
                robot = go_next_state(robot.next_state)

            elif robot.status == False:

                # Se HOUVER exceções "on_error" define o "next_state"
                robot.on_error()
                # Método da super classe para atualizar a instância
                robot = go_next_state(robot.next_state)

        elif robot.status == False:

            # Se HOUVER exceções "on_error" define o "next_state"
            robot.on_error()
            # Método da super classe para atualizar a instância
            robot = go_next_state(robot.next_state)


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
    
"""
→ Tenho planos para os métodos 'on'. O objeto será instanciar coisas neles 
que de alguma forma fiquem guardadas no estado e possam ser recuperadas 
pelo usuário fora.
"""