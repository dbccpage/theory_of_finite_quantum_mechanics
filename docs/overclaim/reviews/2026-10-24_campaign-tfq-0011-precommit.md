# Overclaim Review: `campaign/tfq-0011` (`TFQ-0011`)

- **Date**: 2026-10-24
- **Node**: `TFQ-0011` (`FINITE_QCD`)
- **Branch**: `campaign/tfq-0011`
- **AuthorityEffect**: `None`

## 1. What It Supports
- Formalizes the exact rational `SU(3)` Casimir/Fierz identities, Wilson-loop Creutz ratios, `beta_0`/`beta_1` asymptotic freedom and Banks-Zaks controls, naive lattice Dirac `2^d - 1` doubler obstruction, and epistemic scope fences in `lean4/CampaignTfq0011FiniteQcd.lean` (`L4D`, 10 theorems, 0 sorrys).
- Verifies all 451 independent checks in `checks/independent/tfq-0011.py` and kills 6/6 semantic mutations in `dag/research/campaign_tfq-0011_lean_mutation.json`.

## 2. What It Does Not Support
- Does not identify the finite Wilson-loop or `beta_0` controls with continuum QCD confinement, and does not allow floating-point benchmarks to authorize finite statements.

## 3. Narrowest Defensible Claim
The finite QCD shadow controls verify exact rational algebraic identities and record lattice Dirac doubling as an explicit obstruction while keeping continuum QCD open on `F002`.

## 4. Next Test Needed
Add a multi-plaquette `SU(3)` matrix holonomy test over `Q(i)` paired with the `F002` open-interface fence.
