# Overclaim review: MUB-PRIME-POWER-CONSTRUCTION

AuthorityEffect: None.

## Scope

The narrowed statement of MUB-PRIME-POWER-CONSTRUCTION (record TFQ-0403). Status stays OPEN. No other node is in this review.

## Method

The module `lean4/CampaignMubPrimePowerConstruction.lean` was read in full and built with `lake build CampaignMubPrimePowerConstruction` under Lean 4.35.0. It has no import. Mathlib v4.35.0 commit 56a005855ea17e0b0958f73ec801ae140b0a1679 was present through a junction and unused by this module. Each `#print axioms` line was read from that build. The independent check `checks/independent/mub-prime-power-construction.py` recomputed the same Gaussian-integer identities. Every numeral in the narrowed statement was recomputed that way.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

## Corrections to the PR's own text

None. The statement is the dimension-2 family. Larger prime powers, odd characteristic, a general character sum, and dimension six stay in the bottleneck. Status stays OPEN.

## Per-node table

| Node | Theorems that discharge it | Verdict | Reason |
|---|---|---|---|
| MUB-PRIME-POWER-CONSTRUCTION | `i_squared`, `squared_norms`, `self_inner`, `basis_orthogonal`, `cross_unbiased`, `char_values`, `char_of_double` | NARROWED | The theorems are six explicit vectors and the two-element character. They do not construct a family at any larger prime power. Status stays OPEN. |

### Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| the square of i is -1 | `i_squared` | NARROWED |
| squared norms are 1, 1, 2, 2, 2 and 2 | `squared_norms` | NARROWED |
| each vector's inner product with itself is that squared norm | `self_inner` | NARROWED |
| vectors inside one basis have inner product 0 | `basis_orthogonal` | NARROWED |
| twelve cross-basis pairs satisfy twice the squared modulus equals the product of the squared norms | `cross_unbiased` | NARROWED |
| the two-element character sends 0 to 1 and 1 to -1 | `char_values` | NARROWED |
| the character sends 1+1 to 1 | `char_of_double` | NARROWED |
| a complete family for a larger prime power | not proved | NOT PROVED |
| odd characteristic and a general character sum | not proved | NOT PROVED |
| a dimension-six family | not proved | NOT PROVED |

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 2 | dimension, and the squared norm of each X and Y vector | match |
| 1 | squared norm of each Z vector, and the character of 0 | match |
| -1 | square of i in the real component, and the character of 1 | match |
| 0 | inner product inside each basis, and 1+1 in the two-element field | match |
| 34 | conditions counted by the independent check | match |
| 0 | failures counted by that check | match |

## Axioms

`i_squared`, `squared_norms`, `self_inner`, `basis_orthogonal`, `cross_unbiased`, `char_values`, and `char_of_double` depend on no axioms. The module contains no `sorry`, no `axiom` declaration, no `native_decide`, and no `unsafe`.

## What the scanner could not decide

`scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH 0, MEDIUM 0, LOW 3. Those LOW findings sit on evidence pages refreshed from origin/main and were left unchanged.

These twelve pairs do not prove a statement quantified over every prime power. The scanner cannot tell this dimension-2 family from the original parameterized construction; the table above is the decision.
