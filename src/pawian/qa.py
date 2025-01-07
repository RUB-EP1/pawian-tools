"""Handle output of the QA step performed by Pawian.

Usually, a :file:`pawianHists.root` file is produced if you run Pawian in QA mode. This
module contains handlers for such files.
"""

from __future__ import annotations

import logging
import re  # regex
from math import ceil, sqrt
from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import uproot
from uproot.behaviors.TH1 import TH1

from pawian.data import read_pawian_hists
from pawian.latex import convert

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.container import BarContainer
    from matplotlib.figure import Figure
    from uproot.behaviors.TAxis import TAxis
    from uproot.behaviors.TH2 import TH2
    from uproot.behaviors.TH3 import TH3
    from uproot.reading import ReadOnlyDirectory

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Foobar")


class PawianHists:
    """Data container for a :file:`pawianHists.root` file.

    Data container for a :file:`pawianHists.root` file that is created by the QA step in
    Pawian.
    """

    def __init__(self, filename: str) -> None:
        self.import_file(filename)

    def import_file(self, filename: str) -> None:
        """Set data member by importing a :file:`pawianHists.root` file."""
        self.__file: ReadOnlyDirectory = uproot.open(filename)
        self.__data = read_pawian_hists(filename, type_name="data")
        self.__fit = read_pawian_hists(filename, type_name="fitted")

    def get_uproot_histogram(self, name: str) -> TH1 | TH2 | TH3 | None:
        """Get a histogram from a :file:`pawianHists.root` file.

        Get an `uproot` histogram from the :file:`pawianHists.root` file.
        """
        try:
            obj = self.__file[name]
        except KeyError:
            return None
        if isinstance(obj, TH1):
            return obj
        return None

    def get_histogram_content(self, name: str) -> tuple[list, list] | None:
        """Get an array of lower edges and an array of values for the histogram.

        You can then for instance use `matplotlib.pyplot.hist` to plot it like
        so (note the :code:`bins` argument!):

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
        x_axis: TAxis = histogram.axes[0]
        edges = x_axis.edges()[:-1]
        values = histogram.values()
        return edges, values

    def draw_histogram(
        self, name: str, plot_on: Axes | None = None, **kwargs: Any
    ) -> tuple[np.ndarray, np.ndarray, BarContainer]:
        """Plot a histogram in a matplotlib figure.

        Args:
            name: The name of the histogram in the :file:`pawianHists.root` file that
                you want to plot.
            plot_on: Feed a matplotlib class with a hist method, such as
                `matplotlib.axes.Axes` to draw the histogram on it.

            kwargs: See `matplotlib.pyplot.hist` arguments
        """
        if name not in self.histogram_names:
            msg = f'Histogram "{name}" does not exist'
            raise KeyError(msg)
        hist_content = self.get_histogram_content(name)
        if hist_content is None:
            msg = f'Could not get histogram "{name}"'
            raise KeyError(msg)
        edges, values = hist_content
        if plot_on is None:
            plot_on = plt  # type: ignore[assignment]
        return plot_on.hist(edges, weights=values, bins=len(values), **kwargs)  # type: ignore[call-arg,return-value,union-attr]

    def draw_combined_histogram(
        self,
        name: str,
        plot_on: Axes | None = None,
        data: bool = True,
        fit: bool = True,
        mc: bool = True,
        **kwargs: Any,
    ) -> dict[str, tuple[np.ndarray, np.ndarray, BarContainer]]:
        """Combine the three types of histograms in one plot.

        Args:
            name: The name of the histogram in the :file:`pawianHists.root` file that
                you want to plot, but without the prepended :code:`Data`, :code:`Fit`,
                or :code:`MC/Mc`.
            plot_on: The axis on which to draw the histogram. If `None`, `matplotlib`
                will create a new figure.

            data: Whether to draw the data histogram.
            fit: Whether to draw the 'fitted' histogram.
            mc: Whether to draw the Monte Carlo histogram.
            kwargs: Arguments that are passed to :func:`draw_histogram`.
        """
        if name not in self.unique_histogram_names:
            msg = f'Histogram of type "{name}" does not exist'
            raise KeyError(msg)
        # Construct regular expression
        re_match_list = []
        if data:
            re_match_list.append("Data")
        if fit:
            re_match_list.append("Fit")
        if mc:
            re_match_list.extend(("MC", "Mc"))
        re_match = "|".join(re_match_list)
        re_match = f"({re_match}){name}"
        # Makes selection of names plus corresponding labels
        names = [k for k in self.histogram_names if re.fullmatch(re_match, k)]
        matches = [re.match(re_match, k) for k in names]
        labels = [match[1].lower() for match in matches if match is not None]
        # Create histograms
        hists = {}
        for hist_name, label in zip(names, labels):
            histogram = self.draw_histogram(hist_name, plot_on, label=label, **kwargs)
            hists[label] = histogram
        return hists

    def draw_all_histograms(
        self, plot_on: Figure | None = None, legend: bool = True, **kwargs: Any
    ) -> None:
        """Draw a comparative overview of all histograms.

        .. seealso:: :func:`draw_combined_histogram`.
        """
        _LOGGER.info(f"Drawing all histograms for file {self.__file.file_path}...")
        names = self.unique_histogram_names
        n_hists = len(names)
        n_x = ceil(sqrt(len(names)))
        n_y = ceil(n_hists / n_x)
        if plot_on is None:
            plot_on = plt.figure()
        grid = plot_on.add_gridspec(n_x, n_y)  # type: ignore[union-attr]
        for idx, name in enumerate(names):
            assert plot_on is not None  # noqa: S101
            sub = plot_on.add_subplot(grid[idx % n_x, idx // n_x])
            self.draw_combined_histogram(name, sub, **kwargs)
            sub.set_title(f"${convert(name)}$")
            if legend:
                sub.legend()

    @property
    def histogram_names(self) -> list[str]:
        """Get a list of all histogram names in a :file:`pawianHists.root` file."""
        names = []
        for name in self.__file:
            obj = self.__file[name]
            if isinstance(obj, TH1):
                names.append(obj.name)
        return names

    @property
    def unique_histogram_names(self) -> list[str]:
        """Get a list of unique histograms from a :file:`pawianHists.root` file.

        Get a list of histograms in the :file:`pawianHists.root` file of which the
        keywords :code:`Data`, :code:`MC`, or :code:`Fit` have been removed.
        """
        names = []
        for name in self.__file:
            obj = self.__file[name]
            if isinstance(obj, TH1):
                hist_name = obj.name
                if hist_name.startswith("Data"):
                    hist_name = hist_name[4:]
                    names.append(hist_name)
        return names

    @property
    def particles(self) -> list[str]:
        """Get particle names contained in the file."""
        return self.data.pwa.particles

    @property
    def data(self) -> pd.DataFrame:
        """Get a `~.pandas.DataFrame` of the data intensity sample.

        Get a `~pandas.DataFrame` of the **data events** contained in the
        :file:`pawianHists.root` file.

        .. seealso::
            :func:`fit <pawian.qa.PawianHists.fit>`
        """
        return self.__data

    @property
    def fit(self) -> pd.DataFrame:
        """Get a `~.pandas.DataFrame` of the fit intensity sample.

        Get a `~pandas.DataFrame` of the **fit intensity sample** contained in
        the :file:`pawianHists.root` file.

        .. seealso:: :func:`pawian.qa.PawianHists.data`.
        """
        return self.__fit
