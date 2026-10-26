Q canonical claim and status ledger
===================================

> **Local Lean in this package.** Mechanization shipped here is `lean4/coda_q_*.lean` (namespace `CodaQ`), a small declaration-schema slice (mode-being unpacking, admission-debt records, profile-collision firewall). It does **not** replay `omega_engine` `Paper_Q` / generated `paper_9999` 98× `MECHANIZED` rows. Citations of `Paper_Q.*` below are historical pointers, not files in this checkout.

**Paper:** `coda_q.md` — Level Q v1.0.2 Pre-Print: Quarantined Frontier Probes Beyond the Finite-Shadow Tower
**Document ID:** OMEGA-Q-1.0
**Canonical reconciliation:** G8, 2026-07-17
**Status authority:** historical generated `paper_9999.md` is **not in this checkout**; this file is a readable paper-to-ENC crosswalk, not an independent status mint. Local evidence is `lean4/coda_q_*.lean` plus `code/tests/test_coda_q.py`.

This ledger types the claims in `paper.md` according to the repository's paper
hygiene discipline. Mathematical status, Lean status, and proof-source home are
independent axes. A local `[MECHANIZED]` label means only that the named finite
or quotient statement has a checked Lean realization. It does not certify a
domain ontology, the CODA-FDA `Authority_S` pipeline, or categorical authority
non-creation.

Exact generated vector
----------------------

Generated `paper_9999.md` contains exactly 105 entries:

| Axis | Exact vector |
| --- | --- |
| mathematical status | 7 `DEFINED`; 98 `MECHANIZED` |
| Lean status | 100 `MECHANIZED`; 5 `NOT-PLANNED` |
| source layer | 94 `q`; 11 `quantum` |

The vector is exhaustively described by these ranges:

* `ENC-0935..0939`: `DEFINED / NOT-PLANNED`;
* `ENC-0940` and `ENC-0953`: `DEFINED / MECHANIZED`;
* `ENC-0943..0952`, `ENC-0954..1029`, `ENC-1154..1163`, `ENC-1165`, and
  `ENC-1166`: `MECHANIZED / MECHANIZED`;

* `ENC-1154..1163` and `ENC-1166`: source layer `quantum`, checked in
  QM/PaperAF000 rather than native `Paper_Q`;

* all other rows, including exceptional `ENC-1165`: source layer `q`.

The active paper table has 109 rows. This is not a competing 109-entry status
vector: Q-A3 groups six separate ENC definitions, while nine local protocol,
scope, worked-example, or interpretive rows have no `paper:9999` alias. Those
nine are dispositioned explicitly below and receive no fabricated ENC id.

Paper claim table
-----------------

