> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\authorization_incompleteness_theory.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](RECOVERY_NOTES.md).

---

# Authorization as an Incompleteness Boundary

**Subtitle:** A Primitive Difference research prospectus for total
semantic finality.

**AuthorityEffect:** None.

## Paper metadata

| Field | Value |
| --- | --- |
| Author | Jeremy H. Carroll |
| Date | 2026-08-21 |
| Version | v0.14 working research paper |
| Status | Prospectus with finite rooted Lean results; global theorem open |
| Document class | Chapter / stem research paper |
| Authority effect | None |

## Omega Engine Primitives

<!-- markdownlint-disable MD013 -->
| Slot | Binding in this paper |
| --- | --- |
| Primitive Differences | J011 `PrimitiveDifference P`: declared `delta`, `Zero`, and zero laws. It does not produce a validity predicate. |
| Carriers / Structure | `P : PrimitiveDifference α β`; proposal carrier `α`; canonical quotient report `pdProj P`; supplied `valid : α -> Bool`. |
| Cochain complex | N/A at AIT-PD1. No `C0`, `C1`, `C2`, or cohomological differential is asserted. |
| Coboundary maps | N/A at AIT-PD1. |
| ZeroRel | `ZeroRel P x y := P.Zero (P.δ x y)`; the current J011 candidate proves it is the canonical quotient fiber relation. |
| Licensed repairs / operator family | Canonical quotient construction only. Semantic contract, evaluator, replay, and terminal policy remain added inputs or OPEN. |
| Quotient / Q1 | `ResidualQuotient (pdSetoid P)`, a setoid quotient. It is not a cohomological `Q1` claim. |
| Residuals | `Phi1` and `Gamma2`: N/A. The live residual is a split `ZeroRel` class for supplied validity. |
| Witnesses | `lake build AuthorizationIncompletenessTheory`; theorem-level `#print axioms`; bounded packet replay; unchanged PO-000 source comparison. |
| Observers / profiles | Declared report map `pdProj P`; no physical or cosmic observer is introduced. |
| Anomalons | N/A. |
| CompletionLaw | OPEN. AIT-G5 and AIT-G6 must state their own computability and metatheory hypotheses. |
| Terminal / route | `OpenObstruction` plus `LeanObligation` for the global and policy lifts. |
| AuthorityEffect | None. |
<!-- markdownlint-enable MD013 -->

## Draft status

This is not the final paper and does not claim that the global LLM
conclusion has been derived from Primitive Difference. It is a research
prospectus with finite rooted Lean results. Its job is to name the exact
series of derivations needed to turn the desired conclusion into a
connected proof rather than a slogan.

The proposed series starts from the present Primitive Difference trunk:
two unequal marks, a derived quotient map, and the fact that looks,
reports, sections, dynamics, and host structures are additions. It then
introduces proposal, evidence, replay, authorization, computability, and
self-soundness one at a time. See `seal_derivation_series.md`.

## Abstract

An LLM can generate a proposal, explain it, simulate a check, and
emit a confident verdict. None of those acts by themselves make the
verdict globally final. This paper isolates the exact reason.

Let a proposal have a semantic validity predicate, let a report be the
information shown to an authorizer, and let the authorizer decide only
from that report. If two proposals have the same report but different
validity, no such authorizer can be both sound and complete. The result
is a small factorization theorem, formalized in Lean here. It applies to
an LLM's self-report, a test log, a hash-only receipt, or any other
compressed evidence interface.

The prospectus then couples the finite theorem to two standard global
limits. Rice's theorem blocks a total computable sound-and-complete
decider for a nontrivial semantic property of arbitrary Turing-complete
programs. Goedel-style second-incompleteness limits block a sufficiently
strong, consistent formal theory from closing even its own consistency
question from inside the same theory. Once their model bindings are
formalized, they yield a precise conclusion: an LLM, considered only as
a computable proposal source, cannot provide total semantic
authorization for arbitrary proposals. It may participate in bounded
authorization, but the resulting assurance is conditional on an
independently fixed specification, checker, replay environment, and
trust base.

