# The holographic brain paper and the rendering post

This folder covers one paper and one public post.

- **The paper.** Nishiyama, Tanaka, Tuszynski and Tsenkova, "Holographic Brain Theory: Super-Radiance, Memory Capacity and Control Theory", *Int. J. Mol. Sci.* 25(4):2399 (2024), doi:10.3390/ijms25042399.
- **The post.** A Threads post that cited the paper for "the universe does not render what is offscreen".

## The files, in reading order

| File | What it is |
|---|---|
| `1_README.md` | This page. |
| `2_dag.json` | The plan as a graph. It has four parts. **Goals** say what we want to finish. **Claims** say what we think is true, each with the check that tests it. **Withdrawn** lists claims we made and got wrong, with what caught them. **Files** records every earlier file and what became of it. |
| `3_paper.md`, `3_paper.pdf` | The paper. The `.md` is the full text with every equation re-typeset; the `.pdf` is the original. |
| `4_replies.md` | Seven posts that answer her, in order, each at most 500 characters. Posts 1 to 5 take her reasoning one move at a time and end with what the claim owes. Posts 6 and 7 say why the paper does not hold up. |
| `4_1_record.png` to `4_7_frozen.png` | One picture per post, 1080 × 1080, to upload with that post. |
| `5_dissection.md` | The paper taken apart and put back together in plain language, Sections 5 and 6 first. For a general reader. |
| `6_review_for_the_authors.md` | The technical review, written to the authors. Every point gives an equation, a finding, and a repair or a request. |
| `8_checks.py` | One command that replays every claim and tests every goal. |
| `8_proofs.lean` | Finite proofs behind the reasoning in the posts: equal records give equal odds, and equal reports alone do not. |
| `9_pictures.cjs` | Draws the seven pictures. |

## Two rules

- **A claim stands only on a check.** That means a quote matched letter for letter, an exact derivation, a rerun of the paper's simulation, or a cited textbook result. Agreement between reviewers counts for nothing. Several outside reviews were read. Where one of them caught an error of ours, the error is listed under withdrawn in `2_dag.json`.
- **Keep the mistakes in the open.** When a check overturns a claim, the claim moves to withdrawn with its reason. It is never quietly edited away. The latest example is W1: we had said the density dip in Figure 6 comes from an $e^2$ term, and a rerun at three values of $e$ showed it is first order.

## Running the checks

```
python 8_checks.py              # every claim and goal, about two minutes (sympy, numpy)
python 8_checks.py --selftest   # breaks a quote, a length and a term, and confirms each is caught
python 8_checks.py --rerun      # also the paper's Appendix C simulation, about 30 minutes
lean 8_proofs.lean              # core Lean 4.35, no Mathlib; a silent exit means every proof checks
node 9_pictures.cjs             # redraws the pictures (Node with Playwright)
```

The earlier layout, with subfolders for the thread, the critique, the self-audit, the boards and the code, is in git history at commit `c3f17265a`. `2_dag.json` says what became of each of those files.
