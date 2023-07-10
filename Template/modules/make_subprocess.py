from config import *
import subprocess


def launch():

    # obtem caminho do input
    input_json = Bag.transaction_item["input_json"]

    # pega o main e o venv do projeto pelo idRobo
    _project_name = Bag.transaction_item['project_name']
    try:
        print(Bag.list_of_projects)
        project_info = list(filter(
            lambda project: project['project_name'] == _project_name, Bag.list_of_projects))
        if project_info:
            project_info = project_info[0]
            venv_path = project_info['venv_path']
            main_path = project_info['main_path']
        else:
            raise Exception("Project not found")
    except:
        raise Exception("Error retrieving project information")

    if Bag.xvfb == False:
        # Comando para executar o main.py com xvfb e o arquivo JSON como argumentos
        comando = [venv_path, main_path, input_json]
        print(comando)
    else:
        # Comando para executar o main.py com xvfb e o arquivo JSON como argumentos
        comando = ["xvfb-run", venv_path, main_path, input_json]
        print(comando)

    # Chama a função main passando o JSON usando threading
    subprocess.run(comando)
