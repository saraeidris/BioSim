import matplotlib.pyplot as plt
import numpy as np
import subprocess
import matplotlib.patches as mpatches
from matplotlib.widgets import Button


# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
# _CONVERT_BINARY/magick is only needed if you want to create animated GIFs.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = 'data'
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'  # alternatives: mp4, gif


class Graphics:
    """Provides graphics support for RandVis."""

    def __init__(self, hist_specs, cmax, ymax_animals, img_name=None,
                 img_fmt='png'):
        """
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
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

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._herb_heat_ax = None
        self._carn_heat_ax = None
        self._herbivore_img_axis = None
        self._carn_img_axis = None
        self._animal_age_img_axis = None
        self._animal_weight_img_axis = None
        self._animal_fitness_img_axis = None
        self._animal_weight_ax = None
        self._animal_age_ax = None
        self._animal_fitness_ax = None
        self._animal_count = None
        self._map_ax = None
        self._map_img_axis = None
        self._legends_img_axis = None
        self._legends = None
        self._count_years_ax = None
        self._count_years_img_axis = None
        self._herb_line = None
        self._carn_line = None
        self._pause_ax = None
        self._pause_button = None

    def update(self, year, get_stats, two_d_darray_for_pop, island_map, final_step):
        """Updates graphics with current data."""

        self._update_herb_heatmap(two_d_darray_for_pop)
        self._update_carn_heatmap(two_d_darray_for_pop)
        self._update_animal_age(get_stats)
        self._update_animal_weight(get_stats)
        self._update_animal_fitness(get_stats)
        self._update_animal_count(two_d_darray_for_pop, year, final_step)
        self.update_map(island_map)
        self.update_count_years(year)
        # self._pause_button_click()
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-20)
          # pause required to pass control to GUI
        # while self._paused:
        #     plt.pause(0.05)
        # plt.pause(1e-8)
        # self._save_graphics(year)

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
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
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

    def setup(self, final_step, img_years):
        """Prepare graphics."""

        self._img_years = img_years

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._herb_heat_ax is None:
            self._herb_heat_ax = self._fig.add_axes([0.06, 0.25, 0.35, 0.35])  # llx, lly, w, h
            self._herbivore_img_axis = None
            self._herb_heat_ax.set_xticks([1, 6, 11, 16, 21])
            self._herb_heat_ax.set_title('Herbivore distribution')

        if self._carn_heat_ax is None:
            self._carn_heat_ax = self._fig.add_axes([0.6, 0.25, 0.35, 0.35])
            self._carn_img_axis = None
            self._carn_heat_ax.set_xticks([1, 6, 11, 16, 21])
            self._carn_heat_ax.set_title('Carnivore distribution')

        if self._animal_age_ax is None:
            xmax = self._hist_specs['age']['max']
            self._animal_age_ax = self._fig.add_axes([0.06, 0.07, 0.25, 0.12])
            self._animal_age_img_axis = None
            self._animal_age_ax.set_xticks([0, round(xmax / 4), round(xmax / 2),
                                            round(xmax * 3 / 4), round(xmax / 1)])

        if self._animal_weight_ax is None:
            xmax = self._hist_specs['weight']['max']
            self._animal_weight_ax = self._fig.add_axes([0.37, 0.07, 0.25, 0.12])
            self._animal_weight_img_axis = None
            self._animal_weight_ax.set_xticks([0, round(xmax / 4), round(xmax / 2),
                                               round(xmax * 3 / 4), round(xmax / 1)])
            self._animal_weight_ax.set_title('Weight')

        if self._animal_fitness_ax is None:
            xmax = self._hist_specs['fitness']['max']
            self._animal_fitness_ax = self._fig.add_axes([0.68, 0.07, 0.25, 0.12])
            self._animal_fitness_img_axis = None
            self._animal_fitness_ax.set_xticks([0, round(xmax / 4, 2), round(xmax / 2, 2),
                                                round(xmax * 3 / 4, 2), round(xmax / 1)])

        if self._animal_count is None:
            ymax = self._ymax_animals
            self._animal_count = self._fig.add_axes([0.63, 0.63, 0.25, 0.3])
            if ymax:
                self._animal_count.set_ylim(0, ymax)
            else:
                self._animal_count.set_ylim(0, 15500)

        self._animal_count.set_xlim(0, final_step + 1)

        if self._herb_line is None:
            herbivore_plot = self._animal_count.plot(np.arange(0, final_step + 1),
                                                     np.full(final_step + 1, np.nan), 'b', lw=2)
            self._herb_line = herbivore_plot[0]

        else:
            x_data, y_data = self._herb_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herb_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        if self._carn_line is None:
            carnivore_plot = self._animal_count.plot(np.arange(0, final_step + 1),
                                                     np.full(final_step + 1, np.nan), 'r', lw=2)
            self._carn_line = carnivore_plot[0]

        else:
            x_data, y_data = self._carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        if self._map_ax is None:
            self._map_ax = self._fig.add_axes([0.06, 0.7, 0.2, 0.2])
            self._map_img_axis = None
            self._map_ax.set_xticks([1, 6, 11, 16, 21])
            self._map_ax.set_title('Island')
            self._map_ax.axis('off')

        if self._count_years_ax is None:
            self._count_years_ax = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])
            self._count_years_img_axis = None
            self._count_years_ax.set_title('Animal count')
            self._count_years_ax.axis('off')  # turn off coordinate system
        #
        # if self._pause_ax is None:
        #     self._paused = False
        #     self._pause_ax = self._fig.add_axes([0.6, 0.10, 0.3, 0.15])
        #     self._pause_button = Button(self._pause_ax, "Pause/Run", hovercolor="0.5")
        #     self._pause_button.on_clicked(self._pause_button_click)

    # def _pause_button_click(self, event):
    #     if self._paused:
    #         self._paused = False
    #     else:
    #         self._paused = True

    def _update_herb_heatmap(self, two_d_array_pop):
        """Update the herbivore heatmap every year"""
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
        """Update the carnivore heatmap every year"""
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
        """Update the age histogram every year"""
        herbivore_stats = get_stats[0]
        carnivore_stats = get_stats[1]
        hist_max = self._hist_specs['age']['max']
        num = int(hist_max / self._hist_specs['age']['delta'])

        if self._animal_age_ax is not None:
            self._animal_age_ax.clear()
            self._animal_age_ax.set_title('Age')

        self._animal_age_img_axis = self._animal_age_ax.hist(herbivore_stats, bins=num,
                                                             range=(0, hist_max),
                                                             histtype="step", color="b", lw=2)
        self._animal_age_img_axis = self._animal_age_ax.hist(carnivore_stats, bins=num,
                                                             range=(0, hist_max),
                                                             histtype="step", color="r", lw=2)

    def _update_animal_weight(self, get_stats):
        """Update the weight histogram every year"""
        herbivore_stats = get_stats[2]
        carnivore_stats = get_stats[3]
        hist_max = self._hist_specs['weight']['max']
        num = int(hist_max / self._hist_specs['weight']['delta'])

        if self._animal_weight_ax is not None:
            self._animal_weight_ax.cla()
            self._animal_weight_ax.set_title('weight')

        self._animal_weight_img_axis = self._animal_weight_ax.hist(herbivore_stats, bins=num,
                                                                   range=(0, hist_max),
                                                                   histtype="step", color="b", lw=2)
        self._animal_weight_img_axis = self._animal_weight_ax.hist(carnivore_stats, bins=num,
                                                                   range=(0, hist_max),
                                                                   histtype="step", color="r", lw=2)

    def _update_animal_fitness(self, get_stats):
        """Update the fitness histogram every year"""
        herbivore_stats = get_stats[4]
        carnivore_stats = get_stats[5]
        hist_max = self._hist_specs['fitness']['max']
        num = int(hist_max / self._hist_specs['fitness']['delta'])

        if self._animal_fitness_ax is not None:
            self._animal_fitness_ax.cla()
            self._animal_fitness_ax.set_title('Fitness')

        self._animal_fitness_img_axis = self._animal_fitness_ax.hist(herbivore_stats, bins=num,
                                                                     range=(0, hist_max),
                                                                     histtype="step", color="b", lw=2)
        self._animal_fitness_img_axis = self._animal_fitness_ax.hist(carnivore_stats, bins=num,
                                                                     range=(0, hist_max),
                                                                     histtype="step", color="r", lw=2)

    def _update_animal_count(self, two_d_array_for_pop, year, final_step):
        """Update the animal count plot every year"""
        herbivore_stats = two_d_array_for_pop[2]
        carnivore_stats = two_d_array_for_pop[3]
        herb_data = self._herb_line.get_ydata()
        carn_data = self._carn_line.get_ydata()
        herb_data[year] = herbivore_stats
        carn_data[year] = carnivore_stats
        self._herb_line.set_ydata(herb_data)
        self._carn_line.set_ydata(carn_data)

    def update_map(self, island_map):

        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in island_map.splitlines()]
        self._map_ax.imshow(map_rgb)

        self._map_ax.set_xticks(range(len(map_rgb[0])))
        self._map_ax.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        self._map_ax.set_yticks(range(len(map_rgb)))
        self._map_ax.set_yticklabels(range(1, 1 + len(map_rgb)))

        patches = []
        for name in ("Water", "Lowland", "Highland", "Desert"):
            patches.append(
                mpatches.Patch(edgecolor="none", label=name, facecolor=rgb_value[name[0]])
            )
        self._map_ax.legend(
            handles=patches, loc="best", bbox_to_anchor=(0.8, 0.8, 0.9, 0.3), prop={"size":7}
        )

    def update_count_years(self, year):
        """Counts every year wanted"""
        self._count_years_ax.cla()
        plt.axis('off')
        template = 'Years: {:5d}'
        txt = self._count_years_ax.text(0.5, 0.5, template.format(0),
                                     horizontalalignment='center',
                                     verticalalignment='center',
                                     transform=self._count_years_ax.transAxes)  # relative coordinates

        txt.set_text(template.format(year))

    def _save_graphics(self, year):
        """Saves graphics to file if file name given."""

        if (self._img_base is None) or (year % self._img_years != 0):
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
