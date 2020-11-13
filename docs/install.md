# Installation

As this package is developmental, and not yet published on PyPI (see
[Milestone %1](https://gitlab.ep1.rub.de/redeboer/pyPawianTools/-/milestones/1)),
it is best to install this package in
["editable" mode](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs)
({command}`pip install -e .`), so that you can easily modify the source code,
try out new ideas, and propose your implementations through a merge request.

It is safest to work in a virtual Python environment, so that all dependencies
for this repository are safely contained. After cloning this repository and
navigating into it, you can opt to use either Conda or PyPI.

````{tabbed} Conda

The easiest way to work with these packages is to use
[Anaconda/Conda](https://www.anaconda.com). This allows you to contain all
dependencies you need for this project within a virtual environment that you
can easily throw away or replace later on if you run into trouble. You can
download Conda [here](https://www.anaconda.com/distribution/#download-section).
It can be installed without admin rights on any system!

Once you have Conda, all you need to do is:

```bash
conda env create
conda activate pypawian
```

Note that you can easily switch back with `conda deactivate`. And if you want
to trash this environment to start all over if you messed up something, just
run:

```bash
conda env create --force
```
````

````{tabbed} Python venv

If Conda is not available on your system, you can try to use Python's own
[`venv`](https://docs.python.org/3/library/venv.html). The procedure is
comparable as to Conda:

```bash
python3 -m venv ./venv      # uses your system python3
source ./venv/bin/activate
python3 -m pip install -e . # uses your venv python3
```

_Note: use `activate.csh` in case you use
[`tcsh`](https://en.wikipedia.org/wiki/Tcsh) instead of `bash`._

Now, as with Conda, the nice thing is that if you run into trouble with
conflicting packages or so, just trash the `venv` folder and start over!

````

````{tabbed} User installation

If neither Conda nor `venv` are available on your system and you have no
administrator rights, you can use a `pip` user installation.

```bash
python3 -m pip install -e . --user
```

However, _try to avoid this option_, because it may cause classes with existing
packages you installed. _See
[here](https://realpython.com/python-virtual-environments-a-primer) for why
virtual environments are important._
````

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

(See [Develop](./develop.md) for what `.[test]` means.)
