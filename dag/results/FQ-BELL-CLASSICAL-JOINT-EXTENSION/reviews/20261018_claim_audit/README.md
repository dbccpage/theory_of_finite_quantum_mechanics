# Bell staged run: claim and value audit

The 22 original exact certificates agree with independent recomputation and
fresh Rust replay. The supported claim remains the supplied nonnegative,
normalized common-joint-law CHSH implication. Fine's converse is still open.
AuthorityEffect: None.

The review found real guard and evidence defects, rather than a false numerical
Bell witness. `findings.json` records each defect, its repair and evidence.

| Finding | Repair |
| --- | --- |
| Duplicate JSON keys silently replaced earlier values. | The current checker rejects duplicates in original bytes. A contradictory CHSH field is a regression case. |
| Public context could change without digest validation. | The checker recomputes the context digest. It explicitly treats anchor-name matching as labels, with separate source and native checks. |
| Original replay relied on optimizable assertions and accepted empty receipt arrays. | The current verifier uses explicit failures, requires native invocation/module coverage and logs, and rejects corruption under `python -O`. |
| Some stage deltas were prose or partial references. | Their historical format is disclosed. `operad_delta.yaml` and the cumulative collection retain complete typed generators, relation scopes and composition records. |
| Nullary composition was described more strongly than the original Lean graft formalized. | `bell_nullary_graft` now plugs `productsOp` with Empty input and the law identity with Unit input, then proves the actual closed tree evaluates to the Bell numerator. |
| Old protocol-test receipt retained only a transcribed completion excerpt. | This review retains a fresh command, full stdout/stderr and measured exit status. |

The original run and all 110 manifest-bound artifacts are byte-preserved. Its
checker and replay scripts are historical implementations with the defects above;
use this review's entry points for acceptance. The review is not a retroactive
P3/model turn and does not invent a provider call, independent human review or
unmeasured API charge.

## Current verification

From this directory, run:

    py -3.9 -X utf8 verify_review.py
    py -3.9 -X utf8 -O verify_review.py

The verifier checks original artifact hashes and stage bindings, exact candidate
values, the current source pins, complete native receipt coverage, named Lean
axiom reports, full test summaries, and fresh Rust/Python agreement. It uses
PyYAML for the cumulative operad record. The scripts do not authenticate their
own author or turn a receipt into mathematical authority.

Actual fresh executions and raw logs are in `validation/`. `run_checks.py` records
commands once and refuses to overwrite their output; use a separate destination
for a new check. `sources/` retains the audited native sources and build inputs.
`review_config.json` binds their current repository paths and the immutable
original manifest. `review_manifest.json` binds this review's complete file set.

Fresh checks passed: 12 Python tests, 10 Rust tests, 12 PFP protocol tests, nine
review regressions, 22 exact cross-language public laws, and Lean 4.33.1
compilation of the dependency chain with eight named axiom reports. The PFP
protocol tests inspect/prepare the corpus; they do not execute the other 176
mathematical targets. No full repository or hosted-CI success is claimed.

## Collected operad scope

The reusable maps are the nullary binary-response product table, binary
expectation on one exact law, unary CHSH functional, and the existing
score-partition/slack route. Function substitution has checked units,
associativity and semantic congruence. The actual nullary Bell graft now has a
named Lean theorem. These are scoped endomorphism substitution semantics.

Rust/Python use exact Q-valued APIs with finite regression evidence. Lean's
generic response-table theorem uses integral numerators; its bound requires a
positive common denominator and normalization. The general Q-table and
probability-subtype transport is not formalized. Neither a symmetric action, a
named Mathlib Operad instance nor syntactic quotient completeness is supplied.
The general score-mass/slack identities still lack a separate Lean partition
theorem. Native sample identities must not be promoted to that missing theorem.

No forced C4 numbers, prompt-index arithmetic, unsupported quotient values or
prefilled certificate answers were used in this staged run. Dimension 16 comes
from four binary responses; 22 is the actual retained public-case count, and test
counts come from fresh native summaries. The pair-law PR-box and signed-weight
examples fail the common-law or positivity premises; they are not countermodels
satisfying the proved theorem's premises.

The next mathematical step remains a precise compatible binary pair-marginal
extension contract and checked extension construction. This publication does not
execute that further research step.
