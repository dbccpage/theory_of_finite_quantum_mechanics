---
documentation_contract: education-documentation/v1
title: "Genesis Foundational Primitives & Seed Architectures"
kind: grammar-reference
audience:
- researchers
- engineers
- coding-agents
status: active
maturity: research
claim_status: review_required
authority_effect: "None"
source_paths:
- education/genesis_primitives/README.md
prerequisites: []
aliases:
- 001_genesis
related:
- ../pregenesis_empty_mark/README.md
- ../symmetric_group_presentations/README.md
- ../minimal_symbol_systems/README.md
- ../004_oepfp/README.md
- ../genesis_reading_notes/README.md
- ./primitives/README.md
- ./normal_forms/README.md
last_verified: 2026-10-09
---

# Genesis Foundational Primitives & Seed Architectures

Use the [reading guide](reading_guide.md) to follow the opaque seed, admitted
relations and source-specific changes. It links the new admission-floor
counterexamples and distinguishes teaching milestones from S(n) stages.

**AuthorityEffect:** None.

**2026-10-01 correction & synthesis:** the [Genesis Research Synthesis](_docs/genesis_research_and_level_engine_synthesis.md)
documents the audit showing that the primitive directory is a selected educational family, with
missing native algorithms and supplied domain extensions. Its previous
complete-extraction and blanket advanced-verification claims were withdrawn.
The research extension added concrete source admission/replay proofs, actual certification/search/export
adapters, general signed transport, and domain packets now migrated into native Rust mathematical owners (`omega_wdp`, `omega_holonomy`, `omega_quantum_physics`). The original Genesis seal remains unchanged.

This directory houses the foundational genesis primitives, seed configurations, normal forms, and carrier generation specifications for the Symbol Game and Minimal Symbol System architectures:

- [`genesis.md`](genesis.md): **Genesis: admission, observation and continuation**, the current source-grounded synthesis. The [preceding long account](archive/README.md) and its derivations remain available as history.
- [`levels/`](levels/): **Modular Level-by-Level Documentation (Level 00 to Level 100)**:
  - [`levels/README.md`](levels/README.md): **Master Index & Evidential Stratification** cataloging all 33 modular level specifications with independent carrier, premise and evidence scopes. Levels 00–21 are not a uniformly sealed theorem population.
  - Individual lessons name their supplied assumptions, precise statement, pinned source, evidence class and remaining implementation obligation.
- [`primitives/`](primitives/): **Genesis Foundational Primitives & Composed Types**:
  - [`primitives/README.md`](primitives/README.md): Master index and relational world model roadmap connecting 19 foundational categories to teaching Levels 00–21.
  - [`primitives/primitives_monograph.md`](primitives/primitives_monograph.md): Historical mathematical monograph with dated audit corrections with KaTeX signatures, field matrices, four-gate active obstruction factor theorems, and claim hygiene quads.
  - [`primitives/code/`](primitives/code/): Executable Python dataclasses and targeted unit test suite ([`test_genesis_primitives.py`](primitives/code/tests/test_genesis_primitives.py) with selected computational tests; the pinned Lean build is separately reported, including presheaf contextuality, Regge calculus simplicial complex curvature bounds and Čech gluing obstructions, and the Lake build and axiom audit gate).
  - [`primitives/lean4/`](primitives/lean4/): Formal Lean 4 Lake package with [`lakefile.lean`](primitives/lean4/lakefile.lean), [`lean-toolchain`](primitives/lean4/lean-toolchain) (pinned to `leanprover/lean4:v4.34.0`), and [`AxiomAudit.lean`](primitives/lean4/AxiomAudit.lean) (nine local theorem declarations; fresh 4.33.1 compatibility evidence and the unchanged 4.34.0 pin are distinguished in the audit).
