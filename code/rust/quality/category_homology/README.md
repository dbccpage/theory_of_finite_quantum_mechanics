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


The finite-literal-set checkpoint has 95 completed A records and 97 incomplete
records. FiniteSet remains raw transport; ValidatedFiniteSet owns a checked,
immutable literal set. The new typed FiniteSetError preserves exact indices,
declared/actual counts and prior diagnostic text, including serde refusal.
The L3A assessment binds 16,400 independent prefix/wire cases, 20 valid faults,
constructor/observer/clone isolation and formatter-error checks. Its eight-lemma
model proves scan distinctness/nonblank acceptance, optional cardinality,
first entry refusal, unchanged raw data and admitted invariants. Unicode
whitespace and BTreeSet representation correspondence remain explicitly
reviewed library/source boundaries; no normalization or Rust/MIR proof follows.

The invalid initial fault recipe and failed initial proof remain unsuccessful
evidence. Final namespace controls pass seven tests before/after; the original
category suite still passes 459 tests. All 107 export faults replay on the new
provider and the foundation facade context is explicitly reviewed.
`20261019T021740Z-score-verification` checks all 95 completed records and every
current source/score digest; `cleanup-checkpoint-95.json` finds zero compiled
outputs. Current remaining gates stay in `resume-20261019/progress.json`.

```powershell
python code/rust/quality/category_homology/run_metadata_challenges.py --policy code/rust/quality/category_homology/finite_set_boundary.json --jobs 1
python code/rust/quality/category_homology/run_rank_proof.py --model finite-set
```


The flat-inventory checkpoint has 107 completed A records and 85 incomplete
records. Twelve more L2A modules retain their raw metadata/shape semantics and
now return typed InvalidShape failures. Their explicit source review maps all
42 public production methods. The current campaign passes 1,138 schema cases,
raw constructor/flag/list-binding checks, 60 namespace controls, 459 category
tests before/after and all 156 faults. Four affected facade contexts are
explicitly reviewed and all 107 export faults replay successfully.

The opposite-record helper additionally passes all 125 literal boundary/name
combinations, original-order checks and double reversal. A checked four-lemma
model proves literal component/list involution, length and name/order
preservation; it does not prove an opposite category. The initial failed
length-map proof remains excluded. Raw Set::cardinality is explicitly an
inventory count including repetitions, not distinct-set admission.

`20261019T023336Z-score-verification` checks every completed record and all
192 current source/score digests without drift. Progress/remaining gates stay
in `resume-20261019/progress.json`; `cleanup-checkpoint-107.json` finds zero
owned compiled outputs. The inactive shared checkout debug cache had regrown
to about 6.1 GiB: after native path/Cargo-marker/tracked-file and process checks,
only that cache was removed. The separate second cleanup receipt records the
recovered space; all source and dirty work remain untouched.

```powershell
python code/rust/quality/category_homology/run_metadata_challenges.py --policy code/rust/quality/category_homology/flat_inventory_boundaries.json --jobs 1 --batch-size 4
python code/rust/quality/category_homology/run_rank_proof.py --model literal-reversal
```


The nested-inventory checkpoint has 115 completed A records and 77 incomplete
records. All 108 hierarchical category files now have honest per-file A scores.
Eight raw schema modules are L2A: typed shape errors preserve rejection order
and data, while the discrete shell explicitly checks endomorphisms only.
Category validation is split into cohesive private tag checks. Cone context
preserves non-shape error variants. These records claim no category laws,
commuting cones or universal properties.

The native replay passes 1,593 independent schema/context cases, 49 namespace
controls, all 118 faults and 459 canonical category tests before/after. The
nine-lemma shape model and all 107 export faults pass. The initial missing
snapshot test dependency failure is retained; its correction ledger binds all
118 identical candidate byte strings to their successful rerun. Explicit
provider-delta reviews refresh two facades and the unchanged Arrow/Opposite
callers. `20261019T031207Z-score-verification` rechecks all completed evidence
and every current source/score digest without drift. Cleanup checkpoint 115
finds zero owned compiled outputs; contracts remain pending.


Root-record checkpoint: 125 completed A assessments, 67 incomplete.
SkillMorphism composition previously admitted matching endpoint labels across
different categories despite its documented guard. The retained native pre-fix
regression fails; the repaired conjunction rejects foreign category tags.
Other bridge descriptions now accurately identify declarations and count/shape
checks, with no functor, HoTT, authority, model or registry certification. The
local ten-row contract label table is L1A; nine records/interfaces are L2A.

