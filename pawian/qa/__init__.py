"""
Handle output of the QA step performed by Pawian

Usually, a ``pawianHists.root`` file is produced if you run Pawian in QA mode. This module contains
handlers for such files.
"""

__author__ = "Meike Küßner, Remco de Boer"
__institution__ = "Ruhr-Universität Bochum"


__all__ = ['PawianHists', 'EventSet']


import uproot
from uproot_methods.classes import TH1


_WEIGHT_TAG = 'weight'
_4VEC_BRANCH_TAG = 'Fourvecs'


class PawianHists:
    """Data container for a ``pawianHists.root`` file that is created by the QA step in Pawian"""

    def __init__(self, filename):
        self.import_file(filename)

    def import_file(self, filename):
        """Set data member by importing a ``pawianHists.root`` file"""
        self.__file = uproot.open(filename)
        self.__data = EventSet(self.__file, 'data')
        self.__fit = EventSet(self.__file, 'fit')

    def get_uproot_histogram(self, name):
        """Get an uproot ``TH1``, ``TH2``, or ``TH3`` from the ``pawianHists.root`` file. See `here
        <https://github.com/scikit-hep/uproot-methods/blob/master/uproot_methods/classes/TH1.py>`__
        which methods you can call on these classes or have a look at the ``QA_Histograms.ipynb``
        Jupyter notebook."""
        try:
            obj = self.__file[name]
        except KeyError:
            return None
        if isinstance(obj, TH1.Methods):
            return obj
        return None

    def get_histogram_content(self, name: str) -> (list, list):
        """
        Get an array of lower edges and an array of values for the histogram. You can then for
        instance use
        `matplotlib.pyplot.hist <https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist.html>`__
        to plot it like so (note the ``bins`` argument!):

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

    @property
    def histogram_names(self):
        """Get a list of **all** histogram names in the ``pawianHists.root`` file"""
        names = []
        for name in self.__file.keys():
            obj = self.__file[name]
            if isinstance(obj, TH1.Methods):
                names.append(obj.name.decode())
        return names

    @property
    def unique_histogram_names(self):
        """Get a list of histograms in the ``pawianHists.root`` file of which the keywords ``Data``,
        ``MC``, or ``Fit`` have been removed"""
        names = []
        for name in self.__file.keys():
            obj = self.__file[name]
            if isinstance(obj, TH1.Methods):
                hist_name = obj.name.decode()
                if hist_name.startswith('Data'):
                    hist_name = hist_name[4:]
                    names.append(hist_name)
        return names

    @property
    def particles(self):
        """Get particle names contained in the file"""
        return self.data.particles

    @property
    def data(self):
        """Get :func:`EventSet <EventSet>` object for data. This contains
        :func:`weights <EventSet.weights>` and a :func:`dictionary of particles`, the entries of
        which are arrays of
        `TLorentzVectors <https://root.cern.ch/doc/master/classTLorentzVector.html>`__. 

        .. seealso:: :func:`fit <pawian.qa.PawianHists.fit>`"""
        return self.__data

    @property
    def fit(self):
        """Get :func:`EventSet <EventSet>` object of fit data.

        .. seealso:: :func:`data <pawian.qa.PawianHists.data>`"""
        return self.__fit


class EventSet:
    """
    An array collection: one array for the weights and one for each of the particles
    """

    def __init__(self, uproot_file, type_name='data'):
        """
        :param type_name: data or fitted
        :type type_name: string
        """
        if 'dat' in type_name:
            type_name = 'data'
        elif 'fit' in type_name:
            type_name = 'fitted'
        else:
            raise Exception(
                f'Wrong type_name: should be either data or fitted')
        tree_name = f'_{type_name}{_4VEC_BRANCH_TAG}'
        tree = uproot_file[tree_name]
        self.__particles = [particle.decode() for particle in tree.keys()
                            if particle.decode() != _WEIGHT_TAG]
        self.__tuples = dict()
        for particle in self.__particles:
            self.__tuples[particle] = uproot_file[f'{tree_name}/{particle}'].array()
        self.__weights = uproot_file[f'{tree_name}/{_WEIGHT_TAG}']

    @property
    def particles(self):
        """Get particle names contained in the file"""
        return self.__particles

    @property
    def weights(self):
        """Get array of event weights"""
        return self.__weights

    def __getitem__(self, particle_name):
        """Get array of
        `TLorentzVector <https://root.cern.ch/doc/master/classTLorentzVector.html>`__s
        for one of the particles"""
        return self.__tuples[particle_name]
