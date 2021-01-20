from biosim.simulation import BioSim
import pytest


class TestBioSim:
    """Test class for the BioSim class."""

    @pytest.fixture
    def example_biosim(self):
        return BioSim('W', [], 123456)

    def test_set_animal_parameters_errors(self, example_biosim):
        with pytest.raises(ValueError):
            example_biosim.set_animal_parameters('Failed', {'zeta': 3.2, 'xi': 1.8})
        with pytest.raises(ValueError):
            example_biosim.set_animal_parameters('Herbivore', {'zeta': - 1, 'xi': - 1})

    def test_set_landscape_paramters_errors(self, example_biosim):
        with pytest.raises(ValueError):
            example_biosim.set_landscape_parameters('W', {'f_max': 700})

    def test_simulate_errors(self, example_biosim):
        with pytest.raises(ValueError):
            example_biosim.simulate(100, 5, 6)
