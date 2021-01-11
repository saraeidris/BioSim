from biosim.animals import Animal, Herbivore
import pytest


@pytest.fixture
def set_params(request):
    Animal.set_params(request.param)
    yield
    Animal.set_params(Animal.params)


def test_ani_age():
    """
    Test that a new animal has age 0.
    """
    a = Animal(0, 5)
    assert a.age == 0

def test_animal_should_eat_when_fodder_is_available():
    animal = Herbivore({'F': 10, 'beta': 0.9}, weight=5)
    consumed_fodder = animal.consumed_fodder(100)

    assert consumed_fodder == 10

def test_animal_should_eat_all_remaining_food_when_fodder_is_less_than_F():
    animal = Herbivore({'F': 10, 'beta': 0.9}, weight=5)
    consumed_fodder = animal.consumed_fodder(7)

    assert consumed_fodder == 7



#
#
# @pytest.mark.parametrize('set_params', [{'omega': 100.0}], indirect=True)
# def test_dies(set_params):
#     a = Animals()
#     for _ in range(100):
#         assert a.dies()
