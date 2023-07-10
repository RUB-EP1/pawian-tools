from os.path import dirname, realpath

import pandas as pd
import pytest

import pawian
from pawian.data import create_skeleton_frame, read_ascii

PAWIAN_DIR = dirname(realpath(pawian.__file__))
SAMPLE_DIR = f"{PAWIAN_DIR}/samples"
INPUT_FILE_DATA = f"{SAMPLE_DIR}/momentum_tuples_data.dat"
INPUT_FILE_MC = f"{SAMPLE_DIR}/momentum_tuples_mc.dat"


@pytest.mark.parametrize(
    ("particles", "number_of_rows"),
    [
        (["pi+", "D0", "D-"], 100),
        (None, 50),
    ],
)
def test_create_skeleton(particles, number_of_rows):
    """Test creating an empty pawian dataframe."""
    frame = create_skeleton_frame(
        particle_names=particles,
        number_of_rows=number_of_rows,
    )
    if number_of_rows is None:
        number_of_rows = 0
    assert not frame.pwa.has_weights
    assert len(frame) == number_of_rows
    if frame.pwa.has_particles:
        assert frame.pwa.particles == particles


@pytest.mark.parametrize(
    ("columns", "names"),
    [
        (  # wrong number of column LEVELS
            [
                "A",
                "B",
                "C",
            ],
            ["Particles"],
        ),
        (  # wrong momentum labels
            [
                ("A", "px"),
                ("A", "b"),
                ("B", "px"),
                ("B", "b"),
            ],
            ["Particles", "Momentum"],
        ),
    ],
)
def test_raise_validate(columns, names):
    """Test exception upon validate."""
    multi_index = pd.MultiIndex.from_tuples(columns, names=names)
    frame = pd.DataFrame(columns=multi_index)
    with pytest.raises(AttributeError):
        print(frame.pwa)  # noqa: T201


def test_properties_multicolumn():
    """Test whether properties work for multicolumn dataframe."""
    particles = ["pi+", "D0", "D-"]
    frame_data = read_ascii(INPUT_FILE_DATA, particles=particles)
    frame_mc = read_ascii(INPUT_FILE_MC, particles=particles)

    assert frame_data.pwa.has_weights
    assert not frame_mc.pwa.has_weights
    with pytest.raises(ValueError, match=r"Dataframe doesn't contain weights"):
        assert frame_mc.pwa.weights

    assert frame_data.pwa.weights.iloc[1] == 0.990748
    assert frame_data.pwa.weights.iloc[-1] == 0.986252
    assert frame_data.pwa.weights.equals(frame_data.pwa.intensities)

    assert frame_mc.pwa.particles == particles
    assert frame_data.pwa.particles == particles

    momentum_labels = ["p_x", "p_y", "p_z", "E"]
    assert frame_mc.pwa.momentum_labels == momentum_labels
    assert frame_data.pwa.momentum_labels == momentum_labels

    assert pytest.approx(frame_data.pwa.mass.mean().tolist()) == [
        1.8696104109755363,
        1.8648403010481123,
        0.13957021474219994,
    ]
    assert pytest.approx(frame_data.pwa.rho.mean().tolist()) == [
        0.6915457642796756,
        0.6476585301989026,
        0.14209924919519798,
    ]


def test_properties_single_column():
    """Test whether properties work for single column dataframe."""
    particles = ["pi+", "D0", "D-"]
    pi_data = read_ascii(INPUT_FILE_DATA, particles=particles)["pi+"]
    pi_mc = read_ascii(INPUT_FILE_MC, particles=particles)["pi+"]

    assert pi_data.pwa.energy.iloc[-1] == 0.152749
    assert pi_mc.pwa.energy.iloc[-1] == 0.257006

    assert pytest.approx(pi_data.pwa.rho2.iloc[-1]) == 0.00385247006036

    with pytest.raises(
        ValueError,
        match=r"This dataframe is single-level and does not contain particles",
    ):
        assert pi_data.pwa.particles
