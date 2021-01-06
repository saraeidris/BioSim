import random
from .animals import Herbs

class Landscape:
    def __init__(self, top, left, right, bottom, w_birth, sigma_birth, herb_pop):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        self.w_birth = w_birth
        self.sigma_birth = sigma_birth
        self.herb_pop = herb_pop
        self.w_birth = w_birth
        self.sigma_birth = sigma_birth
        self.herb_pop = herb_pop

    def get_top(self):
        return self.top

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_bottom(self):
        return self.bottom

    def num_herbs(self, ini_pop):
        self.herb_pop = [Herbs() for _ in range(ini_pop)]
        return self.herb_pop



    def set_newborn(self, ini_pop):
        return {'loc': ini_pop[0]['loc'],
                'pop': {'species': 'Herbivore',
                        'age': 0,
                        'weight': random.gauss(self.w_birth, self.sigma_birth)}}

    def death(self, ini_pop):
        def survivors(pop):
            return [animal for animal in pop if not animal.dies()]

        self.herb_pop = survivors(ini_pop)

class Water(Landscape):
    pass

    @staticmethod
    def is_habitable():
        return False


class Dessert(Landscape):
    pass

    @staticmethod
    def get_fodder():
        return 0

    @staticmethod
    def is_habitable():
        return True




class Highland(Landscape):
    f_high = 300.0

    def __init__(self, top, left, right, bottom, fodder, w_birth, sigma_birth, herb_pop):
        super().__init__(top, left, right, bottom, w_birth, sigma_birth, herb_pop)
        self.fodder = fodder

    def set_fodder(self, fodder):
        self.fodder = fodder

    def get_fodder(self):
        return self.fodder


class Lowland(Landscape):
    f_low = 800.0

    def __init__(self, top, left, right, bottom, fodder, w_birth, sigma_birth, herb_pop):
        super().__init__(top, left, right, bottom, w_birth, sigma_birth, herb_pop)
        self.fodder = fodder

    def set_fodder(self, fodder):
        self.fodder = fodder

    def get_fodder(self):
        return self.fodder