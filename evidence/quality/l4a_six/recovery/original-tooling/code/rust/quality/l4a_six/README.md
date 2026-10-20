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
is removed after the run, including failed runs. Default cold-build admission
requires 3 GiB free. Explicit smaller scoped campaigns may select 2 GiB cold
admission and a separately recorded 1 GiB reserve when reusing their own cache;
the completed cache is not charged a second time. These are headroom checks,
not reservations or peak-space guarantees. The receipt
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

## Current integration in progress

`20261020T145316Z` currently holds a **provisional** 134-subject, 268-sidecar
refresh. All scoring records pass the canonical schema, all contracts pass
`contract.schema.json`, both pass source/evidence custody checks, deterministic
regeneration agrees, and independent PyYAML 3.9 parsing agrees with JSON for all
134 exact pairs. Nine malformed contract controls are rejected. This refresh
does not attach an incomplete mutation campaign, so verification-dependent
grades remain unassessed; its zero completed assessments are not a retraction
of the archived, source-bound earlier checkpoints.

Actual-root composition `20261020T145120Z-qm-consumer` passes six selected
filters (39 case executions) with unchanged dependencies, sources and lockfile.
The owned 1,805,795,450-byte build is removed. This includes the real Gleason
consumer after its count-getter migration; it is not a full workspace test run.
The integrated campaign `20261020T145348Z-mutations` passed all five untouched
baselines, caught 33 faults and then lost its disk reserve; 232 remain unrun in
that receipt. All original outcomes remain unchanged. The calibrated continuation
`20261020T154249Z-mutations` retains those 33 executions and catches four more,
then stops with 37 killed and 228 unrun. Subsequent admission refusals are
separate receipts. No completed integrated restoration or A promotion is claimed.

Continuation now verifies exact source, dependency, toolchain, recipe, candidate
and log hashes, and pins the retained Cargo lock. Successful untouched baseline
executions may be reused with explicit provenance; all restoration baselines
must execute in the continuation. A 1.5-GiB cold admission requires a verified
same-source completed-cache observation plus a separate 512-MiB margin. The
measured scoped cache was 713,309,921 bytes. These endpoint observations do not
bound peak compiler use or external disk activity. Compiler disk failures are
inconclusive; an unresolved designated critical fault withholds G4 A even if
the aggregate mutation ratio exceeds 95 percent.

Separate candidates remain outside the installed Cargo source tree:
`20261020T150133Z-holonomy-matrix-candidate` passes its 20-fault trial
`20261020T150139Z-holonomy-matrix-trial`. Borrowed canonical-domain checking,
admitted conjugation and trace changes have passing untouched/restored targets.
`20261020-pi-candidate` supplies a finite dependent-product model with borrowed
admission and mixed-radix rank/decode; `20261020T152451Z-pi-trial` catches all
18 faults and passes both 75-unit/10-doc baselines. The candidate metrics receipt
`20261020T152850Z-candidate-metrics` places both sources in the A metric band.
`20261020-unit-candidate` supplies a finite terminal-object certificate, with
opaque names and no general HoTT inhabitance claim; its standalone trial
`20261020T153809Z-unit-trial` catches all 16 faults and passes both baselines.
Its completed build cache was 93,143,904 bytes. The small five-dependency HoTT
trial supports a 512-MiB cold reserve and 256-MiB warm reserve; this is not the
large root/audit build envelope. These staged results do not award live grades.

The integrated campaign `20261020T110705Z-mutations` completed with **249 killed,
zero surviving, invalid, equivalent, inconclusive or unrun faults**. All five
untouched and restored package baselines passed (652 scoped passing cases).
Source and dependency custody remained stable, and the owned build was removed.
The calibrated metric receipt is `20261020T105944Z`. These are scoped execution
results, not a completed assessment of all 134 subjects.

