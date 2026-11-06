# Claim ledger — Finite Distinction Carriers and History Escape

| ID | Statement | Status | Evidence |
|---|---|---|---|
| WD2-L1 | At horizon n, R_n is the kernel of words of length at most n. | proved | Lean `Wd2.word_kernel_agreement`, `Wd2.poly_word_kernel_agreement`. Python `word_kernel_agrees` on the sharp chain and the update-stable pair. |
| WD2-T1 | Each R_n is an equivalence, R_{n+1} is finer than R_n, and the first equality is permanent. | proved | Lean `Wd2.related_refl`, `Wd2.related_symm`, `Wd2.related_trans`, `Wd2.related_mono`, `Wd2.related_stable`. Python `refinement_holds` inside `stabilized`. |
| WD2-T2 | A finite machine stabilizes by N ≤ \|S\| − b_0, and the sharp chain meets N = \|S\| − b_0. | proved | Lean `Wd2.stabilization_horizon_le_card_sub_b0`, `Wd2.sharp_chain_general_witness`, `Wd2.sharp_m5_bound`. Python `sharp_profile`. |
| WD2-T3 | R_0 is an update congruence if and only if no pair in R_0 has a separating word. | proved | Lean `Wd2.no_escape_equivalence`, `Wd2.isUpdateCongruence_iff_r1_eq_r0`. Python `no_escape_profile`. |
| WD2-T4 | A pair in R_n but not R_{n+1} has shortest separating length n + 1. | proved | Lean `Wd2.shortest_separating_word`. Python `shortest_separating_length` and `factored_report_profile`. |
| WD2-T5 | A report that factors through the two endpoint observations preserves R_n. | proved | Lean `Wd2.factored_report_preserves_related`, `Wd2.factored_report_preserves_polyRelated`, `Wd2.unfactored_report_splits_r0`. Python `factored_report_profile`. |
| WD2-T6 | R_∞ is the largest output-preserving update congruence, and every compatible quotient is at least as large. | withdrawn — non-claim. The quotient mapping property is outside this package; no finite quotient witness is labeled proved | The manuscript proof remains prose. This package does not call the quotient mapping property proved. |

