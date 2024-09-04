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

@cli.command()
@click.argument('output_path', required=False, default='.')
def project(output_path):
    """Cria um novo projeto PyTrobot no caminho especificado (ou no diretório atual se não for informado)."""
    # Verifica se o caminho fornecido é relativo ou absoluto
    output_path = str(Path(output_path).resolve())  # Converta para string e resolva o caminho completo
    scaffold_path = str(Path(project_scaffold.__file__).resolve().parent)  # Converta para string

    try:
        # O cookiecutter já perguntará o nome do projeto automaticamente
        cookiecutter(template=scaffold_path, output_dir=output_path)
        print(f"Projeto criado com sucesso em: {output_path}")
    except Exception as e:
        print(f"Erro ao criar o projeto: {str(e)}")

# if __name__ == "__main__":
#     project()
