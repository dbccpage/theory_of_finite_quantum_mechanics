Status: AI-drafted, awaiting human review.

# Pre-Commit Overclaim & Falsification Review: `ADS-HAPPY-TOY-NOT-DUALITY-GAP` (`TFQ-2212`)

**Date:** 2026-10-23  
**Campaign Node:** `ADS-HAPPY-TOY-NOT-DUALITY-GAP` (`TFQ-2212`, stage `ADS_CFT`)  
**Outcome:** `Narrowed` (`OPEN` status preserved; flat stabilizer Rényi spectrum vs. 2D CFT Rényi scaling defect, explicit Ryu-Takayanagi deficit witnesses and length-resolved census on the 20-qubit 6-pentagon HaPPY patch, disconnected mutual information jumps, and bulk-to-boundary Hilbert codimension formalized in Lean 4 and checked by an independent Python script)  
**AuthorityEffect:** `None`

---

## 1. Falsification & Boundary Audit

1. **Flat Stabilizer Rényi Spectrum vs. Continuum CFT Rényi Scaling**:
   - In `lean4/CampaignAdsHappyToyNotDualityGap.lean`, `renyiSpectrumDefect_formula`, `renyiSpectrumDefect_pos_of_gt_one`, `cft_ne_stabilizer_renyi_of_gt_one`, and `cftRenyiFactor_strict_anti` show that the flat stabilizer Rényi ratio `stabilizerRenyiFactor n = 1` differs from the 2D CFT single-interval Rényi ratio `cftRenyiFactor n = (1 + 1/n)/2` by `((n - 1)/(2n)) * S_1 > 0` for every $n > 1$ and $S_1 > 0$.

2. **Explicit Ryu-Takayanagi Deficit Witnesses and Length-Resolved Census on the 6-Pentagon HaPPY Patch**:
   - Whereas `FrontierHappyMincut` checked only the aggregate counts `340` and `40` across all 380 contiguous intervals, `CampaignAdsHappyToyNotDualityGap` exhibits the explicit deficit witnesses `(start = 2, len = 8)` (`happy_witness_start2_len8_deficit`) and `(start = 2, len = 12)` (`happy_witness_start2_len12_deficit`) where $S(A) = 4 < 5 = \operatorname{mincut}(A)$, the 5-fold rotational orbit `start = 4*k + 2` (`happy_fivefold_rotational_deficit_orbit`), the absence of deficits at lengths `1..7` and `13..19` (`happy_short_and_long_intervals_exact_mincut`), and the exact per-length deficit distribution `(5, 10, 10, 10, 5)` at lengths `8..12` (`happy_deficit_distribution_by_length`).

3. **Disconnected Mutual Information Jumps & Bulk-to-Boundary Hilbert Codimension**:
   - `happy_disconnected_mutual_information_witnesses`, `code_subspace_strict_codimension`, and `recorded_happy_tiling_hilbert_codimensions` formalize the integer jumps of mutual information on disconnected boundary regions (`0`, `0`, `3`, `1` bits) and the positive orthogonal codimension $2^{N_{\mathrm{bdry}}} - 2^{N_{\mathrm{bulk}}} > 0$ (`30`, `1048512`, `33552384`).

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - In `lean4/CampaignAdsHappyToyNotDualityGap.lean` (`L4D`), the Rényi-$n$ spectrum defect between a flat stabilizer state and the 2D CFT single-interval Rényi factor is $((n-1)/(2n)) S_1 > 0$ for all $n > 1, S_1 > 0$; on the 20-qubit 6-pentagon HaPPY `{5,4}` patch, the 40 contiguous-interval Ryu-Takayanagi deficits (`S(A) = mincut(A) - 1`) occur exclusively at lengths `8..12` with distribution `(5, 10, 10, 10, 5)` and explicit witnesses `(2, 8)` and `(2, 12)`; and for $N_{\mathrm{bulk}} < N_{\mathrm{bdry}}$ the encoded bulk subspace has positive orthogonal codimension $2^{N_{\mathrm{bdry}}} - 2^{N_{\mathrm{bulk}}} > 0$.
   - In `checks/independent/ads-happy-toy-not-duality-gap.py`, 499 exact rational and GF(2) symplectic checks pass with 0 failures, and 6 of 6 semantic Lean mutations are killed in `dag/research/campaign_ads-happy-toy-not-duality-gap_lean_mutation.json`.
2. **What it does not support**:
   - A derivation of continuum AdS/CFT, continuum Ryu-Takayanagi minimal-surface area formulas, or Lorentzian gravitational dynamics from finite stabilizer-code tensor networks.
3. **Narrowest defensible claim**:
   - Finite HaPPY stabilizer-code tensor networks are discrete kinematic models whose flat Rényi spectra ($S_n/S_1 = 1$), length-$8..12$ minimal-cut deficits ($S(A) = \operatorname{mincut}(A) - 1$ on 40 of 380 contiguous intervals of the 6-pentagon patch), and finite Hilbert codimension ($2^{N_{\mathrm{bdry}}} - 2^{N_{\mathrm{bulk}}} > 0$) distinguish them from continuum AdS/CFT and the continuum Ryu-Takayanagi formula.
4. **Next test needed**:
   - Proceed to the next available derivation in `dag/pfp/campaign/derivation_queue.json` (Rank 60: `ADS-RT-FORMULA-IMPORT`, `TFQ-2204`).
