"""Test `pawian.qa` module"""

from os.path import dirname, realpath
from math import isclose
from statistics import mean
import matplotlib.pyplot as plt
import pytest

# import pawian.data
from pawian.qa import PawianHists


SCRIPT_DIR = dirname(realpath(__file__))
FILENAME_ROOT5 = f'{SCRIPT_DIR}/pawianHists_ROOT5_SigmaKp.root'
FILENAME_ROOT6 = f'{SCRIPT_DIR}/pawianHists_ROOT6_DDpi.root'


def test_faulty_import():
    """Test exceptions upon corrupt file"""
    with pytest.raises(FileNotFoundError):
        PawianHists('non-existent')
    with pytest.raises(ValueError):
        PawianHists(__file__)


@pytest.mark.parametrize(
    "filename, hist_value, particles, n_data, n_fit, hist_names, unique_names", [
        (
            FILENAME_ROOT5,
            ('DataSigmaplusK0', 14.0),
            ['Sigmaplus', 'antiproton', 'K0'],
            1001,
            2002,
            [
                'FitK0antiproton',
                'DataSigmaplusantiproton',
                'MCSigmaplusantiproton',
                'FitSigmaplusantiproton',
            ],
            [
                'PhiGJ_antiproton_FromK0Sigmaplusantiproton',
                'SigmaplusK0',
                'K0antiproton',
                'Sigmaplusantiproton',
            ],
        ),
        (
            FILENAME_ROOT6,
            ('DataD0Dm', 2.494117),
            ['pi+', 'D0', 'D-'],
            501,
            2505,
            ['FitpipDm', 'DataD0Dm', 'MCD0Dm', 'FitD0Dm'],
            ['PhiGJ_D0_FromD0Dm', 'pipD0', 'pipDm', 'D0Dm'],
        ),
    ])
def test_data_model(filename, hist_value, particles, n_data, n_fit, hist_names, unique_names):
    """Test whether properties are correct"""
    pawian_hists = PawianHists(filename)

    assert pawian_hists.get_uproot_histogram('non-existent') is None
    assert pawian_hists.get_uproot_histogram('_fittedFourvecs') is None

    failure = pawian_hists.get_histogram_content('non-existent')
    assert failure is None
    edges, values = pawian_hists.get_histogram_content(hist_value[0])
    assert len(edges) == 100
    assert len(values) == 100
    assert isclose(values[40], hist_value[1], abs_tol=1e-5)

    assert pawian_hists.particles == particles
    assert pawian_hists.data.pawian.particles == particles
    assert pawian_hists.fit.pawian.particles == particles

    assert len(pawian_hists.data) == n_data
    assert len(pawian_hists.fit) == n_fit

    assert pawian_hists.histogram_names[-4:] == hist_names
    assert pawian_hists.unique_histogram_names[-4:] == unique_names


def test_draw_histogram():
    """Test whether embedded histograms can be drawn"""
    hists = PawianHists(FILENAME_ROOT6)
    with pytest.raises(Exception):
        assert hists.draw_histogram('non-existent')
    values, edges, patch = hists.draw_histogram(
        'FitThetaHeli_pip_FrompipD0Dm')
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
    assert len(plt.gcf().get_axes()) == 20


@pytest.mark.slow
def test_draw_combined_histogram():
    """Test :func:`pawian.qa.PawianHists.draw_combined_histogram`"""
    hists = PawianHists(FILENAME_ROOT6)
    name = 'pipDm'
    with pytest.raises(Exception):
        hists.draw_combined_histogram('non-existent')
    assert list(hists.draw_combined_histogram(
        name, data=False).keys()) == ['mc', 'fit']
    assert list(hists.draw_combined_histogram(
        name, fit=False).keys()) == ['data', 'mc']
    assert list(hists.draw_combined_histogram(
        name, mc=False).keys()) == ['data', 'fit']
    result = hists.draw_combined_histogram(name)
    values, edges, patch = result['data']
    assert values[10] == 0.6596219539642334
    assert mean(edges) == 2.1605122581
    assert patch[5].get_height() == values[5]


@pytest.mark.parametrize('filename, energy', [
    (FILENAME_ROOT5, 0.004492828703895122),
    (FILENAME_ROOT6, 0.20740474665355302),
])
def test_lorentz_vectors(filename, energy):
    """
    Test whether vectors were loaded correctly as ``pandas.DataFrame``.
    """
    pawian_hists = PawianHists(filename)
    particle = pawian_hists.particles[0]
    assert pawian_hists.data[particle].E.mean() == energy
