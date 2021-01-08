from biosim.animals import Animals
import pytest


def test_ani_age():
    """
    Test that a new animal has age 0.
    """
    a = Animals()
    assert a.age == 0


def test_ani_aging():
    """
    This test is *determinstic*: for each call to ages(),
    the age must increase by one year.
    """
    a = Animals()
    for n in range(5):
        a.ages()

        assert a.get_age() == n + 1


# @pytest.fixture
# def set_params(request):
#     Animals.set_params(request.param)
#     yield
#     Animals.set_params(Animals.params)
#
#
# @pytest.mark.parametrize('set_params', [{'omega': 100.0}], indirect=True)
# def test_dies(set_params):
#     a = Animals()
#     for _ in range(100):
#         assert a.dies()