This is not an argument against proof-carrying code, formal proof
checking, or automation. Those are the constructive local case. The
boundary is between a check under a declared contract and an assertion
that the same proposal source has supplied global certainty of that
contract, checker, and semantic interpretation.

## Why this matters

The distinction is operational. A team can put a generator, proof
checker, and policy engine on the same machine and still have a genuine
local boundary if the proposal cannot rewrite the contract, parser,
checker, evidence binding, or policy after the fact. Conversely, moving
an unchecked generator to a different server does not create a boundary.

This gives the LLM business a usable design rule rather than an
anti-automation slogan: automate proposal and bounded checking freely,
but name the contract, report adequacy, replay root, and terminal scope.
Outside that named boundary, return `open` instead of upgrading a fluent
or halted output to total semantic certainty.

## 1. Primitive Difference is the starting interface

The proposed route does not begin by declaring an LLM, a Turing machine,
or a verification protocol. It begins with the smallest live trunk that
has already been made explicit: a carrier with two unequal marks and a
Primitive Difference whose zero relation yields a quotient map.

The J011 support spine is important precisely for what it does not add.
It derives a quotient once the stated relation laws are available, but
does not derive an arbitrary look, a report, a section, a dynamic, a
graph, a norm, a Hilbert host, or an authorization predicate. These are
later imports. The proposed first new derivation must make the same
discipline apply to a proposal contract:

```text
primitive difference
  -> presentation / quotient
  -> declared report
  -> independently interpreted validity predicate
  -> evaluation and replay
  -> terminal authorization
```

The critical point is not that raw marks contain authorization. They do
not. The point is that every lift which purports to add a validity test,
report, or terminal act must state its carrier, new structure, and
invariant. This prevents a semantic predicate from entering as an
unpriced conclusion.

### 1.1 The P0 descent discipline

PO-000 is the fixed formal anchor for the next lift. Let `p : X -> M`
be a declared report or projection. For each later operation, ask a
separate descent question:

```text
evaluation E descends through p
  exactly when p(x) = p(y) implies E(x) = E(y).

authorization A descends through p
  exactly when p(x) = p(y) implies A(x) = A(y).
```

If the authorization predicate splits a `p`-fiber, P0's factorization
obstruction says that no function of `p(x)` alone can recover it. A
proposal may still be generated on `X`; it does not become a
report-level authorized result until its required predicate descends.

This makes the intended route concrete. The series must not push
proposal, evaluation, or authorization through a projection merely by
renaming them. At each stage it must either prove descent, declare an
enriched report, attach extra evidence, or retain an open residual.
P0 itself stays unchanged.

The first connected formal bridge now instantiates this question on the
current J011 candidate quotient. For `P : PrimitiveDifference α β`, J011
supplies `pdProj P : α -> ResidualQuotient (pdSetoid P)` and proves
that its fibers are exactly `ZeroRel P`. The new theorem
`pd_quotient_split_blocks_report_only_authorization` says: if a supplied
`valid : α -> Bool` splits one such `ZeroRel` class, no decision on
`pdProj P` alone is totally correct. This is a statement-level
specialization of P0, not an import or alteration of the P0 source.

## 2. The question and the answer

The question is:

> Is evaluation and authorization always required to be external to a
> proposal source if replayability and local and global certainty are
> wanted?

The prospective theorem answers yes, if “external” means external to the
information and trust that the proposal source controls. It answers no,
if it merely means a physically separate machine, model, company, or
human.

A proof checker can run in the same process as a proposal generator. A
certificate can be checked on the same computer that produced it. That
does not make the result self-authorizing, because the accepted syntax,
the checker, its semantics, and the replay root are additional fixed
objects. They form a logical boundary outside the submitted proposal.

Conversely, moving the same unchecked code to another server does not
create externality. It is still source-controlled if the proposal can
choose its checker, its schema, its evidence interpretation, or the
meaning of “pass.” The required boundary is therefore logical and
causal, not merely organizational.

