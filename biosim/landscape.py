
class Landscape:
    d_landscape = None

    def __init__(self):
        self.list_herbs = []
        self.list_carns = []
        self.list_animals = self.list_herbs + self.list_carns
        # self.top = top
        # self.left = left
        # self.right = right
        # self.bottom = bottom

    def split_animals(self):

        for animal in self.list_animals:
            if animal['species'] == 'Herbivore':
                self.list_herbs.append(animal)
            elif animal['species'] == 'Carnivore':
                self.list_carns.append(animal)



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
        if not len(self.herb_sorting()) == 0:
            for herb in self.herb_sorting():
                if self.get_fodder() > 0:
                    self.set_fodder(self.get_fodder() - herb.eat(self.get_fodder()))
                else:
                    break
        if not len(self.carn_sorting()) == 0:
            for carn in self.carn_sorting():
                killed_herbs = carn.eat(self.herb_sorting())
                if killed_herbs is None:
                    break
                for killed_herb in killed_herbs:
                    self.herb_sorting().remove(killed_herb)

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

    def herb_sorting(self):
        return sorted(self.list_herbs, key=lambda x: x.get_fitness())

    def carn_sorting(self):
        return sorted(self.list_carns, key=lambda x: x.get_fitness(), reverse=True)

    def get_population(self):
        return len(self.list_carns) + len(self.list_herbs)


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
