from biosim.animals import Animal, Herbivore, Carnivore
import pytest
import random
from scipy.stats import normaltest

random.seed(123456)

"""Various tests made for the Animal Class."""

__author__ = "Sara Idris & Thorbjørn L Onsaker, NMBU"
__email__ = "said@nmbu.no & thon@nmbu.no"


@pytest.fixture
def set_params(request):
    Herbivore.set_params(request.param)
    yield
    Herbivore.set_params(Herbivore.params)


@pytest.mark.parametrize('set_params', [{'omega': 0.0}], indirect=True)
def test_bact_certain_survival(set_params):
    """
    This test is *deterministic*: We set death probability to 0
    by setting omega to 0,
    thus the animal must never die. We call dies() multiple
    times to test this.
    """

    h = Herbivore()
    for _ in range(100):
        assert not h.dies()


@pytest.mark.parametrize('set_params', [{'omega': 0.4}], indirect=True)
def test_migration_and_death(mocker, set_params):
    """
    test that all animals migrates and dies when random.random is set
    to 0, and that all animals survive and stay in their cell when
    random.random is set to 1.
    """

    mocker.patch('random.random', return_value=0)
    for _ in range(10):
        h = Herbivore()
        assert h.migrate() is True
        assert h.dies() is True
    mocker.patch('random.random', return_value=1)
    for _ in range(10):
        c = Carnivore()
        assert c.migrate() is False
        assert c.dies() is False


def test_mate_method_and_offspring_weight(mocker):
    """
    Test that an offspring is of same class as parent, and that
    its weight is greater than zero.
    """

    mocker.patch('random.random', return_value=0)
    for _ in range(100):
        h = Herbivore(5, 50)
        c = Carnivore(5, 50)
        h_offspring = h.mate(100)
        c_offspring = c.mate(100)
        assert type(h_offspring) == Herbivore and h_offspring.weight > 0
        assert type(c_offspring) == Carnivore and c_offspring.weight > 0


def test_animal_age():
    """
    Test that a new animal has age 0.
    """

    a = Herbivore()
    assert a.age == 0


def test_animal_aging():
    """
    This test is deterministic: for each call to aging(),
    the age must increase by one year.
    """

    a = Herbivore()
    for n in range(10):
        a.aging()
        assert a.age == n + 1


def test_animal_certain_death():
    """
    Test that animal die if weight is equal or less than 0.
    """

    c = Carnivore()
    h = Herbivore()
    c.weight = 0
    h.weight = -3
    assert c.dies()
    assert h.dies()


def test_herbivore_should_eat_when_fodder_is_available():
    """
    Test that a herbivore eats an amount of
    F when more than F is available.
    """

    animal = Herbivore()
    consumed_fodder = animal.consumed_fodder(100)

    assert consumed_fodder == 10


def test_herbivore_eat_all_remaining_fodder():
    """
    Test that a herbivore eats the amount of fodder
    available when there is less than F amount of fodder
    left.
    """

    animal = Herbivore()
    consumed_fodder = animal.consumed_fodder(7)

    assert consumed_fodder == 7


def test_weight_loss(mocker):
    """
    Test that weight_loss reduces an instance´s weight
    with eta * weight, and 4 * eta * weight if the instance get pyvid.
    """

    mocker.patch('random.random', return_value=0)
    a = Herbivore()
    a.weight = 20
    a.weight_loss()
    assert a.weight == 20 - (a.params['eta'] * 20)
    c = Carnivore()
    c.weight = 20
    c.weight_loss(True, 100)
    assert c.weight == 10


def test_error_when_negative_weight_given():
    """
    Test that a ValueError is raised if the input weight
    is equal or less than 0.
    """

    with pytest.raises(ValueError):
        Animal(weight=-1)
    with pytest.raises(ValueError):
        Animal(weight=0)


def test_age_raise_valueerror():
    """
    Test that a ValueError is raised if the input age
    is less than 0 or not an integer.
    """

    with pytest.raises(ValueError):
        Animal(1.1, 20)
    with pytest.raises(ValueError):
        Animal(-1, 20)


def test_get_fitness():
    """
    Test that get_fitness returns a fitness between 0 and 1.
    """

    for _ in range(100):
        fitness = Herbivore().get_fitness()
        assert 1 >= fitness >= 0


def test_weight_normal_distributed():
    """
    Test that the weight given as default is normal distributed
    and passes the test with an alpha-value of 0.05.
    """

    alpha = 0.05
    herb_weights = [Herbivore().weight for _ in range(1000)]
    carn_weights = [Carnivore().weight for _ in range(1000)]
    result_herb = normaltest(herb_weights)
    result_carn = normaltest(carn_weights)
    assert alpha < result_herb[1]
    assert alpha < result_carn[1]
