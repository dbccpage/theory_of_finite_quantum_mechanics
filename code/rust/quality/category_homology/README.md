# Category theory and homology scoring

AuthorityEffect: None.

Each Rust source in the two directories has an adjacent `name.score.yaml`.
These are SCORING.md v2 records, not contracts. Contract paths remain pending.
The architecture target is L5 and the engineering target is A. Capability
levels describe delivered behavior: a re-export stays L1, a metadata shell
stays L2, and an admitted certificate checker can be L5.

Null gates mean unassessed. A passing package suite, a source hash, or a good
mutation ratio does not automatically award every file A. In particular, the
current records do not certify all failure classes, consumer composition,
macro-expanded flow, resource bounds, or external dependency provenance. The compatibility root
`category_theory/mod.rs` is distinguished from the actual crate entry `lib.rs`.
Completed reviews can additionally pin callee and consumer sources in
`context_inputs`. Verification refuses changed context even when the subject
file itself is unchanged. A historical score is not a current-tree pass.

The homology core checks exact rational rank certificates using `M = UV`,
`LU = I`, and `VR = I`. The certificate checker does not trust elimination.
Its canonical carrier owns immutable admitted cochain data and rank evidence.
Raw candidate certificates remain untrusted until admitted. Rust's unchecked
`BigRational::new_raw` path, deserialization, basis mismatches, degree overflow,
and malformed simplices receive explicit admission checks.
Rank-zero production now handles zero-area matrices independently of metadata
dimensions, including `0 x usize::MAX`. Row-reduction and inverse failures keep
their typed sources. The rank review maps all 15 production symbols to an exact
algebraic specification and audits its canonical-carrier consumers. Its Lean
model proves the rank conclusion, explicit refusal, first-error preservation and
index bounds. The accompanying source review maps Rust construction and error
paths to that model under the declared exact-arithmetic/runtime boundary. This
does not claim mechanized Rust/MIR refinement or machine-checked crash freedom.

The category core owns law-checked finite endpoints and functor maps. Metadata
catalogs remain declarations; their mathematical names do not establish their
advertised structures. Some public APIs now return `Result`/`Option`, and
certificate fields are read-only. Weighted records use `BigRational`.

Finite-category validation builds a sorted borrowed composition view for each
relevant checking phase. Cubic associativity enumeration therefore avoids
temporary owned lookup strings. The independent category challenge examines all
81 unital three-arrow tables via regular-action matrices, with explicit malformed
domain, typed diagnostic and immutable-ownership challenges. `FC05` challenges
diagnostic completeness: removing the totality phase is still observable even
where another phase also rejects the same incomplete table.
`proofs/FiniteCategory.lean` models exact partial composition and reconstructs
Mathlib's actual `Category` interface, with identity and associativity laws.
As with the rank model, Rust representation and failure correspondence receive
a separate source review; a model theorem alone does not verify Rust/MIR.

Natural-transformation admission checks lawful categories and total lawful
functors, exact component domains and every square. Certificates own their
endpoint context. The formerly disabled composition module now builds and
checks identities, vertical composition and horizontal composition, rejecting
different contexts even when names agree. Independent cyclic-group arithmetic
challenges exercise associativity and interchange. Raw declared operations
assemble candidates; only checked operations return admitted certificates.

The rewriting module admits finite globular declarations; its legacy Infinity
names do not establish an infinity-category. Owned, immutable context binds
normal-form witnesses and decreasing-rank termination certificates. Rank
admission checks the exact term domain and strict descent independently of
the iterative topological-sort producer. Directed graph analysis uses forward
edges; formal inverse paths cannot establish forward local confluence.
Whiskering checks fresh names and admission before committing a candidate.
The challenge suite compares all 512 directed graphs on three vertices with a
Boolean Floyd-Warshall oracle and checks a 20,000-node chain without recursion.

