Status: AI-drafted, awaiting human review.

# Pre-Commit Overclaim & Falsification Review: `CQFT-REEH-SCHLIEDER-THEOREM-IMPORT` (`TFQ-2106`)

**Date:** 2026-10-24  
**Campaign Node:** `CQFT-REEH-SCHLIEDER-THEOREM-IMPORT` (`TFQ-2106`, stage `CAUSAL_QFT`)  
**Outcome:** `Narrowed` (`IMPORTED_ASSUMPTION` status preserved; narrowed to dimension-independent cyclicity-implies-separating commutant duality, the complete 3-qubit and 4-qubit stabilizer subsystem cyclicity census, and the discrete cyclic translation aliasing fence in Lean 4 and an independent Python verifier)  
**AuthorityEffect:** `None`

---

## 1. Falsification & Boundary Audit

1. **Dimension-Independent Cyclicity-Implies-Separating Duality and Zero-Column Obstruction**:
   - In `lean4/CampaignCqftReehSchliederTheoremImport.lean`, `cyclic_implies_separating`, `not_cyclic_of_right_kernel`, `no_left_inverse_of_zero_column`, and `not_cyclic_of_zero_column` establish over any semiring `R` and any dimensions `dA, dB` (including `dA < dB`) that `CyclicForA Ω` implies `SeparatingForAc Ω` via `(X Ω) Y = X (Ω Y)`, so any nonzero right-kernel vector or identically zero column precludes cyclicity even when `dA < dB`.

2. **Complete 3-Qubit and 4-Qubit Stabilizer Subsystem Cyclicity Census (`TFQ-2107` Closure)**:
   - Discharging the open finite items recorded in `TFQ-2107`, `single_site_not_cyclic_all_three_states`, `prod3_pair_not_cyclic_and_no_left_inverse`, `ghz3_and_w3_pair_cyclic_and_separating`, `full_three_site_cyclic_all_three_states`, and `four_qubit_half_system_cyclicity_dichotomy` prove `¬ CyclicForA` for `|000⟩, |GHZ_3⟩, |W_3⟩` on all single sites, `¬ HasFullComplementaryRank ∧ ¬ CyclicForA` for `|000⟩` on all pairs of sites, `CyclicForA` for all three states on the full 3-site algebra, and the half-system cyclicity dichotomy between `|0000⟩, |GHZ_4⟩` (`¬ CyclicForA`) and the 4-qubit 2-Bell-pair cluster state (`CyclicForA ∧ SeparatingForAc`).

3. **Discrete Cyclic Translation Group Aliasing vs. Continuum Stone / Tube-Analyticity Fence**:
   - `cyclicShift_periodic_aliasing`, `translation_invariant_zero_momentum_diff`, and `translation_invariant_product_vacuum_not_cyclic_for_proper_subsystems` show that on a finite `N`-site ring, cyclic translations alias with period `N`, translation-invariant constant vectors have zero discrete momentum difference, and the translation-invariant 3-qubit product vacuum `|000⟩` fails cyclicity on every proper subsystem (`|A| ∈ {1, 2}`).

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - In `lean4/CampaignCqftReehSchliederTheoremImport.lean` (`L4D`), the 12 theorems formalize the dimension-independent `CyclicForA → SeparatingForAc` implication, the complete 3-qubit and 4-qubit subsystem cyclicity and non-cyclicity census, and the discrete cyclic translation aliasing fence.
   - In `checks/independent/cqft-reeh-schlieder-theorem-import.py`, 252 algebraic checks pass with 0 failures after removal of repeated modular identities, and 6 of 6 semantic Lean mutations are killed in `dag/research/campaign_cqft-reeh-schlieder-theorem-import_lean_mutation.json`.
2. **What it does not support**:
   - The continuum Reeh-Schlieder theorem, the continuous-time Stone theorem (`FQ-GAP-STONE-CONTINUOUS-TIME`), or the continuum Hilbert space lift (`FQ-GAP-CONTINUUM-HILBERT-LIFT`), which remain imported/conditional.
3. **Narrowest defensible claim**:
   - On the declared bipartite matrix carriers (`FrontierRsCyclicity.lean`), `CyclicForA Ω` implies `SeparatingForAc Ω` for all `dA > 0, dB`, `|000⟩, |GHZ_3⟩, |W_3⟩` are not cyclic on any single site, `|000⟩` is not cyclic on any pair of sites while all three states are cyclic on the full 3-site algebra, the 4-qubit 2-Bell-pair state is cyclic and separating across the `2 + 2` half-system split while `|0000⟩` and `|GHZ_4⟩` are not, and finite `N`-periodic translation invariance of `|000⟩` does not induce proper-subsystem cyclicity.
4. **Next test needed**:
   - Proceed to the next available continuum derivation in `dag/pfp/campaign/derivation_queue.json` (Rank 89: `TFQ-0106`, stage `FINITE_QG`).
