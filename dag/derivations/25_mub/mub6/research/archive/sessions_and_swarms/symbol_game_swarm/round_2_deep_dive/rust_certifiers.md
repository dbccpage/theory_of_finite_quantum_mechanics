# Round 2 Deep-Dive Specification: Rust Native Certifiers & Solvers

**AuthorityEffect:** None  
**Firewall Line:** `stated region only; mints no authority`  
**Authors:** Executive Steering Team & Execution Teams 1–10

---

## 1. Overview of Rust Native Engines in `omega_engine/crates_rs/omega_mub`

### 1.1 Target G1: `src/omega_native/mub6_g1_variety.rs`
- **Responsibilities**:
  1. Exact rational 50-variable Hadamard variety constraint evaluator over `num_rational::BigRational`.
  2. Corner minor evaluation: evaluating $3 \times 3$ corner submatrices and factoring their determinants into known branch polynomials.
  3. Triad compatibility decision solver: given two complex Hadamard matrices $H_1, H_2$ in exact cyclotomic representation `Cyc24`, checks whether $H_1^\dagger H_2$ satisfies unit modulus and column orthogonality.
  4. Network Simplex acceleration confirming positive cycle circulation $\Phi_1 > 0$ across all cross-orbit triads $(S_6, B_6)$, $(S_6, S_6)$, $(B_6, B_6)$.
  5. Strict AST zero-float check via `syn`.

### 1.2 Target Q-Soundness: `src/omega_native/mub6_positivstellensatz.rs`
- **Responsibilities**:
  1. Non-commutative projector word algebra term rewriter and monomial canonizer.
  2. Exact rational Archimedean Positivstellensatz certificate verifier: checks the algebraic identity $25 - \sum \Pi_{i, a}^2 = \sum s_k^* s_k + \sum g_j$.
  3. Exact rational rank evaluator: computes exact matrix rank of $M_2, M_4, M_6, M_8$ via Gaussian row reduction over `BigRational`.
  4. Verifies rank-gap sequence $\Delta_d = \operatorname{rank}(M_d) - \operatorname{rank}(M_{d-1}) > 0$, certifying that flat extension is obstructed at degree $\le 8$.
  5. Emits `MomentSdpStatus::MissingProofObligation` on universal unconstrained claims.

---

## 2. Compilation and Test Standards
- `cargo check -p omega_mub` must compile with zero errors.
- Unit and integration tests must pass cleanly in release mode: `cargo test -p omega_mub --release`.
- 100% exact rational arithmetic; zero floating-point types (`f32`/`f64` forbidden).
