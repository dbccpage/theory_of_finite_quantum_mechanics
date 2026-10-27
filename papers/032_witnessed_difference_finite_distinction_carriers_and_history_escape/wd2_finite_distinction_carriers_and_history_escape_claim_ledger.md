# Claim ledger — Finite Distinction Carriers and History Escape

| ID | Statement | Status | Evidence |
|---|---|---|---|
| WD2-L1 | At horizon n, R_n is the kernel of words of length at most n. | finite instance checked; general Lean proof absent | `word_kernel_agrees` on the sharp chain and the update-stable pair. |
| WD2-T1 | Each R_n is an equivalence, R_{n+1} is finer than R_n, and the first equality is permanent. | proved | Lean `Wd2.related_refl`, `Wd2.related_symm`, `Wd2.related_trans`, `Wd2.related_mono`, `Wd2.related_stable`. Python `refinement_holds` inside `stabilized`. |
| WD2-T2 | A finite machine stabilizes by N ≤ \|S\| − b_0, and the sharp chain meets N = \|S\| − b_0. | finite instance checked; general counting bound withdrawn — non-claim of this package | `sharp_profile`: empty carrier N = 0; one state b_0 = 1 and N = 0; two states b_0 = 2 and N = 0; five states b_0 = 2, N = 3, class counts 2, 3, 4, 5, 5. Lean `Wd2.sharp_m5_bound` is the five-state horizon-3 witness only. |
| WD2-T3 | R_0 is an update congruence if and only if no pair in R_0 has a separating word. | finite instance checked; general Lean proof absent | `no_escape_profile`: two fixed states, N = 0, one class, no separating word. |
| WD2-T4 | A pair in R_n but not R_{n+1} has shortest separating length n + 1. | finite instance checked; general Lean proof absent | `factored_report_profile` on the four-state chain: states 0 and 1 separate at length 2. |
| WD2-T5 | A report that factors through the two endpoint observations preserves R_n. | finite instance checked; general Lean proof absent | `factored_report_profile`: `reports_preserved` is true on the four-state chain through horizon 2. |
| WD2-T6 | R_∞ is the largest output-preserving update congruence, and every compatible quotient is at least as large. | withdrawn — non-claim. The quotient mapping property is outside this package; no finite quotient witness is labeled proved | The manuscript proof remains prose. This package does not call the quotient mapping property proved. |
