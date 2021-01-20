from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Water, Desert, Highland, Lowland, Landscape
import random

__author__ = "Sara Idris & Thorbjørn L Onsaker, NMBU"
__email__ = "said@nmbu.no & thon@nmbu.no"


class RossumIsland:
    """Class for the full ecosystem on the island.

    Attributes:
        island_map: string
            Multi-line string with letters representing cells on the island
        disease: bool
            True if the chance for diseases are turned on for the simulation
        :raises ValueError: if no island map is given, rows in island are not
        of the same length or if island is not surrounded by water.
    """
    island_dict = {'W': Water, 'D': Desert, 'L': Lowland, 'H': Highland}

    def __init__(self, island_map, disease=False):

        self.disease = disease

        if len(island_map) == 0:
            raise ValueError('No island map was given')

        self.island_row_length = len(island_map.splitlines()[0])
        self.island_col_length = len(island_map.splitlines())

        self.island = []
        for lines in island_map.splitlines():
            self.island.append(self.splits(lines, self.island_dict))

        for land_type in self.island[0] + self.island[-1]:
            if not isinstance(land_type, Water):
                raise ValueError('Outer edges of map must be water')

        for rows in island_map.splitlines():
            if len(rows) != self.island_row_length:
                raise ValueError('All rows in the island map must be the same length')
            if not (rows[0] == 'W' or rows[-1] == 'W'):
                raise ValueError('Outer edges of map must be water')

    @staticmethod
    def splits(line, island_dict):
        """Turns characters into landscape objects and splits string into list.

        Returns current fitness for specie
        :raises ValueError: if character not a part of the island dictionary.
        """

        for land_type in line:
            if land_type not in island_dict:
                raise ValueError('Character not allowed as a part of island map')

        return [island_dict[land]() for land in line]

    def insert_population(self, pop):
        """Inserts population of given species to given location.

        :param pop: list with dictionary that contains species and a wanted location.
        :raises ValueError: if location doesn't exist or given location is water.
        """

        for dic in pop:
            location = dic['loc']
            if location[0] <= 0 or location[1] <= 0:
                raise ValueError('Location coordinates must be positive')
            try:
                cell = self.island[location[0] - 1][location[1] - 1]
                if isinstance(cell, Landscape) and cell.is_habitable():
                    herbs_list = []
                    carn_list = []
                    for animal in dic['pop']:
                        if animal['species'] == 'Herbivore':
                            herbs_list.append(Herbivore(animal['age'],
                                                        animal['weight']))
                        if animal['species'] == 'Carnivore':
                            carn_list.append(Carnivore(animal['age'], animal['weight']))
                    cell.list_herbs.extend(herbs_list)
                    cell.list_carns.extend(carn_list)
                else:
                    raise ValueError('Animals are not allowed to stay at given location')
            except IndexError:
                raise ValueError('Specified location does not exist')

    def get_pop_info(self):
        """Get the population density and total sum of animals for each species.

        :return: tuple with 2 dimensional array for herbivore and carnivore
        density and total number of herbivores and carnivores on the island.
        """
        herb_array = [[len(cell.list_herbs) for cell in row] for row in self.island]
        carn_array = [[len(cell.list_carns) for cell in row] for row in self.island]
        sum_herb = sum([sum(row) for row in herb_array])
        sum_carn = sum([sum(row) for row in carn_array])
        return herb_array, carn_array, sum_herb, sum_carn

    def get_stats(self):
        """Get weight, age and fitness for plotting.

        :return: tuple with 6 lists containing weights, fitness and ages for
         all herbivores and carnivores on the island.
        """

        age_herbs, age_carns = [], []
        weight_herbs, weight_carns = [], []
        fitness_herbs, fitness_carns = [], []

        for row in self.island:
            for cell in row:
                age_herbs.extend(cell.get_herb_age())
                age_carns.extend(cell.get_carn_age())
                weight_herbs.extend(cell.get_herb_weight())
                weight_carns.extend(cell.get_carn_weight())
                fitness_herbs.extend(cell.get_herb_fitness())
                fitness_carns.extend(cell.get_carn_fitness())
        return age_herbs, age_carns, weight_herbs, weight_carns, fitness_herbs, fitness_carns

    def pyvid(self):
        """checks if pyvid (Pythonvirus disease) occurs or not.

        :return: True if pyvid occurs in current year.
        """

        return random.randint(1, 30) == 1

    def annual_cycle(self):
        """the annual cycle on the island.

        Making one year pass on the island by doing the following missions:
        1.  Update fodder in all habitable cells.
        2.  Make sure all animals eat or try to eat.
        3.  Procreation for all animals.
        4.  Migration of all animals that will migrate.
        5.  Age all animals.
        6.  Make sure all animals lose weight.
        7.  Remove all animals that die.
        """

        pyvid = False
        if self.disease:
            pyvid = self.pyvid()

        for row in self.island:
            for cell in row:
                if cell.is_habitable():
                    cell.update_fodder()
                    if cell.is_populated():
                        cell.eat_all()
                        cell.give_birth()
        self.migration()

        for row in self.island:
            for cell in row:
                if cell.is_populated():
                    cell.ages()
                    cell.lose_weight(pyvid)
                    cell.death()

    def migration(self):
        """
        Method for migration for all animals that shall migrate.

        This is done by running the migrate_all method in all cells when iterating
        through the island. Then the immigrants from the west and north neighbour
        cell are added to the list of herbivores and carnivores in the main cell.
        Then the focus is on the "finished_cell" in the upper left corner from the
        cell we are originally in. All immigrants have migrated from this cell, so
        the move_lists for herbivores and carnivores are cleared. The last step is
        to add the immigrants from the south and east neighbour cell to the
        "finished_cell"(still the west and north cell with respect to the main cell).
        """

        if not (len(self.island) < 3 or len(self.island[0]) < 3):
            for row in range(1, len(self.island)):
                for col in range(1, self.island_row_length):
                    cell = self.island[row][col]
                    north = self.island[row - 1][col]
                    west = self.island[row][col - 1]
                    if row < len(self.island) - 1 and col < self.island_row_length - 1:
                        south = self.island[row + 1][col]
                        east = self.island[row][col + 1]
                        if cell.is_habitable():
                            cells_around = (north, south, east, west)
                            cell.migrate_all(cells_around)
                            self.move_immigrants_to_cell(cell, north, west)
                    finished_cell = self.island[row - 1][col - 1]
                    if finished_cell.is_habitable():
                        for lst in finished_cell.move_herbs + finished_cell.move_carns:
                            lst.clear()
                        self.move_immigrants_to_finished_cell(finished_cell, north, west)

    @staticmethod
    def move_immigrants_to_cell(main_cell, north, west):
        """Move immigrants from the north and west neighbour cell into the main cell.

        :param main_cell: cell of specific landscape type.
        :param north: cell north of the main_cell.
        :param west: cell west of the main_cell.
        """

        if north.is_habitable() or west.is_habitable():
            main_cell.list_herbs.extend(north.move_herbs[1] + west.move_herbs[2])
            main_cell.list_carns.extend(north.move_carns[1] + west.move_carns[2])

    @staticmethod
    def move_immigrants_to_finished_cell(finished_cell, north, west):
        """Move immigrants from the south and east neighbour cell into "finished_cell".

        :param finished_cell: cell of specific landscape type.
        :param north: cell north of the main_cell, east of finished_cell.
        :param west: cell west of the main_cell, south of finished_cell.

        finished_cell is the cell in the upper left corner from the main cell
        (cell[row - 1][col - 1]) The west and north cell with
        respect to the main cell[row][col]).
        """

        if north.is_habitable() or west.is_habitable():
            finished_cell.list_herbs.extend(north.move_herbs[3] + west.move_herbs[0])
            finished_cell.list_carns.extend(north.move_carns[3] + west.move_carns[0])
