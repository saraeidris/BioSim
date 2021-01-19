import textwrap
from biosim.simulation import BioSim

"""
Simple island with one lowland cell surrounded by water
to simulate the development of both species in same cell.
"""

__author__ = "Sara Idris & Thorbjørn L Onsaker, NMBU"
__email__ = "said@nmbu.no & thon@nmbu.no"


if __name__ == '__main__':

    geogr = """\
               WWW
               WLW
               WWW"""

    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}
                 ]

    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(20)]}
                 ]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456, ymax_animals=240)

    sim.simulate(num_years=50, vis_years=1)
    sim.add_population(ini_carns)
    sim.simulate(num_years=200, vis_years=1)