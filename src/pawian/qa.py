"""Handle output of the QA step performed by Pawian.

Usually, a ``pawianHists.root`` file is produced if you run Pawian in QA mode.
This module contains handlers for such files.
"""

import logging
import re  # regex
from math import ceil, sqrt
from typing import (
    Optional,
    Tuple,
)

import matplotlib.pyplot as plt

import uproot

from uproot_methods.classes import TH1

from pawian.data import read_pawian_hists
from pawian.latex import convert


_WEIGHT_TAG = "weight"
_4VEC_BRANCH_TAG = "Fourvecs"


class PawianHists:
    """Data container for a ``pawianHists.root`` file.

    Data container for a ``pawianHists.root`` file that is created by the QA
    step in Pawian.
    """

    def __init__(self, filename):
        self.import_file(filename)

    def import_file(self, filename):
        """Set data member by importing a ``pawianHists.root`` file."""
        self.__file = uproot.open(filename)
        self.__data = read_pawian_hists(filename, type_name="data")
        self.__fit = read_pawian_hists(filename, type_name="fit")

    def get_uproot_histogram(self, name):
        """Get a histogram from a :file:`pawianHists.root` file.

        Get an uproot ``TH1``, ``TH2``, or ``TH3`` from the
        ``pawianHists.root`` file. See `here
        <https://github.com/scikit-hep/uproot-methods/blob/master/uproot_methods/classes/TH1.py>`__
        which methods you can call on these classes or have a look at the
        ``QA_Histograms.ipynb`` Jupyter notebook.
        """
        try:
            obj = self.__file[name]
        except KeyError:
            return None
        if isinstance(obj, TH1.Methods):
            return obj
        return None

    def get_histogram_content(self, name: str) -> Optional[Tuple[list, list]]:
        """Get an array of lower edges and an array of values for the histogram.

        You can then for instance use `matplotlib.pyplot.hist
        <https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist.html>`__ to
        plot it like so (note the ``bins`` argument!):

        .. code-block:: python

            from pawian.qa import PawianHists
            import matplotlib.pyplot as plt
            hist_file = PawianHists(FILENAME)
            edges, values = hist_file.get_histogram_content(HISTOGRAM_NAME)
            plt.hist(edges, weights=values, bins=len(values))
        """
        histogram = self.get_uproot_histogram(name)
        if histogram is None:
            return None
        edges = histogram.edges[:-1]
        values = histogram.values
        return (edges, values)

    def draw_histogram(self, name, plot_on=plt, **kwargs):
        """Plot a histogram in a matplotlib figure.

        :param plot_on:
            Feed a matplotlib class with a hist method, such as `matplotlib.axes.Axes
            <https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.hist.html>`__
            to draw the histogram on it.
        :param kwargs:
            see `matplotlib.pyplot.hist arguments
            <https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist.html>`__
        """
        if name not in self.histogram_names:
            raise Exception(f'Histogram "{name}" does not exist')
        edges, values = self.get_histogram_content(name)
        return plot_on.hist(edges, weights=values, bins=len(values), **kwargs)

    def draw_combined_histogram(  # pylint: disable=too-many-arguments,invalid-name
        self, name, plot_on=plt, data=True, fit=True, mc=True, **kwargs,
    ):
        """Combine the three types of histograms in one plot.

        :param name:
            The name of the histogram in the ``pawianHists.root`` file that you want to plot, **but
            without the prepended ``Data``, ``Fit``, or ``MC/Mc``**.

        .. seealso:: :func:`draw_histogram`
        """
        if name not in self.unique_histogram_names:
            raise Exception(f'Histogram of type "{name}" does not exist')
        # Construct regular expression
        re_match = []
        if data:
            re_match.append("Data")
        if fit:
            re_match.append("Fit")
        if mc:
            re_match.append("MC")
            re_match.append("Mc")
        re_match = "|".join(re_match)
        re_match = f"({re_match}){name}"
        # Makes selection of names plus corresponding labels
        names = [k for k in self.histogram_names if re.fullmatch(re_match, k)]
        labels = [re.match(re_match, k)[1].lower() for k in names]
        # Create histograms
        hists = dict()
        for hist_name, label in zip(names, labels):
            histogram = self.draw_histogram(
                hist_name, plot_on, label=label, **kwargs
            )
            hists[label] = histogram
        return hists

    def draw_all_histograms(self, plot_on=plt.figure(), legend=True, **kwargs):
        """Draw a comparative overview of all histograms.

        .. seealso::
            :func:`draw_combined_histogram`.
        """
        logging.info(
            "Drawing all histograms for file %s ...", self.__file.name.decode()
        )
        names = self.unique_histogram_names
        n_hists = len(names)
        n_x = ceil(sqrt(len(names)))
        n_y = ceil(n_hists / n_x)

        grid = plot_on.add_gridspec(n_x, n_y)
        for idx, name in enumerate(names):
            sub = plot_on.add_subplot(grid[idx % n_x, idx // n_x])
            self.draw_combined_histogram(name, sub, **kwargs)
            sub.set_title(f"${convert(name)}$")
            if legend:
                sub.legend()

    @property
    def histogram_names(self):
        """Get a list of all histogram names in the :file:`pawianHists.root`."""
        names = []
        for name in self.__file.keys():
            obj = self.__file[name]
            if isinstance(obj, TH1.Methods):
                names.append(obj.name.decode())
        return names

    @property
    def unique_histogram_names(self):
        """Get a list of unique histograms from a :file:`pawianHists.root` file.

        Get a list of histograms in the ``pawianHists.root`` file of which the
        keywords ``Data``, ``MC``, or ``Fit`` have been removed.
        """
        names = []
        for name in self.__file.keys():
            obj = self.__file[name]
            if isinstance(obj, TH1.Methods):
                hist_name = obj.name.decode()
                if hist_name.startswith("Data"):
                    hist_name = hist_name[4:]
                    names.append(hist_name)
        return names

    @property
    def particles(self):
        """Get particle names contained in the file."""
        return self.data.pawian.particles

    @property
    def data(self):
        """Get a `~.pandas.DataFrame` of the data intensity sample.

        Get a `pandas.DataFrame
        <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`__
        of the **data events** contained in the ``pawianHists.root`` file.

        .. seealso::
            :func:`fit <pawian.qa.PawianHists.fit>`
        """
        return self.__data

    @property
    def fit(self):
        """Get a `~.pandas.DataFrame` of the fit intensity sample.

        Get a `pandas.DataFrame
        <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`__
        of the **fit intensity sample** contained in the ``pawianHists.root``
        file.

        .. seealso::
            :func:`data <pawian.qa.PawianHists.data>`.
        """
        return self.__fit
