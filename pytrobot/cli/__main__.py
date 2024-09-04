# pytrobot/cli/__main__.py
import click
from pathlib import Path
from cookiecutter.main import cookiecutter

# Importando scaffolds
import pytrobot.scaffold.project as project_scaffold
import pytrobot.scaffold.state as state_scaffold
import pytrobot.scaffold.celery as celery_scaffold


@click.group()
def cli():
    """CLI para gerenciar scaffolds do PyTrobot."""
    pass


@cli.group()
def new():
    """Comando para criar novos scaffolds."""
    pass


@new.command()
@click.argument('name')
def project(name):
    """Cria um novo projeto PyTrobot."""
    output_path = Path.cwd()
    scaffold_path = Path(project_scaffold.__file__).resolve().parent / "project"
    try:
        cookiecutter(template=scaffold_path, extra_context={'project_name': name}, output_dir=str(output_path))
        print(f"Projeto '{name}' criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o projeto: {str(e)}")


# @new.command()
# @click.argument('name')
# def state(name):
#     """Cria uma nova classe de estado e o teste correspondente."""
#     output_path = Path.cwd()
    
#     # Cria a classe state
#     state_scaffold_path = Path(state_scaffold.__file__).resolve().parent / "state"
#     try:
#         cookiecutter(template=state_scaffold_path, extra_context={'class_name': name}, output_dir=str(output_path))
#         print(f"Classe State '{name}' criada com sucesso.")
#     except Exception as e:
#         print(f"Erro ao criar a classe State: {str(e)}")

#     # Cria o teste correspondente para a classe state
#     test_state_scaffold_path = Path(state_scaffold.__file__).resolve().parent / "state"
#     try:
#         cookiecutter(template=test_state_scaffold_path, extra_context={'class_name': f"test_{name}"}, output_dir=str(output_path))
#         print(f"Teste para a classe State '{name}' criado com sucesso.")
#     except Exception as e:
#         print(f"Erro ao criar o teste de State: {str(e)}")


# @new.command()
# @click.argument('name')
# def task(name):
#     """Cria uma nova classe de tarefa (task) e o teste correspondente."""
#     output_path = Path.cwd()

#     # Cria a classe task
#     task_scaffold_path = Path(celery_scaffold.__file__).resolve().parent / "celery"
#     try:
#         cookiecutter(template=task_scaffold_path, extra_context={'class_name': name}, output_dir=str(output_path))
#         print(f"Classe Task '{name}' criada com sucesso.")
#     except Exception as e:
#         print(f"Erro ao criar a classe Task: {str(e)}")

#     # Cria o teste correspondente para a classe task
#     test_task_scaffold_path = Path(celery_scaffold.__file__).resolve().parent / "celery"
#     try:
#         cookiecutter(template=test_task_scaffold_path, extra_context={'class_name': f"test_{name}"}, output_dir=str(output_path))
#         print(f"Teste para a classe Task '{name}' criado com sucesso.")
#     except Exception as e:
#         print(f"Erro ao criar o teste de Task: {str(e)}")


if __name__ == '__main__':
    cli()
