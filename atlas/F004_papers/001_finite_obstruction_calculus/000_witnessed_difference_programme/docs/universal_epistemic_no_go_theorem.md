# The epistemic no-go theorem: corrected statement, proof status and code

Document `WDP-DOC-EPIS-NOGO-001`. **AuthorityEffect:** None. Date 2026-10-16.

This note replaces the draft of the same identifier that accompanied the
mission specification. The specification's title claims a scope covering every
physical cognition; this note argues the weaker and more defensible thing, that
the theorem is substrate-indifferent by the form of its hypotheses. Every claim
below carries one of five tags:

- **PROVED HERE**: a written proof in this note, or an exact replayable
  computation in the cited module, decides it.
- **COMPUTED**: decided on the six pinned fixture models only.
- **IMPORTED**: taken from outside the programme and used as a hypothesis or an
  analogy; nothing in the code depends on it.
- **DEFINITIONAL**: true by a definition this programme has adopted; enforced
  by code, not discovered by it.
- **FALSE**: a statement of the draft note or of the accompanying "key
  findings" that does not hold as written, with the correction.

The code is `omega_sheaf_theory::epistemic_observer` and
`omega_contracts::three_role_authority` in `omega_engine/crates_rs`, built on
the exact empirical-presheaf module `omega_sheaf_theory::empirical_presheaf`
of the companion branch, and the reference harness
`omega_engine_pfp/tests/normal_forms/test_epistemic_no_go_harness.py`. Section
7 lists the commands, versions and exit statuses.

## 1. Postulates

The theorem has four hypotheses. None is derived; each names where it comes
from.

**P1 (co-evaluable contexts).** A finite set of questions, each with a finite
outcome set, and a cover by maximal contexts, the sets of questions that one
evaluation can answer together. The observed data is an empirical model: one
distribution per context over its joint outcomes, with agreeing marginals on
overlaps (no-signalling). IMPORTED as a definition (Abramsky and Brandenburger,
2011). The module checks no-signalling exactly and refuses a signalling table
with a typed error; it does not assume it.

**P2 (private fiber).** An observer reports through a boundary map
$\pi: K \to B$ whose kernel is not zero. The module refuses to declare an
observer whose boundary dimension equals its state dimension. The physical
readings offered for P2 (Bekenstein bound, Landauer cost, Holevo bound) are
IMPORTED and are used nowhere in a proof; P2 is a postulate about the declared
observer, and whether a given brain, model or prover satisfies it is an
empirical claim about that system, not a theorem.

**P3 (self-reference bridge).** A system that is to certify its own factual
correctness must carry an internal truth predicate for its own carrier.
IMPORTED (Tarski; Löb). This note uses P3 only to say what the draft's clause
III cannot say without it (section 2.III).

**P4 (three roles).** A claim becomes admitted for authorization only through
a packet naming a proposer, an evaluator and an authorizer, whose authority
descends from an admitted root of trust external to the packet.
DEFINITIONAL: `WDP-CH15-D01` and the authority packet of chapter 15. The
separation is a policy a jurisdiction adopts, which the code then enforces.

## 2. The theorem, clause by clause

**Theorem (epistemic no-go, corrected).** Let an observer satisfy P1, P2 and
P4. Then:

**I. No context-free joint prediction on a contextual table.** Let $e$ be a
no-signalling empirical model over the cover. Exactly one of the following
holds, and the module decides which with a replayable certificate:

- a joint distribution over global assignments marginalises to every context
  of $e$ (the verdict `GlobalSection`, carrying the joint, which the module
  re-marginalises before returning it); or
- no such joint exists, and the exact $L^1$ distance
  $d = \min_p \lVert A p - e \rVert_1 > 0$ from the noncontextual polytope is
  attained, together with a dual vector $y$ of sup-norm at most one with
  $\langle y, e\rangle - \text{offset} = d$ (a Bell functional), so that every
  noncontextual joint mispredicts $e$ by at least $d$ in $L^1$.

