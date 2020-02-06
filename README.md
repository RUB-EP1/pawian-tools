# Python Tools for Pawian

This repository serves as a collection of Python tools to complement [Pawian](https://panda-wiki.gsi.de/foswiki/bin/view/PWA/PawianPwaSoftware). There are currently two Python packages:

1. [`pawian`](./pawian), which is a collection of Python modules that facilitate working with Pawian data
2. [`boostcfg`](./boostcfg), which is a tool to read the content of a [Boost config file](https://www.boost.org/doc/libs/1_72_0/doc/html/boost/program_options/parse_co_1_3_32_9_8_1_1_11.html)

To bring it all together, the folder [Notebooks](./Notebooks) provides some handy Jupyter notebooks.


## Installation

The easiest way to work with these packages is to use [Anaconda/Conda](https://www.anaconda.com/). This allows you to contain all dependencies you need for this project within a virtual environment that you can easily throw away or replace later on if you run into trouble. You can download Conda [here](https://www.anaconda.com/distribution/#download-section). It can be installed without admin rights on any system!

Next steps are:
1. Add [Conda-Forge](https://conda-forge.org/) as a channel to your Conda installation:
   ```bash
   conda config --add channels conda-forge
   conda config --set channel_priority strict
   ```

2. Create a Conda environment named `pawian` (or whatever you want) and initialize it with the necessary packages. The required dependencies are listed in the [`requirements.txt`](./requirements.txt) file:
   ```bash
   conda create --name pawian --file requirements.txt
   ```

3. Activate the environment using:
   ```bash
   conda activate pawian
   ```

4. Now the most important step! Activate the pyPawianTools directory as a Conda ['development mode'](https://docs.conda.io/projects/conda-build/en/latest/resources/commands/conda-develop.html) directory by running [`conda develop .`] from the pyPawianTools directory. This means that all packages located within this folder are available in the Python interpreter (and Jupyter notebook!), so you can can then just run `import pawian` or `import boostcfg` from any other directory.
   (Note: `conda develop` is equivalent to [editable installs](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs) in [PyPI](https://pypi.org/), so that would be  `pip install -e .` if you prefer that.)

You can see that you are in a 'virtual environment' by typing `which python` and/or `python --version`—you are now using a Python interpreter of the environment.

Note that you can easily switch back with `conda deactivate`. And if you want to trash this environment to start all over if you messed up something, just run `conda remove --name pawian --all`.


## Contribute

Welcome to fork and submit pull/merge requests! Alternatively, you can [request access](https://jollyj.ep1.rub.de/redeboer1/pyPawianTools/-/project_members/request_access).

### Some recommended packages for Python development

- [`pytest`](https://docs.pytest.org/en/latest/): Run `pytest` in the pyPawian folder to run all `test_*.py` files
- [`autopep8`](https://pypi.org/project/autopep8/0.8/): Auto-format your Python code
- [`pylint`](https://www.pylint.org/): Scan your code for naming conventions and proper use of Python
- [`rope`](https://github.com/python-rope/rope): Python refactoring tools
- [`sphinx`](https://www.sphinx-doc.org/): Generate documentation of your Python package
- [`doc8`](https://pypi.org/project/doc8/): A style checker for [reStructuredText](https://docutils.sourceforge.io/docs/ref/rst/introduction.html)

If you have added Conda-Forge as a channel, all can be installed in one go:

```bash
conda install --file requirements_dev.txt
```

Of course, these packages are also available through `pip install`:

```bash
pip install -r requirements_dev.txt
```