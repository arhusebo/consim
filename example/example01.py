import sys
sys.path.append("./src/")

from convsim import *


class Fibonacci(Experiment):

    @staticmethod
    def run():
        x = [0, 1]
        for i in range(20):
            x.append(x[i]+x[i+1])
        return x
    
    @staticmethod
    def present(x):
        print(", ".join(str(_x) for _x in x))


class ReturnNothing(Experiment):

    @staticmethod
    def run():
        pass

    @staticmethod
    def present(args):
        print("Presenting nothing")