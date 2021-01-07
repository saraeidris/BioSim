#import random
from .animals import Animals


class Landscape:
    d_landscape = {'f_max_h': 300, 'f_max_l': 800}

    def __init__(self, top, left, right, bottom, w_birth, sigma_birth, ini_pop):
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        self.w_birth = w_birth
        self.sigma_birth = sigma_birth
        self.w_birth = w_birth
        self.sigma_birth = sigma_birth
        self.ini_pop = ini_pop
        self.fodder = 0

    def get_top(self):
        return self.top

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_bottom(self):
        return self.bottom

    def num_herbs(self):
        return len(self.ini_pop)

    @staticmethod
    def set_newborn(self, ini_pop):
        new_herbs = []
        for animal in ini_pop:
            if animal.mate:
                new_herbs.append(animal.__class__())

    def death(self, ini_pop):
        def survivors(pop):
            return [animal for animal in pop if not animal.dies()]

        self.ini_pop = survivors(ini_pop)


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
    d_landscape = None

    def __init__(self, d_landscape, top, left, right, bottom, w_birth, sigma_birth, ini_pop, fodder=300):
        super().__init__(top, left, right, bottom, w_birth, sigma_birth, ini_pop)
        self.d_landscape = d_landscape
        self.fodder = fodder

    def update_fodder(self, fodder):
        self.fodder = self.d_landscape['f_max_h']

    def set_fodder(self, fodder):
        self.fodder = fodder

    def get_fodder(self):
        return self.fodder


class Lowland(Landscape):
    d_landscape = None

    def __init__(self, top, left, right, bottom, w_birth, sigma_birth, ini_pop, fodder=800):
        super().__init__(top, left, right, bottom, w_birth, sigma_birth, ini_pop)
        self.fodder = fodder

    def update_fodder(self):
        self.fodder = self.d_landscape['f_max_l']

    def get_fodder(self):
        return self.fodder
