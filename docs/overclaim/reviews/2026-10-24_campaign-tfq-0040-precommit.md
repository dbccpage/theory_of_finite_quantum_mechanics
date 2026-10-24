# Overclaim Review: `campaign/tfq-0040` (`TFQ-0040`)

- **Date**: 2026-10-24
- **Node**: `TFQ-0040` (`FINITE_QCD`)
- **Branch**: `campaign/tfq-0040`
- **AuthorityEffect**: `None`

## 1. What It Supports
- Formalizes the `QM-221` Casimir/Fierz and `81`-entry dimension identities, the `QM-213` `B_2(Q)` punctured-diamond holonomy split (`tr = 5/2, det = 1`), the `3! = 6` Levi-Civita baryon contraction, the ABJ `N_c = 3` color factor, and the tri-language coverage and `F002.S001` scope fences in `lean4/CampaignTfq0040FiniteQcd.lean` (`L4D`, 10 theorems, 0 sorrys).
- Verifies all 209 independent checks in `checks/independent/tfq-0040.py` and kills 6/6 semantic mutations in `dag/research/campaign_tfq-0040_lean_mutation.json`.

## 2. What It Does Not Support
- Does not claim that `F002.S001` is closed or that floating-point prints can authorize exact algebraic identities.

## 3. Narrowest Defensible Claim
Finite QCD controls require all three language twins before being classified as tri-language, floating-point prints are rejected as exact certificates, and `F002.S001` remains an open bridge.

## 4. Next Test Needed
Port the matrix-valued `Q(i)` Gribov diamond check into a standalone Python module and wire it to `TFQ-0042`.
