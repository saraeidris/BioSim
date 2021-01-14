import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os
import seaborn as sns

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
        self._carn_heat = None
        self._mean_line = None

    def update(self, step, sys_map, two_d_darray_for_pop, list_with_years,
               list_with_population_for_all_years):
        """Updates graphics with current data."""

        self._update_system_map(sys_map, two_d_darray_for_pop, list_with_years,
                                list_with_population_for_all_years)
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
            self._herb_heat = self._fig.add_subplot(1, 2, 1)
            self._herbivore_img_axis = None

        # Add right subplot for line graph of mean.
        if self._carn_heat is None:
            self._carn_heat = self._fig.add_subplot(1, 2, 2)
            self._carn_img_axis = None

        # needs updating on subsequent calls to simulate()
        #self._carn_heat.set_xlim(0, final_step + 1)

        if self._mean_line is None:
            mean_plot = self._carn_heat.plot(np.arange(0, final_step + 1),
                                             np.full(final_step + 1, np.nan))
            self._mean_line = mean_plot[0]
        else:
            x_data, y_data = self._mean_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._mean_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

    def _update_system_map(self, tuple_stats, two_d_array_pop, list_with_years,
                           list_with_population_for_all_years):
        """Update the 2D-view of the system."""
        herbivore_stats = two_d_array_pop[0]
        carnivore_stats = two_d_array_pop[1]

        if self._herbivore_img_axis is not None:
            self._herbivore_img_axis.set_data(herbivore_stats)
        else:
            self._herbivore_img_axis = self._herb_heat.imshow(herbivore_stats,
                                                              interpolation='nearest',
                                                              vmin=0, vmax=200)

            plt.colorbar(self._herbivore_img_axis, ax=self._herb_heat,
                         orientation='horizontal')

        if self._carn_img_axis is not None:
            self._carn_img_axis.set_data(carnivore_stats)
        else:
            self._carn_img_axis = self._carn_heat.imshow(carnivore_stats,
                                                         interpolation='nearest',
                                                         vmin=0, vmax=50)
            plt.colorbar(self._carn_img_axis, ax=self._carn_heat,
                         orientation='horizontal')

        # self._mean_ax = None
        # plt.hist(tuple_stats[4])
        # plt.title('Fitness')
        # self._mean_line = None
        # plt.hist(tuple_stats[2])
        # plt.title('weight')
        # #self._fig.add_subplot(2, 3, 5)
        # plt.hist(tuple_stats[0])
        # plt.title('age')
        # #self._fig.add_subplot(2, 3, 6)
        # plt.plot(list_with_years, list_with_population_for_all_years)
        # plt.title('Animal count')

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
