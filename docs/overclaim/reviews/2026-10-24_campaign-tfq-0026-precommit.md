# Pre-Commit Claim Hygiene Review: `TFQ-0026` (`FINITE_QCD`)

- **Date**: 2026-10-24
- **Branch**: `campaign/tfq-0026`
- **Node**: `TFQ-0026` (`FINITE_QCD`)
- **Scanner**: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict`

## Review Summary
1. **What it supports**: Euclidean Clifford algebra relations over `ℤ[i]`, `2^d` naive species count on even-period periodic lattices, rational Wilson corner mass lifting `m + 2rc`, `MAX_CARRIER_DIMENSION = 128` admission guard, and chiral symmetry breaking by scalar Wilson mass.
2. **What it does not support**: Does not take a continuum limit or establish continuum topological index theorems.
3. **Narrowest defensible claim**: On declared finite periodic lattices (`N ≥ 3`, carrier dimension `≤ 128`), the naive symmetric-difference operator has `2^d` zero-velocity corners for even `N`, and a positive rational Wilson coefficient lifts all non-zero `π`-corners at the cost of breaking `γ₅` anticommutativity.
4. **Next test needed**: Proceed to Rank 26 finite QCD derivation (`TFQ-0027`).
