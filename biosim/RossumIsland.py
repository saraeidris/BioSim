from biosim.animals import Herbivore, Carnivore, Animal
from biosim.landscape import Water, Desert, Highland, Lowland, Landscape


class RossumIsland:
    def __init__(self, island_map):
        island_dict = {'W': Water, 'D': Desert, 'L': Lowland, 'H': Highland}
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

    def num_animals(self):
        number = 0
        for row in self.island:
            for cell in row:
                if not isinstance(cell, Water):
                    number += len(cell.list_animals())
        return number

    def set_init_population(self, init_pop):
        for dic in init_pop:
            location = dic['loc']
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

    def get_animal_population_for_each_cell(self):
        dict = {}
        for y, rows in enumerate(self.island):
            for x, cell in enumerate(rows):
                dict[(x, y)] = cell.get_population()
        return dict

    def get_2darray_for_pop(self):
        herb_array = [[len(cell.list_herbs) for cell in row] for row in self.island]
        carn_array = [[len(cell.list_carns) for cell in row] for row in self.island]
        return herb_array, carn_array

    def get_number_of_animals(self):
        number_of_herbs = 0
        number_of_carns = 0
        for rows in self.island:
            for cell in rows:
                number_of_herbs += len(cell.list_herbs)
                number_of_carns += len(cell.list_carns)
        return number_of_herbs, number_of_carns, number_of_herbs + number_of_carns

    def get_fitness_of_animal(self):
        fitness_herbs = []
        fitness_carns = []
        for row in self.island:
            for cell in row:
                fitness_herbs.extend(cell.get_herb_fitness())
                fitness_carns.extend(cell.get_carn_fitness())
        return fitness_carns, fitness_herbs

    def annual_cycle(self):
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
                    cell.lose_weight()
                    cell.death()

    def migration(self):
        if len(self.island) > 3 or len(self.island[0]) > 3:
            for row in range(1, len(self.island) - 1):
                for col in range(1, self.island_row_length - 1):
                    cell = self.island[row][col]
                    if cell.is_habitable() and cell.is_populated():
                        north = self.island[row - 1][col]
                        south = self.island[row + 1][col]
                        east = self.island[row][col + 1]
                        west = self.island[row][col - 1]
                        cells_around = (north, south, east, west)
                        cell.migrate_all(cells_around)
    #                     if north.is_habitable():
    #                         cell.list_herbs.extend(north.move_herbs[1])
    #                         cell.list_carns.extend(north.move_carns[1])
    #                     if west.is_habitable():
    #                         cell.list_herbs.extend(north.move_herbs[2])
    #                         cell.list_carns.extend(north.move_carns[2])
    #                 finished_cell = self.island[row - 1][col - 1]
    #                 if finished_cell.is_habitable():
    #                     for lst in finished_cell.move_herbs:
    #                         lst.clear()
    #                     for lst in finished_cell.move_carns:
    #                         lst.clear()
    #                     if self.island[row][col - 1].is_habitable():
    #                         finished_cell.list_herbs.extend(self.island[row][col - 1].move_herbs[0])
    #                         finished_cell.list_carns.extend(self.island[row][col - 1].move_carns[0])
    #                     if self.island[row - 1][col].is_habitable():
    #                         finished_cell.list_herbs.extend(self.island[row][col - 1].move_herbs[3])
    #                         finished_cell.list_carns.extend(self.island[row][col - 1].move_carns[3])
    #         for lst in self.island[-2][-2].move_herbs:
    #             lst.clear()
    #         for lst in self.island[-2][-2].move_carns:
    #             lst.clear()

            for row in range(1, len(self.island) - 1):
                for col in range(1, self.island_row_length - 1):
                    cell = self.island[row][col]
                    if cell.is_habitable():
                        north = self.island[row - 1][col]
                        south = self.island[row + 1][col]
                        east = self.island[row][col + 1]
                        west = self.island[row][col - 1]
                        cell.list_herbs.extend(north.move_herbs[1] + south.move_herbs[0] +
                                               east.move_herbs[3] + west.move_herbs[2])
                        cell.list_carns.extend(north.move_carns[1] + south.move_carns[0] +
                                               east.move_carns[3] + west.move_carns[2])
                    if self.island[row - 1][col - 1].is_habitable():
                        for lst in self.island[row - 1][col - 1].move_herbs:
                            lst.clear()
                        for lst in self.island[row - 1][col - 1].move_carns:
                            lst.clear()






