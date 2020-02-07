"""
Functions that help converting strings to LaTeX syntax.
"""


__author__ = "Meike Küßner, Remco de Boer"
__institution__ = "Ruhr-Universität Bochum"


__all__ = ["convert"]


__CONVERT_DICT = {
    "+": "^{+}",
    "-": "^{-}",
    "0": "^{0}",
    "pion": R"\pi",
    "etaprime": R"\eta'",
    "eta": R"\eta",
    "phi": R"\phi",
    "rho": R"\rho",
    "pbar": R"\bar{p}",
    "nbar": R"\bar{n}"
}


def convert(phrase):
    """Convert particle names to Latex code which can be used for plot labels etc."""
    for key, value in __CONVERT_DICT.items():
        phrase = phrase.replace(key, value)
    return phrase
