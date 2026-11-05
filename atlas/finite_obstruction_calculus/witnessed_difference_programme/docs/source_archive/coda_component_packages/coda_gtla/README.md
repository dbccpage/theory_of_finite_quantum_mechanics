# CODA-GTLA: six jobs, not one machine

Version 3.2.1 · 2026-09-28 · preprint

The manuscript connects six companion subjects through finite presentation,
span, trace, and evaluation records. Its local Lean results are the thirteen
named record/evaluator lemmas mapped in [the proof map](docs/lean_claim_map.md).
Vendored additive residual algebra is identified separately.

The Python companion computes exact rational quotient certificates, glues
coordinate sections across every actual intersection, constructs the finite
regular action of a validated groupoid, and checks a bounded two-row E2
cycle quotient. The canonical triangle example has zero E2 quotient;
a separate minimal example has a positive class. These examples do not
establish a general category or a general spectral-sequence implementation.

`AuthorityToken` is an unauthenticated declared-licence record. The strict
Boolean compatibility flag creates an explicitly labeled model record.
Subject and scope must match the input, but neither a flag nor an unkeyed
digest verifies an external signature or grants institutional permission.

## Reproduce from this package directory

```console
python -m pip install -e ".[test]"
python -m pytest code/tests -q
cd lean4
lake build
lake env lean Core.lean
lake env lean Algebra.lean
```

Open the three notebooks in `jupyter_notebooks/` from the package root or
that notebook directory. Their finite calculations are examples rather than
proofs of the cited companion theorems.

To generate the standalone routing figure:

```console
python code/generate_figures.py --output public_export/fig1_authority_descent.png
```

The final release verifier and manifests are maintained by the package
assembly process. Publication is not claimed by a successful local build.

## Release archive identity

The ZIP dated 2026-09-28 contains the current reviewed package snapshot.
Older dated ZIPs are historical release objects; their contents are not the
current working manuscript. Archives are excluded from the manifests they
contain. Publication requires author review of the intended release.
