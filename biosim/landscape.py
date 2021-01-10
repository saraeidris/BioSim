import random

class Landscape:
    d_landscape = None

    def __init__(self):
        self.list_herbs = []
        self.list_carns = []
        #self.list_animals = self.list_herbs + self.list_carns
        # self.top = top
        # self.left = left
        # self.right = right
        # self.bottom = bottom

    def update_fodder(self):
        self.fodder = None

    def split_animals(self):

        for animal in self.get_list_animals:
            if animal['species'] == 'Herbivore':
                self.list_herbs.append(animal)
            else:
                self.list_carns.append(animal)

    def get_list_animals(self):
        return self.list_herbs + self.list_carns

    def set_list_animals(self, ):

    @staticmethod
    def is_habitable():
        return True

    @staticmethod
    def get_fodder():
        return 0

    # def get_top(self):
    #     return self.top
    #
    # def get_left(self):
    #     return self.left
    #
    # def get_right(self):
    #     return self.right
    #
    # def get_bottom(self):
    #     return self.bottom

    def eat_all(self):
        shuffle_herbs = random.shuffle(self.list_herbs)
        shuffle_carns = random.shuffle(self.list_carns)
        if not shuffle_herbs is None:
        # if not (shuffle_herbs is None and len(shuffle_herbs) == 0):
            for herb in shuffle_herbs:
                if self.get_fodder() > 0:
                    self.set_fodder(self.get_fodder() - herb.eat(self.get_fodder()))
                else:
                    break
        if not shuffle_carns is None:
        #if not len(shuffle_carns) == 0:
            for carn in shuffle_carns:
                killed_herbs = carn.eat(shuffle_herbs)
                if killed_herbs is None:
                    break
                for killed_herb in killed_herbs:
                    shuffle_herbs.remove(killed_herb)

    def give_birth(self):
        if len(self.herb_sorting()) > 1:
            offspring_herbs = []
            for herb in self.herb_sorting():
                offspring = herb.mate(self.herb_sorting())
                if offspring:
                    offspring_herbs.append(offspring)
        if len(self.herb_sorting()) > 1:
            offspring_carns = []
            for carn in self.herb_sorting():
                offspring = carn.mate(self.herb_sorting())
                if offspring:
                    offspring_carns.append(offspring)

    def ages(self):
        """Species ages by one year each year"""
        for animal in self.get_animals()[2]:
            animal.age += 1
        # self.get_fitness()

    def death(self):
        def survivors(pop):
            return [animal for animal in pop if not animal.dies()]

        self.list_animals() = survivors(self.list_animals())

    def weight_loss(self):
        for animal in self.list_animals:
            animal.lose_weight()
            # animal.get_fitness()

    def set_fodder(self, fodder):
        self.fodder = fodder

    def herb_sorting(self):
        return sorted(self.list_herbs, key=lambda x: x.get_fitness())

    def carn_sorting(self):
        return sorted(self.list_carns, key=lambda x: x.get_fitness(), reverse=True)

    def get_population(self):
        return len(self.list_herbs), len(self.list_carns)
    def get_animals(self):
        return self.list_herbs, self.list_carns, self.list_herbs + self.list_carns


class Water(Landscape):
    pass

    @staticmethod
    def is_habitable():
        return False


class Desert(Landscape):
    pass


class Highland(Landscape):
    d_landscape = {'f_max_h': 300}

    def __init__(self):
        super().__init__()

    def update_fodder(self):
        self.fodder = self.d_landscape['f_max_h']

    def get_fodder(self):
        return self.fodder


class Lowland(Landscape):
    d_landscape = {'f_max_l': 800}

    def __init__(self):
        super().__init__()

    def update_fodder(self):
        self.fodder = self.d_landscape['f_max_l']

    def get_fodder(self):
        return self.fodder
