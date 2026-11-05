# so_k_gauge: Python Reference Implementation

Reference implementation for Paper GS-002: *SO(k)-Invariant Gauge Rigidity for Declared Euclidean Stalks: Local ℓ² Selection and Outer ℓ¹ Aggregation*.

## Package Overview

The `so_k_gauge` package implements cellular cochain complexes with vector stalks, stalk gauge geometries, second-order cone programming (SOCP) duality certifiers, cycle separation analytics, and 2-cell closure bound evaluators.

### Module Structure

The package modules reside directly under `code/` with package facade `so_k_gauge.py` and `code/__init__.py`:

- `so_k_gauge.carrier`:
  - `GraphComplex`: Finite 2-complex $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ with $d_1 d_0 = 0$, vertex count $n \ge 1$, stalk dimension $k \ge 1$, and strictly positive edge weights $w_e > 0$ and face weights $u_f > 0$.
  - `Cochain`: Vector-valued cochain with data shape $(m, k)$, degree $\in \{0, 1, 2\}$, finite real values, and mixed $\ell^1(\ell^2)$ and coordinate $\ell^1(\ell^1)$ norms.
  - `SlaterViolationError`: Raised when weights violate the strict interior Slater condition ($w_e \le 0$).
  - `TopologicalDefectError`: Raised when boundary nilpotency fails ($d_1 d_0 \ne 0$).

- `so_k_gauge.gauges`:
  - `StalkGauge`: Abstract protocol for local gauges $j: \mathbb{R}^k \to [0, \infty)$.
  - `EuclideanGauge`: Isotropic $\ell^2$ norm $j(x) = c \|x\|_2$, proven to be the unique $\mathrm{SO}(k)$-invariant faithful homogeneous gauge.
  - `CoordinateL1Gauge`: Separable coordinate $\ell^1$ gauge $j(x) = c \sum_i |x_i|$.
  - `LpGauge`: General $\ell^p$ gauge for $p \ge 1$.
  - `AnisotropicGauge`: Gauge $j(x) = \|A x\|_2$ for an invertible / full-rank square matrix $A$.
  - `audit_so_k_invariance`: Haar-measure Monte Carlo invariance auditor over $\mathrm{SO}(k)$.
  - `audit_sphere_constancy`: Probes constancy of $j$ on finitely many Euclidean sphere samples.

- `so_k_gauge.socp_certifier`:
  - `SOCPCertifier`: Primal-dual second-order cone certifier. Solves single cycles in closed form and general complexes via numerical subspace optimization.
  - `CycleClosedFormCertifier`: Floating-point evaluator of the analytical formula for simple directed cycles ($m=n$, 2-regular connected).
  - `SOCPDualityCertificate`: Carries `primal_value`, `dual_value`, `duality_gap`, `signed_duality_gap` ($= \text{primal} - \text{dual}$), feasibility metrics, `is_zero_gap`, and `is_optimal`.
  - `ExactSOCPCertifier`: Backward-compatibility alias for `SOCPCertifier`.

- `so_k_gauge.solver`:
  - `MixedNormSolver`: High-level solver for mixed $(1,2)$ quotient obstructions $\Phi_{2,1,c}([\omega])$, supporting `method="auto" | "cycle_closed_form" | "numerical" | "smoothed_lbfgs"`.
  - `CoordinateL1Solver`: Exact linear programming solver for coordinate-separable $\ell^1$ quotient obstructions $\Phi_{1,1,c}([\omega])$ using HiGHS.

- `so_k_gauge.cycle_analytics`:
  - `compute_cycle_circulation`: Signed circulation $S(\omega) = \sum_{e \in C} \varepsilon_e \omega_e$ under orientations $\varepsilon_e \in \{+1, -1\}$.
  - `single_cycle_quotient_analytical`: Closed-form single-cycle quotient formula $(\min_e w_e) \cdot j(S(\omega))$.
  - `analyze_triangle_separation`: Evaluates the canonical triangle anomaly separation: $\Phi_{1,1} = 2$ vs $\Phi_{2,1} = \sqrt{2}$ (ratio $\sqrt{2}$).
  - `analyze_dimension_scaling`: Evaluates discrepancy scaling $\Phi_{1,1}/\Phi_{2,1} = \sqrt{k}$ across stalk dimensions $k$.
  - `compute_holonomy`: Evaluates cycle holonomy $H_C = \prod_{i} R_i^{\varepsilon_i} \in \mathrm{SO}(k)$ along directed cycles.
  - `apply_vertex_gauge_transformation`: Applies genuine vertex gauge transformations $R_{uv}' = g_v R_{uv} g_u^T$ with $g_v \in \mathrm{SO}(k)$, proving conjugacy $H_C' = g_0 H_C g_0^T$ and gauge invariance of holonomy eigenvalues and trace.

- `so_k_gauge.closure`:
  - `ClosureBoundEvaluator`: Evaluates the 2-cell closure inequality $\Gamma_{2,1,u}([h]) \le \|d_1\| \cdot \Phi_{2,1,c}([h])$ and constructive operator norm $\|d_1\|$.
  - `ClosureBoundResult`: Reports `gamma_closure_defect`, `operator_norm_bound`, `candidate_primal_value`, `certified_quotient_value` (None if certificate not optimal), `candidate_bound_holds`, and fail-closed `certified_bound_holds = cert.is_optimal and candidate_bound_holds`.

