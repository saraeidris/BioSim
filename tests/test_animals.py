from biosim.animals import Animal, Herbivore
import pytest


@pytest.fixture
def set_params(request):
    Animal.set_params(request.param)
    yield
    Animal.set_params(Animal.params)


def test_animal_age():
    """
    Test that a new animal has age 0.
    """
    a = Animal(0, 0)
    assert a.age == 0


def test_animal_aging():
    """
    This test is *determinstic*: for each call to aging(),
    the age must increase by one year.
    """

    a = Animal(0, 0)
    for n in range(10):
        a.aging()
        assert a.age == n + 1


def test_animal_certain_death():
    """

    """

    a = Animal(0, 0)
    assert a.dies()
    #h = Herbivore(0, -6)
    #assert h.dies()


def test_animal_should_eat_when_fodder_is_available():
    animal = Herbivore(0, weight=5)
    consumed_fodder = animal.consumed_fodder(100)

    assert consumed_fodder == 10


def test_herbivore_eat_all_remaining_fodder():
    animal = Herbivore(0, weight=5)
    consumed_fodder = animal.consumed_fodder(7)

    assert consumed_fodder == 7


def test_lose_weight():
    a = Animal(0, 20)
    a.weight = 20
    a.weight_loss()
    assert a.weight == 20

