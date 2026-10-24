# Pre-Commit Overclaim & Claim Hygiene Review: `TFQ-0090`

- **Date**: `2026-10-24`
- **Branch**: `campaign/tfq-0090`
- **Target Node**: `TFQ-0090` (`FINITE_QG`, `GAP`)
- **Result**: `PASS (0 overclaim flags)`

## 1. Scope Audit

1. **What it supports**:
   - Exact rational formalization in [`lean4/CampaignTfq0090FiniteQg.lean`](../../../lean4/CampaignTfq0090FiniteQg.lean) and [`checks/independent/tfq-0090.py`](../../../checks/independent/tfq-0090.py) of cochain curvature $d_1 \omega$ on $K_4^{(2)}$, the `OBL-R03` scaling and topological split between cochain curvature and Regge vertex deficit, and the `OBL-R01` lattice-spacing and Manhattan-anisotropy fences for discrete light cones.
2. **What it does not support**:
   - Any identification of finite hinge deficit with smooth manifold Riemannian curvature, any continuum lattice-spacing descent, or any recovery of continuum Lorentz invariance from a finite comparison graph.
3. **Narrowest defensible claim**:
   - On $K_4^{(2)}$ over $\mathbb{Q}$, cochain curvature $d_1 \omega$ (linear, gauge-invariant, zero Bianchi cycle sum) and equilateral Regge vertex deficit $\epsilon_v$ (length-scale invariant, affine, Gauss-Bonnet sum $2 T_{\text{full}}$) vary independently (`OBL-R03`), and discrete causal step counts leave the effective light-cone slope $a_x / a_t$ and Euclidean isotropy uncalibrated (`OBL-R01`).
4. **Next test needed**:
   - Proceed to `TFQ-0107` in `FINITE_QG`.
