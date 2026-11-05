# Holographic brain paper: teardown and rebuild

This folder holds the complete work on one paper and one public thread.

- **The paper:** Nishiyama, Tanaka, Tuszynski and Tsenkova, "Holographic Brain Theory: Super-Radiance, Memory Capacity and Control Theory", *Int. J. Mol. Sci.* 25(4):2399 (2024), doi:10.3390/ijms25042399.
- **The thread:** a Threads post that cited the paper for "the universe does not render what is offscreen".

Two rules run through every file:
- **Replies stay finite; the paper gets the continuum.** Replies to people use finite pictures and counting. The paper is checked with its own continuum equations.
- **Agreement is not evidence.** Several language models reviewed this work, and their agreement counts for nothing. A claim stands only on something checkable: a quote from the paper, a computation in `code/`, a Lean proof in `lean4/`, or a rerun of the paper's simulation. Each claim is tagged **Witnessed** (quoted record), **Derived** (exact check), **Numerical** (floating-point rerun), **Supplied** (an assumption someone put in) or **Open**.

## Reading order

1. `01_thread/exchange.md`: what was said in the thread.
2. `02_paper/ijms-25-02399.md`: the paper. All 91 equations are re-typeset; the original PDF sits next to it.
3. `03_critique/analysis.md`, then `03_critique/claims_ledger.md`: what the post and the paper each supply, derive and witness.
4. `03_critique/adversarial_review.md` and `03_critique/critique_wdp_po.md`: the mathematical teardown.
5. `03_critique/assumptions_ledger.md`, then `03_critique/assumptions_mutation_audit.md`: 78 assumptions, each checked against the paper, mutated, and the paper's claim tried for recovery.
6. `03_critique/math_exam_review.md`: an outside 10-page mathematical examination, checked line by line.
7. `04_self_audit/self_review.md` and `04_self_audit/self_audit.md`: our own work, broken and repaired.
8. `01_thread/replies.md`: the posts that survived all of the above.
9. `05_boards/learning_boards.html`: six plain-logic boards for any reader, one reasoning move each. `05_boards/learning_boards_references.md` lists the check behind every line.

## Layout

| Folder | File | What it is | Kind |
|---|---|---|---|
| `01_thread/` | `exchange.md` | The three-party exchange, with roles A, B and C | record |
| | `replies.md` | Five terse plain posts in one sequence, each at most 500 characters (S5), with no in-house terms (S8); the fifth carries the link to the reconstruction | **live** |
| `02_paper/` | `ijms-25-02399.pdf` | The published paper | source |
| | `ijms-25-02399.md` | The full text with every equation in LaTeX, plus our typo notes | source |
| `03_critique/` | `analysis.md` | Six slots (carrier, gauge, reference, comparison, authority, observer) for the post and for the paper | live |
| | `claims_ledger.md` | Every claim tagged witnessed, derived, supplied, cited or open | **live** |
| | `adversarial_review.md` | Round 1: ChatGPT's review broken and recovered (Gauss's law in Appendix C, Landauer, capacity) | record |
| | `adversary_of_chatgpt.md` | Two ChatGPT arguments broken and recovered, round 2 retest, and a round 3 pointer | record |
| | `critique_wdp_po.md` | Audit with the Witnessed Difference Programme and Projection Obstruction | **live** |
| | `assumptions_ledger.md` | A 78-row assumption ledger forwarded from another reviewer, kept verbatim (say-so) | record |
| | `holographic_brain_math_exam.pdf` | A 10-page mathematical examination from another reviewer, kept as received (say-so) | record |
| | `math_exam_review.md` | That examination checked section by section: agrees / adds / differs, with each new point re-derived | **live** |
| | `assumptions_mutation_audit.md` | Every ledger row checked against the paper, mutated, and the claim tried for recovery: 29 unchanged, 24 recover with a price, 25 do not recover; the classical-comparator test | **live** |
| `04_self_audit/` | `self_review.md` | The math critique, attacked and repaired | live |
| | `self_audit.md` | Replies, boards, Lean and ledger, attacked and repaired. 90 entries, including Jeremy's review (§F), the learning boards (§G) and the terse replies (§H) | **live** |
| | `retest_log.md` | Four regression cases: claim, counterexample, repair, retest, residual obligation | record |
| | `board_repair_log.md` | The board repairs after the card-by-card review | record |
| `05_boards/` | `markup_board.html` | The reply board: three pictures (tree, rendering claim, paper chain), supporting cards, final posts | live |
| | `audit_board.html` | The paper-audit board: 16 cards | live |
| | `learning_boards.html` | Six boards for readers, in plain logic: sort, split, channels, chances, source, math, plus the method. Artifact https://claude.ai/artifact/JaQXLc9z5s13ipw6P7GDzb | **live** |
| | `learning_boards_references.md` | What each board line rests on: quotes, checks and proofs (the boards themselves name none) | **live** |
| `06_reference/` | `sources.md` | Where the observer definitions live in this repository | reference |
| | `observer_article_2026-05-23.md` | Excerpts from "What the Hell Is an Observer?" (2026-05-23) | reference |
| `code/` | `self_audit_checks.py` | S1–S8: Appendix A algebra, the gauge identity, every number, Bayes cases, reply lengths and wording, the boards' attempt time and quoted numbers. Exits 1 on any failure | check |
| | `test_self_audit_checks.py` | Regression tests for that checker | check |
| | `adversarial_review_checks.py` | Gauss's law in Appendix C, the e/m misprint, Landauer numbers, capacity | check |
| | `critique_checks.py` | Eleven checks behind `critique_wdp_po.md`; the last full run is in `critique_checks_output.txt` | check |
| | `math_exam_checks.py` | The re-derivations behind `math_exam_review.md`: the (A70) plane wave, the real-coherence sector, 4 meV sensitivity, corner differences | check |
| | `retest_checks.py` | A rerun of the paper's Appendix C simulation, measuring the Gauss residual | check |
| `lean4/` | `ThreadsReply.lean` | The finite results behind the replies (core Lean 4.35, no Mathlib) | proof |

