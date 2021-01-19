import random

__author__ = "Sara Idris & Thorbjørn L Onsaker, NMBU"
__email__ = "said@nmbu.no & thon@nmbu.no"


class Landscape:
    """
    Baseclass for landscape types that may contain herbivore or carnivore.
    """

    """
           :param sys_size:  system size, e.g. (5, 10)
           :type sys_size: (int, int)
           :param noise: noise level
           :type noise: float
           :param seed: random generator seed
           :type seed: int
           :param img_dir: directory for image files; no images if None
           :type img_dir: str
           :param img_name: beginning of name for image files
           :type img_name: str
           :param img_fmt: image file format suffix
           :type img_fmt: str

           .. note:: For default values for img_* parameters, see :mod:`randvis.graphics`.
           """
    d_landscape = None

    @classmethod
    def set_params(cls, new_params):
        """
        Overrides default params.
        :raises ValueError: if key not an integer, invalid parameter
                            name or fodder value is negative
        :param new_params: new input params

        :raises ValueError: if key not an original key in landscape parameters,
                            new value not an integer or float or if fodder
                            value is negative.
        """
        for key in new_params:
            if key not in cls.d_landscape:
                raise ValueError('Invalid parameter name:' + key)
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
                if self.fodder > 0:
                    self.set_fodder(self.fodder - herb.consumed_fodder(self.fodder))
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
        Calls :meth: 'migrate()' and checks if animal migrate, puts animal in right list

        :param cells_around: the cell north, south, east and west of the current cell
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
        Calls :meth: 'mate()' and checks if animal gets offspring, puts offspring into new list

        Animals give birth to an offspring of the same specie if mate method is fulfilled.
        """
        if len(self.list_herbs) > 1:
            offspring_herbs = []
            for herb in self.list_herbs:
                offspring = herb.mate(len(self.list_herbs))
                if offspring:
                    offspring_herbs.append(offspring)
            self.list_herbs.extend(offspring_herbs)
        if len(self.list_carns) > 1:
            offspring_carns = []
            for carn in self.list_carns:
                offspring = carn.mate(len(self.list_carns))
                if offspring:
                    offspring_carns.append(offspring)
            self.list_carns.extend(offspring_carns)

    def ages(self):
        """Species ages by one year each year"""

        for animal in (self.list_herbs + self.list_carns):
            animal.aging()

    def death(self):
        """Keeps animal if it don't die in method dies()."""

        self.list_herbs = [animal for animal in self.list_herbs if not animal.dies()]
        self.list_carns = [animal for animal in self.list_carns if not animal.dies()]

    def lose_weight(self, pyvid=False):
        """
        Calls the weight_loss method on all animals in the cell.

        :param pyvid: True if this is a year with pyvid (Pythonvirus disease).
        """

        for animal in (self.list_herbs + self.list_carns):
            animal.weight_loss(pyvid, len(self.list_herbs + self.list_carns))

    def set_fodder(self, fodder):
        """ Sets fodder """
        self.fodder = fodder

    def get_population(self):
        """
        Returns of herbivores and carnivores as a tuple.
        """

        return len(self.list_herbs), len(self.list_carns)

    def get_animals(self):
        """
        Returns list with all herbivores, carnivores and both together
        """
        return self.list_herbs, self.list_carns, self.list_herbs + self.list_carns

    def is_populated(self):
        """
        Returns number of total animals
        """
        return len(self.list_herbs + self.list_carns) > 0

    def get_herb_fitness(self):
        """
        Returns fitness for all herbivores
        """
        return [herb.get_fitness() for herb in self.list_herbs]

    def get_carn_fitness(self):
        """
        Returns fitness for all carnivores
        """
        return [carn.get_fitness() for carn in self.list_carns]

    def get_herb_age(self):
        return [herb.age for herb in self.list_herbs]

    def get_carn_age(self):
        """
        Returns age for all carnivores
        """
        return [carn.age for carn in self.list_carns]

    def get_herb_weight(self):
        """
        Returns weight for all herbivores
        """
        return [herb.weight for herb in self.list_herbs]

    def get_carn_weight(self):
        """
        Returns weight for all carnivores as a list.
        """
        return [carn.weight for carn in self.list_carns]


class Water(Landscape):
    """Subclass for Landscape, water is not habitable for animals."""
    pass

    @staticmethod
    def is_habitable():
        return False


class Desert(Landscape):
    """Subclass for Landscape, habitable for animals, but contains no fodder."""
    pass


class Highland(Landscape):
    """Subclass for Landscape, habitable for animals, and contains a fixed amount of fodder."""

    d_landscape = {'f_max': 300}

    def __init__(self):
        super().__init__()

    def update_fodder(self):
        """
        Updates fodder, used to update fodder each year. Overrides method in Landscape.
        """

        self.fodder = self.d_landscape['f_max']


class Lowland(Landscape):
    """Habitable for animals, and contains a fixed amount of fodder """
    d_landscape = {'f_max': 800}

    def __init__(self):
        super().__init__()

    def update_fodder(self):
        """
        Updates fodder, used to update fodder each year. Overrides method in Landscape.
        """
        self.fodder = self.d_landscape['f_max']
