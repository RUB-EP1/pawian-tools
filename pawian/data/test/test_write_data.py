from os import remove
from os.path import dirname, realpath
from numpy import allclose, isclose
from pawian.data import read_ascii


SCRIPT_DIR = dirname(realpath(__file__))
INPUT_FILE_DATA = f'{SCRIPT_DIR}/momentum_tuples_data.dat'
INPUT_FILE_MC = f'{SCRIPT_DIR}/momentum_tuples_mc.dat'
OUTPUT_FILE = f'{SCRIPT_DIR}/temp_output.dat'


def test_write_no_weights():
    frame_in = read_ascii(INPUT_FILE_MC, particles=3)
    frame_in.loc[:9].pawian.write_ascii(OUTPUT_FILE)
    frame_out = read_ascii(OUTPUT_FILE, particles=3)
    assert len(frame_out) == 10
    assert len(frame_out.columns.levels[0]) == 3
    assert len(frame_out.columns.levels[1]) == 4

    embedded_particles = frame_out.columns.droplevel(1).unique().tolist()
    tol = 1e-04
    head = frame_out.head(1)
    assert allclose(
        head[embedded_particles[0]].values.tolist()[0],
        [-0.279306, -0.175576, -0.122704, 0.378648],
        rtol=tol)
    assert allclose(
        head[embedded_particles[2]].values.tolist()[0],
        [0.0245524, -0.146873, 0.193947, 1.88553],
        rtol=tol)

    tail = frame_out.tail(1)
    assert allclose(
        tail[embedded_particles[0]].values.tolist()[0],
        [-0.12336, 0.134471, -0.0713491, 0.240563],
        rtol=tol)
    assert allclose(
        tail[embedded_particles[2]].values.tolist()[0],
        [0.609579, -0.1528, 0.363307, 2.00558],
        rtol=tol)

    remove(OUTPUT_FILE)


def test_write_with_weights():
    frame_in = read_ascii(INPUT_FILE_DATA, particles=3)
    frame_in.loc[:9].pawian.write_ascii(OUTPUT_FILE)
    frame_out = read_ascii(OUTPUT_FILE, particles=3)
    assert len(frame_out) == 10
    assert len(frame_out.columns.levels[0]) == 4
    assert len(frame_out.columns.levels[1]) == 5
    assert '' in frame_out.columns.levels[1]

    column_names = frame_out.columns.droplevel(1).unique().tolist()
    tol = 1e-06
    head = frame_out.head(1)
    assert isclose(head[column_names[-1]].values[0], 0.99407, rtol=tol)
    assert allclose(
        head[column_names[0]].values.tolist()[0],
        [-0.00357645, 0.0962561, 0.0181079, 0.170545],
        rtol=tol)
    assert allclose(
        head[column_names[2]].values.tolist()[0],
        [-0.174404, -0.719412, -0.233159, 2.0243],
        rtol=tol)

    tail = frame_out.tail(1)
    assert allclose(
        tail[column_names[0]].values.tolist()[0],
        [0.0752243, -0.034057, 0.033107, 0.1655130],
        rtol=tol)
    assert allclose(
        tail[column_names[2]].values.tolist()[0],
        [-0.710628, 0.1081589, -0.2437929, 2.01781],
        rtol=tol)

    remove(OUTPUT_FILE)
