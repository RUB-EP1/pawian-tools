from os.path import dirname, realpath
import pandas as pd
import pytest
import numpy as np
from pawian.data import PawianAccessor, read_ascii


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


def test_properties():
    particles = ['pi+', 'D0', 'D-']
    frame_data = read_ascii(INPUT_FILE_DATA, particles=particles)
    frame_mc = read_ascii(INPUT_FILE_MC, particles=particles)

    assert frame_data.pawian.has_weights
    assert not frame_mc.pawian.has_weights

    assert frame_mc.pawian.particles == particles
    assert frame_data.pawian.particles == particles

    momentum_labels = ['p_x', 'p_y', 'p_z', 'E']
    assert frame_mc.pawian.momentum_labels == momentum_labels
    assert frame_data.pawian.momentum_labels == momentum_labels
