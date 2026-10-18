# [TFQ-0387] irreflexive-endpoints-distinct

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `3fd4ae74-d8c2-5043-a117-cd20fc33b12d`  
> **Parent Derivation**: [TFQ-0378](TFQ-0378_regime-tuple-and-events.md)

---

## 1. Abstract & Formal Statement

PG-GEN-IRREFLEXIVE-DISTINCT records that the two given names are distinct because the seed bans xrx, and that bra is not obtained from that ban. Opened H3V7N5QF/Basic.lean declares given_distinct: a legal relation sends related terms to distinct terms. Pre-Genesis Paper.lean declares irreflexive_endpoints. Ongoing claim_ledger.md rows D1, N1, and N2 say a and b are two terms, while neither bra nor its negation follows. Ledger row WDP-P000-010 adds a unique endpoint-preserving map for an oriented two-point witness, which need not preserve non-edges. The finite statement still required keeps that ban as a given.

### Governing Obligation
From the given ban on xrx and the assertion arb, a and b are distinct terms, and bra neither follows nor is refuted.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Ban on xrx (assumption: a stated part of the seed)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The distinctness rests on the ban on xrx being given; when the ban is struck (17th derivation) it is re-derived only under the obstruction rule.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: given_distinct and irreflexive_endpoints, with bra left undecided`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::irreflexive_endpoints`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Basic.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Basic.lean::bra_not_derived`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/H3V7N5QF/Basic.lean::given_distinct`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: no Rust seed module was listed under 001_genesis_ongoing_h3v7n5qf; the ban on xrx still needs a carrier there or an explicit absence`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a seed checker under 001_genesis_ongoing_h3v7n5qf/code that accepts arb, rejects xrx, and leaves bra unset`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0388](TFQ-0388_ongoing-obstruction-answers.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch02_primitive_difference_and_finite_carrier.md`