The native ten-file replay passes 1,201 independent boundary/table combinations,
all 74 designated valid faults, positive namespace controls and 459 canonical
category tests before/after. Eight guard/report/count/mass lemmas check cleanly;
the two initial failed proof attempts remain excluded. Raw rational product
transport and noncanonical positive density mass are explicitly distinguished
from canonical rational admission. Full source/entry-point, dependency and
consumer reviews bind the advertised scope. The latest score verifier
`20261019T032434Z-score-verification` rechecks every completed record and all
192 unchanged source/score digests; cleanup checkpoint 125 finds no owned
compiled outputs. Contracts and the broad L5A goal remain unfinished.


Homology protocol checkpoint: 127 completed A records and 65 incomplete.
All fourteen nominal ID types, checked serde/basis admission, 65,540 degree
values against widened i64 shifts, private display parser cases and all 37
homology error variants receive explicit source/runtime reviews. Native final
replay kills all 59 faults, with 12 controls and 99 canonical homology tests
before/after. The kind checker formerly had CCN 22; cohesive 6/8-kind helpers
preserve its exact 14-call order and reduce the main CCN to 10. Authored macro
methods are explicitly mapped; standard serde/thiserror derive protocols are
trusted runtime dependencies, not falsely measured as zero expanded code.
Eight degree/nonzero lemmas check cleanly. Initial failed proof and encoding
attempts remain excluded. Three affected caller context deltas preserve their
actual earlier primary mathematical/mutation evidence.

Review also establishes three incomplete G2 E records: chain/cochain dim and
Simplex::face narrow the rejected usize index 4294967296 to InvalidDegree(0).
Two verbatim dim-method minimal adapters reproduce the error; the face finding
is a source trace using the same compiled cast behavior, not a claimed whole
simplicial execution. A whole-module typed repair remains next. These known
defects stay visible while other gates remain null. The full 127-record check
is 20261019T034253Z-score-verification; the explicit incremental receipt adds
only the final incomplete face finding and checks all three partial records.
All completed source/score bytes remain identical. Cleanup checkpoint 127
finds zero owned compiled outputs; the concurrent active shared cache is held.


Exact-index/differential checkpoint: 129 completed A assessments and 63
incomplete. A new full-index error preserves rejected usize payloads while
retaining the old signed variant when representable. Both complex dim methods
and simplicial index refusals use that helper. All three original narrowing
findings are resolved on the actual modules, including the exact 4294967296
input in the separately bound auxiliary native replay. The old E witnesses
remain historical evidence. Standalone orientation now retains Boolean parity
instead of summing a potentially overflowing machine-sized inversion total.
Constructor docs name the actual ShapeMismatch/canonical-Q failures, and
provenance text is explicitly an unchecked source label after nonblank admission.

Final full native campaign 040851Z kills all 74 designated valid faults, passes
40 namespace controls and the 99 original homology tests before/after. Initial
040309Z retains one survived direct-face sign fault; added valid direct-face
checks close that blind spot. The candidate/harness revisions are separately
bound, not falsely called identical bytes. Auxiliary 041548Z repeats the exact
original index case and controls on actual peers. Its primary_eligible=false
marker is enforced by the score writer, with a no-write refusal test.

Thirteen DegreeRepair lemmas check full-index/dimension preservation and
Boolean inversion parity; eight TwoStepComplex lemmas check exact-Q admission,
data preservation, zero differential square, image-as-cycles and typed guard
propagation. The first two-step run exhausted the Lean memory cap; smaller
actual imports check cleanly without increasing the cap or altering Mathlib.
Source/representation/runtime correspondence remains explicitly reviewed,
not claimed Rust/MIR extraction. Error protocol is L2A; the two finite complex
files are L4A. Relevant prior rank/hash/alias mutation/model receipts retain
their original providers, with explicit current code/data deltas and fresh
canonical native composition evidence.

Simplicial remains incomplete: its current declared challenge is G4 A, but
close_faces clones a generated face before duplicate detection. A concrete
overlapping-edge trace establishes an avoidable allocation inside the loop,
so G5 is B. G1/G2/G3 remain unassessed pending the full mathematical/refusal
audit; the index/parity models are not a general simplicial/Betti theorem.
The prior finite_report_descent metric E ceiling also remains visible.

20261019T043455Z-score-verification rechecks all 129 completed assessments
and every current source/score digest. The partial simplicial record is also
explicitly rechecked. Cleanup checkpoint 129 finds zero owned debug/tmp or
compiled outputs. An inactive registered Bell cache was separately verified
and removed; active shared builds were preserved. Exact small source
snapshots remain for pinned receipts. Contracts and the all-files goal stay
unfinished.

