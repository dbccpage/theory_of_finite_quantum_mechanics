# Finite Obstruction Calculus: Exact Quotient Diagnostics, Dual Witnesses, Two-Stage Coherence, and Transport (CODA-FOC)

**Author:** Jeremy H. Carroll
**Version:** 3.2.1 · **Date:** 2026-09-28 · preprint
**License:** CC-BY-4.0 for the manuscript; see `LICENSE-CODE` for code.
**Zenodo Record:** <https://zenodo.org/records/23025087>  
**DOI:** [10.5281/zenodo.23025087](https://doi.org/10.5281/zenodo.23025087)  

Start with [the manuscript](coda_foc.md), [claim ledger](coda_foc_claim_ledger.md),
and [formal claim map](docs/lean_claim_map.md).

## Reproduce the finite computations

The verification environment uses Python 3.13.11. From this extracted package:

```console
uv sync --locked --extra verification --python 3.13
uv run --locked --extra verification python -m pytest code/tests/test_finite_obstruction.py -q
uv run --locked --extra verification python -m pytest code/tests/test_foc_conformance.py -q
uv run --locked --extra verification python -m pytest code/tests/test_review_regressions.py -q
uv run --locked --extra verification python code/generate_figures.py
```

The mutation and figure checks are separate named files in `code/tests/`.
Run test files sequentially. [The verification requirements](docs/requirements-verification.txt)
also record the tested tool versions. Core calculations use exact rational
arithmetic; floating inputs are rejected at the computational boundary.

For interactive notebooks, the platform launchers in `public_export/` use the
locked verification and notebook extras. The three notebooks resolve the local
`code/finite_obstruction.py` from either the package or notebook directory.

## Mathematical scope

The packet is a finite real cochain complex with `d1*d0 = 0`, a second-stage
repair map, and positive coordinate weights. The manuscript develops weighted
ℓ¹ quotient distances Φ₁ and Γ₂, exact dual witnesses, a three-case diagnostic,
direct sums, and operator-norm transport bounds. Python implements rational
instances and checks dual coordinate bounds `abs(z[i]) <= w[i]` and annihilation
of the full repair subspace.

`NonclosedDefect` means the input's next defect survives second-stage repair;
the complex law still holds. Growth under transport is permitted up to the
stated operator-norm bound.

`FiniteRepairRegistry` replays every move in an explicit finite list and binds
the packet, defect, scope, evaluator, budget and move outcomes. This establishes
only exhaustion of that list. It supplies no external authorization and makes
no claim that every possible repair has been listed.

## Formal scope and manuscript build

The exact Lean toolchain and Mathlib revision are pinned in `lean4/`. After
preparing those dependencies, run `lake build` from that directory. Lean
formalizes algebraic separation and declared logical kernels. Instantiating the
abstract Φ–Γ kernel with the full numerical weighted LP construction remains
outside the formalized scope. The finite Python certificates do not close that
formalization gap.

The standalone TeX source uses XeLaTeX; run twice from the package root:

```console
xelatex -interaction=nonstopmode -halt-on-error coda_foc.tex
xelatex -interaction=nonstopmode -halt-on-error coda_foc.tex
```

`MANIFEST.sha256` lists the canonical checksums for all source files packaged within the release ZIP. `SHA256SUMS` is the release manifest covering all release assets including `MANIFEST.sha256`. Release ZIP files are excluded from their contained manifests.
