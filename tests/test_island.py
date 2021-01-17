import pytest
import textwrap
from biosim.RossumIsland import RossumIsland


class TestRossumIsland:
    """
    Tests for the RossumIsland class.
    """

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

    def test_no_map_given(self):
        """Test that no map given results in ValueError"""
        with pytest.raises(ValueError):
            RossumIsland('')

    def test_annual_cycle(self, example_island, mocker):
        """
        Test that annual cycle works by checking that all animals'
        age have increased by one after one cycle, and that their weights
        are between 20 and 30 because they all have eaten 10 and lost less
        than 10.
        """
        mocker.patch('random.randint', return_value=0)
        mocker.patch('random.random', return_value=1)
        ini_herbs = [{'loc': (6, 6),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 20}
                              for _ in range(40)]}]
        example_island.insert_population(ini_herbs)
        example_island.annual_cycle()
        for row in example_island.island:
            for cell in row:
                for herb in cell.list_herbs:
                    assert herb.age == 6
                    assert 30 > herb.weight > 20


