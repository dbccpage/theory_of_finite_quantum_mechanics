# Overclaim Review: `campaign/tfq-0010` (`TFQ-0010`)

- **Date**: 2026-10-24
- **Node**: `TFQ-0010` (`FINITE_QED`)
- **Branch**: `campaign/tfq-0010`
- **AuthorityEffect**: `None`

## 1. What It Supports
- Formalizes the exact finite identities for discrete Ward coboundary invariance, Gaussian-rational `Q(i)` charged link transport, 2x2 Clifford/CAR occupation projectors, rational Dirac-Coulomb `n=2` fine structure, 1-loop QED Lamb shift contact datum (`91/120`), and Weinberg electroweak mixing/anomaly controls in `lean4/CampaignTfq0010FiniteQed.lean` (`L4D`, 10 theorems, 0 sorrys).
- Verifies all 3345 independent checks in `checks/independent/tfq-0010.py` and kills 6/6 semantic mutations in `dag/research/campaign_tfq-0010_lean_mutation.json`.

## 2. What It Does Not Support
- Does not claim a derivation of continuum QED or continuum electroweak theory from the finite controls or from the `F002` interface inventory.

## 3. Narrowest Defensible Claim
The finite QED and electroweak shadow controls in `FiniteQM.lean` and `CampaignTfq0010FiniteQed.lean` verify exact rational and Gaussian-rational algebraic identities on finite carriers without authorizing continuum QED.

## 4. Next Test Needed
Add a multi-plaquette simplicial U(1) Ward-Takahashi difference control paired with the `F002` interface fence.
