# Python Tools for Pawian

This repository serves as a collection of Python tools to complement [Pawian](https://panda-wiki.gsi.de/foswiki/bin/view/PWA/PawianPwaSoftware). There are currently two Python packages:

1. [`pawian`](./pawian), which is a collection of Python modules that facilitate working with Pawian data
2. [`boostcfg`](./boostcfg), which is a tool to read the content of a [Boost config file](https://www.boost.org/doc/libs/1_72_0/doc/html/boost/program_options/parse_co_1_3_32_9_8_1_1_11.html)

To bring it all together, the folder [Notebooks](./Notebooks) provides some handy Jupyter notebooks.


## Installation

The easiest way to work with these packages is to use [Anaconda/Conda](https://www.anaconda.com/). This allows you to contain all Python packages you need for this project within a virtual environment that you can easily throw away or replace later on if you run into trouble. You can download Conda [here](https://www.anaconda.com/distribution/#download-section). It can be installed without admin rights on any system!

Next steps are:
1. Create a Conda environment named `pawian` and initialize it with the necessary packages (everything that follows `pawian`):
   ```bash
   conda create --name pawian python numpy uproot
   ```

2. Activate the environment using:
   ```bash
   conda activate pawian
   ```

3. Add [Conda-Forge](https://conda-forge.org/) as a channel to your Conda installation:
   ```bash
   conda config --add channels conda-forge
   conda config --set channel_priority strict
   ```

4. Now the most important step! Activate the pyPawianTools directory as a Conda ['development mode'](https://docs.conda.io/projects/conda-build/en/latest/resources/commands/conda-develop.html) directory by running [`conda develop .`] from the pyPawianTools directory. This means that all packages located within this folder are available in the Python interpreter (and Jupyter notebook!), so you can can then just run `import pawian` or `import boostcfg` from any other directory.
  (Note: `conda develop` is equivalent to [editable installs](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs) in [PyPI](https://pypi.org/), so that would be  `pip install -e .` if you prefer that.)

You can see that you are in a 'virtual environment' by typing `which python` or `python --version`—you are now using a Python interpreter of the environment.

Note that you can easily switch back with `conda deactivate`. And if you want to trash this environment, just run `conda remove --name pawian --all`.