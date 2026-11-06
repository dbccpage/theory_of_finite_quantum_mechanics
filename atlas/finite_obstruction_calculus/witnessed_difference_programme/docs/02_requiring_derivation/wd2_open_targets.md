# WD2 Finite Distinction Carriers — General Lean 4 Formalization Targets (Discharged)

**AuthorityEffect:** None  
**Source Package:** `witnessed_difference_finite_distinction_carriers_and_history_escape` (absorbed into `witnessed_difference_programme`)  
**Status:** `PROVED_LEAN` (`TFQ-0559`, `TFQ-0561` through `TFQ-0565`)

## Context
The absorbed manuscript `docs/01_substantiated/wd2_finite_distinction_carriers.md` and claim ledger `docs/01_substantiated/wd2_claim_ledger.md` establish seven results (`WD2-L1` and `WD2-T1` through `WD2-T6`) for finite Moore machines $(S, \Sigma, Y, u, p)$ and horizon distinguishability relations $R_n$.

All seven results (`WD2-L1` and `WD2-T1` through `WD2-T6`) now have complete, sorry-free Lean 4 proofs in `lean4/WitnessedDifference/FiniteDistinction.lean` (audited in `lean4/WitnessedDifference/FiniteDistinctionAxiomReport.lean`) alongside executable Python checks in `code/witnessed_difference/finite_distinction.py`.

---

## Discharged General Lean 4 Targets

### 1. `WD2-DERIV-01`: Word Kernel Representation (`WD2-L1`, `TFQ-0559`)
- **Statement:** Prove in Lean 4 that for every $n \ge 0$ and $s, t \in S$, $(s, t) \in R_n$ if and only if $p(u_w(s)) = p(u_w(t))$ for every word $w \in \Sigma^*$ of length $|w| \le n$.
- **Lean 4 Discharge:** `FiniteDistinction.lean::Wd2.word_kernel_agreement` and `FiniteDistinction.lean::Wd2.poly_word_kernel_agreement`.

### 2. `WD2-DERIV-02`: General Pigeonhole Stabilization Bound (`WD2-T2`, `TFQ-0561`)
- **Statement:** Prove in Lean 4 that on a finite carrier $S$, if $b_n = |S / R_n|$ is the block count of $R_n$, then $b_n$ is strictly increasing up to stabilization horizon $N \le |S| - b_0 \le |S| - 1$, and construct the general $m$-state delay chain achieving $N = m - 2$ for arbitrary $m \ge 2$.
- **Lean 4 Discharge:** `FiniteDistinction.lean::Wd2.stabilization_horizon_le_card_sub_b0` and `FiniteDistinction.lean::Wd2.sharp_chain_general_witness` (plus 5-state specialization `Wd2.sharp_m5_bound`).

### 3. `WD2-DERIV-03`: No-Escape Characterization (`WD2-T3`, `TFQ-0562`)
- **Statement:** Prove in Lean 4 the four-way equivalence:
  1. $R_0$ is an update congruence on $S$ under all $a \in \Sigma$;
  2. $R_1 = R_0$;
  3. $R_n = R_0$ for all $n \ge 0$;
  4. There exists a deterministic quotient update $\bar{u}_a : Y_0 \to Y_0$ on $Y_0 = p(S)$ such that $p \circ u_a = \bar{u}_a \circ p$.
- **Lean 4 Discharge:** `FiniteDistinction.lean::Wd2.no_escape_equivalence` and `FiniteDistinction.lean::Wd2.isUpdateCongruence_iff_r1_eq_r0`.

### 4. `WD2-DERIV-04`: Shortest Separating Word Length (`WD2-T4`, `TFQ-0563`)
- **Statement:** Prove in Lean 4 that if $(s, t) \in R_n \setminus R_{n+1}$, then there exists a separating word $w \in \Sigma^{n+1}$ of length $n+1$ with $p(u_w(s)) \ne p(u_w(t))$, and no word of length $\le n$ separates $s$ and $t$.
- **Lean 4 Discharge:** `FiniteDistinction.lean::Wd2.shortest_separating_word`.

### 5. `WD2-DERIV-05`: Factored Report Preservation (`WD2-T5`, `TFQ-0564`)
- **Statement:** Prove in Lean 4 that if a secondary report $g : S \to Z$ factors as $g = \bar{g} \circ p$, then adjoining $g$ to the immediate report leaves every horizon relation $R_n$ unchanged; conversely, if $g$ separates a pair in $R_0$, the adjoined horizon-0 relation strictly refines $R_0$.
- **Lean 4 Discharge:** `FiniteDistinction.lean::Wd2.factored_report_preserves_related`, `FiniteDistinction.lean::Wd2.factored_report_preserves_polyRelated`, and `FiniteDistinction.lean::Wd2.unfactored_report_splits_r0`.

### 6. `WD2-DERIV-06`: Minimal Deterministic Quotient Universal Property (`WD2-T6`, `TFQ-0565`)
- **Statement:** Prove in Lean 4 that $S / R_\infty$ is the coarsest quotient of $S$ through which $p$ factors and on which each $u_a$ descends to a deterministic map, and that any other such quotient $(Q, \pi, \tilde{u}, \tilde{p})$ admits a unique surjective homomorphism $Q \to S / R_\infty$ commuting with $\pi$, updates, and reports.
- **Lean 4 Discharge:** `FiniteDistinction.lean::Wd2.rInfinity_coarsest_congruence` and `FiniteDistinction.lean::Wd2.minimal_deterministic_quotient_factorization`.
