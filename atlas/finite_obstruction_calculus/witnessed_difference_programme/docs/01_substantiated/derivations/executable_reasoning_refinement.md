# Executable certificate refinement into witnessed reasoning

Edition 2.4.5, 2026-10-16. AuthorityEffect: None.

The previous edition proved an abstract inference calculus and tested separate
Python and Rust checkers. This edition supplies computable Lean checkers and
proves that their accepted concrete certificates refine that calculus. Foreign
certificates can now produce closed Lean theorems about their explicit input
tasks. The formal boundary is stated below; it does not assume correctness of
the foreign searcher.

## Concrete inputs and semantic interpretation

`FiniteTheory` stores an ordered list of atom names, a list of fact indices and
an ordered list of finite rules. `Valid` requires distinct nonempty names and
all fact, premise and conclusion indices to be inside the named carrier.
Duplicate facts are harmless to membership semantics; their order and
multiplicity remain part of exact certificate-to-task equality. Python exports
its fact set in sorted order; Rust preserves its explicit fact vector.

`FiniteTheory.abstract` interprets a natural number as an atom. Its facts are
exactly the listed indices; its rules are exactly the listed premise/conclusion
pairs. A query must be inside the finite carrier. This ambient natural-number
representation does not add facts or rules outside the declared carrier.

A proof step contains a conclusion index, an optional rule index and an ordered
list of references to earlier steps. `references` recursively matches the two
lists and uses optional lookup into the already accumulated conclusions. It
rejects mismatched lengths, invalid indices and forward references. Empty and
repeated premises retain their ordinary Horn meanings. A fact step must carry
no premise references. A rule step must name an existing rule with the same
conclusion and exactly matching referenced premises.

`replay` appends one checked conclusion at a time. `checkProof` additionally
requires a valid current theory, exact equality of the certificate's theory,
equality of its goal to the separately supplied query, and that query at the
end of the replay. Empty proofs do not prove a query. Every function is total
on its finite Lean input through structural recursion or a finite decidable
predicate. This does not assert a wall-clock or machine-memory bound.

## WDP-RSN-09: executable proof refinement

The formal development is `ExecutableReasoning.lean` in the root
`lean4/research_programs/wdp_reasoning/` library.

1. `references_sound` proves that every matched premise occurs in the earlier
   conclusion list. It follows by simultaneous inspection of the index and atom
   lists; a successful optional lookup supplies list membership.
2. `checkStep_justified` proves that an accepted concrete step is an instance
   of the previous edition's abstract `Justified` relation. A fact comes from
   the current fact list. A firing supplies an actual member of the current
   rule list and prior occurrences for every premise.
3. `replay_refines_trace` proves that successful replay preserves
   `CheckedTrace`. Concrete lists are chronological; the abstract trace
   constructor prepends, so the transport uses list reversal. The induction
   explicitly follows every branch of the executable replay.
4. `replay_sound` preserves derivability of every accumulated conclusion.
   `checkProof_sound` extracts the final requested atom and yields
   `Derivable T.abstract goal`. `checkProof_binding` also recovers current
   theory validity, query bounds, exact source equality and goal equality.

These statements quantify over arbitrary finite concrete theories and arbitrary
finite certificate lengths. They are proved from the definitions of executable
Boolean checkers, rather than from an assumed correctness predicate supplied
by the caller. Composing `checkProof_sound` with the earlier model-soundness
theorem yields `checked_interpretation`: an accepted certificate has its stated
meaning in any world whose facts and rules satisfy the admitted model contract.
The interpretation contract remains a hypothesis.

## WDP-RSN-10: negative certificates and incompatible verdicts

A model certificate carries an exact source theory, a goal and a Boolean vector.
`checkCountermodel` checks its length, all task bindings, truth of every fact,
closure under every rule and falsity of the requested atom. The computable
predicate quantifies over the supplied finite lists.

`checkCountermodel_models` builds a model of `T.abstract`: atom `a` is true
exactly when optional lookup in the vector gives `some true`. The fact and
rule conditions are precisely the model clauses. The goal lookup gives
`some false`, so `checkCountermodel_sound` applies soundness to exclude any
derivation of that goal. `checkCountermodel_binding` recovers the source/query
conditions. `checked_verdicts_exclusive` shows that positive and negative
certificates cannot both be accepted for one task and goal.

A rejected certificate gives no judgment about entailment. A timeout, missing
tool or exhausted search also gives no judgment. In particular, rejection of
a proposed proof is not a countermodel, and a countermodel proves non-entailment
from the supplied theory rather than falsity in an actual world.

## WDP-RSN-11: original graph transport

`graphTheory` makes the start vertex the sole fact and turns each directed edge
`(u,v)` into the rule `[u] => v`. `Reachable` is independently defined by a
zero-edge path at the start and extension along a listed edge.

