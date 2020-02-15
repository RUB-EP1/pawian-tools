from os.path import dirname, realpath
from math import isclose
from statistics import mean
import pytest
import uproot

from pawian.qa import PawianHists, EventSet

import matplotlib.pyplot as plt

SCRIPT_DIR = dirname(realpath(__file__))
FILENAME = f'{SCRIPT_DIR}/pawianHists_epem.root'


def test_faulty_import():
    with pytest.raises(FileNotFoundError):
        PawianHists('non-existent')
    with pytest.raises(ValueError):
        PawianHists(__file__)


def test_data_model():
    pawian_hists = PawianHists(FILENAME)

    assert pawian_hists.get_uproot_histogram('non-existent') is None
    assert pawian_hists.get_uproot_histogram('_fittedFourvecs') is None

    failure = pawian_hists.get_histogram_content('non-existent')
    assert failure is None
    edges, values = pawian_hists.get_histogram_content('DataD0Dm')
    assert len(edges) == 100
    assert len(values) == 100
    assert values[40] == 3.3119699954986572

    particles = ['pion+', 'D0', 'D-']
    assert pawian_hists.particles == particles
    assert pawian_hists.data.particles == particles
    assert pawian_hists.fit.particles == particles

    assert len(pawian_hists.data.weights) == 701
    assert len(pawian_hists.fit.weights) == 7010

    assert pawian_hists.histogram_names[-4:] == [
        'FitpionpDm', 'DataD0Dm', 'MCD0Dm', 'FitD0Dm']
    assert pawian_hists.unique_histogram_names[-4:] == [
        'PhiGJ_D0_FromD0Dm', 'pionpD0', 'pionpDm', 'D0Dm']

    with pytest.raises(Exception):
        uproot_tile = uproot.open(FILENAME)
        EventSet(uproot_tile, 'wrong type')

    assert len(pawian_hists.data) == 701
    assert len(pawian_hists.fit) == 7010
    assert pawian_hists.fit.particles == list(pawian_hists.fit.keys())
    for particle, vectors in pawian_hists.data.items():
        assert len(pawian_hists.data[particle]), len(vectors)
    for item, particle in zip(pawian_hists.data, particles):
        assert item == particle
    for particle, vectors in zip(particles, pawian_hists.data.values()):
        assert isclose(
            pawian_hists.data[particle].mass.mean(), mean(vectors.mass), rel_tol=1e-07)


def test_draw_histogram():
    hists = PawianHists(FILENAME)
    assert hists.draw_histogram('non-existent') is None
    values, edges, patch = hists.draw_histogram(
        'FitThetaHeli_pionp_FrompionpD0Dm')
    assert len(values) == 100
    assert values[0] == 0.9994157552719116
    assert len(edges) == 101
    assert edges[0] == -1.0
    assert patch[-5].get_height() == values[-5]


@pytest.mark.slow
def test_draw_all_histograms():
    hists = PawianHists(FILENAME)
    hists.draw_all_histograms()
    assert len(plt.gcf().get_axes()) == 20


@pytest.mark.slow
def test_draw_combined_histogram():
    hists = PawianHists(FILENAME)
    assert hists.draw_combined_histogram('non-existent') is None
    name = 'pionpDm'
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


def test_lorentz_vectors():
    """
    Example to show to get arrays from the array of TLorentzVectors. See uproot-methods
    (particularly `here
    <https://github.com/scikit-hep/uproot-methods/blob/master/uproot_methods/classes/TLorentzVector.py>`__)
    for all available methods. **Note the last tests with added vectors!**
    """
    pawian_hists = PawianHists(FILENAME)
    pions = pawian_hists.data['pion+']
    dms = pawian_hists.data['D-']
    d0s = pawian_hists.data['D0']
    assert pions[0].__class__.__name__ == 'TLorentzVector'

    tol = 1e-07
    assert isclose(mean(pions.E), 0.19838214843147323, rel_tol=tol)
    assert isclose(mean(pions.t), 0.19838214843147323, rel_tol=tol)
    assert isclose(mean(pions.x), 0.0018455800283019288, rel_tol=tol)
    assert isclose(mean(pions.y), 0.001420538076775025, rel_tol=tol)
    assert isclose(mean(pions.z), 0.0004007101935645387, rel_tol=tol)

    assert isclose(mean(pions.mass), 0.1395702247308923, rel_tol=tol)
    assert isclose(mean(pions.mag2), 0.019479847631677847, rel_tol=tol)
    assert isclose(mean(pions.mt2), 0.037077681833282194, rel_tol=tol)
    assert isclose(mean(pions.p), 0.12978163322838815, rel_tol=tol)
    assert isclose(mean(pions.p2), 0.024227213818737492, rel_tol=tol)
    assert isclose(mean(pions.perp), 0.10969761189229306, rel_tol=tol)
    assert isclose(mean(pions.perp2), 0.017597834201604347, rel_tol=tol)
    assert isclose(mean(pions.phi), -0.04516685633166736, rel_tol=tol)
    assert isclose(mean(pions.Et), 0.1690431041350526, rel_tol=tol)

    assert isclose(mean((pions+dms+d0s).mass), 4.181807110562101, rel_tol=tol)
    assert isclose(mean((pions+dms).mass), 2.0967288718149146, rel_tol=tol)
    assert isclose(mean((pions+d0s).mass), 2.055877519379495, rel_tol=tol)
    assert isclose(mean((dms+d0s).mass), 3.9803164571933958, rel_tol=tol)
