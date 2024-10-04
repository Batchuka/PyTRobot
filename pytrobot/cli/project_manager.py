# # pilot/src/pytrobot.py
# from pathlib import Path
# from shutil import copyfile
# from cookiecutter.main import cookiecutter
# from pilot.base.manager import BaseManager

# # TODO : Implementar o scaffold de outros objetos 'classes' e 'tests'

# # Importa os módulos diretamente para obter o caminho dos scaffolds
# import pytrobot.scaffold.project as project_scaffold
# # import pytrobot.scaffold.state as state_scaffold
# # import pytrobot.scaffold.celery as celery_scaffold

# class PytrobotManager(BaseManager):

#     def __init__(self):
#         super().__init__()
#         self.section_name = 'pytrobot'
#         self.default_section = 'default_pytrobot'

#     def init(self, **kwargs):
#         raise NotImplementedError

#     def update(self, **kwargs):
#         raise NotImplementedError

#     def new(self):
#         """Cria um novo projeto PyTrobot ou classes de estado/tarefas de forma interativa."""

#         # Exibe as opções para o usuário
#         print("Escolha o que deseja criar:")
#         print("1. Project")
#         # print("2. State Class")
#         # print("3. Task  Class")
#         # print("4. State Test")
#         # print("5. Task  Test")

#         option = input("Selecione o número correspondente (1-5): ")

#         # Baseado na escolha do usuário, realiza a ação correspondente
#         if option == '1':
#             name = input("Digite o nome do novo projeto: ")
#             self.create_project(name)
#         # elif option == '2':
#         #     name = input("Digite o nome da nova classe State: ")
#         #     self.create_state_class(name)
#         # elif option == '3':
#         #     name = input("Digite o nome da nova classe Task: ")
#         #     self.create_task_class(name)
#         # elif option == '4':
#         #     name = input("Digite o nome do novo teste de State: ")
#         #     self.create_test_state(name)
#         # elif option == '5':
#         #     name = input("Digite o nome do novo teste de Task: ")
#         #     self.create_test_task(name)
#         else:
#             print("Opção inválida. Tente novamente.")

#     def create_project(self, name):
#         """Cria um novo projeto PyTrobot usando cookiecutter."""
#         self.log.info(f"Criando novo projeto PyTrobot '{name}'...")
#         output_path = Path.cwd()
#         scaffold_path = Path(project_scaffold.__file__).resolve().parent / "project"
#         try:
#             cookiecutter(template=scaffold_path, extra_context={'project_name': name}, output_dir=str(output_path))
#             self.log.info(f"Projeto '{name}' criado com sucesso.")
#         except Exception as e:
#             self.log.error(f"Erro ao criar o projeto: {str(e)}")

#     # def create_state_class(self, name):
#     #     """Cria uma nova classe state usando cookiecutter."""
#     #     self.log.info(f"Criando nova classe State '{name}'...")
#     #     output_path = Path.cwd()
#     #     scaffold_path = Path(state_scaffold.__file__).resolve().parent / "state"
#     #     try:
#     #         cookiecutter(template=scaffold_path, extra_context={'class_name': name}, output_dir=str(output_path))
#     #         self.log.info(f"Classe State '{name}' criada com sucesso.")
#     #     except Exception as e:
#     #         self.log.error(f"Erro ao criar a classe State: {str(e)}")

#     # def create_task_class(self, name):
#     #     """Cria uma nova classe task usando cookiecutter."""
#     #     self.log.info(f"Criando nova classe Task '{name}'...")
#     #     output_path = Path.cwd()
#     #     scaffold_path = Path(celery_scaffold.__file__).resolve().parent / "celery"
#     #     try:
#     #         cookiecutter(template=scaffold_path, extra_context={'class_name': name}, output_dir=str(output_path))
#     #         self.log.info(f"Classe Task '{name}' criada com sucesso.")
#     #     except Exception as e:
#     #         self.log.error(f"Erro ao criar a classe Task: {str(e)}")

#     # def create_test_state(self, name):
#     #     """Cria um novo teste para uma classe state usando cookiecutter."""
#     #     self.log.info(f"Criando novo teste de State '{name}'...")
#     #     output_path = Path.cwd()
#     #     scaffold_path = Path(state_scaffold.__file__).resolve().parent / "state"
#     #     try:
#     #         cookiecutter(template=scaffold_path, extra_context={'class_name': name, 'test': True}, output_dir=str(output_path))
#     #         self.log.info(f"Teste de State '{name}' criado com sucesso.")
#     #     except Exception as e:
#     #         self.log.error(f"Erro ao criar o teste de State: {str(e)}")

#     # def create_test_task(self, name):
#     #     """Cria um novo teste para uma classe task usando cookiecutter."""
#     #     self.log.info(f"Criando novo teste de Task '{name}'...")
#     #     output_path = Path.cwd()
#     #     scaffold_path = Path(celery_scaffold.__file__).resolve().parent / "celery"
#     #     try:
#     #         cookiecutter(template=scaffold_path, extra_context={'class_name': name, 'test': True}, output_dir=str(output_path))
#     #         self.log.info(f"Teste de Task '{name}' criado com sucesso.")
#     #     except Exception as e:
#     #         self.log.error(f"Erro ao criar o teste de Task: {str(e)}")

