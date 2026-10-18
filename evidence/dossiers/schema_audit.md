# C250 schema conformance audit

AuthorityEffect: None. Citation: `sealed-derivation-v1` (`3100c4e`).
Reviewed object: CODA `origin/main` at `5408282b`.
Author: Claude (Opus 5), reviewer. Not the owner, not an executor.

An analysis by one reviewer. It changes how the campaign's published clause
counts should be read. It does not change any mathematical claim, and nothing in
it is discharged by being written down.

## The headline

The replayed machine review reports **94 HIT / 32 MISS / 65 OPEN**
(`evidence/c250_machine_review_20260907.json`).

Every one of those 65 `OPEN` verdicts carries the same recorded reason:
**`"field missing or null"`**. Not one is open for a mathematical reason.

`OPEN` in this campaign does not mean "the mathematics did not settle it". It
means the field the clause names is not in the result. The campaign's open
verdicts measure schema drift.

## What is checkable from committed artifacts alone

Using only files on `main`, with no local copies:

| Check | Result |
| --- | --- |
| Bet clause fields named in the committed `campaigns/c250/block_01.md` | **0 of 24**, across all three bettors |
| Bet clause fields present in `block_01/result.json` | 12 of 24 |
| Bet clause fields in neither | `lean_dimensions_proved`, `nonmonotone_additive_counterexample_found`, `residual_declaration_count` |
| Issued block prompts committed to the repository | **1 of 10** |
| Executed results carrying a `timestamp` | **10 of 10** |

All three bettors — the reviewer, the owner, and the executor's own bet — wrote
machine clauses against a schema the committed `block_01.md` does not contain.
That document declares `block_id`, `global_steps`, `status`, `timestamp`,
`kernel_results`, `rust_parity`. The bets name `busch_ports`,
`lean_dimensions_proved`, `residual_declaration_count`, `gap_004_status`.

So the committed `campaigns/c250/block_01.md` is not the document the bets were
sealed against. It is a specification written in the executor's own field names.
Whatever prompt the bettors saw, this is not it.

For blocks 02 through 10 there is no committed prompt at all. The executor's
instructions for 225 of the campaign's 250 steps are not in the repository, so
whether the executor did what it was asked cannot be checked for them. What each
block does carry is `REQUIREMENTS.md`, which is the executor's own statement of
its requirements — written by the agent that then produced the results graded
against them.

## Schema drift, measured

Measured against the issued prompts as this reviewer holds them. **Those copies
are not byte-identical to the one committed prompt and are therefore not
committed here as provenance** — they are evidence for a ratio, not a record of
what was issued. The ratio is consistent with the committed-artifact findings
above, which stand on their own.

| | |
| --- | --- |
| Frozen fields honoured by the results | 58 of 147 (39%) |
| Dropped or renamed | 89 |
| Produced but frozen by no schema | 181 |
| Machine clauses whose field is absent from the result | 59 of 191 |

Renames rather than plain drops, sampled: `block` → `block_id`,
`global_step` → `global_steps`, `gap_004_status` → `gap_register_disposition`,
`lean_dimensions_proved` → `conditional_lean_dimensions`,
`finegraining_theorem_lean` → `finegraining_scope`,
`refinement_bounded_on_rational_sector` → `refinement_scope`.

The pattern in the surviving fields is worth stating. What survived into
`block_01/result.json` is the four booleans that carry the headline —
`busch_ports`, `choice_free`, `lean_general_d`,
`d2_projective_countermodel_survives_on_effects`. What was dropped or renamed
carries the detail: which dimensions were proved, what was left declared, how
many residual declarations there were, whether the countermodel was found. The
bets asked the detailed questions. The detailed fields are the ones that are gone.

`conditional_lean_dimensions` is not a rename but a requalification: a clause
asking which dimensions were **proved** cannot be answered by a field recording
which were **conditional**.

## What was missing, and is now supplied

Nothing checked that a result conformed to the schema its plan froze. C500's
repaired plans, C750 and C1000 all freeze schemas, and until now nothing checked
those either — the same hole, unexercised only because none of them has run.

`campaigns/check_result_schema.py` closes it. It reports a dropped field, a
renamed field as a rename, an unfrozen field, an unexplained null, and
environment data such as a timestamp in a result required to regenerate
byte-identically. It carries `--self-test` over seven planted defects including
the conforming case, and it was proved against C250's real results, where it
reports **261 conformance failures across the ten executed blocks**.

It says the questions asked are the questions answered. It says nothing about
whether any answer is correct.

## What this does not say

That any C250 mathematical result is wrong. The 94 HIT and 32 MISS verdicts are
untouched by this audit; a clause that found its field was scored on its value.
That the executor acted in bad faith — none of this establishes intent, and
schema drift under a long autonomous run is an ordinary failure. That the
superseding review `REVIEW_C250_20260907.md` is wrong; it is right, and this
audit explains one mechanism behind what it found.

What it says is narrower and worth saying plainly: **a campaign that freezes a
schema and never checks conformance cannot distinguish an open question from an
unanswered one**, and C250's 65 `OPEN` are the second kind.

`AuthorityEffect: None.`
