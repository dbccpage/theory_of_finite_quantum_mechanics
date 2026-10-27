## [v1.2.0] - 2026-08-05 (S9b Necessity Completion, Monoid Lattice Sharpening & Scope Boundary Companion Map)

- **Two-Sided S9b Necessity Table:** Completed the satisfied-property half for all counterexample rows (P1 additivity via $\nu_{\max}$, P2 faithfulness via $\nu_{\text{zero}}$, P3 maximal symmetry via $\nu_{\text{aniso}}$, and P4 uniformity via $\nu_{\text{weighted}}$). Upgraded Theorem 4.2 to a full two-sided characterization theorem.
- **Monoid Partial Order & Lattice:** Explicitly detailed the monoid partial order $\{e\} \subset \mathbb{Z}_2^n \rtimes S_n \subset \mathbf{Diag}_{>0} \subset \mathrm{End}_b(V)$ and its corresponding admissible gauge classes.
- **GS-001 Scope Boundary & Companion Map (§8.5):** Positioned GS-001 as the definitive maximal-symmetry classification endpoint and registered 4 controlled companion papers (`011_weaker_monoid_gauge_classification`, `012_higher_degree_cochain_gauge_rigidity`, `013_projection_obstruction_residual_oracles_and_lattice_scaling`, `014_finite_and_infinite_as_observer_relative_regimes_of_obstruction`).
- **Python Test Infrastructure & Coverage:** Fixed module import paths across `gs001_gauges.py`, `rigidity.py`, and test suite. 19/19 tests passing with 95% production test coverage.

## [v1.1.1] - 2026-07-30 (R2 — Cat_Res morphism cross-reference in §1.2)

- **Cat_Res binding (HANDOFF-003):** Published residual-honest morphism cross-reference $F_{\mathrm{GS001}}\colon P_{\mathrm{host}}\to P_{\mathrm{gauge}}$ under §1.2, with GS-001 packet sketch $(K,Z,J,W,R,Q,L,A)$ and HANDOFF-003 contract table.
- **Path truth:** Live carrier is `published/008_engine_runtime/008_residual_handoff_category.md`(relocated 2026-07-27). Historical label`100_mathematical_foundations/008_residual_handoff_category.md`is not a live file on this tree.
- **Nonclaims preserved:** Conditional on declared Banach-presheaf inputs; does not derive ambient space; does not mint FuncDiffAdapter; does not claim full Cat_Res identity/associativity or residual handoff *certificate*.
- **Ledger:** Claim row`2b`records SCOPE FENCE / PACKAGING status for the cross-reference.

## [v1.1.0] - 2026-07-30 (Red Team Review Corrections & Republication Readiness)

- **CPTP Trace-Norm Rigidity Theorem:** Retracted false non-uniqueness claim. Proved that full CPTP contractivity on trace-zero Hermitian operators forces trace norm $j(X) = c\|X\|_1$ via measure-and-prepare channel reachability. Added 4D Frobenius non-contractivity counterexample.
- **Monoid Reachability Organizing Principle:** Formally established the Bidirectional Sphere-Reachability Criterion.
- **P4 Locality Axiom:** Explicitly specified locality/excision and fiberwise isometry requirements for edge-weight uniformity.
- **Presheaf Definition:** Clarified covering-edge Banach diagram input structure and path-coherence requirement.
- **Quotient Geometry:** Defined $h_{1,e}$ and added explicit finite-dimensionality and closed-range hypotheses for $\ell^1$ quotient minimizer selection.
- **PCC Adapter Bridge:** Formally specified the 3-element adapter equation bridging PCC set-level witnesses to cochain residuals.
- **Errata & Scaling Fixes:** Fixed Theorem 3.1 unit ball scaling ($B_j = c^{-1}B_2$) and monoid size qualifier ("may yield larger families"). Updated mechanization badge to`MECHANIZATION CLAIMED; ARTIFACT NOT INCLUDED`.
- **Demanded Test Suite:** Implemented 20-test validation suite (`tests/test_rt_demanded_20.py`).

## Extracted from paper body (preflight G6)

## Changelog

### v4.6 (June 2026) — Lean Independence Witness Packet

- Replaced the S9 "relative to examples" qualifier with Lean-checked finite
  witnesses in`L002_05_Counterexamples.lean`.

- Closed PL-002-2 / ENC-0523 by proving`Enc0523.max_not_additive`,
 `Enc0523.zero_not_faithful`,`Enc0523.anisotropic_not_p3`, and
 `Enc0523.weighted_not_uniform`.

### v4.5 (June 2026) — Lean Hahn--Banach Discharge

- Added`L002_09_HahnBanachDischarge.lean`, which uses Mathlib's
 `exists_dual_vector`Hahn--Banach corollary to discharge the explicit
  norming-functional hypothesis in the local maximal-symmetry theorem.

- Added theorem pointers for`norming_functional_from_hahn_banach`,
 `direction_independence_hahn_banach`, and
 `gauge_proportional_hahn_banach`.

- Closed PL-002-1 as a Lean mechanization obligation. The theorem remains
  conditional on the stated PaperGS001 hypotheses, including P1--P3 and the
  declared native Banach norm; it no longer has an extra supplied-functional
  mechanization gap.

