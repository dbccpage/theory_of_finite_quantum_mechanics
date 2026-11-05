# Fixed-carrier Genesis Ongoing bridge

This is an external interpretation of the independently derived source, not a modification of its blind derivation. The input repository `/workspace/H3V7N5QF` remains read-only. The implemented scope is the chosen fixed-writing, fixed-carrier interpretation of derivations 23 and 25. It preserves every one of the n² ordered pairs, including loops and independent reverse arcs, actual nonnegative integer multiplicities in both relations, and the declared marked oriented triples. It does not merge the different seeds into one cumulative axiom list.

## Source bindings

The twenty-third seed (`prompt/twentythird/seed_prompt.md`, lines 3–11) declares two relations with multiplicities, empty initial data, four kinds of change, cancellation of simultaneous r/s assertions as sameness, and raising. The source's `paper/twentythird/paper.md`, D1 at line 238, derives sameness as excess tables differing by g(x)-g(y), up to one rewriting; D2 at line 263 establishes the loop, two-way and triangle invariants. `code/twentythird/state.py`, lines 95–118, explicitly forms e=M_r-M_s and performs raising; `normal_table` at line 137 fixes g(0)=0. Source formal names include `gen3_iff_same3`, `Same3.loop`, `Same3.twoWay`, `Same3.around`, and `same3_nothing_iff`.

The twenty-fifth seed (`prompt/twentyfifth/seed_prompt.md`, line 7) additionally declares filling three different terms and the balance record. The operational meaning of a fill is chosen C-F1, cyclic orientation is chosen C-O1, and identification's treatment of marks is chosen C-I1; alternatives remain recorded in `paper/twentyfifth/claim_ledger.md`. `code/twentyfifth/state.py`, lines 118–129, validates the source FState marks; lines 208–218 add a mark without modifying assertions or requiring balance. `paper/twentyfifth/paper.md`, D1 at line 275, proves balance descends to source sameness (`Same25.balanced_iff`); D4/D5 at lines 329/344 distinguish told from unseen discrepancies. D6 at line 364 supplies the blind three-term witness; D7 at line 394 states the conditional rank criterion. These are the actual statements used here, rather than an inference that marking a face makes it balance.

## Native interface and delegation

`omega_wdp::genesis_ongoing_adapter::GenesisOngoingPacket` contains ordered term labels, row-major n² BigInt tables r and s, and sorted, unique, canonically cyclic `MarkedTriple` records. Validation refuses malformed lengths, negative multiplicities, missing/repeated vertices, noncanonical/duplicate marks, and duplicate or empty labels. The zero-term source beginning is supported: its tables and marks are empty, and the native matrix owner represents the corresponding empty maps.

`GenesisOngoingAdapter::try_new` constructs the actual rational matrices

- d0: Q^n -> Q^(n²), with (d0 g)(x,y)=g(x)-g(y); diagonal rows are zero;
- D_F: Q^(n²) -> Q^|F|, with (D_F e)(x,y,z)=e(x,y)+e(y,z)+e(z,x).

Their allocation, shape validation and products are owned by `linear_algebra::BasicMatrix` and `semiring_product`. `omega_functional::LinearObserverPresentation::try_new(D_F,d0)` independently checks every entry of D_F d0 is zero before accepting the presentation. No elimination, quotient solver or graph construction is duplicated in WDP. The source's integer multiplicities and integer excess remain retained separately; rational matrices provide their exact symbolic realization.

`receipt()` returns actual excess, diagnostic values and per-mark balance flags. `repair(g)` delegates the d0 product to the matrix owner and returns e+d0g with its independently calculated diagnostics. It is a gauge-equivalent excess calculation; it neither executes a single seed change nor fabricates new r/s multiplicity histories. Both receipt types bind the complete actual source packet, and independently regenerate their computations during `verify_against`. A pair simultaneously added to r and s leaves e unchanged, but still changes the raw-source receipt binding.

`repair_equivalence(other)` is a complete constructive integer-potential test for two packets with exactly the same ordered labels and marked triples. It chooses g(0)=0 and g(x)=e_other(x,0)-e_self(x,0) for x≠0, delegates the actual d0 product, and checks all n² coordinates. It returns Some(g) exactly when the two excess tables differ by an integer repair; None is an actual all-pair obstruction. It does not merely compare marked diagnostic rows. The fixed-writing restriction deliberately omits renaming, adding terms, identifying terms or changing marks. A changed carrier/mark context receives a typed refusal.

