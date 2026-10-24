# Pre-Commit Claim Hygiene Review: `TFQ-0027` (`FINITE_QCD`)

- **Date**: 2026-10-24
- **Branch**: `campaign/tfq-0027`
- **Node**: `TFQ-0027` (`FINITE_QCD`)
- **Scanner**: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict`

## Review Summary
1. **What it supports**: Exact rational `wilson_species_count` shell selection, non-anticommutation of scalar Wilson terms with `γ_*`, `zero_mode_count = s*N^d - rank`, zero species under even-`N` antiperiodic twists, and non-equivalence between `IntegralRefinementC3C6.lean` and the lattice Dirac obstruction.
2. **What it does not support**: Does not cite `IntegralRefinementC3C6.lean` as a stand-in for lattice Dirac doubling or take a continuum limit.
3. **Narrowest defensible claim**: `wilson_species_count` selects rational corner shells `m + 2rc = 0`, even-`N` antiperiodic twists eliminate corner zero modes, and `IntegralRefinementC3C6.lean` covers `C₃ → C₆` scalar charge refinement rather than `2^d` lattice Dirac doubling.
4. **Next test needed**: Proceed to Rank 28 finite QCD `β₀` rational arithmetic window derivation (`TFQ-0028`).
