# Contribute

This repository is meant for development within the RUB EP1 group, so you're
welcome to fork and submit pull/merge requests! Alternatively, you can
[request access](https://gitlab.ep1.rub.de/redeboer/pyPawianTools/-/project_members/request_access).

## Developer extensions

As a developer, you need to install pyPawianTools in
["editable" mode](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs).
See [installation instructions](./README.md#installation). You only need to do
one additional thing: install the developer packages listed under
`options.extras_requires` of the [`setup.cfg`](./setup.cfg). This is simply done
with:

```bash
pip install -e .[dev]
```

(assuming you are in your [virtual environment](./README.md#installation)).

## Conventions

- Please use
  [conventional commit messages](https://www.conventionalcommits.org/): start
  the commit with a semantic keyword (see e.g.
  [Angular](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#type)
  or [these examples](https://seesparkbox.com/foundry/semantic_commit_messages),
  followed by [a column](https://git-scm.com/docs/git-interpret-trailers), then
  the message. The message itself should be in imperative mood—just imagine the
  commit to give a command to the code framework. So for instance:
  `feat: add coverage report tools` or `fix: remove`.
- In the master branch, each commit should compile and be tested. In your own
  branches, it is recommended to commit frequently (WIP keyword), but squash
  those commits upon submitting a merge request.
- Try to keep test coverage high. You can test current coverage by running
  ```
  pytest --cov-config=.coveragerc --cov=./ --cov-report html
  ```
  from the main directory and opening the resulting file `htmlcov/index.html`.
