"""
Handle output of the QA step performed by Pawian

Usually, a ``pawianHists.root`` file is produced if you run Pawian in QA mode. This module contains
handlers for such files.
"""

__author__ = "Meike Küßner, Remco de Boer"
__institution__ = "Ruhr-Universität Bochum"


__all__ = ['PawianHists', 'EventSet']


from os.path import dirname, realpath
import math
import numpy as np
from matplotlib.pyplot import hist
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

    def get_histogram(self, name):
        """Get a TH1F from the pawianHists.root file and convert to a numpy histogram"""
        try:
            obj = self.__file[name]
        except KeyError:
            return None
        if isinstance(obj, TH1.Methods):
            values = obj.values
            edges = obj.edges[:-1]
            return hist(
                edges, weights=values, bins=len(values))
        return None

    @property
    def histogram_names(self):
        """Get a list of histograms in the pawianHists.root file"""
        names = []
        for name in self.__file.keys():
            obj = self.__file[name]
            if isinstance(obj, TH1.Methods):
                names.append(obj.name.decode())
        return names

    @property
    def particles(self):
        """Get particle names contained in the file"""
        return self.data.particles

    @property
    def fit(self):
        """Get :func:`EventSet <EventSet>` object of fit data, see
        :func:`data <pawian.qa.PawianHists.data>`"""
        return self.__fit

    @property
    def data(self):
        """Get :func:`EventSet <EventSet>` object. This contains :func:`weights <EventSet.weights>`
        and a :func:`dictionary of particles`, the entries of which are arrays of
        `TLorentzVectors <https://root.cern.ch/doc/master/classTLorentzVector.html>`__.\n
        See :func:`fit <pawian.qa.PawianHists.fit>`
        """
        return self.__data


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

    def keys(self):
        """Modulate dictionary behavior by returning the keys for __getitem__"""
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