The strict 2-category module now owns checked underlying and vertical categories.
It checks globularity, exact horizontal composition domain and boundaries,
strict units, horizontal associativity, identity preservation and interchange.
Boundary and identity queries return typed errors for unknown identifiers.
Before enumeration, checked arithmetic admits a declared law-work measure;
its default limit is 1,000,000 units. This measure bounds the enumerated tuple
families up to constant phase multiplicities, ordered-map lookup and label-size
costs; it is not a machine-instruction count or a wall-clock timeout.
The independent scalar challenge examines all 6,561 pairs of unital operations
on three elements using the Eckmann-Hilton characterization. Two-color examples
separately distinguish associativity, strict-unit and identity-preservation
failures. `TC` selects the designated mutation campaign for these boundaries.

Run the audit with Python 3.11+ and Cargo:

```powershell
python code/rust/quality/category_homology/run_audit.py --mutations
python code/rust/quality/category_homology/run_metrics.py
python code/rust/quality/category_homology/run_rank_proof.py
python code/rust/quality/category_homology/run_rank_proof.py --model category
python code/rust/quality/category_homology/write_scores.py --receipt evidence/quality/category_homology/RECEIPT --metrics evidence/quality/category_homology/METRICS
python code/rust/quality/category_homology/write_scores.py --receipt evidence/quality/category_homology/RECEIPT --metrics evidence/quality/category_homology/METRICS --check
```

