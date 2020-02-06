# Documentation folder

If you are developing [pyPawianTools](../), it is useful to check the structure of your modules from time to time and to have a look at how your [docstrings](https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring) are rendered.

Python documentation can be generated with with [Sphinx](https://www.sphinx-doc.org/). How to do it?

1. Install all required packages by running either `conda install --file requirements.txt` or `pip install -r requirements.txt` from this folder.
2. Run `make html`
3. Open the file `_build/html/index.html` in a web browser.

If you add more (sub-)modules, you'll have to modify the rst file that corresponds to your module, for instance, [`boostcfg.rst`](./boostcfg.rst). The syntax you should follow there (and in your Python docstrings) is that of [reStructuredText](https://docutils.sourceforge.io/docs/ref/rst/introduction.html).

As a trick, you can run
```bash
sphinx-apidoc -f -M -o docs .
```
from the pyPawianTools folder to generate these rst files for all (sub-)modules automatically, but note that this will overwrite the existing files!