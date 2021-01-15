import matplotlib.pyplot as plt
import textwrap

from biosim.simulation import BioSim

if __name__ == "__main__":
    plt.ion()

    geogr = """\
               WWWWWWWWWWW
               WDDDDDDDDDW
               WDDDDDDDDDW
               WDDDDDDDDDW
               WDDDDDDDDDW
               WDDDDDDDDDW
               WDDDDDDDDDW
               WDDDDDDDDDW
               WDDDDDDDDDW
               WDDDDDDDDDW
               WWWWWWWWWWW"""

    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (6, 6),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}
                 ]

    ini_carns = [{'loc': (6, 6),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456)

    sim.set_animal_parameters('Herbivore', {'mu': 1, 'omega': 0, 'a_half': 1000, 'gamma': 0})
    sim.set_animal_parameters('Carnivore', {'a_half': 1000, 'mu': 1,
                                            'omega': 0, 'F': 0,
                                            'gamma': 0})

    sim.simulate(num_years=100, vis_years=1)
