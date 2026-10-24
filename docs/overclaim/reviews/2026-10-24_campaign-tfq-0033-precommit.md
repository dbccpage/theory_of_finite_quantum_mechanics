# Pre-Commit Claim Hygiene Review: `TFQ-0033` (`FINITE_QCD`)

- **Date**: 2026-10-24
- **Branch**: `campaign/tfq-0033`
- **Node**: `TFQ-0033` (`FINITE_QCD`)
- **Scanner**: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict`

## Review Summary
1. **What it supports**: Exact rational `SU(3)` diquark Casimir arithmetic (`-2/3`, `+1/3`), explicit 3-index alternating contraction `eps3` / `baryonEpsilonContract`, pairwise baryon Casimir sum `3 * (-2/3) = -2`, and non-equivalence between 2-index diquarks (`dim 3`, `C_2 = 4/3`) and 3-index baryon singlets (`dim 1`, `C_2 = 0`).
2. **What it does not support**: Does not claim that `qcd_beta0_wilson_confinement_control.rs` implements the 3-index baryon contraction or spatial 3-body wavefunctions.
3. **Narrowest defensible claim**: `-2/3` and `+1/3` are two-index diquark Casimir factors, while a baryon color singlet requires an explicit three-index alternating contraction `ε_{ijk} u_i v_j w_k`.
4. **Next test needed**: Proceed to the next finite derivation in `dag/pfp/campaign/derivation_queue.json`.
