# debug.py
import os
from pytrobot import debug, auto_import_states

# Obtém o diretório atual onde debug.py está localizado
current_directory = os.path.dirname(os.path.abspath(__file__))

# Constrói o caminho para o diretório do projeto adicionando o nome do projeto
# Aqui, '{{cookiecutter.project_name}}' é o nome do diretório do projeto que você precisa ajustar para o seu caso específico
project_directory = os.path.join(current_directory, '{{cookiecutter.project_name}}')

# Configura automaticamente os imports e inicia o debug
auto_import_states(directory=project_directory)
debug(directory=project_directory)