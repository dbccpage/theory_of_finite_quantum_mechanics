# Six-directory L4A review

AuthorityEffect: None.

The scope is every Rust source and Cargo manifest under `holonomy`, `homology`,
`homotopy_type_theory`, `lie_theory`, `linear_algebra` and
`local_green_global_red_lggr`. Each subject has adjacent
`<complete filename>.scoring.yaml` and `<complete filename>.contract.yaml` files.
For example, `lggr_v.rs` has `lggr_v.rs.scoring.yaml` and
`lggr_v.rs.contract.yaml`. These are YAML 1.2 documents using JSON syntax.
Assessment metadata is not recursively treated as another source subject.
The older homology `*.score.yaml` files remain historical records.

The user explicitly confirmed that each file must gain actual L4 capability,
including current helpers and reexports. Preserving their current L1/L2 level
and only improving the engineering grade does not fulfill this goal.

`SCORING.md` version 2 is authoritative. L4A is the requested target, not a label
assigned by a generator. Capability is assessed independently of engineering
grade: export facades remain L1, and reference validators can remain L2.
Unreviewed gates remain null. Demonstrated E findings remain visible even if
other gates are incomplete, as required by section 1.4. Metric ceilings are
recorded separately from a complete semantic/operational G5 assessment.

Contracts initially record source custody, an interface index, and explicit
review obligations. `specs.json` supplies individually reviewed semantic scope
where available. Draft contracts do not assert that their requirements have
already been discharged. Lexical declaration indexes can include cfg/test
items and omit macro-generated items and reexports. The calibrated syn tool
measures explicit source bodies, not compiler-expanded code or operational cost.

Replays use a dedicated ignored source snapshot, offline dependencies, two
build jobs and disabled incremental compilation. Each owned build directory
is removed after the run, including failed runs. A new Cargo test invocation
requires 3 GiB free; this is a headroom check, not a reservation. The receipt
binds commands, versions, working directories, input hashes, logs, exit status,
and timeout outcomes. No other checkout or build directory is removed.

External absolute path dependencies are explicit. The replay binds resolved
package Rust sources, manifests and lockfiles before and after execution.
It does not attest authorship, non-Rust included assets, compiler expansion,
exact compiler file reads, universal memory safety or the entire workspace.
Default package tests compile `lib.rs`; compatibility `mod.rs` entry points
need distinct composition evidence.

Use Python 3.11+ and the installed offline Rust toolchain:

```powershell
python code/rust/quality/l4a_six/replay.py --metrics
python code/rust/quality/l4a_six/replay.py --metrics-only
python code/rust/quality/l4a_six/mutations.py
python code/rust/quality/l4a_six/differential.py
python code/rust/quality/l4a_six/probes.py
python code/rust/quality/l4a_six/consumer.py
python code/rust/quality/l4a_six/records.py --receipt evidence/quality/l4a_six/BASELINE/receipt.json --mutations evidence/quality/l4a_six/CAMPAIGN-mutations/receipt.json
python code/rust/quality/l4a_six/records.py --receipt evidence/quality/l4a_six/BASELINE/receipt.json --mutations evidence/quality/l4a_six/CAMPAIGN-mutations/receipt.json --check
```

The writer refuses changed source sets, source hashes, dependencies, metric
tool sources, logs or mutation reports. It checks all six mutation counts.
Passing a selected campaign does not award G4 A to every file. Candidate
recipes, compilation failures, survivors, timeouts and unrun cases remain
visible. An empty eligible campaign reports a null ratio.

Use `--baseline-extra RECEIPT` for successful targets from the same source
snapshot, `--defect-controls RECEIPT` for counterexample observations, and
`--differential RECEIPT` for sealed before/after comparisons. A DEFECT_CONFIRMED
marker establishes the failure class described in its witness (panic or
undefined-input coercion). NO_PANIC_OBSERVED is a finite observation, not
universal crash freedom. Counterexamples are never added to baseline counts.

## Current checkpoint

`evidence/quality/l4a_six/20261020T064257Z/REVIEW.md` binds 133 subjects and
266 scoring/contract sidecars. Schema/custody validation, deterministic
regeneration and PyYAML parsing pass. Six files have complete L4A assessments:
canonical rational admission, rank certificates, finite syntax, finite-category
nerves, strict finite A-infinity algebras, and the LGGR allocation regression
harness. Dense/sparse Smith remains L4B. Another 126 assessments are incomplete.

The primary `20261020T064307Z-mutations` campaign caught 191 faults, with two
literal recipe-construction failures and no survivors, equivalents, timeouts or
unrun cases. All five untouched/restored baselines pass: 573 scoped cases, with
stable sources and dependencies. Two multi-line hashing recipes did not match
CRLF source under the old LF-only runner. The corrected
`20261020T065325Z-mutations` replay caught all four hashing faults with successful
untouched/restored baselines. Its four kills are separate; the original two
invalid outcomes remain visible in `hashing_recipe_replay.json`.

The scalar control `20261020T064416Z-native-scalar-control` retains the public
provider i64 overflow finding. Exact unchanged trait/implementation item bytes
and Cargo/module/re-export bindings are pinned. This executable excerpt witness
does not assert a new whole-root package invocation. Known E remains visible.

Original sources, specifications and all 266 prior assessment bytes are sealed
in `20261020T064227Z-rank-activation`. The allocation-test repair now catches the
previous LGGR early-return survivor. Shared production faults may calibrate the
observer test file through explicit source/claim links; campaign totals count
each execution once. Empty, missing, duplicate or failed restoration runs cannot
support a complete G4 judgement. Seven retained-campaign regression checks cover
these evidence-refusal boundaries.

The new Smith candidate is staged separately. No all-files L4A, full-workspace
success, commit, pull request or merge is claimed.

## Previous completed checkpoint

The source-bound checkpoint is
`evidence/quality/l4a_six/20261020T060838Z/REVIEW.md`.
It covers 133 subjects and 266 scoring/contract sidecars. All sidecars pass
schema/custody validation, deterministic regeneration and PyYAML parsing.
Three individual files have complete L4A assessments: the executable finite
syntax, finite-category nerve and strict finite A-infinity modules. All three
formerly whole-file-disabled modules now have executable bounded replacements.
These claims are finite and domain-specific; the contracts state their limits.

The current focused campaign `20261020T060853Z-mutations` caught all 65
syntax/category/algebra/allocation faults, with successful untouched/restored
HoTT package baselines and stable sources/dependencies. Its 88 passing scoped
cases include unit tests, allocation observations and doctests. This does not
establish a new baseline for the other four packages. The all-package campaign
`20261020T061219Z-mutations` finished with 175 killed, one surviving LGGR
early-return candidate and no invalid, equivalent, inconclusive or unrun cases.
All five untouched/restored package baselines pass, with stable source/dependency
inputs. The current records use this campaign: 567 scoped cases passed. The
allocation-test repair for the surviving fault is staged separately; it does not
rewrite that outcome.

The source-grounded scalar control `20261020T062544Z-native-scalar-control`
reproduces the public provider i64 ExactRing/Semiring overflow. Exact unchanged
trait/implementation items and alias/Cargo/module bindings are pinned. This is
an executable excerpt witness, not a fresh whole-root package invocation.
The E finding remains visible. Three L4A and two L4B assessments are complete; the remaining 128 are incomplete.
No all-files L4A, full-workspace success, commit, pull request or merge is claimed.

## Historical checkpoints

The following earlier receipts explain intermediate repairs and failures.
Their source/dependency pins must be checked before reuse; their old status
statements do not describe the current checkpoint above.

An earlier source-bound checkpoint was
`evidence/quality/l4a_six/20261020T012607Z/REVIEW.md`. This metrics-only receipt
binds the source inventory and calibrated measurements; runtime baselines come
from the same-source campaign `20261020T013111Z-mutations`. All five untouched
and restored package baselines pass. A metrics-only run cannot establish test
adequacy without that separate same-source execution evidence.

