from biosim.landscape import Water, Lowland, Highland, Desert
from biosim.animals import Carnivore, Herbivore

import pytest, random
from scipy.stats import chisquare

random.seed(123456)

"""Various tests made for the Landscape class."""

__author__ = "Sara Idris & Thorbjørn L Onsaker, NMBU"
__email__ = "said@nmbu.no & thon@nmbu.no"


class TestLandscape:
    """Test class for the landscape class."""

    @pytest.fixture
    def water(self):
        """Creates an instance of the water class."""
        return Water()

    @pytest.fixture
    def highland(self):
        """Creates an instance of the highland class."""
        return Highland()

    @pytest.fixture
    def lowland(self):
        """Creates an instance of the lowland class."""
        return Lowland()

    @pytest.fixture
    def desert(self):
        """Creates an instance of the desert class."""
        return Desert()

    @pytest.fixture
    def create_herbs(self):
        """Creates a list of 100 herbivores for use in multiple test."""
        return [Herbivore(5, 50) for _ in range(100)]

    @pytest.fixture
    def create_carns(self):
        """Creates a list of 100 carnivores for use in multiple test."""
        return [Carnivore(5, 50) for _ in range(100)]

    def test_water_not_habitable(self, water):
        """Test that water is not habitable for animals."""

        assert not water.is_habitable()

    def test_ages(self, create_herbs, create_carns, lowland):
        """Test that ages() increase all ages with 1 every time it is called."""

        herbs = lowland.list_herbs = create_herbs
        carns = lowland.list_carns = create_carns
        lowland.ages()
        lowland.ages()
        lowland.ages()
        for herb in herbs:
            assert herb.age == 8
        for carn in carns:
            assert carn.age == 8

    def test_give_birth(self, create_herbs, create_carns, lowland, mocker):
        """
        test that all animals give birth when chance of giving birth is
        set to 100% with weight = 50 and use of mocker. This is done
        by checking that the population after birth is doubled.
        """

        mocker.patch('random.random', return_value=0)
        cell = lowland
        cell.list_herbs = create_herbs
        cell.list_carns = create_carns
        before = len(cell.list_herbs + cell.list_carns)

        cell.give_birth()
        after = len(cell.list_herbs + cell.list_carns)
        print(after)
        assert (2 * before) == after

    def test_set_fodder(self, lowland, highland):
        """Test that new fodder values can be set for landscape types."""

        lowland.set_fodder(700)
        highland.set_fodder(100)
        assert lowland.fodder == 700
        assert highland.fodder == 100

    def test_no_fodder_water_desert(self, water, desert):
        """Test that fodder values in water and desert cells are 0."""

        w = water
        d = desert
        assert w.fodder == 0
        assert d.fodder == 0

    def test_fodder_values_highland_lowland(self, lowland, highland):
        """Test fodder values in Lowland and Highland.

        Test that fodder values in highland and lowland are 0, and that
        fodder values get updated to 300 and 800 when update_fodder is called.
        """

        l = lowland
        h = highland
        assert l.fodder == 0
        assert h.fodder == 0
        l.update_fodder()
        h.update_fodder()
        assert l.fodder == 800
        assert h.fodder == 300

    def test_set_landscape_params(self, lowland, highland):
        """Test that new landscape parameters can be set."""

        l = lowland
        h = highland
        l.set_params({'f_max': 1000})
        h.set_params({'f_max': 500})
        l.update_fodder()
        h.update_fodder()
        assert l.fodder == 1000
        assert h.fodder == 500

    def test_set_landscape_params_errors(self, lowland, highland):
        """Test that wrong inputs to set_landscape_params raises errors."""

        l = lowland
        h = highland
        with pytest.raises(ValueError):
            l.set_params({'f_min': 1000})
        with pytest.raises(ValueError):
            h.set_params({'f_max': -5})
        with pytest.raises(ValueError):
            h.set_params({'f_max': 'five'})

    def test_no_migration_to_water(self, water, lowland, create_herbs, create_carns):
        """Test that no animals migrate to cells of class water."""

        lowland.list_herbs = create_herbs
        lowland.list_carns = create_carns
        list_herbs2 = lowland.list_herbs.copy()
        list_carns2 = lowland.list_carns.copy()
        cells_around = (water, water, water, water)
        lowland.migrate_all(cells_around)
        assert lowland.list_herbs == list_herbs2
        assert lowland.list_carns == list_carns2

    def test_migration_with_chi_squared(self, lowland, highland, desert, mocker):
        """Test that migration is randomly to the 4 neighbour cells.

        Statistical test to check that animals choose to migrate to each
        neighbour cell with the same probability (25% each if cells are not water).
        """

        mocker.patch('random.random', return_value=0)
        c1 = lowland
        c2 = highland
        c3 = highland
        c4 = lowland
        desert.list_herbs = [Herbivore() for _ in range(1000)]
        cells_around = (c1, c2, c3, c4)
        desert.migrate_all(cells_around)

        move_herbs = desert.move_herbs
        expected = [250, 250, 250, 250]
        observed = [len(move_herbs[0]), len(move_herbs[1]),
                    len(move_herbs[2]), len(move_herbs[3])]
        _, p_value = chisquare(expected, observed)

        assert p_value > 0.01











