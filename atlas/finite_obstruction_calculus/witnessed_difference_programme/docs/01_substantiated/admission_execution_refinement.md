# Source-specific admission execution and the COUNT minimum

AuthorityEffect: None. This supplement covers the unnamed integer states of
H3V7N5QF seeds 9, 15 and 16 at revision
`5d9488324ce976817987bd83a28d901371cfc073`. It completes the correspondence
below for canonical enabled descriptions in that declared domain. The other
Genesis systems and the five enlarged programme obligations remain open.

## Two meanings of admission

Seed 15 chooses C-A1: admission is separate result data. Its state contains
terms and nonnegative r/s multiplicities. Reaching an outcome records false;
admitting records true without adding an assertion or selecting r or s.
The native `Source9State` and `Source15Admission` keep that distinction.

The source also retains the unchosen C-A2 `Tagged` reading. Its actual
`tagged_admit` preserves the raw assertion state and is idempotent. Its
`tagged_perform` executes a ninth-state change, jointly canonicalizes r and s
under one vertex permutation, then resets admission to false. The native
`Source15Tagged` follows those functions. In particular, admission does not
canonicalize the state, and reaching may rename the coordinates of later
events. The source function accepts admission of the empty tagged beginning;
the native function does too. An extra reached-state guard would change it.

Seed 16 chooses C-R1, COUNT. Its state additionally contains an n-by-n
nonnegative leftover table L. An unadmitted leftover is neither an r nor an
s assertion. Admitting L(x,y) consumes one leftover and adds one assertion
in the chosen relation. This remains the source's fourth kind of change,
assertion addition; its `admits` flag distinguishes it from direct addition.
The separate native enum constructor preserves that distinction, without
claiming a fifth source kind. `Source16State` retains all three tables.

## Representation and all enabled operations

The representation maps source vertex i to `t{i}` and each integer tuple to
the same row-major BigInt table. It is a bijection on finite unnamed states
with well-formed nonnegative tables. It includes loops and independent
reverse arcs. Source descriptors with invalid fields, names or untyped Python
aliases are outside this domain. The native ninth-state constructor refuses
filled triples; these are not fields of this source regime.

For every state in the domain, the following checked cases preserve and
reflect enablement, exact outputs and the declared addition prices:

| Operation | Assertion state | COUNT record | Price (terms, assertions) |
| --- | --- | --- | --- |
| Add term | Zero-extend r and s | Zero-extend L | (1,0) |
| Direct assertion addition | Increase the selected r/s entry | Unchanged | (0,1) |
| Remove assertion | Require a positive selected entry and decrease it | Increase L at the same pair | (0,0) |
| Admit leftover | Increase the selected r/s entry | Require a positive L entry and decrease it | (0,1) |
| Identify x<y | Push r and s over the endpoint fibers | Push L over the same fibers | (0,0) |

Identification uses q(y)=x and q(k)=k-[k>y] for k≠y. The matrix owner computes
P M Pᵀ. The universal [pair-transport proof](source_execution_refinement.md)
identifies that formula with the source's fiber sums for each of the three
tables. Direct operations change exactly one count; term addition introduces
only zero coordinates. Thus the table above proves the raw step
correspondence for every domain state, not only the finite replay corpus.

The enabled list has identifications, occupied removals in r then s, a term,
all direct additions in r then s, and admissions in r then s. Occupancy lists
each pair once, independently of its multiplicity. Its length is
C(n,2)+occupied(r)+occupied(s)+1+2n²+2occupied(L). The native list retains this
order. Reading `Admit` as a direct addition would lose its enabling condition
and record consumption, despite the same assertion output and price.

The source retains SET and DROP as unchosen readings. SET suppresses the
extra record on removal when that pair is already occupied; identification
still sums counts and can produce L(x,y)>1. DROP clears every leftover
incident to either merged term before identification. Native execution
retains both behaviors; it does not coerce SET records to Boolean values.
The COUNT mass and minimum laws below are not promoted to those readings.

For each fixed reading, induction on a finite legal event word now carries
the step correspondence to every raw intermediate, ordered occurrence,
final state and accumulated addition price. `Source16Run::then` requires
the same reading and the complete intermediate state, including L. A cycle
can return to the same state with additional paid occurrences. Forgetting
L can preserve r/s while removing future enabled admissions. Mixed-reading
histories and a quotient-level transport theorem are separate obligations.

## Joint canonical writing

The source's least writing minimizes the concatenated row-major tuples
(r,s), or (r,s,L), over one common vertex permutation. Independent minima
of the tables need not be one rewriting of a state: for n=2, opposing
diagonal r and s entries cannot both become the last diagonal entry.

`linear_algebra::pair_table_canonical` owns this operation. It uses the
kernel's exact permutation enumerator, applies the common permutation
through matrix transport and retains the least tuple and its witness. Since
every permutation is examined, its result is exactly the source minimum;
ties retain the first lexical witness. This argument holds at every finite
carrier size where the native search is admitted. The n! bound is checked
before enumeration. Insufficient fuel returns a typed resource refusal,
never a partial minimum. The empty carrier has one permutation. Seed 16's
raw `perform16` does not canonicalize; `canonical16` is a separate operation.

## Exact global COUNT minimum on the declared domain

Write R=Σr, S=Σs, L=Σleftovers and P=n+R+S+2L. Term addition, direct assertion
addition and removal increase P by one. Admission and identification
decrease it by one. From the empty state, every m-change run therefore has
P≤m. This is a universal lower bound on legal COUNT runs.

For any valid target tables, add n terms. For each ordered pair (x,y), add
r(x,y)+L(x,y) copies in r, add s(x,y) copies in s, then remove L(x,y) copies
of r. Every removal is enabled: before the j-th removal its r count is
r(x,y)+L(x,y)-j>0. Counts on other pairs remain unchanged. The final tables
are exactly the target, and the length is
n+Σ(r+s)+2ΣL=P. The lower bound is attained. This proves the global minimum
change count for every declared COUNT state, including loops and arbitrary
integer multiplicities.

Its addition price is (n,R+S+L). To see that these coordinates are also
minimal, COUNT mass R+S+L increases only under direct assertion addition;
removal, admission and identification preserve it. Every run's paid
assertion count is target mass plus its number of admissions. Its paid term
count is target n plus its number of identifications. The construction uses
neither admissions nor identifications and attains both lower bounds. Change
length and addition price remain distinct quantities.

`Source16CountRecipe` stores this construction as counted blocks. A target
with 2^140 copies remains compact; materializing its word requires an
explicit whole-word limit and refuses before allocation if that limit is
too small. The mathematical minimum does not imply practical enumeration.

[`AdmissionCount.lean`](../lean4/WitnessedDifference/AdmissionCount.lean)
checks twelve selected declarations: the COUNT aggregate step laws, all-run
lower bound, mass monotonicity, construction and exact aggregate minimum.
The cellwise argument above supplies realization on valid pair tables.
Lean does not check Python/Rust storage, pair predicates, canonicalization
or the separate addition-price argument. The source-bound
[axiom receipt](../lean4/admission_count_axioms.txt) lists propext and
Quot.sound and no admitted proofs.

## Independent finite execution evidence

The [17 dependency pins](../manifests/admission_execution_inputs.json) and
[original-function verifier](../scripts/verify_admission_execution.py) retain
their own custody, separate from the unchanged older 24-input manifest.
The [receipt](../evidence/admission_execution_receipt.json) binds:

- 528 seed-15 tagged inputs and 7,356 transitions: every binary r/s table
  on zero, one and two terms with both admission flags, plus three larger
  states, including 2^140 counts;
- 12,327 seed-16 state/readings and 221,724 transitions: every binary r/s/L
  table on zero, one and two terms, under COUNT, SET and DROP, plus four
  larger states;
- complete raw outputs, joint canonical forms, enabled order, sizes,
  potentials, masses, diagonal masses and addition prices;
- a tagged history, five record histories, reading countermodels and an
  explicit future-admission distinction after record forgetting.

Native tests reproduce both complete stream digests from those inputs.
They also realize all 4,105 binary COUNT targets with their compact minimum
recipes and check every prefix split of each retained record history.
All imported original modules are bound by regular-file size, SHA-256 and
Git-blob identity. Source and control bytes are rechecked after execution.
Six selected mutation tests exercise regular-file, linked-parent and
post-execution substitution refusals.

These checks support finite concrete-program comparison. They do not turn
the written universal correspondence or aggregate proof into formal
verification of either executable, close all-source refinement, or create
institutional standing, jurisdiction, appeal or human authorization.

From this paper directory, with the pinned dependency closure available:

```text
python scripts/verify_admission_execution.py --source-root /path/to/source_snapshots --output /path/to/new_receipt.json
```

The verifier refuses an existing output path. Compare its bytes with the
retained receipt after replay. From the repository, native checks use the
tracked workspace lockfile:

```bash
cargo test --offline --locked --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_wdp --test genesis_admission_execution --test admission_execution_oracle
cargo test --offline --locked --manifest-path omega_engine/crates_rs/Cargo.toml -p linear_algebra --test pair_table_canonical
```
