[![pipeline status](https://gitlab.ep1.rub.de/redeboer/pyPawianTools/badges/master/pipeline.svg)](https://gitlab.ep1.rub.de/redeboer/pyPawianTools/commits/master)
[![coverage report](https://gitlab.ep1.rub.de/redeboer/pyPawianTools/badges/master/coverage.svg)](https://gitlab.ep1.rub.de/redeboer/pyPawianTools/commits/master)

# Python Tools for Pawian

This repository serves as a collection of Python tools to complement
[Pawian](https://panda-wiki.gsi.de/foswiki/bin/view/PWA/PawianPwaSoftware).
There are currently two Python packages:

1. [`pawian`](./pawian), which is a collection of Python modules that facilitate
   working with Pawian data
2. [`boostcfg`](./boostcfg), which is a tool to read the content of a
   [Boost config file](https://www.boost.org/doc/libs/1_72_0/doc/html/boost/program_options/parse_co_1_3_32_9_8_1_1_11.html)

To bring it all together, the folder [Notebooks](./Notebooks) provides some
handy Jupyter notebooks.

## Installation

As this package is developmental, and not yet published on PyPI (see Milestone
%1), it is best to install this package in
["editable" mode](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs)
(`pip install -e .`), so that you can easily modify the source code, try out new
ideas, and proposer your implementations through a merge request.

It is safest to work in a virtual Python environment, so that all dependencies
for this repository are installed there. After cloning this repository and
navigating into it, you can opt to use either Conda or PyPI.

### Option 1: Conda

The easiest way to work with these packages is to use
[Anaconda/Conda](https://www.anaconda.com/). This allows you to contain all
dependencies you need for this project within a virtual environment that you can
easily throw away or replace later on if you run into trouble. You can download
Conda [here](https://www.anaconda.com/distribution/#download-section). It can be
installed without admin rights on any system!

Once you have Conda, all you need to do is:

```bash
conda env create
conda activate pawian
pip install -e .
```

Note that you can easily switch back with `conda deactivate`. And if you want to
trash this environment to start all over if you messed up something, just run
`conda remove --name pawian --all`.

### Option 2: Python's `venv`

If Conda is not available on your system, you can try to use Python's own
[`venv`](https://docs.python.org/3/library/venv.html). The procedure is
comparable as to [Conda](#Option-1:-Conda):

```bash
python3 -m venv ./venv      # uses your system python3
source ./venv/bin/activate
python3 -m pip install -e . # uses your venv python3
```

_Note: use `activate.csh` in case you use
[`tcsh`](https://en.wikipedia.org/wiki/Tcsh) instead of `bash`._

Now, as with Conda, the nice thing is that if you run into trouble with
conflicting packages or so, just trash the `venv` folder and start over!

### Option 3: `pip` user installation

If neither [Conda](#Option-1:-Conda) nor [`venv`](#Option-2:-Python's-venv) are
available on your system and you have no administrator rights, you can use a
`pip` user installation.

```bash
python3 -m pip install -e . --user
```

However, _try to avoid this option_, because it may cause classes with existing
packages you installed. _See
[here](https://realpython.com/python-virtual-environments-a-primer/) for why
virtual environments are important._

## Testing

To check whether your [installation](#installation) went correctly, run:

```bash
python3 -c 'import pawian'
```

For more thorough testing of the framework, you can run

```bash
python3 -m pip install -e .[test] # only once
pytest
```

(See [Documentation](#documentation) for what `.[test]` means.)

## Documentation

Want to have a nice overview of the modules in pyPawianTools? If you have
followed the [installation instructions](#installation), just do the following:

```bash
python3 -m pip install -e .[doc] # only once
cd docs
make html
```

Here, `.[doc]` specifies that you install the package _and_ install the
additional requirements defined under the `doc` section of the
[`setup.cfg`](./setup.cfg) file.

## Contribute

See [`CONTRIBUTING.md`](./CONTRIBUTING.md)
