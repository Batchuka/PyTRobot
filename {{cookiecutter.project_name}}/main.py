from framework import *


def run():

    Config.load_config()
    Config.set_assets()
    Config.set_config()
    robot = Starter()

    while True:

        robot.on_entry()

        if robot.status == True:

            robot.execute()

            if robot.status == True:

                # Se NÂO HOUVER exceções "on_exit" define o "next_state"
                robot.on_exit()
                # Método da super classe para atualizar a instância
                robot = eval(robot.next_state.value+"()")

            elif robot.status == False:

                # Se HOUVER exceções "on_error" define o "next_state"
                robot.on_error()
                # Método da super classe para atualizar a instância
                robot = eval(robot.next_state.value+"()")

        elif robot.status == False:

            # Se HOUVER exceções "on_error" define o "next_state"
            robot.on_error()
            # Método da super classe para atualizar a instância
            robot = eval(robot.next_state.value+"()")


# é possível configurar valores na Bag
if __name__ == "__main__":
    run()
