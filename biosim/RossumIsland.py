from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Water, Desert, Highland, Lowland, Landscape
import random


class RossumIsland:
    def __init__(self, island_map):
        island_dict = {'W': Water, 'D': Desert, 'L': Lowland, 'H': Highland}
        if len(island_map) == 0:
            raise ValueError('No island map was given')
        self.island_row_length = len(island_map.splitlines()[0])

        self.island = []
        for lines in island_map.splitlines():
            self.island.append(self.splits(lines, island_dict))

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
        for land_type in line:
            if land_type not in island_dict:
                raise ValueError('Character not allowed as a part of island map')

        return [island_dict[land]() for land in line]

    def insert_population(self, pop):
        """
        Inserts population of either herbivores or carnivores
        :param pop: list with dictionary that contains either
                    herbivore or carnivore, and a wanted location.
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
        """
        :return: the total amount of herbivores and carnivores on the island.
        """
        herb_array = [[len(cell.list_herbs) for cell in row] for row in self.island]
        carn_array = [[len(cell.list_carns) for cell in row] for row in self.island]
        sum_herb = sum([sum(row) for row in herb_array])
        sum_carn = sum([sum(row) for row in carn_array])
        return herb_array, carn_array, sum_herb, sum_carn

    def get_stats(self):
        """

        :return: list with different attributes for both herbivores and carnivores
        """
        age_herbs = []
        age_carns = []
        weight_herbs = []
        weight_carns = []
        fitness_herbs = []
        fitness_carns = []
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
        """
        checks if pyvid (Pythonvirus disease) occurs or not.

        :return:
        bool
            True if pyvid occurs in current year.
        """
        return random.randint(1, 20) == 20

    def annual_cycle(self):
        """
        the annual cycle on Rossumøya.
        """
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
                    cell.lose_weight(self.pyvid())
                    cell.death()

    def migration(self):
        """
        Checks if the cell the animal wants to migrate to is habitable
        """
        if not (len(self.island) < 3 or len(self.island[0]) < 3):
            for row in range(1, len(self.island)): # må fjerne -1 på versjon 2
                for col in range(1, self.island_row_length): # må fjerne -1 på versjon 2
                    cell = self.island[row][col]
                    north = self.island[row - 1][col]  # V2
                    west = self.island[row][col - 1]  # V2
                    if row < len(self.island) - 1 and col < self.island_row_length - 1: # V2
                        south = self.island[row + 1][col]  # V2
                        east = self.island[row][col + 1] # V2
                        if cell.is_habitable(): #and cell.is_populated(): # cell is populated må bort i versjon 2
                        # north = self.island[row - 1][col] # V1
                        # south = self.island[row + 1][col] # V1
                        # east = self.island[row][col + 1] # V1
                        # west = self.island[row][col - 1] # V1
                            cells_around = (north, south, east, west)
                            cell.migrate_all(cells_around) # Her slutter versjon 1
                            self.move_immigrants_to_cell(cell, north, west)
                    finished_cell = self.island[row - 1][col - 1]
                    if finished_cell.is_habitable():
                        for lst in finished_cell.move_herbs + finished_cell.move_carns:
                            lst.clear()
                        self.move_immigrants_to_finished_cell(finished_cell, north, west)

            # for row in range(1, len(self.island)):
            #     for col in range(1, self.island_row_length):
            #         cell = self.island[row][col]
            #         if cell.is_habitable():
            #             north = self.island[row - 1][col]
            #             south = self.island[row + 1][col]
            #             east = self.island[row][col + 1]
            #             west = self.island[row][col - 1]
            #             cell.list_herbs.extend(north.move_herbs[1] + south.move_herbs[0] +
            #                                    east.move_herbs[3] + west.move_herbs[2])
            #             cell.list_carns.extend(north.move_carns[1] + south.move_carns[0] +
            #                                    east.move_carns[3] + west.move_carns[2])
            #         if self.island[row - 1][col - 1].is_habitable():
            #             for lst in self.island[row - 1][col - 1].move_herbs:
            #                 lst.clear()
            #             for lst in self.island[row - 1][col - 1].move_carns:
            #                 lst.clear()
    @staticmethod
    def move_immigrants_to_cell(cell, north, west):
        if north.is_habitable() or west.is_habitable():
            cell.list_herbs.extend(north.move_herbs[1] + west.move_herbs[2])
            cell.list_carns.extend(north.move_carns[1] + west.move_carns[2])

    @staticmethod
    def move_immigrants_to_finished_cell(cell, north, west):
        if north.is_habitable() or west.is_habitable():
            cell.list_herbs.extend(north.move_herbs[3] + west.move_herbs[0])
            cell.list_carns.extend(north.move_carns[3] + west.move_carns[0])
