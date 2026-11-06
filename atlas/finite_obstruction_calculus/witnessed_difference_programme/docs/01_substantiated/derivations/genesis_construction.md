# From literal `<>` to an executable chain complex

This is the first implementation increment of the Genesis construction within
WDP. It connects `omega_ooutwire_primitives` to WDP's existing execution and
homology code. The later sheaf, higher-identity, and quantum constructions will
extend this same recorded development.

The [ownership plan](../../../plans/genesis_crate_and_math_extraction.md)
names `omega_genesis` as the permanent primitive owner after the planned
rename. This WDP connection is temporary: its mathematical components will
move into their domain crates as their correspondences are established.

## The implemented starting point

`GenesisConstruction::pre_genesis()` has no recorded presentation and nothing
admitted. `from_literal_seed()` records exactly `Supply(Token("<>"))`. The
literal string survives in the history; the admitted state stays empty.
`AdmitDatum("<>")` is a different event, and would admit one datum.

The construction calls the existing primitive `admission::step`. It does not
replace its events, parse the two printed glyphs into endpoints, or introduce
another primitive engine. Each event also runs through WDP's existing
`PrimitiveRegime` under the deduplicating reading. The complete resulting data,
forms, instances, uniform rules, and separation requirements must agree before
the new prefix is returned. The original construction is unchanged on refusal.

WDP's occurrence reading remains a different model. A repeated token produces
one admitted datum in this construction, while its two admission occurrences
remain in the history.

## An explicit next construction

We choose the following interpretation of admitted forms and instances:

- a datum's admission index identifies a vertex;
- an arity-k form is available for (k-1)-dimensional simplices;
- an instance supplies the strictly increasing list of its vertex indices;
- every vertex and every face must have its own admitted instance.

This is a construction choice recorded here. It is not extracted from the
spelling of `<>` or from labels such as `vertex:3`. Uniform rules and separation
requirements require another interpretation and are refused by this particular
incidence reader. The retained primitive history still supports all six event
kinds and retains those fields.

**Finite construction result.** Let n be positive and let K be a finite family
of nonempty subsets of vertices 0 through n-1, containing every singleton and
closed under nonempty faces. This is the nonempty-simplex storage convention
for a finite abstract simplicial complex; the empty simplex is not an admitted
zero-arity instance. Choose n distinct opaque token labels. Starting with the
literal supply, admit those data, one form for each arity from 1 to the largest
simplex size, and one instance for each simplex, using its increasing vertex
list. Provided the
declared resource limits admit this construction, its incidence interpretation
is exactly K.

**Proof.** Deduplicating admission retains each chosen datum once and in order,
so its index is the intended vertex index. The arity-k form has index k-1.
Every proposed instance has the admitted arity and existing argument indices,
so admission succeeds. Distinct simplices give distinct instances. The reader
copies their argument indices, producing precisely the simplex lists of K.
The singleton and face checks succeed by the hypotheses. It adds no cells.
This is a written construction argument; it is not yet a Lean verification of
the Rust implementation.

The interpretation is not a replacement for the execution state. For example,
an unused admitted ternary form does not change the current complex, but does
change which instance may be admitted next. The engine therefore retains the
whole primitive state and history alongside the mathematical result.

## The first complete walk

The runnable example records these stages:

| Stage | Recorded operation | Computed result |
| --- | --- | --- |
| Pre-genesis | No events | No admitted data or forms |
| Literal root | Supply `<>` | Still no admitted data or forms |
| Data | Supply and admit `<a>`, `<ab>`, `<c>` | Three admission indices |
| Forms | Admit arities 1, 2, 3 | Available vertex, edge, and face forms |
| Vertices | Admit the three unary instances | Three explicit vertices |
| Cycle | Admit edges 01, 12, 02 | Rational Betti numbers (1, 1) |
| Filling | Admit the single instance 012 | Rational Betti numbers (1, 0, 0) |

The last step is an actual primitive `AdmitInst` event. With edge basis
(01, 02, 12), the signed boundary matrices are

$$
\partial_1=
\begin{pmatrix}-1&-1&0\\1&0&-1\\0&1&1\end{pmatrix},
\qquad
\partial_2=
\begin{pmatrix}1\\-1\\1\end{pmatrix}.
$$

Before the filling, the one-dimensional kernel of the first matrix is the
first homology. After the filling, it is exactly the image of the second
matrix. The native homology owner constructs the matrices, checks the boundary
law, and computes the rational ranks; the example does not return stored Betti
numbers. Verification replays the separately supplied history and recomputes
the full report, including operator entries.

This filling changes H1. It is recorded as a change of the mathematical object,
not as a repair preserving the old homology question. The prior cycle, its
history, and its result remain available.

## Replay and the categorical connection

The existing `GenerativeHistoryCompression.lean` constructs typed histories
from accepted transitions, with identity and associative composition.
`GenesisConstruction.lean` adds the converse: every accepted event-list replay
has a typed history with exactly that event list. It retains the literal
`Supply("<>")` as the first event even when supply is inert.

The new replay theorem also proves that a state/event interpretation commuting
with each partial step commutes with every finite replay, including refusal.
With an injective state interpretation it reflects the exact final state.
These results reuse the existing history model; they do not define another
Genesis state model.

The step-commutation premise has not been formally proved for these Rust
implementations. Runtime comparison checks every accepted prefix. The raw
primitive `Pair` fields are public, but canonical admission now rejects reversed,
diagonal and out-of-range pairs before the WDP correspondence check. The
regression test exercises values constructed without `Pair::new`. A full
correspondence proof still needs to cover the checked transition interface,
including both implementations' refusals.

## Run and check

From the repository root:

```sh
cargo run -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_wdp --example genesis_construction --locked
cargo test -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_wdp --test genesis_construction --locked
```

The example prints every actual event and both computed chain reports. Default
limits are 4,096 events, 512 incidence cells, and a conservative allowance of
262,144 matrix entries, checked as the square of the cell count before calling
the homology owner. Limits stay with a construction on continuation; exceeding
them is a resource refusal. The caller may supply different explicit limits.
These bound event count and matrix dimensions, not arbitrary token byte lengths
or a wall-clock deadline.

Focused controls cover the literal root, all six event kinds, duplicate-token
semantics, rejected admissions, malformed pairs, restart at every prefix,
renaming opaque tokens, missing faces, duplicate cells, forged operators and
Betti numbers, and execution limits. The
[validation receipt](../../manifests/genesis_construction_validation.json)
records 25 passing Rust tests, the executed example, and seven selected Lean
theorems under Lean 4.33.1, with only `propext` used by four of them. Those
Lean declarations compile from the two listed core-only sources; this is not
a build of the complete WDP formalization.

## Continuation within WDP

The next executable connection is to construct contexts, restriction maps,
and compatible local assignments from the same retained admissions, then use
the existing finite-presheaf owner. A parity cycle gives a first shared test of
local satisfiability, global failure, and an explicitly computed obstruction.
The existing exact Pauli contextuality implementation is a subsequent quantum
instance of that route. Typed path transport supplies the selected higher
identity work along the way.

Provisional choices belong in this construction record. An unfinished proof
can remain an explicit premise while engineering continues. A provisional
premise is not replaced by a success flag, and a missing implementation is not
reported as executed. This development supplement has not yet been integrated
into a rebuilt manuscript PDF or published archive.