## Mathematical guarantees

**Diagnostic descent.** For every marked triple of distinct terms,
D_F d0g = (g(x)-g(y))+(g(y)-g(z))+(g(z)-g(x))=0.
Consequently D_F(e+d0g)=D_F e, including for unbalanced triples. No antisymmetry premise on e is needed.

**Exact repair test.** If delta=d0h, subtract the constant h(0) from all h values. Then h(0)=0 and h(x)=delta(x,0), so the returned candidate is forced. Checking d0h=delta therefore proves sufficiency and necessity. For the empty carrier both tables are empty and the unique empty potential is returned. The test allows common r/s assertion pairs to differ because source sameness explicitly cancels those pairs.

**Faithful rationalization of integer repair equality.** For integer tables delta, if delta=d0g for rational g, set h(0)=0 and h(x)=g(x)-g(0)=delta(x,0) for x≠0. Every h(x) is integer, and d0h=d0g=delta. Thus passing from integer matrices to rational matrices identifies no extra integer source tables by repairs. This argument concerns equality of fixed-carrier classes. It does not assert that integer shortest-change cost equals an arbitrary continuous optimization objective, that every rational defect has a source integer realization, or that a source norm/physical calibration has been supplied.

**Quotient versus closure.** The repair quotient is Q=C1/im(d0). The marked diagnostic descends on all Q because D_F d0=0. H1 would instead be ker(D_F)/im(d0) under a separately declared cochain-complex interpretation. A general unbalanced source table lies outside that kernel. Accordingly the adapter exposes the diagnostic presentation without labelling Q as H1 or declaring every source result closed.

## Countermodels and boundary restrictions

The loop excess e(0,0)=1 has zero diagnostic on every triple of distinct vertices, but cannot be an integer repair because d0 always has zero diagonal. The source's blind three-term example `arb arc csb csa` gives e(0,1)=e(0,2)=1, e(2,0)=e(2,1)=-1 and other entries zero. Both oriented triangle sums vanish, yet its two-way sum at (0,1) is 1, and no repair potential realizes it. Thus balanced marked triples do not imply zero quotient class. A packet with no marks may have a nonzero discrepancy and no diagnostic rows. Conversely a mark with diagnostic 9 is a valid filled, unbalanced source state.

The generic source has independent e(x,y) and e(y,x), not a single antisymmetric edge value. The source's 25:D7 rank theorem requires *all loops and all two-way sums zero*. These hypotheses allow the antisymmetric restriction; they are not typing defaults. No source coordinate is deleted to fit a simple graph or simplicial complex, and no marked triple is equated to a Kan filler.

A source change need not descend to its quotient. Source 23:D4 (`paper/twentythird/paper.md`, line 291; `addTerm_not_respected`) explicitly gives two equivalent two-term states whose added-term outcomes differ; identification can also fail from four terms. Source 25:D9 retains this failure (`addTerm_not_respected25`). Consequently this fixed-carrier adapter provides no quotient-respecting carrier-changing transition, temporal memory, presheaf transport, policy or permission. Replaying mathematical evidence is separate from admission; source fifteenth and sixteenth derivations assign different admission semantics, neither present in the chosen latest seed.

## Scoped production evidence

`omega_wdp/tests/genesis_ongoing_adapter.rs` contains six focused tests: all ordered coordinates including loops/reverse arcs; an explicitly filled unbalanced triple; actual native repair with unchanged diagnostics and forged-potential/output refusals; loop and blind-three countermodels; complete integer-potential comparison and context mismatch; malformed domains/multiplicities/marks/labels, empty carrier, and raw-source multiplicity binding. The production Cargo result is recorded separately after running the registered module against the locked offline workspace.

Production verification completed: `cargo +stable test -p omega_wdp --test genesis_ongoing_adapter --manifest-path omega_engine/crates_rs/Cargo.toml --locked --offline -j 2` passes **6/6**, using `/workspace/the_symbol_game/omega_engine/crates_rs/target` as the shared target. The empty-carrier test passes through the actual functional/linear matrix owners, including the empty receipt, repair and equivalence witness. A 2^256 simultaneous r/s multiplicity confirms exact unbounded integer retention and strict raw-packet replay binding. Rustfmt and scoped diff checks pass. Existing dependency warnings were emitted; no test failure occurred.
