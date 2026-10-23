Change Log — GS-003: Vector and Quantum Observer Geometries
===========================================================

--- yaml
title: GS-003 Vector and Quantum Observer Geometries Change Log
file_name: 006_vector_and_quantum_observer_geometries_change_log.md
file_location: omega_engine/research/published/005_gauge_selection/
status: Canonical
authority_effect: None
paper_id: GS-003
canonical_version: v0.4
legacy_filename: 000_vector_and_quantum_observer_geometries.md
date: 2026-09-21
---

v0.4 (2026-09-21) — Full Absorption of QM_081 & QM_082 and PL-000BN-1 Discharge
---

- Permanently absorbed unpublished foundation notes **QM_081** (*Trace Norm CPTP Transport Audit*) and **QM_082** (*Channels as Stochastic Kernels and the CPTP Lift*).
- Added the **Metric Non-Selection Firewall** ($\mathsf{CPTPMonotone}(j) \not\Longrightarrow j(X) = \frac{1}{2}\|X\|_1$), proved via scale-invariance of data-processing monotonicity (`QM.scale_monotone`, `QM.cptp_monotone_not_select`, [[ENC-0247]]) and halving contraction (`QM.id_cptpMonotone_halving`).
- Discharged open obligation **PL-000BN-1** conditionally: proved that $j(X) = \frac{1}{2}\|X\|_1$ is uniquely selected on Hermitian trace-zero operators under unitary invariance and classical total-variation reduction / Helstrom single-shot binary discrimination ([[ENC-0246]]).
- Formulated classical **Markov Population Shadows** of finite CPTP channels ($K(\gamma'\mid\gamma) = \sum_k |\langle\gamma'|A_k|\gamma\rangle|^2$, column-stochastic; `QM.StochasticChannel`, [[ENC-1127]]) and classical $\ell^1$ contraction ($\|Sx\|_1 \le \|x\|_1$, `QM.stochastic_l1_contraction`, [[ENC-1055]]) as the division-algebra-free shadow of quantum data processing. Complete positivity and coherence transport isolated as the licensed lift.
- Added Python implementations and test suites for population shadows and classical $\ell^1$ contraction in `code/cptp_channels.py` and `code/tests/test_cptp_channels.py`.
- Mechanized **Weak Vector Fenchel Duality** in Lean 4 (`mixed_vector_duality.lean`): proved Cauchy–Schwarz pointwise bound (`weak_vector_duality_pointwise`), quotient obstruction lower bound (`weak_vector_duality_quotient`), and exact duality gap certificate (`duality_gap_zero_certificate`) under standard axioms `{propext, Classical.choice, Quot.sound}` with zero `sorry`.
- Mechanized **Strong Vector Duality & Minimax Attainment via Hahn–Banach Separation** in Lean 4 (`strong_vector_duality.lean`): proved explicit stalk norming vector construction (`stalkNormingVector_inner_eq`, `stalkNormingVector_norm_le_one`, `stalkNormingVector_norm_eq_one`), subgradient attainment of quotient obstruction (`subgradient_attainment`), global dual maximality (`dual_witness_is_maximizer`), strong minimax saddle-point identity (`strong_duality_minimax_identity`), complementary slackness / exact pointwise subgradient alignment (`complementary_slackness_edge_alignment`), full minimax certificate (`full_minimax_attainment_certificate`), first-order stationary dual existence (`strong_vector_duality_of_stationary_subgradient`), and abstract Hahn–Banach separating functional existence (`hahn_banach_separation_existence`) strictly within `{propext, Classical.choice, Quot.sound}` with zero `sorry`.
- Mechanized **Quantum Trace-Norm Obstruction Duality (Row C6)** in Lean 4 (`quantum_trace_duality.lean`): formalized axiomatic Hermitian operator stalks with Schatten duality and spectral sign operators; proved Helstrom binary POVM decision observable spectral norm bound (`helstromStalkObservable_specNorm_le`), trace-distance bound attainment (`helstromStalkObservable_inner_eq`), pointwise Cauchy–Schwarz slack non-negativity (`helstrom_slack_nonneg`), canonical Helstrom cochain boundedness and pairing equality (`canonicalHelstromCochain_bounded`, `canonicalHelstromCochain_pairing_eq`), divergence-free repair invariance (`dualPairing_Q_repair_invariance`), weak quantum duality (`weak_quantum_duality_pointwise`, `weak_quantum_duality_quotient`), Helstrom attainment (`helstrom_attainment`), quantum dual witness global maximality (`quantum_dual_witness_is_maximizer`), strong quantum minimax saddle-point identity (`quantum_strong_duality_minimax_identity`), quantum complementary slackness (`quantum_complementary_slackness`), strong quantum duality existence from stationary Helstrom subgradients (`strong_quantum_duality_of_stationary_helstrom`), and exact verification of the single-cycle 3-edge qubit fixture (`single_cycle_qubit_fixture_exact`), certified with exit code 0 and zero axioms beyond `{propext, Classical.choice, Quot.sound}`.
- Decommissioned obsolete legacy `po000_l***_` filename prefixes across the package's Lean 4 estate, normalizing all 10 modules to canonical descriptive basenames (`projection_transfer.lean`, `replica_hierarchy.lean`, `affine_obstruction.lean`, `double_commutator_rate.lean`, `schatten_orthogonal.lean`, `su2_curvature.lean`, `cptp_monotonicity.lean`, `mixed_vector_duality.lean`, `strong_vector_duality.lean`, `quantum_trace_duality.lean`) and synchronizing package roots, internal imports, and provenance ledgers.
- Cross-referenced sibling Paper 080 v1.2 (*CPTP-Compatible Obstruction Theory: Trace-Norm Geometry and Quantum Dual Witnesses*, Zenodo DOI: 10.5281/zenodo.20550459).

v0.3 (2026-07-25) — Gauge Selection Programme Normalization
---

- Standardized primary paper identity as `GS-003 — Vector and Quantum Observer Geometries: Gauge Relativity and Trace Metric Bounds` (legacy identity: `Paper 000`, `Paper 000BN`).
- Positioned as Synthesis Branch (Step 4 in logical programme order).
- Fixed Authority header field to standard wording: `Authority: none` (replacing descriptive text).
- Emphasized core doctrine: *"The quotient class is structural; the scalar obstruction magnitude is observer-gauge-relative."* ($\Phi_{1,1}=2$ vs $\Phi_{2,1}=\sqrt{2}$ on triangle fixture).
- Fenced quantum trace-distance gauge: CPTP monotonicity gives admissibility, not operational uniqueness (open obligation PL-000BN-1 / GS-005).
- Consolidated in-body version history into this companion change log.

v0.2.0 (June 2026)
---

- Pre-print establishing synthesis of vector vs quantum trace-distance observer geometries.
