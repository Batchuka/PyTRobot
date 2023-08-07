from enum import Enum


class Environment(Enum):
    DEV = 'DEV.properties'
    HML = 'HML.properties'
    OPS = 'OPS.properties'


class Config:
    assets = None
    transaction_item = {}
