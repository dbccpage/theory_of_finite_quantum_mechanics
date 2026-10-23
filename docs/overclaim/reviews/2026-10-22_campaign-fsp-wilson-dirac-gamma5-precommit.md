# Review of campaign/fsp-wilson-dirac-gamma5 before commit

**AuthorityEffect:** None.

Scope: uncommitted working tree of `campaign/fsp-wilson-dirac-gamma5` in `C:\gw\tfqm`, base `origin/main` (merge base `3924d378ff1de685948bf2b419dc63a5a9560881`). There is no commit on the branch and no pull request. Reviewed against `FSP-WILSON-DIRAC-GAMMA5` as it stands in `dag/fragments/application_branches.json:3263-3283`, and against the uncommitted module that would be cited for it. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the node statement, bottleneck, and empty `lean` list; read each declaration named by `#print axioms` in `lean4/CampaignFspWilsonDiracGamma5.lean`. Ran `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` from the worktree (exit 0, HIGH 0, MEDIUM 0, LOW 0, merge base `3924d378ff1d`). Ran `checks/independent/fsp-wilson-dirac-gamma5.py` with `python -I -X utf8` (exit 0). Recomputed the witness determinant, its square, the characteristic polynomial, and `gamma5 M gamma5 - Mᴴ` with a separate `fractions.Fraction` elimination, not the check's SymPy code. Lean was not rebuilt. Axiom lines are taken from the previous `lake build CampaignFspWilsonDiracGamma5` log `C:\Users\a343o\AppData\Local\Temp\wilson_lake5.log` (that build printed `EXIT:1`). Cargo was not run. No replay receipt is in the tree.

Result: 1 node reviewed. 0 FULL, 0 NARROWED, 1 OVERCLAIM for any citation of this module as discharging the node. No node was raised. Status stays `IMPORTED_ASSUMPTION`. No commit and no pull request follow from this review.

## Corrections to text that would be committed

- Node statement (`dag/fragments/application_branches.json:3267`): "The Wilson-Dirac operator satisfies gamma5 D_W gamma5 = D_W^dagger, so its nonreal eigenvalues come in conjugate pairs and det D_W is real; for two degenerate flavors det(D_W)^2 >= 0." The only declarations that compile with the three allowed axioms do not mention `diracOp`. Citing them for this sentence would present a hypothesis, or a lemma about a different object, as the theorem. Do not add them to the node's `lean` list and do not change the status.
- Module section comment (`lean4/CampaignFspWilsonDiracGamma5.lean:906`): "Witness: 2×2 periodic lattice, mass -1, det = -3". `witness_det_eq_neg_three` (`lean4/CampaignFspWilsonDiracGamma5.lean:1091`) has that type and depends on `sorryAx` (log line 1125). The determinant `-3` is a Python fact about the matrix built from the Wilson formula.
- Module header (`lean4/CampaignFspWilsonDiracGamma5.lean:19-21`) names gamma5-hermiticity, the characteristic polynomial, and the two-flavor square as the scope of the campaign file. `wilson_dirac_gamma5_consequences` (`lean4/CampaignFspWilsonDiracGamma5.lean:785`) states those conjuncts and depends on `sorryAx` (log line 1123).
- Source-corpus sentence `papers/core/fsp/theory_of_finite_fsp.md:468` ("det(D_W) is real and strictly non-negative for two degenerate flavors", status line `PROVED_LEAN` at line 465) is not in this diff. The node `source_status` already records that audit. Do not copy that sentence into a derivation note or a pull-request body.
- `periodic_wilson_consequences` (`lean4/CampaignFspWilsonDiracGamma5.lean:892-904`) states only the adjoint identity and `star (det) = det` for a rectangular periodic lattice, and it depends on `sorryAx`. It does not state conjugate root multiplicities or the two-flavor square.

What the four clean declarations do state, and must not be substituted for the node:

- `euclideanClifford2` (`lean4/CampaignFspWilsonDiracGamma5.lean:120`): there is a Euclidean Clifford representation in dimension 2 on spin space `Fin 2`. Axioms: propext, Classical.choice, Quot.sound (log line 1115).
- `charpoly_rootMultiplicity_conj` (`lean4/CampaignFspWilsonDiracGamma5.lean:736`): if every coefficient of a polynomial `p : ℂ[X]` is fixed by `star`, then `p.rootMultiplicity (star z) = p.rootMultiplicity z`. The real-coefficient hypothesis is an assumption of the theorem. Axioms: the three allowed (log line 1120).
- `two_flavor_det_eq_sq` (`lean4/CampaignFspWilsonDiracGamma5.lean:772`): for every matrix `D`, `det (fromBlocks D 0 0 D) = (det D)^2`. Axioms: the three allowed (log line 1121).
- `two_flavor_det_real_nonneg` (`lean4/CampaignFspWilsonDiracGamma5.lean:776`): if `star z = z`, then `(z ^ 2).im = 0` and `0 ≤ (z ^ 2).re`. Reality of `z` is an assumption. Axioms: the three allowed (log line 1122).

