# `code/`directory (compatibility surface)

This folder exists for notebook path compatibility. It **must not** be placed
on`sys.path`as a parent of a package named`code`when the package root
is the CWD — that shadows the Python stdlib`code`module and breaks pytest.

**Canonical import surface:**`gs001_lib/`- Tests: use package-root`conftest.py`(prefers`*_lib`).

- Notebooks: insert the **module directory** (this folder or`*_lib`), not the package root alone.
- Prefer`python -m pytest tests -q` from package root after conftest is present.