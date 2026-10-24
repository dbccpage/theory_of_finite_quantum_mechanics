# Independent review of PR #314

Scope: original head d4727e64929533c6256d71c0d2cf4df7b69abaf2. Exact source lean4/CampaignFspLaughlinExchangePhase.lean, SHA-256 ce6c4862a88bb315a12e5e3865898dafb56986b59cb303839b9ec35dc55f467f.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Jastrow exchange identities hold in commutative rings. A supplied 2x2 integer companion matrix and its square satisfy cyclotomic identities and fail involution tests. The quasihole polynomial is symmetric. The matrix model is not identified with a physical Berry holonomy, and symmetry alone does not derive a Berry phase or its physical origin.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignFspLaughlinExchangePhase.lean:24 laughlin_two_body_jastrow_exchange_parity` | `{R : Type*} [CommRing R] (m : ℕ) (z1 z2 : R) : jastrowTwoBody m z2 z1 = (-1 : R) ^ m * jastrowTwoBody m z1 z2` |
| `lean4/CampaignFspLaughlinExchangePhase.lean:32 laughlin_odd_m_fermionic_and_even_m_bosonic` | `{R : Type*} [CommRing R] (k : ℕ) (z1 z2 : R) : jastrowTwoBody (2 * k + 1) z2 z1 = -jastrowTwoBody (2 * k + 1) z1 z2 ∧ jastrowTwoBody (2 * k) z2 z1 = jastrowTwoBody (2 * k) z1 z2` |
| `lean4/CampaignFspLaughlinExchangePhase.lean:49 laughlin_three_body_vandermonde_transposition_flips_sign_for_odd_m` | `{R : Type*} [CommRing R] (k : ℕ) (z1 z2 z3 : R) : jastrowThreeBody (2 * k + 1) z2 z1 z3 = -jastrowThreeBody (2 * k + 1) z1 z2 z3` |
| `lean4/CampaignFspLaughlinExchangePhase.lean:64 laughlin_quasihole_holomorphic_polynomial_symmetric_fence` | `{ι : Type*} [Fintype ι] {R : Type*} [CommRing R] (z : ι → R) (eta1 eta2 : R) : twoQuasiholePrefactor z eta2 eta1 = twoQuasiholePrefactor z eta1 eta2` |
| `lean4/CampaignFspLaughlinExchangePhase.lean:83 laughlin_m3_exchange_companion_cyclotomic_relations` | `: exchangeR6.det = 1 ∧ Matrix.trace exchangeR6 = 1 ∧ exchangeR6 * exchangeR6 - exchangeR6 + 1 = 0 ∧ exchangeR6 ^ 3 = -1 ∧ exchangeR6 ^ 6 = 1 ∧ exchangeR6 ≠ 1 ∧ exchangeR6 ≠ -1` |
| `lean4/CampaignFspLaughlinExchangePhase.lean:94 laughlin_m3_monodromy_cyclotomic_and_non_involution` | `: monodromyM3 = exchangeR6 * exchangeR6 ∧ monodromyM3.det = 1 ∧ Matrix.trace monodromyM3 = -1 ∧ 1 + monodromyM3 + monodromyM3 * monodromyM3 = 0 ∧ monodromyM3 ^ 3 = 1 ∧ monodromyM3 * monodromyM3 ≠ 1` |
| `lean4/CampaignFspLaughlinExchangePhase.lean:104 no_z2_involution_matches_m3_monodromy_fence` | `(J : Matrix (Fin 2) (Fin 2) ℤ) (hJ : J * J = 1) : J ≠ monodromyM3 ∧ J ≠ exchangeR6` |
| `lean4/CampaignFspLaughlinExchangePhase.lean:117 general_m_monodromy_residue_and_odd_coprime` | `(m k : ℕ) (hm : 3 ≤ m) : 2 % m = 2 ∧ 2 % m ≠ 0 ∧ Nat.gcd 2 (2 * k + 1) = 1` |
| `lean4/CampaignFspLaughlinExchangePhase.lean:131 abelian_anyon_modular_s_exponent_and_z3_character_sum` | `(a b : ℤ) : modularSPhaseExponent a b + modularSPhaseExponent 0 0 - modularSPhaseExponent a 0 - modularSPhaseExponent 0 b = a * b ∧ (1 : Matrix (Fin 2) (Fin 2) ℤ) + monodromyM3 + monodromyM3 * monodromyM3 = 0` |
| `lean4/CampaignFspLaughlinExchangePhase.lean:141 unequal_quasihole_quasielectron_weights_prevent_z3_cancellation_fence` | `(w_qh w_qe : ℤ) (hne : w_qh ≠ w_qe) : w_qh • (1 : Matrix (Fin 2) (Fin 2) ℤ) + w_qe • monodromyM3 + w_qe • (monodromyM3 * monodromyM3) = (w_qh - w_qe) • (1 : Matrix (Fin 2) (Fin 2) ℤ) ∧ w_qh • (1 : Matrix (Fin 2) (Fin 2) ℤ) + w_qe • monodromyM3 + w_qe • (monodromyM3 * monodromyM3) ≠ 0` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_314_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
