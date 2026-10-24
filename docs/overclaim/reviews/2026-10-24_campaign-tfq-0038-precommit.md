# Overclaim Review: `campaign/tfq-0038` (`TFQ-0038`)

- **Date**: 2026-10-24
- **Node**: `TFQ-0038` (`FINITE_QCD`)
- **Branch**: `campaign/tfq-0038`
- **AuthorityEffect**: `None`

## 1. What It Supports
- Formalizes the exact `Conf_2(G)` Betti accounting, the side-by-side separation of the two `Conf_2(K_5)` boundary-rank readings (`rank_Q = 7, b_1 = 14` vs `rank_Q = 15, rank_F2 = 14, b_1(Q) = 6, b_1(F_2) = 7, tors = 1`), and the unresolved exchange-loop representative fences in `lean4/CampaignTfq0038FiniteQcd.lean` (`L4D`, 10 theorems, 0 sorrys).
- Verifies all 4990 independent checks in `checks/independent/tfq-0038.py` and kills 6/6 semantic mutations in `dag/research/campaign_tfq-0038_lean_mutation.json`.

## 2. What It Does Not Support
- Does not claim that the exchange loop on `Conf_2(K_5)` is proved to have order 2 in homology.

## 3. Narrowest Defensible Claim
The `rank_Q = 7` (`b_1 = 14`) disjoint-edge square boundary rank and the `rank_Q = 15, rank_F2 = 14` (`b_1(Q) = 6, b_1(F_2) = 7`) literal certificate on `Conf_2(K_5)` are kept apart as distinct readings, and the exchange-loop torsion representative question remains open.

## 4. Next Test Needed
Identify the explicit 2-cell family on `Conf_2(K_5)` that produces `(rank_Q, rank_F2) = (15, 14)` and compute the Smith normal form coordinates of the exchange loop.
