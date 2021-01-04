
from numpy import random as rand


class Herbivores:
    def __init__(self, w_birth, sigma_birth):
        self.w_birth = w_birth
        self.sigma_birth = sigma_birth

    def weight(self):
        return rand.normal(self.w_birth, self.sigma_birth)


if __name__ == '__main__':
    p1 = Herbivores(8, 1.5)
    print(p1.weight())
