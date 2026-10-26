# Omniversal Re-Presentation (CODA-OR)

**Subtitle:** Re-Presentations Transport Rules  
**Version:** 1.0.1 (v1.0.1 Pre-Print)  
**Date:** 2026-09-28  
**Zenodo Record:** <https://zenodo.org/records/23025162>  
**DOI:** [10.5281/zenodo.23025162](https://doi.org/10.5281/zenodo.23025162)  

This package contains the canonical theorem paper, production Python module, non-vacuous regression and mutation test suite, pedagogical Jupyter notebooks, standalone exact rational cochain solver, and a Lean 4 kernel for declared finite comparison records.

```console
python -m pip install ".[test,notebooks]"
python -m pytest code/tests -v
```

The implementation formalizes:
1. **Overlap Compatibility & Pair Gluing (OR-D1, OR-T1–OR-T3):** Compatible pairs glue uniquely to a triple; incompatible overlaps refuse gluing.
2. **Four-Case Square Defect Classification (OR-D2, OR-T4):** Defect $\delta \in C_1$ classified into `StrictCommute`, `WeakCommuteCertified` (exact repair $d_0 \alpha = \delta$), `H1DiagramTear` (closed residual), and `OpenDiagramObstruction` ($d_1 \delta \neq 0$). Exact repairs are closed because $d_1 d_0 = 0$.
3. **Comparison Object Standing & Non-Creation Firewall (OR-D3, OR-T5–OR-T6):** Sieve targets and arrow targets must strictly bind to the comparison object ID. Empty support sieve forces hard refusal `R_empty_support`. Envelope membership does not confer authority.
4. **Limit Candidate Standing & Omniversal Non-Assumption (OR-D4, OR-T7–OR-T8):** Limits require declared local terminalizers and valid component legs. A global omniversal object is not assumed.
5. **Standalone Exact Cochain Solver:** `LinearRepairProblem` in vendored `cochain_presentation.py` solving exact rational $\ell^1$ quotient distances.
6. **Zero Floats Invariant & Defensive Immutability:** Strictly exact rational arithmetic (`sympy.Rational` / `fractions.Fraction`). Floats, booleans, and symbols in matrix positions strictly raise `TypeError`. `EnrichedEnvironment` and `DiagramDefectResult` store immutable matrix snapshots (`sympy.ImmutableMatrix`).

Run these commands from the detached package root. Formal builds use `lean4/lean-toolchain` (`leanprover/lean4:v4.34.0-rc1`). OR-T9 is a scope fence and OR-T10 a declared policy; neither is an additional mechanized theorem.