`graph_derivable_reachable` interprets every atom as reachability: the start is
reachable and every graph rule preserves reachability. Abstract soundness
then maps every derivation to a path judgment. Conversely,
`graph_reachable_derivable` inducts on the independent reachability relation,
introducing the start fact and firing the rule corresponding to each edge.
Their combination is `graph_derivable_iff_reachable` for arbitrary finite
edge lists. No enumeration of graphs is used in this theorem.

`checked_graph_proof` and `checked_graph_countermodel` compose this equivalence
with the executable checker theorems. Thus a concrete accepted certificate
proves reachability or excludes it in the explicitly supplied graph. The Python
`graph_module` emits these original-question theorems directly. The older
Python path decoder still has its separate executable tests; its operational
semantics has not been formalized by this argument.

## WDP-RSN-12: foreign certificate replay

Python's `reasoning_refinement.py` and native Rust's
`witnessed_reasoning_replay.rs` export data constructors and a theorem of the
following form, with all task and certificate data filled in:

```lean
theorem result : Derivable task.abstract goal :=
  checkProof_sound (T := task) (goal := goal) (p := certificate) (by decide)
```

Negative results use `checkCountermodel_sound`; graph exports use the corresponding
graph theorem. `by decide` constructs a proof checked by the Lean kernel. The
route uses neither `native_decide` nor an asserted Boolean result from Python
or Rust. Failed decision proofs remain compilation failures. A valid instance
therefore receives a closed theorem about the explicit Lean input literal.

Names are exported as Unicode scalar constructors, so user text cannot become
Lean declarations or tactics. Python rejects surrogate code points rather than
silently changing identity. Natural-number indices reject negative integers and
Python booleans. Out-of-carrier countermodel entries are rejected before vector
conversion, which otherwise could erase them. Malformed proof references are
preserved for the Lean checker to reject. Rust exports both the independently
supplied task and the certificate's own task, retaining stale-source differences.
Python validates its existing digest binding and reconstructs the current task;
the Lean theorem checks the actual supplied facts and rules, without assuming
that SHA-256 is mathematically injective.

The live Python adapter emits a theorem, invokes Lean and records the source
hash, task digest and query. It returns a logical judgment only with
`KERNEL_ACCEPTED`; all other statuses carry `judgment = None`. Its generated
source is temporary. The verification harness retains complete generated
sources, command logs and their hashes for audit.

## Verification and exact scope

`scripts/verify_reasoning_refinement.py` builds the root `WdpReasoning` target,
audits all 17 new declarations, constructs 2,048 two-atom Horn obligations and
64 two-vertex original graph obligations, and replays them through the kernel.
Horn outcomes are compared with independent Boolean valuations. The harness
also rejects ten malformed Python obligations and replays eleven obligations
emitted by a freshly compiled native Rust example, including seven refusals.
Unicode names, repeated premises and zero-premise rules have positive controls.
The native checker and exporter test targets each have two tests; the checker
retains its independent 2,048-query valuation census.

These are bounded checks of serialization and foreign execution. The universal
refinement results belong to the executable Lean functions and their checked
theorems. Seventeen new declarations use only `propext` and `Quot.sound`, with
no custom axioms or admitted proofs. The prior fifteen declarations retain their
own audit. Fresh elaboration uses installed Lean 4.34.1; the repository pin
remains 4.34.0. Selected Rust modules are compiled afresh, not the entire crate.
The input-bound result is
[the refinement receipt](../../manifests/executable_reasoning_refinement.json).

The harness requires Python 3.12 with assertions enabled and refuses optimized
execution (`-O`, `-OO` or `PYTHONOPTIMIZE`) before running tools or creating its
output directory. Its regression test checks that refusal. The retained receipt
was regenerated after adding this guard; the 12 exporter and harness tests pass.

## Remaining obligations

The completed records are `WDP-REASONING-EXECUTABLE-KERNEL`,
`WDP-REASONING-CERTIFICATE-REPLAY` and `WDP-REASONING-GRAPH-TRANSPORT`.
`WDP-REASONING-FOREIGN-SEMANTICS` retains a universal correspondence proof for
the Python/Rust serializers, checkers, source-language execution and searcher,
including a formal finite saturation/termination argument. Kernel replay
reduces the trusted foreign computation needed for an individual result; it
does not establish those whole-program equivalences. Lean's kernel, elaborator,
toolchain, file/process boundary and the input-literal correspondence remain
explicit parts of the verification trust boundary.

`WDP-REASONING-EXTENSIONS` also retains deployment into a production consumer,
observed-world adequacy, probabilistic or defeasible semantics and fully priced
recursive reuse. The foundational, physical and institutional WDP goals remain
at their independently recorded statuses.
