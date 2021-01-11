#import random


class Landscape:
    d_landscape = None

    def __init__(self):
        self.list_herbs = []
        self.list_carns = []

    def update_fodder(self):
        self.fodder = None

    # def split_animals(self):
    #
    #     for animal in self.get_list_animals():
    #         if animal['species'] == 'Herbivore':
    #             self.list_herbs.append(animal)
    #         else:
    #             self.list_carns.append(animal)

    def get_list_animals(self):
        return self.list_herbs + self.list_carns

    def set_list_animals(self):
        pass

    @staticmethod
    def is_habitable():
        return True

    @staticmethod
    def get_fodder():
        return 0

    def eat_all(self): # Kan bruke shuffle her kanskje?
        if not len(self.herb_sorting()) == 0:
            for herb in self.herb_sorting():
                if self.get_fodder() > 0:
                    self.set_fodder(self.get_fodder() - herb.consumed_fodder(self.get_fodder()))
                else:
                    break
        if not len(self.carn_sorting()) == 0:
            for carn in self.carn_sorting():
                killed_herbs = carn.consumed_herbs(self.herb_sorting())
                if killed_herbs is None:
                    break
                for killed_herb in killed_herbs:
                    self.herb_sorting().remove(killed_herb)
                    #self.herb_sorting() = [killed_herb for killed_herb in self.herb_sorting() if not killed_herb in killed_herbs]

    # def migration(self, ):
    #     move_north = []
    #     move_south = []
    #     move_east = []
    #     move_west = []
    #     for herb in self.list_herbs:
    #         if herb.migrate():


    def give_birth(self):
        if len(self.herb_sorting()) > 1:
            offspring_herbs = []
            for herb in self.herb_sorting():
                offspring = herb.mate(self.herb_sorting())
                if offspring:
                    offspring_herbs.append(offspring)
            self.list_herbs += offspring_herbs
        if len(self.carn_sorting()) > 1:
            offspring_carns = []
            for carn in self.carn_sorting():
                offspring = carn.mate(self.carn_sorting())
                if offspring:
                    offspring_carns.append(offspring)
            self.list_carns += offspring_carns

    def ages(self):
        """Species ages by one year each year"""
        for herb in self.list_herbs:
            herb.age += 1
        for carn in self.list_carns:
            carn.age += 1

    def death(self):
        def survivors(pop):
            return [animal for animal in pop if not animal.dies()]

        self.list_herbs = survivors(self.list_herbs)
        self.list_carns = survivors(self.list_carns)

    def lose_weight(self):
        for animal in (self.list_herbs + self.list_carns):
            animal.weight_loss()

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
