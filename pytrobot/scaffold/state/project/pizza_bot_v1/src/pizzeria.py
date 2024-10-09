# from pytrobot.scaffold.state.project.pizza_bot.src.pizza import Pizza

from .pizza import Pizza

class Pizzeria:
    def __init__(self):
        self.flavor = None
        self.slices = 0

    def order(self) -> Pizza:
        """Ask the user the flavor of the pizza and the number of slices, then return a Pizza instance."""
        self.flavor = input("What flavor of pizza would you like? ")

        # Ask the number of slices
        while True:
            try:
                self.slices = int(input("How many slices should the pizza have? (Enter a number): "))
                if self.slices > 0:
                    break
                else:
                    self.logger.info("Please enter a number greater than zero.")
            except ValueError:
                self.logger.info("Invalid entry. Please enter a number.")
        
        # Return a Pizza instance
        return Pizza(flavor=self.flavor, slices=self.slices)

    def __str__(self):
        return f"Pizza flavor: {self.flavor}, with {self.slices} slices."