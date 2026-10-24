# Overclaim Review: `campaign/tfq-0171` (`TFQ-0171`)

- **Date**: 2026-10-24
- **Node**: `TFQ-0171` (`IMPLEMENTATION_SIBLING`)
- **Branch**: `campaign/tfq-0171`
- **AuthorityEffect**: `None`

## 1. What It Supports
- Separates unnormalized finite Boolean valuations (`finite_valuation.rs`), scaled integer simplex grids (`H001ProbabilitySimplex.lean`), signed quasi-probability valuations (`signed_representation.rs`), deterministic context vertices (`local_deterministic.rs`), and marginal scenarios (`marginal_compatibility.rs`) from the normalized rational probability simplex (`simplex.rs`).

## 2. What It Does Not Support
- Does not collapse unnormalized finite valuations or fixed-scale integer grids into the normalized rational probability simplex.

## 3. Narrowest Defensible Claim
All 10 theorems in `lean4/CampaignTfq0171ImplementationSibling.lean` compile with zero sorrys/axioms, all 6 semantic mutations are killed, and `checks/independent/tfq-0171.py` passes 200 exact-rational checks.

## 4. Next Test Needed
Proceed to `TFQ-0183`.