## Per-node table

Node: FSP-WILSON-DIRAC-GAMMA5. Status on the base and in the working tree: `IMPORTED_ASSUMPTION`. `lean` is `[]`. Bottleneck on disk (`application_branches.json:3277`): "A single-flavor det D_W can be negative; the JSONL claim that det D_W is nonnegative is only the two-flavor square. Not established in this checkout."

| Atomic claim in the node statement | Declaration whose type would have to state it | Verdict |
|---|---|---|
| `gamma5 D_W gamma5 = D_Wᴴ` for the Wilson-Dirac operator | `gamma5_wilson_adjoint` (`lean4/CampaignFspWilsonDiracGamma5.lean:598`) states it for every `WilsonDirac` (`:318`, real `mass`, `link_unitary`). `periodic_wilson_consequences` (`:892`) states it for every finite rectangular periodic lattice. Both depend on `sorryAx` (log lines 1117 and 1124). | OVERCLAIM if cited. Not proved. |
| Nonreal eigenvalues come in conjugate pairs | `charpoly_rootMultiplicity_conj` (`:736`) states equal algebraic multiplicities of `z` and `star z` for a polynomial whose coefficients are already fixed by `star`. `charpoly_coeff_conj` (`:721`) would supply that hypothesis for `(diracOp W).charpoly` and depends on `sorryAx` (log line 1119). The node says eigenvalues; the clean lemma says root multiplicity of an arbitrary polynomial. | OVERCLAIM if cited. Not proved for `D_W`. |
| `det D_W` is real (`star (det) = det`) | `det_eq_conj` (`:688`) states it and depends on `sorryAx` (log line 1118), through `gamma5Op_sq` and `gamma5_wilson_adjoint`. | OVERCLAIM if cited. Not proved. |
| Two degenerate flavors: `det(D_W ⊕ D_W) = (det D_W)^2` is a nonnegative real | `two_flavor_det_eq_sq` (`:772`) is the block-determinant identity for every matrix. `two_flavor_det_real_nonneg` (`:776`) is the square of a number already assumed real. The packaged conjuncts are `wilson_dirac_gamma5_consequences` (`:785-803`), which depends on `sorryAx` (log line 1123) because it uses `det_eq_conj`. | The two lemmas are FULL for their own types. Citing them for `D_W` is OVERCLAIM. |
| A Euclidean representation exists in dimension 2 | `euclideanClifford2` (`:120`), three allowed axioms. | FULL for this atom. The node statement does not say this, and this atom does not discharge the node. |
| A Euclidean representation exists in dimension 4 | `euclideanClifford4` (`:289`) depends on `sorryAx` (log line 1116). The open goal in that build is `temporal_sq` (`:206`): `fromBlocks (1 * 1) 0 0 (1 * 1) = 1`. The independent check's `d = 4` relations returned exit 0. | Not proved in Lean. |
| On the periodic 2×2 lattice, `d = 2`, mass `-1`, color `U(1)`, `det D_W = -3`, and the two-flavor determinant is `9` | `witness_det_eq_neg_three` (`:1091`), `witness_det_neg` (`:1096`), `witness_two_flavor_det` (`:1102`) all depend on `sorryAx` (log lines 1125-1127). The build left `if 1 = -1` in the row lemmas (`:1045` through `:1061`) and `3 ^ 2 = 9`, `0 ≤ (3 ^ 2).re` at `:1108-1109`. | Not proved in Lean. Exact computation matches; see the numbers table. |

`WilsonDirac.link_unitary` (`:325`) is part of the structure, so every compiled statement about `diracOp W` has unitary links as data. Whether a future proof term uses that field is not settled: `gamma5_wilson_adjoint` does not compile.

