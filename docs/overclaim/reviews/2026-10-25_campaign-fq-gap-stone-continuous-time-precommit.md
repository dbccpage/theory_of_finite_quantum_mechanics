# Review of FQ-GAP-STONE-CONTINUOUS-TIME

Scope: campaign branch for FQ-GAP-STONE-CONTINUOUS-TIME against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict`, then a statement-versus-theorem reading of FQ-GAP-STONE-CONTINUOUS-TIME. Lean was not rebuilt for this review. The receipt `dag/research/campaign_fq-gap-stone-continuous-time_lean_replay.json` records the earlier `lake build CampaignFqGapStoneContinuousTime` (exit 0, module job 977 ms, replay wall 6325 ms). Axiom lines were read from that build.

Result: 1 node FULL on the standing integer statement. Campaign class Narrowed. 0 OVERCLAIM. No node was raised. Status stays CONDITIONAL.

Corrections to the PR's own text:
- None. The standing statement is the integer equation below. The original fence stays in the bottleneck.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| FQ-GAP-STONE-CONTINUOUS-TIME | `pythagorean345` (`lean4/CampaignFqGapStoneContinuousTime.lean:156`); `fiveMulSqEqFourMulSq` (`lean4/CampaignFqGapStoneContinuousTime.lean:159`) | FULL | The standing statement has two claims, and each claim is the type of one declaration. Status stays CONDITIONAL. |

Standing statement: The integers 3, 4 and 5 satisfy 3 * 3 + 4 * 4 = 5 * 5. For all natural numbers a and b, if 5 * a * a = 4 * b * b then a = 0 and b = 0.

| Claim | Declaration | Verdict |
|---|---|---|
| 3 * 3 + 4 * 4 = 5 * 5 | `pythagorean345` at line 156, closed by `decide` | FULL |
| For all natural numbers a and b, if 5 * a * a = 4 * b * b then a = 0 and b = 0 | `fiveMulSqEqFourMulSq` at line 159 | FULL |

`#print axioms` at lines 171 and 172: `pythagorean345` has no axioms; `fiveMulSqEqFourMulSq` uses propext and Quot.sound. Both sit inside propext, Classical.choice, and Quot.sound.

The Python script audits residues 0, 1, 2, 3, 4 and the pairs with a and b at most 30. That window is an audit. The Lean declaration has no upper bound, and the standing statement has no upper bound.

Older Lean citations remain on the node. They are not the standing statement. Continuous time, the Stone theorem, strong continuity, a one-parameter group, generator selection, causal order, and a rational matrix square root stay in the bottleneck.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Standing statement | 3 * 3 + 4 * 4 = 5 * 5 | 9 + 16 = 25 and 5 * 5 = 25, integer arithmetic in `checks/independent/fq-gap-stone-continuous-time.py` | match |
| Standing statement | equation forces a = 0 and b = 0 | descent on (0, 0); residue table mod 5 is exhaustive; window a, b in 0..30 has only (0, 0) | match |
| Evidence page for this node | grade E3; files 6; symbols found 18; receipt-covered declarations 12 | `docs/evidence/nodes/FQ-GAP-STONE-CONTINUOUS-TIME.md` after `build_evidence.py --write` | match |
| `docs/evidence/README.md` | distinct declarations 1865; receipt-backed 1803; itemised 1735; grades E0 164, E1 222, E2 40, E3 499 | same page; grades match origin/main | match |
| README fact rows for this change | papers 1069; Lean references 2289; lake libraries/roots 91/943; lean4 `.lean` files 1000 | `README.md` from `build_readme_facts.py --write` | match |
| Validator | nodes=925 routes=934 records=977 failures=0 | `dag/validate_derivation_dag.py --no-files` | match |
| Pytest | 32 passed | the six dag receipt tests, 14.61 s | match |

Generator catch-up in the same README and evidence rewrite, not this node's arithmetic: review directories 178 to 208, P4 mutations 43982 to 47271, tracked dag `.lean` files 3 to 2428, flags 270 on 196 nodes to 253 on 190, broken_reference 70 to 53. Scope-effect counts move from consistent 69 and statement_narrowed 65 to consistent 68 and statement_narrowed 66.

## Scanner output

HIGH 0, MEDIUM 0, LOW 5. `--strict` exit 0.

- LOW R10 TENSOR-ASSUMPTION-COUNTERMODELS: pre-existing, file not edited.
- LOW R5 `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`: date 20261019, pre-existing, file not edited.
- LOW R5 `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`: fractions 1/2 and 1/4, pre-existing, file not edited.
- LOW R5 `dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md`: operad numerals, file not edited. In scope because this node is named there.
- LOW R5 `dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md`: numeral 150, file not edited. In scope because this node is named there.

No baseline edit.

## What the scanner could not decide

The scanner does not compare a declaration's type with the English statement. That comparison is the table above. It also does not separate the older carrier citations from the standing statement. Those older citations stay listed, and the bottleneck keeps the fence they belong to.