Refreshing the actual-root consumer evidence remains separate. The selected
12 tests passed in `20261020T141243Z-qm-consumer`, but a concurrent edit outside
the six directories changed its dependency envelope during execution. That
receipt cannot discharge current composition custody. The subsequent
`20261020T143828Z-qm-consumer` attempt did not start compilation because its
three-GiB admission check failed. Earlier receipts retain their original status.

The ordered-algebra candidate's first fresh
trial `20261020T144202Z-ordered-trial` passed 32 ordered tests, then stopped at
the next disk admission: all 16 designated faults remain unrun in that receipt.
The successor trial records separate cold-build and warm-cache admission
thresholds, releases the test cache before metric compilation, and retains all
refusals. That successor, `20261020T144403Z-ordered-trial`, caught all 16 faults,
passed both untouched/restored targets and met calibrated A metric ceilings.
`20261020T145101Z-ordered-activation` installed the private count admission and
LDL phases, migrated the direct QM getter, and archived replaced sources and
sidecars. Fresh root composition, a 265-fault integrated replay and sidecar
validation are required before treating its individual review as completed.

The checked scalar/matrix migration was activated in
`20261020T104119Z-scalar-activation`, after 46 staged faults were caught and the
separate full root-module test composition compiled. That activation archives
all replaced sources and all 266 preceding assessment sidecars. The new provider
adapter makes the live subject count 134. Fresh integrated scoring is pending;
the earlier provider scalar/matrix E controls are historical source-bound facts,
not counterexamples against the replacement owned APIs.

The first restarted integrated replay exposed three scalar test regressions:
constructor-zero, imaginary-component and unknown-wire-field faults survived.
Its incomplete outcomes remain in `20261020T104923Z-mutations/INTERRUPTION.json`.
All nine original scalar contract tests were restored with explicit Result API
adaptations in `20261020T105520Z-scalar-regression-restoration`. Production scalar
code was unchanged by that restoration. The preceding headroom-interrupted
attempt is separately retained in `20261020T104241Z-mutations/INTERRUPTION.json`.
Neither incomplete run is accepted as grade evidence.

The focused corrective replay `20261020T105539Z-mutations` catches all 18 scalar
faults, with passing complete untouched/restored package baselines and stable
custody. `20261020T105944Z` supplies refreshed calibrated metrics. The actual-root
receipt `20261020T110235Z-qm-consumer` passed five explicit filters (12 cases)
with stable custody at completion; later dependency drift makes it historical.
It does not execute the complete root/workspace suite. The full integrated
249-fault campaign completed in `20261020T110705Z-mutations` before the ordered
activation. A fresh integrated campaign must bind the new ordered bytes.

The former public Inertia count-overflow finding is reproduced in
`20261020T110958Z-inertia-control` with an external caller module. It remains
bound to the archived public-field source. The replacement count representation
is activated as described above; no counterexample against old bytes is silently
reclassified or passed to the writer as a current-source control.

## Last completed checkpoint

The Smith candidate is integrated byte-for-byte after the separate 29-fault
staged trial. Original source and all 266 prior assessment bytes are sealed in
`evidence/quality/l4a_six/20261020T074553Z-smith-activation`.
The heuristic now returns Result and has an explicit workspace-limit variant;
its outputs remain explicitly uncertified as Smith invariants.
`evidence/quality/l4a_six/20261020T074554Z/REVIEW.md` records seven L4A files,
582 passing scoped cases, and 126 incomplete assessments. All 266 sidecars pass
schema and custody validation. The `20261020T074603Z-mutations` campaign caught
all 208 faults with no other outcomes; all five untouched and restored package
baselines passed with stable source/dependency custody and owned build cleanup.

The then-current scalar and matrix controls (`20261020T074614Z-native-scalar-control`
and `20261020T082506Z-native-matrix-control`) retain separate G2/G3 E findings:
native scalar addition and public legacy matrix multiplication overflow. The
matrix control invokes the exact pinned provider behind the unchanged root
alias; it does not claim a fresh whole-root build. The scalar protocol and caller
migration were still staged under `scalar_port` at that checkpoint.

## Previous completed checkpoint

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
