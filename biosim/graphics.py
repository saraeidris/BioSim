import matplotlib.pyplot as plt
import numpy as np
import subprocess
import matplotlib.patches as mpatches
from matplotlib.widgets import Button

__author__ = "Sara Idris & Thorbjørn L Onsaker, NMBU"
__email__ = "said@nmbu.no & thon@nmbu.no"


_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

_DEFAULT_GRAPHICS_DIR = 'data'
_DEFAULT_GRAPHICS_NAME = 'bs'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'


class Graphics:
    """Class providing graphics support for BioSim class."""

    def __init__(self, hist_specs, cmax, ymax_animals, img_name=None, img_fmt='png'):
        """
        :param hist_specs: properties for histograms for both species
        :type hist_specs: dict
        :param cmax: color-code limits for animal density
        :type cmax: dict
        :param ymax_animals: number specifying y-axis for graph showing animal count
        :type ymax_animals: int
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix, default 'png'
        :type img_fmt: str
        """

        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        self._img_base = img_name

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_fmt = img_fmt
        self._hist_specs = hist_specs
        self._cmax = cmax
        self._ymax_animals = ymax_animals
        self._img_ctr = 0
        self._img_years = 1

        self._fig = None
        self._herb_heat_ax = None
        self._carn_heat_ax = None
        self._herbivore_img_axis = None
        self._carn_img_axis = None
        self._animal_weight_ax = None
        self._animal_age_ax = None
        self._animal_fitness_ax = None
        self._animal_count_ax = None
        self._map_ax = None
        self._map_img_axis = None
        self._count_years_ax = None
        self._count_years_img_axis = None
        self._herb_line = None
        self._carn_line = None
        self._pause_ax = None
        self._pause_button = None
        self.herb_w_hist = None
        self.carn_w_hist = None
        self.herb_a_hist = None
        self.carn_a_hist = None
        self.herb_f_hist = None
        self.carn_f_hist = None
        self._paused = False

    def update(self, year, get_stats, two_d_array_for_pop):
        """Updates graphics with current data."""

        self._update_herb_heatmap(two_d_array_for_pop)
        self._update_carn_heatmap(two_d_array_for_pop)
        self._update_animal_age(get_stats)
        self._update_animal_weight(get_stats)
        self._update_animal_fitness(get_stats)
        self._update_animal_count(two_d_array_for_pop, year)
        self.update_count_years(year)
        self._fig.canvas.flush_events()
        self._save_graphics(year)
        plt.pause(1e-20)
        while self._paused:
            plt.pause(0.05)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF
        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def setup(self, final_year, img_years, island_map):
        """Prepare graphics."""

        self._img_years = img_years

        if self._fig is None:
            self._fig = plt.figure(figsize=(10, 7))

        if self._herb_heat_ax is None:
            self.setup_herb_heatmap()

        if self._carn_heat_ax is None:
            self.setup_carn_heatmap()

        if self._animal_age_ax is None:
            self.setup_hist_age()

        if self._animal_weight_ax is None:
            self.setup_hist_weight()

        if self._animal_fitness_ax is None:
            self.setup_hist_fitness()

        self.setup_animal_count(final_year)

        if self._map_ax is None:
            self.setup_map(island_map)

        if self._count_years_ax is None:
            self.setup_count_years()

        if self._pause_ax is None:
            self.setup_pause_button()

    def setup_pause_button(self):
        """Sets up the axes for the pause button.

        Returns True/False for every mouseclick
        """

        self._paused = False
        self._pause_ax = self._fig.add_axes([0.45, 0.7, 0.1, 0.1])
        self._pause_button = Button(self._pause_ax, "Pause", color="red", hovercolor="pink")
        self._pause_button.on_clicked(self._pause_button_click)

    def setup_count_years(self):
        """Sets up the figure axes for count years, and turns off the coordinate system."""

        self._count_years_ax = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])
        self._count_years_img_axis = None
        self._count_years_ax.axis('off')

    def setup_map(self, island_map):
        """Sets up the figure axes for island_map and plots the different colors.

        :param island_map: linestring of characters
        """

        self._map_ax = self._fig.add_axes([0.06, 0.7, 0.27, 0.25])
        self._map_img_axis = None
        self._map_ax.set_title('Island')
        self._map_ax.axis('off')
        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow
        map_rgb = [[rgb_value[column] for column in row]
                   for row in island_map.splitlines()]
        self._map_ax.imshow(map_rgb)
        patches = []
        for name in ("Water", "Lowland", "Highland", "Desert"):
            patches.append(
                mpatches.Patch(edgecolor="none", label=name, facecolor=rgb_value[name[0]])
            )
        self._map_ax.legend(
            handles=patches, bbox_to_anchor=(0.8, 0.8, 0.57, 0.24), prop={"size": 7})
        self._map_ax.set_xticks(range(len(map_rgb[0])))
        self._map_ax.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        self._map_ax.set_yticks(range(len(map_rgb)))
        self._map_ax.set_yticklabels(range(1, 1 + len(map_rgb)))

    def setup_animal_count(self, final_year):
        """Sets up the figure axes for animal count.

        herb_line/carn_line is a line with just NaN who gets
        updated with numbers for every simulation.
        :param final_year: last year of wanted simulation
        """

        if self._animal_count_ax is None:
            ymax = self._ymax_animals
            self._animal_count_ax = self._fig.add_axes([0.63, 0.66, 0.25, 0.3])
            self._animal_count_ax.set_title('Animal count')
            if ymax:
                self._animal_count_ax.set_ylim(0, ymax)

        self._animal_count_ax.set_xlim(0, final_year + 1)

        if self._herb_line is None:
            herbivore_plot = self._animal_count_ax.plot(np.arange(0, final_year + 1),
                                                        np.full(final_year + 1, np.nan),
                                                        'b.', lw=2)
            self._herb_line = herbivore_plot[0]

        else:
            x_data, y_data = self._herb_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herb_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        if self._carn_line is None:
            carnivore_plot = self._animal_count_ax.plot(np.arange(0, final_year + 1),
                                                        np.full(final_year + 1, np.nan),
                                                        'r.', lw=2)
            self._carn_line = carnivore_plot[0]

        else:
            x_data, y_data = self._carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

    def setup_hist_fitness(self):
        """Sets up axes for fitness histogram, and adds step for bins."""

        xmax = self._hist_specs['fitness']['max']
        self._animal_fitness_ax = self._fig.add_axes([0.68, 0.07, 0.25, 0.12])
        self._animal_fitness_ax.margins(x=0)
        self._animal_fitness_ax.set_title('Fitness')
        bin_lims = np.arange(0, self._hist_specs['fitness']['max'],
                             self._hist_specs['fitness']['delta'])
        self.herb_f_hist, self.carn_f_hist = self._animal_fitness_ax.step(bin_lims,
                                                                          np.zeros_like(
                                                                              bin_lims), 'b-',

                                                                          bin_lims,
                                                                          np.zeros_like(
                                                                              bin_lims), 'r-',
                                                                          where='mid')
        self._animal_fitness_ax.set_xticks([0, round(xmax / 4, 2), round(xmax / 2, 2),
                                            round(xmax * 3 / 4, 2), xmax])

    def setup_hist_weight(self):
        """Sets up axes for weight histogram, and adds step for bins."""

        xmax = self._hist_specs['weight']['max']
        self._animal_weight_ax = self._fig.add_axes([0.37, 0.07, 0.25, 0.12])
        self._animal_weight_ax.margins(x=0)
        self._animal_weight_ax.set_title('Weight')
        bin_lims = np.arange(0, xmax, self._hist_specs['weight']['delta'])
        self.herb_w_hist, self.carn_w_hist = self._animal_weight_ax.step(bin_lims,
                                                                         np.zeros_like(
                                                                             bin_lims), 'b-',

                                                                         bin_lims,
                                                                         np.zeros_like(
                                                                             bin_lims), 'r-',
                                                                         where='mid')

        self._animal_weight_ax.set_xticks([0, round(xmax / 4, 2), round(xmax / 2, 2),
                                           round(xmax * 3 / 4, 2), xmax])

    def setup_hist_age(self):
        """Sets up axes for age histogram, and adds step for bins."""

        xmax = self._hist_specs['weight']['max']
        self._animal_age_ax = self._fig.add_axes([0.06, 0.07, 0.25, 0.12])
        self._animal_age_ax.margins(x=0)
        self._animal_age_ax.set_title('Age')
        bin_lims = np.arange(0.0, self._hist_specs['weight']['max'],
                             self._hist_specs['weight']['delta'])
        self.herb_a_hist, self.carn_a_hist = self._animal_age_ax.step(bin_lims,
                                                                      np.zeros_like(
                                                                          bin_lims), 'b-',

                                                                      bin_lims,
                                                                      np.zeros_like(
                                                                          bin_lims), 'r-')

        self._animal_age_ax.set_xticks([0, round(xmax / 4, 2), round(xmax / 2, 2),
                                        round(xmax * 3 / 4, 2), xmax])

    def setup_carn_heatmap(self):
        """Sets up axes for carnivore heatmap"""

        self._carn_heat_ax = self._fig.add_axes([0.6, 0.25, 0.35, 0.35])
        self._carn_img_axis = None
        self._carn_heat_ax.set_title('Carnivore distribution')

    def setup_herb_heatmap(self):
        """Sets up axes for herbivore heatmap"""

        self._herb_heat_ax = self._fig.add_axes([0.06, 0.25, 0.35, 0.35])
        self._herbivore_img_axis = None
        self._herb_heat_ax.set_title('Herbivore distribution')

    def _pause_button_click(self, event):
        """Changing color and names for pause button"""

        if self._paused:
            self._paused = False
            self._pause_button.label.set_text("Pause")
            self._pause_button.color = 'red'
            self._pause_button.hovercolor = 'pink'
        else:
            self._paused = True
            self._pause_button.label.set_text("Run")
            self._pause_button.color = 'green'
            self._pause_button.hovercolor = 'lightgreen'

    def _update_herb_heatmap(self, two_d_array_pop):
        """Update the data for herbivore heatmap every year.

        :param two_d_array_pop: two dimensional array with herbivore density on island
        """

        herbivore_stats = two_d_array_pop[0]
        vmax = self._cmax['Herbivore']

        if self._herbivore_img_axis is not None:
            self._herbivore_img_axis.set_data(herbivore_stats)
        else:
            self._herbivore_img_axis = self._herb_heat_ax.imshow(herbivore_stats,
                                                                 interpolation='nearest',
                                                                 vmin=0, vmax=vmax)

            plt.colorbar(self._herbivore_img_axis, ax=self._herb_heat_ax,
                         orientation='vertical')

    def _update_carn_heatmap(self, two_d_array_pop):
        """Update the data for carnivore heatmap every year.

        :param two_d_array_pop: two dimensional array with carnivore density on island
        """

        carnivore_stats = two_d_array_pop[1]
        vmax = self._cmax['Carnivore']

        if self._carn_img_axis is not None:
            self._carn_img_axis.set_data(carnivore_stats)
        else:
            self._carn_img_axis = self._carn_heat_ax.imshow(carnivore_stats,
                                                            interpolation='nearest',
                                                            vmin=0, vmax=vmax)

            plt.colorbar(self._carn_img_axis, ax=self._carn_heat_ax,
                         orientation='vertical')

    def _update_animal_age(self, get_stats):
        """Update the data for age histogram every year.

        :param get_stats: tuple with lists containing data for all animals on the island.
        """

        herbivore_stats = get_stats[0]
        carnivore_stats = get_stats[1]
        hist_max = self._hist_specs['age']['max']
        num = int(hist_max / self._hist_specs['age']['delta'])

        self.herb_a_hist.set_ydata(np.histogram(herbivore_stats, num, (0, hist_max))[0])
        self.carn_a_hist.set_ydata(np.histogram(carnivore_stats, num, (0, hist_max))[0])
        herb_y_max = max(np.histogram(herbivore_stats, num, (0, hist_max))[0])
        carn_y_max = max(np.histogram(carnivore_stats, num, (0, hist_max))[0])

        if herb_y_max >= carn_y_max:
            self._animal_age_ax.set_ylim(0, herb_y_max * 1.15)
        else:
            self._animal_age_ax.set_ylim(0, carn_y_max * 1.15)

    def _update_animal_weight(self, get_stats):
        """Update the data for weight histogram every year.

        :param get_stats: tuple with lists containing data for all animals on the island.
        """

        herbivore_stats = get_stats[2]
        carnivore_stats = get_stats[3]
        hist_max = self._hist_specs['weight']['max']
        num = int(hist_max / self._hist_specs['weight']['delta'])

        self.herb_w_hist.set_ydata(np.histogram(herbivore_stats, num, (0, hist_max))[0])
        self.carn_w_hist.set_ydata(np.histogram(carnivore_stats, num, (0, hist_max))[0])
        herb_y_max = max(np.histogram(herbivore_stats, num, (0, hist_max))[0])
        carn_y_max = max(np.histogram(carnivore_stats, num, (0, hist_max))[0])

        if herb_y_max >= carn_y_max:
            self._animal_weight_ax.set_ylim(0, herb_y_max * 1.15)
        else:
            self._animal_weight_ax.set_ylim(0, carn_y_max * 1.15)

    def _update_animal_fitness(self, get_stats):
        """Update the data for fitness histogram every year.

        :param get_stats: tuple with lists containing data for all animals on the island.
        """

        herbivore_fitness = get_stats[4]
        carnivore_fitness = get_stats[5]
        hist_max = self._hist_specs['fitness']['max']
        num = int(hist_max / self._hist_specs['fitness']['delta'])

        self.herb_f_hist.set_ydata(np.histogram(herbivore_fitness, num, (0, hist_max))[0])
        self.carn_f_hist.set_ydata(np.histogram(carnivore_fitness, num, (0, hist_max))[0])
        herb_y_max = max(np.histogram(herbivore_fitness, num, (0, hist_max))[0])
        carn_y_max = max(np.histogram(carnivore_fitness, num, (0, hist_max))[0])

        if herb_y_max >= carn_y_max:
            self._animal_fitness_ax.set_ylim(0, herb_y_max * 1.15)
        else:
            self._animal_fitness_ax.set_ylim(0, carn_y_max * 1.15)

    def _update_animal_count(self, two_d_array_for_pop, year):
        """Update the data for animal count plot every year.

        :param two_d_array_for_pop: Total number of animals per species on island
        :param year: current year being simulated
        """

        herbivore_stats = two_d_array_for_pop[2]
        carnivore_stats = two_d_array_for_pop[3]

        herb_data = self._herb_line.get_ydata()
        carn_data = self._carn_line.get_ydata()
        herb_data[year] = herbivore_stats
        carn_data[year] = carnivore_stats
        self._herb_line.set_ydata(herb_data)
        self._carn_line.set_ydata(carn_data)

        ymax = self._ymax_animals
        if not ymax:
            self._animal_count_ax.set_ylim(0, (max(herb_data) * 1.1 + 500))

        color = {'H': (0.0, 0.0, 1.0),
                 'C': (1.0, 0.0, 0.0)}

        patches = []
        for name in ("Herbivores", "Carnivores"):
            patches.append(
                mpatches.Patch(edgecolor="none", label=name, facecolor=color[name[0]])
            )
        self._animal_count_ax.legend(
            handles=patches, loc="upper left", prop={"size": 7}
        )

    def update_count_years(self, year):
        """Counts every simulated years.

        :param year: current year being simulated
        """

        self._count_years_ax.cla()
        self._count_years_ax.axis('off')
        template = 'Years: {:5d}'
        txt = self._count_years_ax.text(0.5, 0.5, template.format(0),
                                        horizontalalignment='center',
                                        verticalalignment='center',
                                        transform=self._count_years_ax.transAxes)

        txt.set_text(template.format(year))

    def _save_graphics(self, year):
        """Saves graphics to file if file name given.

        :param year: current year being simulated
        """

        if (self._img_base is None) or (year % self._img_years != 0):
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
