<!-- cspell:ignore coveragerc htmlcov -->

# Develop

[![GitPod](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/redeboer/PawianTools)

This repository is meant for development within the RUB EP1 group, so you're
welcome to fork and submit pull/merge requests!

## Developer extensions

As a developer, you need to install PawianTools in
["editable" mode](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs).
See [installation instructions](./install.md). You only need to do one
additional thing: install the developer packages listed under
`options.extras_requires` of the {download}`setup.cfg <../setup.cfg>`. This is
simply done with:

```bash
pip install -e .[dev]
```

(assuming you are in your [virtual environment](./install.md)).

## Conventions

- Please use
  [conventional commit messages](https://www.conventionalcommits.org/): start
  the commit with a semantic keyword (see e.g.
  [Angular](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#type)
  or
  [these examples](https://seesparkbox.com/foundry/semantic_commit_messages),
  followed by [a column](https://git-scm.com/docs/git-interpret-trailers), then
  the message. The message itself should be in imperative mood—just imagine the
  commit to give a command to the code framework. So for instance:
  `feat: add coverage report tools` or `fix: remove`.

- In the master branch, each commit should compile and be tested. In your own
  branches, it is recommended to commit frequently (WIP keyword), but squash
  those commits upon submitting a merge request.

- Try to keep test coverage high. You can test current coverage by running

  ```bash
  pytest --cov-config=.coveragerc --cov=./ --cov-report html
  ```

  from the main directory and opening the resulting file `htmlcov/index.html`.

## Documentation

Want to have a nice overview of the modules in PawianTools? If you have
followed the [installation instructions](./install.md), just do the following:

```bash
python3 -m pip install -e .[doc] # only once
cd docs
make html
```

Here, `.[doc]` specifies that you install the package _and_ install the
additional requirements defined under the `doc` section of the
{download}`setup.cfg <../setup.cfg>` file.
