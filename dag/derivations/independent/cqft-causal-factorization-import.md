# Independent Derivation Note: `CQFT-CAUSAL-FACTORIZATION-IMPORT` (`TFQ-2109`)

**AuthorityEffect:** None.
**Node:** `CQFT-CAUSAL-FACTORIZATION-IMPORT` (`TFQ-2109`, stage `CAUSAL_QFT`, status `IMPORTED_ASSUMPTION`)
**Outcome Class:** Narrowed (`IMPORTED_ASSUMPTION` status preserved; narrowed to the exact Bogoliubov relative S-matrix cocycle and shift-invariance equivalence, full adjacent-spacelike-swap connectivity and ordered-product equality across all 5 linear extensions of `posetN`, and the coincident-diagonal counterterm ambiguity fence in [CampaignCqftCausalFactorizationImport.lean](../../../lean4/CampaignCqftCausalFactorizationImport.lean) and [cqft-causal-factorization-import.py](../../../checks/independent/cqft-causal-factorization-import.py)).

---

## 1. Statement & Scope Boundary

`CQFT-CAUSAL-FACTORIZATION-IMPORT` (`TFQ-2109`) records the imported Epstein-Glaser (1973, Section 1.1 pp. 214–215, Section 2.1 eq. (9) p. 218, Section 2.2 eq. (30) p. 223) and Brunetti-Fredenhagen (2000, `arXiv:math-ph/9903028`, Section 1 eq. (2) p. 4, Section 3 Condition P3 p. 15) causal factorization property of the scattering matrix:
$$V(g, h_1 + h_2) = S(g)^{-1} S(g + h_1 + h_2) = V(g, h_1)\,V(g, h_2)$$
whenever $\mathrm{supp}\,h_1 \cap (\mathrm{supp}\,h_2 + V^-) = \emptyset$, and at each perturbative order $n$, $T(P \cup Q) = T(P)\,T(Q)$ whenever $\{x_i : i \in P\} \cap (\{x_j : j \in Q\} + V^-) = \emptyset$, with renormalization reducing to extending time-ordered operator-valued distributions across the total diagonal $\Delta_n$.

Continuum operator-valued distributions and the Minkowski causal cone remain imported assumptions. We narrow `CQFT-CAUSAL-FACTORIZATION-IMPORT` by proving three exact finite/algebraic counterparts and non-equivalence fences in Lean 4 and cross-checking them in Python.

---

## 2. Three Formalized Components and Non-Equivalence Fences

### 2.1 Abstract Bogoliubov Relative S-Matrix Algebra and Causal Separation Asymmetry

1. **Identity and Unconditional Telescoping Cocycle Law**:
   Over any group $G$ and additive coupling carrier $A$, the relative Bogoliubov operator $\mathrm{bogoliubovV}(S, g, h) := S(g)^{-1} S(g + h)$ satisfies
   $$\mathrm{bogoliubovV}(S, g, 0) = 1, \qquad \mathrm{bogoliubovV}(S, g, h_1)\,\mathrm{bogoliubovV}(S, g + h_1, h_2) = \mathrm{bogoliubovV}(S, g, h_1 + h_2)$$
   without any causal restriction ([`bogoliubovV_zero`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L59-L62), [`bogoliubovV_cocycle_telescoping`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L66-L70)).
2. **Equivalence Between Causal Factorization and Background-Shift Invariance**:
   By left-cancellation in $G$ applied to the telescoping cocycle identity, Bogoliubov causal factorization holds if and only if adding $h_1$ outside the causal past of $h_2$ leaves the relative S-matrix for $h_2$ invariant:
   $$\mathrm{bogoliubovV}(S, g, h_1 + h_2) = \mathrm{bogoliubovV}(S, g, h_1)\,\mathrm{bogoliubovV}(S, g, h_2) \iff \mathrm{bogoliubovV}(S, g + h_1, h_2) = \mathrm{bogoliubovV}(S, g, h_2)$$
   ([`bogoliubovV_factorization_iff_background_shift_invariance`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L75-L84)), and at $g = 0$ ($S(0) = 1$) reduces to $S(h_1 + h_2) = S(h_1)\,S(h_2)$ ([`bogoliubovV_causal_factorization_at_zero_iff`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L88-L93)).
3. **Asymmetry of Epstein-Glaser Causal Separation vs. Symmetric Spacelike Separation**:
   On the 4-element diamond poset `C2` (`0 < 1, 0 < 2, 1 < 3, 2 < 3`), the finite Epstein-Glaser predicate `noInCausalPast C2 L₁ L₂` ($\forall x \in L_1, \forall y \in L_2, \neg(x < y)$) holds symmetrically on the spacelike pair `([d1], [d2])`, holds one-way on the future-before-past partition `([d1, d2, d3], [d0])` (where `allSpacelikeBetween` is `false`), and fails on the reversed partition `([d0], [d1, d2, d3])` ([`c2_epstein_glaser_separation_asymmetry`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L112-L119)).

### 2.2 Complete Adjacent-Spacelike-Swap Connectivity and Product Equality on `posetN`

Discharging the open finite-poset question recorded in `TFQ-2110` (`CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET`):
- All three unordered spacelike pairs `{n0, n1}`, `{n2, n3}`, and `{n0, n3}` of `posetN` (`0 < 2`, `1 < 2`, `1 < 3`) satisfy `isSpacelike posetN` ([`posetN_all_spacelike_pairs`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L133-L140)), and filtering all `24` permutations of `Fin 4` yields the exact 5-element list `[extN0, extN1, extN2, extN3, extN4]` ([`posetN_exact_five_linear_extensions`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L144-L146)).
- All 5 linear extensions of `posetN` are connected to `extN0 = [n0, n1, n2, n3]` via `SpacelikeSwapChain posetN` ([`posetN_all_five_extensions_swap_connected`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L151-L170)), so for any monoid $M$ and spacelike-commuting assignment $A : \mathrm{Fin}\,4 \to M$, all 5 linear extensions have identical ordered products ([`posetN_all_five_ordered_products_eq`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L175-L187)), whereas anticommuting Pauli matrices $X, Z$ on `(n0, n3)` flip the sign between `extN3` and `extN4` ([`posetN_pauli_commuting_vs_anticommuting_witness`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L207-L212)).

### 2.3 Coincident-Diagonal Renormalization Ambiguity Fence (`Δ_n` Distribution Extension)

- By `spacelike_irrefl`, no coincident pair `(x, x)` on the diagonal of a `FiniteStrictPoset n` is spacelike separated, and in 4D the Epstein-Glaser polynomial counterterm dimension $\binom{\omega + 4}{4}$ at singular orders $\omega = 0, 1, 2, 3, 4$ equals $1, 5, 15, 35, 70$ ([`coincident_diagonal_not_spacelike_and_counterterm_dim`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L232-L239)).
- On a two-point kernel `twoPointKernelWithCounterterm T1 c x y`, off-diagonal factorization ($x \neq y$) is independent of the contact counterterm $c \in \mathbb{Z}$, while the coincident diagonal ($x = y$) shifts by $c_1 - c_2$ ([`diagonal_counterterm_preserves_off_diagonal_factorization`](../../../lean4/CampaignCqftCausalFactorizationImport.lean#L244-L254)).
