# [TFQ-0537] wdp-pointed-apartness

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `2048523c-d29b-5a9b-bf70-5fb66f0dcbaa`  
> **Parent Derivation**: [TFQ-0360](tfq_0360_supply_the_admitted_cut_x_e_tau_k_as_data_and_do.md)

---

## 1. Abstract & Formal Statement

WDP-CH01-P02: for a pointed relation (X, R, a, b) on a finite carrier, R(a,b) does not imply a ≠ b (one-point carrier with R = {(a,a)} and b = a), a ≠ b does not imply R(a,b) (the empty relation on two points), and R(a,b) with R irreflexive implies a ≠ b, since a = b would give R(a,a). Irreflexivity is therefore a declared ingredient of the admitted package, not a consequence of relatedness, and a carrier hosting an irreflexive related pair has at least two elements; PrimDiff.lean states the same endpoint fact for an irreflexive witness. The Python census over every pointed relation on carriers of size 1 to 3 counts 4674 relations, 2337 with R(a,b), 196 with R(a,b) and R irreflexive, 3104 with a ≠ b, and none with R irreflexive, R(a,b) and a = b.

### Governing Obligation
Check the two countermodels and the irreflexive substitution step, and reproduce the bounded census 4674 / 2337 / 196 / 3104 with zero irreflexive related pairs having equal poles at carrier sizes 1 to 3.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared irreflexivity law on the relation R (assumption)`

### Further Prerequisites
- [TFQ-0515](../05_mssn_sn/tfq_0515_sn_endpoint_lemma.md) sn-endpoint-lemma

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean pointed_relation_independence_fin gives the Fin 1 and Fin 2 countermodels and the irreflexive implication over every type; the census stops at size 3, and neither the relation nor the irreflexivity law is derived from <>.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean::pointed_relation_independence_fin`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/PointedRelation.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs::GenesisAdmissionKernel`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_pointed_relation.py::test_census_matches_the_closed_forms_on_carriers_up_to_three`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_pointed_relation.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/pointed_relation.py::enumerate_pointed_relations`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/pointed_relation.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:466-478`
  - `omega_engine_education/documentation/006_oewdp/levels/level_00_admitted_cut.md:165-170`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md:43-50`
