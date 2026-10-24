Status: AI-drafted, awaiting human review.

# Pre-Commit Overclaim & Falsification Review: `CQFT-CAUSAL-FACTORIZATION-IMPORT` (`TFQ-2109`)

**Date:** 2026-10-24  
**Campaign Node:** `CQFT-CAUSAL-FACTORIZATION-IMPORT` (`TFQ-2109`, stage `CAUSAL_QFT`)  
**Outcome:** `Narrowed` (`IMPORTED_ASSUMPTION` status preserved; narrowed to the Bogoliubov relative S-matrix cocycle and shift-invariance equivalence, full adjacent-spacelike-swap connectivity and ordered-product equality across all 5 linear extensions of `posetN`, and the coincident-diagonal counterterm ambiguity fence in Lean 4 and an independent Python verifier)  
**AuthorityEffect:** `None`

---

## 1. Falsification & Boundary Audit

1. **Abstract Bogoliubov Relative S-Matrix Algebra (`V(g, h) = S(g)⁻¹ S(g + h)`) and Causal Asymmetry**:
   - In `lean4/CampaignCqftCausalFactorizationImport.lean`, `bogoliubovV_zero`, `bogoliubovV_cocycle_telescoping`, `bogoliubovV_factorization_iff_background_shift_invariance`, `bogoliubovV_causal_factorization_at_zero_iff`, and `c2_epstein_glaser_separation_asymmetry` formalize the group-theoretic Bogoliubov cocycle identity `V(g, h1) V(g + h1, h2) = V(g, h1 + h2)`, the exact equivalence between causal factorization `V(g, h1 + h2) = V(g, h1) V(g, h2)` and background-shift invariance `V(g + h1, h2) = V(g, h2)`, and the strict inclusion of symmetric spacelike separation inside the asymmetric Epstein-Glaser condition `noInCausalPast C2` on the 4-element diamond poset `C2`.

2. **Complete Adjacent-Spacelike-Swap Connectivity and Ordered-Product Equality on `posetN`**:
   - Discharging the finite-poset connectivity question left open in `TFQ-2110`, `posetN_all_spacelike_pairs`, `posetN_exact_five_linear_extensions`, `posetN_all_five_extensions_swap_connected`, `posetN_all_five_ordered_products_eq`, and `posetN_pauli_commuting_vs_anticommuting_witness` show that all 5 linear extensions `extN0..extN4` of the 4-element `N` poset are connected by chains of adjacent spacelike swaps and have identical ordered products for any spacelike-commuting monoid assignment, while anticommuting Pauli operators `X, Z` on `(n0, n3)` flip the sign between `extN3` and `extN4`.

3. **Coincident-Diagonal Renormalization Ambiguity Fence (`Δ_n` Distribution Extension)**:
   - `coincident_diagonal_not_spacelike_and_counterterm_dim` and `diagonal_counterterm_preserves_off_diagonal_factorization` show that coincident points `(x, x)` on a `FiniteStrictPoset` are never spacelike separated, evaluate the 4D Epstein-Glaser counterterm dimension `binom(omega + 4, 4)` at `omega = 0..4` (`1, 5, 15, 35, 70`), and demonstrate that off-diagonal factorization (`x ≠ y`) is invariant under arbitrary diagonal contact counterterms `c : Int` while the diagonal `x = y` shifts by `c1 - c2`.

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - In `lean4/CampaignCqftCausalFactorizationImport.lean` (`L4D`), the 12 theorems formalize the Bogoliubov relative S-matrix cocycle and shift-invariance equivalence, the complete swap-connectivity and product equality of the 5 linear extensions of `posetN`, and the coincident-diagonal counterterm ambiguity fence.
   - In `checks/independent/cqft-causal-factorization-import.py`, 795 exact algebraic and combinatorial checks pass with 0 failures, and 6 of 6 semantic Lean mutations are killed in `dag/research/campaign_cqft-causal-factorization-import_lean_mutation.json`.
2. **What it does not support**:
   - Continuum operator-valued distributions, a continuum Minkowski causal cone, or the Epstein-Glaser distribution extension across the continuum total diagonal $\Delta_n$, which remain `IMPORTED_ASSUMPTION`.
3. **Narrowest defensible claim**:
   - On the declared group, monoid, and `FiniteStrictPoset` carriers (`CausalOrder.lean`, `FrontierPosetNet.lean`, `FrontierLinearExtension.lean`), Bogoliubov causal factorization `V(g, h1 + h2) = V(g, h1) V(g, h2)` is equivalent to background-shift invariance `V(g + h1, h2) = V(g, h2)`, all 5 linear extensions of `posetN` are connected by adjacent spacelike swaps and yield equal ordered products for spacelike-commuting operators, and off-diagonal factorization (`x ≠ y`) leaves coincident-diagonal contact counterterms `c` unconstrained.
4. **Next test needed**:
   - Proceed to the next available continuum derivation in `dag/pfp/campaign/derivation_queue.json` (Rank 71: `CQFT-REEH-SCHLIEDER-THEOREM-IMPORT`, `TFQ-2106`).
