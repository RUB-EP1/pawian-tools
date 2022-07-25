from os.path import dirname, realpath
from statistics import mean

import matplotlib.pyplot as plt
import pytest

import pawian
from pawian.qa import PawianHists

PAWIAN_DIR = dirname(realpath(pawian.__file__))
SAMPLE_DIR = f"{PAWIAN_DIR}/samples"
FILENAME_ROOT5 = f"{SAMPLE_DIR}/pawianHists_ROOT5_SigmaKp.root"
FILENAME_ROOT6 = f"{SAMPLE_DIR}/pawianHists_ROOT6_DDpi.root"


def test_faulty_import():
    """Test exceptions upon corrupt file."""
    with pytest.raises(FileNotFoundError):
        PawianHists("non-existent")
    with pytest.raises(ValueError):
        PawianHists(__file__)


@pytest.mark.parametrize(
    "filename, hist_value, particles, n_data, n_fit, hist_names, unique_names",
    [
        # cspell:ignore Sigmaplus Sigmaplusantiproton
        (
            FILENAME_ROOT5,
            ("DataSigmaplusK0", 14.0),
            ["Sigmaplus", "antiproton", "K0"],
            1001,
            2002,
            [
                "FitK0antiproton",
                "DataSigmaplusantiproton",
                "MCSigmaplusantiproton",
                "FitSigmaplusantiproton",
            ],
            [
                "PhiGJ_antiproton_FromK0Sigmaplusantiproton",
                "SigmaplusK0",
                "K0antiproton",
                "Sigmaplusantiproton",
            ],
        ),
        (
            FILENAME_ROOT6,
            ("DataD0Dm", 2.494117),
            ["pi+", "D0", "D-"],
            501,
            2505,
            ["FitpipDm", "DataD0Dm", "MCD0Dm", "FitD0Dm"],
            ["PhiGJ_D0_FromD0Dm", "pipD0", "pipDm", "D0Dm"],
        ),
    ],
)
def test_data_model(  # pylint: disable=too-many-arguments
    filename, hist_value, particles, n_data, n_fit, hist_names, unique_names
):
    """Test whether properties are correct."""
    pawian_hists = PawianHists(filename)

    assert pawian_hists.get_uproot_histogram("non-existent") is None
    assert pawian_hists.get_uproot_histogram("_fittedFourvecs") is None

    failure = pawian_hists.get_histogram_content("non-existent")
    assert failure is None
    edges, values = pawian_hists.get_histogram_content(hist_value[0])  # type: ignore
    assert len(edges) == 100
    assert len(values) == 100
    assert pytest.approx(values[40]) == hist_value[1]

    assert pawian_hists.particles == particles
    assert pawian_hists.data.pwa.particles == particles  # type: ignore[attr-defined]
    assert pawian_hists.fit.pwa.particles == particles  # type: ignore[attr-defined]

    assert len(pawian_hists.data) == n_data
    assert len(pawian_hists.fit) == n_fit

    assert pawian_hists.histogram_names[-4:] == hist_names
    assert pawian_hists.unique_histogram_names[-4:] == unique_names


def test_draw_histogram():
    """Test whether embedded histograms can be drawn."""
    hists = PawianHists(FILENAME_ROOT6)
    with pytest.raises(Exception):
        assert hists.draw_histogram("non-existent")
    values, edges, patch = hists.draw_histogram("FitThetaHeli_pip_FrompipD0Dm")
    # cspell:ignore Frompip
    assert len(values) == 100
    assert values[0] == 0.7086924910545349
    assert len(edges) == 101
    assert edges[0] == -1.0
    assert patch[-5].get_height() == values[-5]


@pytest.mark.slow
def test_draw_all_histograms():
    """Test :func:`pawian.qa.PawianHists.draw_all_histograms`"""
    hists = PawianHists(FILENAME_ROOT6)
    hists.draw_all_histograms()
    n_plots = len(plt.gcf().get_axes())  # type: ignore
    assert n_plots == 19


@pytest.mark.slow
def test_draw_combined_histogram():
    """Test :func:`pawian.qa.PawianHists.draw_combined_histogram`"""
    hists = PawianHists(FILENAME_ROOT6)
    name = "pipDm"
    with pytest.raises(Exception):
        hists.draw_combined_histogram("non-existent")
    assert list(hists.draw_combined_histogram(name, data=False).keys()) == [
        "mc",
        "fit",
    ]
    assert list(hists.draw_combined_histogram(name, fit=False).keys()) == [
        "data",
        "mc",
    ]
    assert list(hists.draw_combined_histogram(name, mc=False).keys()) == [
        "data",
        "fit",
    ]
    result = hists.draw_combined_histogram(name)
    values, edges, patch = result["data"]
    assert values[10] == 0.6596219539642334
    assert mean(edges) == 2.1605122581
    assert patch[5].get_height() == values[5]


@pytest.mark.parametrize(
    "filename, energy",
    [
        (FILENAME_ROOT5, 1.338907402473968),
        (FILENAME_ROOT6, 0.20740474665355302),
    ],
)
def test_lorentz_vectors(filename, energy):
    """Test whether vectors were loaded correctly as `~pandas.DataFrame`."""
    pawian_hists = PawianHists(filename)
    particle = pawian_hists.particles[0]
    assert pawian_hists.data[particle].E.mean() == energy  # type: ignore[attr-defined]
