import textwrap

from biosim.simulation import BioSim

if __name__ == "__main__":

    geogr = """\
               WWWWWWWWW
               WLLLLLLLW
               WLLLLLLLW
               WLLLLLLLW
               WLLLLLLLW
               WLLLLLLLW
               WLLLLLLLW
               WLLLLLLLW
               WWWWWWWWW"""

    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (5, 5),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 50}
                          for _ in range(1000)]}
                 ]

    ini_carns = [{'loc': (5, 5),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 50}
                          for _ in range(1000)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456)

    sim.set_animal_parameters('Herbivore', {'mu': 1, 'omega': 0, 'a_half': 1000, 'gamma': 0, 'F': 0})
    sim.set_animal_parameters('Carnivore', {'a_half': 1000, 'mu': 1,
                                            'omega': 0, 'F': 0,
                                            'gamma': 0})

    sim.simulate(num_years=20, vis_years=1)
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=20, vis_years=1)
