import random

import matplotlib.pyplot as plt
from .graphics import Graphics

from biosim.RossumIsland import RossumIsland
from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland


class BioSim:

    DEFAULT_CMAX_ANIMALS = {'Herbivore': 200, 'Carnivore': 50}
    DEFAULT_HIST_SPECS = {'weight': {'max': 60, 'delta': 2},
                          'age': {'max': 60, 'delta': 2},
                          'fitness': {'max': 1, 'delta': 0.05}}

    def __init__(self, island_map, ini_pop, seed,
                 ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_base=None, img_fmt='png'):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. ’png’"""

        random.seed(seed)
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.ini_pop = ini_pop
        self.island = RossumIsland(island_map)
        self.island.insert_population(self.ini_pop)
        self.island_map = island_map
        self.animal = 0
        self._step = 0

        if self.cmax_animals is None:
            self.cmax_animals = self.DEFAULT_CMAX_ANIMALS

        if self.hist_specs is None:
            self.hist_specs = self.DEFAULT_HIST_SPECS
        if len(self.hist_specs) < 3:
            new = self.merge_params(self.DEFAULT_HIST_SPECS, self.hist_specs)
            self.hist_specs = new

        self._graphics = Graphics(self.hist_specs, self.cmax_animals, self.img_base, self.img_fmt)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        for key in params:
            if key not in Carnivore.params:
                raise KeyError('Invalid parameter name: ' + key)
            if not (isinstance(params[key], int) or
                    isinstance(params[key], float)) or params[key] < 0:
                raise ValueError(key + ' must be a positive integer og float')
            if 'DeltaPhiMax' in params and params['DeltaPhiMax'] <= 0:
                raise ValueError('DeltaPhiMax must be strictly positive')
            if 'eta' in params and params['eta'] > 1:
                raise ValueError('eta must be a value between 0 and 1')
        if species == 'Carnivore':
            Carnivore().set_params(self.merge_params(Carnivore().params, params))
        elif species == 'Herbivore':
            Herbivore().set_params(self.merge_params(Herbivore().params, params))
        else:
            raise ValueError('Species must be either Carnivore or Herbivore')

    @staticmethod
    def merge_params(params1, params2):
        """
        merges default parameters with wanted parameters
        :param params1: default parameters
        :param params2: wanted parameters
        :return:
        """
        return {**params1, **params2}

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'L':
            Lowland().set_params(self.merge_params(Lowland().d_landscape, params))
        elif landscape == 'H':
            Highland().set_params(self.merge_params(Highland().d_landscape, params))
        else:
            raise ValueError(landscape + ' is not a legal landscape type')

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """

        if img_years is None:
            img_years = vis_years

        if img_years % vis_years != 0:
            raise ValueError('img_steps must be multiple of vis_steps')

        self._final_step = self._step + num_years
        self._graphics.setup(self._final_step, img_years)

        # plot initial status if at very beginning of simulation
        if self._step == 0:
            self._graphics.update(self._step,
                                  self.island.get_stats(),
                                  self.island.get_pop_info(),
                                  self.island_map)
            self.island.annual_cycle()
        while self._step < self._final_step:
            self._step += 1

            if self._step % vis_years == 0:
                self._graphics.update(self._step,
                                      self.island.get_stats(),
                                      self.island.get_pop_info(),
                                      self.island_map)
            self.island.annual_cycle()

    def add_population(self, population):
        """
        Add a population to the island
        :param population: List of """
        self.island.insert_population(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._step

    @property
    def num_animals(self):
        """
        Total number of animals
        dictionaries specifying population
        on island.
        """
        total_num = (self.island.get_pop_info()[2] +
                     self.island.get_pop_info()[3])
        return total_num

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        """
        num_animal_dict = {'Herbivore': self.island.get_pop_info()[2],
                           'Carnivore': self.island.get_pop_info()[3]}
        return num_animal_dict

    def make_movie(self):
        """
        Create MPEG4 movie from visualization images saved.
        """
        return self._graphics.make_movie("mp4")
