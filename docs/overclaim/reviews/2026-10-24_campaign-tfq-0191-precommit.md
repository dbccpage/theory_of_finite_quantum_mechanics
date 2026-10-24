# Overclaim Review: `campaign/tfq-0191` (`TFQ-0191`)

- **Date**: 2026-10-24
- **Node**: `TFQ-0191` (`IMPLEMENTATION_SIBLING`)
- **Branch**: `campaign/tfq-0191`
- **AuthorityEffect**: `None`

## 1. What It Supports
- Formalizes interval measurement evidence separation (`IntervalRequiresPolicy`), affine calibration and finite chain clock interval width propagation, and the exact discrepancy of `f64`-built fixed-scale decimals (`BigDecimal::from_f64_unchecked`) across 10 sorry-free Lean 4 theorems and 280 Python checks.

## 2. What It Does Not Support
- Does not promote interval evidence to a governance scalar without a policy or allow `f64`-built decimals to authorize exact bounds.

## 3. Narrowest Defensible Claim
All 10 theorems in `lean4/CampaignTfq0191ImplementationSibling.lean` compile with zero sorrys/axioms, all 6 semantic mutations are killed, and `checks/independent/tfq-0191.py` passes 280 checks.

## 4. Next Test Needed
Proceed to `TFQ-0199`.