Simplicial checkpoint: 130 completed A assessments and 62 incomplete out of
192. Simplicial is L4A; capability is not raised just because it now uses the
existing L5 rank architecture. Face closure checks duplicate keys by reference
and moves fresh keys; Betti computes each differential rank once, independently
checks the split-map certificate, and carries that rank to the next degree.
Typed rank failures now propagate directly. Public signatures, wire formats,
mathematical input bounds and the other 43 production bodies are unchanged.

Final native 20261019T051112Z detects all 21 designated valid faults, passes the
full control (including the 16-vertex Boolean lattice and distinct-face cap),
and passes 99 original homology tests before/after. Initial 045558Z retains
18 detected faults and one inconclusive factorial traversal timeout. Its old
hash-at-end runner discrepancy is recorded against its retained start snapshot;
that initial run is excluded from grading. Dispatch now uses a small decisive
fixture for the no-insertion fault. Candidate/harness revisions are separately
bound, and no identical-byte replay is claimed. The timeout fallback was also
checked against an owned direct child; future summaries bind their start
snapshot and report live source drift separately.

The 45-function source/body/failure/consumer review connects 15 worklist/erasure
lemmas, five signed-face/indicator-matrix lemmas and three rational homology
lemmas to concrete canonical bases and independently certified ranks. Existing
index/parity and rank-certificate models retain their actual scopes. Two Betti
proof attempts exceeded 1024 MiB; the final explicit 1536 MiB check succeeds on
a host measured to have about 5.4 GiB free RAM, without custom axioms or unfinished
proofs. Failed and warning receipts remain historical. Representation/runtime
correspondence is reviewed source evidence, not a Rust/MIR extraction claim.
The external consumer attribution here was corrected at checkpoint 134:
same-named omega_homology imports bind a separate package. This local
assessment establishes no external caller panic or application grade.

20261019T052226Z-score-verification revalidates all 130 completed assessments,
all current source/score digests and 22 receipt groups. Calibrated current source
metrics place all 45 simplicial functions within A ceilings. The prior allocation
ceiling is resolved; finite_report_descent's separate metric E ceiling remains
visible. Cleanup checkpoint 130 finds zero owned debug/tmp or compiled outputs.
Exact source snapshots remain for receipt custody. Contracts and the all-files
goal remain unfinished; the draft PR is a partial, reviewable checkpoint.

Current score verification snapshots its exact writer. Refreshing an unchanged
source/primary/metric now creates a distinct record-digest batch when needed,
preserving the published historical manifest byte-for-byte. The actual rank
refresh preservation check is recorded in score-manifest-custody-repair.json.

Storage/admission checkpoint: 134 completed A assessments and 58 incomplete.
All 13 completed homology files retain honest capabilities. Four new records
are exact_scalar L3A, witness and carrier_manifest L2A, and Carrier L5A. The
scalar/witness source change is full-line documentation only: every non-comment
line, production declaration and algorithm remains unchanged. Stored witness
annotations and internal canonical-input preconditions are now explicit.
Seven dependent records retain their own original primary/metrics/proof
receipts, with a separate complete source delta and current composition replay.

Native 20261019T053739Z detects all 44 designated valid faults: scalar 9,
witness 12, carrier 11 and manifest 12. The 99 original local homology tests
pass before/after, as do four controls; the Carrier control runs 99 native
context tests plus two independent fixtures. Initial 053100Z failed harness
compilation on copied Carrier/canonical-manifest nominal types, so all 44
faults remain unrun there. The corrected harness copies the complete native
homology context under a reversible uniform crate-path rename, preserving the
nominal cycle without substituting providers, removing methods or widening
visibility. An independent audit restores every unmutated peer text exactly
in all 12 contexts. Thirty-three candidate byte strings match the initial
copies; the eleven renamed Carrier candidates differ and are labeled so.

Nine ScalarAdmission declarations connect positive/coprime stored integer
pairs with Rat, preserve exact fields, reject invalid domains at the first
index and model literal receipt transport only. Two CarrierDimensions
statements check quotient dimension and subtraction bounds; existing two-step,
homology and split-rank models supply the other declared algebraic premises.
Failed proof attempts remain retained and excluded. Current calibrated metrics
cover all 32 production functions within A ceilings. G1/G2/G3 reviews map every
entry, private field and failure branch to actual local consumers and runtime
trust; no Rust/MIR, allocator-totality, hash-authentication or physical claim.