There is now a finite Lean countermodel to both physical-placement
mistakes. `coLocatedComplete` puts proposal source and evaluator at the
same `Unit` site and authorizes a complete Boolean report. Conversely,
`separatedCollapsed` places them at different Boolean site labels yet
cannot authorize because its report erases the validity bit. The theorem
`physical_separation_neither_needed_nor_sufficient_for_toy_authorization`
does not certify any real deployment's security; it establishes exactly
that site distinction alone is neither the necessary nor sufficient
condition in this model.

The answer separates three levels.

<!-- markdownlint-disable MD013 -->
| Level | What can be certain | Necessary boundary |
| --- | --- | --- |
| Local replay | A named artifact reproduces a named finite check under a fixed environment | Frozen input, parser/schema, checker, and replay command |
| Contract authorization | A proposal satisfies a declared decidable contract | A trusted checker and a policy that says what the check licenses |
| Global semantic authorization | An arbitrary proposal is correct in every intended semantic sense | Impossible for a total computable decider over a Turing-complete proposal class; any real system must narrow the class, return unknown, or import an oracle/trust base |
<!-- markdownlint-enable MD013 -->

“Total certainty” means both soundness and completeness over the stated
domain. It does not mean a high confidence score, a test pass, a model
agreement rate, or an authenticated log.

## 3. The Authorization Incompleteness Theorem

The theorem has a finite core and two global lifts.

### 3.1 Finite information form

Let `X` be proposals, `R` reports, `rho : X -> R` a report function,
and `V : X -> Bool` the validity predicate relevant to a stated
contract. A report-only authorizer is a function `A : R -> Bool`.

It is totally correct when

```text
for every x in X, A(rho(x)) = V(x).
```

**Theorem AIT-1 (report-factorization impossibility).** If there are
`x` and `y` such that `rho(x) = rho(y)` while `V(x) != V(y)`, then no
report-only authorizer is totally correct.

The proof is one equality chain. If `A(rho(x)) = V(x)` and
`A(rho(y)) = V(y)`, equal reports force equal decisions and hence equal
validities, contradicting the split fiber. The Lean theorem is
`split_fiber_blocks_total_authorization` in
`formal/authorization_incompleteness_core.lean`.

The theorem does not assume an LLM, deceit, bad faith, or limited
computation. It is an information boundary. A proposal can be
mathematically correct and still not be certifiable from a report that
forgets a fact on which the contract depends.

### 3.1.1 Primitive Difference quotient specialization

The generic theorem is now connected to the current J011 candidate
Primitive Difference trunk rather than only to a Boolean analogue. Given
the J011 quotient report `pdProj P`, the bridge proves both directions at
the appropriate ceiling:

```text
valid splits a ZeroRel P class
  -> no total decision factors through pdProj P.

valid is constant on every ZeroRel P class
  -> a well-defined quotient decision exists.
```

The second line has the constancy condition as an explicit hypothesis.
Primitive Difference does not manufacture it. The quotient theorem uses
the J011 setoid quotient and therefore its negative direction depends on
Lean's `propext` and `Quot.sound`; the positive quotient-lift theorem is
axiom-free. The exact source is
`formal/primitive_difference_p0_bridge.lean`, rooted by
`AuthorizationIncompletenessTheory`.

### 3.2 Self-attestation as a special case

The formal file instantiates AIT-1 with a packet whose semantic bit is
validity and whose self-receipt is the unique `Unit` value. The receipt
has the same value for a valid and an invalid packet, so no function of
that receipt decides validity. It also supplies a positive witness: a
report that retains the semantic bit can decide this deliberately tiny
contract.

This positive witness matters. The theorem is not “nothing can be
authorized.” It is “an authorizer needs evidence adequate to the claim.”
The adequacy condition is exactly that validity be constant on report
fibers.

### 3.3 Global semantic form

For a Turing-complete proposal language, let `V` be a nontrivial
extensional semantic property of the program denoted by a proposal.
For example, `V` might mean that the program never reaches a forbidden
state, terminates on every input, or implements a supplied mathematical
specification.

