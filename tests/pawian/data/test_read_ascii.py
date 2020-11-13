from os.path import dirname, realpath

import pytest

import pawian
from pawian.data import DataParserError, read_ascii

PAWIAN_DIR = dirname(realpath(pawian.__file__))
SAMPLE_DIR = f"{PAWIAN_DIR}/samples"
INPUT_FILE_DATA = f"{SAMPLE_DIR}/momentum_tuples_data.dat"
INPUT_FILE_MC = f"{SAMPLE_DIR}/momentum_tuples_mc.dat"


def test_read_with_weight():
    """Read a file that contains weights"""
    frame = read_ascii(INPUT_FILE_DATA)
    assert len(frame) == 1000
    assert len(frame.columns.levels[0]) == 4
    assert len(frame.columns.levels[1]) == 5
    assert "" in frame.columns.levels[1]

    column_names = frame.columns.droplevel(1).unique().tolist()
    head = frame.head(1)
    assert pytest.approx(head[column_names[-1]].values[0]) == 0.99407
    assert pytest.approx(head[column_names[0]].values.tolist()[0]) == [
        -0.00357645,
        0.0962561,
        0.0181079,
        0.170545,
    ]
    assert pytest.approx(head[column_names[2]].values.tolist()[0]) == [
        -0.174404,
        -0.719412,
        -0.233159,
        2.0243,
    ]

    tail = frame.tail(1)
    assert pytest.approx(tail[column_names[0]].values.tolist()[0]) == [
        -0.0487412,
        -0.0343714,
        0.0171864,
        0.152749,
    ]
    assert pytest.approx(tail[column_names[2]].values.tolist()[0]) == [
        0.376848,
        0.225407,
        -0.659593,
        2.0306,
    ]


@pytest.mark.parametrize(
    "particles",
    [
        ["pi+", "D0", "D-"],
        3,
        [1, 2, 3],
    ],
)
def test_read_no_weights(particles):
    """Read a file without weights"""
    frame = read_ascii(INPUT_FILE_MC, particles=particles)
    assert len(frame) == 1000
    assert len(frame.columns.levels[0]) == 3
    assert len(frame.columns.levels[1]) == 4

    column_names = frame.columns.droplevel(1).unique().tolist()
    head = frame.head(1)
    assert pytest.approx(head[column_names[0]].values.tolist()[0]) == [
        -0.279306,
        -0.175576,
        -0.122704,
        0.378648,
    ]
    assert pytest.approx(head[column_names[2]].values.tolist()[0]) == [
        0.0245524,
        -0.146873,
        0.193947,
        1.88553,
    ]

    tail = frame.tail(1)
    assert pytest.approx(tail[column_names[0]].values.tolist()[0]) == [
        -0.189277,
        -0.0520959,
        -0.0896247,
        0.257006,
    ]
    assert pytest.approx(tail[column_names[2]].values.tolist()[0]) == [
        0.640318,
        -0.186286,
        -0.0528645,
        1.98569,
    ]


def test_read_with_weights_wrong_particles():
    """Test whether exceptions are raised"""
    with pytest.raises(DataParserError):
        read_ascii(INPUT_FILE_DATA, 4)
    with pytest.raises(DataParserError):
        read_ascii(INPUT_FILE_MC)
