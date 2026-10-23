# Complete marked results and their carrier boundary

AuthorityEffect: None. This supplement advances GEN-WDP-O02/O03 for the
actual source-25 result relation and balance record. The five enlarged
obligations remain open at their full scopes. The source's filled triples
retain orientation and incidence; a balance verdict is an observation of
those triples, rather than an automatic condition on filling or editing.

## Retained source and meanings

The [input manifest](../manifests/marked_result_inputs.json) binds the fifteen
actual imported files from `H3V7N5QF` at revision
`5d9488324ce976817987bd83a28d901371cfc073`. Each existing pin retains its
path, byte count, SHA-256 and Git blob. The
[original-function replay](../scripts/verify_marked_result.py) checks that
the actual import closure is exactly that declared set, verifies regular
files and parents, and rehashes source and controls after execution.

`twentyfifth/state.py` declares the following choices.

| Source meaning | Preserved native meaning |
| --- | --- |
| FState carries unnamed natural assertion tables r/s and sorted unique filled triples | The existing checked `Source25State`; no quotient replaces its raw packet |
| C-O1 rotates a triple to its least term and retains its direction | A common writing transports all three endpoints; reversing the direction remains a different filling |
| `canonical_state` minimizes raw r, then raw s, then fillings | One shared permutation compares the complete tuple, retaining multiplicities |
| `result_mark` minimizes normal excess, then fillings | One shared permutation transports excess and fillings, then normalizes the transported excess |
| `align` chooses the first rewriting matching the target's fixed normal table and fillings | The result retains the original raw r/s, rather than replacing them with target or plain tables |
| `plain_state`, `swap25`, `nothing_with` retain fillings | Their native methods preserve the actual marked carrier |
| `balance_record` and `unbalanced` use oriented cycle sums in filling order | The adapter delegates arithmetic to the existing checked D_F/d0 owner |
| C-I1 identifies endpoints, drops degenerate fillings, and merges duplicates | The existing raw execution kernel applies precisely those source edits |

The generic math owners are
`linear_algebra::pair_table_canonical::canonical_pair_tables_with_decoration`
and the decorated canonicalization/alignment functions in
`linear_algebra::gauge_pair_table`. Their decoration callback transports
source data under the same permutation as the tables. The WDP adapter
supplies the source-specific triple transport. Unit-decoration wrappers
retain the earlier table-only APIs. Full n! is checked before callbacks or
orbit traversal; an insufficient budget refuses. That permutation bound
does not bound scalar bit length, matrix allocation or callback work.

## Written completeness and diagnostic descent

Put e=r-s and let N be source 23's fixed-root normalization, with root
potential zero and root loops retained. At a fixed writing the complete
pair is (N(e), F), where F is the ordered filling list. For every finite n,
including n=0, two such pairs agree exactly when their filling lists agree
and their excess tables differ by an integer gradient on the active
carrier. The proof subtracts their root potentials to obtain the gradient;
in the converse, any active endpoint implies n>0, so the root comparison is
available. Thus the empty case requires no nonexistent root element.

Under a permutation p, transport e and F together. Define the action on
normal tables by normalizing again after transport. The previous
[root-normalization proof](gauge_result_refinement.md) shows that inserting
an earlier normalization cannot change this result. Together with cyclic
normalization of each distinct-endpoint triple, these actions obey identity,
composition and inverse. Therefore two joint orbit minima agree iff some
single writing carries one fixed pair to the other. This is the written
finite-group proof of complete `result_mark`; minimizing the components
independently would use incompatible witnesses.

For an oriented filling t=(x,y,z), its diagnostic is
e(x,y)+e(y,z)+e(z,x). A gradient cancels around the cycle, and a cyclic
rotation preserves the sum. A common renaming carries the diagnostic to
the renamed triple. Consequently balance records descend through the
fixed-mark gradient relation and transport with a writing. Reverse
orientation need not have the same verdict for arbitrary directed tables.

`MarkedGaugeTransport.lean` proves the fixed-writing criterion, cyclic and
gradient diagnostic laws, normalization invariance, and the concrete source
step formulas below. Its nineteen selected declarations have a
[source-bound axiom receipt](../lean4/marked_gauge_transport_axioms.txt).
The receipt uses only propext and Quot.sound, with no admitted proofs.
The finite-group orbit proof, concrete storage, parsing and Python/Rust
program correspondence retain their separate written/differential scopes.

