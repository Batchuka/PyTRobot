# pytrobot/scaffold/celery/project/pizzeria_bot/src/pizza.py

from pytrobot.core.singleton import Singleton

class Pizza(metaclass=Singleton):
    
    def __init__(self, flavor=None, slices=0):
        self.flavor = flavor
        self.total_slices = slices
        self.slices_eaten = 0
    
    def eat_slice(self):
        self.slices_eaten += 1
    
    def is_satisfied(self):
        return self.slices_eaten >= self.total_slices
    
    def __str__(self):
        return f"Pizza: {self.flavor}, Total slices: {self.total_slices}, Slices eaten: {self.slices_eaten}"
