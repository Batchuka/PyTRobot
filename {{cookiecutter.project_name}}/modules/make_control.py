from config import *
import schedule
import os


def look_for_transaction_item(self):

    if Bag.transaction_item:
        # se hourve item, vai para o perfomer processar e mata todos schedules ativos
        kill_pending_schedule()
        self.next_state = State.PERFORMER
    else:
        if len(schedule.get_jobs()) == 0:
            # quando não há schedules, vai para dispatcher criar um
            self.next_state = State.DISPATCHER
        else:
            # verifica se os schedules ativos atingiram a hora atual
            run_pending_schedule()
            self.next_state = State.CONTROLLER


def run_pending_schedule():
    # procura pelos schedules ativos
    schedule.run_pending()


def kill_pending_schedule():
    # limpa qualquer schedule ativo
    schedule.clear()


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

def delete_input_json():
    
    if os.path.exists(Bag.transaction_item["input_json"]):
        os.remove(Bag.transaction_item["input_json"])
    
    Bag.transaction_item = {}
