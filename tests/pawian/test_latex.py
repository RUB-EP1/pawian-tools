# cspell:ignore Drho testpi

import pytest

from pawian import latex


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        # cspell:ignore testpion
        ("testpi+pion-pion+", r"test \pi^+ \pi^- \pi^+"),
        ("testpion+pion+", r"test \pi^+ \pi^+"),
        ("etaD0pion-pion+Drho0", r"\eta D^0 \pi^- \pi^+ D \rho^0"),
        ("phi", r"\phi"),
    ],
)
def test_convert(test_input, expected):
    tex_string = latex.convert(test_input)
    assert tex_string == expected