## Two component minima lose a protected incidence

On four terms place one r assertion on loop (0,0), with every other r/s
entry zero. In state A fill (0,1,2); in B fill (1,2,3). Their unmarked
tables are equal, and their filling-only orbits are equal. Both fillings
balance. But A's filled triangle contains the loop's vertex, and B's does
not. No common writing can change this incidence. Their joint result
marks and raw canonical states differ; alignment refuses.

This collision rules out reconstructing the joint mark from separate
table and filling minima. It also shows why balance truth alone cannot
replace the filled carrier. A second source counterexample has one r
assertion 0→1 on three terms: (0,1,2) has diagnostic 1, whereas (0,2,1)
has diagnostic 0. The order of traversal is protected source data.

## The actual carrier-changing edits do not descend

Begin with zero assertions on two terms. Raise term 0 once, producing
e(0,1)=1 and e(1,0)=-1. These raw states have the same result mark, with
no fillings. Apply the same enabled AddTerm operation to both. The new
term has zero incident assertions. The raised representative now has
cycle sum 1 around (0,1,2), while the other still has zero excess.
The first result is no longer a gradient, so even a common renaming cannot
identify the two new result classes. Filling (0,1,2) afterward exposes
different balance records.

For identification, begin with zero assertions on four terms and fillings
(0,2,3), (1,2,3). Raise term 2 once. The result mark is unchanged and both
fillings still balance. Identify terms 0 and 1 in each raw representative.
C-I1 merges the fillings to (0,1,2). In the raised representative, the new
cycle entries are -2, 1, 0, hence diagnostic -1; the zero representative
still has diagnostic 0. Both source changes are enabled. Their new joint
marks and balance records differ.

The Lean declarations bind AddTerm and this identification to the existing
`Source25PairTransport.sourceStep`, prove the nonzero diagnostics, and
exclude gradients on the target carrier. Identification uses raw endpoint
fiber sums, rather than the pullback operation from the preceding proof.
The existing matrix/fiber theorem still applies to that source operation.
These witnesses refute a representative-independent transition on result
marks for the declared edits. They do not refute every restricted edit or
select a replacement semantics. Ordered runs continue to require equality
of the complete raw intermediate state.

## Original/native evidence and replay

The [retained original receipt](../evidence/marked_result_receipt.json) and
`omega_wdp/tests/marked_result_oracle.rs` agree on a streamed ordered
comparison of:

- 261 states with binary r/s on carriers of size at most two;
- 2,048 three-term states: every binary r table, zero s, and all four
  subsets of the two oriented triples;
- five declared extras, including the four-term incidence/identification
  examples and arbitrary-precision inputs with 141-bit counts;
- 17,489 bulk raisings with counts 0 or 1, all 12,907 carrier permutations,
  and 2,314 first-witness alignments.

Each base observation retains raw canonical state, complete mark, plain
state, swapped state, balance record, unbalanced fillings and nothing-with
state. Every raising and rewriting retains its raw output, complete mark
and balance record. Alignment retains both the target and returned original
raw rewriting. The ordered stream SHA-256 is
`1d95c8f4ffefce7af51a325b98cc1ee6cfd5dfdd7cc0757dccdf2c09fd74a092`.
The four independently retained counterexamples use actual original
functions, including the enabled source carrier edits.

The eleven new native cases comprise three generic decoration-owner cases,
six marked-adapter cases and two complete oracle comparisons. Six control
mutation cases exercise same-byte linked files/parents, nonregular controls
and post-execution source drift. Earlier raw table, gauge, source-25 edit
and admission comparisons are separate regression evidence.

From this package, use a fresh external output path:

```powershell
py -3.12 scripts/verify_marked_result.py --source-root <pinned-source-root> --output <fresh-external-output.json>
py -3.12 scripts/verify_finite_derivations.py --lean <lean-4.33.1-binary>
```

From the repository root:

```powershell
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p linear_algebra --test decorated_pair_orbits -p omega_wdp --test genesis_marked_result --test marked_result_oracle --target-dir <shared-cargo-target>
```

The original corpus is finite program evidence; the table statements and
explicit source-step countermodels have their stated formal scopes. This
does not attest a full workspace suite, hosted CI, operational reconstruction,
institutional standing, publication or completion of all five obligations.