| ID | Claim | Paper label (not a replacement ENC status) | Basis / boundary |
| --- | --- | --- | --- |
| Q-A0 | Level Q does not use bare "being" as a primitive; mode-being means primitive descent plus terminalization under a declared engagement mode, with descent pushing forward only along declared mode refinement. | `[DEFINITION]` + `[SCOPE FENCE]` | §§4.1, 7 Q-T0. Local Lean `CodaQ.mode_being_unpacks_to_descent_and_terminalization` in `lean4/coda_q_t01_mode_descent_firewall.lean` is **definitional unfolding** (`Iff.rfl` of `ModeBeing`), not a content theorem. Historical `Paper_Q.*` names are not in this checkout. |
| Q-A1 | Level Q is a quarantine discipline for frontier questions and does not create authority. | `[DEFINITION]` + `[SCOPE FENCE]` | Defined in §§1, 3, 4. Authority remains governed by GTLA/CODA-FDA. |
| Q-A2 | Q receipts have the form $Q \to P_Q \to D(P_Q) \to \Omega_Q \to R_Q \to P_{\mathrm{next}}$. | `[DEFINITION]` | Protocol shape introduced in §§1, 6. |
| Q-A3 | Q-box, q-probe, q-packet, q-obstruction, q-residual, and q-status are formal protocol objects. | `[DEFINITION]` | Definitions 5.1-5.6. |
| Q-A4 | Q statuses are not authority terminals. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T1; Lean `Paper_Q.q_terminal_not_authority_terminal`, `Paper_Q.no_q_status_equals_authority_terminal`. Pointwise constructor disjointness in a local sum type; not the categorical CODA-FDA authority pipeline. |
| Q-A4a | Claim-machine statuses are typed receipts, not authority terminals or oracle answers. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T1a; Lean `Paper_Q.ClaimMachineStatus`, `Paper_Q.claim_machine_status_not_authority_terminal`, `Paper_Q.no_claim_machine_status_equals_authority_terminal`. Pointwise constructor disjointness only. |
| Q-A4b | QHeld admission requires complete Q debt: finite shadow, refinement relation, declared topology, convergence-certificate route, and descent trigger; TerminalWithinScope additionally requires finite witness support. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T1b; contract `omega_q_admission.contract.yaml`; Rust `omega_q::admission`; Lean `Paper_Q.QAdmissionEvidence`, `Paper_Q.qheld_admissible_iff_complete_admission_debt`, `Paper_Q.missing_finite_shadow_blocks_qheld`, `Paper_Q.missing_refinement_relation_blocks_qheld`, `Paper_Q.missing_declared_topology_blocks_qheld`, `Paper_Q.missing_convergence_certificate_route_blocks_qheld`, `Paper_Q.missing_descent_trigger_blocks_qheld`, `Paper_Q.AdmissionDebtGap`, `Paper_Q.admission_debt_gap_blocks_qheld`, `Paper_Q.admission_debt_gap_blocks_terminal_within_scope`, `Paper_Q.terminal_within_scope_without_witness_blocked`. No Q admission status mints authority. |
| Q-A5 | Finite-shadow profile collision blocks target factorization. | `[MECHANIZED]` | §7 Q-T2; Lean `Paper_Q.profile_collision_blocks_factorization`. |
| Q-A5a | Finite descent permission is exactly target factorization through the declared profile; local shadow permissions do not imply target permission. | `[DEFINITION]` + `[MECHANIZED]` | §§4.2, 7 Q-T2a; Lean `Paper_Q.FiniteDescentPermission`, `Paper_Q.local_permissions_global_permission_red`, `Paper_Q.augmented_permission_requires_profile_collision_separation`. |
| Q-A5b | Finite descent permission requires target invariance on profile fibers; a permitted target cannot separate worlds the declared profile identifies. | `[MECHANIZED]` | §7 Q-T2b; Lean `Paper_Q.TargetInvariantOnProfileFibers`, `Paper_Q.target_factorization_implies_profile_fiber_invariance`, `Paper_Q.finite_descent_permission_implies_profile_fiber_invariance`, `Paper_Q.augmented_permission_implies_augmented_profile_fiber_invariance`. |
| Q-A5c | Profile refinement preserves target factorization; adding an augmentation field preserves any target permission already present in the old finite-shadow profile. | `[MECHANIZED]` | §7 Q-T2c; Lean `Paper_Q.profile_refinement_preserves_factorization`, `Paper_Q.augmented_permission_of_finite_descent_permission`. |
| Q-A5d | A target factors through the profile-fiber quotient exactly when it is invariant on profile fibers; finite-shadow agreement gives the corresponding exact quotient carrier. | `[MECHANIZED]` | §7 Q-T2d; Lean `Paper_Q.ProfileFiberQuotient`, `Paper_Q.profile_fiber_factor_exists_iff_invariance`, `Paper_Q.finite_shadow_profile_fiber_factor_exists_iff_invariance`, `Paper_Q.finite_descent_permission_implies_profile_fiber_factorization`. |
| Q-A5e | A primitive impossibility certificate is a target-distinct profile collision; it blocks profile invariance, profile factorization, quotient factorization, and finite descent permission. | `[DEFINITION]` + `[MECHANIZED]` | §7 Q-T2e; Lean `Paper_Q.PrimitiveImpossibility`, `Paper_Q.primitive_impossibility_blocks_profile_fiber_invariance`, `Paper_Q.primitive_impossibility_blocks_profile_factorization`, `Paper_Q.primitive_impossibility_blocks_profile_fiber_factorization`, `Paper_Q.primitive_impossibility_of_finite_shadow_collision`, `Paper_Q.finite_shadow_primitive_impossibility_blocks_permission`. |
| Q-A5f | A target is determined on the observed profile image exactly when it is invariant on profile fibers; finite descent permission implies this image-relative determinacy, while primitive impossibility blocks it. | `[DEFINITION]` + `[MECHANIZED]` | §7 Q-T2f; Lean `Paper_Q.ObservedProfileDeterminesTarget`, `Paper_Q.observed_profile_determines_target_iff_profile_fiber_invariance`, `Paper_Q.finite_descent_permission_implies_observed_profile_determinacy`, `Paper_Q.primitive_impossibility_blocks_observed_profile_determinacy`. |
| Q-A5g | Any full profile decoder restricts to the observed profile image; any observed-image decoder determines realized fibers, primitive impossibility blocks it, and finite descent permission restricts to the observed finite-shadow image. | `[DEFINITION]` + `[MECHANIZED]` | §7 Q-T2g; Lean `Paper_Q.ObservedProfileImage`, `Paper_Q.observedProfileImageValue`, `Paper_Q.profile_factorization_restricts_to_observed_image`, `Paper_Q.observed_image_factorization_implies_observed_profile_determinacy`, `Paper_Q.primitive_impossibility_blocks_observed_image_factorization`, `Paper_Q.finite_descent_permission_restricts_to_observed_image`. |
| Q-A5h | Two observed-image decoders that both replay the target on every realized world are equal; observed-image terminalization has a unique decoder inside the declared packet. | `[MECHANIZED]` | §7 Q-T2h; Lean `Paper_Q.observed_image_decoder_unique`. |
| Q-A5i | Ambient profile decoders that both replay the target may disagree off image but have equal restrictions to the observed profile image; finite-shadow decoders likewise agree on the observed finite-shadow image. | `[MECHANIZED]` | §7 Q-T2i; Lean `Paper_Q.profile_factorization_observed_restrictions_unique`, `Paper_Q.finite_shadow_decoders_agree_on_observed_image`. |
| Q-A5j | Off-image decoder variance is inert: if two decoders agree on the observed profile image and one replays the target, the other replays the target too; the finite-shadow version is identical over the observed finite-shadow image. | `[MECHANIZED]` | §7 Q-T2j; Lean `Paper_Q.observed_restriction_equivalent_preserves_profile_replay`, `Paper_Q.finite_shadow_observed_restriction_equivalent_preserves_replay`. |
| Q-A5k | Target postprocessing preserves permission: if a target factors through a profile, then every declared readout of that target factors through the same profile; finite descent permission is closed under target readout maps. | `[MECHANIZED]` | §7 Q-T2k; Lean `Paper_Q.profile_factorization_postprocesses_target`, `Paper_Q.finite_descent_permission_postprocesses_target`. |
| Q-A5l | Product-target descent is exact componentwise: a paired target factors through a profile exactly when both component targets do; finite descent permission for a pair is exactly permission for each component. | `[MECHANIZED]` | §7 Q-T2l; Lean `Paper_Q.profile_pair_factorization_iff_component_factorizations`, `Paper_Q.finite_descent_permission_pair_iff_component_permissions`. |
| Q-A5m | Profile readouts cannot repair primitive impossibility: any readout of an impossible profile preserves the target-distinct collision and cannot replay the target; the same holds for readouts of bundled finite-shadow profiles. | `[MECHANIZED]` | §7 Q-T2m; Lean `Paper_Q.profile_readout_preserves_primitive_impossibility`, `Paper_Q.profile_readout_impossibility_blocks_factorization`, `Paper_Q.finite_shadow_profile_readout_impossibility_blocks_factorization`. |
| Q-A6 | Continuum LGGR: the profile factors through itself while the paired profile/target cannot factor through a colliding profile. | `[MECHANIZED]` | §7 Q-T3; Lean `Paper_Q.shadow_profile_factors_through_itself`, `Paper_Q.continuum_lggr_profile_obstruction`. |
| Q-A6a | Every declared shadow coordinate factors through the bundled profile, while a target separated by a profile collision still does not. | `[MECHANIZED]` | §7 Q-T3a; Lean `Paper_Q.all_shadow_components_factor_through_profile`, `Paper_Q.continuum_lggr_components_obstruction`. |
| Q-A7 | A successful next q-probe must separate a previous target-distinct profile collision. | `[MECHANIZED]` | §7 Q-T4; Lean `Paper_Q.augmentation_must_separate_profile_collision`. |
| Q-A7a | An added augmentation that does not separate the live target-distinct collision cannot lift red: no decoder through the augmented profile can replay the target, and augmented finite descent permission is denied. | `[MECHANIZED]` | §7 Q-T4a; Lean `Paper_Q.profile_augmentation_collision_blocks_factorization`, `Paper_Q.unseparated_augmentation_blocks_augmented_permission`. |
| Q-A7b | Any repairing profile must separate an old primitive-impossibility witness: if a new profile replays the target, it separates an old target-distinct collision; the finite-shadow form separates a pair all old shadows identified. | `[MECHANIZED]` | §7 Q-T4b; Lean `Paper_Q.repaired_permission_separates_primitive_impossibility_witness`, `Paper_Q.finite_shadow_repaired_permission_separates_collision`. |
| Q-A7c | Fiber-respecting profiles cannot repair red: if a proposed new profile preserves every old-profile collision, then it cannot replay a target blocked by an old primitive-impossibility witness; the finite-shadow form preserves all old-shadow collisions. | `[MECHANIZED]` | §7 Q-T4c; Lean `Paper_Q.fiber_respecting_profile_cannot_repair_primitive_impossibility`, `Paper_Q.finite_shadow_fiber_respecting_profile_cannot_repair`. |
| Q-A7d | Old-profile factors cannot repair red: if a proposed new profile factors through an old profile with a primitive-impossibility witness, then it cannot replay the blocked target; the finite-shadow form applies to readouts of the bundled old shadow profile. | `[MECHANIZED]` | §7 Q-T4d; Lean `Paper_Q.old_profile_factor_cannot_repair_primitive_impossibility`, `Paper_Q.finite_shadow_old_profile_factor_cannot_repair`. |
| Q-A8 | Primitive-difference continuum LGGR: a profile may descend through a residual quotient while a target-separated pair blocks paired descent. | `[MECHANIZED]` | §7 Q-T5; Lean `Paper_Q.primitive_continuum_lggr_nonpromotion`. |
| Q-A8a | Primitive-difference modulo LGGR: a profile may descend modulo a declared profile equivalence while a target that remains separated modulo its own declared equivalence blocks paired quotient descent. | `[MECHANIZED]` | §7 Q-T5a; Lean `Paper_Q.primitive_continuum_lggr_mod_nonpromotion`. |
| Q-A8b | Primitive-difference target-readout red: if a readout of a target separates a zero-related pair while the profile descends, then the paired profile/readout cannot descend through the residual quotient. | `[MECHANIZED]` | §7 Q-T5b; Lean `Paper_Q.primitive_continuum_lggr_target_readout_nonpromotion`. |
| Q-A8c | Primitive-difference product descent is componentwise: a paired readout descends through the residual quotient exactly when both component readouts descend. | `[MECHANIZED]` | §7 Q-T5c; Lean `Paper_Q.primitive_difference_pair_descends_iff_component_descents`. |
| Q-A8d | Primitive-difference modulo product descent is componentwise: a paired quotient readout descends through the residual quotient exactly when both component quotient readouts descend. | `[MECHANIZED]` | §7 Q-T5d; Lean `Paper_Q.primitive_difference_mod_pair_descends_iff_component_descents`. |
| Q-A8e | Primitive-difference modulo target-readout red: if a target readout remains separated modulo its declared equivalence on a zero-related pair, then the paired profile/readout cannot descend modulo the product equivalence. | `[MECHANIZED]` | §7 Q-T5e; Lean `Paper_Q.primitive_continuum_lggr_mod_target_readout_nonpromotion`. |
| Q-A8f | Primitive-difference descent postprocesses targets: if a target descends through the residual quotient, then every declared readout of that target also descends. | `[MECHANIZED]` | §7 Q-T5f; Lean `Paper_Q.primitive_difference_descent_postprocesses_target`. |
| Q-A8g | Primitive-difference modulo descent postprocesses targets: if a target descends modulo a target equivalence and a readout respects that equivalence into a readout equivalence, then the readout descends modulo the readout equivalence. | `[MECHANIZED]` | §7 Q-T5g; Lean `Paper_Q.primitive_difference_mod_descent_postprocesses_target`. |
| Q-A8h | Primitive-difference descent is zero-invariance: a target descends through the residual quotient exactly when it is invariant on zero-related worlds. | `[MECHANIZED]` | §7 Q-T5h; Lean `Paper_Q.primitive_difference_descent_iff_zero_invariant`. |
| Q-A8i | Primitive-difference modulo descent is zero-invariance: a target descends to a declared quotient exactly when it is invariant modulo that quotient on zero-related worlds. | `[MECHANIZED]` | §7 Q-T5i; Lean `Paper_Q.primitive_difference_mod_descent_iff_zero_invariant`. |
| Q-A8j | Primitive-difference zero-separation blocks descent: if a zero-related pair remains target-separated, then the target cannot descend through the residual quotient. | `[MECHANIZED]` | §7 Q-T5j; Lean `Paper_Q.primitive_difference_zero_separation_blocks_descent`. |
| Q-A8k | Primitive-difference modulo zero-separation blocks descent: if a zero-related pair remains separated modulo the declared target equivalence, then the target cannot descend to that quotient. | `[MECHANIZED]` | §7 Q-T5k; Lean `Paper_Q.primitive_difference_mod_zero_separation_blocks_descent`. |
| Q-A8l | Primitive-difference modulo zero-invariance is preserved by output coarsening: if a fine declared output equivalence implies a coarse one, then fine modulo zero-invariance implies coarse modulo zero-invariance. | `[MECHANIZED]` | §7 Q-T5l; Lean `Paper_Q.primitive_difference_mod_zero_invariance_preserved_by_coarser_output`. |
| Q-A8m | Primitive-difference modulo descent is preserved by output coarsening: if a target descends modulo a fine declared output equivalence, it also descends modulo any coarser declared output equivalence implied by the fine one. | `[MECHANIZED]` | §7 Q-T5m; Lean `Paper_Q.primitive_difference_mod_descent_preserved_by_coarser_output`. |
| Q-A8n | Primitive-difference law descent is delta-congruence: the primitive difference law descends to the residual quotient exactly when it is congruent on zero-related inputs in both coordinates. | `[MECHANIZED]` | §7 Q-T5n; Lean `Paper_Q.primitive_difference_law_descent_iff_delta_congruent`. |
| Q-A8o | Primitive-difference law zero-separation blocks descent: if zero-related inputs in both coordinates still produce different primitive-difference outputs, then the primitive difference law cannot descend to the residual quotient. | `[MECHANIZED]` | §7 Q-T5o; Lean `Paper_Q.primitive_difference_law_zero_separation_blocks_descent`. |
| Q-A8p | Primitive-difference modulo law descent is delta-congruence: modulo a declared difference-output equivalence, the primitive difference law descends to the residual quotient exactly when it is delta-congruent modulo that equivalence. | `[MECHANIZED]` | §7 Q-T5p; Lean `Paper_Q.primitive_difference_mod_law_descent_iff_delta_congruent`. |
| Q-A8q | Primitive-difference modulo law zero-separation blocks descent: if zero-related inputs in both coordinates remain separated modulo a declared difference-output equivalence, then the primitive difference law cannot descend to that quotient. | `[MECHANIZED]` | §7 Q-T5q; Lean `Paper_Q.primitive_difference_mod_law_zero_separation_blocks_descent`. |
| Q-A8r | Primitive-difference modulo law congruence is preserved by output coarsening: if a fine declared difference-output equivalence implies a coarse one, then fine modulo delta-congruence implies coarse modulo delta-congruence. | `[MECHANIZED]` | §7 Q-T5r; Lean `Paper_Q.primitive_difference_mod_law_delta_congruence_preserved_by_coarser_output`. |
| Q-A8s | Primitive-difference modulo law descent is preserved by output coarsening: if the primitive difference law descends modulo a fine declared difference-output equivalence, it also descends modulo any coarser declared difference-output equivalence implied by the fine one. | `[MECHANIZED]` | §7 Q-T5s; Lean `Paper_Q.primitive_difference_mod_law_descent_preserved_by_coarser_output`. |
| Q-A8t | QM residual-density LGGR is a Q-level PrimitiveDifference non-promotion instance: a density-like profile may descend through the residual quotient while a hidden/global or authority coordinate blocks paired descent. Hypotheses: finite PrimitiveDifference carrier $P$, discrete density-like diagnostic $d$, hidden/authority readout $h$. Discrete bound: $d \downarrow P/{\sim}$ holds with zero defect while $h$ separates zero-related pair $a \sim_P b$ ($h(a) \neq h(b)$), producing strictly positive quotient defect $\operatorname{dist}_{Q^1}((d,h)) > 0$ and blocking paired descent. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5; PaperQF002 §1.8; Lean `QM.QLevelLGGRBridge.density_lggr_is_q_level_primitive_nonpromotion`, `QM.QLevelLGGRBridge.density_q_bridge_not_authority_certificate`, `QM.QLevelLGGRBridge.joint_density_authority_factor_implies_authority_quotient_compatible`. Does not derive QM, the Born rule, continuum dynamics, or authority. |
| Q-A8u | QM residual-density LGGR persists under declared Q output equivalences: a density-like diagnostic may descend modulo its declared equivalence while a hidden/global or authority coordinate separated modulo its own declared equivalence blocks paired modulo descent. Hypotheses: declared diagnostic equivalence $S$, declared readout equivalence $T$, zero-related witness pair $a \sim_P b$ with $\neg T(h(a), h(b))$. Discrete bound: modulo descent $d \downarrow P/{\sim} \pmod S$ holds with zero defect while paired packet defect is non-zero: $\neg((d,h)\downarrow P/{\sim} \pmod{S\times T})$. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5t; PaperQF002 §1.8; Lean `QM.QLevelLGGRBridge.density_mod_lggr_is_q_level_primitive_nonpromotion`, `QM.QLevelLGGRBridge.density_mod_q_bridge_not_authority_certificate`, `QM.QLevelLGGRBridge.joint_mod_density_authority_factor_implies_authority_quotient_compatible`. Does not derive QM, the Born rule, continuum dynamics, or authority. |
| Q-A8v | QM residual-density LGGR persists under density-side diagnostic coarsening: if a density diagnostic descends modulo a fine declared equivalence, it descends modulo any coarser density equivalence, while a hidden/global or authority coordinate still separated modulo its own declared equivalence continues to block paired descent. Hypotheses: fine equivalence $S_f$, coarse equivalence $S_c$ ($S_f \Rightarrow S_c$), hidden equivalence $T$. Discrete bound: $d$ descends modulo $S_c$, but paired defect persists modulo $S_c \times T$ under the explicit hidden separation witness. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5u; PaperQF002 §1.8; Lean `QM.QLevelLGGRBridge.density_mod_descent_preserved_by_diagnostic_coarsening`, `QM.QLevelLGGRBridge.density_mod_lggr_persists_under_density_coarsening`, `QM.QLevelLGGRBridge.density_mod_authority_firewall_persists_under_density_coarsening`. Does not derive QM, the Born rule, continuum dynamics, or authority. |
| Q-A8w | QM residual-density LGGR is closed under visible local-green product composition: two quotient-compatible diagnostics pair into another local-green diagnostic, but a hidden/global or authority coordinate separated on a zero-related witness still blocks augmented product descent. Hypotheses: visible diagnostics $l, r$ invariant on $P$-zero-related worlds, hidden coordinate $h$ separating zero-related witness $a \sim_P b$. Discrete bound: $(l, r)$ descends with exact zero quotient defect, while $((l, r), h)$ retains non-zero quotient obstruction. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5v; PaperQF002 §1.8; Lean `QM.QLevelLGGRBridge.local_pair_lggr_is_q_level_primitive_nonpromotion`, `QM.QLevelLGGRBridge.local_pair_mod_lggr_is_q_level_primitive_nonpromotion`, `QM.QLevelLGGRBridge.local_pair_mod_q_bridge_not_authority_certificate`. Does not derive QM, the Born rule, continuum dynamics, LQG, or authority. |
| Q-A8x | QM residual-density LGGR is closed under diagnostic/readout postprocessing: equivalence-respecting readouts of local-green diagnostics remain local-green, and hidden/global readouts that still separate a zero-related witness keep the augmented packet red. Hypotheses: equivalence-respecting readout $r(d)$ of quotient-compatible diagnostic $d$, hidden readout $s(h)$ separating zero-related witness. Discrete bound: $r(d)$ descends with zero defect, while paired packet $(d, s(h))$ has strictly positive residual obstruction. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5w; PaperQF002 §1.8; Lean `QM.QLevelLGGRBridge.diagnostic_readout_lggr_is_q_level_primitive_nonpromotion`, `QM.QLevelLGGRBridge.hidden_readout_lggr_is_q_level_primitive_nonpromotion`, `QM.QLevelLGGRBridge.diagnostic_readout_mod_lggr_is_q_level_primitive_nonpromotion`, `QM.QLevelLGGRBridge.hidden_readout_mod_lggr_is_q_level_primitive_nonpromotion`. Does not derive QM, the Born rule, continuum dynamics, LQG, or authority. |
| Q-A8y | QM residual-density LGGR has an augmented-certificate converse: if a visible product/readout packet with a hidden/global coordinate really descends through the PrimitiveDifference residual quotient, then the hidden/global or hidden-readout coordinate was already quotient-compatible, raw or modulo its declared equivalence. Hypotheses: visible side $v$ and hidden coordinate $h$ with paired descent $(v, h) \downarrow P/{\sim}$. Discrete bound: exact quotient compatibility $\forall a \sim_P b, h(a) \sim_T h(b)$ is strictly necessary (zero hidden defect). | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5x; PaperQF002 §1.8; Lean `QM.QLevelLGGRBridge.local_pair_factor_implies_hidden_quotient_compatible`, `QM.QLevelLGGRBridge.diagnostic_readout_factor_implies_hidden_quotient_compatible`, `QM.QLevelLGGRBridge.hidden_readout_factor_implies_readout_quotient_compatible`, `QM.QLevelLGGRBridge.local_pair_mod_factor_implies_hidden_quotient_compatible`, `QM.QLevelLGGRBridge.diagnostic_readout_mod_factor_implies_hidden_quotient_compatible`, `QM.QLevelLGGRBridge.hidden_readout_mod_factor_implies_readout_quotient_compatible`. Does not derive QM, the Born rule, continuum dynamics, LQG, or authority. |
| Q-A8z | QM residual-density LGGR has an augmented-certificate criterion: once the visible product/readout side is already quotient-compatible, augmented descent through the PrimitiveDifference residual quotient is equivalent to hidden/global or hidden-readout quotient compatibility, raw or modulo declared equivalences. Hypotheses: visible side $v$ already quotient-compatible ($v \downarrow P/{\sim}$). Discrete bound: $(v, h) \downarrow P/{\sim} \iff h \downarrow P/{\sim}$ (exact criterion with zero duality gap). | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5y; PaperQF002 §1.8; Lean `QM.QLevelLGGRBridge.local_pair_factor_iff_hidden_quotient_compatible`, `QM.QLevelLGGRBridge.diagnostic_readout_factor_iff_hidden_quotient_compatible`, `QM.QLevelLGGRBridge.hidden_readout_factor_iff_readout_quotient_compatible`, `QM.QLevelLGGRBridge.local_pair_mod_factor_iff_hidden_quotient_compatible`, `QM.QLevelLGGRBridge.diagnostic_readout_mod_factor_iff_hidden_quotient_compatible`, `QM.QLevelLGGRBridge.hidden_readout_mod_factor_iff_readout_quotient_compatible`. Does not derive QM, the Born rule, continuum dynamics, LQG, or authority. |
| Q-A8aa | QM residual-density paired descent is componentwise: a paired diagnostic descends through the PrimitiveDifference residual quotient exactly when both components descend, raw or modulo declared product equivalences. Hypotheses: paired diagnostic $(d_1, d_2)$ over pointed residual quotient $P/{\sim}$. Discrete bound: exact componentwise equivalence $(d_1, d_2) \downarrow P/{\sim} \iff (d_1 \downarrow P/{\sim}) \wedge (d_2 \downarrow P/{\sim})$. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5z; PaperQF002 §1.8; Lean `QM.ResidualDensityBridge.factorsThroughResidual_pair_iff_component_factors`, `QM.ResidualDensityBridge.factorsThroughResidualMod_pair_iff_component_factors`. This is residual certificate algebra only; it does not derive QM, the Born rule, continuum dynamics, LQG, or authority. |
| Q-A8ab | QM residual-density red-coordinate monotonicity: if either component of a paired diagnostic fails to descend through the PrimitiveDifference residual quotient, then the paired diagnostic cannot descend, raw or modulo declared product equivalences. Hypotheses: paired diagnostic $(d_1, d_2)$ with $d_1$ or $d_2$ non-descending. Discrete bound: non-zero residual lower bound $\operatorname{dist}_{Q^1}((d_1, d_2)) \ge \max(\operatorname{dist}_{Q^1}(d_1), \operatorname{dist}_{Q^1}(d_2)) > 0$. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5aa; PaperQF002 §1.8; Lean `QM.ResidualDensityBridge.pair_no_factor_of_left_not_factor`, `QM.ResidualDensityBridge.pair_no_factor_of_right_not_factor`, `QM.ResidualDensityBridge.pair_mod_no_factor_of_left_not_factor`, `QM.ResidualDensityBridge.pair_mod_no_factor_of_right_not_factor`. This is residual certificate algebra only; it does not derive QM, the Born rule, continuum dynamics, LQG, or authority. |
| Q-A8ac | QM residual-density nested-triple descent is componentwise: a three-coordinate diagnostic descends through the PrimitiveDifference residual quotient exactly when all three coordinates descend, and any one non-descending coordinate blocks the whole triple, raw or modulo declared nested product equivalences. Hypotheses: nested triple $(d_1, d_2, d_3)$ over $P/{\sim}$. Discrete bound: $(d_1, d_2, d_3) \downarrow P/{\sim} \iff \bigwedge_{i=1}^3 (d_i \downarrow P/{\sim})$. | `[MECHANIZED]` + `[SCOPE FENCE]` | §7 Q-T5ab; PaperQF002 §1.8; Lean `QM.ResidualDensityBridge.factorsThroughResidual_triple_iff_component_factors`, `QM.ResidualDensityBridge.triple_no_factor_of_left_not_factor`, `QM.ResidualDensityBridge.triple_no_factor_of_middle_not_factor`, `QM.ResidualDensityBridge.triple_no_factor_of_right_not_factor`, `QM.ResidualDensityBridge.factorsThroughResidualMod_triple_iff_component_factors`, `QM.ResidualDensityBridge.triple_mod_no_factor_of_left_not_factor`, `QM.ResidualDensityBridge.triple_mod_no_factor_of_middle_not_factor`, `QM.ResidualDensityBridge.triple_mod_no_factor_of_right_not_factor`. This is residual certificate algebra only; it does not derive QM, the Born rule, continuum dynamics, LQG, or authority. |
| Q-A8ad | QM PaperAF000 trace acceptance does not bypass Q admission: accepted density step/path traces cannot repair incomplete Q admission debt into QHeld and cannot create TerminalWithinScope without separate witness support. Hypotheses: density step/path trace with admission debt gap $\Delta_{\mathrm{debt}} > 0$ (missing shadow, refinement, declared topology, convergence-certificate route, or descent trigger). Discrete bound: QHeld and TerminalWithinScope are strictly blocked ($\operatorname{IsAdmissible} = \text{False}$). | `[MECHANIZED]` + `[SCOPE FENCE]` | PaperAF000 §6b; §7 Q-T1b; Lean `QM.PaperAF000OperatorTraceBridge.density_trace_acceptance_admission_gap_blocks_qheld`, `QM.PaperAF000OperatorTraceBridge.density_path_acceptance_admission_gap_blocks_qheld`, `QM.PaperAF000OperatorTraceBridge.density_trace_acceptance_without_witness_blocks_terminal`, `QM.PaperAF000OperatorTraceBridge.density_path_acceptance_without_witness_blocks_terminal`. Does not derive QM, the Born rule, continuum dynamics, LQG, QHeld, TerminalWithinScope, or authority. |
| Q-A9 | Boolean continuum shadow fixture blocks target factorization. | `[WORKED EXAMPLE]` + `[MECHANIZED]` | §7 Q-T6; Lean `Paper_Q.bool_continuum_shadow_collision_blocks_target`. |
| Q-A9a | Primitive-spine raw exact terminalization: represented raw classes terminalize as exact repair exactly when the congruent raw `Phi` score is zero. | `[MECHANIZED]` | §7 Q-T6a; Lean `Paper_Q.primitive_spine_raw_terminal_exact_iff_phi_zero`. |
| Q-A9b | Primitive-spine raw survivor terminalization: represented raw classes terminalize as stabilized survivors exactly when raw `Phi` is nonzero and raw `Gamma` is zero. | `[MECHANIZED]` | §7 Q-T6b; Lean `Paper_Q.primitive_spine_raw_terminal_survivor_iff_phi_nonzero_gamma_zero`. |
| Q-A9c | Primitive-spine raw open terminalization: represented raw classes terminalize as open obstructions exactly when raw `Phi` and raw `Gamma` are both nonzero. | `[MECHANIZED]` | §7 Q-T6c; Lean `Paper_Q.primitive_spine_raw_terminal_open_iff_phi_nonzero_gamma_nonzero`. |
| Q-A9d | Primitive-spine raw `Phi` noncongruence blocks quotient classifiers: no residual-quotient classifier can supply a raw `Phi` score that is not invariant on zero-related worlds. | `[MECHANIZED]` | §7 Q-T6d; Lean `Paper_Q.primitive_spine_phi_noncongruence_blocks_classifier`. |
| Q-A9e | Primitive-spine raw `Gamma` noncongruence blocks quotient classifiers: no residual-quotient classifier can supply a raw `Gamma` score that is not invariant on zero-related worlds. | `[MECHANIZED]` | §7 Q-T6e; Lean `Paper_Q.primitive_spine_gamma_noncongruence_blocks_classifier`. |
| Q-A9f | Primitive-spine repair boundary requires all governance gates: policy permission, rule availability, budget, and admissible witness are jointly necessary and sufficient for repaired boundary status. | `[MECHANIZED]` | §7 Q-T6f; Lean `Paper_Q.primitive_spine_repair_boundary_repaired_iff_all_gates`. |
| Q-A9g | Exact classifier status without a certificate is not a repaired primitive terminal packet. | `[MECHANIZED]` | §7 Q-T6g; Lean `Paper_Q.primitive_spine_exact_without_certificate_not_repaired`. |
| Q-A9h | A primitive terminal packet is not ready exactly when its boundary is repaired but its certificate is absent. | `[MECHANIZED]` | §7 Q-T6h; Lean `Paper_Q.primitive_spine_packet_not_ready_iff_repaired_without_certificate`. |
| Q-A9i | Licensed primitive lifts must provide replay, residual-reduction, and closure-preservation evidence. | `[MECHANIZED]` | §7 Q-T6i; Lean `Paper_Q.primitive_spine_lift_requires_replay_reduction_closure`. |
| Q-A9j | A primitive lift candidate with no source obstruction or no new carrier is not licensed. | `[MECHANIZED]` | §7 Q-T6j; Lean `Paper_Q.primitive_spine_missing_source_or_carrier_blocks_lift`. |
| Q-A9k | A primitive lift certificate licenses its boolean candidate and supplies replay, residual-reduction, and closure-preservation evidence. | `[MECHANIZED]` | §7 Q-T6k; Lean `Paper_Q.primitive_spine_lift_certificate_implies_licensed_and_evidenced`. |
| Q-A9l | A primitive repair witness supplies the promised zero-class repair endpoint. | `[MECHANIZED]` | §7 Q-T6l; Lean `Paper_Q.primitive_repair_witness_repairs_to_zero`. |
| Q-A9m | A repair map that sends the represented quotient class to the primitive zero class supplies ordinary repair-witness data. | `[MECHANIZED]` | §7 Q-T6m; Lean `Paper_Q.primitive_repair_map_to_zero_gives_witness`. |
| Q-A9n | Budget admissibility is stronger than ordinary admissibility for primitive repair maps. | `[MECHANIZED]` | §7 Q-T6n; Lean `Paper_Q.primitive_budget_admissible_implies_admissible`. |
| Q-A9o | An admissible primitive repair witness supplies ordinary repair-witness data on the pointed residual quotient. | `[MECHANIZED]` | §7 Q-T6o; Lean `Paper_Q.primitive_admissible_witness_implies_repair_witness`. |
| Q-A9p | Admissible witnessed exact repair refines ordinary witnessed exact repair for some repair map. | `[MECHANIZED]` | §7 Q-T6p; Lean `Paper_Q.primitive_admissible_witnessed_exact_implies_witnessed_exact`. |
| Q-A9q | If a repair system rejects the constant-zero collapse map, no admissible witness in that system can use that map. | `[MECHANIZED]` | §7 Q-T6q; Lean `Paper_Q.primitive_constant_zero_inadmissible_blocks_constant_zero_witness`. |
| Q-A9r | A no-trivial-collapse policy blocks admissible witnesses whose repair map is the constant-zero collapse. | `[MECHANIZED]` | §7 Q-T6r; Lean `Paper_Q.primitive_no_trivial_repair_collapse_blocks_constant_zero_witness`. |
| Q-A9s | A primitive repair certificate supplies exact classifier status, admissible repair evidence, and zero-class repair evidence. | `[MECHANIZED]` | §7 Q-T6s; Lean `Paper_Q.primitive_repair_certificate_supplies_exact_admissible_and_zero`. |
| Q-A9t | A primitive repair certificate refines to ordinary witnessed exact repair on the pointed residual quotient. | `[MECHANIZED]` | §7 Q-T6t; Lean `Paper_Q.primitive_repair_certificate_implies_witnessed_exact`. |
| Q-A9u | Admissible witnessed exact repair is sufficient to build a primitive repair certificate. | `[MECHANIZED]` | §7 Q-T6u; Lean `Paper_Q.primitive_admissible_witnessed_exact_gives_certificate`. |
| Q-A9v | Exact classifier status alone is not a primitive repair certificate; there is an empty repair system under which exact status has no certificate. | `[MECHANIZED]` | §7 Q-T6v; Lean `Paper_Q.primitive_exact_status_alone_is_not_repair_certificate`. |
| Q-A9w | A primitive terminal packet is repaired when its boundary is repaired and its certificate flag is present. | `[MECHANIZED]` | §7 Q-T6w; Lean `Paper_Q.primitive_terminal_packet_repaired_if_boundary_and_certificate`. |
| Q-A9x | Primitive terminal-packet readiness is exactly blocked-or-repaired readiness. | `[MECHANIZED]` | §7 Q-T6x; Lean `Paper_Q.primitive_terminal_packet_ready_iff_blocked_or_repaired`. |
| Q-A9y | A repaired primitive terminal packet is not blocked. | `[MECHANIZED]` | §7 Q-T6y; Lean `Paper_Q.primitive_terminal_packet_repaired_not_blocked`. |
| Q-A9z | A blocked primitive terminal packet is not repaired. | `[MECHANIZED]` | §7 Q-T6z; Lean `Paper_Q.primitive_terminal_packet_blocked_not_repaired`. |
| Q-A9aa | A raw carrier remembers the quotient class represented by its raw world. | `[MECHANIZED]` | §7 Q-T6aa; Lean `Paper_Q.primitive_raw_carrier_class_eq`. |
| Q-A9ab | A raw carrier's terminal packet status matches classifier terminalization of the represented quotient class. | `[MECHANIZED]` | §7 Q-T6ab; Lean `Paper_Q.primitive_raw_carrier_packet_status_matches`. |
| Q-A9ac | Primitive lift licensing is exactly the conjunction of all five checklist fields. | `[MECHANIZED]` | §7 Q-T6ac; Lean `Paper_Q.primitive_lift_license_iff_all_fields_true`. |
| Q-A9ad | Missing replay, residual-reduction, or closure evidence blocks primitive lift licensing. | `[MECHANIZED]` | §7 Q-T6ad; Lean `Paper_Q.primitive_lift_missing_replay_reduction_or_closure_blocks_lift`. |
| Q-A9ae | Missing replay, residual-reduction, or closure evidence blocks a structured primitive lift certificate. | `[MECHANIZED]` | §7 Q-T6ae; Lean `Paper_Q.primitive_lift_missing_replay_reduction_or_closure_blocks_certificate`. |
| Q-A9af | A primitive spine summary terminal packet reports classifier terminalization of its quotient class. | `[MECHANIZED]` | §7 Q-T6af; Lean `Paper_Q.primitive_spine_summary_terminal_status_matches`. |
| Q-A9ag | A primitive spine summary with a repair certificate supplies exact classifier status. | `[MECHANIZED]` | §7 Q-T6ag; Lean `Paper_Q.primitive_spine_summary_with_certificate_implies_exact`. |
| Q-A9ah | A primitive spine summary with a repair certificate supplies admissible witnessed exact repair. | `[MECHANIZED]` | §7 Q-T6ah; Lean `Paper_Q.primitive_spine_summary_with_certificate_implies_admissible_witnessed_exact`. |
| Q-A9ai | A primitive terminal packet has exact-repair status exactly when its classifier marks the represented quotient class exact. | `[MECHANIZED]` | §7 Q-T6ai; Lean `Paper_Q.primitive_terminal_packet_exact_iff_classifier_exact`. |
| Q-A9aj | A primitive terminal packet has stabilized-survivor status exactly when its classifier marks the represented quotient class stabilized. | `[MECHANIZED]` | §7 Q-T6aj; Lean `Paper_Q.primitive_terminal_packet_survivor_iff_classifier_survivor`. |
| Q-A9ak | A primitive terminal packet has open-obstruction status exactly when its classifier marks the represented quotient class open. | `[MECHANIZED]` | §7 Q-T6ak; Lean `Paper_Q.primitive_terminal_packet_open_iff_classifier_open`. |
| Q-A9al | Every primitive terminal packet is classified as exact repair, stabilized survivor, or open obstruction by its classifier. | `[MECHANIZED]` | §7 Q-T6al; Lean `Paper_Q.primitive_terminal_packet_classifier_total`. |
| Q-A9am | A primitive lift certificate supplies source-obstruction, new-carrier, replay, residual-reduction, and closure-preservation evidence. | `[MECHANIZED]` | §7 Q-T6am; Lean `Paper_Q.primitive_lift_certificate_supplies_all_evidence`. |
| Q-A9an | Missing source-obstruction or new-carrier evidence blocks a structured primitive lift certificate. | `[MECHANIZED]` | §7 Q-T6an; Lean `Paper_Q.primitive_lift_missing_source_or_carrier_blocks_certificate`. |
| Q-A9ao | Licensing a boolean primitive lift candidate does not itself produce a structured lift certificate. | `[MECHANIZED]` | §7 Q-T6ao; Lean `Paper_Q.primitive_licensed_lift_candidate_not_certificate`. |
| Q-A10 | A finite operational Hilbert-space packet on $\mathcal{H} \cong \mathbb{C}^2$ may terminalize an operational prediction under discrete projector measurement $\sum \Pi_i = I_2$ without terminalizing wavefunction/Hilbert-space ontology. Hypotheses: finite dimension $d=2$, state $\rho = \vert 0\rangle\langle 0 \vert$, PVM $\{\Pi_0, \Pi_1\}$, tolerance $\epsilon = 0$. Discrete bound: operational prediction probability $p_0 = \operatorname{Tr}(\Pi_0 \rho) = 1$; ontological discriminator defect remains 1 (unsupported by packet). | `[WORKED EXAMPLE]` + `[INTERPRETIVE]` | §8 toy qubit packet. Shows packet non-identifiability only; does not refute wavefunction realism. |
| Q-A10a | Finite Quantum Obstruction Calculus is strictly scoped to finite-dimensional Hilbert spaces $\mathcal{H} \cong \mathbb{C}^d$ ($d < \infty$) and discrete orthogonal projector decompositions $\sum_{i=1}^k \Pi_i = I_d$ ($\Pi_i \Pi_j = \delta_{ij} \Pi_i$, $\Pi_i^\dagger = \Pi_i$). Operational profiles are discrete probability distributions $\mathbf{p}(\rho) = (\operatorname{Tr}(\Pi_i \rho))_{i=1}^k \in \Delta^{k-1}$. Continuum field operators, infinite-dimensional $C^*$-algebras, and $L^2(\mathbb{R}^n)$ remain unadmitted Q-debts. | `[DEFINITION]` + `[SCOPE FENCE]` | §8.5. Strictly eliminates ungrounded continuum overclaims. |
| Q-A10b | Numerical state-defect bound on $\mathbb{C}^d$: IEEE754 `numpy.linalg.eigh` computes a trace-distance surrogate $D_{\mathrm{tr}}(\rho, \sigma) = \frac{1}{2}\|\rho - \sigma\|_1$ and a spectral-sign witness $W = \Pi_+ - \Pi_-$. This is a **numerical regression**, not exact $\mathbb{Q}$ arithmetic and not a Lean duality theorem. `DualWitness.lean` is **not in this package**. | `[COMPUTED]` + `[SCOPE FENCE]` | §8.5; `code/coda_q_core.py` `StateDefectBound.compute_defect`; `code/tests/test_coda_q.py` numerical check. |
| Q-A10c | Continuum Non-Promotion Scope Fence: discrete projector statistics and exact trace defect bounds on $\mathbb{C}^d$ do not authorize promotion to continuous spatial wavefunctions $\psi(x)$ on $\mathbb{R}^3$, continuous path integrals, or quantum field ontologies; all such extensions remain unproved continuum debts. | `[SCOPE FENCE]` | §8.5. Finiteness fence against metaphysical and continuum promotion. |
| Q-A11 | Participatory realism currently reads as `representation_only` / `survivor` under the seed packet because it lacks a Born-rule derivation, collapse mechanism, or operational discriminator. | `[INTERPRETIVE]` | §9 Q receipt over the seed discussion. Not a physics verdict; a packet-relative status. |
| Q-A12 | Tao/Lean-style machine-assisted mathematics is a positive precedent for decomposition, proposal, verification, and residual mapping. | `[STANDARD]` + `[INTERPRETIVE]` | §10, citing Quanta/Hartnett (2026). The broader Omega mapping is interpretive. |
| Q-A13 | Riemann, consciousness, cancer, biosignature, and interpersonal examples are valid Q-template examples when scoped to finite probes. | `[INTERPRETIVE]` | §11 templates only; no domain result claimed. |
| Q-A14 | A failed Q descent is not proof of falsity. | `[SCOPE FENCE]` | §12 NOT 7. Packet-relative failure only. |
| Q-A15 | The release boundary is "publish the descent attempt and obstruction before publishing the claim." | `[SCOPE FENCE]` / protocol rule | §13. |
| Q-A16 | The practical Omega target is a claim terminalization engine with obstruction receipts, not ASI, an oracle, or "truth AI." | `[SCOPE FENCE]` + `[INTERPRETIVE]` | §14. The White Barn is interface metaphor only. |
| Q-A17 | PR #1345 is a worked Q-process receipt for a frozen-corpus, typed-proposal, exact finite evaluation, replay, refusal, independent-adversary handoff, and human-review boundary. | `[WORKED EXAMPLE]` + `[UNREGISTERED-LOCAL]` | §11.6. The `principia_anomalonica/.../pl_gtoc_15_duration_solver_receipt_20260723.md` path is **historical-not-in-this-tree**. It adds no Q theorem; PL-GTOC-15 remains OPEN. |

