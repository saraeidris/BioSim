import random
from biosim.animals import Herbivore
from biosim.landscape import Landscape, Lowland, Highland


class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_base=None, img_fmt='png'):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param img_base: String with beginning of file name for figures, including path :param img_fmt: String with file type for figures, e.g. ’png’
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used. cmax_animals is a dict mapping species names to numbers, e.g.,
            {’Herbivore’: 50, ’Carnivore’: 20}
        hist_specs is a dictionary with one entry per property for which a histogram shall be shown. For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {’weight’: {’max’: 80, ’delta’: 2}, ’fitness’: {’max’: 1.0, ’delta’: 0.05}} Permitted properties are ’weight’, ’age’, ’fitness’.
        If img_base is None, no figures are written to file. Filenames are formed as
            ’{}_{:05d}.{}’.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0. img_base should contain a path and beginning of a file name. """
        self.island_map = island_map
        random.seed(seed)
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.ini_pop = ini_pop
        self.carnivore_params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125,
                                 'a_half': 40.0, 'phi_age': 0.3, 'w_half': 4.0,
                                 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
                                 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}
        self.herbivore_params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
                                 'a_half': 40.0, 'phi_age': 0.6, 'w_half': 10.0,
                                 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                                 'omega': 0.4, 'F': 10.0}
        self.lowland_params = {'f_max': 800}
        self.highland_params = {'f_max': 300}
        self.island = island_map
        # Highland(None, None, None, None, self.highland_params['f_max'],
        # self.herbivore_params['w_birth'],
        # self.herbivore_params['sigma_birth'],
        # self.ini_pop)
        self.ini_pop = self.create_population(ini_pop)

    def annual_cycle(self):
        self.island[35].update_fodder()
        self.island[35].eat()
        self.island[35].mate()
        self.island[35].ages()
        self.island[35].lose_weight()
        self.island[35].death()

    def create_population(self, init_pop):
        animals = []
        for cell in init_pop:
            for animal in cell['pop']:
                if animal['species'] == 'Herbivore':
                    animals.append(Herbivore(
                        self.herbivore_params, animal['age'],
                        animal['weight']))
                    # Må fikses på når hele øya er på plass
        print(animals)
        return animals

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Carnivore':
            self.carnivore_params = self.merge_params(self.carnivore_params, params)
        elif species == 'Herbivore':
            self.herbivore_params = self.merge_params(self.herbivore_params, params)
        else:
            raise ValueError

    # Hjelpemetode bør være privat
    def merge_params(self, params, params2):
        return {**params, **params2}

    # Må fikses
    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape """
        if landscape == 'L':
            self.lowland_params = self.merge_params(self.lowland_params, params)
        elif landscape == 'H':
            self.highland_params = self.merge_params(self.highland_params, params)
        else:
            raise ValueError

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """

        for _ in range(num_years):
            self.feeding()
            self.fodder_grow()
            self.ages()
            for animal in self.ini_pop:
                print(animal.weight())
                print(animal.get_fitness())
                print(animal.get_age())

    def fodder_grow(self):
        Lowland.update_fodder()
        Highland.update_fodder()

    def ages(self):
        for animal in self.ini_pop:
            animal.ages()

    def feeding(self):
        herbs = list(filter(lambda obj: isinstance(obj, Herbivore), self.ini_pop))
        new_herbs_list = []
        # carnivores = list(filter(lambda obj: isinstance(obj, Carnivores), self.ini_pop))
        while len(herbs) > 0:
            index = random.randint(0, len(herbs) - 1)
            herb = herbs.pop(index)
            herb.eat(Landscape.get_fodder())
            new_herbs_list.append(herb)

        # Do carnivore stuff

        self.ini_pop = new_herbs_list

    # def add_population(self, population):
    #
    #     """
    #     Add a population to the island
    #     :param population: List of """

    # @property
    # def year(self):
    # """Last year simulated."""

    # @property
    # def num_animals(self, ini_pop):
    #
    #     """
    #     Total number of animals
    #     dictionaries specifying population
    #     on island.
    #     """
    #
    #  @property
    #  def num_animals_per_species(self):
    #  """Number of animals per species in island, as dictionary."""

    # def make_movie(self):
    # """Create MPEG4 movie from visualization images saved."""
