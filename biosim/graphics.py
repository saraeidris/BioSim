import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
# _CONVERT_BINARY/magick is only needed if you want to create animated GIFs.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_MOVIE_FORMAT = 'mp4'  # alternatives: mp4, gif


class Graphics:
    """Provides graphics support for RandVis."""

    def __init__(self,
                 img_base,
                 img_fmt='png'):
        """
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix, default 'png'
        :type img_fmt: str
        """

        self._img_base = img_base
        self._img_fmt = img_fmt

        self._img_ctr = 0
        self._img_step = 1

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._herb_heat = None
        self._herbivore_img_axis = None
        self._carn_img_axis = None
        self._animal_age_img_axis = None
        self._animal_weight_img_axis = None
        self._animal_fitness_img_axis = None
        self._animal_weight = None
        self._carn_weight = None
        self._carn_heat = None
        self._animal_age = None
        self._animal_fitness = None
        self._carn_age = None
        self._animal_count = None
        self._animal_count_img_axis = None

    def update(self, step, get_stats, two_d_darray_for_pop, number_of_animals):
        """Updates graphics with current data."""

        self._update_herb_heatmap(two_d_darray_for_pop)
        self._update_carn_heatmap(two_d_darray_for_pop)
        self._update_animal_age(get_stats)
        self._update_animal_weight(get_stats)
        self._update_animal_fitness(get_stats)
        self._update_animal_count(number_of_animals)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        self._save_graphics(step)

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

    def setup(self, final_step, img_step):
        """Prepare graphics."""

        self._img_step = img_step

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._herb_heat is None:
            self._herb_heat = self._fig.add_axes([0.06, 0.35, 0.3, 0.2])  # llx, lly, w, h
            self._herbivore_img_axis = None
            plt.title('Herbivore distribution')

        if self._carn_heat is None:
            self._carn_heat = self._fig.add_axes([0.6, 0.35, 0.3, 0.2])
            self._carn_img_axis = None
            plt.title('Carnivore distribution')

        if self._animal_age is None:
            self._animal_age = self._fig.add_axes([0.10, 0.1, 0.2, 0.15])
            self._animal_age_img_axis = None
            plt.title('animal age')

        if self._animal_weight is None:
            self._animal_weight = self._fig.add_axes([0.40, 0.1, 0.2, 0.15])
            self._animal_weight_img_axis = None
            plt.title('animal weight')

        if self._animal_fitness is None:
            self._animal_fitness = self._fig.add_axes([0.70, 0.1, 0.2, 0.15])
            self._animal_fitness_img_axis = None
            plt.title('animal fitness')

        if self._animal_count is None:
            self._animal_count = self._fig.add_axes([0.6, 0.7, 0.3, 0.2])
            self._animal_count_img_axis = None
            plt.title('animal count')

    def _update_herb_heatmap(self, two_d_array_pop):
        """Update the 2D-view of the system."""
        herbivore_stats = two_d_array_pop[0]

        if self._herbivore_img_axis is not None:
            self._herbivore_img_axis.set_data(herbivore_stats)
        else:
            self._herbivore_img_axis = self._herb_heat.imshow(herbivore_stats,
                                                              interpolation='nearest',
                                                              vmin=0, vmax=200)

            plt.colorbar(self._herbivore_img_axis, ax=self._herb_heat,
                         orientation='vertical')

    def _update_carn_heatmap(self, two_d_array_pop):
        carnivore_stats = two_d_array_pop[1]

        if self._carn_img_axis is not None:
            self._carn_img_axis.set_data(carnivore_stats)
        else:
            self._carn_img_axis = self._carn_heat.imshow(carnivore_stats,
                                                         interpolation='nearest',
                                                         vmin=0, vmax=50)

            plt.colorbar(self._carn_img_axis, ax=self._carn_heat,
                         orientation='vertical')

    def _update_animal_age(self, get_stats):
        herbivore_stats = get_stats[0]
        carnivore_stats = get_stats[1]

        self._herb_age_img_axis = self._animal_age.hist(herbivore_stats,
                                                        histtype="step", color="b")
        self._carn_age_img_axis = self._animal_age.hist(carnivore_stats,
                                                        histtype="step", color="r")

    def _update_animal_weight(self, get_stats):
        herbivore_stats = get_stats[2]
        carnivore_stats = get_stats[3]
        n =
        self._herb_age_img_axis = self._animal_weight.hist(herbivore_stats,
                                                        histtype="step", color="b", bins=int(n))
        self._carn_age_img_axis = self._animal_weight.hist(carnivore_stats,
                                                        histtype="step", color="r")

    def _update_animal_fitness(self, get_stats):
        herbivore_stats = get_stats[4]
        carnivore_stats = get_stats[5]
        self._herb_fitness_img_axis = self._animal_fitness.hist(herbivore_stats,
                                                                histtype="step", color="b")
        self._carn_fitness_img_axis = self._animal_fitness.hist(carnivore_stats,
                                                                histtype="step", color="r")

    def _update_animal_count(self, number_of_animals):
        herbivore_stats = number_of_animals[0]
        carnivore_stats = number_of_animals[1]
        self._herb_number_img_axis = self._animal_count.plot(herbivore_stats)
        self._carn_number_img_axis = self._animal_count.plot(carnivore_stats)

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
