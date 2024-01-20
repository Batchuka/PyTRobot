from abc import ABC, abstractmethod

from pytrobot.core.states import *


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

# Exemplo de Uso:
true_table = TrueTable()
true_table.add_variable('doc_downloaded', False)
doc_downloaded_condition = Condition(true_table.variables['doc_downloaded'])
transition_rule = Rule([doc_downloaded_condition], 'HANDLER')
true_table.add_rule(transition_rule)

# Avaliar e obter o próximo estado
current_state = 'STARTER'
next_state = true_table.get_next_state(current_state)