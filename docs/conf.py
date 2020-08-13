"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import shutil
import subprocess


# -- Copy example notebooks ---------------------------------------------------
print("Copy example notebook and data files")
PATH_SOURCE = "../examples"
PATH_TARGET = "usage"
FILES_TO_COPY = [
    "ASCII_Data.ipynb",
    "QA_Histograms.ipynb",
]
shutil.rmtree(PATH_TARGET, ignore_errors=True)
os.makedirs(PATH_TARGET, exist_ok=True)
for file_to_copy in FILES_TO_COPY:
    path_from = os.path.join(PATH_SOURCE, file_to_copy)
    path_to = os.path.join(PATH_TARGET, file_to_copy)
    print("  copy", path_from, "to", path_to)
    shutil.copyfile(path_from, path_to, follow_symlinks=True)

# -- Generate API skeleton ----------------------------------------------------
shutil.rmtree("api", ignore_errors=True)
subprocess.call(
    "sphinx-apidoc "
    "--force "
    "--no-toc "
    "--templatedir _templates "
    "--separate "
    "-o api/ ../boostcfg/; ",
    shell=True,
)
subprocess.call(
    "sphinx-apidoc "
    "--force "
    "--no-toc "
    "--templatedir _templates "
    "--separate "
    "-o api/ ../pawian/; ",
    shell=True,
)


# -- Project information -----------------------------------------------------
project = "pyPawianTools"
copyright = "2020, RUB EP1"
author = "Meike Küßner, Remco de Boer"


# -- Include constructors ----------------------------------------------------
def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


# -- General configuration ---------------------------------------------------
extensions = [
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.ifconfig",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]
exclude_patterns = [
    "**.ipynb_checkpoints",
    "*build",
    "test",
    "tests",
]
pygments_style = "sphinx"

todo_include_todos = False
add_module_names = False
viewcode_follow_imported_members = True
autodoc_member_order = "bysource"


# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_show_sourcelink = False

# Settings for nbsphinx
if "NBSPHINX_EXECUTE" in os.environ:
    print("\033[93;1mWill run Jupyter notebooks!\033[0m")
    nbsphinx_execute = "always"
else:
    nbsphinx_execute = "never"
nbsphinx_timeout = -1
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]
