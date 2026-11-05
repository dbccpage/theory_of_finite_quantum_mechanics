# `code/` directory (compatibility surface)

This folder exists for notebook path compatibility. It **must not** be placed
on `sys.path` as a parent of a package named `code` when the package root
is the CWD — that shadows the Python stdlib `code` module and breaks pytest.

**Canonical import surface:** the flat modules in this directory, including
`coord_additivity.py`.

- Tests: `code/tests/conftest.py` inserts this module directory explicitly.
- Notebooks: insert this **module directory**, not the package root alone.
- Run `uv run --frozen --extra dev python -m pytest code/tests -q -p no:debugging`
  from the package root; add `--cov=code --cov-branch --cov-fail-under=95`
  for the release coverage gate.
