## Contribute

This repository is meant for development within the RUB EP1 group, so you're welcome to fork and submit pull/merge requests! Alternatively, you can [request access](https://jollyj.ep1.rub.de/redeboer1/pyPawianTools/-/project_members/request_access).

### Conventions
* Please use [conventional commit messages](https://www.conventionalcommits.org/): start the commit with a semantic keyword (see e.g. [Angular](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#type) or [these examples](https://seesparkbox.com/foundry/semantic_commit_messages), followed by [a column](https://git-scm.com/docs/git-interpret-trailers), then the message. The message itself should be in imperative mood—just imagine the commit to give a command to the code framework. So for instance: `feat: add coverage report tools` or `fix: remove `.
* In the master branch, each commit should compile and be tested. In your own branches, it is recommended to commit frequently (WIP keyword), but squash those commits upon submitting a merge request.
* Try to keep test coverage high. You can test current coverage by running
  ```
  pytest --cov-config=.coveragerc --cov=./ --cov-report html
  ```
  from the main directory and opening the resulting file `htmlcov/index.html`.


### Some recommended packages for Python development
- [`pytest`](https://docs.pytest.org/en/latest/): Run `pytest` in the pyPawian folder to run all `test_*.py` files
- [`autopep8`](https://pypi.org/project/autopep8/0.8/): Auto-format your Python code
- [`pylint`](https://www.pylint.org/): Scan your code for naming conventions and proper use of Python
- [`rope`](https://github.com/python-rope/rope): Python refactoring tools
- [`sphinx`](https://www.sphinx-doc.org/): Generate documentation of your Python package
- [`doc8`](https://pypi.org/project/doc8/): A style checker for [reStructuredText](https://docutils.sourceforge.io/docs/ref/rst/introduction.html)

If you have added Conda-Forge as a channel, all can be installed in one go:

```
conda install --file requirements_dev.txt
```

Of course, these packages are also available through `pip install`:

```
pip install -r requirements_dev.txt
```