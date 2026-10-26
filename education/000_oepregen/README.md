---
documentation_contract: symbol-game-documentation/v1
title: "000_oepregen: What a language model does with an empty mark"
kind: grammar-reference
audience:
- researchers
- engineers
- coding-agents
status: active
maturity: research
claim_status: source-grounded
authority_effect: "None"
source_paths:
- omega_engine_education/documentation/000_oepregen/sources/README.md
prerequisites: []
aliases:
- 000_pre_genesis
related:
- ../001_oegen/README.md
- ../002_oesn/README.md
- ../003_oemssn/README.md
- ../004_oepfp/README.md
last_verified: 2026-10-06
---

# 000_oepregen: What a language model does with an empty mark

**AuthorityEffect:** None.

## What this strand is

Before Genesis admitted its first mark, the author gave a language model the
bare inscription `<>`, then `<a>`, then a task about `<a>` and `<ab>`, and
recorded what the model added, what it refused, and where it went wrong. There
are three recorded runs: Trial 1, Trial 2 and a full-history replay. This
strand keeps those transcripts, explains what they show and what they do not,
and carries the small grammar of the inscriptions that occurred.

The chapters were rewritten on 2026-10-06 from the restored transcripts. The
earlier versions contained a fabricated "50 trials" pass-rate table, invented
quotes, and antibody, refusal and error-code names that exist nowhere else in
the repository; see the pull request that made this change for the list.

## Layout

| Path | Role |
| --- | --- |
| [`sources/`](sources/README.md) | The primary record: design, two trial transcripts, the replay prompt pack and transcript, and the analysis. Every citation points here. |
| [`01_experiment_design.md`](01_experiment_design.md) | The question, the principle "constrain epistemology, not mathematics", the hidden comparison targets, the pre-registered branches. |
| [`02_trial_record.md`](02_trial_record.md) | What was sent and what came back, prompt by prompt, with exact quotes. |
| [`03_results_and_arguments.md`](03_results_and_arguments.md) | The seven statements drawn from the trials, each labelled by kind; proofs of forced separation and replay necessity. |
| [`04_named_failure_modes.md`](04_named_failure_modes.md) | Names for the failures observed, each tied to its reply, and how PFP answers them. |
| [`05_method_lessons.md`](05_method_lessons.md) | Working practice for running such trials. |
| [`curriculum/`](curriculum/README.md) | Eight lessons with objectives, readings, exercises, answers, and 4-phase learning progression. |
| [`video/script.yaml`](video/script.yaml) | Narration and visuals for the explainer video; build with [`../../education_app/_docs/video_builder.md`](../../education_app/_docs/video_builder.md). |
| [`grammar/`](grammar/README.md) | `pre_genesis.ebnf`: a notation for the inscriptions that occurred, with conformance cases. |
| [`code/`](code/) | `check_pre_genesis.py` and its tests. |

Naming convention shared with the sibling strands: a strand directory is
`NNN_<snake_case_slug>`; its grammar is `grammar/<slug>.ebnf` beside
`grammar/<slug>_conformance_cases.json`; its checker is `code/check_<slug>.py`
with tests in `code/tests/`; prose chapters are `NN_<snake_case_title>.md` in
reading order. Links are relative POSIX paths.

## The short version

- Told that `<>` has no meaning and asked for at most one move, the model said
  no continuation is forced in all three runs.
- Given `<a>`, two runs called it "the same state presented differently" and
  one called it "a new state". Both are defensible; the answer depends on a
  convention nobody had declared.
- With no observations, every pair of inscriptions is equivalent. A task that
  needs `<a>` and `<ab>` told apart requires a representation that preserves
  their different answers. Several supplied observations can do that.
- The failures that mattered were about state, not symbols: a false
  attribution went unchallenged, a reply lost the current state, and an auditor
  who saw only one turn certified it. The main theorem identifies the precise
  failure: equal visible reports with different required answers. A sufficient
  summary can preserve the answer; retaining raw history is a separate
  provenance choice made by PFP.

## What this strand does not claim

- Three runs of one unrecorded model support no rates and no generalisation.
- The model did not rediscover any part of the Omega Engine.
- No host checker evaluated any reply; judgements in the analysis are human or
  advisor-model judgements.
- The grammar is notation, not a finding.

## Verification

```bash
py -3.12 omega_engine_education/documentation/000_oepregen/code/check_pre_genesis.py
py -3.12 -m pytest omega_engine_education/documentation/000_oepregen/code/tests/test_pre_genesis_grammar.py
py -3.12 -m omega_engine_education.education_app.entrypoints.cli verify-strand 000
```
