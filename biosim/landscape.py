import random


class Landscape:
    d_landscape = None

    def __init__(self):
        self.list_herbs = []
        self.list_carns = []
        self.fodder = None

    @classmethod
    def set_params(cls, new_params):
        for key in new_params:
            if key not in cls.d_landscape:
                raise KeyError('Invalid parameter name:' + key)
        cls.d_landscape.update(new_params)

    def update_fodder(self):
        pass

    @staticmethod
    def is_habitable():
        return True

    @staticmethod
    def get_fodder():
        return 0

    def eat_all(self):
        if not len(self.list_herbs) == 0:
            random.shuffle(self.list_herbs)
            for herb in self.list_herbs:
                if self.get_fodder() > 0:
                    self.set_fodder(self.get_fodder() - herb.consumed_fodder(self.get_fodder()))
                else:
                    break
        if not len(self.list_carns) == 0:
            sorted_carns = sorted(self.list_carns, key=lambda x: x.get_fitness(), reverse=True)
            sorted_herbs = sorted(self.list_herbs, key=lambda x: x.get_fitness())
            for carn in sorted_carns:
                killed_herbs = carn.consumed_herbs(sorted_herbs)
                if len(killed_herbs) == 0:
                    continue
                for herb in killed_herbs:
                    sorted_herbs.remove(herb)
            self.list_herbs = sorted_herbs

    # def migration(self, around):
    #     move_north = []
    #     move_south = []
    #     move_east = []
    #     move_west = []
    #     for herb in self.list_herbs:
    #         if herb.migrate():

    def give_birth(self):
        if len(self.list_herbs) > 1:
            offspring_herbs = []
            for herb in self.list_herbs:
                offspring = herb.mate(self.list_herbs)
                if offspring:
                    offspring_herbs.append(offspring)
            self.list_herbs += offspring_herbs
        if len(self.list_carns) > 1:
            offspring_carns = []
            for carn in self.list_carns:
                offspring = carn.mate(self.list_carns)
                if offspring:
                    offspring_carns.append(offspring)
            self.list_carns += offspring_carns

    def ages(self):
        """Species ages by one year each year"""
        for herb in self.list_herbs:
            herb.aging()
        for carn in self.list_carns:
            carn.aging()

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
    d_landscape = {'f_max': 300}

    def __init__(self):
        super().__init__()

    def update_fodder(self):
        self.fodder = self.d_landscape['f_max']

    def get_fodder(self):
        return self.fodder


class Lowland(Landscape):
    d_landscape = {'f_max': 800}

    def __init__(self):
        super().__init__()

    def update_fodder(self):
        self.fodder = self.d_landscape['f_max']

    def get_fodder(self):
        return self.fodder
