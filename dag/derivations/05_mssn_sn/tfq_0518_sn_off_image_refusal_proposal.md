# [TFQ-0518] sn-off-image-refusal-proposal

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `732546f5-4026-55ca-9ede-9bf086bd82ba`  
> **Parent Derivation**: [TFQ-0517](tfq_0517_sn5_continuation_recorded_request.md)

---

## 1. Abstract & Formal Statement

For the pinned education SnCarrier model, SnOffImage.lean compiles the domain restriction of the S(6) retraction law: retractionDownMap n p = accepted q implies p = sectionLift n b and q = b.toPresentation for some base presentation b (accepted_only_from_section), refusal holds exactly off the section image (nonDescent_iff_off_image), the witness b is unique (sectionLift_injective), a lift at stage m ≠ n is refused by r_n (retraction_stage_strict), and image membership is a Bool test computed from the syntax (inImage_iff). With old_image_base this gives a left inverse on the image and refusal off it. The accompanying note is a proposal with AuthorityEffect None and records a Lean 4.34.0 build whose six axiom lines stay within propext and Quot.sound.

### Governing Obligation
Show that retractionDownMap n accepts exactly the images of sectionLift n, with a unique witness, an exact stage test and a decidable image test, inside the five base shapes of the pinned carrier.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Pinned education SnCarrier model: BasePresentation, sectionLift and retractionDownMap in 002_oesn/lean4/SnCarrier.lean (assumption)`

### Further Prerequisites
- [TFQ-0335](tfq_0335_from_typed_old_image_recovery_record_injectivity_of_the_lift_only_and_refuse.md) From typed old-image recovery, record injectivity of the lift only, and refuse
- [TFQ-0372](../01_pregenesis/tfq_0372_off_image_refusal_half.md) off-image-refusal-half

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A proposal only: ledger row WDP-P001-019 is untouched and TFQ-0372 is not discharged by this record; the corrected cardinality theorem, OB-1, carrierCard, the wire grammar, the Python codec and any stage beyond the five base shapes are outside its scope, and S6Descent checks the separate integer example u(x) = (x,0).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean::accepted_only_from_section`](../../../lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean)
- [`lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean::inImage_iff`](../../../lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean)
- [`lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean::nonDescent_iff_off_image`](../../../lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean)
- [`lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean::retraction_stage_strict`](../../../lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean)
- [`lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean::sectionLift_injective`](../../../lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust implementation of the SnCarrier retraction`

### Python Oracles & Numerical Evaluators
- `omega_engine_education/documentation/002_oesn/code/sn_core.py::S6Descent` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0519](tfq_0519_sn_protected_answer_transport.md)
- [TFQ-0520](tfq_0520_sn_postnikov_refusal.md)
- [TFQ-0521](tfq_0521_sn_representation_quotient.md)
- [TFQ-0528](tfq_0528_mssn_atlas_not_derivation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `lean4/Imported/SymmetricGroupPresentations/SnOffImage.lean:19-23`
  - `omega_engine_education/documentation/002_oesn/docs/off_image_refusal_note.md:155-158`
  - `omega_engine_education/documentation/002_oesn/docs/off_image_refusal_note.md:98-99`
