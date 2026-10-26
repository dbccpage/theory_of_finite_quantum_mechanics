# Overclaim review: TFQ-0171 positive-mass narrowing

Scope: worktree `derive/TFQ-0171` against `origin/main` at `7a26a36b6460`. One node edited: TFQ-0171. Status stays OPEN.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Read `lean4/CampaignTfq0171PositiveMass.lean` against the node statement. Rebuilt that module with Lean 4.35.0 (`lake build CampaignTfq0171PositiveMass`, exit 0). Ran `python -I -X utf8 checks/independent/tfq-0171.py` (checks=519, failed=0).

Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM. Status was not raised.

## Statement versus theorem

| Claim | Declaration | Verdict |
|---|---|---|
| For all natural numbers a and b at least 1, a + b is not 1 | `CampaignTfq0171PositiveMass.positivePairMassNotOne` | FULL |
| The pair (1, 1) sums to 2 | `CampaignTfq0171PositiveMass.oneOneMass` | FULL |
| 2 is not 1 | `CampaignTfq0171PositiveMass.twoNotOne` | FULL |
| The empty mass 0 is not 1 | `CampaignTfq0171PositiveMass.emptyMassNotOne` | FULL |
| In the rationals, 1/2 + 1/2 = 1 | `CampaignTfq0171PositiveMass.halfPairSumsToOne` | FULL |
| 1 + 1 is not 1 | `CampaignTfq0171PositiveMass.oneOneNotUnit` | FULL |
| The pair (1, 1) is not the pair (1/2, 1/2) | `CampaignTfq0171PositiveMass.unnormalizedPairDiffers` | FULL |
| If a + b is positive, then a/(a + b) + b/(a + b) = 1 | `CampaignTfq0171PositiveMass.normalizeByTotal` | FULL |
| A general Boolean valuation, the Rust module contracts, and a ban on standing in for a unit-sum law stay outside this finite case | not proved | NOT PROVED |

The node statement still contains that last scope sentence, so the node is not PROVED_LEAN. Status remains OPEN.

## Axioms

`positivePairMassNotOne`, `oneOneMass`, `twoNotOne`, and `emptyMassNotOne` depend on no axioms. `halfPairSumsToOne`, `oneOneNotUnit`, `unnormalizedPairDiffers`, and `normalizeByTotal` depend only on `propext`, `Classical.choice`, and `Quot.sound`.

## Numbers recomputed

The checker enumerates a and b from 0 through 12. Pairs with both coordinates at least 1: 12 * 12 = 144, each with sum at least 2 and not 1. Pairs with positive total: 13 * 13 - 1 = 168, each normalizing under exact `Fraction`. The printed total is 519 and the run exited 0. The statement numbers 0, 1, 2, and 1/2 match those checks and the Lean declarations. No other number is claimed.

## What the scanner could not decide

Three LOW findings are on notes and modules pulled in because regenerated sha256 lines touched `FQ-GAP-TENSOR-UNIQUENESS` and `TENSOR-ASSUMPTION-COUNTERMODELS`. They are not claims of this narrowing. AuthorityEffect: None.