PROVED HERE. The dichotomy is linear-programming strong duality over
$\mathbb Q$; the companion module solves the primal and dual exactly and the
kernel re-verifies the receipt (`verify_l1_defect`) before it is reported. Two
refinements of the obstructed case are decided by enumeration of the support
presheaf: *strong* contextuality (no global assignment lies in every context's
support, so the defect is forced positive) and *logical* contextuality (some
supported local section has no supported global extension). For the strong
case on a parity-shaped model the module also returns the parity cut, the
subset of contexts whose $\mathbb F_2$ constraints sum to $0 = 1$, which is the
finite counterexample of WDP section 15.5 named by its contexts.

Scope. Clause I obstructs *noncontextual* predictive models, those that answer
every question from one joint distribution regardless of which other questions
are asked alongside. A predictor that carries the context, as a quantum state
with a measurement setting does, reproduces the table. The clause is a bound on
a class of world-models, not on prediction as such. (The draft's reading, "no
world-model exists", is FALSE as stated; see section 5.) In the author's
words (2026-10-16): contextuality excludes one global representation, a joint
distribution reproducing the contextual statistics; a system can still
understand and represent the contextual structure, and the kernel's verdict,
with its table, its defect and its dual witness, is such a representation.
Every sentence of this note that says "obstructed" is to be read at that
width and no wider. A unified representation of many contexts does not
thereby supply a context-independent assignment of all their outcomes; a
system can hold the whole specification of a contextual model, obstruction
included, without holding a global assignment that does not exist, and
Abramsky and Brandenburger make that distinction explicit. Bell is therefore
not a quantum analogy attached to a classical argument: in a foundation whose
primitive question is which local accounts can be combined, Bell is the
rigorous instance in which the demanded combination fails. What this note
does not do is establish the corresponding obstruction for the particular
claims a self-presenting reasoner makes about itself; that is the open
research task named in section 8.

**II. No perfect peer prediction from the boundary.** If
$\ker \pi \ne 0$, there are two states with the same boundary report, so any
predictor of the peer that reads only the boundary assigns one prediction to
two states and is wrong on at least one of them. PROVED HERE, and it is a
triviality of linear algebra once P2 is granted; the content of the clause is
P2 itself. Wolpert's inference-device theorem (that no device in a world can
strongly infer every other device in it) is IMPORTED as the general background
and is neither used nor re-proved here. The AMC Lean "intersubjective privacy"
theorems cited by the draft are integer toy models that *assume*
$\dim \mathrm{Fib} > 0$; they instantiate P2, they do not establish it.

