# Claim Ledger — qm_083_completely_positive_import_boundary

**Date:** July 2026  
**Paper Key:** `003_quantum_foundations/083_completely_positive_import_boundary`  
**Paper Identity:** `QM_083`  
**AuthorityEffect:** `None`  

---

| Claim ID | Claim Type | Scope / Statement | Verification Target |
| :--- | :--- | :--- | :--- |
| `QM_083-C1` | `[DERIVED]` | Markov stochastic kernel 0-cochain transport $K_{ij} \ge 0, \sum_i K_{ij} = 1$ | `003_qm_stochastic_channel.lean` |
| `QM_083-C2` | `[DERIVED]` | Unconditional $L^1$ norm contraction $\|K \rho\|_1 \le \|\rho\|_1$ | `003_qm_stochastic_l1.lean` |
| `QM_083-C3` | `[SCOPE FENCE]` | Local Green $\neq$ Global Red — local positivity $K \ge 0$ does not force complete positivity $K \otimes I \ge 0$ | `003_qm_trace_non_select.lean` |
| `QM_083-C4` | `[Q-HELD]` | Kraus operator decomposition is an external $L^2$ observer projection | `003_qm_continuum_non_promotion.lean` |
