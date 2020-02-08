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


def test_histograms():
    pawian_hists = PawianHists(FILENAME)

    assert pawian_hists.get_histogram('non-existent') is None
    assert pawian_hists.get_histogram('_fittedFourvecs') is None

    hist = pawian_hists.get_histogram('DataD0Dm')
    assert len(hist[0]) == 100
    assert hist[0][40] == 3.3119699954986572

    particles = ['pion+', 'D0', 'D-']
    assert pawian_hists.particles == particles
    assert pawian_hists.data.particles == particles
    assert pawian_hists.fit.particles == particles
    assert pawian_hists.fit.keys() == particles

    assert len(pawian_hists.data.weights) == 701
    assert len(pawian_hists.fit.weights) == 7010

    assert pawian_hists.histogram_names[-4:] == [
        'FitpionpDm', 'DataD0Dm', 'MCD0Dm', 'FitD0Dm']

    with pytest.raises(Exception):
        uproot_tile = uproot.open(FILENAME)
        EventSet(uproot_tile, 'wrong type')


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
