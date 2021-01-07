import random
from math import exp


class Animals:
    def __init__(self, age):
        self.age = age

    def ages(self):
        self.age += 1

    def get_age(self):
        return self.age


class Herbs(Animals):
    def __init__(self, age, cell, params):
        super().__init__(age)
        self.cell = cell
        self.sigma_birth = params['sigma_birth']
        self.phi_age = params['phi_age']
        self.a_half = params['a_half']
        self.phi_weight = params['phi_weight']
        self.w_half = params['w_half']
        self.weight = params['weight']
        self.beta = params['beta']
        self.F = params['F']
        self.gamma = params['gamma']
        self.zeta = params['zeta']
        self.w_birth = params['w_birth']
        self.omega = params['omega']
        self.eta = params['eta']

    def set_weight(self, weight):
        self.weight = weight

    def get_weight(self):
        return self.weight

    def eat(self):
        food = self.cell.get_fodder()
        if food > 0:
            if food < self.F:
                self.cell.set_fodder(0)
                self.weight += (food * self.beta)
            else:
                self.cell.set_fodder(food - self.F)
                self.weight += (self.F * self.beta)

    def get_fitness(self):
        if self.weight <= 0:
            return 0
        else:
            fitness = ((1 / (1 + exp(self.phi_age * (self.age - self.a_half)))) *
                       (1 / (1 + exp(self.phi_weight * (self.weight - self.w_half)))))
            return fitness

    def mate(self, ini_pop):
        if len(ini_pop) > 1:
            for _ in ini_pop:
                if not self.weight < self.zeta(self.w_birth + self.sigma_birth):
                    if random.random() < self.gamma * self.get_fitness() * (len(ini_pop) - 1):
                        return self.set_newborn()
                    return None
        else:
            return None

    def weight_loss(self):
        self.weight -= self.eta * self.weight

    def dies(self):
        return self.get_weight == 0 or random.random() < self.omega * (1 - self.get_fitness())
