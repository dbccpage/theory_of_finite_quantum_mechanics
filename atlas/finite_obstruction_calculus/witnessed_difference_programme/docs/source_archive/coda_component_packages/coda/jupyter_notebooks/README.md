# Worked notebook

[01_coda_walkthrough.ipynb](01_coda_walkthrough.ipynb) is the executed
companion to the unified manuscript. It has eight code cells, including
setup and figure display, with exact assertions for the mathematical
examples and the actual inherited embedding counterexample.

Open it with the Python 3.13.11 verification environment pinned in
[docs/requirements-verification.txt](../docs/requirements-verification.txt), or
run `python code/replay_notebook.py` from the package root. The replay
script uses that interpreter for a temporary kernel and shuts it down before
removing its temporary directory. Launching from the package root or this
notebook directory resolves the code and images locally.

Rebuild source cells with `python code/build_notebook.py` only when editing
the notebook recipe; then replay it to restore executed outputs. The notebook
does not mechanize the manuscript's analytic prose proofs or complete its
open targets.
