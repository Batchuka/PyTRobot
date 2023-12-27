# pytrobot/__init__.py

from invoke import Program, Collection, Argument #type:ignore
import tasks
__version__ = '2.0.0'

class MyProgram(Program):
    def core_args(self):
        core_args = super().core_args()
        extra_args = [
            Argument(names=('build', 'b'), help="Build the pytrobot project")
            # Adicione mais argumentos conforme necessário
        ]
        return core_args + extra_args

# Crie uma instância do seu programa personalizado
program = MyProgram(namespace=Collection.from_module(tasks), version=__version__)