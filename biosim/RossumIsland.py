from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Water, Desert, Highland, Lowland

class RossumIsland:
    def __init__(self, island_map, ini_pop=None):
        self.island_map = island_map
        self.ini_pop = ini_pop
        island_dict = {'W': Water, 'D': Desert, 'L': Lowland, 'H': Highland}

        self.island_map = self.island_map.splitlines()
        #self.island_coloumn_length = len(island_map) trengs denne?
        self.island_row_length = len(island_map[0])
        def splits(line):
            return [island_dict[land] for land in line]

        new_map = []
        for lines in island_map:
            new_map.append(splits(lines))
        for land_type in island_map[0] + island_map[-1]:
            if not land_type == 'W':
                raise ValueError('Outer edges of map must be water')

        for rows in island_map:
            if len(rows) != self.island_row_length:
                raise ValueError('All rows in the island map must be the same length')
            if not rows[0] == 'W' or rows[-1] == 'W':
                raise ValueError('Outer edges of map must be water')

            for land_type in rows:
                if land_type not in island_dict:
                    raise ValueError('Character not allowed as a part of island map')



    def count_animals(self):
        num_animals = []
        for specie in self.species:
            num_animals.append(specie)
