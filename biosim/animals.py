import random
from math import exp


class Animals:

    # carns_params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125,
    #                 'a_half': 40.0, 'phi_age': 0.3, 'w_half': 4.0,
    #                 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
    #                 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}

    def __init__(self, age=0, weight=None):
        self.age = age
        if weight is None:
            self.weight = random.gauss(self.w_birth, self.sigma_birth)



    def ages(self):
        self.age += 1

    def get_age(self):
        return self.age


    @classmethod
    def set_params(cls, new_params):
        for key in new_params:
            if key not in cls.herbs_params:
                raise KeyError('Invalid parameter name:' + key)
            if not isinstance(new_params[key], int) or isinstance(new_params[key], float):
                raise ValueError('Parameters must be integers or floats')



    @classmethod
    def get_params(cls):

        return


class Herbs(Animals):
    d_params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
                    'a_half': 40.0, 'phi_age': 0.6, 'w_half': 10.0,
                    'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                    'omega': 0.4, 'F': 10.0}
    parameters = None

    def __init__(self, age, cell):
        super().__init__(age)
        self.cell = cell

    def weight(self):
        if self.weight is None:
            self.weight = random.gauss(self.w_birth, self.sigma_birth)

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