The word “arbitrary” cannot be supplied by rhetoric. Before this paper
uses the global theorem as an in-tree result, AIT-G5b requires a frozen
carrier record: program and input encodings, execution semantics,
universality, observational equivalence, nontrivial witnesses, a
reduction plan, the report/policy split, and replay closure. The finite
tape models, PO-022, PO-023, and an isolated no-literature derivation
run are candidate sources for such a record; none is already a
Turing-complete proposal class. The live requirements are in
[computability_lift_admission.md](computability_lift_admission.md).

**Theorem AIT-5 (global authorization incompleteness, target).** No
total computable procedure `A` is both sound and complete for `V` over
all proposals in that language.

This is a direct application of Rice's theorem once the proposal
language, extensional semantics, and nontriviality witnesses are fixed.
The paper treats the statement as a standard external theorem until the
planned in-tree reduction has been formalized. Its precise scope is
important: it concerns arbitrary programs and nontrivial semantic
properties. It does not prohibit a proof checker from deciding whether
a finite proof object satisfies a fixed proof calculus.

The current Lean target now proves the neutral transport step that a
Rice-style argument needs. Given a source predicate with no total decider
in a declared decision class, a validity-preserving reduction into
proposals, and closure of the proposal decision class under
precomposition with that reduction,
`no_source_decider_blocks_total_authorizer` transfers the no-decider
boundary to proposal validity. Its `allowedHard` and `allowedProposal`
parameters are intentional: the theorem does not call arbitrary Boolean
functions “computable.” A future Rice lift must instantiate them with a
real program representation, a total-computability class, a source
undecidability theorem, and an actual reduction.

### 3.3.1 Terminalization consequence (AIT-G5c)

The next abstract bridge states what a declared class-relative
no-decider boundary means for a terminal policy. If an allowed
`authorized` bit is acceptance-sound and acceptance-complete for the
validity predicate, that bit itself is a total Boolean decider. Thus it
contradicts a supplied `NoTotalDecider` premise for the declared decision
class. If a terminalizer is additionally rejection-sound and never
returns `unresolved`, it is acceptance-complete and reaches the same
contradiction.

This is conditional, not a universal mandate to leave every result open.
`formal/terminal_authorization_boundary_models.lean` also gives a finite
Boolean contract with a closed, two-sided sound terminalizer. Under the
named no-decider and allowed-membership premises, the remaining sound
routes are an unresolved case or the abandonment of at least one of the
two semantic soundness conditions. The module does not prove Rice's
theorem, model an LLM, establish physical separation or custody, or
identify an actual program class; AIT-G5b, AIT-G5, and AIT-G7 remain open.

### 3.4 Internal closure form

Suppose a formal system `T` is recursively axiomatized, consistent,
sufficiently expressive for arithmetic, and its internal provability
predicate satisfies the required derivability conditions.

**Theorem AIT-6 (self-soundness boundary, target).** `T` cannot establish
its own consistency from within `T` under the preceding hypotheses.

This is the second-incompleteness lift. It is weaker than global semantic
soundness, so it cannot by itself prove every claim sometimes made about
AI systems. Its role is narrower and stronger: even a formal system that
checks many individual proofs does not close the metatheoretic question
of whether its own global proof discipline is sound. A meta-theory can
establish a relative result, but it becomes the next trust boundary.

### 3.5 Turing is not wrong: computation is not authorization

The program does not seek a computation that exceeds Turing computation.
The criticism is directed instead at an interpretation that silently
treats an operational computation trace as a completed authorization.
Turing-machine formalisms give a standard account of effective
algorithmic procedure. What that form does not by itself describe is the
full authorization relation:

```text
proposal bytes + parser + intended semantics + contract
  + checker + replay environment + terminal policy.
```

A Turing machine can calculate any of these components once they are
given as inputs. It does not select the intended semantics, establish
that a report preserved every contract-relevant distinction, or confer a
policy effect merely by halting. Those are not failures of the model of
computation; they are additional structures and trust relations that a
model of computation presupposes when it is used as an authorizer.

