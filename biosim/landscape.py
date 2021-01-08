class Landscape:
    d_landscape = {'f_max_h': 300, 'f_max_l': 800}

    def __init__(self, top, left, right, bottom, w_birth, sigma_birth, ini_pop, species):
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
        self.species = species

    @staticmethod
    def is_habitable():
        return True

    @staticmethod
    def get_fodder():
        return 0

    def list_species(self):
        self.num_herbs = []
        self.num_carns = []
        if self.species == 'Carnivore':
            self.species.append(self.num_carns)
        elif self.species == 'Herbivore':
            self.species.append(self.num_herbs)
        return self.num_herbs, self.num_carns

    def get_top(self):
        return self.top

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_bottom(self):
        return self.bottom

    def num_herbs(self):
        return len(self.ini_pop)  # bytt ut

    def give_birth(self):
        if len(self.ini_pop) > 1:  # bytt ut
            offspring_herbs = []
            for herb in self.ini_pop:  # bytt ut
                offspring = herb.mate(self.ini_pop)  # bytt ut
                if offspring:
                    offspring_herbs.append(offspring)

    def death(self, ini_pop):
        def survivors(pop):
            return [animal for animal in pop if not animal.dies()]

        self.ini_pop = survivors(ini_pop)

    def weight_loss(self):
        for animal in self.ini_pop:
            animal.lose_weight()
            animal.get_fitness()

    def herb_sorting(self):
        herb_sorted = []
        return sorted(self.num_herbs, key=lambda x: x.get_fitness(), reverse=True).append(herb_sorted)

    def carn_sorting(self):
        carn_sorted = []
        return sorted(self.num_carns, key=lambda x: x.get_fitness(), reverse=True).append(carn_sorted)


class Water(Landscape):
    pass

    @staticmethod
    def is_habitable():
        return False


class Dessert(Landscape):
    pass


class Highland(Landscape):
    d_landscape = None

    def __init__(self, d_landscape, top, left, right, bottom, w_birth, sigma_birth, ini_pop, fodder=300):
        super().__init__(top, left, right, bottom, w_birth, sigma_birth, ini_pop)
        self.d_landscape = d_landscape
        self.fodder = fodder

    def update_fodder(self):
        self.fodder = self.d_landscape['f_max_h']

    def get_fodder():
        return 0

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