Exact paper-to-ENC crosswalk
----------------------------

“In local order” below is literal: advance through the listed local suffixes and
the listed ENC ids together. This compact crosswalk covers every registered
paper claim without duplicating the generated 105-row ledger.

| Local paper row(s) | Generated ENC row(s) | Canonical disposition |
| --- | --- | --- |
| Q-A0 | ENC-0950 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A3, Definitions 5.1–5.6 | ENC-0935..0940 | ENC-0935..0939 `DEFINED / NOT-PLANNED`; ENC-0940 `DEFINED / MECHANIZED`, native Q |
| Q-A4 | ENC-0943 | `MECHANIZED / MECHANIZED`, native Q; local constructor disjointness only |
| Q-A4a | ENC-0952 | `MECHANIZED / MECHANIZED`, native Q; local constructor disjointness only |
| Q-A4b | ENC-1165 | `MECHANIZED / MECHANIZED`, native Q/Paper_Q admission gate |
| Q-A5 | ENC-0944 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A5a | ENC-0951 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A5b..Q-A5j | ENC-0954..0962, in local order | nine `MECHANIZED / MECHANIZED` native-Q rows |
| Q-A5k..Q-A5m | ENC-0964..0966, in local order | three `MECHANIZED / MECHANIZED` native-Q rows |
| Q-A6 | ENC-0945 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A6a | ENC-0949 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A7 | ENC-0946 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A7a | ENC-0963 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A7b..Q-A7d | ENC-0968..0970, in local order | three `MECHANIZED / MECHANIZED` native-Q rows |
| Q-A8 | ENC-0947 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A8a | ENC-0967 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A8b..Q-A8s | ENC-0971..0988, in local order | eighteen `MECHANIZED / MECHANIZED` native-Q rows |
| Q-A8t..Q-A8ac | ENC-1154..1163, in local order | ten `MECHANIZED / MECHANIZED` quantum/PaperAF000 bridge rows; not native `Paper_Q` payload |
| Q-A8ad | ENC-1166 | `MECHANIZED / MECHANIZED`, quantum/PaperAF000 trace-admission bridge |
| Q-A9 | ENC-0948 | `MECHANIZED / MECHANIZED`, native Q |
| Q-A9a..Q-A9ao | ENC-0989..1029, in local order | forty-one `MECHANIZED / MECHANIZED` native-Q rows |
| Q-A16 | ENC-0953 | `DEFINED / MECHANIZED`, native Q claim-machine definition |

