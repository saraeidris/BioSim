import random
from math import exp

__author__ = "Sara Idris & Thorbjørn L Onsaker, NMBU"
__email__ = "said@nmbu.no & thon@nmbu.no"


class Animal:
    """Baseclass for animals on the island."""

    params = None

    @classmethod
    def set_params(cls, new_params):
        """Overrides animal parameters.

        :param new_params: new input parameters

        """

        cls.params.update(new_params)

    def __init__(self, age=0, weight=None):
        r"""
            :param age:  age of animal; age 0 if None.
            :type age: int
            :param weight:  weight of animal; randomly normal distributed weight if None
            :type weight: float

            :raises ValueError: if age is 0 or not of type int,
                                or weight is less than or equal to 0
        Animals are born with weight

        .. math::

            \begin{equation}
            w \sim N(w_{birth} + \sigma_{birth})
            \end{equation}

        """

        self.age = age
        self.weight = weight

        if self.weight is None:
            self.weight = 0
            while self.weight <= 0:
                self.weight = random.gauss(self.params['w_birth'], self.params['sigma_birth'])
        if self.weight <= 0:
            raise ValueError('All animals must have a positive weight')
        if not isinstance(self.age, int):
            raise ValueError('Age of animal must be an integer')
        if self.age < 0:
            raise ValueError('Age of animal must be a non-negative value')

    def aging(self):
        """Updates the age with 1 for each year."""

        self.age += 1

    def get_fitness(self):
        r"""Calculate fitness for specie.

        The animals' fitness is calculated with the following formula:

        .. math::

            \begin{equation}
            \Phi
            \begin{cases}
            0 & w \leq 0 \\
            q^{+}(a, a_{\frac{1}{2}}, \phi_{age}) \times (q^{-}(w, w_{1/2}, \phi_{weight})) & else
            \end{cases}
            \end{equation}

        where

        .. math::

            \begin{equation}
            q^{\pm}(x, x,_{\frac{1}{2}}, \phi) = \frac{1}{1+e^{\pm}\phi(x-x_{\frac{1}{2}})}
            \end{equation}

        Note that

        .. math::

            \begin{equation}
            0 \leq 0 \Phi \leq 1.
            \end{equation}

        :returns: Current fitness for specie.

        """

        if self.weight <= 0:
            return 0
        else:
            fitness = ((1 / (1 + exp(self.params['phi_age'] *
                                     (self.age - self.params['a_half'])))) *
                       (1 / (1 + exp(-self.params['phi_weight'] *
                                     (self.weight - self.params['w_half'])))))
            return fitness

    def weight_loss(self, pyvid=False, num_animals=None):
        """
        Reduces the weight of the animal with eta * its own weight,
        and half its weight if it gets infected with pyvid (Pythonvirus Disease).

        :param pyvid: True if pyvid occurs this year; default False
        :param num_animals: number of animals in cell; default None
        """

        if pyvid and random.random() < 0.02 * num_animals:
            self.weight -= 0.5 * self.weight
        else:
            self.weight -= self.params['eta'] * self.weight

    def migrate(self):
        """Decides whether a specie migrates or stay in the same cell.

        Returns True if specie migrate
        """

        return random.random() < self.params['mu'] * self.get_fitness()

    def dies(self):
        r"""Decide whether the specie dies or not.

        Animals die with certainty if its weight is w = 0.
        Otherwise, the probability for death is

        .. math::

            \begin{equation}
            \omega(1-\Phi)
            \end{equation}

        Returns True if specie dies
        """

        return (self.weight <= 0) or (random.random() <
                                      self.params['omega'] * (1 - self.get_fitness()))

    def mate(self, n):
        r"""Decide whether a specie gets an offspring or not.

        The probability to give birth to an offspring in a year

        .. math::

            \begin{equation}
            min(1, \gamma \times \Phi \times (N-1))
            \end{equation}

        The probability is also 0 if the weight is

        .. math::

            \begin{equation}
            w < \zeta (w_{birth} + \sigma_{birth})
            \end{equation}

        :param n: number of animals of the same specie
        :returns: an offspring of the same specie if instance give birth
        """

        if self.weight < self.params['zeta'] * (self.params['w_birth'] +
                                                self.params['sigma_birth']):
            return
        if random.random() < self.params['gamma'] * self.get_fitness() * (n - 1):
            offspring = self.__class__()
            if self.weight < (self.params['xi'] * offspring.weight):
                return
            self.weight -= (self.params['xi'] * offspring.weight)
            return offspring


class Herbivore(Animal):
    """Subclass for Animal, contains parameters for herbivores."""

    params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
              'a_half': 40.0, 'phi_age': 0.6, 'w_half': 10.0,
              'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
              'omega': 0.4, 'F': 10.0}

    def consumed_fodder(self, available_fodder):
        """Decide how much fodder a herbivore eats and adds the gained weight.

        :param available_fodder: Amount of available fodder left in current cell
        :returns: fodder left in current cell
        """

        if available_fodder >= 0:
            if available_fodder < self.params['F']:
                self.weight += (available_fodder * self.params['beta'])
                return available_fodder
            else:
                self.weight += (self.params['F'] * self.params['beta'])
                return self.params['F']


class Carnivore(Animal):
    """Subclass for Animal, contains parameters for carnivores."""

    params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125,
              'a_half': 40.0, 'phi_age': 0.3, 'w_half': 4.0,
              'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
              'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}

    def consumed_herbs(self, herb_sorted):
        r"""Decides whether a carnivore kills and eat a herbivore.

        Carnivores will kill a herbivore with probability

        .. math::

            \begin{equation}
            p =
            \begin{cases}
            0 & if  \Phi_{carn} \leq \Phi_{herb} \\
            \frac{\Phi_{carn}-\Phi_{herb}}{\Delta\Phi_{max}}& if
            0 < \Phi_{carn}-\Phi_{herb} < \Delta\Phi_{max} \\
            1 & otherwise.
            \end{cases}
            \end{equation}

        :param herb_sorted: Herbivores sorted by fitness from low to high
        :returns: list of killed herbs
        """

        wanted_food = self.params['F']
        killed_herbs = []
        if len(herb_sorted) == 0:
            return killed_herbs
        for herb in herb_sorted:
            if wanted_food == 0:
                break
            if self.get_fitness() <= herb.get_fitness():
                break
            elif (self.get_fitness() - herb.get_fitness()) < self.params['DeltaPhiMax']:
                p = ((self.get_fitness() - herb.get_fitness()) / self.params['DeltaPhiMax'])
            else:
                p = 1
            if random.random() < p:
                if wanted_food < herb.weight:
                    self.weight += self.params['beta'] * wanted_food
                    killed_herbs.append(herb)
                    break
                self.weight += self.params['beta'] * herb.weight
                wanted_food -= herb.weight
                killed_herbs.append(herb)
        return killed_herbs
