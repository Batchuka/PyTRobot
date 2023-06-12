from framework import *
from config import *

# global transaction_data   # <List<rows>> tabela que guarda itens da execução — cada item, é uma trasação a ser feita
# global transaction_number # <int> é um int que representa o número da transação atual do robô;
# global transaction_item   # <row> é um item da tabela transaction_data, que está sendo manipulado no momento;
# global debugger_mode      # <bool> que faz robô printar info adicional para debug
# global enviroment_type    # <enum> usada para definir o ambiente onde está sendo executado o que pode mudar seu comportamento;


def run():

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
    Bag.debugger_mode = True
    run()
