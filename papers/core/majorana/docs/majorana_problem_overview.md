# The Majorana Problem — Overview & Architecture Documentation

**Package:** `coda_atlas/F004_papers/002_projection_obstruction/026_microsoft_majorana_problem`  
**Series:** Projection Obstruction 026  
**AuthorityEffect:** `None`  

---

## 1. Executive Summary

This package formalizes the **Microsoft Majorana Problem**: the realization packet gap between laboratory hardware claims (interferometric parity readout, zero-bias conductance anomalies) and discrete algebraic verification obligations ($\mathbb{F}_2$ cochain homology, Ising matrix identities).

The package provides:

1. **Mathematical Monograph**:
   - [`the_majorana_problem.md`](../the_majorana_problem.md): Core research monograph.
   - [`the_majorana_problem_claim_ledger.md`](../the_majorana_problem_claim_ledger.md): Epistemic claim ledger (`MAJ-C1` through `MAJ-C17`).
   - [`the_majorana_problem_change_log.md`](../the_majorana_problem_change_log.md): Version history from v0.1.0 to v1.0.0.
2. **Computational Engine (`code/`)**:
   - GF(2) row reduction and Gaussian elimination.
   - Residual trichotomy classification: `Exact`, `ClosedResidual`, `OpenObstruction`.
   - Parameterized tetron arrays (disk $H^1=0$, cylinder $H^1=1$, torus $H^1=2$).
   - Gray-code coset traversal for $\Phi_1$ syndrome decoding with budget capping.
   - Invariance of $L^p$ norms over binary carriers ($\|v\|_p^p = \operatorname{wt}(v)$).
3. **Formal Verification (`lean4/`)**:
   - `MajoranaCore.lean`: Machine-checked proofs under `{propext, Quot.sound}` with zero axioms.
4. **Stratified Test Suite (`code/tests/`)**:
   - `unit/`: GF(2) linear algebra, nilpotency refusal, and norm equivalence.
   - `integration/`: Tetron-array homology, code distance, and additive diagonal weights.
   - `e2e/`: Full monograph derivation walk and end-to-end receipt generation.

---

## 2. Directory Layout

```
026_microsoft_majorana_problem/
├── the_majorana_problem.md
├── the_majorana_problem_change_log.md
├── the_majorana_problem_claim_ledger.md
├── README.md
├── docs/
│   └── majorana_problem_overview.md
├── lean4/
│   └── MajoranaCore.lean
├── code/
│   ├── __init__.py
│   ├── majorana_evaluator.py
│   └── tests/
│       ├── unit/
│       │   └── test_gf2_trichotomy.py
│       ├── integration/
│       │   └── test_tetron_surface_codes.py
│       └── e2e/
│           └── test_majorana_problem_e2e.py
├── majorana/            (Legacy Python reference modules)
└── omega_majorana/      (Rust crate reference implementation)
```
