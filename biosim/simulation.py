import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from biosim.RossumIsland import RossumIsland
from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Lowland, Highland


class BioSim:
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
        :param img_fmt: String with file type for figures, e.g. ’png’
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
            {’Herbivore’: 50, ’Carnivore’: 20}
        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {’weight’: {’max’: 80, ’delta’: 2}, ’fitness’: {’max’: 1.0, ’delta’: 0.05}}
        Permitted properties are ’weight’, ’age’, ’fitness’.
        If img_base is None, no figures are written to file.
        Filenames are formed as
            ’{}_{:05d}.{}’.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name. """
        random.seed(seed)
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.ini_pop = ini_pop
        self.island = RossumIsland(island_map)
        self.current_year = 0
        self.island.set_init_population(self.ini_pop)
        self.island_map = island_map
        self.animal = 0
        self._year = 0

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        for key in params:
            if key not in Carnivore.params:
                raise KeyError('Invalid parameter name: ' + key)
            if not (isinstance(params[key], int) or isinstance(params[key], float)) or params[key] < 0:
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

        fig = plt.figure(constrained_layout=False)
        ax1 = fig.add_subplot(2, 3, 1)

        # axes for text
        # ax1 = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        ax1.axis('off')  # turn off coordinate system
        _map = self.island_map

        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in _map.splitlines()]

        fig.add_subplot(2, 3, 2)

        ax1.imshow(map_rgb)

        ax1.set_xticks(range(len(map_rgb[0])))
        ax1.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        ax1.set_yticks(range(len(map_rgb)))
        ax1.set_yticklabels(range(1, 1 + len(map_rgb)))

        axlg = fig.add_axes([3.85, 1.1, 0.1, 0.8])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

        list_with_population_for_all_years = []
        list_with_years = []
        for _ in range(num_years):
            self.island.annual_cycle()
            list_with_years.append(self.current_year)
            list_with_population_for_all_years.append(self.island.get_number_of_animals())
            self.current_year += 1
            fig.add_subplot(2, 3, 3)
            plt.hist(self.island.get_fitness_of_animal()[1])
            plt.title('Fitness')
            fig.add_subplot(2, 3, 4)
            plt.hist(self.island.get_stats()[3])
            plt.title('weight')
            fig.add_subplot(2, 3, 5)
            plt.hist(self.island.get_stats()[1])
            plt.title('age')
            fig.add_subplot(2, 3, 6)
            plt.plot(list_with_years, list_with_population_for_all_years)
            plt.title('Animal count')


            plt.pause(10e-3)

    # sns.heatmap(self.island.get_2darray_for_pop()[0], cbar=False, cmap="YlGnBu")

    def add_population(self, population):

        """
        Add a population to the island
        :param population: List of """
        self.island.set_init_population(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """
        Total number of animals
        dictionaries specifying population
        on island.
        """
        return self.island.get_number_of_animals()[2]

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        """
        num_animal_dict = {'Herbivore': self.island.get_number_of_animals()[0],
                           'Carnivore': self.island.get_number_of_animals()[1]}
        return num_animal_dict

    # def make_movie(self):
    # """Create MPEG4 movie from visualization images saved."""
