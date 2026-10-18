# Claim Ledger — qm_064_phase_gauge_residual

**Date:** July 2026  
**Paper Key:** `003_quantum_foundations/064_phase_gauge_residual`  
**Paper Identity:** `QM_064`  
**AuthorityEffect:** `None`  

---

| Claim ID | Claim Type | Scope / Statement | Verification Target |
| :--- | :--- | :--- | :--- |
| `QM_064-C1` | `[DERIVED]` | $U(1)$ phase 1-cochain coboundary transformation $(\delta \theta')(u,v) = (\delta \theta)(u,v) + (\delta \alpha)(u,v)$ | `003_qm_phase_fiber_interference.lean` |
| `QM_064-C2` | `[DERIVED]` | Gauge invariance of cycle phase holonomy $\Phi_{\text{phase}}'(C) = \Phi_{\text{phase}}(C)$ | `003_qm_phase_fiber_interference.lean` |
| `QM_064-C3` | `[SCOPE FENCE]` | Local Green $\neq$ Global Red — local phase gauge choice does not eliminate global cycle holonomy $H^1(G; U(1)) \neq 0$ | `003_qm_holonomy_curvature.lean` |
| `QM_064-C4` | `[Q-HELD]` | Continuous Lie group gauge lift is an external $L^2$ observer projection | `003_qm_continuum_non_promotion.lean` |
