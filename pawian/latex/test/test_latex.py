import pawian.latex as latex
import pytest
import matplotlib.pyplot as plt


@pytest.mark.parametrize("test_input,expected", [
    (
        "testpion+pion+",
        R"test \pi^+ \pi^+"
    ), (
        "testpion+pion+",
        R"test \pi^+ \pi^+"
    ), (
        "etaD0pion-pion+Drho0",
        R"\eta D^0 \pi^- \pi^+ D \rho^0"
    ), (
        "phi",
        R"\phi"
    ),
])
def test_convert(test_input, expected):
    tex_string = latex.convert(test_input)
    assert tex_string == expected
