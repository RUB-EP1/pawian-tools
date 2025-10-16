"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full list see the
documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from __future__ import annotations

from sphinx_api_relink.helpers import (
    get_branch_name,
    get_execution_mode,
    get_package_version,
    pin,
    pin_minor,
    set_intersphinx_version_remapping,
)

set_intersphinx_version_remapping({
    "ipython": {
        "8.12.2": "8.12.1",
        "8.12.3": "8.12.1",
    },
})

BRANCH = get_branch_name()
ORGANIZATION = "RUB-EP1"
PACKAGE = "pawian"
REPO_NAME = "pawian-tools"
REPO_TITLE = REPO_NAME

add_module_names = False
api_github_repo = f"{ORGANIZATION}/{REPO_NAME}"
api_target_substitutions: dict[str, str | tuple[str, str]] = {
    "Axes": "matplotlib.axes.Axes",
    "BarContainer": "matplotlib.container.BarContainer",
    "Figure": "matplotlib.figure.Figure",
    "np.ndarray": "numpy.ndarray",
    "Path": "pathlib.Path",
    "pd.DataFrame": "pandas.DataFrame",
    "TH1": "uproot.behaviors.TH1.TH1",
    "TH2": "uproot.behaviors.TH2.TH2",
    "TH3": "uproot.behaviors.TH3.TH3",
}
author = ""
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": ", ".join([  # noqa: FLY002
        "__call__",
        "__eq__",
    ]),
}
autodoc_member_order = "bysource"
autodoc_typehints_format = "short"
autosectionlabel_prefix_document = True
codeautolink_concat_default = True
codeautolink_global_preface = """
from IPython.display import display
"""
copybutton_prompt_is_regexp = True
copybutton_prompt_text = r">>> |\.\.\. "  # doctest
copyright = "2020, RUB EP1"
default_role = "py:obj"
exclude_patterns = [
    "**.ipynb_checkpoints",
    "*build",
    "tests",
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
    "sphinx_api_relink",
    "sphinx_codeautolink",
    "sphinx_copybutton",
    "sphinx_thebe",
    "sphinx_togglebutton",
]
generate_apidoc_package_path = [
    f"../src/{PACKAGE}",
    "../src/boostcfg",
]
graphviz_output_format = "svg"
html_copy_source = True  # needed for download notebook button
html_last_updated_fmt = "%-d %B %Y"
html_logo = (
    "https://gitlab.ep1.rub.de/uploads/-/system/project/avatar/7/pawian-logo.jpg"
)
html_show_copyright = False
html_show_sourcelink = False
html_show_sphinx = False
html_sourcelink_suffix = ""
html_theme = "sphinx_book_theme"
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": f"https://github.com/{ORGANIZATION}/{REPO_NAME}",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Launch on Binder",
            "url": f"https://mybinder.org/v2/gh/{ORGANIZATION}/{REPO_NAME}/{BRANCH}?filepath=docs",
            "icon": "https://mybinder.readthedocs.io/en/latest/_static/favicon.png",
            "type": "url",
        },
        {
            "name": "Launch on Colaboratory",
            "url": f"https://colab.research.google.com/github/{ORGANIZATION}/{REPO_NAME}/blob/{BRANCH}",
            "icon": "https://avatars.githubusercontent.com/u/33467679?s=100",
            "type": "url",
        },
    ],
    "logo": {"text": REPO_TITLE},
    "repository_url": f"https://github.com/{ORGANIZATION}/{REPO_NAME}",
    "repository_branch": BRANCH,
    "path_to_docs": "docs",
    "use_download_button": True,
    "use_edit_page_button": True,
    "use_issues_button": True,
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
html_title = REPO_TITLE
intersphinx_mapping = {
    "awkward": ("https://awkward-array.org/doc/stable", None),
    "IPython": (f"https://ipython.readthedocs.io/en/{pin('IPython')}", None),
    "compwa": ("https://compwa.github.io", None),
    "matplotlib": (f"https://matplotlib.org/{pin('matplotlib')}", None),
    "numpy": (f"https://numpy.org/doc/{pin_minor('numpy')}", None),
    "pandas": (
        f"https://pandas.pydata.org/pandas-docs/version/{pin_minor('pandas')}",
        None,
    ),
    "python": ("https://docs.python.org/3", None),
    "uproot": ("https://uproot.readthedocs.io/en/stable", None),
}
linkcheck_anchors = False
linkcheck_ignore = [
    "https://panda-wiki.gsi.de/bin/view/PWA/PawianPwaSoftware",
    "https://www.gnu.org",
]
master_doc = "index"
modindex_common_prefix = [
    "boostcfg.",
    f"{PACKAGE}.",
]
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "dollarmath",
    "smartquotes",
    "substitution",
]
myst_heading_anchors = 2
myst_update_mathjax = False
nb_execution_mode = get_execution_mode()
nb_execution_show_tb = True
nb_execution_timeout = -1
nb_output_stderr = "remove"
nitpick_ignore = [
    ("py:class", "PandasObject"),
]
nitpicky = True
primary_domain = "py"
project = REPO_TITLE
pygments_style = "sphinx"
release = get_package_version("pawian-tools")
source_suffix = {
    ".ipynb": "myst-nb",
    ".md": "myst-nb",
    ".rst": "restructuredtext",
}
thebe_config = {
    "repository_url": html_theme_options["repository_url"],
    "repository_branch": html_theme_options["repository_branch"],
}
version = get_package_version("pawian-tools")
