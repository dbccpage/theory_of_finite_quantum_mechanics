---
documentation_contract: symbol-game-documentation/v1
title: "Prime Triad Level 00: Executive Architecture — Protocol Stages vs. Pure Types"
kind: mathematical-reference
level: 0
status: active
maturity: production
claim_status: verified
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/source_archive/prime_algorithm_package/oe_prime_algorithms.md
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_scope.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/descent_engine.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/mod.rs
  - omega_engine/crates_rs/omega_types/src/prime.rs
last_verified: 2026-10-01
---

# Prime Triad Level 00: Executive Architecture — Protocol Stages vs. Pure Types

**AuthorityEffect:** None. Complete mathematical and architectural reference for the separation between protocol stages and pure domain types; no operational authorization is conferred.

---

## 1. Executive Intuition: The Clean Architecture Invariant

A central vulnerability of recursive evaluation engines is **semantic conflation**: treating protocol lifecycle stages as domain data types, or allowing operational runners to mutate noun-shaped evidence records.

In the Omega Engine, this is prevented by an absolute Clean Architecture boundary:

$$\boxed{\begin{aligned}
\text{\textbf{Protocol Stages}} &\quad\neq\quad \text{\textbf{Domain Types}} \\
(\text{Prime -1, 000, 001, 002}) &\quad\neq\quad (\text{CandidatePacket, AdmittedDeclaration, LossLedger, StepPermit})
\end{aligned}}$$

1. **Protocol Stages are Verifiers & State Machines:** Stages (Prime -1, Prime 000, Prime 001, Prime 002) are state-machine checkpoints, compilers, and behavioral runners. They live under runtime crates:
   - [`omega_prime_algos`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/) (dedicated sovereign crate)
   - [`omega_discrete_deformation_calculus`](../../../../../omega_engine/crates_rs/omega_wdp/src/ddc/) (bridge & alphabet)
   - [`omega_symbol_game::prime`](../../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/source_archive/prime_algorithm_package/code/)
2. **Domain Types are Immutable Nouns:** Data structures (`CandidatePacket`, `DeclarationPacket`, `AdmissionDecision`, `LossEntry`, `LossLedger`, `CanContinueInput`, `ScopeBinding`) represent mathematical evidence and propositions. They live under domain crates:
   - [`omega_types::prime`](../../../../../omega_engine/crates_rs/omega_types/src/prime.rs)
   - [`omega_types::causal_trace`](../../../../../omega_engine/crates_rs/omega_types/src/causal_trace.rs)

---

## 2. The Five Cardinal Invariants of the Prime Triad

The Prime Triad enforces five architectural constraints across both Rust and Python estates:

```
  +-------------------------------------------------------------------------------+
  |                          THE FIVE CARDINAL INVARIANTS                         |
  +-------------------------------------------------------------------------------+
  |  1. Measurement Never Precedes Admission (Prime 000 Gate)                     |
  |  2. Translation Does Not Confer Validity (Prime 001 Transport Law)            |
  |  3. Evidence is Scope-Bound and Sealed (Prime 002 Evidence Discipline)        |
  |  4. Execution Permits are Single-Use (Linear Type Move Semantics)             |
  |  5. Authority Effect is Invariant None (GTOC-5 Firewall)                      |
  +-------------------------------------------------------------------------------+
```

### Invariant 1: Measurement Never Precedes Admission
A cochain cannot be evaluated for quotient potential ($\Phi_1$) or closure defect ($\Gamma_2$) before its carrier, observer, and primitive difference have been admitted by Prime 000. In Rust:
```rust
// compile_fail: measuring without AdmittedDeclaration is unrepresentable
pub fn run_admitted(
    admitted: &AdmittedDeclaration,
    adapter: &dyn DomainAdapter,
) -> PrimeAlgorithm0Receipt;
```
In Python (`oe_prime_algorithms.py#L580`):
```python
if not admitted:
    raise PermissionError("MEASUREMENT_REFUSED_UNADMITTED_PACKET")
```

### Invariant 2: Translation Does Not Confer Validity
Transporting an obstruction from carrier $A$ to carrier $B$ arrives strictly with status `Proposed`, never `Admitted`. An adapter that preserves status across carrier boundaries is an authority-laundering device.

### Invariant 3: Evidence is Scope-Bound and Sealed
Every piece of evidence (`Gamma2Zero`, `DetectorAdequacy`, `ObligationWitness`, `SameCarrierExhaustion`, `LossLedger`) binds a specific [`ScopeBinding`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_scope.rs). Evidence minted for residual $A$ on carrier $K_1$ cannot be reused to authorize residual $B$ on carrier $K_2$.

