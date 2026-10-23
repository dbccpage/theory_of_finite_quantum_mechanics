# SO(k)-Invariant Gauge Rigidity for Declared Euclidean Stalks (GS-002)

**Canonical Title:** *SO(k)-Invariant Gauge Rigidity for Declared Euclidean Stalks: Local $\ell^2$ Selection and Outer $\ell^1$ Aggregation*  
**Package:** `008_so_k_invariant_gauge_classification`  
**Release Version:** `2.0.0` (Date: 2026-09-21)  
**Preprint:** Candidate for Zenodo Record [20683681](https://zenodo.org/records/20683681) (v2.0.0 upgrade)

---

## 1. Overview

Within the framework of cohomological obstruction theory on finite cell complexes, this package supplies scoped Lean and computational evidence for local gauge rigidity and finite obstruction kernels. The outer network form remains a conditional, explicitly declared aggregation rule:

1. **Local Gauge Rigidity (Theorem 3.1):** For stalk dimension $k \ge 2$, every absolutely homogeneous, faithful gauge on a declared Euclidean space $\mathbb{R}^k$ that is invariant under the standard continuous rotational group action $\mathrm{SO}(k)$ is uniquely determined up to scale as $j(x) = c \|x\|_2$ ($c > 0$).
2. **Separation of Local and Outer Geometry (Theorem 3.2):** Conditional on the strong edgewise declaration $J(\omega)=\sum_e j_e(\omega_e)$, substituting the local rigidity result yields the weighted mixed norm $\|\eta\|_{1,2,w} = \sum_{e \in E} w_e \|\eta_e\|_2$. This outer sum is definitional aggregation, not a consequence of rotational symmetry alone.
3. **Finite-Dimensional Quotient Duality (Theorem 4.2):** The weighted $\ell^1(E; \ell^2)$ quotient obstruction norm under flat repair fields $\alpha \in C^0(G; \mathbb{R}^k)$ admits an exact zero-gap second-order cone programming (SOCP) dual over divergence-free circulations $z \in C_1(G; \mathbb{R}^k)$ with edgewise Euclidean ball bounds $\|z_e\|_2 \le w_e$.
4. **Single-Cycle Closed-Form Formula (Lemma 5.1 and weighted refinement):** On any simple directed cycle graph $C$ with strictly positive edge weights $w_e > 0$, the quotient infimum evaluates in closed form to $\Phi_{j,w}([\omega]) = (\min_{e \in C} w_e) j(S(\omega))$, where $S(\omega)$ is the total cycle circulation vector.
5. **Normalized Triangle Separation (Theorem 5.2):** Under normalized unit weights on a directed 3-cycle, the uniform circulation $S(\omega) = (1, 1)$ yields quotient value $2$ under coordinate-separable $\ell^1$ and $\sqrt{2}$ under $\mathrm{SO}(2)$-invariant Euclidean gauge, proving observer-class geometry dependence on exact finite cochains.
6. **Mixed Closure Invariant Bound (Theorem 6.1):** On a 2-cell complex with nilpotent boundary operators $d_1 d_0 = 0$, the 2-cell closure diagnostic satisfies $\Gamma_{2,1,u}([h]) \le \|d_1\|_{(1,2,c) \to (1,2,u)} \Phi_{2,1,c}([h])$.

Theorem 2.1 is reproduced as imported evidence from the companion
M-compatible gauge paper. It is not locally proved or mechanized in this
package.

---

## 2. Installation and Requirements

The package requires Python 3.11+ and `uv`; `uv.lock` pins the resolved
environment, including the optional notebook stack.

- `numpy >= 1.24.0`
- `scipy >= 1.10.0`
- `pytest >= 7.3.0`
- `pytest-cov >= 4.0.0`
- `pytest-xdist >= 3.0.0`

Create the locked environment:

```bash
uv sync --frozen --extra notebooks
```

---

## 3. Test and Verification Suite

Run the full automated unit, adversarial, domain-validation, release-tooling,
and fault-injection suite:

```bash
uv run --frozen --extra notebooks python -m pytest code/tests -n 8
```

Run the release coverage gate (statement and branch coverage):

```bash
uv run --frozen --extra notebooks python -m pytest code/tests -n 8 \
  --cov=code --cov-branch --cov-report=term-missing --cov-fail-under=95
```

The required threshold is 95.0%. Treat the command's fresh output—not a
historical count in prose—as the current test and coverage evidence.

Replay both notebooks in fresh subprocess kernels without overwriting their
source files:

```bash
uv run --frozen --extra notebooks python scripts/replay_notebooks.py
```

Run the fail-closed release-envelope gate after the Lean receipt, manifests,
and archive have been regenerated from the intended release tree:

```bash
uv run --frozen --extra notebooks python verify_deposit.py
```

`--tree-only` skips only the ZIP comparison. Passing either mode is an
integrity result, not a proof of the paper's claims or publication readiness.

---

## 4. Formal Verification (Lean 4)

Formalization is provided in the `lean4/` directory under Lean toolchain `leanprover/lean4:v4.34.0-rc1` and Lake package `gs002` (target `GS002`):

- `gs002_core.lean`: Master module importing all formalization components.
- `gs002_l003_01_triangle_separation.lean`: Rational squaring proof certifying $2^2 \ne 2$ ($4 \ne 2$) in $\mathbb{Q}$.
- `gs002_l003_02_s_ok_local_gauge.lean`: Constructive $\mathrm{SO}(2)$ circle transitivity (`so2_transitive_on_circle`) and native-norm radial constancy (`so_k_local_gauge_simplified`).
- `gs002_l003_03_weighted_cycle_quotient.lean`: Closed-form single-cycle quotient minimization.
- `gs002_l003_04_edge_decomposition.lean`: Disjoint-support finite edge splitting.
- `gs002_l003_05_mixed_closure_bound.lean`: Submultiplicative operator norm closure bound under $d_1 d_0 = 0$.
- `gs002_l003_06_mixed_duality_weak.lean`: Weak duality theorem for mixed $(1, 2)$ cochains.
- `gs002_l003_07_cycle_exactness.lean`: Coboundary exactness on tree-spanning cycle complexes.

The retained 2026-09-28 receipt records a completed build with **zero sorries**
and **zero admits**. The sources and receipt have not been changed in this
review. Every theorem and lemma is a census target; the release gate requires a
fresh build and an exact match to the stored axiom dependencies. The 2026-10-02
review host could not run the pinned Lean/Lake gate, and notebook kernel replay
was blocked by socket permissions. See [publication review](docs/publication_review.md)
for fresh results and outstanding release checks.

---

## 5. Directory Structure

```
008_so_k_invariant_gauge_classification/
├── code/
│   ├── carrier.py              # GraphComplex and Cochain data structures
│   ├── gauges.py               # Stalk gauges: Euclidean, CoordinateL1, Lp, Anisotropic
│   ├── solver.py               # Primal-dual mixed norm solvers
│   ├── socp_certifier.py       # Second-order cone programming certifier
│   ├── socp_exact_certifier.py # Backward-compatibility alias
│   ├── cycle_analytics.py      # Analytical cycle and triangle separation routines
│   ├── closure.py              # Mixed closure bound evaluator
│   ├── falsification.py        # Invasive adversary and fault-injection suites
│   ├── so_k_gauge.py           # Compatibility facade
│   └── tests/                  # Unit, adversarial, and release-tooling tests
├── docs/
│   ├── claim_code_map.yaml     # Claim-to-code traceability map
│   ├── descriptions.md         # Extended technical descriptions
│   ├── keywords.md             # Standardized research keywords
│   ├── quick_start.md          # Reviewer quick-start card
│   └── references.md           # Bibliographic references
├── jupyter_notebooks/
│   ├── so_k_invariant_gauge_classification.ipynb
│   └── visual_gauge_rigidity_and_separation.ipynb
├── lean4/                      # Lean 4 formalization package
├── so_k_invariant_gauge_classification.md   # Complete preprint manuscript
├── so_k_invariant_gauge_classification.tex  # LaTeX source
├── so_k_invariant_gauge_classification.pdf  # Compiled preprint PDF
├── so_k_invariant_gauge_classification_claim_ledger.md # Claim ledger
├── so_k_invariant_gauge_classification_change_log.md    # Release change log
├── zenodo_metadata.json        # Zenodo deposit metadata (v2.0.0)
├── pyproject.toml              # Build and dependency configuration
└── uv.lock                     # Resolved reproducible environment
```

---

## 6. Teaching and Review

- [Study guide](docs/study_guide.md): hypotheses, proof sequence, signed weighted examples, and evidence limits.
- [Landau quiz](docs/landau_quiz.md): sixteen written proof and counterexample problems.
- [Solutions](docs/landau_quiz_solutions.md): derivations and grading criteria.
- [Publication review](docs/publication_review.md): repairs, validation, and remaining release gates.

## 7. License

- Prose and documentation: Creative Commons Attribution 4.0 International (CC-BY-4.0).
- Software and formal proofs: Apache License, Version 2.0.

## Rebuild the paper

With Pandoc and XeLaTeX installed, run `uv run --frozen python scripts/build_paper.py`. The builder takes the title and four header fields from the Markdown source, uses `scripts/paper_template.tex`, compiles twice in a temporary directory, and rejects missing glyphs or overfull boxes. It writes only the canonical TeX and PDF. The archive retains the existing candidate date in its name; the dated review receipt records the later maintenance checks.
