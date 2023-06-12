from config import *
import schedule
import os


def kill_schedule():
    # limparemos qualquer schedule ativo, pois não queremos mais observar a fila
    schedule.clear()


def look_for_transaction_item(self):

    print(Bag.transaction_item)

    if Bag.transaction_item:
        kill_schedule()
        self.next_state = State.PERFORMER
    else:
        if len(schedule.get_jobs()) == 0:
            self.next_state = State.DISPATCHER
        else:
            self.next_state = State.CONTROLLER


def delete_all_temp_files():

    temp_directory = 'temp'

    # Verifica se o diretório temporário existe
    if os.path.exists(temp_directory) and os.path.isdir(temp_directory):
        # Obtém a lista de arquivos no diretório temporário
        files = os.listdir(temp_directory)

        for file in files:
            # Verifica se o arquivo é diferente de 'placeholder.txt'
            if file != 'placeholder.txt':
                file_path = os.path.join(temp_directory, file)
                # Verifica se o caminho é um arquivo
                if os.path.isfile(file_path):
                    # Exclui o arquivo
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
    else:
        print(f"Temporary directory '{temp_directory}' not found")
