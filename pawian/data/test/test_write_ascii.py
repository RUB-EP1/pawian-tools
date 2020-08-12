"""Test :func:`pawian.data.write_ascii`"""

from os import remove
from os.path import dirname, realpath
from pandas.testing import assert_frame_equal
import pytest

from pawian.data import read_ascii


SCRIPT_DIR = dirname(realpath(__file__))
INPUT_FILE_DATA = f"{SCRIPT_DIR}/momentum_tuples_data.dat"
INPUT_FILE_MC = f"{SCRIPT_DIR}/momentum_tuples_mc.dat"
OUTPUT_FILE = f"{SCRIPT_DIR}/temp_output.dat"


@pytest.mark.parametrize("input_file", [INPUT_FILE_DATA, INPUT_FILE_MC,])
def test_write_ascii(input_file):
    """Write, then read an ASCII file"""
    particles = ["pi+", "D0", "D-"]
    frame_in = read_ascii(input_file, particles=particles).loc[:9]
    frame_in.pawian.write_ascii(OUTPUT_FILE)
    frame_out = read_ascii(OUTPUT_FILE, particles=particles)
    assert_frame_equal(frame_in, frame_out)
    remove(OUTPUT_FILE)