The controlled derivation branch makes this visible without attacking
the computation model. Its vocabulary is deliberately narrow:

<!-- markdownlint-disable MD013 -->
| Turing-style operational item | Role in this paper | Further structure still required |
| --- | --- | --- |
| Tape/configuration | A presentation or proposal state | Intended semantic interpretation |
| Declared blank/marked cell | A syntactic distinction | A claim about meta-level absence |
| Head/read rule | A syntactic selection | Evaluation of what the symbol means |
| Transition and advance/stay outcome | A declared state update | Proof that a supplied contract is preserved |
| Halt condition | Declared execution terminality | Authorization or policy effect |
| Output decoder | Semantic adapter | A proof that the adapter is adequate |
| Terminal policy | Licensing rule | A named owner, scope, and trust base |
<!-- markdownlint-enable MD013 -->

### 3.5.1 A tape boundary has more than one typed role

The phrase “the reader evaluates the tape” hides several distinct maps.
The current finite control model makes them explicit:

```text
TapeCell        = blank | marked
ReadControl     = read | unread
ReadReport      = unread | observed TapeCell
SemanticAdapter = TapeCell -> Bool
TerminalPolicy  = ControlOutcome -> Bool
```

`blank` and `marked` are declared alphabet members in this model.
`unread` is instead a control/report constructor: it says that the
observer did not expose a cell. A genuine meta-level absence needs a
separate encoding such as `Option TapeCell`; it must not be silently
identified with the declared blank symbol. Once either distinction is
encoded it is, of course, part of the formal presentation, but the two
types play different roles.

A read rule selects a declared mark. It becomes an evaluator only after
a semantic adapter, a contract predicate, and an evidence procedure are
specified. It becomes an authorizer only after a terminal policy binds a
successful check to a scope. The axiom-free finite theorems
`same_read_token_allows_distinct_semantic_adapters` and
`unread_report_blocks_content_decider` exhibit those two boundaries:
the same blank token admits distinct supplied interpretations, and an
`unread` report cannot decide a contract that distinguishes the hidden
cell. They are countermodels about this tiny carrier, not a theorem that
standard Turing machines lack semantics.

The word `stay` in the controlled branch is an explicitly declared
transition variant, not a claim about which instruction set is primitive
in every historical Turing-machine formalism. Equally, `blank` is a
declared tape symbol; a meta-level absent value must be modeled
explicitly rather than smuggled into the tape alphabet.

The finite model in
`formal/tape_control_authorization_models.lean` already gives the small
negative control: two presentations share the same `halt` report while a
supplied content contract distinguishes them, and two terminal policies
give that same report opposite effects. The next experiments are listed
in `controlled_turing_derivation_series.md`. They must prove their
invariants and countermodels; a narrative that a tape "understands" a
symbol is not evidence.

The next finite lift now does exactly that for one declared transition
table. `formal/tape_transition_invariant_models.lean` enumerates four
configurations, realizes `advance`, `stay`, and `halt`, and proves that
its `cleanTerminalContract` is preserved. The same table has the named
`runningMarked` countertrace for its separately supplied
`markedCellContract`; moreover, two configurations with the same `stay`
report still split that contract. Thus a transition can preserve one
specified invariant and violate another. The table does not choose the
semantic contract, and its finite proof is not a claim about arbitrary
Turing machines.

AIT-DTM0 is the next, still bounded, operational refinement. Its direct
finite-rule model has a total mathematical tape, left-biased rule lookup,
a fuel-bounded evaluator, and distinct halted, stuck, and
fuel-exhausted results. It proves that a declared halt is exactly the
designated control state, while the same halt result can receive
different supplied terminal policies. The generic terminal statements
and closed stuck/fuel fixtures depend on propext; blank/absence and
closed write/reaches-halt fixtures have no axiom dependencies. This is a
direct syntax-and-execution seed, not a byte encoding, universal-machine
theorem, Rice reduction, or a claim about P versus NP.