Package custody distinguishes the local pub mod homology from the separate
omega_homology dependency. A preceding simplicial consumer note incorrectly
attributed the local 16-vertex cap to an external GR import; that external panic
attribution is withdrawn in the current review. Broad same-name searches are
locators until package identity is established, not proof of a consumer edge.
No external package/application grade is inherited from these local receipts.

20261019T054854Z-score-verification passes all 134 completed source-bound
assessments, all current source/score digests and 23 receipt groups. The first
134 verification encountered an immutable-ledger grouping refusal: two refreshed
records and a third unchanged record occupied different preserved batches.
The current checker verifies each selected digest against the same primary/
metric ledger without inventing a combined execution. The actual three-record
regression passes with every historical manifest byte preserved. Cleanup
checkpoint 134 finds zero owned debug/tmp or compiled outputs. An inactive
registered cache cleanup also recovered 13,981,419,646 bytes after verifying
no active compiler. Exact small source snapshots remain for receipt custody;
contracts and the full all-files goal remain unfinished.

Vector/map checkpoint: 137 completed A assessments and 55 incomplete. Graded
vector, boundary and coboundary are L3A. Ten unchanged-own-source dependent
records retain their original primary/metric receipts with an explicit current
provider transformation argument. Homology has 16 completed files and three
incomplete; category theory has 121 completed and 52 incomplete.

All raw public/wire/scalar gates, compatibility/refusal order, signatures and
mathematical domains are preserved. An internal canonical-result constructor
is justified at all seven producer sites: raw admission, normalized Q zero,
addition/subtraction/multiplication and the two admitted matrix-vector folds.
Removing redundant output GCD scans eliminates the pinned large-digit heap-copy
path. This is source/cost evidence, not an allocation benchmark. Wire is
explicitly untagged with kind selected statically; map matrices preserve caller
family labels and do not own/authenticate a family or certify a whole complex.

Native 20261019T060338Z independently detects all 46 designated valid faults,
passes three controls with eight tests, and passes 99 original local homology
tests before/after. Oracles check 1250 vector pairs and 6250 scalar cases over
both kinds, 2025 integer matrix-vector cases per map, rectangular/zero shapes,
raw/wire/degree/length failures and >200-bit results. VectorMaps checks 15 exact
context/pointwise/dot-sum/linear statements; its initial notation parse failure
is retained and excluded. The thirty-function source/data/producer audit and
current calibrated metrics fit A ceilings. Canonical Q/backend/index/allocator
trust remains explicit; no Rust/MIR, basis authentication or A+ claim.

20261019T061817Z-score-verification passes all 137 completed assessments, all
current source/score digests and 24 receipt groups. Every historical score batch
is preserved; current groups may draw unchanged and refreshed records from
separate immutable batches. Cleanup checkpoint 137 finds no owned debug/tmp or
compiled output. Small exact source snapshots remain for evidence custody.
The full goal and contracts remain unfinished, and the PR remains draft.

Carrier facade checkpoint: 139 completed A assessments and 53 incomplete.
Root and directed-graph carrier facades are L4A; homology has 18 completed
files and one incomplete challenge file. Category theory remains 121/52.
Fourteen unchanged-own-source dependent records retain their original primary
and metric receipts with an explicit current facade preservation argument.

Root serialization now borrows matrices and weights instead of cloning the
whole admitted carrier/certificates and then cloning its buffers again. Legacy
fingerprint framing, field order, Serde CarrierWire/ExactMatrix/Hash256 names,
hash-first deserialization and core admission are preserved. The graph domain
explicitly allows opposite directed edges and repeated triangle rows while
refusing duplicate directed pairs and repeated vertices inside a triangle.
Dense initialization and exact law/rank costs remain separate from table work.
This is source-cost evidence, not an allocation benchmark.

Native 20261019T064912Z detects all 40 designated valid faults (22 root,
18 graph), with no unresolved outcomes, and passes all 99 original local tests
before/after plus positive controls. Initial 20261019T064602Z caught 39/40:
equal outer dimensions hid a serialized C2/C0 substitution. An independent
unequal-dimension zero-area wire case detects it in the final campaign; the
initial survivor remains recorded. GraphIncidence checks nine finite incidence,
sparse-row and signed-cancellation statements without warnings or unfinished
axioms. Existing core admission, canonical scalar, rank and quotient proofs
retain their precise statements and separate Rust correspondence review.
Fresh metrics and all 35 explicit function/data/derive obligations fit A.

20261019T065405Z-score-verification passes all 139 completed assessments,
all current source/score digests and 25 receipt groups. Cleanup checkpoint 139
finds zero owned debug/tmp/compiled outputs. Exact small source snapshots remain
for receipt custody. Contracts and the full goal remain unfinished; PR is draft.