### Invariant 4: Execution Permits are Single-Use
The authorization to execute a step or terminalize a run is encapsulated in linear, non-clonable structs:
```rust
pub struct StepPermit { /* private fields */ }  // not Clone, not Deserialize
pub struct TerminalPermit { /* private fields */ }  // consumed by value
```

### Invariant 5: Authority Effect is Strictly None
All receipts and transcripts register:
```rust
pub fn authority_is_none(&self) -> bool {
    self.authority_effect == AuthorityEffect::None
}
```

---

## 3. The Scope Binding Architecture: `prime_scope.rs`

All Prime operations require explicit scope attestation through [`ScopeBinding`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_scope.rs):

```rust
# [derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ScopeBinding {
    run: Hash256,
    carrier: Hash256,
    residual: Hash256,
    tape_head: Hash256,
}
```

A scope binding binds four distinct coordinates:
1. `run`: The unique evaluation session identifier.
2. `carrier`: The SHA-256 cryptographic digest of the declared discrete simplicial carrier $K$.
3. `residual`: The digest of the active primitive difference $\omega \in C^1$.
4. `tape_head`: The cryptographic state digest of the DDC letter tape prior to the step.

If any coordinate mismatches between the site and presented evidence, [`require_same_scope`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_scope.rs#L276) immediately emits a typed `ScopeMismatch` refusal:

$$\operatorname{commit}(\mathrm{Scope}) = \operatorname{SHA256}(\texttt{"oeprm.scope.v1"} \parallel \operatorname{run} \parallel \operatorname{carrier} \parallel \operatorname{residual} \parallel \operatorname{tape\_head})$$

---

## 4. Architectural Layer Crosswalk

| Layer | Responsibility | Rust Implementation | Python Implementation |
| :--- | :--- | :--- | :--- |
| **Stage -1** | Ingest raw artifacts, propose carriers | [`prime_candidate.rs`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_candidate.rs) | `CandidatePacket`, `IntakeTrace` |
| **Stage 000 Admission** | 7-step declaration verification | [`prime_algorithm_0_admission.rs`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_0_admission.rs) | `LocalDeclarationOrder` |
| **Stage 000 Execution** | 12-step cochain fill & tape emission | [`prime_algorithm_0.rs`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_0.rs) | `ObstructionCalculus`, `Simplex` |
| **Stage 001 Intake/Transport** | Preserves ops, records lost data | [`prime_algorithm_1.rs`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_1.rs) | `AdapterContract`, `check_adapter` |
| **Stage 002 Continuation** | Master predicate & anti-cheat halting | [`prime_algorithm_2.rs`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_2.rs) | `CanContinueInput`, `ResidualQueue` |
| **Sovereign Coordinator** | Exact solver diagnostics & Coda wiring | [`descent_engine.rs`](../../../../../omega_engine/crates_rs/omega_wdp/src/prime_algos/descent_engine.rs) | `PrimeDescentCoordinator` |

---

## 5. Self-Assessment Micro-Checks

1. **Why is `AdmittedDeclaration` constructed only through `prime_algorithm_0_admission::admit`?**  
   *Answer:* It has private fields and no public constructor. This guarantees at compile time that no code path can pass an unadmitted proposal into the execution engine.
2. **Why does `StepPermit` lack `Clone` and `Deserialize` derives?**  
   *Answer:* If a permit could be cloned or deserialized from JSON, a single authorization could be spent multiple times or forged from untrusted text, violating single-use linear execution.
3. **What is the consequence of identifying locus $L$ with carrier $C_L$?**  
   *Answer:* It bypasses the Prime -1 intake compiler and Prime 000 admission gate, silently promoting arbitrary unstructured entities into simplicial carriers without topological validation.

---

## 6. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal Clean Architecture separation between immutable domain evidence types and behavioral stage runners.
   - Machine-enforced compile-time boundaries preventing measurement of unadmitted proposals.
2. **What this does not support:**
   - Does not establish that software type safety prevents all logical bugs in mathematical modeling.
   - Does not license un-scoped global green certificates.
3. **The narrowest defensible claim:**
   - Under Rust type-system rules and linear move semantics, evidence cannot be synthesized without calling verifying constructors, and permits cannot be duplicated across steps.
4. **Next test needed:**
   - Verify scope matching and admission gating by running `cargo test --manifest-path omega_engine/crates_rs/omega_wdp/src/prime_algos/Cargo.toml`.
