# From Pre-Genesis to MSS-N

[Read the paper](paper.md). The PDF, standalone TeX and dated release ZIP are
generated from this manuscript. Version 1.0.0, dated 2026-10-09, is an author review draft.

The paper consolidates Pre-Genesis trial records, the S(n) presentation account,
the Minimal Symbol System account and the corrected architectural walkthrough.
Historical source bytes and current imported proofs are pinned in
[the source manifest](manifests/imported_sources.json).
It is an entry companion to the WDP monograph; follow the
[reading route](docs/monograph_route.md) from admission and reports to repair,
then to the monograph's conditional finite-QM constructions.

From this folder, with Python 3.12, Lean 4.33.0, Rust and Cargo installed:

```sh
python -m pip install ".[dev]"
python code/verify_package.py
python -m pytest code/tests
cd lean4
lake build
cd ..
python tools/replay_full_axiom_census.py
python code/reproduce.py --native
python scripts/execute_notebook.py
python verify_deposit.py --lean
```

The mathematical kernel uses Python's standard library and a dependency-free
Rust crate. Native reproduction runs Rust tests and keeps Rust build products
in a temporary directory. Tests require pytest. The notebook requires nbformat and nbclient.
The Lean companion constructs quotient homology groups and induced maps.
Its integral class-encoding theorem is exercised by the shared runtime replay,
including negative and zero moduli and a nonzero order-two class.
The graph companion identifies integral zeroth homology with the free abelian
group on connected components. The finite replay includes component coordinates,
with empty graphs, loops and repeated edges.
The current derivations add explicit reduced-H0 and triangle-H1 isomorphisms,
constructive graph-edge retractions, cochain duality and canonical free-word
reduction. Exact rational joint mixtures obey the oriented CHSH bound.
Continuous-loop comparison for the two-circle wedge remains an open formal
obligation. See [the theorem map](docs/mechanization.md) for precise scope.
The grammar recognizer is the pinned finite EBNF recognizer, not a semantic
evaluator. See [the reproduction guide](docs/000_quick_start.md) for scope.

No public deposit or author approval is implied by a successful local check.
