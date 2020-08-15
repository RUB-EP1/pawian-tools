# cspell:ignore mathrm

"""Functions that help converting strings to LaTeX syntax."""


import re  # regex


__PARTICLES = ["D", "pi", "pion", "eta", "rho"]


__LATEX_COMMANDS = ["pion", "eta", "rho", "pi", "theta", "Theta", "phi", "Phi"]


__OTHER_REPLACEMENTS = {
    r"(GJ|Heli)_": r"_{\1}: ",
    r"_From": r"\\mathrm{~from~}",
    r"\\pion": r"\\pi",
    f"({'|'.join(__PARTICLES)}) *[m-]": r"\1^- ",
    f"({'|'.join(__PARTICLES)}) *[p+]": r"\1^+ ",
    f"({'|'.join(__PARTICLES)}) *0": r"\1^0 ",
    r"[ ]+([_\^\{\[])": r"\1",
    r"(^\s+|\s+$)": "",  # leading or trailing spaces
    r"\s\s+": " ",  # double spaces
}


def convert(phrase):
    """Convert particle names to Latex code which can be used for plot labels etc."""
    phrase = re.sub(f"({'|'.join(__LATEX_COMMANDS)})", r" \\\1 ", phrase)
    for pattern, repl in __OTHER_REPLACEMENTS.items():
        phrase = re.sub(pattern, repl, phrase)
    return phrase
