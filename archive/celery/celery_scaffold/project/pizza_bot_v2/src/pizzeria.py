# pytrobot/scaffold/celery/project/pizzeria_bot/src/pizzeria.py

from .pizza import Pizza

class Pizzeria:
    def __init__(self):
        pass

    def order(self, flavor, slices):
        """
        Recebe o sabor da pizza e o número de fatias para criar uma instância de Pizza.
        """
        # Retorna uma nova instância de Pizza com os detalhes fornecidos
        return Pizza(flavor=flavor, slices=slices)

    def __str__(self):
        return f"Pizzeria ready to make a pizza."