# [TFQ-0519] sn-protected-answer-transport

> **Stage**: `MSSN_SN` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `26db6fbc-6946-5835-975b-48f71515ff5a`  
> **Parent Derivation**: [TFQ-0518](tfq_0518_sn_off_image_refusal_proposal.md)

---

## 1. Abstract & Formal Statement

S(6) recovers the old image exactly, but transporting a protected answer F across the lift u requires a target counterpart F′ with F′∘u = F, and preserving future operations requires the corresponding commuting transition equations. In Lean 4, OldImageLaw u r yields canonical retraction-induced transport retractionTransport r F d satisfying F′∘u = F (retraction_transport_law) and canonical transition lifts (canonical_transition_lift_commutes), including for SnCarrier (snCarrier_answer_transport, snCarrier_canonical_transition_square) and the integer S6Descent slice model (s6Descent_answer_transport, s6Descent_canonical_transition_square), while k-step commuting squares preserve transported answers (commuting_square_preserves_transported_answer). Off the image, F′ has |Q|^(|B|−|A|) counterparts (transport_counterpart_card, transport_off_image_underdetermined), unconstrained target transitions violate preservation (snCarrier_transition_counterexample, s6Descent_transition_counterexample), and the old-image identity alone establishes neither a logical conservative extension off the image (not_conservative_extension_off_image), nor an adjunction (old_image_not_right_inverse, old_image_not_left_galois_adjunction), nor resolution of an unrelated demand (unrelated_demand_not_resolved_by_lift, snCarrier_s6_demand_active).

### Governing Obligation
For each protected answer F supply F′ with F′∘u = F (such as retractionTransport r F d under OldImageLaw u r), and for each future admitted event supply and check the commuting transition square before claiming that the lift preserves that answer or operation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0335](tfq_0335_from_typed_old_image_recovery_record_injectivity_of_the_lift_only_and_refuse.md) From typed old-image recovery, record injectivity of the lift only, and refuse

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The canonical retraction-induced transport, counterpart count, k-step commuting-square preservation, SnCarrier and integer S6Descent instances, and non-implication countermodels are checked in Lean 4; the node remains OPEN because arbitrary future target transitions require case-by-case commuting-square verification, the external Python S6Descent class in 002_oesn/code/sn_core.py is outside this checkout, and the exercise value s₆ = 1 records an issued descent-checking obligation, not a forced survivor.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.canonical_transition_lift_commutes`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.commuting_square_iff_boolean_answers_preserved_on_image`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.commuting_square_preserves_transported_answer`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.not_conservative_extension_off_image`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.old_image_not_left_galois_adjunction`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.retraction_transport_law`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.s6Descent_answer_transport`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.s6Descent_transition_counterexample`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.snCarrier_answer_transport`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.snCarrier_canonical_transition_square`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.snCarrier_transition_counterexample`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.transport_counterpart_card`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.transport_off_image_underdetermined`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)
- [`lean4/CampaignSnProtectedAnswerTransport.lean::CampaignSnProtectedAnswerTransport.unrelated_demand_not_resolved_by_lift`](../../../lean4/CampaignSnProtectedAnswerTransport.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of answer transport across a lift`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-sn-protected-answer-transport.py::main`](../../../checks/independent/pgw-sn-protected-answer-transport.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md:237`
  - `omega_engine_education/documentation/002_oesn/levels/level_06_tower_extension_retraction.md:39-42`
  - `omega_engine_education/documentation/002_oesn/sn.md:97-99`
  - `dag/derivations/independent/pgw-sn-protected-answer-transport.md:13-18`
