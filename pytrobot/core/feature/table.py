# pytrobot/core/dataset_layer/dataset.py

from pytrobot.core.singleton import Singleton
from typing import List


class Item:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getitem__(self, key):
        """Permite o acesso a atributos usando item['key']"""
        return getattr(self, key, None)

    def __setitem__(self, key, value):
        """Permite a modificação de atributos usando item['key'] = value"""
        setattr(self, key, value)

    def update(self, **kwargs):
        """Método para atualizar os valores das colunas."""
        for key, value in kwargs.items():
            self[key] = value  # Usando __setitem__ internamente

    def __repr__(self):
        """Método para representar o objeto como string (útil para depuração)."""
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

class Table(metaclass=Singleton):

    def __init__(self, columns):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.columns = columns
            self.items : List[Item] = []
            self.transaction_number = 0
            self.transaction_item = None

    def __iter__(self):
        return iter(self.items)

    def add_item(self, **kwargs):
        if any(item[self.columns[0]] == kwargs.get(self.columns[0], None) for item in self.items):
            raise ValueError(f"An item with the same {self.columns[0]} already exists.")
        item = Item(**kwargs)
        self.items.append(item)
        if self.transaction_item is None:
            self.transaction_item = item

    def get_item(self, id):
        for item in self.items:
            if item[self.columns[0]] == id:
                return item
        return None

    def update_item(self, id, **kwargs):
        item = self.get_item(id)
        if item is not None:
            item.update(**kwargs)
        else:
            raise ValueError(f"Item with {self.columns[0]} '{id}' not found.")

    def get_next_item(self):

        self.transaction_number += 1
        if self.transaction_number <= len(self.items):
            self.transaction_item = self.items[self.transaction_number - 1]
            return self.transaction_item
        else:
            self.transaction_number = 0
            self.transaction_item = None
            return None

