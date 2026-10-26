# [TFQ-0472] rung9-two-ness-observational-classes

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `16f0755d-8406-5bed-94b4-6c7817b531d4`  
> **Parent Derivation**: [TFQ-0471](tfq_0471_rung8_element_count_across_iso.md)

---

## 1. Abstract & Formal Statement

Rung nine (pull request 264) takes X-6 for two-ness and observational classes: a regime holds two when some two admitted data are separable, and a representative list holds pairwise separable admitted data with every admitted datum collapsed with an entry. In Lean separability, collapse, holding two and representative lists are carried by the isomorphism with no hypothesis, collapse is reflexive, symmetric and transitive, and holding two needs two data, a form and an instance, so its first stage is four events from the empty regime and two from each Lean reading regime, both attained. Supply, datum, form and requirement admissions keep separable pairs, while an instance or a rule admission can end holding two. That two representative lists of one regime have one length, the class count as a number, is OPEN in Lean (T-1).

### Governing Obligation
Carry holding two and representative lists across the isomorphism, the least lengths four and two, and the per-kind keeping laws, leaving the class count as a number to a decision for collapse.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Lean declaration SecondProfile.Classes.holdsTwo_iso at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondProfile.Stage.twoness_needs_four at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`
- **Admitted**: `Lean declaration SecondProfile.Carry.separable_iso at dbccpage/19L57G1@85a83ae7c, not elaborated in this checkout (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> separable_iso and collapsed_iso are stated forward only, the reverse being their application to the exchanged structure, which is not stated as a theorem; the class count as a number waits on a decision for collapse (X-1) and is a finite computation on the rectangle.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_profile/lean/SecondProfile/Carry.lean::collapsed_iso`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Carry.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_profile/lean/SecondProfile/Carry.lean::separable_iso`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Carry.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_profile/lean/SecondProfile/Classes.lean::holdsTwo_iso`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Classes.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_profile/lean/SecondProfile/Stage.lean::twoness_needs_four`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Stage.lean)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_profile/lean/SecondProfile/Stage.lean::twoness_needs_two_L`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/lean/SecondProfile/Stage.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: the second-derivation rung trees hold no Rust`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_profile/profile_rows.py::class_count`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/profile_rows.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_profile/profile_rows.py::holds_two`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_profile/profile_rows.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0473](tfq_0473_rung10_responder_adjacency_reach.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:310`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:446-453`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt:349-354`
