from os import remove
from os.path import dirname, realpath

import pytest
from pandas.testing import assert_frame_equal

import pawian
from pawian.data import read_ascii

PAWIAN_DIR = dirname(realpath(pawian.__file__))
SAMPLE_DIR = f"{PAWIAN_DIR}/samples"
INPUT_FILE_DATA = f"{SAMPLE_DIR}/momentum_tuples_data.dat"
INPUT_FILE_MC = f"{SAMPLE_DIR}/momentum_tuples_mc.dat"
OUTPUT_FILE = "temp_output.dat"


@pytest.mark.parametrize(
    "input_file",
    [
        INPUT_FILE_DATA,
        INPUT_FILE_MC,
    ],
)
def test_write_ascii(input_file):
    """Write, then read an ASCII file."""
    particles = ["pi+", "D0", "D-"]
    frame_in = read_ascii(input_file, particles=particles).loc[:9]
    frame_in.pwa.write_ascii(OUTPUT_FILE)  # type: ignore[attr-defined]
    frame_out = read_ascii(OUTPUT_FILE, particles=particles)
    assert_frame_equal(frame_in, frame_out)
    remove(OUTPUT_FILE)
