from os.path import dirname, realpath

import pytest

import pawian
from pawian.data import read_pawian_hists

PAWIAN_DIR = dirname(realpath(pawian.__file__))
SAMPLE_DIR = f"{PAWIAN_DIR}/samples"


@pytest.mark.parametrize(
    "input_file, has_weights, particles, energy",
    [
        (
            "pawianHists_ROOT5_SigmaKp.root",
            False,
            ["Sigmaplus", "antiproton", "K0"],
            1.338907402473968,
        ),
        (
            "pawianHists_ROOT6_DDpi.root",
            True,
            ["pi+", "D0", "D-"],
            0.20740474665355302,
        ),
    ],
)
def test_read_pawian_hists(input_file, has_weights, particles, energy):
    """Test loading pawianHists.root file"""
    input_file = f"{SAMPLE_DIR}/{input_file}"
    data = read_pawian_hists(input_file, type_name="data")
    fit = read_pawian_hists(input_file, type_name="fit")

    assert fit.pwa.has_weights
    assert data.pwa.has_weights == has_weights

    assert data.pwa.particles == particles

    assert data[particles[0]].pwa.energy.mean() == energy


def test_read_pawian_hists_exception():
    """Test whether expected exceptions are raised"""
    with pytest.raises(Exception):
        read_pawian_hists(
            f"{SAMPLE_DIR}/pawianHists_ROOT6_DDpi.root",
            type_name="wrong",
        )
