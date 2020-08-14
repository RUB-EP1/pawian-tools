import pytest

import pawian.latex as latex


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("testpi+pion-pion+", r"test \pi^+ \pi^- \pi^+"),
        ("testpion+pion+", r"test \pi^+ \pi^+"),
        ("etaD0pion-pion+Drho0", r"\eta D^0 \pi^- \pi^+ D \rho^0"),
        ("phi", r"\phi"),
    ],
)
def test_convert(test_input, expected):
    tex_string = latex.convert(test_input)
    assert tex_string == expected
