import random as rand
from math import exp


class Animals:
    def __init__(self, age):
        self.age = age

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age


class Herbs(Animals):
    def __init__(self, age, w_birth, sigma_birth, phi_age, a_half, phi_weight, w_half):
        super().__init__(age)
        self.w_birth = w_birth
        self.sigma_birth = sigma_birth
        self.phi_age = phi_age
        self.a_half = a_half
        self.phi_weight = phi_weight
        self.w_half = w_half
        self.weight = rand.gauss(self.w_birth, self.sigma_birth)

    def set_weight(self, weight):
        self.weight = weight

    def get_weight(self):
        return self.weight

    def get_fitness(self):
        if self.weight <= 0:
            return 0
        else:
            fitness = ((1 / (1 + exp(self.phi_age * (self.age - self.a_half)))) *
             (1 / (1 + exp(self.phi_weight * (self.weight - self.w_half)))))
            return fitness

    def is_dead(self):
            return self.get_weight() == 0
