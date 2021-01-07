import random
from math import exp


class Animals:
    params = None

    # d_params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125,
    #                 'a_half': 40.0, 'phi_age': 0.3, 'w_half': 4.0,
    #                 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
    #                 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}

    @classmethod
    def get_species_params(cls):
        return cls.params

    def __init__(self, age=0, weight=None):
        self.age = age
        if self.params is None:
            self.get_species_params()

        if weight is None:
            self.weight = random.gauss(self.params['w_birth'], self.params['sigma_birth'])

    def ages(self):
        self.age += 1

    def get_age(self):
        return self.age

    @classmethod
    def set_params(cls, new_params):
        for key in new_params:
            if key not in cls.params:
                raise KeyError('Invalid parameter name:' + key)
            if not isinstance(new_params[key], int) or isinstance(new_params[key], float):
                raise ValueError('Parameters must be integers or floats')


class Herbs(Animals):
    params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
              'a_half': 40.0, 'phi_age': 0.6, 'w_half': 10.0,
              'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
              'omega': 0.4, 'F': 10.0}

    def __init__(self, params, island, age=0, weight=None):
        super().__init__(age=age, weight=weight)
        self.params = params
        self.island = island

    def set_weight(self):
        if self.weight is None:
            self.weight = random.gauss(self.params['w_birth'], self.params['sigma_birth'])

    def get_weight(self):
        return self.weight

    def eat(self):
        food = self.island.get_fodder()
        if food >= 0:
            if food < self.params['F']:
                self.weight += (food * self.params['beta'])
            else:
                self.island.set_fodder(food - self.params['F'])
                self.weight += (self.params['F'] * self.params['beta'])
        else:
            raise ValueError('Fodder value must be zero or positive')

    def get_fitness(self):
        if self.weight <= 0:
            return 0
        else:
            fitness = ((1 / (1 + exp(self.params['phi_age'] * (self.age - self.params['a_half'])))) *
                       (1 / (1 + exp(self.params['phi_weight'] * (self.weight - self.params['w_half'])))))
            return fitness

    def mate(self, ini_pop):
        if len(ini_pop) > 1:
            for _ in ini_pop:
                if not self.weight < self.params['zeta'](self.params['w_birth'] + self.params['sigma_birth']):
                    if random.random() < self.params['gamma'] * self.get_fitness() * (len(ini_pop) - 1):
                        return True
                    return False
        else:
            return False

    def weight_loss(self):
        self.weight -= self.params['eta'] * self.weight

    def dies(self):
        return self.get_weight == 0 or random.random() < self.params['omega'] * (1 - self.get_fitness())
