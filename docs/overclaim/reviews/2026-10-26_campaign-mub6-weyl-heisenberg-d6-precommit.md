# Review of campaign-mub6-weyl-heisenberg-d6-precommit

Scope: uncommitted derivation of MUB6-WEYL-HEISENBERG-D6 on derive/MUB6-WEYL-HEISENBERG-D6, merge base 4fea09ae176aae31115e38bb2b21819237055811. Reviewed against the standing statement in dag/fragments/unified_dag.json. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: scripts/overclaim_scan.py --changed-since origin/main --strict. Read the standing statement, obligation, and the cited declarations in lean4/CampaignMub6WeylHeisenbergD6.lean with the #print axioms lines from the campaign build. The campaign build was lake build CampaignMub6WeylHeisenbergD6, exit 0, Lean 4.35.0. This review did not rebuild. Cargo was not run.

Result: 1 node FULL against the narrowed standing statement, 0 NARROWED, 0 OVERCLAIM. No node was raised. The campaign outcome is Narrowed because the source claim is wider than the standing statement. Status stays IMPORTED_ASSUMPTION.

Corrections to the PR's own text:
- MUB6-WEYL-HEISENBERG-D6: an earlier draft called the integer pairs a ring. No declaration states the ring axioms. The standing statement says "set of integer pairs" and "matrices over those pairs".

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| MUB6-WEYL-HEISENBERG-D6 | w_sq, w_cube, w_six, conj_pair, shift_entry, clock_entry, zx_eq, xz_ne, hs_orth | FULL | Every atomic claim of the standing integer-pair statement is the type of a cited declaration. The complex exponential, the identification of w with exp(2 pi i / 6), and any count of mutually unbiased bases are in the obligation and are not claimed. Status stays IMPORTED_ASSUMPTION. |

Atomic claims of the standing statement:

- Product (a, b)*(c, d) = (a*c - b*d, a*d + b*c + b*d) is rMul (lean4/CampaignMub6WeylHeisenbergD6.lean:16).
- Conjugate (a + b, -b) is conj_pair (line 32). Axioms: none.
- w*w = w - (1, 0) is w_sq (line 29): rMul w w = rSub w rOne, with rOne = (1, 0) and rSub coordinate subtraction (lines 15, 20). Axioms: none.
- w*w*w = (-1, 0) is w_cube (line 30): wpow 3 = rNegOne. wpow iterates rMul by w (lines 25-27). Axioms: none.
- The sixth power of w is (1, 0) is w_six (line 31): wpow 6 = rOne. Axioms: none.
- Shift X has a 1 at each (j+1 mod 6, j) is shift_entry (line 399). Axioms: propext.
- Clock Z is diagonal with entry w^j is clock_entry (line 403): wpow of the diagonal index. Axioms: propext.
- Z X = w X Z is zx_eq (line 407). mScale multiplies each entry on the left by w (line 192). Axioms: propext.
- X Z and w Z X differ is xz_ne (line 410). Axioms: propext.
- For p, q, r, s in Fin 6, the trace of the conjugate-transpose of X^p Z^q times X^r Z^s is (6, 0) when the exponents match and (0, 0) otherwise is hs_orth (line 856). rSix is (6, 0) and rZero is (0, 0) (lines 19, 22). Axioms: propext, Classical.choice, Quot.sound.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| checks/independent/mub6-weyl-heisenberg-d6.py | operators=36, pairs=1296, comm_mismatch=0, opposite_mismatch=6, entry_fail=0, orth_fail=0 | python -I -X utf8 checks/independent/mub6-weyl-heisenberg-d6.py printed those values and exited 0. 36 is the count of (p, q) with p, q in 0..5. 1296 is the count of (p, q, r, s). | match |
| derivation note | 36 operators, 1296 ordered pairs, 6 opposite-convention mismatches | same independent check | match |
| README.md | derivation papers 1116; resolving Lean refs 2554; lean4 tracked files 1047; lake libraries 138; module roots 990 | scripts/build_readme_facts.py --check passed. The increments from the base row are +1 paper, +9 Lean refs, +1 lean4 file, +1 library, +1 root. | match |
| standing statement | dimension 6, trace (6, 0) or (0, 0), exponents 0 through 5 | hs_orth quantifies over Fin 6 and returns rSix or rZero | match |

## Scanner output
HIGH 0, MEDIUM 0, LOW 3. No new HIGH findings. The three LOW findings are the existing baseline items, not this node: R10 TENSOR-ASSUMPTION-COUNTERMODELS (cited Lean modules in no replay receipt), R5 tfq_1019 number 20261019, R5 tfq_0413 fractions 1/2 and 1/4. No baseline change.

What the scanner could not decide: the import closure is empty because the module has no import. Keeping IMPORTED_ASSUMPTION while the narrowed statement matches Lean is a campaign choice, not a status rise. The source commutation X Z = w Z X is recorded as the opposite clock convention and is not the proved identity.
