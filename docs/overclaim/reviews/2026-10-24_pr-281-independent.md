# Independent review of PR #281

Scope: original head e0dded2a1a24bd8fdb0bb1425e18c190bd749ba3. Exact source lean4/CampaignTfq0011FiniteQcd.lean, SHA-256 6714d88efe82d60e3e927d446179f5c57153b561fc1dc04d320aad992fab816f.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

General group plaquette conjugation and rational beta/Creutz identities; the supplied color formulas and monomials are inputs. No gauge complex, continuum QCD, confinement, or lattice-count construction is supplied.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignTfq0011FiniteQcd.lean:22 plaquette_gauge` | `{G : Type*} [Group G] (g h k m a b c d : G) : (a⁻¹ * g * b) * (b⁻¹ * h * c) * (c⁻¹ * k * d) * (d⁻¹ * m * a) = a⁻¹ * (g * h * k * m) * a` |
| `lean4/CampaignTfq0011FiniteQcd.lean:30 s3_swaps_do_not_commute` | `: s01 * s12 ≠ s12 * s01` |
| `lean4/CampaignTfq0011FiniteQcd.lean:33 s3_two_swap_product_ne_one` | `: s01 * s12 * (1 : Equiv.Perm (Fin 3)) * 1 ≠ 1` |
| `lean4/CampaignTfq0011FiniteQcd.lean:44 su3_channel_values` | `: cF 3 = 4 / 3 ∧ cA 3 = 3 ∧ singlet 3 = -4 / 3 ∧ octet 3 = 1 / 6 ∧ sextet 3 = 1 / 3 ∧ antitriplet 3 = -2 / 3 ∧ singlet 3 < 0 ∧ octet 3 > 0` |
| `lean4/CampaignTfq0011FiniteQcd.lean:61 gluon_split_and_one_flavor` | `: (4 : Rat) * cA 3 + (-1 / 3) * cA 3 = 11 ∧ (-4 / 3 : Rat) * (1 / 2) = -2 / 3 ∧ (-4 / 3 : Rat) < 0` |
| `lean4/CampaignTfq0011FiniteQcd.lean:68 beta0_values` | `: beta0 3 0 = 11 ∧ beta0 3 3 = 9 ∧ beta0 3 5 = 23 / 3 ∧ beta0 3 6 = 7 ∧ beta0 3 16 = 1 / 3 ∧ beta0 3 17 = -1 / 3` |
| `lean4/CampaignTfq0011FiniteQcd.lean:78 beta0_window` | `(nf : Rat) : beta0 3 nf > 0 ↔ nf < 33 / 2` |
| `lean4/CampaignTfq0011FiniteQcd.lean:82 beta0_nat_through_16` | `(n : Nat) (hn : n ≤ 16) : beta0 3 (n : Rat) > 0` |
| `lean4/CampaignTfq0011FiniteQcd.lean:85 beta0_17_negative` | `: beta0 3 17 < 0` |
| `lean4/CampaignTfq0011FiniteQcd.lean:89 beta1_su3` | `(nf : Rat) : beta1 3 nf = 102 - (38 / 3) * nf` |
| `lean4/CampaignTfq0011FiniteQcd.lean:93 beta1_values` | `: beta1 3 0 = 102 ∧ beta1 3 5 = 116 / 3 ∧ beta1 3 16 = -302 / 3` |
| `lean4/CampaignTfq0011FiniteQcd.lean:100 banks_zaks_ratio_nf16` | `: (-beta0 3 16) / beta1 3 16 = 1 / 302` |
| `lean4/CampaignTfq0011FiniteQcd.lean:109 area_exponent` | `(r t : Nat) (hr : 1 ≤ r) (ht : 1 ≤ t) : r * t + (r - 1) * (t - 1) = r * (t - 1) + (r - 1) * t + 1` |
| `lean4/CampaignTfq0011FiniteQcd.lean:114 perim_exponent` | `(r t : Nat) : 2 * (r + t) + 2 * ((r - 1) + (t - 1)) = 2 * (r + (t - 1)) + 2 * ((r - 1) + t)` |
| `lean4/CampaignTfq0011FiniteQcd.lean:119 creutz_area` | `(b : Rat) (hb : b ≠ 0) (r t : Nat) (hr : 1 ≤ r) (ht : 1 ≤ t) : creutz (areaMonomial b r t) (areaMonomial b (r - 1) (t - 1)) (areaMonomial b r (t - 1)) (areaMonomial b (r - 1) t) = b` |
| `lean4/CampaignTfq0011FiniteQcd.lean:129 creutz_perim` | `(b : Rat) (hb : b ≠ 0) (r t : Nat) (hr : 1 ≤ r) (ht : 1 ≤ t) : creutz (perimMonomial b r t) (perimMonomial b (r - 1) (t - 1)) (perimMonomial b r (t - 1)) (perimMonomial b (r - 1) t) = 1` |
| `lean4/CampaignTfq0011FiniteQcd.lean:142 creutz_one_ninth` | `: creutz (areaMonomial (1 / 9) 2 2) (areaMonomial (1 / 9) 1 1) (areaMonomial (1 / 9) 2 1) (areaMonomial (1 / 9) 1 2) = 1 / 9 ∧ creutz (areaMonomial (1 / 9) 3 3) (areaMonomial (1 / 9) 2 2) (areaMonomial (1 / 9) 3 2) (areaMonomial (1 / 9) 2 3) = 1 / 9 ∧ creutz (perimMonomial (1 / 9) 2 2) (perimMonomial (1 / 9) 1 1) (perimMonomial (1 / 9) 2 1) (perimMonomial (1 / 9) 1 2) = 1 ∧ creutz (perimMonomial (1 / 9) 3 3) (perimMonomial (1 / 9) 2 2) (perimMonomial (1 / 9) 3 2) (perimMonomial (1 / 9) 2 3) = 1 ∧ (1 / 9 : Rat) ≠ 1` |
| `lean4/CampaignTfq0011FiniteQcd.lean:159 declared_lattice_counts` | `: ((9 : Int) - 1 = 8) ∧ ((12 : Int) - 9 + 1 = 4) ∧ ((12 : Int) - 8 = 4)` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_281_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
