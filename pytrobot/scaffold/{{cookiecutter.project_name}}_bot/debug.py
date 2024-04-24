# debug.py
from pytrobot import debug, auto_import
dir='/diretorio/para/{{cookiecutter.project_name}}' # ← Coloque o caminho para {{cookiecutter.project_name}}
auto_import(directory=dir)
debug(directory=dir)