**Live** files are kept current. **Record** files are left as written so the trail stays readable. Their later repairs are logged in `04_self_audit/`.

## Where the paper stands

Each line names the file that carries it.

- **Appendix C breaks Gauss's law.** The added $M^2$, $\gamma$ and $v$ terms are exactly what breaks it (Derived, `adversarial_review_checks.py`). Along the paper's own run, the violation is 1.1 to 2.3 times the charge change (Numerical, `retest_checks.py`).
- **Appendix A contradicts itself.** Its gauge, $A^0=0$ with $\nabla\cdot\mathbf A=0$, together with its own (A7), freezes the charge density. That removes the radiating term in the two-level model (Derived, S2a and `critique_checks.py` check 1).
- **No energy barrier is given for retention.** A record held by one barrier needs $\Delta E = k_BT\ln(1\,\text{yr}/\tau_0)$. With a supplied $\tau_0 = 1$ ps that is 1.2 eV; with 1 s it is 0.46 eV (Derived, S3e). A collective record could have a larger barrier (Open).
- **The hologram is assumed.** (A51) supposes $\lvert\varphi\rvert^2\propto\lvert r+o\rvert^2$, and the object wave $o$ has no equation (Witnessed).
- **The capacity arithmetic holds.** Unrounded it gives 2.6 PB; the paper says 2.5 PB (Derived, S3f–g).
- **The petabyte is the thickness.** A surface hologram over the same area holds 0.5 TB; the factor $n_r d/\lambda = 5200$ makes it 2.6 PB (Derived, `assumptions_mutation_audit.md` Y1).
- **The gauge pair can be repaired at a price.** Letting $A^0$ obey Poisson's equation restores the coherence and adds a Coulomb term the paper would have to bound (Derived, row D1).
- **The paper makes no rendering claim.** The word "render" occurs zero times. The paper calls how a quantum mind perceives the macro-world "yet another mystery altogether" (Witnessed).

Still open:
- the paper's input amplitude (about 3 in the paper, 2.13 in our recursion);
- the size of the near-field term dropped in Appendix A;
- the value of the mass scale $m$;
- a comparison with the authors' own code.

## Running the checks

Run these from this folder:

```
python code/self_audit_checks.py            # S1–S8; exit 0 only if all pass (needs sympy)
python code/test_self_audit_checks.py       # regression tests for the checker
python -I code/adversarial_review_checks.py # needs sympy
python -I code/critique_checks.py           # needs sympy and numpy; exit 0 only if all pass
python -I code/math_exam_checks.py          # needs sympy and numpy; exit 0 only if all pass
python code/retest_checks.py                # needs numpy; about 30 minutes
lean lean4/ThreadsReply.lean                # Lean 4.35, core only
```
