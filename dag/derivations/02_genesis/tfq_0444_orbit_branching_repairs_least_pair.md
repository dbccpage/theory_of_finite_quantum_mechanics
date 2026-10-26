# [TFQ-0444] orbit-branching-repairs-least-pair

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `1f665f34-13ba-5306-b39c-a893303eace5`  
> **Parent Derivation**: [TFQ-0443](tfq_0443_challenge_source_policies.md)

---

## 1. Abstract & Formal Statement

Raw least-pair selection is not isomorphism-equivariant. On the regression regime (four data, one unary form, instances on data 2 and 3) both the regime and its renaming by the double transposition 0↔2, 1↔3 collapse the pair (0, 1), yet the renaming carries (0, 1) to (2, 3) (least_pair_selection_not_congruent); that the two same-index choices give non-isomorphic children is a computational test. The repair branches once per automorphism orbit of collapsed pairs. Under datum renamings with forms fixed, the selection-free transition relation over every collapsed pair and every valid response transports (transStep_rename_fwd, transStep_image_total), and valid-response counts over caller-supplied candidate lists transport (validCount_rename).

### Governing Obligation
Show that the index-least collapsed pair is not carried along a renaming of the regression regime, and that the selection-free transition relation and its valid-response counts transport under datum renamings.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The congruence is relation-level with forms fixed; conversion to equal canonical-key class sets, form-bijection transport and minimum-family transport stay computational with CL-ISO-SOUND, and no exported run reached a state with more than one orbit.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean::least_pair_selection_not_congruent`](../../../lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean::transStep_image_total`](../../../lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean::transStep_rename_fwd`](../../../lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean::validCount_rename`](../../../lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/automorphism.rs::orbits_are_equivariant_under_renaming` (private upstream source, not in this repository)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/automorphism.rs::pair_orbits` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::pair_orbits` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0445](tfq_0445_response_existence_mark_progress.md)
- [TFQ-0447](tfq_0447_count_invariance_transport.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:371-379`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:385-391`
  - `lean4/Imported/Genesis19l57g1/Derivation/TransitionTransport.lean:1067-1072`
