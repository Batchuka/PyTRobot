import time

from pytrobot.core.singleton import Singleton

class Pizza(metaclass=Singleton):
    
    def __init__(self):
        self.pizza_count = 0
        self.time_limit = 20  # tempo limite para comer, em segundos
        self.last_pizza_time = time.time()
    
    def eat_pizza(self):
        self.pizza_count += 1
        self.last_pizza_time = time.time()
    
    def is_satisfied(self):
        return self.pizza_count >= 8
    
    def is_starved(self):
        return time.time() - self.last_pizza_time > self.time_limit