The clause is an instance of a lemma that needs no vector space and no
`NB-9`, stated by the author (2026-10-16) as the foundation to use instead.
*Fiber lemma.* Let $E: W \to K$ be everything available to a system for one
decision and $q: W \to A$ the answer sought. If $E(w) = E(w')$ and
$q(w) \ne q(w')$, then there is no $f: K \to A$ with $f \circ E = q$:
$f$ receives one input in both cases and cannot return two answers. PROVED
HERE (the harness checks it by exhausting every $f$ on a small instance).
Internal computation of any depth is a choice of $f$ and leaves the
obstruction where it is while $E$ is fixed. What the lemma does not supply is
its premise: that two worlds with the same $E$-image and different answers
exist is the substantive obligation of each application, and clause II meets
it only for the one-step boundary map of P2.

That is also where the clause stops short of privacy. The kernel of
$\pi$ is an *instantaneous* statement. A coordinate hidden now need not stay
hidden: with $\pi(a, b) = a$ and dynamics $F(a, b) = (b, a)$ the hidden $b$ is
the next report (the author's example; the harness records it). Permanent
privacy is indistinguishability under every allowed observation history and
intervention, and the draft's Proposition 2.4 asserts that stronger statement
from the instantaneous kernel alone. That step is OPEN here: the Rust
`BoundaryProjection` and `private_fiber_dim` are one-step objects, and the
note claims nothing about a peer observed over time.

**III. No self-grounding.** What this programme can state and support:

- An observer's own evaluation of its own claim carries `AuthorityEffect:
  None` (DEFINITIONAL, `ENC-0195`; enforced by the receipt types).
- An observer's ledger of its own evaluations cannot establish its own
  completeness: a truncated tail is a consistent prefix, and completeness is
  decidable only against a tip pinned outside the ledger. PROVED HERE and
  COMPUTED (`verify_ledger`, `complete_against`; the integration test
  truncates and tampers).
- `WDP-CH14-T01` is cited at its declared scope (`WDP-CH14-N03`): autonomous
  syntactic processes without external grounding. Its Axis 1 rests on
  `collapsed_of_no_insts`, which is an admitted result. Its Axis 2 cites a
  "Lemma D" that this note could not source, and its Axis 3 cites `NB-9`, which
  the programme's own notebook review has refuted; those two axes are therefore
  not usable as proved steps here.
- Axis 3 (relabeling blindness), restated with its hypothesis. Let $G$ be the
  group of presentation relabelings of a carrier $K$. A verdict $V$ on carriers
  cannot separate $K$ from $gK$ *when $V$ is $G$-invariant, or factors through
  a $G$-invariant export*; under that hypothesis the statement is a one-line
  consequence of invariance (PROVED HERE, and it is the form the author's
  §3.3 states: "any functional on carriers that is $G$-invariant cannot
  distinguish $K$ from $gK$"). Without the hypothesis it is FALSE: take two
  carriers swapped by a relabeling $\sigma$ and the verdict "the first token
  is `a`"; it is a function of the carrier and it separates the pair
  (countermodel recorded in the author's review of the companion branch,
  2026-10-16). So Axis 3 bounds invariant verdicts, not verdicts. The
  companion note FOC-035 (section 3.1) derives the axis from `NS-14` and
  `CL-13` alone, with `NB-9` dropped, under exactly that hypothesis made
  explicit as a *declared export*: the verdict reads a history only through
  an export built from receipts read up to renaming and from conserved
  charges, so $V = \bar V \circ \mathrm{Exp}$ with $\mathrm{Exp}(\sigma H) =
  \mathrm{Exp}(H)$. This note takes that derivation as it stands and keeps its
  two claims apart, as the author's reply of 2026-10-16 asks: (1) an invariant
  defect can be detected by internal computation whenever the supplied data
  determine it, and (2) a relabeling cannot change that defect. Both hold.
  The kernel is the witness for (1): the defect is a function of the table
  alone (clause I), the table is the supplied data, and the kernel computes
  the defect from it with no interaction beyond reading the table; (2) is the
  permutation of the polytope onto itself. The draft slides from (2) into
  denying (1) ("token manipulation cannot detect quotient defects"); that
  denial is FALSE for defects the data determine. What Axis 3 adds is
  narrower than either claim, and it is an instance of the fiber lemma of
  clause II with the indistinguishable pair exhibited: $H$ and $\sigma(H)$
  have the same export, and the question "do the tokens of this history
  denote what the tokens of that one denote" is answered differently by a
  nontrivial $\sigma$ on grounded tokens. So a drop in the internal defect is
  certified as a drop, and what no export-reading verdict decides is whether
  the drop is a repair (the same referents, a smaller defect) or a
  reinterpretation (new referents under old tokens). That is a question about
  the grounding map, which lives in a declared observer outside the system.
  Internal computation cannot change $E$; it can read what $E$ already
  carries.
- The Tarski and Löb forms of the clause (no consistent system derives its
  own soundness predicate; a system that derives "if I derive $\varphi$ then
  $\varphi$" derives $\varphi$) hold only under P3, which is IMPORTED. The draft's
  rendering of Löb is misstated (section 5).

**IV. No self-granted authority.** A provenance packet in which the proposer is
the authorizer, or the evaluator is the authorizer, is refused before any
mathematics is consulted; so is one whose authorizer's standing is prose
rather than a certificate, one whose root is not admitted, and one whose root
is the proposer or the evaluator themselves. DEFINITIONAL and enforced:
`verify_three_role_authority` returns a typed `ThreeRoleRefusal` and never a
receipt in those cases, and under the regime policy that admits
self-authorization the receipt still carries `AuthorityEffect: None`. The
companion Python gate `ThreeRoleGate` enforces the role separations and the
admitted root over the same cases (section 6 says which layer refuses which
case). Authority is a license granted from an admitted root; it is not a
property of the proposer's competence, and no verdict of clauses I to III
changes a packet's standing. The clause does not say that a system may never
authorize anything: an authorization executed inside a system is valid when
the standing it acts under was delegated to it earlier by an admitted root,
and the contract models exactly that case (the regime policy that admits
self-authorization issues the receipt, still marked `AuthorityEffect: None`
on the evaluation). What the system cannot supply from its own intelligence
is the delegation. The premise is the regime, as WDP §15.1 has it: the bridge
from a proof or a measurement to a permission is a jurisdictional choice.

**Substrate indifference.** The hypotheses mention a cover, a boundary map, a
ledger and a provenance packet. Nothing in them names neurons, weights, or
proof terms. So the theorem applies to a brain, a language model, a proof
assistant or a hypothetical superhuman system exactly when that system is
described by P1, P2 and P4, and the description is the empirical step that this
note does not take. "Invariant across all physical cognition" is therefore a
statement about the form of the hypotheses (PROVED HERE, by inspection), not a
statement about every physical system (not claimed).

## 3. The topological derivation, corrected

The draft derives clause I from a nonzero Čech $H^1$ of the cover. Three
things must be separated.

1. **Nerve cohomology is a cover invariant.** On the Bell cover (four
   contexts, overlapping in a four-cycle) the rational $H^1$ of the nerve has
   dimension one for *every* model: the PR box, the classical mixture, the
   deterministic table, the near-Tsirelson table and the Hardy-type table all
   return `nerve_h1_dim = 1`. Two of those five are global sections (the classical mixture and the deterministic table). The near-Tsirelson and Hardy-type tables still support global assignments; the PR box supports none.
   COMPUTED on the fixtures, and expected: the nerve does not see the
   distributions. The module reports the number as a cover invariant and
   never as evidence of contextuality.
2. **The obstruction lives in the presheaf, not in the cover.** For
   parity-shaped supports the obstruction is a 1-cocycle of the support
   presheaf with $\mathbb F_2$ coefficients, and the parity cut names the
   contexts that carry it (the triangle of section 15.5: cut $\{0,1,2\}$; the
   PR box: cut $\{0,1,2,3\}$). For general distributions the obstruction is the
   $L^1$ defect with its dual witness. Both are exact and replayable. The
   Abramsky–Brandenburger cohomological obstruction is sufficient but not
   necessary for contextuality (IMPORTED; there are contextual models with
   vanishing cohomological obstruction), which is why the module decides by
   the LP and not by cohomology.
3. **Descent, and one name with two meanings.**
   `omega_category_theory::finite_report_descent` classifies the cover; on the
   maximal cover every fiber is a `NoGlobalExtension` or a matching family,
   and the kernel asserts that a strong obstruction produces no `Unique` and
   no `Ambiguous` family. The companion branch records that *its*
   `NoGlobalExtension`, the cover-gluing verdict on the maximal cover, is a
   restatement of "no supported global assignment" and not an independent
   witness (FOC-035, L035-B6 and L035-B7). The module generated on the author's
   workstation (`epistemic_nogo.rs`, 2026-10-15) uses the same name for a
   different object: there `DescentOutcome::NoGlobalExtension` is returned
   either by exhaustive non-extendability of a local section over all global
   assignments (its `logical_contextuality`, which is complete for logical
   contextuality) or by a Farkas certificate found by a floating-point
   nonnegative least-squares solve and re-checked in floating point, with
   `Undetermined` otherwise. L035-B6 and L035-B7 are about the cover-gluing
   verdict and say nothing against the exhaustive form. The exhaustive form
   is what this kernel computes exactly, through `global_support` and
   `logical_contextuality_witness` (the Hardy-type fixture's unextendable
   section is its output). What is not adopted is the floating-point branch:
   a certificate re-verified in `f64` is not a witness under the programme's
   exact-arithmetic rule, and the module's `Undetermined` outcome is the
   price of that choice, where this kernel's rational LP always terminates
   in a verdict or a typed refusal. The gap between the two modules is
   certification, not topology.

Fine's theorem (for the two-party, two-setting, two-outcome scenario, a joint
distribution exists exactly when all eight CHSH inequalities hold) is IMPORTED
and CHSH-specific. The harness re-derives the classical bound 2 by enumerating
the sixteen deterministic strategies and checks that the near-Tsirelson fixture
attains $14/5 > 2$, which certifies its positive defect independently of the LP.

## 4. The knife with one cut (demarcation)

**Combinatorial competence** is what a system can do inside a context: answer
questions, compose answers, search, prove, predict, compress. It is measured by
witnesses and costs, it is unbounded in principle, and nothing in this note
caps it.

**Self-grounding sovereignty** is the standing to make one's own answers
admitted: to be, for one's own claims, proposer, evaluator and authorizer at
once. This note says that no amount of the first buys the second, because the
second is not a capability. It is a license, and a license is issued by a root
outside the licensee, recorded in a packet whose three roles are held by three
parties, revocable by the procedure that issued it.

The cut is between a *verdict* and a *standing*. A verdict is what the kernel
returns: a global section with its joint, or an obstruction with its defect and
dual witness, or a typed refusal. A standing is what a jurisdiction grants to a
packet. The kernel's receipts all carry `AuthorityEffect: None`, and the
contract refuses, before reading any verdict, every packet in which the
proposer or the evaluator holds the authorizer's seat.

So: competence is intrinsic and graded; authority is social, institutional and
cryptographic, granted from an admitted root of trust, and never an intrinsic
property of the system that holds it. A system that grows in competence does
not approach sovereignty; it approaches nothing on that axis, because there is
no path on that axis that starts inside the system.

The author's formulation of the cut (2026-10-16), adopted here as the
theorem's one-sentence reading:

> A unified self-presentation supplies neither a guarantee of complete
> knowledge nor an independent source of authority. Each claim still requires
> sufficient evidence; each permission still requires standing under the
> applicable authority regime.

Calling the presentation "I" or "ASI" adds no evidence and no standing; being
able to use those names is also not enough to trigger an incompleteness
theorem, whose hypotheses (P3) must be established per system.

## 5. Corrections to the draft

- "A nonzero Čech $H^1$ of the context cover obstructs a global world-model."
  FALSE as a witness: section 3, item 1.
- "$\partial[\gamma]/\partial N = 0$" (the obstruction class does not vary with
  the number of parameters $N$). The expression is not defined: $[\gamma]$ is
  a cohomology class of a fixed presheaf, $N$ is not a coordinate of anything
  it depends on. The intended content, that the obstruction is a property of
  the table and not of the predictor's size, is PROVED HERE in the form of
  clause I (the defect is a function of $e$ alone).
- "No world-model exists" (Pillar I). FALSE as stated; corrected to "no
  noncontextual joint predictive model reproduces a contextual table, and
  every such model misses by at least $d$".
- Wolpert's theorem as a proved step. IMPORTED; clause II establishes only the
  finite boundary statement under P2.
- "AMC Lean intersubjective-privacy theorems establish the private fiber."
  FALSE: they assume it (section 2.II).
- "`AuthorityEffect: None` is Löb's theorem expressed as a type." FALSE. The
  tag is a value on a receipt enforced by `omega_contracts::no_authority`; no
  fixed point and no provability predicate are involved. Löb's theorem says
  that if a theory derives $\Box\varphi \to \varphi$ then it derives $\varphi$;
  the draft's paraphrase ("a system cannot prove its own soundness") is Gödel's
  second theorem's neighbourhood, not Löb's, and both require P3.
- `WDP-CH14-T01` Axes 2 and 3 as proved steps. Not usable here (section
  2.III).
- "Definition 4.1: PairwiseDistinct(P,E,A) and A chains to root $R \notin
  \{P,E\}$" and "Proposition 4.3 (self-authorization collapse)". DEFINITIONAL,
  kept, and enforced by code; they are not theorems about cognition.
- Pillar IV as a mathematical consequence of Pillars I to III. FALSE: it is a
  normative definition (Article 002), independent of the other three.

The author's own revision of the note (`WDP-DOC-EPIS-NOGO-001`, dated
2026-10-15, posted 2026-10-16) keeps several of the statements above and adds
a few; the differences that matter:

- "$\check H^1(\mathcal U, \mathcal E) \neq 0$ for every contextual $e$"
  (its §3.2). FALSE for the Čech obstruction of the support presheaf: the
  `near_tsirelson` fixture has full support (sixteen supported global
  assignments), so its support presheaf has a global section and the
  obstruction class vanishes, while its $L^1$ defect is $4/5$ and its CHSH
  value $14/5$. The author's longer prose states the correct form (the
  obstruction class is sound, not complete, for contextuality) and the
  generated output from which the note was condensed records $\gamma = 0$ for
  the Tsirelson box; the condensation dropped the qualifier. The nerve $H^1$
  is a different object again (section 3, item 1).
- "an optimal dual circulation witness with zero rational duality gap" (its
  §3.2). The statement is true of a rational LP and is what this kernel
  returns; the author's generated module does not compute it (its certificate
  is a floating-point Farkas vector, section 3, item 3), so the sentence
  describes this branch's code and not the code the note's §8 cites.
- Its §8 reports 19 Rust and 25 Python passes on the author's workstation.
  Those runs are not reproduced here and are not cited as evidence; the
  receipts this note stands on are in section 7. The two of its cases that
  carry information beyond the six fixtures are ported as the two
  `refusals` of section 6. Its `file:///` links are host-absolute and do not
  resolve outside that workstation.
- Its Theorem 1.2 (in the longer prose) is the Abramsky–Mansfield–Barbosa
  obstruction class of the *support* presheaf. It is not the nerve $H^1$ of
  the cover, and the two must not be read as one object.
- Its Proposition 4.3 (self-authorization collapse) is derived from its
  Corollary 3.3, which rests on Löb and so on P3. In this note the same
  statement is DEFINITIONAL and needs no P3: the contract refuses the packet
  by its role fields, before any logic is consulted.
- Its Axis 3 cites `NB-9` as a passage-charge result; `NB-9` is refuted, and
  the axis is restated above with the hypothesis that makes it hold. The
  author (2026-10-16) treats the `NB-9` citations in the prompt and in the WDP
  snapshot as stale dependencies; the fiber lemma of clause II is the
  replacement foundation, and it cites nothing.
- Its Proposition 2.4 (private fiber) derives permanent privacy from the
  instantaneous kernel. OPEN: clause II states the gap and the swap-dynamics
  witness.

## 6. Evidence: the fixtures

`omega_engine/crates_rs/tests/omega_sheaf_theory/fixtures/epistemic_no_go/empirical_models.json`
(schema `omega.epistemic_no_go.empirical_models.v1`). The Bell models use
questions $a_0, a_1, b_0, b_1$ with the four contexts $\{a_i, b_j\}$.

| model | verdict | $L^1$ defect | parity cut | nerve $H^1$ | supported globals |
| --- | --- | --- | --- | --- | --- |
| `pr_box` | Strong | 2 | {0,1,2,3} | 1 | 0 |
| `classical_mixture` | GlobalSection | 0 | none | 1 | 2 |
| `deterministic_zero` | GlobalSection | 0 | none | 1 | 1 |
| `near_tsirelson` (CHSH $14/5$) | Probabilistic | 4/5 | none | 1 | 16 |
| `wdp_15_5_triangle` | Strong | 2 | {0,1,2} | 1 | 0 |
| `hardy_type` | Logical | 1/3 | none | 1 | 5 |

The Rust test replays every dual witness; the Python harness re-derives the
supported globals, the parity cuts, the nerve ranks over $\mathbb Q$, the CHSH
values and a marginalising joint for the global-section rows, without calling
the Rust code.

The same file carries two `refusals`, inputs on which the kernel returns a
typed refusal and no verdict. Both are ported from the test cases of the
author's workstation module (section 5):

| case | input | refusal |
| --- | --- | --- |
| `signalling_family` | Bell cover; $a_0b_0$, $a_1b_0$, $a_1b_1$ fully correlated, $a_0b_1$ fixes $a_0 = 0$ | `Signalling`: contexts 0 and 1 disagree on $a_0$ ($1/2, 1/2$ against $1, 0$) |
| `oversized_singletons` | 21 binary questions in 21 singleton contexts | `EnumerationLimit { limit: 2^20 }`: $2^{21}$ global assignments |

The first is the $\check H^0$-level failure the author's prose separates from
contextuality: the tables are not a presheaf, so no question of gluing arises,
and the kernel says so before any verdict. The second is the kernel's declared
cap, hit without enumerating. The harness checks the disagreeing marginals
and the bound arithmetically, and a third harness test aggregates the PR box
from four peer agents who each hold one context exactly: the aggregator has
every local section and still no supported global assignment, and the same
peers glue once the $a_1b_1$ report is replaced by the correlated table.

`omega_engine/crates_rs/tests/omega_contracts/fixtures/epistemic_no_go/provenance_cases.json`
(nine cases). Which layer refuses each:

| case | Rust contract | Python gate |
| --- | --- | --- |
| distinct roles, admitted root, certificate | receipt (`AuthorityEffect: None`) | admitted |
| proposer is authorizer | `RefuseSelfAuthorization` | `SELF_AUTHORIZATION` |
| evaluator is authorizer | `RefuseSelfAuthorization` | `EVALUATOR_IS_AUTHORIZER` |
| proposer evaluates itself | `RefuseSelfEvaluation` | `EVALUATOR_IS_PROPOSER` |
| prose declaration of authority | `RefuseProseAuthority` | admitted (no basis field) |
| no admitted root | `RefuseNoExternalRoot` | `UNADMITTED_ROOT` |
| root is the proposer | `RefuseNoExternalRoot` | admitted (root not compared to parties) |
| regime permits self-authorization | receipt (`AuthorityEffect: None`) | `SELF_ATTESTED`, never admitted |
| empty identifier | `RefuseMalformed` | `EMPTY_IDENTIFIER` |

The two rows the gate admits are refusals the Rust contract adds; the
harness pins that difference so that it is a recorded gap, not a silent one.

## 7. Reproducibility

Run from `omega_engine/crates_rs` (Rust) and the repository root (Python).

| command | tool version | exit | scope |
| --- | --- | --- | --- |
| `cargo test -j 1 -p omega_sheaf_theory --lib epistemic_observer` | cargo 1.97.0, rustc 1.97.0 | 0 | 5 unit tests |
| `cargo test -j 1 -p omega_sheaf_theory --test epistemic_observer` | cargo 1.97.0 | 0 | 8 fixture tests |
| `cargo test -j 1 -p omega_contracts --test three_role_authority` | cargo 1.97.0 | 0 | 4 fixture tests |
| `pytest omega_engine_pfp/tests/normal_forms/test_epistemic_no_go_harness.py -q` | pytest 9.1.1, Python 3.13.16 | 0 | 22 tests |
| `ruff check --select F,I,E,W,E501 omega_engine_pfp/tests/normal_forms/test_epistemic_no_go_harness.py` | ruff 0.16.8 | 0 | one file |

## 8. Nonclaims

- Nothing here bounds competence: no capability ceiling is stated or implied.
- Nothing here is a statement about any particular brain, model or prover;
  the hypotheses must be checked per system.
- The physical imports (Bekenstein, Landauer, Holevo, Bell violations,
  Wolpert) motivate P1 and P2; no proof here uses them.
- No Lean is elaborated for this note; the Lean citations of the draft are
  discussed, not rebuilt.
- Every receipt, verdict and ledger entry of the code carries
  `AuthorityEffect: None`; a `GlobalSection` verdict admits nothing.
- The author's workstation module is not merged here. Not ported from it:
  the floating-point Farkas branch, the floating-point boundary projection
  and the `interact` numerics of its Pillar II, its keyed-hash receipts, and
  its Tsirelson box at $1/\sqrt 2$ (irrational, not representable in an exact
  fixture; `near_tsirelson` at $14/5$ stands in). Its `pr_box` and
  `classical_box` tables are the fixtures `pr_box` and `classical_mixture`
  already here.
- Axis 3 is stated for relabeling-invariant verdicts only; nothing here
  bounds a verdict that reads the presentation.
- Nothing here says a system cannot know something about itself, or cannot
  exercise authority delegated to it. The fiber lemma obstructs only answers
  the available data do not determine; the contract refuses only standing
  the packet does not carry.
- Privacy over time (the draft's Proposition 2.4) is not established; the
  kernel of the boundary map is a one-step statement.
- OPEN (the author, 2026-10-16): the obstruction of clause I is established
  for empirical models on a cover of question contexts. Whether the claims a
  self-presenting reasoner makes about its own states form such a model, and
  whether their demanded combination fails in the same way, is a research
  task this note names and does not discharge.
