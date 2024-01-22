from abc import ABC, abstractmethod

from pytrobot.core.states import *


class TransitionRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, cls):
        self._registry[cls.__name__] = cls
        return cls

    def get_class(self, class_name):
        return self._registry.get(class_name)

class Variable:
    def __init__(self, name, value=False):
        self.name = name
        self.value = value

class Condition:
    def __init__(self, variable):
        self.variable = variable

    def evaluate(self):
        return self.variable.value

class Rule:
    def __init__(self, conditions, result_state):
        self.conditions = conditions  # Lista de instâncias de Condition
        self.result_state = result_state

    def evaluate(self):
        # Implementar a lógica para avaliar as condições
        # Exemplo: uma operação AND ou OR entre as condições
        pass

class TrueTable:
    def __init__(self):
        self.variables = {}  # Dicionário para armazenar variáveis pelo nome
        self.rules = []      # Lista para armazenar regras

    def add_variable(self, name, value):
        self.variables[name] = Variable(name, value)

    def add_rule(self, rule):
        self.rules.append(rule)

    def get_next_state(self, current_state):
        for rule in self.rules:
            if rule.evaluate():
                return rule.result_state
        return current_state

