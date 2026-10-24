# Pre-Commit Overclaim & Claim Hygiene Review: `TFQ-0107`

- **Date**: `2026-10-24`
- **Branch**: `campaign/tfq-0107`
- **Target Node**: `TFQ-0107` (`FINITE_QG`, `GAP`)
- **Result**: `PASS (0 overclaim flags)`

## 1. Scope Audit

1. **What it supports**:
   - Exact rational replay in [`lean4/CampaignTfq0107FiniteQg.lean`](../../../lean4/CampaignTfq0107FiniteQg.lean) and [`checks/independent/tfq-0107.py`](../../../checks/independent/tfq-0107.py) of the discrete Regge and Hamiltonian constraint expressions in `field_equation.rs` and `hamiltonian_constraint.rs`, plus formal proofs of $\Lambda$ underdetermination, 3D scaling mismatch, and two-hinge deficit cancellation.
2. **What it does not support**:
   - Any derivation or discharge of the continuum Einstein equations, any selection of a physical cosmological constant $\Lambda$, or any identification of discrete hinge deficits with smooth Riemannian curvature.
3. **Narrowest defensible claim**:
   - Over $\mathbb{Q}$, the discrete Regge edge residual and simplicial vertex Hamiltonian constraint vanish if and only if the caller-supplied $\lambda$ equals $C / V_{\text{grad}}$ or $(U_v - K_v)/(2 V_v)$, static balance is not invariant under uniform 3D edge rescaling at fixed $\lambda \neq 0$, and vanishing of an edge curvature gradient does not imply vanishing of individual hinge deficits.
4. **Next test needed**:
   - Proceed to `TFQ-0117` in `CONTINUUM_INTERFACE`.
