# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = 'pyPawianTools'
copyright = '2020, Remco de Boer'
author = 'Remco de Boer'


# -- General configuration ---------------------------------------------------
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
exclude_patterns = ['*build', 'test', 'tests']
pygments_style = 'sphinx'

todo_include_todos = False
add_module_names = False
viewcode_follow_imported_members = True
autodoc_member_order = 'bysource'


# -- Options for HTML output -------------------------------------------------
html_theme = 'nature'
html_show_sourcelink = False
