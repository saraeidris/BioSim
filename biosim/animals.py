import random as rand
from math import exp


class Animals:
    def __init__(self, age):
        self.age = age

    def setAge(self, age):
        self.age = age

    def getAge(self):
        return self.age


class Herbs(Animals):
    w_birth = 8.0
    sigma_birth = 1.5
    phi_age = 0.6
    a_half = 40.0
    phi_weight = 0.1
    w_half = 10.0
    DEFAULT_PARAMETER = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
                         'a_half': 40.0, 'phi_age': 0.6, 'w_half': 10.0,
                         'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                         'omega': 0.4, 'F': 10.0}

    def __init__(self, age):
        super().__init__(age)
        self.weight = rand.gauss(self.w_birth, self.sigma_birth)

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def Fitness(self):
        if self.weight <= 0:
            return 0
        else:
            fitness = ((1 / (1 + exp(self.phi_age * (self.age - self.a_half)))) *
             (1 / (1 + exp(self.phi_weight * (self.weight - self.w_half)))))
            return fitness

    def Death(self):
        if Fitness() == 0:
