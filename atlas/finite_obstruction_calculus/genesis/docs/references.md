# Source reader

Every manuscript citation has a local destination in this package. The original
repositories were private when checked on 2026-10-09. Their URLs identify source
custody; reading the cited material does not require repository access.
The [citation manifest](../manifests/cited_sources.json) gives each original
path, full revision, Git blob identity, byte count and SHA-256 hash. Reading
copies retain the original UTF-8 bytes, including line endings. The `.txt`
copies contain historical Markdown source; their internal links retain original
paths and are not links to a newly reconstructed website. The index below gives
the corresponding reading locations. A `#L` suffix in a manuscript citation
identifies the original line number.

## Pre-Genesis record

These records come from `dbccpage/the_symbol_game` at
`d1d2f034198a72b730320a69691e63351557c019`. They retain the
[source repository license](sources/symbol_game_license.txt).

- [Strand introduction](sources/pre_genesis/readme.txt).
- [Experiment design chapter](sources/pre_genesis/01_experiment_design.txt).
- [Trial record chapter](sources/pre_genesis/02_trial_record.txt).
- [Results and arguments chapter](sources/pre_genesis/03_results_and_arguments.txt).
- [Named failure modes](sources/pre_genesis/04_named_failure_modes.txt).
- [Method lessons](sources/pre_genesis/05_method_lessons.txt).
- [Original source index and missing metadata](sources/pre_genesis/sources/readme.txt).
- [Original design](sources/pre_genesis/sources/design_derivation_v0.txt).
- [Trial 1 transcript](sources/pre_genesis/sources/trial_1_transcript.txt).
- [Trial 2 transcript and appended analysis](sources/pre_genesis/sources/trial_2_transcript.txt).
- [Full-history replay prompt pack](sources/pre_genesis/sources/full_replay_prompt_pack.txt).
- [Full-history replay transcript](sources/pre_genesis/sources/full_replay_transcript.txt).
- [Historical analysis of the trials](sources/pre_genesis/sources/analysis_derivation_v1.txt).

The historical analysis is part of the recorded experiment, rather than a
review of this manuscript. Its author and the trials' model metadata were not
recorded. It does not supply host-checker verdicts or measured success rates.

## Mathematical and continuation accounts

These records come from `dbccpage/19L57G1` at
`f1d56c010e6ba10a3b9418bd7cc5953c067250f2` and retain its
[Apache 2.0 license](../code/derivation/LICENSE).

- [Genesis source manuscript](sources/genesis_source.txt).
- [Continuation manuscript and bounded census](sources/continuation.txt).
- [Source closeout and approved freeze](sources/closeout.txt).
- [Source README and historical verification counts](sources/genesis_readme.txt).
- [Pinned proof and Python source manifest](../manifests/mechanization_sources.json).

The manuscript's theorem citations point directly to the bundled `.lean` or
`.py` files, including relocated research modules in the flat Lake package.
All 120 imported files are checked against the saved upstream Git inventory,
including their line endings. Compilation and mathematical replay are separate
checks; byte identity alone does not establish a theorem or reproduce a census.

## Education and incidence interpretation

These accounts use the same Symbol Game revision and source license as the
Pre-Genesis record.

- [Genesis education account](sources/genesis_education.txt).
- [Primitive-to-incidence construction account](sources/incidence_construction.txt).

The incidence account is a historical description of the chosen interpretation
and checked executions. The standalone reproduction does not claim a general
Lean refinement theorem for that Rust construction.