AIT-DTM1 adds one narrow syntax lift to that direct seed. A finite machine
is represented by one halt-state token followed by complete five-token rule
frames. The parser consumes the entire `List Nat` code, rejects an empty
header, a truncated frame, an invalid symbol tag, and an invalid movement
tag, and satisfies
`decodeMachine (encodeMachine machine) = some machine`. The two tag
round-trip theorems print no axioms; the rule-list and machine round trips
plus the malformed-code fixtures print `propext`. This is neither source
bytes nor an input/configuration encoding, parser-to-execution agreement,
universal-machine theorem, Rice reduction, or authorization result.

P versus NP is a separate resource-bounded question. A fixed
polynomial-time verifier can authorize the verifier's stated relation
for a supplied finite witness; it does not thereby find a witness, decide
the intended natural-language specification, or establish that every
NP relation has a polynomial-time decision procedure. SEAL-TC-05 is
therefore a controlled certificate-verification lift with a P0 adequacy
audit, not a P versus NP attack. Any later complexity result would need
a fixed uniform encoding, machine/cost model, reduction, and exact
quantifier scope before it receives an AIT claim ID.

The Rice lift sharpens this distinction. It says that even after those
relations are represented as program semantics, there is no total
computable sound-and-complete authorizer for arbitrary programs and a
nontrivial extensional property. The desired theorem is therefore an
incompleteness theory of authorization around computation, not a claim
that Turing machines compute incorrectly.

### 3.5.2 A bounded executable adequacy packet

The next finite packet makes the P0 condition executable without
pretending it solves the global question. Its proposal is the exact
four-configuration transition table. Its contract separately names the
clean-terminal and marked-cell predicates. Its evaluator recomputes the
transition facts rather than reading the proposal's own pass Boolean.
The manifest binds the proposal, contract, terminal policy, evaluator,
entrypoint, Lean model, its direct formal dependency, and Lean toolchain
with SHA-256 digests.

The bounded result has both a positive and a negative side. The Lean
theorem full_configuration_report_adequate_for_marked_cell_contract
establishes adequacy for the full configuration report. The theorem
control_report_not_adequate_for_marked_cell_contract exhibits a
same-stay report fiber on which the marked-cell contract differs. The
PowerShell evaluator returns open_due_to_inadequate_report for that
control-only route. Its terminal policy remains open even after a
successful local replay.

This is a concrete answer to a narrower engineering question: how can a
system avoid upgrading an inadequate report into a final decision? It
does not make SHA-256 collision resistance, evaluator-to-Lean
correspondence, runtime integrity, or custody true by declaration. The
manifest itself must be fixed outside proposal-controlled bytes; a
co-located working tree does not establish independent custody.

## 4. Consequence for LLM systems

An ordinary deployed LLM inference run is a computable proposal source:
given model weights, an input, a sampler seed or distribution, tool
responses, and a finite execution budget, it emits finite text or a
finite tool trace. If the system itself produces the final decision
without an independently fixed semantic checker, it falls under one of
two cases.

1. Its decision reads only a source-controlled report. AIT-1 applies
   whenever the report omits a contract-relevant distinction.
2. It claims to settle arbitrary executable proposals. AIT-5 applies
   once the proposal class is Turing complete and the claim is a
   nontrivial semantic property.

Randomness does not create an exception to a certainty claim. If
certainty means correctness on every permitted run, fix a random seed
and the alleged guarantee becomes a deterministic one. If a probability
qualification remains, the claim is no longer total certainty.

External tools also do not evade the theorem. They can make a system
more capable and can support a real bounded authorization. But a tool
whose answer is required for the decision belongs to the authorization
boundary; the LLM is no longer the sole source of assurance.

The resulting business conclusion is the target conclusion:

> No LLM alone can supply globally total semantic authorization for an
> arbitrary proposal class. A system may issue a bounded authorization
> only relative to an externally fixed contract and trusted replay
> boundary, or it must emit `unknown` / `open` outside that boundary.

This is stronger than “LLMs sometimes hallucinate” and narrower than
“LLMs can never establish anything.” It applies equally to a human,
compiler, theorem prover, or workflow engine asked to serve as a total
semantic authorizer of arbitrary programs.

