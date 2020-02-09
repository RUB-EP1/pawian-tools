[![pipeline status](https://jollyj.ep1.rub.de/redeboer/pyPawianTools/badges/master/pipeline.svg)](https://jollyj.ep1.rub.de/redeboer/pyPawianTools/commits/master)
[![coverage report](https://jollyj.ep1.rub.de/redeboer/pyPawianTools/badges/master/coverage.svg)](https://jollyj.ep1.rub.de/redeboer/pyPawianTools/commits/master)

# Python Tools for Pawian

This repository serves as a collection of Python tools to complement [Pawian](https://panda-wiki.gsi.de/foswiki/bin/view/PWA/PawianPwaSoftware). There are currently two Python packages:

1. [`pawian`](./pawian), which is a collection of Python modules that facilitate working with Pawian data
2. [`boostcfg`](./boostcfg), which is a tool to read the content of a [Boost config file](https://www.boost.org/doc/libs/1_72_0/doc/html/boost/program_options/parse_co_1_3_32_9_8_1_1_11.html)

To bring it all together, the folder [Notebooks](./Notebooks) provides some handy Jupyter notebooks.


## Installation

As this repository is developmental (see [Contribute](#contribute)), there is no setup procedure. Instead, it is easiest to work in a virtual Python environment and have this repository added as a development directory. In that sense, the instructions here are useful in general if you want to experiment with Python development! Now, after cloning this repository and moving into it, you can opt to use either Conda or PyPI.

### Option 1: Conda
The easiest way to work with these packages is to use [Anaconda/Conda](https://www.anaconda.com/). This allows you to contain all dependencies you need for this project within a virtual environment that you can easily throw away or replace later on if you run into trouble. You can download Conda [here](https://www.anaconda.com/distribution/#download-section). It can be installed without admin rights on any system!

Next steps are:
1. Add [Conda-Forge](https://conda-forge.org/) as a channel to your Conda installation:
   ```
   conda config --add channels conda-forge
   conda config --set channel_priority strict
   ```

2. Create a Conda environment named `pawian` (or whatever you want) and initialize it with the necessary packages. The required dependencies are listed in the [`requirements.txt`](./requirements.txt) file, apart from Python itself:
   ```
   conda create --name pawian python --file requirements.txt
   ```

3. Activate the environment using:
   ```
   conda activate pawian
   ```
   You can see that you are in a 'virtual environment' by typing `which python` and/or `python --version`—you are now using a Python interpreter of the environment.

4. Now the most important step! Activate the pyPawianTools directory as a Conda ['development mode'](https://docs.conda.io/projects/conda-build/en/latest/resources/commands/conda-develop.html) directory by running `conda develop .` from the pyPawianTools directory. This means that all packages located within this folder are available in the Python interpreter (and Jupyter notebook!), so you can can then just run `import pawian` or `import boostcfg` from any other directory.

Note that you can easily switch back with `conda deactivate`. And if you want to trash this environment to start all over if you messed up something, just run `conda remove --name pawian --all`.

### Option 2: Python Package Index
If Conda is not available on your system, you can go the conventional route: using [PyPI](https://pypi.org/) (`pip`). In order to make the pyPawianTools packages known to your Python interpreter, you will have to use [`virtualenvwrapper`](https://virtualenvwrapper.readthedocs.io/en/latest/) (just like `conda develop`). Again, it is safest if you do this by working in a virtual environment. So before you get going, make sure you have Python3's [`venv`](https://docs.python.org/3/library/venv.html) installed on your system.

Now, let's go:
1. Create a virtual environment (and call it `venv`):
   ```
   python3 -m venv venv
   ```
   Note that we append `python3 -m` to ensure that we use the `venv` module of Python3.

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
   If this went correctly, you should see `(venv)` on your command line and `which python3` should point to `venv/bin`.

3. Set the directory of this repository as a development path. For this you need to install and activate `virtualenvwrapper`, then you can use the command `add2virtualenv`:
   ```
   python3 -m pip install virtualenvwrapper
   source venv/bin/virtualenvwrapper.shF
   add2virtualenv .
   ```
   where we assume you run `add2virtualenv` from the pyPawianTools directory. You can use `add2virtualenv -d .` to unregister the path again.

Now, as with Conda, the nice thing is that if you run into trouble with conflicting packages or so, just trash the `venv` folder and start over!


## Documentation

Want to have a nice overview of the modules in pyPawianTools? If you have followed the [installation instructions](#installation), just do the following:

1. Navigate into the [`docs`](./docs) folder.
2. Install the required packages (either `conda install --file requirements.txt` or `pip install -r requirements.txt`).
3. Run `make html` and/or `make pdflatex`.
4. See the output in the `_build` folder!


## Contribute

See [`CONTRIBUTING.md`](./CONTRIBUTING.md)