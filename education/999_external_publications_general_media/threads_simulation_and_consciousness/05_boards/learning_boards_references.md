# Learning boards: what each line rests on

Companion to `learning_boards.html` (artifact https://claude.ai/artifact/JaQXLc9z5s13ipw6P7GDzb). The boards are written for readers, so they name no files, proofs or scripts. This file lists, board by board, the check behind each line. Paths are relative to this folder's parent, `threads_simulation_and_consciousness/`.

Tags are the same as on the boards: Witnessed, Derived, Numerical, Cited, Supplied, Open. The repairs made before the first publish are logged in `04_self_audit/self_audit.md`, section G.

## Board 1: sort before you argue

| Line | Backing |
|---|---|
| Two records; identity, fall and sound supplied | `03_critique/claims_ledger.md` §1 and §1a. Lean: `records_do_not_fix_identity` in `lean4/ThreadsReply.lean` (the same pair of records fits two different falls). Self-audit A10, A13, B1. |
| The post's words sorted: render, what is offscreen, our consciousness, the game analogy | `03_critique/claims_ledger.md` §1 (rows render, offscreen, simulation, observer); `03_critique/analysis.md` (six slots). The quoted words are in `01_thread/exchange.md`, post B. |
| Fridge exercise | Teaching example. No check needed beyond everyday experience; it stands in for "add a channel". |

## Board 2: split the word

| Line | Backing |
|---|---|
| Draw, run and keep are separate jobs; Minecraft's far chunks and seed generation | Cited: game behavior. Fact notes at the end of `01_thread/replies.md`. Self-audit A14, A15 (the earlier save-file error). |
| None of the three follows from another | Self-audit A16 and R5 (the withdrawn implication and ranking; the paused, saved chunk counterexample). |
| Each reading either changes some record's chance or changes none | Definition on the back page. Self-audit A18 ("no test proposed" is not "no test exists") and G2. |
| A full catch-up predicts the same records | Derived from the definition; its Bayes consequence is board 4. |

## Board 3: count the channels

| Line | Backing |
|---|---|
| Same report, same verdict | Lean: `same_report_same_verdict`. `03_critique/claims_ledger.md` §1b. |
| (a) does not give (b) | Lean: `one_channel_not_every_channel`. Board repair log, picture 2. |
| (b) to (c) needs a supplied rule | `03_critique/claims_ledger.md` §1b. |
| More states than reports forces a shared report; enough reports forces none | Lean: `pigeonhole` and `small_domain_all_reported`. Self-audit A17 and G5. |
| Which-path records remove the fringes, read or not | Cited: textbook quantum mechanics and many experiments. `03_critique/claims_ledger.md` row C2. |

## Board 4: compare chances, not stories

| Line | Backing |
|---|---|
| 9 in 10 against 5 in 10, factor 1.8 | Lean: `same_report_not_same_likelihood`. Check S4a in `code/self_audit_checks.py`. |
| Two coins against one coin read twice, factor 2 | Lean: `same_marginals_not_same_joint`. Check S4c. Review finding R2 in self-audit §F. |
| Equal chances for every record, nonzero, give factor 1 | Lean: `same_weights_same_likelihood` with `iidLikelihood_pos` (independent sampling). Check S4b. The first reply is C1 in `03_critique/claims_ledger.md`. |
| The post gives no chances | `01_thread/exchange.md`, post B. |

## Board 5: find the sentence

All quotes are from `02_paper/ijms-25-02399.md` (the full text; the PDF is beside it).

| Line | Where |
|---|---|
| 2.5 PB in the cortex, 30 TB for one bit per synapse | Section 3, equations (4) and (5); repeated in Section 5 (Discussion). |
| One simulated configuration | Section 4 and Appendix C, Figures 4 to 6 (N = 4). |
| "render" occurs zero times | `grep -ci render 02_paper/ijms-25-02399.md` prints 0. |
| "Vision is perhaps the most important link ..." | Section 6, Concluding Remarks and Perspectives. Self-audit A19 and A20 (the earlier misreading). |
| "yet another mystery altogether" | Section 5, Discussion. |
| No measurement of its own | `03_critique/analysis.md` (Authority row); `03_critique/claims_ledger.md` §3. |

## Board 6: check it on its own terms

| Line | Backing |
|---|---|
| Capacity 8.32e10 bit/mm², 2.6 PB, 31.25 TB | Derived: checks S3f, S3g and S3h in `code/self_audit_checks.py`. |
| Appendix A: the two conditions freeze the charge and rule out the pulse | Derived: check S2a; check 1 in `code/critique_checks.py`; `03_critique/critique_wdp_po.md` §2.1 and §2.2; self-audit C2. |
| Appendix C: only the M², γ and v terms break Gauss's law | Derived: check 1a in `code/adversarial_review_checks.py`; `03_critique/adversarial_review.md` steps 5 and 6. |
| The printed e/m in (A76) and (A78) | Derived: check 1b in `code/adversarial_review_checks.py`; `03_critique/claims_ledger.md` §4 item 4. |
| Error 1.1 to 2.3 times the charge change; dips within about 10% | Numerical: `code/retest_checks.py`; table and result in `04_self_audit/retest_log.md`. |
| Retention 1.20 eV (τ₀ = 1 ps) and 0.461 eV (τ₀ = 1 s) | Derived: checks S3e and S3e2. τ₀ is supplied. |
| Erasure bound 18.5 meV, photon 2.48 eV, and the bound's conditions | Derived: checks S3b and S3d. Conditions and the kept-copy case: review finding R3 in self-audit §F and entry C5; `03_critique/adversary_of_chatgpt.md`. |
| The hologram is assumed; the object wave has no equation | Witnessed: (A51) in Appendix B ("We shall then consider the case ..."). `03_critique/claims_ledger.md` §3. |
| Open items | `README.md` ("Still open"); `04_self_audit/self_review.md` A6 (input amplitude 2.13 against about 3); self-audit §E. |
| "approaches the target ... due to damping term", no error measure | Witnessed: Section 4, the paragraph on Figure 5. |

## Method page

The six steps are the procedure used in `04_self_audit/self_audit.md`, `04_self_audit/retest_log.md` and `04_self_audit/board_repair_log.md`. The two mistakes named are self-audit A15 (Minecraft) and A19 (the vision quote). The rule that reviewer agreement is not evidence is the second rule in `README.md`.

## Plain reply that carries the link

Post 5 in `01_thread/replies.md` is the plain-logic reply meant to go out with the link to these boards.
