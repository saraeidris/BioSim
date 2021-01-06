import random
from math import exp


class Animals:
    def __init__(self, age):
        self.age = age

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age


class Herbs(Animals):
    def __init__(self, age, weight, cell, sigma_birth, phi_age, a_half, phi_weight, w_half, beta, F, gamma, zeta,
                 w_birth):
        super().__init__(age)
        self.cell = cell
        self.sigma_birth = sigma_birth
        self.phi_age = phi_age
        self.a_half = a_half
        self.phi_weight = phi_weight
        self.w_half = w_half
        self.weight = weight
        self.beta = beta
        self.F = F
        self.gamma = gamma
        self.zeta = zeta
        self.w_birth = w_birth

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

    # def mate(self):
    #     born_herbs = []
    #     if len(self.ini_pop) > 1:
    #         for _ in self.ini_pop:
    #             if not self.weight < self.zeta(self.w_birth + self.sigma_birth):
    #                 if self.gamma * self.get_fitness() * (len(self.ini_pop) - 1) < random.random():
    #                     born_herbs.append(self.set_newborn())
    #
    # def set_newborn(self):
    #     return {'loc': self.ini_pop[0]['loc'],
    #             'pop': {'species': 'Herbivore',
    #                     'age': 0,
    #                     'weight': random.gauss(self.w_birth, self.sigma_birth)}}

    # def is_dead(self):
    #     if self.get_weight == 0:
    #         self.ini_pop.pop()
    #     else:
