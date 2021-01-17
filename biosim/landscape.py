import random


class Landscape:
    d_landscape = None

    @classmethod
    def set_params(cls, new_params):
        """
        Overrides default params
        :param new_params: input of wanted params
        :return:
            new dictionary with updated params
        """
        for key in new_params:
            if key not in cls.d_landscape:
                raise KeyError('Invalid parameter name:' + key)
            if not (isinstance(new_params[key], int) or isinstance(new_params[key], float)):
                raise ValueError(key + ' must be of type integer or float')
            if new_params[key] < 0:
                raise ValueError('Fodder value must be positive')
        cls.d_landscape.update(new_params)

    def __init__(self):
        self.list_herbs = []
        self.list_carns = []
        self.fodder = 0
        self.move_herbs = [[], [], [], []]
        self.move_carns = [[], [], [], []]

    def update_fodder(self):
        pass

    @staticmethod
    def is_habitable():
        return True

    @staticmethod
    def get_fodder():
        return 0

    def eat_all(self):
        """
        Iterates over all animals and check if they eat.
        Herbivores eats in random order.
        Carnivores eats in order based on fitness. In the end,
        the eaten herbivores are removed, and the survivors
        are stored in list_herbs.

        """
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

    def migrate_all(self, cells_around):
        """
        migrate each animal if picked cell is habitable
        :param cells_around: cells around the animal, north, south, east and west.
        """
        if len(self.list_herbs) > 0:
            herbs_stay = []
            for herb in self.list_herbs:
                if herb.migrate():
                    num = random.randint(0, 3)
                    if cells_around[num].is_habitable():
                        self.move_herbs[num].append(herb)
                    else:
                        herbs_stay.append(herb)
                else:
                    herbs_stay.append(herb)
            self.list_herbs = herbs_stay
        if len(self.list_carns) > 0:
            carns_stay = []
            for carn in self.list_carns:
                if carn.migrate():
                    num = random.randint(0, 3)
                    if cells_around[num].is_habitable():
                        self.move_carns[num].append(carn)
                    else:
                        carns_stay.append(carn)
                else:
                    carns_stay.append(carn)
            self.list_carns = carns_stay

    def give_birth(self):
        """
        Animals give birth to an offspring
         of the same specie if mate method is fulfilled.
        """
        if len(self.list_herbs) > 1:
            offspring_herbs = []
            for herb in self.list_herbs:
                offspring = herb.mate(len(self.list_herbs))
                if offspring:
                    offspring_herbs.append(offspring)
            self.list_herbs += offspring_herbs
        if len(self.list_carns) > 1:
            offspring_carns = []
            for carn in self.list_carns:
                offspring = carn.mate(len(self.list_carns))
                if offspring:
                    offspring_carns.append(offspring)
            self.list_carns += offspring_carns

    def ages(self):
        """Species ages by one year each year"""
        for animal in (self.list_herbs + self.list_carns):
            animal.aging()

    def death(self):
        """
        Keep animal if it don't die in method dies().
        """
        self.list_herbs = [animal for animal in self.list_herbs if not animal.dies()]
        self.list_carns = [animal for animal in self.list_carns if not animal.dies()]

    def lose_weight(self, pyvid=False):
        """
        calls the weight_loss method on all animals in the cell.
        :param pyvid: True if this is a year with pyvid (Pythonvirus disease).
        """
        for animal in (self.list_herbs + self.list_carns):
            animal.weight_loss(pyvid, len(self.list_herbs + self.list_carns))

    def set_fodder(self, fodder):
        self.fodder = fodder

    def get_population(self):
        """
        :return: number of herbivores and carnivores separated
        """
        return len(self.list_herbs), len(self.list_carns)

    def get_animals(self):
        """
        :return: list with all herbivores, carnivores and both together
        """
        return self.list_herbs, self.list_carns, self.list_herbs + self.list_carns

    def is_populated(self):
        """
        :return: number of total animals
        """
        return len(self.list_herbs + self.list_carns) > 0

    def get_herb_fitness(self):
        """
        :return: fitness for all herbivores
        """
        return [herb.get_fitness() for herb in self.list_herbs]

    def get_carn_fitness(self):
        """
        :return: fitness for all carnivores
        """
        return [carn.get_fitness() for carn in self.list_carns]

    def get_herb_age(self):
        return [herb.age for herb in self.list_herbs]

    def get_carn_age(self):
        """
        :return: age for all carnivores
        """
        return [carn.age for carn in self.list_carns]

    def get_herb_weight(self):
        """
        :return: Weight for all herbivores
        """
        return [herb.weight for herb in self.list_herbs]

    def get_carn_weight(self):
        """
        :return: Weight for all carnivores
        """
        return [carn.weight for carn in self.list_carns]


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
        """
        Updates fodder, used to update fodder each year. Overrides method in Landscape.
        :return:
        """
        self.fodder = self.d_landscape['f_max']

    def get_fodder(self):
        """
        :return: Amount of fodder in current cell.
        """
        return self.fodder


class Lowland(Landscape):
    d_landscape = {'f_max': 800}

    def __init__(self):
        super().__init__()

    def update_fodder(self):
        """
        Updates fodder, used to update fodder each year. Overrides method in Landscape.
        :return:
        """
        self.fodder = self.d_landscape['f_max']

    def get_fodder(self):
        """
        :return: Amount of fodder in current cell.
        """
        return self.fodder