### Unregistered local prose dispositions

These nine rows remain useful paper framing. They are not generated
`paper_9999` entries, do not carry an ENC theorem status, and cannot be counted
as extra mechanized claims.

| Local row | Disposition | Boundary |
| --- | --- | --- |
| Q-A1 | `SCOPE-FENCE / UNREGISTERED-LOCAL` | Q's quarantine role; no authority constructor |
| Q-A2 | `PROTOCOL-DEFINITION / UNREGISTERED-LOCAL` | receipt shape only |
| Q-A10 | `WORKED-EXAMPLE / UNREGISTERED-LOCAL` | toy Hilbert-space non-identifiability packet, no domain theorem |
| Q-A10a | `SCOPE-FENCE / UNREGISTERED-LOCAL` | Finite quantum obstruction calculus finite-dimensional Hilbert space & discrete PVM scoping |
| Q-A10b | `COMPUTED / UNREGISTERED-LOCAL` | IEEE754 numpy state-defect regression; DualWitness.lean not in this package |
| Q-A10c | `SCOPE-FENCE / UNREGISTERED-LOCAL` | Finiteness fence eliminating ungrounded continuum overclaims |
| Q-A11 | `INTERPRETIVE / UNREGISTERED-LOCAL` | packet-relative participatory-realism readout |
| Q-A12 | `STANDARD-INTERPRETATION / UNREGISTERED-LOCAL` | workflow analogy, not proof or authority |
| Q-A13 | `INTERPRETIVE / UNREGISTERED-LOCAL` | template examples only |
| Q-A14 | `SCOPE-FENCE / UNREGISTERED-LOCAL` | failed descent is not falsity |
| Q-A15 | `PROTOCOL-RULE / UNREGISTERED-LOCAL` | publication discipline, not a theorem |
| Q-A17 | `WORKED-EXAMPLE / UNREGISTERED-LOCAL` | PR #1345 exact finite duration receipt; universal obligation, Lean route, independent adversary, and human decision remain open |