- `so_k_gauge.falsification`:
  - `InvasiveAdversary`: Adversarial fault injector asserting detection and recovery for divergence violations, gauge anisotropy, Lipschitz noise perturbations, dual norm ball violations, direct connection repair, and vertex gauge conjugacy.

---

## Solver Bounds and Limitations

Mathematical formulas and numerical evidence have different scopes:

1. **Exact Closed-Form Solutions**:
   - **Simple Cycles**: On connected 2-regular directed cycles ($m=n \ge 3$), `solver_method="cycle_closed_form"` evaluates the analytical closed-form in floating-point arithmetic:
     $$\Phi_{2,1,w}([\omega]) = (\min_{e \in C} w_e) \|S(\omega)\|_2$$
     with an explicit dual witness $z_e = \varepsilon_e w_{\min} \frac{S(\omega)}{\|S(\omega)\|_2} \in \ker(d_0^*)$. Duality gap is zero to machine precision.
   - **Exact Coboundaries**: For coboundaries $\omega \in \operatorname{im}(d_0)$, `solver_method="zero_circulation"` checks a zero dual witness using a floating-point repair and its weighted primal-dual gap. It does not prove exact membership in the repair image.

2. **Numerical Subspace Optimization on General Graphs**:
   - For arbitrary graph complexes with multiple cycles or theta topologies, `solver_method="numerical_socp_subspace"` optimizes the dual in the cycle subspace $\ker(d_0^*)$ using SLSQP and the primal using smoothed L-BFGS-B continuation.
   - Results are **tolerance-certified numerical candidates**. The certificate's validity is governed by `is_optimal`, `divergence_norm <= tol`, `max_dual_norm_violation <= tol`, and `duality_gap <= tol` (default $\text{tol} = 10^{-7}$).
   - The signed weak-duality gap `signed_duality_gap = primal_value - dual_value` is explicitly preserved.
   - On ill-conditioned complexes ($\kappa(w) \gg 10^5$), numerical optimization may terminate with a non-zero gap; the certifier honestly sets `is_optimal = False`.

---

## Input Domain Validation (Fail-Fast Discipline)

All public entry points enforce fail-fast preconditions:

- **Cochains**: Must have rank $\le 2$, degree $\in \{0, 1, 2\}$, and strictly finite real values. NaN or $\pm\infty$ raise `ValueError`.
- **GraphComplex**: Vertex count $n \ge 1$ (non-boolean integer), stalk dimension $k \ge 1$, edge count $m \ge 1$ (empty-edge complex rejected at construction), valid directed edges $(u, v)$ with non-boolean integers $0 \le u, v < n$ and $u \ne v$ (no self-loops). Edge and face weights must be strictly positive and finite; non-positive weights raise `SlaterViolationError`. Face signs must be in $\{+1, -1\}$.
- **Rotations & Dimensions**: Dimension scaling and random rotation generators require positive non-boolean integers $k \ge 1$. $\mathrm{SO}(2)$ rotation requires finite real angles.
- **Auditors**: Sphere constancy audit requires strictly positive finite radius and nonnegative finite tolerance. Invariance audit requires nonnegative finite tolerance and $n_{\text{samples}} \ge 1$.
- **Certifiers**: Both `SOCPCertifier` and `CycleClosedFormCertifier` validate that cochain data shape matches $(m, k)$ and orientations are in $\{+1, -1\}$.

---

## Installation and Testing

### Requirements

- Python $\ge 3.11$
- `numpy >= 1.24.0`
- `scipy >= 1.10.0`
- `pytest >= 7.3.0`
- `pytest-cov >= 4.0.0`
- `pytest-xdist >= 3.0.0`

### Installation

From the package root:

```bash
uv sync --frozen --extra notebooks --extra dev
```

### Running Tests

Execute the full test suite over 8 parallel workers:

```bash
uv run --frozen --extra notebooks python -m pytest code/tests -n 8 \
  --cov=code --cov-branch --cov-fail-under=95
```

Expected result: every collected test passes and the configured 95% statement
and branch coverage gate succeeds. Use the command output as the current
receipt; this page intentionally does not preserve a mutable test count.

### Code Hygiene

```bash
uv run --frozen --extra dev ruff check code scripts verify_deposit.py
```

Zero lint or bugbear warnings.

### Numerical evidence limits

All solver paths use finite, nonnegative acceptance tolerances. Cycle routing preserves nonzero circulation even when its coordinates are small; weighted residual gaps govern zero-witness acceptance. The smoothed solver uses the same declared tolerance for its gap, divergence, and ball checks. Random gauge audits reject nonfinite or negative outputs and an empty effective sample; a pass covers only sampled data. `certified_quotient_value` is tolerance-qualified. `is_exact_repair` reports a computed zero primal residual cost, and is not an exact-arithmetic membership proof. A closure ratio is supplied only for a positive, tolerance-qualified quotient. The coordinate LP reports the HiGHS optimizer status and does not supply an independent exact primal-dual certificate.
