# Claim Ledger — QM_041

**Paper Key:** `003_quantum_foundations/qm_041_heisenberg_picture_shadow.md`  
**Paper:** `qm_041_heisenberg_picture_shadow.md`  
**Authority:** None  
**Status:** ABSORBED_REDIRECT (2026-10-17 packaging merge)

## Claims & Reconciliation

| ID | Claim | Type | Status | Live Destination |
| --- | --- | --- | --- | --- |
| `QM_041-C1` | Gell-Mann--Hartle decoherence matrix $D(\gamma_j, \gamma_k) = \text{Tr}(C_j \rho C_k^\dagger)$ has non-negative diagonal $D(\gamma_j, \gamma_j) = P(\gamma_j) \ge 0$. | [DERIVED] | MERGED | Consolidated into [`qm_043_gellmann_hartle_cochain_decoherence.md`](qm_043_gellmann_hartle_cochain_decoherence.md) (`QM_043-C2`) |
| `QM_041-C2` | Off-diagonal vanishing $D(\gamma_j, \gamma_k) = 0$ ($j \neq k$) certifies exact probability additivity across alternative histories. | [DERIVED] | MERGED | Consolidated into [`qm_043_gellmann_hartle_cochain_decoherence.md`](qm_043_gellmann_hartle_cochain_decoherence.md) (Exact coarse-graining residual & weak/medium decoherence conditions) |
| `QM_041-C3` | For Hermitian $H$ and $U(t)=\exp(-i t H)$, the evolution $A(t) = U^\dagger(t) A U(t)$ satisfies $\frac{d}{dt}A(t) = i[H, A(t)]$. | [DERIVED] | RETIRED_RETAINED | Retained in dynamics material ([`034_unitary_finite_shadow/unitary_finite_shadow.md`](034_unitary_finite_shadow/unitary_finite_shadow.md)), `omega_quantum_physics::heisenberg_picture`, and test suite `heisenberg_picture_shadow.rs` |
| `QM_041-C4` | Infinite history spaces and continuous master equations are quarantined as optional observer coordinate lifts. | [SCOPE FENCE] | PROVED | Retained architectural boundary fence |

No claims are promoted beyond their declared finite graph scope.
