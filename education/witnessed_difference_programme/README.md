---
documentation_contract: education-documentation/v1
title: "The Witnessed Difference Programme (WDP)"
kind: grammar-reference
audience:
  - researchers
  - engineers
  - coding-agents
status: active
maturity: production
claim_status: source-grounded
authority_effect: "None"
source_version: "2.4.1"
source_paths:
  - atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md
  - atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md
prerequisites:
  - ../symmetric_group_presentations/README.md
  - ../minimal_symbol_systems/README.md
aliases:
  - wdp
  - witnessed_difference_programme
related:
  - ../symmetric_group_presentations/README.md
  - ../minimal_symbol_systems/README.md
  - ../genesis_primitives/README.md
  - ../004_oepfp/README.md
  - ../005_genesis_ongoing/README.md
  - ./levels/README.md
last_verified: 2026-10-11
---

# The Witnessed Difference Programme (WDP)

The [reading and learning guide](reading_guide.md) gives a seven-step study
route and a worked example that separates raw repair classes from closed
cohomology. The [admission and transport lab](curriculum/710_wdp_finite_obstruction/concepts/lesson_710_04_admission_and_transport.md)
connects exact examples to the current Lean proofs and native mathematical owners.

The [observation budgets lesson](curriculum/710_wdp_finite_obstruction/concepts/lesson_710_05_observation_budgets_and_cost.md)
is new for edition 2.4.1. It follows the monograph's theorem map result
R15 (Appendix T, WDP-DIM-1 and WDP-DIM-R) and the cost appendices that
reuse it (§14.6, Appendices X and Y), and it links each topic to its native
`omega_wdp` module. The monograph reports three kinds of completion
separately: written theorems, mechanized Lean statements and executed
implementations. This course keeps the same three labels.

The merged [CODA reading route](curriculum/coda_reading_route.md),
[Prime reading route](curriculum/prime_reading_route.md), and
[DDC reading route](curriculum/ddc_reading_route.md) now live in this course.
Their source notes are in [domains/coda](domains/coda/README.md),
[domains/prime](domains/prime/README.md), and [domains/ddc](domains/ddc/README.md).
Differing historical normal-form inputs are retained separately from the corrected WDP contracts.

