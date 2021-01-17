import textwrap
from biosim.simulation import BioSim


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
                          for _ in range(150)]}
                 ]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456)

    sim.simulate(num_years=100, vis_years=1)