### v4.4 (June 2026) — Lean Weighted-to-Unweighted Hardening

- Added a named Lean theorem wrapper for the weighted-to-unweighted transition:
 `weighted_sum_eq_scalar_l1_of_uniform_weights`.

- Added the single-orbit/invariant-weight companion:
 `weighted_sum_eq_scalar_l1_of_single_orbit_weights`.

- Updated Proposition 7.1, Support Ledger S8, and the Lean4 status block to cite
 `L002_08_WeightedToUnweightedTransition.lean`.

- No scope change: the unweighted scalar form still requires edge-uniformity,
  a single edge orbit, or explicit normalization.

### v4.3 (June 2026) — Claim-Typing & Ledger Pass

- **Added the missing statement blocks for Corollaries 1–4** (Order Reversal, Maximal-Symmetry Endpoint, Compact-Group Construction, Transitive Sphere Action). These were previously *proven in §2.4 without ever being stated*; statements now appear in a new §2.4 with explicit hypotheses and claim-type tags, and the proofs moved to §2.5.
- **Added inline claim-type tags at the point of statement** for Theorem 3.4, Theorem 3.7, Lemma 4.1, Theorem 4.2, Proposition 7.1, and Corollary 7.2 (previously typed only in the summary ledger table).
- **Corrected the stale Lean-mechanization status:** the rank-one contraction construction and proportionality argument are formalized and`sorry`-free (`direction_independence_tier1`,`gauge_proportional_tier1`in`MaximalSymmetry.lean`); at that release, the sole Tier-2 step was discharging the norming-functional hypothesis via Mathlib Hahn–Banach (closed in v4.5).`EdgeSum.lean`(`weighted_ell1`,`uniform_weights`) is likewise complete.
- Tied §1.5 related-work neighbors 1 and 5 to existing references (Megginson [2], Pestov [1], Helstrom [8]).
- Added a standalone Claim Ledger (`002_M_Compatible_Gauge_Classification_Claim_Ledger.md`) and registered the open proof obligations in the dated global proof ledger (`proof_ledger_20260609.md`).
- No scope change, no new claims, no softened hedges.

### v4.2 (June 2026) — Hygiene Pass

- Added front-matter hygiene (Status/Authority/Main-claim/Non-claim), payoff-first lead sentence, why-care paragraph, §1.5 Related Work, falsifiability line, "what this does not claim" box, Claim-Type Ledger, and Support Ledger (S1–S10).
- **Corrected the $C^1$ definition:** $C^1(P,F)$ is the ambient cochain space $\bigoplus_e F(a_e)$ (plain vector space); coboundary vectors are $\operatorname{im}(d_0)\subseteq C^1$; the $\ell^1$ cross-norm is *selected* by Theorem 4.2, not pre-installed. Removes an ambient-norm circularity and the "space of coboundary vectors" wording.
- **Repaired Corollary 7.2:** non-$\ell^1$ alternatives are excluded by edge-additivity (P1) or functoriality (P3), not by contractivity (an $\ell^2$ aggregation is contractive but non-additive). Added supporting Lemma S7.
- Made ambient-norm hypotheses explicit across §3 (Euclidean / signed-permutation-invariant / $\ell^\infty$); rewrote Thm 3.2; added Lemma S3.
- Added a numerical illustration of the weighted/unweighted $\ell^1$ boundary, retitled to make clear it is downstream of the Lemma-4.1 local result, not a demonstration of it.
- Softened Corollary 1 to weak reduction (strict only with a separating example) and, at that release, kept the necessity table at examples-only support until Lemma S9 was mechanized in v4.6.
- Bumped version to v4.2; updated Status to republication candidate.

### v4.1 (May 2026)

- Made the maximal-symmetry assumption explicit: $M=\mathrm{End}_b(V)$ is a strong observer regime, not a default physical assumption.
- Narrowed the positive-cone result to positive diagonal contractions on the cone and added a boundary note for arbitrary positive maps.
- Reframed CPTP compatibility as an example/definition rather than an iff uniqueness theorem.
- Fixed the convex-body proof typo "No Nontrivial Lines."
- Completed references [4]--[6] and aligned the strategic dependency names with the current title.

### v4.0 (May 2026)

- Retitled the paper around M-compatible gauge classification for Banach presheaf coboundaries.
- Added status, non-claim, and publication-order dependency metadata.
- Clarified finite-dimensional convex-body scope versus Banach-stalk maximal-symmetry theorem.
- Renumbered internal results as Lemma 4.1, Theorem 4.2, Proposition 7.1, and Corollary 7.2.
- Made the edge-additive observer-class assumption explicit before the maximal theorem.
- Replaced informal free-object wording with the finite $\ell^1$ coproduct finite-structural property.

### v3.0 (May 2026)

- Added §8.4: Connection to Observer Theory and Contextual Congruence.
- Linked M-compatible gauge classification to observer passivity (O1), contextual congruence, reflective completion, and sheaf gluing obstruction.
- Renumbered §8.4 → §8.5 and the final dynamical connection to §8.6.
- Added reference [6] (general theory).
- Consolidated the general framework connection into this paper.

### v2.0 (April 2026)

- Initial pre-print with M-compatible classification, maximal symmetry endpoint, and necessity analysis.

---
