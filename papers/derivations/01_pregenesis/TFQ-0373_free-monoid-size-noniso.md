# [TFQ-0373] free-monoid-size-noniso

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `115630ba-5146-590e-8d4d-cb7e886b3400`  
> **Parent Derivation**: [TFQ-0372](TFQ-0372_off-image-refusal-half.md)

---

## 1. Abstract & Formal Statement

PG-FREE-MONOID-NONISO and ledger rows WDP-P001-007 and WDP-P001-008 say free monoids on finite alphabets of different sizes are not isomorphic, and discrete categories with different finite object counts are not equivalent. Opened Paper.lean declares unequal_finite_alphabets_not_iso. Pre-Genesis paper.md section 11.1 is the heading. The finite statement still required is that a numeral or alphabet re-presentation is not an isomorphism of those structures. DiscreteCategory.lean is listed beside Paper.lean and still needs its own check against the discrete-category half of the ledger row.

### Governing Obligation
Free monoids on finite alphabets of different sizes are not isomorphic, and discrete categories of different finite object counts are not equivalent.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> none (finite-cardinality argument).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: unequal_finite_alphabets_not_iso for unequal finite alphabet sizes`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::unequal_finite_alphabets_not_iso`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::no_discrete_equivalence`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::no_free_monoid_iso`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: finite-alphabet non-isomorphism in crate pre_mssn_preservation`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a size comparison beside free_reduce in preservation.py that refuses an isomorphism when alphabet sizes differ`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/tests/test_free_words.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0374](TFQ-0374_three-recovery-contracts.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