### 4.1 The Chinese Room as a bounded illustration

Searle's Chinese Room is useful here as an illustration of a different
question, not as a premise about consciousness. A system can return
symbols that are acceptable to an external reader without its output
alone demonstrating which semantic interpretation, evaluation path, or
authorization rule made the answer reliable. That is structurally close
to the present concern: surface linguistic fit does not bind a claim to
an adequate semantic contract.

The analogy must stop there. The Chinese Room argument concerns
intentionality; this paper concerns sound-and-complete authorization.
It does not infer that LLM output is random, that a linguistic system
lacks understanding, or that a symbol-matching system cannot pass a
real external check. It only says that an output string, considered by
itself, underdetermines the route from proposal to licensed conclusion.

For an LLM, the “monkeys happened to type Shakespeare” intuition is a
useful negative control: an externally recognizable output can exist
without the output itself carrying a proof of its production history or
semantic adequacy. A replayable authorization must bind that history and
adequacy through a declared checker; otherwise several incompatible
histories remain consistent with the same string.

## 5. A constructive architecture

The theorem tells us what an honest authorization path must expose.

```text
proposal source
    -> immutable proposal bytes
    -> independent parser and contract selector
    -> replay checker / proof kernel
    -> evidence receipt bound to inputs and toolchain
    -> terminal policy owner
    -> scoped authorization or open result
```

“Independent” here has concrete tests.

- The proposal cannot select a parser that changes the meaning of its
  own bytes.
- The proposal cannot substitute the checker or schema after the policy
  has bound it.
- A replay receipt binds artifact bytes, checker version, command,
  declared assumptions, and outcome.
- The terminal policy states whether a passing local check licenses a
  deployment, publication, payment, or merely a narrower next step.
- The trust base is named rather than silently absorbed into a model
  confidence score.

The present finite rooted model makes a small structural instance of
this boundary executable. It supplies a `TrustRoot` separately from a
`Submission`, issues a receipt only from the rooted verification result,
and replays only when the observed submission matches the receipt's
bound submission. In that model, a source-supplied `selfPass` field, a
checker substitution, a schema or contract-version substitution, and a
post-receipt payload substitution are rejected. It also proves that a
terminal policy is not selected by verification. The equality is
structural equality, not a cryptographic digest; this is deliberately
not a claim about collision resistance, verifier soundness, custody, or
deployment security.

The adjacent bounded packet is a separate, stronger engineering
exemplar. It uses actual bytes and SHA-256 digests rather than the
structural equality of the Lean model, runs its evaluator, and replays a
target-local two-source Lean closure. It rejects twenty-one tested
substitutions and keeps the terminal open. It is still not a custody
proof, a collision proof, a general protocol, or evidence that the
evaluator and Lean model have identical semantics. Those are named
assumptions or later proof obligations, not effects of the packet's own
success.

This architecture does not make the trust base infallible. It makes the
base inspectable, shrinkable, replayable, and replaceable. Global
semantic certainty remains unavailable without assumptions; local
certainty is conditional on a stated boundary.

## 6. Existing CODA evidence and the new contribution

The source map in `evidence/source_map.md` separates four things that
must not be conflated.

1. PO-000 already proves a report/fiber factorization obstruction. AIT
   repeats no paper claim and does not modify PO-000.
2. NSA-000 proves a symmetry-based unforced-selection result but keeps
   a general evaluation-and-authorization impossibility theorem open.
3. The authority-firewall work mechanically separates two terminal
   types, while retaining verifier soundness as an external trust-root
   problem.
4. `19L57G1@sealed-derivation-v1` records a rigorous mechanical replay
   and explicitly says that its gates do not establish semantic
   correspondence or the strongest defensible mathematical conclusion.
5. PO-022 and PO-023 already formulate the finite-presentation and
   stop-bit projection questions. Their current Lean companions are
   explicitly `True` scaffolds, so they are inherited as research
   designs and scope fences, not as mechanized support for this paper.
