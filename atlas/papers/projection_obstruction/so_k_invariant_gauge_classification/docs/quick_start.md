# Reviewer Quick-Start Card: GS-002 (v2.0.0)

**Package:** `so_k_invariant_gauge_classification`  
**Paper:** *SO(k)-Invariant Gauge Rigidity for Declared Euclidean Stalks: Local $\ell^2$ Selection and Outer $\ell^1$ Aggregation*  
**Date:** 2026-09-21

---

## 1. Quick Reproduction Commands

### Environment Setup
```bash
# Resolve nothing at review time: install the checked-in lock.
uv sync --frozen --extra notebooks
```

### Run All Tests
```bash
# Run pytest across parallel workers
uv run --frozen --extra notebooks python -m pytest code/tests -n 8

# Run the statement + branch coverage gate
uv run --frozen --extra notebooks python -m pytest code/tests -n 8 \
  --cov=code --cov-branch --cov-report=term-missing --cov-fail-under=95

# Replay exact notebook inventory in isolated subprocess kernels
uv run --frozen --extra notebooks python scripts/replay_notebooks.py
```

### Inspect Lean 4 Formalization
```bash
cd lean4
# Toolchain: leanprover/lean4:v4.34.0-rc1
lake build GS002
```

---

## 2. Key Code Entry Points

| Component | Module | Key Classes / Functions |
|:---|:---|:---|
| **Carrier & Complex** | `carrier.py` | `GraphComplex`, `Cochain`, `SlaterViolationError` |
| **Local Stalk Gauges** | `gauges.py` | `EuclideanGauge`, `CoordinateL1Gauge`, `AnisotropicGauge`, `audit_so_k_invariance` |
| **Primal-Dual Solver** | `solver.py` | `MixedNormSolver`, `CoordinateL1Solver`, `DualityCertificate` |
| **SOCP Certifier** | `socp_certifier.py` | `SOCPCertifier`, `SOCPDualityCertificate`, `ExactSOCPCertifier` |
| **Cycle & Triangle Analytics** | `cycle_analytics.py` | `single_cycle_quotient_analytical`, `analyze_triangle_separation`, `analyze_dimension_scaling` |
| **2-Cell Closure Bound** | `closure.py` | `ClosureBoundEvaluator`, `ClosureBoundResult` |
| **Adversarial Injections** | `falsification.py` | `InvasiveAdversary`, `InjectionRecoveryResult` |

---

## 3. Core Verification Points

1. **Triangle Separation (2 vs $\sqrt{2}$):**
   Evaluated in `test_triangle_and_extensions.py::test_triangle_separation_metrics` and formalized in `lean4/gs002_l003_01_triangle_separation.lean`.
2. **Local Rigidity under $\mathrm{SO}(k)$:**
   Tested across random and exact $\mathrm{SO}(k)$ rotations in `test_gauges_and_sok.py` and formalized in `lean4/gs002_l003_02_s_ok_local_gauge.lean`.
3. **Exact Duality Gap:**
   Zero-gap certificate verified across cycles and general graphs in `test_mixed_norm_solver.py` and `test_primal_dual_duality.py`.
4. **Closure Bound:**
   Verified in `test_closure_bound_and_operator_norm.py` and formalized in `lean4/gs002_l003_05_mixed_closure_bound.lean`.

## Teaching and publication evidence

Read [study_guide.md](study_guide.md) before the [Landau quiz](landau_quiz.md); then compare [solutions](landau_quiz_solutions.md). The [publication review](publication_review.md) separates fresh checks from historical Lean evidence and kernel replay still required for release.
