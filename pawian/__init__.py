"""
A collection of Python tools that facilitate working with
`Pawian <https://panda-wiki.gsi.de/foswiki/bin/view/PWA/PawianPwaSoftware>`__
output. Note that the tools here **are specific to Pawian**. Any tools that are
more general in usage should be extracted to a separate module.
"""

__author__ = "Meike Küßner, Remco de Boer"
__institution__ = "Ruhr-Universität Bochum"


__all__ = ["data", "latex", "qa"]


from . import data
from . import qa
from . import latex
