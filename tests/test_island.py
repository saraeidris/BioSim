import pytest
import textwrap
from biosim.Island import RossumIsland

__author__ = "Sara Idris & Thorbjørn L Onsaker, NMBU"
__email__ = "said@nmbu.no & thon@nmbu.no"


class TestRossumIsland:
    """Test class for the RossumIsland class."""

    @pytest.fixture
    def example_island(self):
        """Create an island for use in later tests."""

        geogr = """\
                   WWWWWWWWWWW
                   WLLLLLLLLLW
                   WLHHHHHHHLW
                   WLHDDDDDHLW
                   WLHDWLWDHLW
                   WLHDLLLDHLW
                   WLHDWLWDHLW
                   WLHDDDDDHLW
                   WLHHHHHHHLW
                   WLLLLLLLLLW
                   WWWWWWWWWWW"""

        island_map = textwrap.dedent(geogr)
        return RossumIsland(island_map)

    def test_wrong_location_error(self, example_island):
        """Test that illegal coordinates raises ValueError."""

        ini_herbs = [{'loc': (100, 100),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(150)]}]
        ini_carns = [{'loc': (-3, 0),
                      'pop': [{'species': 'Carnivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(150)]}]

        with pytest.raises(ValueError):
            example_island.insert_population(ini_herbs)
        with pytest.raises(ValueError):
            example_island.insert_population(ini_carns)

    def test_insert_population_in_water(self, example_island):
        """Test that ValueError is raised if population is placed in water."""

        ini_herbs = [{'loc': (1, 1),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(150)]}]
        with pytest.raises(ValueError):
            example_island.insert_population(ini_herbs)

    def test_no_map_given(self):
        """Test that no map given results in ValueError"""

        with pytest.raises(ValueError):
            RossumIsland('')
