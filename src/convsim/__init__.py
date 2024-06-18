import pickle
from abc import ABC, abstractmethod

class ExperimentResults:

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_object(cls, o: object):
        return cls(data=o)

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.data, f)

    @classmethod 
    def load(cls, path):
        with open(path, "rb") as f:
            return cls(data=pickle.load(f))


class Experiment(ABC):

    @staticmethod
    @abstractmethod
    def run() -> object:
        ...
    
    @staticmethod
    @abstractmethod
    def present(*args):
        ...