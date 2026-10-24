# Independent Derivation Note: `CQFT-REEH-SCHLIEDER-THEOREM-IMPORT` (`TFQ-2106`)

**AuthorityEffect:** None.
**Node:** `CQFT-REEH-SCHLIEDER-THEOREM-IMPORT` (`TFQ-2106`, stage `CAUSAL_QFT`, status `IMPORTED_ASSUMPTION`)
**Outcome Class:** Narrowed (`IMPORTED_ASSUMPTION` status preserved; narrowed to dimension-independent cyclicity-implies-separating commutant duality, the complete 3-qubit and 4-qubit stabilizer subsystem cyclicity census discharging the open finite items of `TFQ-2107`, and the discrete cyclic translation aliasing fence in [CampaignCqftReehSchliederTheoremImport.lean](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean) and [cqft-reeh-schlieder-theorem-import.py](../../../checks/independent/cqft-reeh-schlieder-theorem-import.py)).

---

## 1. Statement & Scope Boundary

`CQFT-REEH-SCHLIEDER-THEOREM-IMPORT` (`TFQ-2106`) records the imported Reeh-Schlieder property (Reeh and Schlieder 1961, *Il Nuovo Cimento* 22, 1051–1068; Haag and Kastler 1964, *J. Math. Phys.* 5, 848–861): in a net of local algebras on Minkowski space with a continuous translation group whose generators satisfy the relativistic spectrum condition ($P^0 \ge 0$) and a translation-invariant vacuum vector $\Omega$, $\Omega$ is cyclic for every local algebra $\mathcal{A}(\mathcal{O})$ and separating for $\mathcal{A}(\mathcal{O})$ whenever $\mathcal{O}'$ has nonempty interior.

The continuum Hilbert lift (`FQ-GAP-CONTINUUM-HILBERT-LIFT`) and continuous-time Stone generator (`FQ-GAP-STONE-CONTINUOUS-TIME`) remain open/conditional in this repository. We narrow `CQFT-REEH-SCHLIEDER-THEOREM-IMPORT` by proving three exact finite/algebraic counterparts and non-equivalence fences in Lean 4 and cross-checking them in Python.

---

## 2. Three Formalized Components and Non-Equivalence Fences

### 2.1 Dimension-Independent Cyclicity-Implies-Separating Duality and Zero-Column Obstruction

1. **General Commutant Duality (`CyclicForA Ω → SeparatingForAc Ω`)**:
   Over any semiring $R$ and for any dimensions $d_A, d_B$ (even when $d_A < d_B$, such as single sites $d_A = 2 < d_B = 4$), if $\mathrm{Fin}\,d_A$ is inhabited by $i_0$ and $\Omega : \mathrm{Fin}\,d_A \to \mathrm{Fin}\,d_B \to R$ is cyclic for $\mathrm{End}(H_A)$ acting on the left (`CyclicForA Ω`), then $\Omega$ is separating for $\mathrm{End}(H_{A^c})$ acting on the right (`SeparatingForAc Ω`) via matrix associativity $(X \Omega) Y = X (\Omega Y)$ ([`cyclic_implies_separating`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L61-L75)).
2. **Non-Cyclicity from a Right-Kernel Vector or Zero Column (Even When $d_A < d_B$)**:
   Combining `cyclic_implies_separating` with `not_separating_of_right_kernel` yields `not_cyclic_of_right_kernel` for arbitrary $d_A > 0, d_B$ ([`not_cyclic_of_right_kernel`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L79-L85)), and shows that any identically zero column $k_0 \in \mathrm{Fin}\,d_B$ of $\Omega$ precludes both a left inverse (`¬ HasFullComplementaryRank Ω`) and cyclicity (`¬ CyclicForA Ω`) ([`no_left_inverse_of_zero_column`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L90-L98), [`not_cyclic_of_zero_column`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L103-L116)).

### 2.2 Complete 3-Qubit and 4-Qubit Stabilizer Subsystem Cyclicity Census (`TFQ-2107` Closure)

Discharging the open finite-dimensional obligations noted in `TFQ-2107` (`CQFT-RS-FINITE-CYCLICITY-TARGET`):
- **Single sites ($|A| = 1$, $2 \times 4$ unfolding)**: None of $|000\rangle$, $|\mathrm{GHZ}_3\rangle$, or $|W_3\rangle$ is cyclic for any single site $s \in \{0, 1, 2\}$ ([`single_site_not_cyclic_all_three_states`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L127-L143)).
- **Pairs of sites ($|A| = 2$, $4 \times 2$ unfolding)**: $|000\rangle$ has neither a left inverse nor cyclicity on any pair of sites ([`prod3_pair_not_cyclic_and_no_left_inverse`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L148-L157)), whereas both $|\mathrm{GHZ}_3\rangle$ and $|W_3\rangle$ have `HasFullComplementaryRank`, `CyclicForA`, and `SeparatingForAc` on every pair of sites ([`ghz3_and_w3_pair_cyclic_and_separating`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L161-L184)).
- **Full 3-site algebra ($|A| = 3$, $8 \times 1$ unfolding)**: All three states $|000\rangle$, $|\mathrm{GHZ}_3\rangle$, and $|W_3\rangle$ have full complementary rank $1$ and are cyclic ([`full_three_site_cyclic_all_three_states`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L193-L209)).
- **4-qubit half-system bipartition ($|A| = |A^c| = 2$, $4 \times 4$ unfolding)**: Neither $|0000\rangle$ (rank 1) nor $|\mathrm{GHZ}_4\rangle$ (rank 2) is cyclic, whereas the 2-Bell-pair cluster state $(|00\rangle + |11\rangle)_{02} \otimes (|00\rangle + |11\rangle)_{13}$ has unfolding `matId 4`, hence has full complementary rank $4$ and is both cyclic and separating ([`four_qubit_half_system_cyclicity_dichotomy`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L226-L242)).

### 2.3 Discrete Cyclic Translation Group Aliasing vs. Continuum Stone / Tube-Analyticity Fence

- On a finite $N$-site ring, `cyclicShift N` aliases with period $N$ (`cyclicShift N N x = x` and `cyclicShift N (k + N) x = cyclicShift N k x`, [`cyclicShift_periodic_aliasing`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L264-L274)), and every translation-invariant constant vector `constVec N c` has identically zero discrete momentum difference ([`translation_invariant_zero_momentum_diff`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L280-L283)).
- On $N = 3$ qubits, the translation-invariant product vacuum $|000\rangle$ has identical single-site unfoldings across $s \in \{0, 1, 2\}$ yet fails cyclicity on every single site and on every pair of sites ([`translation_invariant_product_vacuum_not_cyclic_for_proper_subsystems`](../../../lean4/CampaignCqftReehSchliederTheoremImport.lean#L291-L302)).
