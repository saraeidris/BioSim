from biosim.landscape import Water, Lowland, Highland
from biosim.animals import Carnivore, Herbivore

import pytest


class TestLandscape:

    @pytest.fixture
    def water(self):
        return Water()

    @pytest.fixture
    def highland(self):
        return Highland()

    @pytest.fixture
    def lowland(self):
        return Lowland()

    @pytest.fixture
    def create_herbs(self):
        return [Herbivore() for _ in range(10)]

    @pytest.fixture
    def create_carns(self):
        return [Carnivore() for _ in range(10)]

    def test_aging(self, create_herbs, create_carns, lowland):
        herbs = lowland.list_herbs = create_herbs
        carns = lowland.list_carns = create_carns
        lowland.ages()
        lowland.ages()
        lowland.ages()
        for herb in herbs:
            assert herb.age == 3
        for carn in carns:
            assert carn.age == 3

    def test_update_fodder(self, highland, lowland):
        highland.update_fodder()
        lowland.update_fodder()
        assert highland.fodder == 300
        assert lowland.fodder == 800

    def test_set_fodder(self, lowland):
        lowland.set_fodder(700)
        assert lowland.fodder == 700








