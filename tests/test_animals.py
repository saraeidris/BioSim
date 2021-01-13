from biosim.animals import Animal, Herbivore, Carnivore
import pytest


@pytest.fixture
def set_params(request):
    Herbivore.set_params(request.param)
    yield
    Herbivore.set_params(Herbivore.params)


@pytest.mark.parametrize('set_params', [{'omega': 10000}], indirect=True)
def test_bact_certain_death(set_params):
    """
    This test is *deterministic*: We set death probability to 1,
    thus the bacterium must always die. We call dies() multiple
    times to test this.

    Paramterization with a single-element list of parameter values will run
    this test once. Because we set `indirect=True`, Pytest will first invoke
    the set_params fixture defined above, passing the dictionary
    `{'p_death': 1.0}` as `request.param` to the fixture. The fixture then
    calls `Bacteria.set_params()` and also ensures clean-up after the test.
    """

    h = Herbivore()
    for _ in range(100):
        assert h.dies()


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
    Test that animal die if weight is 0.
    """

    a = Carnivore()
    a.weight = 0
    assert a.dies()


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


def test_age_set_to_zero():
    with pytest.raises(ValueError):
        Animal(1.1, 1)


def test_get_fitness():
    """
    Test that get_fitness returns a fitness of type float.
    """

    fitness = Herbivore().get_fitness()
    assert type(fitness) == float
