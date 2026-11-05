# lean4: finite results for the replies

`ThreadsReply.lean` uses core Lean 4 (v4.35.0) only, with no Mathlib and no lakefile. To check it:

```
lean ThreadsReply.lean
```

A silent exit means every proof checks. The file uses no `sorry`. Axioms: `pigeonhole` uses `propext`, `Classical.choice` and `Quot.sound`; `records_do_not_fix_identity` uses `propext`; `iidLikelihood_pos` uses `propext`; `same_weights_same_likelihood` uses `propext` and `Quot.sound`; the rest use none. The statements were tightened in the self-audit ([../self_audit.md](../self_audit.md) §D).

| Theorem | Board card | What it says |
|---|---|---|
| `records_do_not_fix_identity` | Picture 1, the tree | There are two one-to-one matchings of the lines between the records under which a different line is the one that fell. Which line fell is supplied, not witnessed. |
| `same_report_same_verdict` | Picture 2, rendering | An evaluator that reads only the report cannot separate two states with the same report. |
| `one_channel_not_every_channel` | Picture 2, rendering | Equal on one channel does not mean equal on another. |
| `same_report_not_same_likelihood` | Picture 2, rendering | Two hypotheses with the same total weight (10) can both produce a report and still weigh it differently (9 against 5), so equal reports do not give a Bayes factor of 1. |
| `same_weights_same_likelihood` | Picture 2, rendering | The condition that does give a Bayes factor of 1, **under independent sampling**: equal weights on every report give equal likelihoods (`iidLikelihood`, the product of weights) for every finite data list, with a nonzero denominator when every observed report has positive weight. |
| `same_marginals_not_same_joint` | Picture 2, rendering | Without independence the product rule fails: two independent fair bits and one fair bit read twice have the same single-report weights, but (true, true) has weight 1 of 4 against 2 of 4, a Bayes factor of 2. |
| `pigeonhole` | supporting | With more states than reports (`m < n`), two states share a report. The condition is part of the statement. |
| `small_domain_all_reported` | supporting | Without that condition (`n ≤ m`), every state can get its own report. |

These results are for the Threads replies, which stay finite. The continuum analysis of the paper is in `../code/`.

This folder is outside the repo's top-level `lean4/` library, so it is not part of the lake build or the governance scoring.
