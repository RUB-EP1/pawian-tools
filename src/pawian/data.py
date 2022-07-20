# cspell:ignore astype dropna

"""Data module of PawianTools.

This module allows you to parse and analyze ASCII data files of momentum
tuples. The files have the following form:

.. code-block::

    0.99407
    -0.00357645   0.0962561   0.0181079    0.170545
       0.224019    0.623156    0.215051     1.99057
      -0.174404   -0.719412   -0.233159      2.0243
    0.990748
     -0.0328198   0.0524406   0.0310079    0.155783
      -0.619592    0.141315     0.32135     1.99619
       0.698477   -0.193756   -0.352357     2.03593

The lines with single values are weights, but do not have to be present.
Whitespaces are arbitrary.

The allows you to import the ASCII file to a nicely formatted
`~pandas.DataFrame` that has additional PWA methods in the form of
`~pandas.DataFrame` accessors.
"""


import pandas as pd
import uproot
from numpy import sqrt

_ENERGY_LABEL = "E"
_MOMENTUM_LABELS = ["p_x", "p_y", "p_z", _ENERGY_LABEL]
_WEIGHT_LABEL = "weight"


class DataParserError(Exception):
    """Exception for if a data file can't be handled."""


@pd.api.extensions.register_dataframe_accessor("pwa")  # type: ignore
class PwaAccessor:
    """PWA-specific accessor for a `~pandas.DataFrame`.

    Additional namespace to interpret DataFrame as Pawian style dataframe, see
    :doc:`pandas:development/extending`.
    """

    def __init__(self, pandas_object):
        self._validate(pandas_object)
        self._obj = pandas_object

    @staticmethod
    def _validate(obj):
        columns = obj.columns
        if isinstance(columns, pd.MultiIndex):
            # if multicolumn, test if 2 levels
            columns = columns.levels
            if len(obj.columns.levels) != 2:
                raise AttributeError(
                    "Not a Pawian data object!\n"
                    "pandas.DataFrame must have multi-columns of 2 levels:\n"
                    " - 1st level are particles\n"
                    f" - 2nd level are define the 4-momentum: {_MOMENTUM_LABELS}"
                )
            # then select 2nd columns only
            columns = columns[1]
        # Check if (sub)column names are same as momentum labels
        if not set(_MOMENTUM_LABELS) <= set(columns):
            raise AttributeError(f"Columns must be {_MOMENTUM_LABELS}")

    @property
    def has_weights(self):
        """Check if dataframe contains weights."""
        return _WEIGHT_LABEL in self._obj.columns

    @property
    def has_particles(self):
        """Check if dataframe contains a main column with particles."""
        return isinstance(self._obj.columns, pd.MultiIndex)

    @property
    def weights(self):
        """Get list of weights, if available."""
        if not self.has_weights:
            raise Exception("Dataframe doesn't contain weights")
        return self._obj[_WEIGHT_LABEL]

    @property
    def intensities(self):
        """Alias for :func:`weights` in the case of a fit intensity sample."""
        return self.weights

    @property
    def particles(self):
        """Get list of particles contained in the data frame."""
        if not self.has_particles:
            raise Exception(
                "This dataframe is single-level and does not contain particles"
            )
        particles = self._obj.columns.droplevel(1).unique()
        if self.has_weights:
            particles = particles.drop(_WEIGHT_LABEL)
        return particles.to_list()

    @property
    def momentum_labels(self):
        """Get list of momentum labels contained in the data frame."""
        momentum_labels = self._obj.columns.droplevel(0).unique()
        if self.has_weights:
            momentum_labels = momentum_labels[:-1]
        return momentum_labels.to_list()

    @property
    def energy(self):
        """Get a dataframe containing only the energies."""
        if self.has_particles:
            return self._obj.xs(_ENERGY_LABEL, level=1, axis=1)
        return self._obj[_ENERGY_LABEL]

    @property
    def p_xyz(self):
        """Get a dataframe containing only the 3-momenta."""
        return self._obj.filter(
            regex=("p_[xyz]")
        )  # ! may conflict with _MOMENTUM_LABELS

    @property
    def rho2(self):
        """Compute a dataframe containing the square sum of the 3-momenta."""
        if self.has_particles:
            return (self.p_xyz**2).sum(axis=1, level=0)
        return (self.p_xyz**2).sum(axis=1)

    @property
    def rho(self):
        """**Compute** a dataframe with the absolute value of the 3-momenta."""
        return sqrt(self.rho2)

    @property
    def mass2(self):
        """**Compute** the square of the invariant masses."""
        return self.energy**2 - self.rho2

    @property
    def mass(self):
        """**Compute** the invariant masses."""
        return sqrt(self.mass2)

    def write_ascii(self, filename, **kwargs):
        """Write to Pawian-like ASCII file."""
        new_dict = []
        if self.has_weights:
            new_dict.append(self._obj[_WEIGHT_LABEL])
        for par in self.particles:
            new_dict.append(
                self._obj[par].apply(
                    lambda x: " ".join(x.dropna().astype(str)),
                    axis=1,
                )
            )
        # cspell:ignore mergesort
        interleaved = pd.concat(new_dict).sort_index(kind="mergesort")
        interleaved.to_csv(filename, header=False, index=False, **kwargs)