**AuthorityEffect:** None.\
**Curriculum scope:** Levels 00–23 and Level 100 across Parts I–V.\
**Source monograph:** *The Witnessed Difference Programme: From Finite Distinction to Witnessed Measurement*, edition 2.4.1 (2026-10-11), [`witnessed_difference_programme.md`](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md). Start with its [theorem map](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md#theorem-map-when-a-presentation-preserves-the-question) (R1–R15).\
**Claim authority:** the monograph's single live ledger, [`witnessed_difference_programme_claim_ledger.md`](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md).\
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0).

---

## 1. What the programme is

The Witnessed Difference Programme asks how much mathematical structure can be
made explicit when one begins with an exhibited difference and refuses to
smuggle in an observer, a clock, a probability space, a quantum state, or an
authority relation.

This strand is structured into canonical derivation level specifications under [`levels/`](levels/README.md). Each level file states its exact status, definitions, worked examples, and evidence bindings.

---

## 2. Derivation Levels Register

| Level | Ch. | Part | Title and focus | Diagram | Level Specification |
| :---: | :---: | :---: | :--- | :--- | :---: |
| **00** | 1 | I | **The admitted cut:** the package $(X,E,\tau,\mathcal K)$; irreflexivity and orientation are declared, not derived. | [`wdp_00`](_images/wdp_00_admitted_cut.svg) | [`level_00_admitted_cut.md`](levels/level_00_admitted_cut.md) |
| **01** | 2 | I | **Residuals and the typed witness taxonomy:** residual before witness; seven non-coercing witness roles. | [`wdp_01`](_images/wdp_01_residuals_witness_taxonomy.svg) | [`level_01_witness_function.md`](levels/level_01_witness_function.md) |
| **02** | 3 | I | **Symmetry, nonselection, and the price of retention:** no equivariant point choice on a bare set; retention countermodels CM1–CM5. | [`wdp_02`](_images/wdp_02_symmetry_nonselection_retention.svg) | [`level_02_residuals_obstructions.md`](levels/level_02_residuals_obstructions.md) |
| **03** | 4 | I | **Finite cochains, quotients, and certificates:** the signature $(\Phi_1,\Gamma_2,R_{cl})$; dual certificates without strong duality. | [`wdp_03`](_images/wdp_03_finite_cochains_quotients_certificates.svg) | [`level_03_discrete_complex_cochains.md`](levels/level_03_discrete_complex_cochains.md) |
| **04** | 5 | I | **Optional quantum-capable carriers:** declared $U(1)$ connections, holonomy, connection Laplacians. | [`wdp_04`](_images/wdp_04_optional_quantum_carriers.svg) | [`level_04_boundary_separation_contraction.md`](levels/level_04_boundary_separation_contraction.md) |
| **05** | 6 | II | **Recurrence, succession, and constitutive order:** no external clock in the definition. | [`wdp_05`](_images/wdp_05_recurrence_succession_constitutive_order.svg) | [`level_05_retention_discrete_succession.md`](levels/level_05_retention_discrete_succession.md) |
| **06** | 7 | II | **Duration, exactness, periods, and clocks:** declared valuations and path independence. | [`wdp_06`](_images/wdp_06_duration_exactness_clocks.svg) | [`level_06_finite_event_valuations.md`](levels/level_06_finite_event_valuations.md) |
| **07** | 8 | II | **Multiplicity, additive weight, and finite probability:** matching before number. | [`wdp_07`](_images/wdp_07_multiplicity_additive_weight_probability.svg) | [`level_07_finite_probability_multiplicity.md`](levels/level_07_finite_probability_multiplicity.md) |
| **08** | 9 | II | **Probability scope fences:** five notions of probability kept apart. | [`wdp_08`](_images/wdp_08_probability_scope_fences.svg) | [`level_08_discrete_observer_layer.md`](levels/level_08_discrete_observer_layer.md) |
| **09** | 10 | III | **A layered observer architecture:** presentation, memory, evaluator, policy. | [`wdp_09`](_images/wdp_09_layered_observer_architecture.svg) | [`level_09_behavioral_quotients_finite_states.md`](levels/level_09_behavioral_quotients_finite_states.md) |
| **10** | 11 | III | **Intersubjective presentation, descent, and redundancy:** local satisfiability is not global satisfiability. | [`wdp_10`](_images/wdp_10_intersubjective_presentation_descent.svg) | [`level_10_observation_measurement_calibration.md`](levels/level_10_observation_measurement_calibration.md) |
| **11** | 12 | III | **The observation ladder:** five levels and their failure modes. | [`wdp_11`](_images/wdp_11_observation_ladder.svg) | [`level_11_linear_sensing_projection.md`](levels/level_11_linear_sensing_projection.md) |
| **12** | 13 | III | **Measurement as a typed extension of observation:** calibration, uncertainty, traceability, provenance. | [`wdp_12`](_images/wdp_12_measurement_typed_extension.svg) | [`level_12_context_interference_state_spaces.md`](levels/level_12_context_interference_state_spaces.md) |
| **13** | 14 | III | **Self-reference and the awareness boundary:** blind spots and the awareness firewall. | [`wdp_13`](_images/wdp_13_self_reference_awareness_boundary.svg) | [`level_13_self_reference_gaps_fixed_points.md`](levels/level_13_self_reference_gaps_fixed_points.md) |
| **14** | 15 | III | **Authority is a separate layer:** typed authority and its separations. | [`wdp_14`](_images/wdp_14_authority_separate_layer.svg) | [`level_14_traceability_provenance_receipts.md`](levels/level_14_traceability_provenance_receipts.md) |
| **15** | 16 | IV | **Spatial/history diagnostics and the curved-complex fork:** presentation descent, chain contractions, truncation leakage. | [`wdp_15`](_images/wdp_15_spatial_history_diagnostics_curved_complex.svg) | [`level_15_simplicial_branch.md`](levels/level_15_simplicial_branch.md) |
| **16** | 17 | IV | **Finite weighted histories:** semiring path sums and cancellation. | [`wdp_16`](_images/wdp_16_finite_weighted_histories.svg) | [`level_16_discrete_deformation_dynamics.md`](levels/level_16_discrete_deformation_dynamics.md) |
| **17** | 18 | IV | **Quantum reconstruction as an audit:** a finite operational package and its classical corner. | [`wdp_17`](_images/wdp_17_quantum_reconstruction_audit.svg) | [`level_17_semiring_coarse_graining.md`](levels/level_17_semiring_coarse_graining.md) |
| **18** | 19 | IV | **The unpaid quantum interfaces:** what a reconstruction would still have to pay for. | [`wdp_18`](_images/wdp_18_unpaid_quantum_interfaces.svg) | [`level_18_exact_rational_bounds.md`](levels/level_18_exact_rational_bounds.md) |
| **19** | 20 | V | **Relative completeness for observer-indexed presentations:** a five-valued status algebra. | [`wdp_19`](_images/wdp_19_relative_completeness_observer_presentations.svg) | [`level_19_quantum_reconstruction_audit.md`](levels/level_19_quantum_reconstruction_audit.md) |
| **20** | 21 | V | **Falsifiers, nonclaims, and open obligations:** what would refute the programme and what remains open. | [`wdp_20`](_images/wdp_20_falsifiers_nonclaims_open_obligations.svg) | [`level_20_finite_adequacy_continuum_limits.md`](levels/level_20_finite_adequacy_continuum_limits.md) |
| **21** | 22 | V | **Synthesis:** trunk, observer/measurement waist, branches, and the four-tier ambition hierarchy. | [`wdp_21`](_images/wdp_21_synthesis_finite_calculus.svg) | [`level_21_open_horizon_claim_ledger.md`](levels/level_21_open_horizon_claim_ledger.md) |
| **22** | Ext. | Ext. | **Genesis to WDP Foundational Bridges:** 11 derivation bridges connecting Genesis to WDP. | — | [`level_22_genesis_to_wdp_bridges.md`](levels/level_22_genesis_to_wdp_bridges.md) |
| **23** | Ext. | Ext. | **Sovereign Difference Grounding:** autonomous difference primitives and native Rust mathematical owners. | — | [`level_23_sovereign_difference_grounding.md`](levels/level_23_sovereign_difference_grounding.md) |
| **100** | Term. | Term. | **Terminal Claim Ledger Gate:** cryptographic SHA-256 byte digests and 154-row ledger gate. | — | [`level_100_terminal_claim_ledger.md`](levels/level_100_terminal_claim_ledger.md) |

---

## 3. Subdirectories

1. **[`levels/`](levels/README.md):** comprehensive Derivation Levels index and dedicated specification pages (Level 00 to Level 23, Level 100, plus domain levels for [`coda/`](levels/coda/), [`prime/`](levels/prime/), and [`ddc/`](levels/ddc/)).
2. **[`curriculum/`](curriculum/README.md):** pedagogical laboratory tracks (Track 700 Overview, Track 710 Finite Obstruction Calculus, Track 720 Derivation Levels, Track 730/740 CODA, Track 750/760 Prime, Track 770/780 DDC), with lesson concepts and interactive Jupyter notebooks.
3. **[`domains/`](domains/README.md):** integrated mathematical domains for [CODA](domains/coda/), [Prime Algorithms](domains/prime/), and [DDC](domains/ddc/).
4. **[`normal_forms/`](normal_forms/README.md):** canonical normal form contracts across WDP, CODA, Derivation, Epistemic, and DDC families.
5. **[`_images/`](_images/):** teaching diagrams (`wdp_00_...svg` to `wdp_21_...svg`, and `ddc_01_...svg` to `ddc_08_...svg`).