On this machine the bundled Python is at
`C:/Users/a343o/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.
For a category-only replay use `--scope category`; `--mutation-prefix NT`
selects the natural-transformation campaign. Use `--only` followed by
repository-relative Rust paths when refreshing a subset of score records.
A category-only receipt is refused for homology records. This allows separate
source-bound semantic receipts without rebuilding unrelated dependencies.
`--scope homology` runs only the homology package. New replays also capture
offline Cargo metadata, resolved lockfiles, package/ancestor file hashes,
compiler binary digests, relevant flags and the exact harness. Dependency file
contents must agree before and after the replay. Mutation restoration preserves
original source bytes, including line endings. These records bind content;
they do not attest authorship or prove exact compiler file-read tracing.
The `RK` campaign covers rank-certificate faults. Historical invalid recipes
remain disclosed in their receipts, alongside corrected source-bound replays.
The `RW` mutation prefix selects designated rewriting failures. Explicit,
source-pinned gate reviews may be supplied with `--assessment` when selecting
one file with `--only`. A metric or mutation ratio never grants a grade by
itself; unreviewed gates stay null and prevent a completed score token.

The AST metric tool pins syn 3.0.9 and its dependencies in `rust_metrics/Cargo.lock`.
Eight hand-counted calibration cases cover lifetimes, closures, control flow,
guards, typed exits, test exclusion, macro opacity and malformed source. The
measurement policy is documented in its source: CCN includes typed `?` exits;
cognitive values are conservative upper bounds; closure scopes contribute to
nesting, including control expressions inside conditions. Known standard formatting/vector macro arguments are parsed, while
unknown macro bodies are explicitly opaque. Macro-generated functions and
compiler expansion require separate review. These metrics constrain structure;
they do not certify semantic correctness or automatically establish G5.

Replay copies source into an ignored snapshot and uses a distinct build
directory per run, with incremental compilation disabled. Mutations affect
only that snapshot. Completed builds delete their `target/debug` and `target/tmp`
outputs, including failed builds. The run also removes its remaining build tree
on completion, preserving source snapshots and receipts. Rebuilding dependencies
costs time; bounded disk use takes precedence. The initial and restored baselines must pass. Every
candidate is retained as killed, survived, equivalent, invalid, inconclusive,
or unrun; only eligible semantic candidates enter the conservative ratio.
Earlier failed or limited campaigns remain in the evidence directory.
New Cargo invocations require 3 GiB free each time and use two build jobs. A
headroom refusal starts no compiler and records the mutant as unrun. Proof
checks use Lean's internal 1024 MB memory limit and two threads. Heavy compiler
replays are run serially; these controls do not claim a global process-memory or
disk-space reservation guarantee.

The writer refuses stale source hashes, changed logs, inconsistent mutation
accounting, stale AST tool sources, or unsuccessful/restoration baselines.
Rank-model proof receipts also bind the compiler, explicit dependency search
paths, direct library inputs and clean Mathlib revision. Proof execution uses
the resolved compiler directly, excluding mutable main-project output modules.
Timeouts remain unsuccessful even if axiom reports were printed before timeout.
Unresolved proof warnings also prevent acceptance. New proof receipts retain
both the exact runner and its execution helper as hashed runtime snapshots.
`--check` verifies both the adjacent YAML files and their SHA-256 manifest.
Derived score manifests live in the metric receipt, preserving historical
semantic receipts. This scoped replay does not
claim a successful build of every Rust workspace member.

Publication checkpoint (restoration after the concurrent merge): all 192 Rust
files have adjacent records. `finite_category.rs` is L5A and
`finite_category_validation.rs` is L3A. The other 190 records have incomplete
gates. The earlier rank L5A assessment remains historical evidence for its
pinned provider context; incoming linear-algebra changes invalidate its use as
a current-tree pass. Those provider changes are preserved. Contracts remain
pending, and the directory-wide engineering A goal remains unfinished.

Historical execution receipts describe this Windows checkout and its pinned
local dependency and toolchain paths. They are not portable CI attestations.
The scoped Git attributes preserve the exact source, harness and evidence
bytes referenced by their hashes, including historical CRLF source snapshots.
Fresh replay requires the declared dependencies and produces new receipts.

The publication integration receipt `20261018T214243Z` has successful category
and homology baselines and a successful category repeat. The homology repeat
printed 95 passing tests but its Cargo process hit the deadline, so the receipt
correctly remains unsuccessful. Sources and dependencies stayed stable, and
all owned build outputs were removed. See the publication checkpoint for this
limitation; it does not replace the earlier category-only grading receipt.

Cargo deadlines are configurable with `--build-timeout SECONDS` (default 900).
The deadline covers the whole Cargo process, including compilation and exit.
A printed test-success line never overrides a timed-out process result.

The resumed 2026-10-18 checkpoint has 66 completed engineering-A records and
126 incomplete records, with a current source digest beside all 192 Rust files.
The 62 reviewed constant-length label schemas remain L2A. Their validation
returns the existing typed `ArithmosError::InvalidShape`; constructors and serde
still return raw declarations, never a proof of the named mathematical laws.
The separate schema specification, all public-method source mappings, checked
ordered-refusal model and 586 single-fault challenges support those narrow
assessments. Independent module namespaces share compilation; each candidate
contains one fault and executes its own tests. This is not an alternate compiler.

The historical 66-file checkpoint rank replay restored `rank_certificate.rs` to L5A after
an explicit provider-delta review, 95 ordinary homology tests before/after and
eight separately dispatched rank faults. The degree-window metadata file is
L2A after repairing its reachable signed-subtraction overflow. Its 49 extreme
endpoint pairs, checked integer-bound model and eight eligible semantic faults
cover the repaired boundary. The original overflow source, ambiguous invalid
recipe and disk-refused attempt remain visible; the latter is explicitly tied
by candidate SHA to its later successful challenge. No failed execution is a
passing receipt. The final category replay passes 455 tests before and after.

Replay the additional scoped challenges and verify the checkpoint with:

```powershell
python code/rust/quality/category_homology/run_metadata_challenges.py
python code/rust/quality/category_homology/run_rank_context_replay.py
python code/rust/quality/category_homology/run_rank_proof.py --model metadata
python code/rust/quality/category_homology/run_rank_proof.py --model degree
python evidence/quality/category_homology/resume-20261018/verify_scores.py
```

The score writer accepts an explicit `--assessment-map` for an exact selected
batch. Missing reviews are refused before any adjacent record is written;
this option does not infer gates or promote an unreviewed file. The progress
inventory and per-file remaining work are in
`evidence/quality/category_homology/resume-20261018/progress.json`.
The broader architecture/engineering goal and all pending contracts remain open.


The 2026-10-19 checkpoint supersedes that rank failure review: 79 of 192
records have completed engineering A assessments; 113 remain incomplete.
All 192 source digests and all 79 completed evidence chains pass
`20261019T014040Z-score-verification`. The per-file inventory and remaining gates
are in `evidence/quality/category_homology/resume-20261019/progress.json`.
New assessments cover the bounded counter (L3A), nine public hierarchy facades
and two coordinate aliases (L1A), and raw hashing (L2A). None inherits its
providers' mathematical grade. The additional Boolean checklist challenge
covers mixed flags without promoting raw declarations to mathematical laws.

A missed public rank replay panic was found after the earlier checkpoint:
the shared rational hasher normalized a zero-denominator candidate before
scalar admission. The failing regression and correction of the earlier provider
review remain in `resume-20261019/rank-replay-finding.json`. Replay now admits
canonical Q first. Raw matrix/vector/weight fingerprints and the legacy root
fingerprint encode undefined stored pairs without admitting them as Q.
Defined-value encodings and all existing tags remain unchanged. Rank is L5A
only under the new explicit admission-first assessment; the wider compatibility
root remains incomplete. No failed campaign is used as passing evidence.

The repaired rank replay catches nine designated faults. Final hash replay
catches 57 faults against independently assembled expected wire encodings;
BLAKE3 and BigInt storage remain trusted. Alias replay catches both wrong-kind
bindings with same-binary nominal type controls. Each final homology composition
run passes 99 tests before and after. Counter replay catches ten faults and
its checked Nat model has eight lemmas. The namespace and proof scopes are
explicit; none claims a whole-workspace or machine-checked Rust/MIR proof.

```powershell
python code/rust/quality/category_homology/run_hash_context_replay.py
python code/rust/quality/category_homology/run_alias_challenges.py
python code/rust/quality/category_homology/run_audit.py --scope counter --mutations --mutation-prefix BC
python code/rust/quality/category_homology/verify_current_scores.py
```

Every completed compiler invocation still removes its debug/tmp outputs,
including failures. Owned remaining build trees and copied executables are
removed at campaign completion; small source snapshots and receipts are retained.
The inactive registered-worktree cache cleanup is separately recorded in
`resume-20261019/registered-worktree-cleanup.json`. This goal remains open and
contracts remain pending.


The subsequent parameter-metadata checkpoint has 86 completed A records and
106 incomplete records. The seven additional L2A files retain their literal
level/bound/tag predicates and now return the existing typed InvalidShape
variant. Their 237 independent schema cases, constructor checks, 57 isolated
faults and seven-lemma parameter model cover the declared metadata scope.
The initial failed proof attempt remains excluded. The actual category suite
still passes all 459 tests before/after; all 107 nominal export faults are
replayed against the changed provider signatures, without awarding provider
mathematics to a facade. Four affected facade assessments explicitly review
that provider delta.

`20261019T015208Z-score-verification` checks every completed record and binds
all adjacent YAML digests as well as Rust digests. None changed during the
verification. `resume-20261019/progress.json` now records this checkpoint;
`cleanup-checkpoint-86.json` confirms zero remaining owned compiled outputs.
Replay the new narrow checks with:

```powershell
python code/rust/quality/category_homology/run_metadata_challenges.py --policy code/rust/quality/category_homology/parameter_boundaries.json
python code/rust/quality/category_homology/run_rank_proof.py --model parameters
```


The collection checkpoint has 94 completed A records and 98 incomplete records.
Eight more L2A inventory files preserve their label/component predicates and
now return typed InvalidShape refusals. The explicit source review maps all
39 public production methods. Their 1,116 independent cases check component
subsets, first/middle/last and multiple-invalid positions, label-first refusal,
raw serde transport and distinct constructor/setter values. The final campaign
kills all 100 designated faults and passes 43 namespace controls plus all 459
category tests before/after. No adjunction, order, naturality or lifting theorem
is inferred from these inventories.

The first collection build failed on a dependency compiler allocation before
subject tests. Its 100 candidates remain unrun in that receipt. The successful
retry uses one compiler job and batches of four; the resolution ledger binds
every retried candidate to the same SHA-256 bytes. Owned outputs are removed
after both failed and successful builds. Export checks replay all 107 faults
on the changed signatures and explicitly refresh the two affected facade
contexts. Metrics/export/metadata runners now accept an explicit --jobs bound.

`20261019T020311Z-score-verification` verifies all 94 completed assessments and
all 192 unchanged source/score digests. Current remaining gates are in
`resume-20261019/progress.json`; `cleanup-checkpoint-94.json` finds zero owned
compiled outputs. Replay the inventory checks with:

```powershell
python code/rust/quality/category_homology/run_metadata_challenges.py --policy code/rust/quality/category_homology/collection_boundaries.json --jobs 1 --batch-size 4
```