Support Ledger
--------------

| Item | Status | Remaining obligation |
| --- | --- | --- |
| Full categorical placement of $\Omega_Q$ | Not claimed | If Q becomes more than a quarantine wrapper, specify its categorical interface to GTLA without adding an authority constructor. |
| Categorical authority non-creation from Q-T1/T1a | Not claimed | Current Lean proves pointwise constructor disjointness in local sum types, not CODA-FDA `Authority_S`, a descent functor, or a categorical theorem. |
| Domain ontology from PrimitiveDescent | Not claimed | The Lean theorem defines mode-being as descent plus terminalization; it does not derive an external ontology or a universal existence predicate. |
| Genesis from PrimitiveDescent | Not claimed | The repository root remains the admitted `Difference sqcup Structure` cut; all Q carriers, worlds, modes, observers, profiles, and targets are explicit packet imports. |
| Domain authority from finite permission | Not claimed | Finite descent permission is profile-relative factorization only; authority still requires the separate terminalized packet. |
| Mechanized Q receipt schema | QM bridge schema present; general Q schema still open | `omega_engine/research/derive_qm/qm_q_bridge.schema.json` gives the QM-facing bridge contract. A general Appendix A Q receipt schema plus validator remains a future engineering artifact. |
| Hilbert-space ontology discriminator | Not supplied | Any ontology claim needs a finite discriminator separating ontological realism from operationally equivalent representation readings. |
| Participatory realism discriminator | Not supplied | A finite prediction, derivation, or terminal discriminator would be needed to upgrade the §9 receipt. |
| Domain-specific Q bridges | QM bridge supplied; other domains not supplied | `omega_engine/research/derive_qm/qm_q_bridge.md` supplies the finite-QM-to-Level-Q routing boundary. RH, consciousness, transfinite, biology, and interpersonal probes still require their own declared target, shadow profile, verifier, and terminalizer. |
| QM/PaperAF000 bridge ownership | Mechanized outside native Q | ENC-1154..1163 and ENC-1166 are checked in QM/PaperAF000 and only alias into paper 9999; ENC-1165 alone is the later native Q/Paper_Q row. |
| PL-GTOC-15 worked receipt | Python-$\mathbb Q$ executable partial evidence; no Q theorem | Independent adversarial review, general coefficient/carrier proof, chain telescoping, rooted converse, Lean, and human acceptance remain open. |

