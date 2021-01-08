
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
            self.num_carns.append(self.species)
        elif self.species == 'Herbivore':
            self.num_herbs.append(self.species)
        return self.num_herbs, self.num_carns

    def get_top(self):
        return self.top

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_bottom(self):
        return self.bottom

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

    def set_fodder(self, fodder):
        self.fodder = fodder

    def eat_all(self):
        for herb in self.list_species[0]:
            if self.get_fodder() > 0:
                self.set_fodder(self.get_fodder() - herb.eat(self.get_fodder))
            else:
                break
        # for carn in self.list_species[1]:
        #     if carn.eat() == 0:
        #         return
        #     elif carn.eat() == p:
        #         if p > random.random():
        #             herb_sorted.pop(0)
        #     else:
        #         herb_sorted.pop(0)

    def herb_sorting(self):
        herb_sorted = []
        return herb_sorted.append(sorted(self.num_herbs, key=lambda x: x.get_fitness(), reverse=True))

    def carn_sorting(self):
        carn_sorted = []
        return carn_sorted.append(sorted(self.num_carns, key=lambda x: x.get_fitness(), reverse=True))


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