- [`demos/`](demos/): **Genesis Educational & Architectural Demonstrations**:
  - [`demos/README.md`](demos/README.md): Master documentation of the 12-stage Genesis ascent, Category 12 sheaf contextuality, and Category 5 Regge calculus Čech curvature bounds.
  - [`demos/demo_01_genesis_ascent.py`](demos/demo_01_genesis_ascent.py): Executable ladder from admission examples to separately supplied Boson/Fermion exchange examples and `presentation -> instance -> regime -> comparison -> eval -> auth`.
  - [`demos/demo_02_observer_presheaf_cech_bell.py`](demos/demo_02_observer_presheaf_cech_bell.py): Historical binary contextuality illustration. The checked helper evaluates all eight CHSH facets and compatible normalized distributions; its scalar diagnostic is not a computed Čech cohomology class.
  - [`demos/demo_03_regge_cech_curvature.py`](demos/demo_03_regge_cech_curvature.py): Executable higher-dimensional Regge calculus suite evaluating discrete deficit angles, validating discrete Gauss-Bonnet $\sum \epsilon = 2\pi\chi(K)$, certifying discrete curvature bounds, and illustrating a supplied curvature diagnostic without proving Čech gluing equivalence $\gamma_{\check{C}} = |\epsilon|$.
  - [`demos/demo_04_sheaf_hott_quantum_regge.py`](demos/demo_04_sheaf_hott_quantum_regge.py): Historical advanced-helper illustrations. Identity/equivalence flags and broad sheaf/gravity claims have explicit countermodels; use the checked audit and extension for current evidence.
- [`normal_forms/`](normal_forms/): **Normal Forms & Extended Form Contracts**:
  - [`normal_forms/README.md`](normal_forms/README.md): Governance index and formal standard mapping against `standard.yaml`.
  - Canonical form contracts governing derivation, observer profiles, authority firewalls, and evidence provenance:
    - [`nf.derivation.apnf.yaml`](normal_forms/nf.derivation.apnf.yaml): Constructive Apartness Normal Form (declared irreflexivity, symmetry and cotransitivity).
    - [`nf.derivation.ignf.yaml`](normal_forms/nf.derivation.ignf.yaml): Isomorphism Gauge Normal Form ($S_n$ automorphism quotient, canonical orbit representatives and retained transport).
    - [`nf.derivation.irnf.yaml`](normal_forms/nf.derivation.irnf.yaml): Integer Ray Normal Form (exact integer weights, primitive representative and retained positive scale).
    - [`nf.derivation.lsnf.yaml`](normal_forms/nf.derivation.lsnf.yaml): Lawful Skeletal Filtration Normal Form (parent availability, face closure and signed boundaries).
    - [`nf.epistemic.efnf.yaml`](normal_forms/nf.epistemic.efnf.yaml): Endogenous Fidelity Normal Form (No-Outside invariant, symmetry-breaking witnesses).
    - [`nf.runtime.mtnf.yaml`](normal_forms/nf.runtime.mtnf.yaml): Mazurkiewicz Trace Normal Form (DDC 8-letter transition alphabet, trace commutation).
- [`scripts/`](scripts/):
  - [`scripts/generate_genesis_svgs.py`](scripts/generate_genesis_svgs.py): Deterministic generator for the first ten schematics (00–09); twelve later SVGs are retained separately. Diagram coverage is not a proof census.
