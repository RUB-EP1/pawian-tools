import pawian.latex as latex
import pytest


@pytest.mark.parametrize("test_input,expected", [
    (
        "testpion+pion+",
        R"test\pi^{+}\pi^{+}"
    ), (
        "etapion-pion+rho0",
        R"\eta\pi^{-}\pi^{+}\rho^{0}"
    ), (
        "phi",
        R"\phi"
    ),
])
def test_convert(test_input, expected):
    assert latex.convert(test_input) == expected
