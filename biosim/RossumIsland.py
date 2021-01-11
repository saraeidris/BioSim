from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Water, Desert, Highland, Lowland, Landscape


class RossumIsland:
    def __init__(self, island_map): # , params):
        island_dict = {'W': Water, 'D': Desert, 'L': Lowland, 'H': Highland}
        # self.island_coloumn_length = len(island_map) trengs denne?
        self.island_row_length = len(island_map.splitlines()[0])
        # self.params = params

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

    def fodder_grow(self):
        for rows in self.island:
            for element in rows:
                if isinstance(element, Highland) or isinstance(element, Lowland):
                    element.update_fodder()

    def eat_all(self):
        for rows in self.island:
            for element in rows:
                # Hvordan få autocomplete når vi har objekter i array
                if isinstance(element, Landscape):
                    element.eat_all()

    def set_init_population(self, init_pop):
        for dict in init_pop:
            location = dict['loc']
            cell = self.island[location[0]][location[1]]
            if isinstance(cell, Landscape) and cell.is_habitable():
                herbs_list = []
                carn_list = []
                for animal in dict['pop']:
                    if animal['species'] == 'Herbivore':
                        herbs_list.append(Herbivore())
                    if animal['species'] == 'Carnivore':
                        carn_list.append(Carnivore())
                cell.list_herbs += herbs_list
                cell.list_carns += carn_list

    def get_animal_population_for_each_cell(self):
        dict = {}
        for y, rows in enumerate(self.island):
            for x, cell in enumerate(rows):
                dict[(x, y)] = cell.get_population()
        return dict

    def get_number_of_animals(self):
        number_of_herbs = 0
        number_of_carns = 0
        for rows in self.island:
            for cell in rows:
                number_of_herbs += len(cell.list_herbs)
                number_of_carns += len(cell.list_carns)
        return number_of_herbs, number_of_carns, number_of_herbs + number_of_carns

    def annual_cycle(self):
        for row in self.island:
            for cell in row:
                if cell.is_habitable():
                    cell.update_fodder()
                    cell.eat_all()
                    cell.give_birth()
        #self.migration()
                    cell.ages()
                    cell.lose_weight()
                    cell.death()

    # def migration(self):
    #     for row in range(1, len(self.island) - 1):
    #         for col in range(1, self.island_row_length - 1):
    #             cell = self.island[row][col]
    #             if cell.is_habitable():
    #                 cell.migrate()
