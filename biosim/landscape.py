import random

class Landscape:
    def __init__(self, top, left, right, bottom, num_animals, w_birth, sigma_birth):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        self.num_animals = num_animals
        self.w_birth = w_birth
        self.sigma_birth = sigma_birth

    def get_top(self):
        return self.top

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_bottom(self):
        return self.bottom

    def count_num_animals(self):
        return self.num_animals


    def set_newborn(self, ini_pop):
        return {'loc': ini_pop[0]['loc'],
                'pop': {'species': 'Herbivore',
                        'age': 0,
                        'weight': random.gauss(self.w_birth, self.sigma_birth)}}

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

    def __init__(self, top, left, right, bottom, fodder):
        super().__init__(top, left, right, bottom)
        self.fodder = fodder

    def set_fodder(self, fodder):
        self.fodder = fodder

    def get_fodder(self):
        return self.fodder


class Lowland(Landscape):
    f_low = 800.0

    def __init__(self, top, left, right, bottom, fodder):
        super().__init__(top, left, right, bottom)
        self.fodder = fodder

    def set_fodder(self, fodder):
        self.fodder = fodder

    def get_fodder(self):
        return self.fodder