The source text of the module contains no `sorry`, `admit`, `axiom`, `native_decide`, or `unsafe` token. The build still reports `sorryAx` on the nine declarations above. That is the same defect as scanner rule R3 for a PROVED_LEAN citation: elaboration recovered with `sorryAx`. The scanner did not flag it, because no node cites the module and the token is not in the source.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Independent check and `witnessLiteral` (`lean4/CampaignFspWilsonDiracGamma5.lean:1002-1010`); section comment `:906` | `det = -3` for the 8×8 witness matrix | `fractions.Fraction` Gaussian elimination on that literal: `(-3, 0)`. The check builds the same matrix from the Wilson formula (`checks/independent/fsp-wilson-dirac-gamma5.py:98-154`), requires equality with the literal, and prints `det -3` (exit 0). | Match. Lean equality `det (diracOp witnessWilson) = -3` is unproved. |
| Same witness, two-flavor block diagonal | `det(D ⊕ D) = 9` and the value is a nonnegative real | Elimination: `det^2 = (9, 0)`. Check prints `two_flavor_det 9`. | Match as a computation. `witness_two_flavor_det` depends on `sorryAx`. |
| Characteristic polynomial of `det(λI - M)`, high degree first | `[1, -8, 28, -56, 66, -40, 4, 8, -3]` | Newton interpolation of `det(tI - M)` at `t = 0..8` over `Fraction`: the same nine coefficients. Constant term `-3` agrees with `det M` at even size 8. Check prints the same list. | Match as a computation. No Lean theorem states these coefficients. |
| `gamma5 M gamma5 = Mᴴ` on the witness literal, with the `d = 2` gamma5 | identity holds | Separate complex-rational product: 0 mismatched entries. The check requires the same identity on the matrix built from the formula. | Match as a computation. `gamma5_wilson_adjoint` depends on `sorryAx`. |
| Single-flavor sign | imaginary part 0, real part negative | Elimination: imaginary part 0, real part `-3 < 0`. Check requires `re < 0` and `im = 0`. | Match as a computation. This agrees with the bottleneck that a single flavor can be negative. It is not a Lean theorem. |
| `d = 2` and `d = 4` Clifford relations in the check | squares, hermiticity, anticommutators | Required inside `checks/independent/fsp-wilson-dirac-gamma5.py` before it prints; the script exited 0. No second `d = 4` script was run. | Match for the check's own requirements. `euclideanClifford4` depends on `sorryAx`. |

No numeric mismatch. The Lean file's `-3` and `9` are claims of declarations that do not compile with the three allowed axioms.

## Scanner output

`scripts/overclaim_scan.py --changed-since origin/main --strict`: HIGH 0, MEDIUM 0, LOW 0. Changed files seen by git are the dirty `lean4/lakefile.lean` and the untracked Lean module and independent check. The node status did not change, so R9 does not fire. R3 does not fire: the module has no source-level `sorry`. R1, R4, and R10 do not fire: nothing cites the module and there is no replay receipt.

Findings the scanner could not decide, decided here:

- `sorryAx` in the previous build's `#print axioms` output. Nine declarations that state the node's mathematics depend on it. Treat a future PROVED_LEAN citation of those declarations as OVERCLAIM until a rebuild prints only propext, Classical.choice, and Quot.sound.
- `charpoly_rootMultiplicity_conj` assumes real coefficients. `two_flavor_det_real_nonneg` assumes `star z = z`. `two_flavor_det_eq_sq` is about every matrix. None of these is `gamma5 D_W gamma5 = D_Wᴴ`.
- The section comment at line 906 states `det = -3` above a theorem that did not close.
- The paper sentence at `papers/core/fsp/theory_of_finite_fsp.md:468` is outside the diff. It remains a source-corpus status claim. This review does not edit it.

No baseline entry is proposed. `docs/overclaim/report.md` and `report.json` were not written and must not be committed.

## Gate

Do not cite the unfinished module for `FSP-WILSON-DIRAC-GAMMA5` and do not raise its status. The status to keep is `IMPORTED_ASSUMPTION`.

## Shipped module (rebuild after the gate)

The unfinished proofs were removed before commit. `temporal_sq` was closed with `mul_one` before `fromBlocks_one`. A later build of the cut module, Lean 4.35.0, log `C:\Users\a343o\AppData\Local\Temp\wilson_lake6.log`, printed `Build completed successfully` and `EXIT:0`. This review did not treat the earlier `EXIT:1` log as the receipt for the shipped file.

`#print axioms` on the shipped file:

- `euclideanClifford2` (`lean4/CampaignFspWilsonDiracGamma5.lean:368` in that build): propext, Classical.choice, Quot.sound
- `euclideanClifford4`: the same three axioms. Dimension 4 is checked.
- `charpoly_rootMultiplicity_conj`: the same three axioms. The real-coefficient hypothesis remains an assumption.
- `two_flavor_det_eq_sq`: the same three axioms. The statement is for every matrix.
- `two_flavor_det_real_nonneg`: the same three axioms. Reality of the input remains an assumption.

The node statement is unchanged. `lean` stays empty. These five declarations still do not state `gamma5 D gamma5 = D†`, reality of `det D_W`, or `det = -3`. Citing them as the node would remain OVERCLAIM. The independent check still matches `-3`, `9`, and the characteristic polynomial `[1, -8, 28, -56, 66, -40, 4, 8, -3]`. That check is not a Lean proof.
