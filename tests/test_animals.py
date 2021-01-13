from biosim.animals import Animal, Herbivore, Carnivore
import pytest
import random
from scipy.stats import normaltest


@pytest.fixture
def set_params(request):
    Herbivore.set_params(request.param)
    yield
    Herbivore.set_params(Herbivore.params)


@pytest.mark.parametrize('set_params', [{'omega': 0.0}], indirect=True)
def test_bact_certain_survival(set_params):
    """
    This test is *deterministic*: We set death probability to 0,
    thus the bacterium must never die. We call dies() multiple
    times to test this.
    """

    h = Herbivore()
    for _ in range(100):
        assert not h.dies()


@pytest.mark.parametrize('set_params', [{'omega': 0.4}], indirect=True)
def test_migration_and_death(mocker, set_params):
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


def test_animal_age():
    """
    Test that a new animal has age 0.
    """
    a = Herbivore()
    assert a.age == 0


def test_animal_aging():
    """
    This test is *determinstic*: for each call to aging(),
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

    animal = Herbivore(0, weight=5)
    consumed_fodder = animal.consumed_fodder(100)

    assert consumed_fodder == 10


def test_herbivore_eat_all_remaining_fodder():
    animal = Herbivore(0, weight=5)
    consumed_fodder = animal.consumed_fodder(7)

    assert consumed_fodder == 7


def test_weight_loss():
    """
    Test that weight_loss reduces an instance´s weight.
    """
    a = Herbivore()
    a.weight = 20
    a.weight_loss()
    assert a.weight < 20


def test_error_when_negative_weight_given():
    with pytest.raises(ValueError):
        Animal(0, -1)


def test_age_raise_valueerror():
    with pytest.raises(ValueError):
        Animal(1.1, 1)


def test_get_fitness():
    """
    Test that get_fitness returns a fitness of type float.
    """

    fitness = Herbivore().get_fitness()
    assert type(fitness) == float


def test_weight_normal_distributed():
    random.seed(123456)
    alpha = 0.05
    herb_weights = [Herbivore().weight for _ in range(1000)]
    carn_weights = [Carnivore().weight for _ in range(1000)]
    result_herb = normaltest(herb_weights)
    result_carn = normaltest(carn_weights)
    assert alpha < result_herb[1]
    assert alpha < result_carn[1]







