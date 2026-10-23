Status: AI-drafted, awaiting human review.

AuthorityEffect: None.

This supplies the full finite-game array/source representation behind the
Genesis-Ongoing fewest-change result and its obstruction/rewriting interfaces.
The source state contains a finite term set, a finite assertion set and both
tracked names. The wire model retains every field, including merged names and
arbitrary natural term labels. It places no apart-name or consecutive-label
restriction on the state.

Arrays may contain duplicates. Decode takes their finite sets; encode chooses
a finite-set enumeration and is noncomputable. Decode(encode(s)) = s, while
raw array order and multiplicity are not source fields. The array operations
and decode are computable. The theorem is a mathematical set representation,
not a deterministic serialization or external-runtime/compiler theorem.

Adding a term, adding an assertion, removing an assertion, and identifying
terms are independently defined array operations. Identification updates the
term store, every assertion endpoint and both names; its image is interpreted
as a set. Every operation commutes with source decode. The wire Step relation
retains every source membership, freshness, distinctness and nonrelation guard.
Every wire step is a source step and every source step from a represented
state has a wire representative. Induction gives the same two directions for
all finite Reach sequences, preserving their exact number of steps. This is
an interpreter-relation proof, not merely a comparison of count tables.

Raw array Legal and WF predicates are equivalent to the actual source Legal
and WF predicates. Thus every represented performed history preserves them.
An attempted assertion image is legal exactly when its endpoints differ;
an identification image is legal exactly when neither directed pair between
the merged terms was asserted. An illegal image is diagnostic and is not
counted as a performed step.

The actual source set-size and destroyed-given costs have exact raw-array
formulas using distinct term/assertion counts and both tracked names. These
costs commute with decode. The general source lower and upper bounds therefore
transport to the wire model. For each legal well-formed target, some permutation
of the initial seed reaches it with n + 3 = costA or n + 4 = costB. From no
permutation of that seed is it reached in fewer steps. This includes merged
names and every natural writing. It does not claim that every fixed writing
of a seed reaches every arbitrary target at that same cost.

Injective rewriting commutes with every source step and every finite source
history, preserves the costs, and transports wire histories with the same
number of steps. A source ReachNoRemove history tracks an asserted pair through
identifications and permits removal only of other pairs. Induction preserves
its membership; source legality keeps its endpoints different and their
identification obstructed. These results quantify over all natural writings,
not a finite list of permutations.

A legal build answer adds a fresh term and an assertion involving it in two
performed changes. Collapsing that fresh term back gives the would-be loop
image; performing the illegal final identification is refused. Any legal
result whose quotient fixes old terms but produces a loop must have a new
assertion involving a new endpoint. No single source move both introduces
an endpoint and asserts a new pair involving it. A general Lean lower bound
therefore gives at least two steps, matched by the build construction. The
bound is transported to the wire model. It is not inferred from one fixture.

Compilation boundary

The immutable H3V7N5QF Basic, Finite, Cost, Paths and Answers modules, and Second
Step, Carry and Cost modules compiled unchanged with Lean 4.35.0 and pinned
Mathlib. The original Second/Rename.lean DID NOT compile unchanged: its inverse
rewrites in the two all-writing bounds and its indexed induction proofs fail.
That failed output remains in the replay receipt. The archive is not edited.

CampaignGenesisOngoingRename.lean is a separate compatibility proof port. It
retains the source definitions and theorem statements, repairs the inverse
rewrites and indexed cases, and proves tracked pair membership directly before
the obstruction conclusion. CampaignGenesisOngoingRefinement imports this port
and the actual unchanged source game types. Successful replay and every audited
axiom belong to these delivered modules, not to the failed original file.

Independent exact check

The standalone SymPy/Python audit imports no repository code. Over the declared
three-label universe, it enumerates all 627 legal well-formed states, including
merged names, and compares separate set and array implementations on 18,810
attempts: 4,494 performed and 14,316 refused. It tests a duplicate-containing
wire representative for every state. Breadth-first search from all writings
of each seed reaches all states; its distances satisfy both exact cost formulas.
The maximum distances are 10 and 11; distance sums are 3,006 and 3,225. A separate
nonconsecutive writing checks all 18,810 transition squares. The 1,827 build
controls check a legal two-step construction, its illegal diagnostic image,
refusal of the final identification, and absence of a zero/one-step path to
that target in the declared one-step universe. Four exact semantic mutants
are contradicted. Normal/optimized output agrees and strict mypy passes.
These finite checks are separate from the unbounded Lean theorems.

What is proved

Full state/Legal/WF/Step/Reach representation; exact costs and matching lower
and upper bounds for all target writings; source rewriting and multi-step
tracked obstruction persistence; both obstruction iff statements; and the
general two-step minimum for a build answer under its stated quotient premise.

What is assumed

The actual finite-game source definitions and the declared set interpretation
of wire arrays. The compatibility port's unchanged source definitions and
statement shapes, plus its repaired proof terms, are reviewed explicitly.
All successful audits use only propext, Classical.choice and Quot.sound. Both
new Lean files and the checker are author-assessed L4D; Lake configuration is
L1C under the explicit configuration exception. Human review is pending.

What is open

External runtime/compiler refinement, deterministic byte serialization and
claims beyond this finite game. The failed original Rename module is not
silently called compiled. Existing DAG statuses are unchanged; outcomes remain
provisional for the reviewer.
