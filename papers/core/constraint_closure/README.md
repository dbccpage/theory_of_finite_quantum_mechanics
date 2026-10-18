# 002 — Constraint Closure Toy Model and the ℓ¹ Structure of Physical Law

**Publication Class:** As-Is Toy-Model Republication (v1.2, 2026-09-11)
**Author:** Jeremy H. Carroll
**Scope:** An as-is continuation of the original constraint-closure toy model: rigorous finite linear $\ell^1$ quotient/certificate statements, Regge-calculus examples, best-effort Python and Lean evidence, and five quarantined high-energy falsification receipts. It is an exploratory finite model, not a derivation of continuous general relativity or physical law.

---

## Paper Architecture & Repository Layout

| Surface | Path | Role |
|---|---|---|
| **Canonical Paper (Markdown)** | [`constraint_closure_and_the_l1structure_of_physical_law.md`](constraint_closure_and_the_l1structure_of_physical_law.md) | **Canonical Toy-Model Manuscript (v1.2)** — Finite $\ell^1$ cochain quotients, strong LP duality, dual witnesses, Regge calculus examples, and explicit nonclaims. |
| **TeX Source** | [`constraint_closure_and_the_l1structure_of_physical_law.tex`](constraint_closure_and_the_l1structure_of_physical_law.tex) | **Generated TeX Source** — Produced from the canonical manuscript and compiled with Tectonic/XeTeX for the publication PDF. |
| **Compiled Manuscript (PDF)** | [`constraint_closure_and_the_l1structure_of_physical_law.pdf`](constraint_closure_and_the_l1structure_of_physical_law.pdf) | **Publication PDF** — Built from the generated TeX source by `public_export/build_publication_assets.py`; TeX log and page count recorded in the manifest. |
| **Plain Text Manuscript** | [`constraint_closure_and_the_l1structure_of_physical_law.txt`](constraint_closure_and_the_l1structure_of_physical_law.txt) | **Accessible Text Export** — Plain-text rendering of the canonical manuscript for deposit metadata and search. |
| **Zenodo Source Bundle** | [`constraint_closure_toy_model_zenodo_v1_2.zip`](constraint_closure_toy_model_zenodo_v1_2.zip) | **Deposit Bundle** — Paper package plus the CODA `omega_engine/` dependency snapshot needed for paper-local replay, generated text, generated TeX, generated PDF, and manifest. |
| **Publication Manifest** | [`publication_assets_manifest.json`](publication_assets_manifest.json) | **Asset Receipt** — SHA-256 digests, PDF page count, line-overflow audit, and ZIP source inventory count. |
| **Claim Ledger** | [`constraint_closure_and_the_l1structure_of_physical_law_claim_ledger.md`](constraint_closure_and_the_l1structure_of_physical_law_claim_ledger.md) | **Claim Register** — Rigorous status mapping across all theorems, definitions, and quarantined claims. |
| **Change Log** | [`constraint_closure_and_the_l1structure_of_physical_law_change_log.md`](constraint_closure_and_the_l1structure_of_physical_law_change_log.md) | **Audit Trail** — Line-by-line remediation log resolving all 14 peer review items. |
| **Code Implementation** | [`code/`](code/) | **Flat Python Layout** — Core geometric operators, LP solvers, dual witnesses, and quarantine fences. |
| **Test Suite** | [`code/tests/`](code/tests/) | Recorded suite, not re-run in this correspondence pass: 297 items, 286 passed, 11 skipped, 0 failures (`pytest -n 8`). |
| **Interactive Notebooks** | [`jupyter_notebooks/`](jupyter_notebooks/) | **Reviewer Notebooks** — Levels 1–5 demonstrating simplicial intuition through exact Boltzmann equilibria. |
| **Lean 4 Formalization** | [`lean4/`](lean4/) | **Lake Lakehouse** — Formal proofs of Hodge--Laplacian identities and fixed-carrier quotient homogeneity. |
| **Release Builder** | [`public_export/build_publication_assets.py`](public_export/build_publication_assets.py) | **Deterministic Export Script** — Rebuilds the text export, PDF, manifest, and Zenodo ZIP from checked-in package contents. |

---

## Core Mathematical Contributions

1. **Finite $\ell^1$ Cochain Quotients:** For any finite cell complex and coboundary operator $D: C^{k-1} \to C^k$, the quotient norm $\Phi_D([\omega]) = \min_\alpha \|\omega - D\alpha\|_1$ is gauge-invariant and measures true topological/differential obstructions.
2. **Exact Strong LP Duality & Certified Dual Witnesses:** If $\Phi_D([\omega]) > 0$, the dual LP yields a divergence-free cycle $w^* \in C_k$ ($D^T w^* = 0$, $\|w^*\|_\infty \le 1$) saturating the residual $\langle w^*, \omega \rangle = \Phi_D([\omega])$. This certifies non-closability by direct arithmetic.
3. **Joint Direct-Sum Constraint System:** Embedding spatial diffeomorphism and Hamiltonian scalar constraints in $C^1 \oplus C^0$ with block operator $D_{\mathrm{joint}} = \begin{pmatrix} d_0 \\ 0 \end{pmatrix}$ strictly resolves the Hamiltonian blind spot of naive coboundary encodings ($\Phi_{\mathrm{joint}} = \Phi_{d_0}(p) + \|H_\perp\|_1$).
4. **Scale-Invariant Simplicial Dihedral Angles:** Edge length scale normalization prevents ill-conditioned Gram matrices, guaranteeing exact dihedral angles $\theta_4 = \arccos(1/4)$ across all physical length scales ($10^{-8}$ to $10^8$).
5. **Exact Rational Solver:** `exact_rational_l1_quotient` operates strictly over $\mathbb{Q}$ using `fractions.Fraction`, deciding true membership in $\operatorname{im}(D)$ and resolving numerical precision regressions.
6. **Five Quarantined Speculative Falsification Receipts:** Formal receipts fencing early speculative extrapolations (Standard Model 3-2-1 hierarchy, Higgs VEV 246 GeV, SUSY saturation scale, hexagonal $\alpha$, and isolated-edge dark matter) as missing physics, category errors, or dimensional inconsistencies.

---

## Test Execution

Run the complete test suite across 8 logical CPUs:
```bash
python -m pip install -e ".[test]"
python -m pytest code/tests -n 8
```

Or replay against the checked-in lockfile:
```bash
uv run --locked --extra test python -m pytest code/tests -n 8
```

**Current Status:** Recorded suite, not re-run in this correspondence pass: 286 passed, 11 skipped, 0 failures.
