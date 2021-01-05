
from numpy import random as rand
import textwrap

class Herbivores:
    def __init__(self, w_birth, sigma_birth, a):
        self.w_birth = w_birth
        self.sigma_birth = sigma_birth
        self.a_birth = a

    def weight(self):
        return rand.normal(self.w_birth, self.sigma_birth)

    #def age(self):


if __name__ == '__main__':
        geogr = """\
                   WWWWWWWWWWWWWWWWWWWWW
                   WWWWWWWWHWWWWLLLLLLLW
                   WHHHHHLLLLWWLLLLLLLWW
                   WHHHHHHHHHWWLLLLLLWWW
                   WHHHHHLLLLLLLLLLLLWWW
                   WHHHHHLLLDDLLLHLLLWWW
                   WHHLLLLLDDDLLLHHHHWWW
                   WWHHHHLLLDDLLLHWWWWWW
                   WHHHLLLLLDDLLLLLLLWWW
                   WHHHHLLLLDDLLLLWWWWWW
                   WWHHHHLLLLLLLLWWWWWWW
                   WWWHHHHLLLLLLLWWWWWWW
                   WWWWWWWWWWWWWWWWWWWWW"""
        geogr = textwrap.dedent(geogr)

        ini_herbs = [{'loc': (10, 10),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(150)]}]
        sim = Herbivores(island_map=geogr, ini_pop=ini_herbs,
                     seed=123456,
                     hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                                 'age': {'max': 60.0, 'delta': 2},
                                 'weight': {'max': 60, 'delta': 2}},
                     )

        sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
        sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                                'omega': 0.3, 'F': 65,
                                                'DeltaPhiMax': 9.})
        sim.set_landscape_parameters('L', {'f_max': 700})

        sim.simulate(num_years=100, vis_years=1)
   # p1 = Herbivores(8, 1.5)
    #print(p1.weight())