6. The rooted structural replay model is now accompanied by a bounded
   byte-bound packet. The latter rejects source-controlled pass fields
   and named substitutions for its finite carrier, but it leaves custody,
   hash collision resistance, evaluator correspondence, and deployment
   security open.

The new contribution is a single theorem program joining these ideas
without pretending they are already one theorem: a finite information
theorem, finite replay-packet binding model, a class-relative reduction
transport, a computability lift, a metatheoretic closure limit, and a
future attacked authorization protocol.

## Falsifiability and proof program

The proof program is intentionally sequential. Every later claim has a
named earlier carrier, theorem, and evidence obligation. See
`proof_program.md` and `goals.yaml`.

The central finite theorem is falsified by either of the following:

- a Lean counterexample to
  `split_fiber_blocks_total_authorization`; or
- a report-only decision function that is equal to a validity predicate
  on a split report fiber.

The global semantic theorem is falsified by a total computable sound and
complete decider for a nontrivial extensional property of arbitrary
programs. Such a construction would contradict Rice's theorem, so a
claimed counterexample must identify which Rice hypothesis fails.

The architecture claim is not falsified merely because a checker shares
a machine or an organization with a producer. It is falsified if a
proposal-controlled evidence interface is shown adequate for a
contract-relevant predicate despite a demonstrated split fiber.

## 8. Nonclaims

- This paper does not claim that local proofs, finite certificates, or
  restricted contracts cannot be authorized.
- It does not claim that a separate human is required for every local
  check. A trusted kernel can be automated.
- It does not claim that all external evaluators are independent, sound,
  or safe.
- It does not turn a replay receipt into semantic truth or public
  authority.
- It does not treat the finite replay model's structural equality as a
  cryptographic binding, a custody proof, verifier soundness, or
  deployment security.
- It does not treat the bounded SHA-256 packet as self-authentication,
  a collision-resistance proof, an independent-custody receipt, or a
  proof that the PowerShell evaluator and Lean model have identical
  semantics.
- It does not prove the Rice or Goedel lifts in local Lean yet. They are
  standard results cited with their exact hypotheses and are queued as
  successive formalization targets.
- It does not redefine, resolve, or claim evidence about P versus NP.
  Fixed-witness verification is treated only as a bounded contract case.
- It does not assert consciousness, intent, moral standing, or policy
  rights for LLMs.

## References

- Turing, A. M. (1936--37). *On computable numbers, with an application
  to the Entscheidungsproblem*. Proceedings of the London Mathematical
  Society, s2-42(1), 230-265.
  [DOI](https://doi.org/10.1112/plms/s2-42.1.230)
- Rice, H. G. (1953). *Classes of recursively enumerable sets and their
  decision problems*. Transactions of the American Mathematical Society,
  74, 358-366. [DOI](https://doi.org/10.1090/S0002-9947-1953-0053041-6)
- Goedel, K. (1931). *Ueber formal unentscheidbare Saetze der Principia
  Mathematica und verwandter Systeme I*. Monatshefte fuer Mathematik und
  Physik, 38, 173-198. [DOI](https://doi.org/10.1007/BF01700692)
- Loeb, M. H. (1955). *Solution of a problem of Leon Henkin*. Journal of
  Symbolic Logic, 20(2), 115-118. [DOI](https://doi.org/10.2307/2266895)
- Necula, G. C. (1997). *Proof-carrying code*. POPL '97, 106-119.
  [DOI](https://doi.org/10.1145/263699.263712)
- Searle, J. R. (1980). *Minds, brains, and programs*. Behavioral and
  Brain Sciences, 3(3), 417-457.
  [DOI](https://doi.org/10.1017/S0140525X00005756)
- Carroll, J. H. (2026). PO-000 authorization boundary source, local
  replay binding in `projection_obstruction/projection_obstruction_paper`.
- Carroll, J. H. (2026). `19L57G1@sealed-derivation-v1`
  (`3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`), cited as a sealed
  mechanical verification record only.

**AuthorityEffect:** None.