The primary campaign records 70 killed and two surviving candidates (70/72),
with zero invalid, equivalent, inconclusive or unrun cases. One survivor is the
LGGR early-return mutation: final Boolean rejection remains intact, but
allocation/error behavior changes. No equivalence is inferred. The other is
scalar privacy: Cargo's filtered default test command omitted doctests. The
separate `20261020T014249Z-mutations` replay selects the doc target explicitly
and kills the same candidate. Input/candidate byte equality is recorded in
`20261020T012607Z/privacy_replay_comparison.json`. The original survivor remains;
this corrective replay does not overwrite it or add a count to the primary 72.
Untouched/restored baselines are complete; injections may use recorded source
filters. Privacy challenges now select the doc target explicitly.

The counterexample receipt `20261020T015314Z-defect-controls` no longer
reproduces the repaired Gaussian panic. It does reproduce the provider's
reexported i64 ExactRing overflow (G2/G3 E), public LGGR NaN-to-zero coercion
(G2 E), and a separate Smith sparse-output capacity panic (G3 E). The NaN
helper case does not show that admitted capacity-evidence constructors accept
NaN. Earlier receipts remain historical; UTC receipt dates are still October 19
in America/New_York.

All four former CCN-above-50 functions are factored into semantic phases, and
the rank certificate identity phase is below A structural ceilings. Other
functions still exceed some A ceilings. Pre-refactor bytes are sealed in
`20261020-complexity-before`. The `20261020T012738Z-differential` receipt records
746 Smith output/error comparisons, 48 complete ordered detector diagnostic
vectors, and 30 quintic validation outcomes. One new workspace refusal is not
replayed against the old allocation path. These are separate controls, not
production baseline tests or universal correctness proofs.

The individually reviewed holonomy matrix and dense Smith sources provide L4
capability. Matrix storage/domain admission, checked access/decoding and sealed
Q/Q(i) arithmetic were expanded earlier. The dense Smith API now exposes
configurable aggregate workspace/pivot limits, fallible row reservations,
iterative Bezout reduction and a checked U A V = D identity. Its separate sparse
API remains unsafe: the file is L4E, not L4A. Source hashes bind the individual
level reviews; no file has received a completed five-gate A assessment.

Root Gaussian construction/decoding and rational hash failures remain repaired.
Fallible homology digests preserve valid byte frames. Independent cases include
2401 Gaussian integer-pair combinations, literal signed digest frames, 729 Smith
matrices with determinantal-divisor/unimodularity checks, 4225 signed Bezout
inputs, a 2000-step Euclidean chain, and 11111 short CLI argument sequences.
Quintic certificate fixtures exercise F20, S5 and A5 paths with tampered bindings.

Priority work remains actual per-file L4 capability and all five A gates,
including the three semantic/failure E subjects, remaining metric ceilings,
provider/graph/connection admission and the three disabled HoTT modules.

`consumer.py` runs the selected QM density/Pauli test against the actual root
crate, using frozen resolution and host-filtered metadata. Its receipts are
separate from the scoped package baseline; require a successful run and unchanged
inputs before treating one as composition evidence. Earlier metadata failures
remain preserved. The root lockfile now includes the holonomy serde_json test
dependency already declared in its manifest.
The actual-root run `20261020T005803Z-qm-consumer` compiled and passed its one
selected test, with stable inputs at completion. A later edit to
`src/mub/Cargo.toml` made its full-root dependency envelope stale; the writer
refused to attach it as current composition evidence. It remains historical,
separate from the current six-directory assessment.

The initial baseline had 458 passing tests. Its structural replay found 170
functions beyond at least one A ceiling, including four with CCN above 50.
The focused repairs add trace arithmetic/domain controls, LGGR admission and
allocation controls, a 6561-pair finite rank/witness oracle, and malformed
holonomy endpoint controls. Historical failing regression receipts are kept
separately from successful replays. The broad L4A objective remains active.