- [`_images/`](_images/): **First 22 Levels of Genesis (Metatheoretic Schematics & Post-Pin Research Estate Evolution)**:
  - [`genesis_00_presentation_void.svg`](_images/genesis_00_presentation_void.svg): Level 0 — Presentation Void & Supply No-Op (`present(x) / R -> R`)
  - [`genesis_01_external_admission_datum.svg`](_images/genesis_01_external_admission_datum.svg): Level 1 — External Supply & Datum Admission (`D -> D U {x}`)
  - [`genesis_02_primitive_difference_separation.svg`](_images/genesis_02_primitive_difference_separation.svg): Level 2 — Primitive Difference & Persistent Separation (`Q -> Q U {(i, j)}`)
  - [`genesis_03_judgment_form_arities.svg`](_images/genesis_03_judgment_form_arities.svg): Level 3 — Judgment-Form Arities & Declarations (`F -> F ++ [n]`)
  - [`genesis_04_instance_admission.svg`](_images/genesis_04_instance_admission.svg): Level 4 — Instance Admission & Asserted Tuples (`I -> I U {f(a)}`)
  - [`genesis_05_metatheoretic_regime_state.svg`](_images/genesis_05_metatheoretic_regime_state.svg): Level 5 — Metatheoretic Regime State (`R = (D, F, I, U, Q)`)
  - [`genesis_06_minimal_candidate_response.svg`](_images/genesis_06_minimal_candidate_response.svg): Level 6 — Minimal Candidate Responses & Cost Floor (`μ₁ = 2`, `μ₂`)
  - [`genesis_07_observational_context_profiles.svg`](_images/genesis_07_observational_context_profiles.svg): Level 7 — Observational Contexts & Profile Collapse (`Prof_R(d)`)
  - [`genesis_08_structural_isomorphism_quotient.svg`](_images/genesis_08_structural_isomorphism_quotient.svg): Level 8 — Structural Isomorphism Quotient & Token Erasure (`R₁ ≅ R₂`)
  - [`genesis_09_readings_branch_closure.svg`](_images/genesis_09_readings_branch_closure.svg): Level 9 — Surviving Readings Branching & Separation Closure (`Reading L vs F`)
  - [`genesis_10_epistemic_quarantine.svg`](_images/genesis_10_epistemic_quarantine.svg): Level 10 — Epistemic Quarantine & Axiom Containment (`{propext, Quot.sound}`)
  - [`genesis_11_trace_algebra_confluence.svg`](_images/genesis_11_trace_algebra_confluence.svg): Level 11 — Trace Algebra & Confluence Gate (`rw_confluent` & Unique Normal Forms)
  - [`genesis_12_deterministic_replay_export.svg`](_images/genesis_12_deterministic_replay_export.svg): Level 12 — Deterministic Replay & Evidence Serialization (40 JSON Exports & Byte Replay)
  - [`genesis_13_primitive_passage_routing.svg`](_images/genesis_13_primitive_passage_routing.svg): Level 13 — Primitive Passage Routing (Two-Rule Repair vs Lift Routing)
  - [`genesis_14_search_exhaustion_gate.svg`](_images/genesis_14_search_exhaustion_gate.svg): Level 14 — Search Exhaustion & Bounded Gate (Budget Stop `UNKNOWN` vs Proved Obstruction)
  - [`genesis_15_progress_licensing_contract.svg`](_images/genesis_15_progress_licensing_contract.svg): Level 15 — Alpha Progress Licensing Contract (Progress Contract & R-B-G Authority)
  - [`genesis_16_presentation_descent_coherence.svg`](_images/genesis_16_presentation_descent_coherence.svg): Level 16 — Presentation Descent & Retract Coherence ($d \circ u = \text{id}$ & NB-16 Transport)
  - [`genesis_17_digest_identity_compression.svg`](_images/genesis_17_digest_identity_compression.svg): Level 17 — Digest Identity Compression (`regime_sha256` & `dup_no_refine`)
  - [`genesis_18_discrete_cochain_fencing.svg`](_images/genesis_18_discrete_cochain_fencing.svg): Level 18 — Discrete Cochain & Exact Rational Fencing (Exact Rational $\mathbb{Q}$ & `FloatProbabilityError`)
  - [`genesis_19_spectral_zeta_fencing.svg`](_images/genesis_19_spectral_zeta_fencing.svg): Level 19 — Spectral Zeta & Characteristic Polynomial Fencing (Integer Characteristic Polynomial Fence)
  - [`genesis_20_autopoietic_reflection_symmetry.svg`](_images/genesis_20_autopoietic_reflection_symmetry.svg): Level 20 — Autopoietic Reflection & Symmetry Breaking (`Breaking.cycle_detected` & Floor)
  - [`genesis_21_combinatorial_simplex_ceiling.svg`](_images/genesis_21_combinatorial_simplex_ceiling.svg): Level 21 — Explicit Four-Simplex & Supplied Boundary (`LadderGeneral.d4_demo`)
- **Opaque & Explicit Seeds:** Canonical representations of initial configurations prior to level-ascent iteration.
- **Primitive Difference Carrier:** Carrier honesty, gauge-invariance verification, and root seed derivations.

## Integration with the central paper