Lean Verification
-----------------

On 2026-07-17, from `omega_engine/lean4` under Lean 4.31.0-rc1 with
`LEAN_NUM_THREADS=2`:

* `lake build Paper_Q` passes (638 jobs; 26.812 s on the byte-verified warm
  replay);

* nine imported `Paper_Q/*.lean` modules contain 159 literal theorem
  declarations, zero project `axiom`, and zero `sorry`;

* six emitted admission-firewall receipts depend on no axioms;
* `lake build QM.QLevelLGGRBridge` separately passes (620 jobs; 4.810 s), with
  only standard `Quot.sound` and `propext` dependencies where emitted.

The native root is index:index:Paper_Q.lean (`omega_engine/research/_indexes/_master_index.yaml`, historical repository path; not included in this package). The Lean checks prove
mode-indexed receipt decomposition, finite permission, admission, and
factorization/non-factorization boundaries only. They do not prove a domain
ontology, RH bridge, consciousness theory, categorical authority pipeline, or
transfinite claim. These are inherited validations of the current base, not new
proof progress created by G8.

<!-- claim-id-body-only-sync:begin -->

Body-only ID sync (packaging 2026-07-25)
----------------------------------------


| ID | Claim | Type | Status |
| --- | --- | --- | --- |
| Q-000 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-000a | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-001 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-002 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-003 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-004 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-005 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-006 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-007 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-008 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-009 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-010 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-011 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-012 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-013 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-014 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-1 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-A10a | Finite Quantum Obstruction Calculus finite-dimensional Hilbert space & discrete PVM scoping | `[DEFINITION]` + `[SCOPE FENCE]` | packaging |
| Q-A10b | IEEE754 numpy state-defect regression; DualWitness.lean not in this package | `[COMPUTED]` + `[SCOPE FENCE]` | packaging |
| Q-A10c | Finiteness fence strictly eliminating ungrounded continuum overclaims | `[SCOPE FENCE]` | packaging |
| Q-T0 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T1 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T1a | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T1b | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2a | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2b | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2c | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2d | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2e | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2f | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2g | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2h | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2i | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2j | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2k | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2l | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T2m | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T3 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T3a | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T4 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T4a | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T4b | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T4c | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T4d | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5a | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5aa | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5ab | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5b | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5c | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5d | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5e | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5f | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5g | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5h | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5i | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5j | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5k | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5l | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5m | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5n | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5o | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5p | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5q | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5r | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5s | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5t | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5u | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5v | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5w | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5x | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5y | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T5z | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6a | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6aa | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6ab | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6ac | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6ad | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6ae | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6af | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6ag | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6ah | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6ai | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6aj | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6ak | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6al | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6am | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6an | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6ao | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6b | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6c | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6d | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6e | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6f | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6g | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6h | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6i | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6j | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6k | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6l | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6m | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6n | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6o | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6p | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6q | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6r | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6s | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6t | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6u | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6v | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6w | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6x | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6y | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| Q-T6z | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |

<!-- claim-id-body-only-sync:end -->
---

Dual-home absorption from 008 (2026-07-26)
------------------------------------------

| Claim ID | Claim Type | Scope / Statement Summary | File / Section Binding | Verification / Evidence Status |
| --- | --- | --- | --- | --- |
| `ABSORB-008-010_information_q_and_gtoc-01` | `[PACKAGING]` | Thin 008 dual-home shell `010_information_q_and_gtoc` absorbed into this 001_coda monograph for Information, Q & GTOC; no new theorem status. | Appendix — 008 dual-home absorption | `[PACKAGING ONLY]` |
| `ABSORB-008-010_information_q_and_gtoc-02` | `[SCOPE FENCE]` | Absorption does not mint authority or flip OPEN→PROVED. | Appendix — 008 dual-home absorption | `[PROVEN, CONDITIONAL]` |
