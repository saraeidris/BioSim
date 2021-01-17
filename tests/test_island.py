import pytest
import textwrap
from biosim.RossumIsland import RossumIsland


class TestRossumIsland:
    """
    Tests for the RossumIsland class.
    """

    @pytest.fixture
    def example_island(self):
        geogr = """\
                   WWWWWWWWWWW
                   WLLLLLLLLLW
                   WLHHHHHHHLW
                   WLHDDDDDHLW
                   WLHDLWLDHLW
                   WLHDWWWDHLW
                   WLHDLWLDHLW
                   WLHDDDDDHLW
                   WLHHHHHHHLW
                   WLLLLLLLLLW
                   WWWWWWWWWWW"""

        island_map = textwrap.dedent(geogr)
        return RossumIsland(island_map)

    def test_wrong_location_error(self):
        with pytest.raises(ValueError):
            RossumIsland.