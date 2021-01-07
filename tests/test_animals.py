
from biosim.animals import Animals


def test_ani_age():
    """
    Test that a new animal has age 0.
    """
    a = Animals(0)
    assert a.age == 0


def test_ani_aging():
    """
    This test is *determinstic*: for each call to ages(),
    the age must increase by one year.
    """
    a = Animals(0)
    for n in range(5):
        a.ages()

        assert a.get_age() == n + 1

