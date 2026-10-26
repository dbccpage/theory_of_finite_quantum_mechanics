# The Continuum Shadow (CODA-CS)

**Author:** Jeremy H. Carroll
**License:** CC-BY-4.0 (manuscript); see LICENSE-CODE for source terms.

The historical release metadata records reserved Zenodo identifier `10.5281/zenodo.22730852`; its publication state was not independently verified during this repair.

A query constant on coarse fibres is constant on refined fibres. Equality of family observations is pointwise equality. A first-coordinate observation of Boolean pairs cannot recover the second coordinate.

The declared authority predicate additionally requires a local terminalizer and a nonempty authorized finite shadow tower. Missing a terminalizer makes this predicate false. It says nothing about uniqueness or existence of a mathematical answer: a constant-zero query remains uniquely defined. Authorized gluing of overlapping shadows is outside the proved scope.

## Replay

Start each command block from this extracted package's root, using its own Python environment (Python 3.11 or newer). The replay extra declares test, notebook, lint, and type tools. A release environment lock records the exact verified versions; these minimum dependency declarations alone are not a lock.

```console
python -m pip install -e ".[replay]"
python -m pytest code/tests -v
python -m ruff check code
python -m mypy --config-file pyproject.toml code/coda_cs_core.py code/cochain_presentation.py
```

Use `-n auto` with pytest for optional parallel execution. Collect current test counts with `python -m pytest code/tests --collect-only -q`.

Replay the notebooks from this package root:

```console
python -m nbclient jupyter_notebooks/000_a_blurry_photo_is_not_the_original.ipynb
python -m nbclient jupyter_notebooks/001_when_coarse_and_fine_agree.ipynb
python -m nbclient jupyter_notebooks/002_four_dots_that_look_the_same.ipynb
```

Enter `lean4/` so Elan selects the toolchain pinned there. This block returns to the package root:

```console
cd lean4
lake build
lake env lean coda_cs_000.lean
cd ..
```

Generate the figure and build the manuscript from the package root:

```console
python code/generate_figures.py
xelatex -interaction=nonstopmode -halt-on-error coda_cs.tex
```

The claim ledger and `docs/lean_claim_map.md` state the exact formal scope. Build success, finite tests, and general mathematical claims are separate evidence. Standard kernel axiom dependencies are reported by the entrypoint axiom queries.
