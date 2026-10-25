# [TFQ-0558] wdp-handoff-to-l1

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `315f5352-fe40-5e3f-89d1-0633412de97d`  
> **Parent Derivation**: [TFQ-0557](tfq_0557_wdp_synthesis_trunk_tiers.md)

---

## 1. Abstract & Formal Statement

Narrowed boundary, status left OPEN. On one triangle with edges (01, 12, 02) and unit integer weights, the coboundary of vertex values (f0, f1, f2) is (f1 - f0, f2 - f1, f2 - f0), and the face of an edge triple (x01, x12, x02) is x01 + x12 - x02. For every integer edge triple and every integer vertex repair, the unit l1 length of the residual is at least the absolute face value. When the face is negative, the repair (0, h01, h01 + h12) leaves residual (0, 0, -face); otherwise the repair (0, h01 - face, h02) leaves residual (face, 0, 0). Both residuals have unit l1 length equal to the absolute face value, so on this triangle that length is the distance to integer coboundaries. A face of 0 means the edge triple is the coboundary of the non-negative repair. Vertex values (0, 1, 0) have coboundary l1 length 2, the edge triple (1, -1, 0) is that coboundary, and the residual of (1, -1, 0) against itself has length 0, so 2 is not the quotient value. The edge triple (1, 0, 0) has face 1. The verdict of (1, 1) is 0 and the verdict of (0, 0) is 1. Equal fibre decisions (1, 1) pass and (0, 1) does not.

### Governing Obligation
Keep the certified window open beyond this triangle: weighted l1 over the rationals, a bounded-circulation dual on a general carrier, the second coboundary diagnostic, and a checked adapter before any LGGR verdict reads the quotient value as a coboundary length.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Terminal for the WDP stage on the original window. This triangle case does not identify WDP's quotient value with 007's coboundary length (the LGGR crate's register_stabilized_family consumes verified quotient evidence for ClosedResidual families only), does not make the two window quantities sector weights or a quantum state (TFQ-0004), and does not derive the L1 stage. The weighted certificate over the rationals, the bounded-circulation dual on a general carrier, the LGGR adapter, sector weights, general complexes, and the full diagnostic trichotomy stay open. A face of 0 is an integer coboundary on this triangle only.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwWdpHandoffToL1.lean::closed_verdict`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::distance_at_least`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::equal_report_passes`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::face_of_obstruction`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::face_zero_is_coboundary`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::leakage_is_not_quotient`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::meet_neg`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::meet_nonneg`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::obstructed_verdict`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::repair_residual_neg`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::repair_residual_nonneg`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- [`lean4/CampaignPgwWdpHandoffToL1.lean::unequal_report_fails`](../../../lean4/CampaignPgwWdpHandoffToL1.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_local_green_global_red_lggr/src/ledger.rs::register_stabilized_family`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine/crates_rs/omega_local_green_global_red_lggr/src/ledger.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-wdp-handoff-to-l1.py::main`](../../../checks/independent/pgw-wdp-handoff-to-l1.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::obstruction_signature`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:1487-1498`
  - `omega_engine_education/documentation/007_oelggr/local_green_global_red_foundational_series.md:147-161`
  - `omega_engine_education/documentation/007_oelggr/curriculum/1000_local_green_global_red_foundations/concepts/lesson_1000_01_local_green_global_red_foundations.md:116-120`
  - `dag/derivations/independent/pgw-wdp-handoff-to-l1.md:5`
  - `dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json:6`
