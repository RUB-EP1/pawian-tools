from os.path import dirname, realpath
import pandas as pd
import pytest
import numpy as np
from pawian.data import read_ascii


SCRIPT_DIR = dirname(realpath(__file__))
INPUT_FILE_DATA = f'{SCRIPT_DIR}/momentum_tuples_data.dat'
INPUT_FILE_MC = f'{SCRIPT_DIR}/momentum_tuples_mc.dat'


@pytest.mark.parametrize("columns,names", [
    (  # wrong number of column LEVELS
        [
            ('A'), ('B'), ('C'),
        ],
        ['Particles'],
    ), (   # wrong momentum labels
        [
            ('A', 'px'), ('A', 'b'),
            ('B', 'px'), ('B', 'b'),
        ],
        ['Particles', 'Momentum'],
    )
])
def test_raise_validate(columns, names):
    multi_index = pd.MultiIndex.from_tuples(columns, names=names)
    frame = pd.DataFrame(columns=multi_index)
    with pytest.raises(AttributeError):
        print(frame.pawian)


def test_properties_multicolumn():
    particles = ['pi+', 'D0', 'D-']
    frame_data = read_ascii(INPUT_FILE_DATA, particles=particles)
    frame_mc = read_ascii(INPUT_FILE_MC, particles=particles)

    assert frame_data.pawian.has_weights
    assert not frame_mc.pawian.has_weights

    assert frame_data.pawian.weights.iloc[1] == 0.990748
    assert frame_data.pawian.weights.iloc[-1] == 0.986252

    assert frame_mc.pawian.particles == particles
    assert frame_data.pawian.particles == particles

    momentum_labels = ['p_x', 'p_y', 'p_z', 'E']
    assert frame_mc.pawian.momentum_labels == momentum_labels
    assert frame_data.pawian.momentum_labels == momentum_labels

    assert np.allclose(
        frame_data.pawian.mass.mean().tolist(),
        [
            0.13957,
            1.86484,
            1.86961,
        ], atol=1e-5)
    assert np.allclose(
        frame_data.pawian.rho.mean().tolist(),
        [
            0.14209,
            0.64765,
            0.69154,
        ], atol=1e-5)


def test_properties_single_column():
    particles = ['pi+', 'D0', 'D-']
    pi_data = read_ascii(INPUT_FILE_DATA, particles=particles)['pi+']
    pi_mc = read_ascii(INPUT_FILE_MC, particles=particles)['pi+']

    assert pi_data.pawian.energy.iloc[-1] == 0.152749
    assert pi_mc.pawian.energy.iloc[-1] == 0.257006

    assert pi_data.pawian.rho2.iloc[-1] == 0.0038524700603599993
