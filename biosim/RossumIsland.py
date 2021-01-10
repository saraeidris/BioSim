from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Water, Desert, Highland, Lowland, Landscape


class RossumIsland:
    def __init__(self, island_map, params):
        island_dict = {'W': Water, 'D': Desert, 'L': Lowland, 'H': Highland}
        # self.island_coloumn_length = len(island_map) trengs denne?
        self.island_row_length = len(island_map.splitlines()[0])
        self.params = params

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

    def splits(self, line, island_dict):
        for land_type in line:
            if land_type not in island_dict:
                raise ValueError('Character not allowed as a part of island map')

        return [island_dict[land]() for land in line]

    def count_animals(self):
        num_animals = []
        for specie in self.species:
            num_animals.append(specie)

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
                        herbs_list.append(Herbivore(self.params, animal['age'],
                                                    animal['weight']))
                    if animal['species'] == 'Carnivore':
                        carn_list.append(Carnivore(self.params, animal['age'],
                                                   animal['weight']))
                cell.list_herbs = cell.list_herbs + herbs_list
                cell.list_carns = cell.list_carns + carn_list

    def get_animal_stats(self):
        dict = {}
        for y, rows in enumerate(self.island):
            for x, cell in enumerate(rows):
                dict[(x, y)] = cell.get_population()
        return dict

    def annual_cycle(self):
        self.island[10][10].update_fodder()
        self.island[10][10].eat()
        self.island[10][10].mate()
        self.island[10][10].ages()
        self.island[10][10].lose_weight()
        self.island[10][10].death()
