from biosim.landscape import Water, Lowland, Highland, Desert
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
    def desert(self):
        return Desert()

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

    def test_set_fodder(self, lowland):
        lowland.set_fodder(700)
        assert lowland.fodder == 700

    def test_fodder_values_all_landscapes(self, desert, water, lowland, highland):
        w = water
        d = desert
        l = lowland
        h = highland
        assert w.fodder == 0
        assert d.fodder == 0
        assert l.fodder == 0
        assert h.fodder == 0
        l.update_fodder()
        h.update_fodder()
        assert l.fodder == 800
        assert h.fodder == 300

    def test_set_landscape_params(self, lowland, highland):
        l = lowland
        h = highland
        l.set_params({'f_max': 1000})
        h.set_params({'f_max': 500})
        l.update_fodder()
        h.update_fodder()
        assert l.fodder == 1000
        assert h.fodder == 500

    def test_set_landscape_params_errors(self, lowland, highland):
        l = lowland
        h = highland
        with pytest.raises(KeyError):
            l.set_params({'f_min': 1000})
        with pytest.raises(ValueError):
            h.set_params({'f_max': -5})
        with pytest.raises(ValueError):
            h.set_params({'f_max': 'five'})