def create_skeleton_frame(particle_names=None, number_of_rows=None):
    """Create skeleton `~pandas.DataFrame`.

    Create an empty `~pandas.DataFrame` that complies with the standards of the
    registered `.PwaAccessor`.
    """
    index = None
    if number_of_rows is not None:
        index = pd.RangeIndex(number_of_rows)
    if particle_names is None:
        return pd.DataFrame(index=index, columns=_MOMENTUM_LABELS)
    cols = [(par, mom) for par in particle_names for mom in _MOMENTUM_LABELS]
    multi_column = pd.MultiIndex.from_tuples(
        tuples=cols, names=["Particle", "Momentum"]
    )
    return pd.DataFrame(index=index, columns=multi_column)


def read_ascii(filename, particles=None, **kwargs):
    """Import from a Pawian-like ASCII file."""
    full_table = pd.read_table(
        filepath_or_buffer=filename,
        names=_MOMENTUM_LABELS,
        sep=r"\s+",
        skip_blank_lines=True,
        dtype="float64",
        **kwargs,
    )

    # Determine if ascii file contains weights
    py_values = full_table[_MOMENTUM_LABELS[1]]
    has_weights = py_values.first_valid_index() > 0
    if not has_weights:
        if isinstance(particles, int):
            particles = [f"Particle {i}" for i in range(1, particles + 1)]
        elif particles is None or not isinstance(particles, list):
            raise DataParserError(
                f'Cannot determine number of particles in file"{filename}"\n'
                "--> Please provide an array of particles for interpretation"
            )

    # Try to determine number of particles from file
    if has_weights:
        file_n_particles = py_values.index[py_values.isnull()][1] - 1
        if particles is None:
            particles = range(1, file_n_particles + 1)
        if isinstance(particles, int):
            particles = range(1, particles + 1)
        if len(particles) != file_n_particles:
            raise DataParserError(
                f'File "{filename}" contains {file_n_particles}, but you said there '
                f"were {len(particles)} ({particles})"
            )

    # Prepare splitting into particle columns
    first_momentum_row = 0
    n_rows = len(particles)
    if has_weights:
        first_momentum_row = 1
        n_rows += 1

    # Create multi-column pandas.DataFrame
    frame = create_skeleton_frame(
        particle_names=particles,
        number_of_rows=len(full_table) // n_rows,
    )

    # Convert imported table to the multi-column one
    if has_weights:
        frame[_WEIGHT_LABEL] = full_table[_MOMENTUM_LABELS[0]][
            0::n_rows
        ].reset_index(drop=True)
    for start_row, par in enumerate(particles, first_momentum_row):
        for mom in _MOMENTUM_LABELS:
            frame[par, mom] = full_table[mom][start_row::n_rows].reset_index(
                drop=True
            )

    return frame


def read_pawian_hists(filename, type_name="data"):
    """Read a :file:`pawianHists.root`.

    Import one of the momentum tuple branches of a :file:`pawianHists.root`.

    Args:
        filename (str): Path to the file that you want to read.
        type_name (str): :code:`"data"` or :code:`"fitted"`.
    """
    # Determine tree name
    if "dat" in type_name.lower():
        type_name = "data"
    elif "fit" in type_name.lower():
        type_name = "fitted"
    else:
        raise Exception('Wrong type_name: should be either "data" or "fitted"')
    tree_name = f"_{type_name}Fourvecs"

    # Get particle names
    uproot_file = uproot.open(filename)
    tree = uproot_file[tree_name]
    particles = [
        particle.decode()
        for particle in tree.keys()
        if particle.decode() != _WEIGHT_LABEL
    ]

    # Import tuples as dataframe
    weights = uproot_file[f"{tree_name}/{_WEIGHT_LABEL}"].array()
    frame = create_skeleton_frame(
        particle_names=particles,
        number_of_rows=len(weights),
    )
    if weights.max() != weights.min():
        frame[_WEIGHT_LABEL] = weights
    try:  # ROOT >= 6
        for particle in particles:
            vectors = uproot_file[f"{tree_name}/{particle}"].array()
            frame[particle, _MOMENTUM_LABELS[0]] = vectors.x
            frame[particle, _MOMENTUM_LABELS[1]] = vectors.y
            frame[particle, _MOMENTUM_LABELS[2]] = vectors.z
            frame[particle, _MOMENTUM_LABELS[3]] = vectors.E
    except ValueError:  # ROOT <= 5
        for particle in particles:
            frame[particle, _MOMENTUM_LABELS[0]] = uproot_file[
                f"{tree_name}/{particle}/fP/fP.fX"
            ].array()
            frame[particle, _MOMENTUM_LABELS[1]] = uproot_file[
                f"{tree_name}/{particle}/fP/fP.fY"
            ].array()
            frame[particle, _MOMENTUM_LABELS[2]] = uproot_file[
                f"{tree_name}/{particle}/fP/fP.fZ"
            ].array()
            frame[particle, _MOMENTUM_LABELS[3]] = uproot_file[
                f"{tree_name}/{particle}/fE"
            ].array()
    return frame
