# [TFQ-0383] closure-round-inequality

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `4531da17-d806-522b-9e08-2f74ec8afd64`  
> **Parent Derivation**: [TFQ-0382](tfq_0382_refined_minimum_class.md)

---

## 1. Abstract & Formal Statement

Ledger row WDP-P000-009 says that with n fixed data, fresh well-formed targets, no new-datum response items, and duplicate-free initial requirements, m rounds satisfy 2 times (count of Q plus m) at most n times (n - 1). Search found closedRun_round_bound and closedRun_round_bound_from_empty in Derivation/Rounds.lean. The ledger says the requirement count is the measure and that this is not a runtime bound. Genesis paper.md section 8 is the heading. The finite statement still required is that inequality under those hypotheses only. Resource-limited search may stop earlier, as row WDP-P000-016 also notes.

### Governing Obligation
Under the WDP-P000-009 hypotheses, m rounds satisfy 2(count(Q)+m) at most n(n-1), and that measure is not a runtime bound.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: closedRun_round_bound under the ledger hypotheses of WDP-P000-009`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: closure.rs must store the inequality hypotheses beside the round count`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a round counter in 000_genesis_19l57g1/code/derivation/engine.py matching the requirement-count inequality, not a wall-clock bound`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0384](tfq_0384_cumulative_count_no_return.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
