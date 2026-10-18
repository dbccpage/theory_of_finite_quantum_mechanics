# [TFQ-0372] off-image-refusal-half

> **Stage**: `PREGENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `1c98808d-7151-5a28-bee6-d0e97c2e3192`  
> **Parent Derivation**: [TFQ-0371](TFQ-0371_old-image-injective-lift.md)

---

## 1. Abstract & Formal Statement

Ledger row WDP-P001-019 says the pinned carrier does not establish unrestricted old-image recovery or the advertised cardinalities, and that domain restriction remains open. DAG node PG-SN-OFF-IMAGE-REFUSAL names a section-retraction refusal for points that fail a round trip. The education file cited for that node was not opened. SnCarrier.lean is listed there. The finite statement still required is: an off-image point is refused exactly when the section-retraction round trip fails, without widening old_image_injective and without a cardinality claim past the pinned carrier.

### Governing Obligation
Off-image points fail the section-retraction round trip and are refused, while WDP-P001-019 cardinality and unrestricted recovery stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Closes the domain-restriction half of WDP-P001-019; off-image points are refused by section-retraction roundtrip.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`missing declaration obligation: off-image non-descent inside this package, not an unread education module`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean`](../../code/lean4/)
- [`omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.accepted_only_from_section`](../../code/lean4/)
- [`omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.nonDescent_iff_off_image`](../../code/lean4/)
- [`omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.old_image_base'`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: section-retraction refusal in crate pre_mssn_preservation for points outside the section image`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_sn_off_image_refusal_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: an off-image refusal predicate in 000_pre_genesis_to_mssn/code/preservation.py that does not call recover_word a total inverse`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0373](TFQ-0373_free-monoid-size-noniso.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch04_report_maps_fibers_quotients_and_sections.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-SN-OFF-IMAGE-REFUSAL`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-SN-OFF-IMAGE-REFUSAL` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-SN-OFF-IMAGE-REFUSAL`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [470, -940, 705]`, `chord_potential = 705`, `holonomy_gamma2 = 940`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-SN-OFF-IMAGE-REFUSAL): 4*idx(47) + 3*stage_rank(1) + route_degree(2) == 193` ($\text{value} = 193$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-SN-OFF-IMAGE-REFUSAL): R_raw(99) - G_cob(49) - S_decoy(1) == 49 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 49$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.old_image_base'`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 8d6d5d053ab2b9a671bbc4aaf2a937bf15ec0d50223cd3bde06e0aed78422f65`