The [Genesis/WDP crosswalk](wdp_integration.md) records existing coverage,
source grades and native owners. The [shared language boundary](normal_forms/shared_language_boundary.md)
connects the 14 draft form contracts to the existing AutoP/PTIR compiler and a
proposed first SQL target. APNF and IRNF use the meanings of their actual YAML
contracts; labels, flags and diagram titles do not establish executable proofs.

## Architectural Strands & System Boundaries

The canonical documentation architecture comprises:

0. **[`../symmetric_group_presentations`](../symmetric_group_presentations):** The symbolic presentation ($S(n)$) and survivor series ($s_n$) carrier history strand.
1. **[`../minimal_symbol_systems`](../minimal_symbol_systems):** The Minimal Symbol System (MSS-0 to MSS-100) normative specifications, stage verifiers, and schematics.
2. **`genesis_primitives/`:** The Genesis foundational primitives, seed configurations, and primordial carrier specifications.
3. **[`../004_oepfp`](../004_oepfp):** The proposer-host evaluation protocol, Proposal Fidelity Protocol (PFP), and runtime execution gates.
4. **[`../005_genesis_ongoing`](../005_genesis_ongoing):** Active research trajectories, post-closure ascent extensions, and open frontiers.
5. **[`../witnessed_difference_programme`](../witnessed_difference_programme):** The Witnessed Difference Programme (WDP) curriculum, monographs, and finite measurement foundations.

## Layout and naming

| Path | Role |
| --- | --- |
| `README.md`, `reading_guide.md` | Scope and reading order. |
| `genesis.md` | The Genesis text: stages, admissions, obligations. |
| `wdp_integration.md` | How this strand hands off to the Witnessed Difference Programme. |
| `grammar/genesis.ebnf`, `grammar/genesis_conformance_cases.json` | Presentation and event grammar with its replayed cases. |
| `code/check_genesis.py`, `code/tests/test_genesis_grammar.py` | Grammar checker and its test; `verify-strand 001` runs the checker. |
| `levels/level_NN_<slug>.md` | Teaching levels in order. |
| `primitives/` | The 19 primitive categories, Python and Lean 4 side by side. |
| `adversarial_verification/`, `research_extension/` | Executed audits and extensions with their own manifests and tests. |
| `normal_forms/`, `demos/`, `scripts/`, `_images/` | Contracts, demos, scripts, figures. |

Convention shared with `pregenesis_empty_mark`, `symmetric_group_presentations` and `minimal_symbol_systems`:
a strand directory is `NNN_<snake_case_slug>`; its grammar is `grammar/<slug>.ebnf`
beside `grammar/<slug>_conformance_cases.json`; its checker is `code/check_<slug>.py`
with tests in `code/tests/`. The shared S(n) models live once, in `../symmetric_group_presentations/code/`.
The empty placeholder directories `contracts/`, `domains/`, `lean4/`, `papers/`,
`prompts/` and `wire_representations/` were removed on 2026-10-06; they return when
they have content. The `curriculum/` lesson tree was removed the same day.

The [source crosswalk](source_crosswalk.md) covers all 121 research directories. The [October 9 education audit](education_audit_2026-10-09.json) records the original 212-file inventory, archival hashes, fresh checks and unrun evidence populations.

## Source-checkout configuration

Use a read-only checkout of `dbccpage/19L57G1` at the revision in the source inventory, including the historical `sealed-derivation-v1` Git tag for inventory comparisons. Set `GENESIS_SOURCE_ROOT` to that checkout. On POSIX shells use `export GENESIS_SOURCE_ROOT=/path/to/19L57G1`; on PowerShell use `$env:GENESIS_SOURCE_ROOT = 'C:\path\to\19L57G1'`. The October 9 checks used Python 3.12.14 on Linux; the PowerShell spelling is configuration guidance, not a fresh Windows execution receipt.

Run the existing tests with the selected Python interpreter from the repository root. Historical Lean 4.34.0 and Python 3.14.7 receipts retain their original scope. Fetching the exact historical tag supplies Git metadata; it does not alter the frozen source tree or justify claiming its proofs were recompiled.
