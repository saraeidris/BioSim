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

def test_bact_aging():
    """
    This test is *determinstic*: for each call to ages(),
    the age must increase by one year.
    """

    a = Animal(0,0)
    for n in range(10):
        a.aging()
        assert a.age == n + 1

def test_bact_certain_death(mocker):
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

    a = Animal(0,0)
    assert a.dies()
    h = Herbivore(0,20)
    h.set_fitness(0)
    assert h.dies()
    # a = Animal(0, 2)
    # mocker.patch('random.random', 1)
    # for _ in range(100):
    #     assert a.dies()




def test_animal_should_eat_when_fodder_is_available():
    animal = Herbivore({'F': 10, 'beta': 0.9}, weight=5)
    consumed_fodder = animal.consumed_fodder(100)

    assert consumed_fodder == 10


def test_herbivore_should_eat_all_remaining_food_when_fodder_is_less_than_F():
    animal = Herbivore({'F': 10, 'beta': 0.9}, weight=5)
    consumed_fodder = animal.consumed_fodder(7)

    assert consumed_fodder == 7

