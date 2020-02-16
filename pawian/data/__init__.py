"""
Parser(s) for Pawian data files.
"""


__all__ = ['DataParserError', 'PawianAccessor', 'read_ascii']


import math
import re
import numpy as np
import pandas as pd


_MOMENTUM_LABELS = ['p_x', 'p_y', 'p_z', 'E']
_WEIGHT_LABEL = 'weight'


class DataParserError(Exception):
    """Exception for if a data file can't be handled"""


@pd.api.extensions.register_dataframe_accessor('pawian')
class PawianAccessor:
    """Additional namespace to interpret DataFrame as Pawian style dataframe, see `here
    <https://pandas.pydata.org/pandas-docs/stable/development/extending.html#registering-custom-accessors>`__
    """

    def __init__(self, pandas_object):
        self._validate(pandas_object)
        self._obj = pandas_object

    @staticmethod
    def _validate(obj):
        columns = obj.columns.levels
        if len(columns) != 2:
            raise AttributeError(
                "Not a Pawian data object!\n"
                "pandas.DataFrame must have multicolumns of 2 levels:\n"
                " - 1st level are particles\n"
                f" - 2nd level are define the 4-momentum: {_MOMENTUM_LABELS}"
            )
        for mom in _MOMENTUM_LABELS:
            if mom not in obj.columns.levels[1]:
                raise AttributeError(f"Must have subcolumn {mom}")

    @property
    def has_weights(self):
        """Check if dataframe contains weights"""
        return _WEIGHT_LABEL in self._obj.columns.levels[0]

    @property
    def particles(self):
        """Get list of particles contained in the data frame"""
        particles = self._obj.columns.droplevel(1).unique()
        if self.has_weights:
            particles = particles.drop(_WEIGHT_LABEL)
        return particles.to_list()

    @property
    def momentum_labels(self):
        """Get list of momentum labels contained in the data frame"""
        momentum_labels = self._obj.columns.droplevel(0).unique()
        if self.has_weights:
            momentum_labels = momentum_labels[:-1]
        return momentum_labels.to_list()

    def write_ascii(self, filename, **kwargs):
        """Write to Pawian-like ASCII file

        :param kwargs:
            Optional, additional arguments that are passed on to `pandas.DataFrame.to_csv
            <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv>`__.
        """
        new_dict = list()
        if self.has_weights:
            new_dict.append(self._obj[_WEIGHT_LABEL])
        for par in self.particles:
            new_dict.append(self._obj[par].apply(
                lambda x: ' '.join(x.dropna().astype(str)),
                axis=1,
            ))
        interleaved = pd.concat(new_dict).sort_index(kind="mergesort")
        interleaved.to_csv(filename, header=False, index=False, **kwargs)


def read_ascii(filename, particles=None, **kwargs):
    """Import from a Pawian-like ASCII file

    :param particles:
        Interpretation for the tuples. **This argument is required if there are no weights.**
        Provide either the number of particles or a list of particles.
    :param kwargs:
        Optional, additional arguments that are passed on to `pandas.read_table
        <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_table.html>`__.
    """

    full_table = pd.read_table(
        filepath_or_buffer=filename,
        names=_MOMENTUM_LABELS,
        sep=R'\s+',
        skip_blank_lines=True,
        dtype='float64',
    )

    # Determine if ascii file contains weights
    py_values = full_table[_MOMENTUM_LABELS[1]]
    has_weights = (py_values.first_valid_index() > 0)
    if not has_weights:
        if isinstance(particles, int):
            particles = [f'Particle {i}' for i in range(1, particles + 1)]
        elif particles is None or not isinstance(particles, list):
            raise DataParserError(
                f'Cannot determine number of particles in file\"{filename}\"\n'
                "--> Please provide an array of particles for interpretation")

    # Try to determine number of particles from file
    if has_weights:
        file_n_partices = \
            py_values.index[py_values.isnull()][1] - 1
        if particles is None:
            particles = range(1, file_n_partices + 1)
        if isinstance(particles, int):
            particles = range(1, particles + 1)
        if len(particles) != file_n_partices:
            raise DataParserError(
                f"File \"{filename}\" contains {file_n_partices}, but you said there "
                f"were {len(particles)} ({particles})")

    # Prepare splitting into particle columns
    first_momentum_row = 0
    nrows = len(particles)
    if has_weights:
        first_momentum_row = 1
        nrows += 1

    # Create multi-column pandas.DataFrame
    cols = [(par, mom)
            for par in particles
            for mom in _MOMENTUM_LABELS]
    multi_index = pd.MultiIndex.from_tuples(
        tuples=cols, names=['Particle', 'Momentum'])
    frame = pd.DataFrame(
        index=pd.RangeIndex(len(full_table)/nrows),
        columns=multi_index)

    # Convert imported table to the multi-column one
    if has_weights:
        frame[_WEIGHT_LABEL] = \
            full_table[_MOMENTUM_LABELS[0]][0::nrows].reset_index(drop=True)
    for start_row, par in enumerate(particles, first_momentum_row):
        for mom in _MOMENTUM_LABELS:
            frame[par, mom]\
                = full_table[mom][start_row::nrows].reset_index(drop=True)

    return frame
