"""Test :func:`pawian.data.read_pawian_hists`"""

from os.path import dirname, realpath
import pytest
from pawian.data import read_pawian_hists

import pawian.qa


QA_TEST_DIR = dirname(realpath(pawian.qa.__file__))


@pytest.mark.parametrize('input_file, has_weights, particles, energy', [
    (
        f'{QA_TEST_DIR}/test/pawianHists_ROOT5_SigmaKp.root',
        False,
        ['Sigmaplus', 'antiproton', 'K0'],
        0.004492828703895122,
    ),
    (
        f'{QA_TEST_DIR}/test/pawianHists_ROOT6_DDpi.root',
        True,
        ['pi+', 'D0', 'D-'],
        0.20740474665355302,
    ),
])
def test_read_pawian_hists(input_file, has_weights, particles, energy):
    """Test loading pawianHists.root file"""
    data = read_pawian_hists(input_file, type_name='data')
    fit = read_pawian_hists(input_file, type_name='fit')

    assert fit.pawian.has_weights
    assert data.pawian.has_weights == has_weights

    assert data.pawian.particles == particles

    assert data[particles[0]].pawian.energy.mean() == energy


def test_read_pawian_hists_exception():
    """Test whether expected exceptions are raised"""
    with pytest.raises(Exception):
        read_pawian_hists(
            f'{QA_TEST_DIR}/test/pawianHists_ROOT6_DDpi.root', type_name='wrong')
