# Claim Ledger — QM_043

## Consolidated Finite Histories Formulation (Merging QM_041 & QM_043)

**Date:** 2026-10-17  
**Paper Key:** `003_quantum_foundations/qm_043_gellmann_hartle_cochain_decoherence.md`  
**Paper Identity:** `QM_043`  
**Paper Version:** `v2.0.0`  
**AuthorityEffect:** `None`  
**Stage-0 Gate:** `CONDITIONAL_UPDATE_PACKET_APPROVED`

---

## Normalized Claims

| Claim ID | Exact Tags | Scope / Statement | Evidence State | Verification Target |
|---|---|---|---|---|
| `QM_043-C1` | `[IMPORTED, CONDITIONAL]` | Finite-dimensional decoherence matrix definition $D_{jk} = \operatorname{Tr}(C_j \rho C_k^\dagger)$ for class operators $\{C_j\}$ and state $\rho$. | `SOURCE_ADMITTED; RUST_VERIFIED` | `omega_functional::decoherence::DecoherenceFunctional::matrix` |
| `QM_043-C2` | `[DERIVED, CONDITIONAL]` | For $\rho \ge 0$ and $A_z = \sum_j \overline{z_j} C_j$, $z^\dagger D z = \operatorname{Tr}(A_z \rho A_z^\dagger) \ge 0$. $D$ is positive semidefinite with Cauchy–Schwarz bounds $|D_{jk}|^2 \le D_{jj} D_{kk}$. | `PROVED_FINITE_MATH; RUST_VERIFIED` | Self-contained linear algebra; `tests/.../gell_mann_hartle_decoherence.rs` |
| `QM_043-C3` | `[DERIVED, CONDITIONAL]` | Exact coarse-graining residual identity: $\mu(S) - \sum_{j \in S} D_{jj} = 2 \sum_{j < k, j,k \in S} \operatorname{Re} D_{jk}$. Absorbs the $(2, 1, 3)$ integer arithmetic fixture. | `PROVED_FINITE_MATH; RUST_VERIFIED` | `DecoherenceFunctional::sum_rule_residual`; `tests/.../gell_mann_hartle_decoherence.rs` |
| `QM_043-C4` | `[SCOPE FENCE, CONDITIONAL]` | In the encoded finite-shadow intake, absence of the required certificate returns `oracleNeeded` and cannot return a promoted target object. | `LEAN_BOUND` | Receipt: `continuum_scope_fence_receipt.json`<br>`QM.shadow_no_cert_oracleNeeded`<br>`QM.shadow_no_cert_not_promoted` |
| `QM_043-C5` | `[RETIRED_DROPPED]` | Phase-class persistence in $H^1(G; U(1))$: retired from required foundational derivation list as disconnected from finite history probability additivity. | `RETIRED` | None (dropped placeholder obligation) |
| `QM_043-C6` | `[DERIVED, CONDITIONAL]` | Diagonal normalization: $\operatorname{Tr}(\rho) = 1$ and $\sum_j C_j^\dagger C_j = I \implies \sum_j D_{jj} = 1$. The completeness premise is load-bearing. | `PROVED_FINITE_MATH; RUST_VERIFIED` | `DecoherenceFunctional::is_complete`; `tests/.../gell_mann_hartle_decoherence.rs` |
| `QM_043-C7` | `[DERIVED, CONDITIONAL]` | Weak decoherence ($\operatorname{Re} D_{jk} = 0$) characterizes single-family additivity but fails under tensor composition because $(i b_A)(i b_B) = -b_A b_B$ (Diósi objection). Medium decoherence ($D_{jk} = 0$) is tensor-stable. | `PROVED_FINITE_MATH; RUST_VERIFIED` | `DecoherenceFunctional::weak_decoherence_witness`; `tests/.../heisenberg_picture_shadow.rs` |
| `QM_043-C8` | `[DERIVED, CONDITIONAL]` | $L^1$ interference score bound: $|\mu(S) - \sum_{j \in S} D_{jj}| \le \Phi_{\mathrm{int}}(D) = \sum_{j \ne k} |D_{jk}|$. Bounds coarse-graining error without asserting a dynamical dissipation law. | `PROVED_FINITE_MATH` | Static arithmetic bound |

---

## Admitted Primary Sources

- `GH1990`: Murray Gell-Mann and James B. Hartle, "Quantum Mechanics in the Light of Quantum Cosmology," <https://arxiv.org/abs/1803.04605>
- `HARTLE1992`: James B. Hartle, "The Quantum Mechanics of Closed Systems," <https://arxiv.org/abs/gr-qc/9210006>
- `DIOSI1994`: Lajos Diósi, "Irreversible quantum dynamics and the Gell-Mann–Hartle decoherence functional," <https://arxiv.org/abs/gr-qc/9409017>
- `DOWKER_HALLIWELL1992`: H. F. Dowker and J. J. Halliwell, "Quantum mechanics of history: The decoherence functional in quantum mechanics," <https://journals.aps.org/prd/abstract/10.1103/PhysRevD.46.1580>

---

## Evidence Boundary

- `QM_043-C1`, `QM_043-C2`, `QM_043-C3`, `QM_043-C6`, `QM_043-C7`, and `QM_043-C8` are exact finite-dimensional linear-algebra theorems verified in sovereign Rust crates (`omega_functional` and `omega_quantum_physics`).
- `QM_043-C4` is Lean-bound within the encoded intake scope recorded by `continuum_scope_fence_receipt.json`.
- `QM_043-C5` is retired and no longer tracked as an active obligation.
- No claim in this ledger carries `AuthorityEffect` other than `None`.
