# lean4: finite results for the replies

`ThreadsReply.lean` uses core Lean 4 (v4.35.0) only, with no Mathlib and no lakefile. To check it:

```
lean ThreadsReply.lean
```

A silent exit means every proof checks. The file uses no `sorry`. `pigeonhole` uses `Classical.byContradiction`.

| Theorem | Board card | What it says |
|---|---|---|
| `records_do_not_fix_identity` | Picture 1, the tree | Two records are consistent with two different matchings of the lines, so which line fell is supplied, not witnessed. |
| `same_report_same_verdict` | Picture 2, rendering | An evaluator that reads only the report cannot separate two states with the same report. |
| `one_channel_not_every_channel` | Picture 2, rendering | Equal on one channel does not mean equal on another. |
| `same_report_not_same_likelihood` | Picture 2, rendering | Two hypotheses can both produce a report and still weigh it differently, so equal reports do not give a Bayes factor of 1. |
| `same_weights_same_likelihood` | Picture 2, rendering | The condition that does give a Bayes factor of 1: equal weights on every report. |
| `pigeonhole` | supporting | With more states than reports (`m < n`), two states share a report. The condition is part of the statement. |
| `small_domain_all_reported` | supporting | Without that condition, every state can be reported. |

These results are for the Threads replies, which stay finite. The continuum analysis of the paper is in `../code/`.

This folder is outside the repo's top-level `lean4/` library, so it is not part of the lake build or the governance scoring.
