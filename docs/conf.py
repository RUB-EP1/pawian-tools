"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full list see the
documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import re
import shutil
import subprocess
import sys
from typing import Dict

if sys.version_info < (3, 8):
    from importlib_metadata import PackageNotFoundError
    from importlib_metadata import version as get_package_version
else:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as get_package_version

# -- Project information -----------------------------------------------------
project = "PawianTools"
PACKAGE = "pawian"
REPO_NAME = "PawianTools"
copyright = "2020, RUB EP1"
author = "Meike Küßner, Remco de Boer"

try:
    __VERSION = get_package_version(PACKAGE)
    version = ".".join(__VERSION.split(".")[:3])
except PackageNotFoundError:
    pass

# -- Generate API ------------------------------------------------------------
shutil.rmtree("api", ignore_errors=True)
subprocess.call(
    " ".join(
        [
            "sphinx-apidoc",
            "../src/",
            "-o api/",
            "--force",
            "--no-toc",
            "--templatedir _templates",
            "--separate",
        ]
    ),
    shell=True,  # noqa: S602
)

# -- General configuration ---------------------------------------------------
master_doc = "index.md"
source_suffix = {
    ".ipynb": "myst-nb",
    ".md": "myst-nb",
    ".rst": "restructuredtext",
}

# The master toctree document.
master_doc = "index"
modindex_common_prefix = [
    "boostcfg.",
    f"{PACKAGE}.",
]

extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_codeautolink",
    "sphinx_copybutton",
    "sphinx_thebe",
    "sphinx_togglebutton",
]
exclude_patterns = [
    "**.ipynb_checkpoints",
    "*build",
    "tests",
]

# General sphinx settings
add_module_names = False
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": ", ".join(
        [
            "__call__",
            "__eq__",
        ]
    ),
}
autodoc_member_order = "bysource"
autodoc_typehints_format = "short"
codeautolink_concat_default = True
codeautolink_global_preface = """
from IPython.display import display

"""
graphviz_output_format = "svg"
html_copy_source = True  # needed for download notebook button
html_last_updated_fmt = "%-d %B %Y"
html_show_copyright = False
html_show_sourcelink = False
html_show_sphinx = False
html_sourcelink_suffix = ""
html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": f"https://github.com/redeboer/{REPO_NAME}",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_download_button": True,
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "colab_url": "https://colab.research.google.com",
        "deepnote_url": "https://deepnote.com",
        "notebook_interface": "jupyterlab",
        "thebe": True,
        "thebelab": True,
    },
    "show_navbar_depth": 2,
    "show_toc_level": 2,
}
html_title = "PawianTools"
pygments_style = "sphinx"
todo_include_todos = False
viewcode_follow_imported_members = True

# Cross-referencing configuration
default_role = "py:obj"
primary_domain = "py"
nitpicky = True  # warn if cross-references are missing
nitpick_ignore = [
    ("py:class", "pandas.core.base.PandasObject"),
]


# Intersphinx settings
version_remapping: Dict[str, Dict[str, str]] = {
    "ipython": {
        "8.12.2": "8.12.1",
        "8.12.3": "8.12.1",
    },
}


def get_version(package_name: str) -> str:
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    constraints_path = f"../.constraints/py{python_version}.txt"
    package_name = package_name.lower()
    with open(constraints_path) as stream:
        constraints = stream.read()
    for line in constraints.split("\n"):
        line = line.split("#")[0]  # remove comments
        line = line.strip()
        line = line.lower()
        if not line.startswith(package_name):
            continue
        if not line:
            continue
        line_segments = tuple(line.split("=="))
        if len(line_segments) != 2:  # noqa: PLR2004
            continue
        _, installed_version, *_ = line_segments
        installed_version = installed_version.strip()
        remapped_versions = version_remapping.get(package_name)
        if remapped_versions is not None:
            existing_version = remapped_versions.get(installed_version)
            if existing_version is not None:
                return existing_version
        return installed_version
    return "stable"


def get_minor_version(package_name: str) -> str:
    installed_version = get_version(package_name)
    if installed_version == "stable":
        return installed_version
    matches = re.match(r"^([0-9]+\.[0-9]+).*$", installed_version)
    if matches is None:
        msg = f"Could not find documentation for {package_name} v{installed_version}"
        raise ValueError(msg)
    return matches[1]


intersphinx_mapping = {
    "awkward": ("https://awkward-array.org/doc/stable", None),
    "IPython": (f"https://ipython.readthedocs.io/en/{get_version('IPython')}", None),
    "compwa-org": ("https://compwa-org.readthedocs.io", None),
    "matplotlib": (f"https://matplotlib.org/{get_version('matplotlib')}", None),
    "numpy": (f"https://numpy.org/doc/{get_minor_version('numpy')}", None),
    "pandas": (
        f"https://pandas.pydata.org/pandas-docs/version/{get_minor_version('pandas')}",
        None,
    ),
    "python": ("https://docs.python.org/3", None),
    "uproot": ("https://uproot.readthedocs.io/en/stable", None),
}

# Settings for autosectionlabel
autosectionlabel_prefix_document = True

# Settings for copybutton
copybutton_prompt_is_regexp = True
copybutton_prompt_text = r">>> |\.\.\. "  # doctest

# Settings for linkcheck
linkcheck_anchors = False
linkcheck_ignore = [
    "https://panda-wiki.gsi.de/bin/view/PWA/PawianPwaSoftware",
]


# Settings for myst_nb
def get_nb_execution_mode() -> str:
    if "EXECUTE_NB" in os.environ:
        print("\033[93;1mWill run Jupyter notebooks!\033[0m")
        return "cache"
    return "off"


nb_execution_mode = get_nb_execution_mode()
nb_execution_timeout = -1

# Settings for myst-parser
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "dollarmath",
    "smartquotes",
    "substitution",
]
myst_update_mathjax = False

# Settings for Thebe cell output
thebe_config = {
    "repository_url": html_theme_options["repository_url"],
    "repository_branch": html_theme_options["repository_branch"],
}

# -- Visualize dependencies ---------------------------------------------------
if nb_execution_mode != "off":
    print("Generating module dependency tree...")
    subprocess.call(
        " ".join(
            [
                "HOME=.",  # in case of calling through tox
                "pydeps",
                f"../src/{PACKAGE}",
                "-o module_structure.svg",
                "--exclude *._*",  # hide private modules
                "--max-bacon=1",  # hide external dependencies
                "--noshow",
            ]
        ),
        shell=True,  # noqa: S602
    )
    if os.path.exists("module_structure.svg"):
        with open(f"api/{PACKAGE}.rst", "a") as stream:
            stream.write("\n.. image:: /module_structure.svg")
