# Claim Ledger — qm_033_schrodinger_finite_shadow

**Date:** July 2026  
**Paper Key:** `003_quantum_foundations/033_schrodinger_finite_shadow`  
**Paper Identity:** `QM_033`  
**AuthorityEffect:** `None`  

---

| Claim ID | Claim Type | Scope / Statement | Verification Target |
| :--- | :--- | :--- | :--- |
| `QM_033-C1` | `[DERIVED]` | Discrete Schrödinger cochain transport equation $i\hbar \frac{d\psi_v}{dt} = \sum_{w} H_{vw} \psi_w$ on graph $G=(V,E)$ | `003_qm_schrodinger_discrete_cochain.lean` |
| `QM_033-C2` | `[DERIVED]` | Conservation of the squared Euclidean norm $\frac{d}{dt} \sum_v \|\psi_v\|^2 = 0$ under Hermitian $H=H^\dagger$. The sum is $\|\psi\|_2^2$, not an $\ell^1$ mass. The named Lean file was not found beside this package. | manuscript Theorem 1 |
| `QM_033-C3` | `[DERIVED]` | The cycle sum of a gauge coboundary cancels, so $\Theta(C)$ is gauge-invariant. Non-vanishing whenever $H^1\neq 0$ is not proved here. | manuscript Theorem 2 |
| `QM_033-C4` | `[Q-HELD]` | Hilbert space continuous differential equation is an external $L^2$ observer lift | `003_qm_continuum_non_promotion.lean` |
