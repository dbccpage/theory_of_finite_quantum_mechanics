# Curriculum: 001 Genesis

**AuthorityEffect:** None.

Eight lessons, about five hours of study including the video (about 30
minutes). Genesis here means the external `19L57G1` study, pinned at
`dbccpage/19L57G1@sealed-derivation-v1` (commit `3100c4e`). Its Lean proofs live
in that repository, not in this one; this strand teaches what the sealed study
established and labels everything else.

**Prerequisite:** [`000_pre_genesis`](../000_pre_genesis/curriculum.md).
**Next strand:** [`002_s_n`](../002_s_n/README.md).
**Main reading:** [`reading_guide.md`](reading_guide.md), [`levels/README.md`](levels/README.md),
[`genesis.md`](genesis.md) sections up to "Axiom Census". Line references to
19L57G1 are to `paper/paper.md` and `lean4/Derivation/*.lean` at the sealed tag.

Scope rule for the whole course: by repository rule, 19L57G1 is an external,
self-contained study and a conceptual analogy for the Omega Engine. It is not the
engine's mathematical foundation. The Witnessed Difference Programme keeps the
two apart (WDP Appendix L) and takes no Lean credit for the archived derivation.

---

## Lesson 1. From model behaviour to a formal regime

**After this lesson you can** say how 001 differs from 000 and state what a
claim of "forced" must declare.

**Read:** [`reading_guide.md`](reading_guide.md) lines 1 to 20.

- 000 recorded what a language model did with `<>`. 001 asks what a formal
  system can derive when it is handed only `<>`.
- "The inscription `<>` is one opaque datum in the declared source regime. Its
  printed glyphs do not supply two elements, an ordering or a relation."
- Any claim that something is forced must state the regime, the permitted
  changes, the cost measure, the isomorphism convention and the bounds.

**Exercise.** Why is "`<>` contains two symbols, so it forces a pair" not an
admissible argument? *Answer:* the glyphs are presentation; the regime treats
`<>` as one atomic datum, and nothing was declared that reads inside it.

## Lesson 2. The regime and its events

**After this lesson you can** write the five components of a regime and the six
events, and replay a history.

- A regime is R = (D, F, I, U, Q): a count of admitted data, a list of form
  arities, the admitted instances, the uniform all-tuples rules, and the
  separation requirements (`lean4/Derivation/Basic.lean`, `structure Regime`).
- Genesis is the empty regime ⟨0, [], [], [], []⟩.
- Events: `supply`, `admitDatum`, `admitForm a`, `admitInst f args`,
  `admitRuleAll f`, `impose i j`. An ill-formed admission returns nothing and
  "poisons the whole history".

**Exercises.**
1. Which of these is ill-formed on genesis: `admitInst 0 [0]`, `admitForm 0`,
   `impose 0 1`? *Answer:* all three: no form 0 exists, a form needs arity at
   least 1, and `impose` needs two admitted data.
2. Run `py -3.12 omega_engine_education/documentation/001_genesis/code/check_genesis.py`.
   What does it check? *Answer:* the text grammar of events and deltas (29
   cases), not their semantics.

## Lesson 3. Supply is not admission

**After this lesson you can** state and explain `supply_no_op` and
`genesis_underivable`.

- `stepE r (.supply t) = some r`: supplying a token changes nothing.
- Nothing is derivable at genesis. "Result: **inertia**. Exactly nothing
  follows from the initial inscription alone." (19L57G1 `paper/paper.md`, lines 192 to 193).
- Compare 000: a presentation change is not an expressive lift. Here the same
  point is a Lean theorem about a declared regime.

**Exercise.** In 000 the full replay called `<a>` "a new state". Under
`supply_no_op`, what is the regime after `supply <a>`? *Answer:* unchanged; a
supply is not an admission.

## Lesson 4. Observation and total collapse

**After this lesson you can** define contexts, plugging, derivability,
collapse and separability, and prove collapse without instances.

- A context is a form with holes; plugging fills every hole with the same datum;
  derivability is membership in the admitted instances or coverage by a uniform
  rule. "No other inference is admitted."
- `collapsed r d d'`: every well-formed context gives the same derivability for
  d and d'. `separable`: some context witnesses a difference, and the proof
  carries its witness.
- `collapsed_of_no_insts`: with no instances every pair is collapsed. Admitting
  `<a>` and `<ab>` gives two data that are externally distinct and internally
  collapsed; the number of observational classes stays 1.

**Exercise.** Relate this to 000's forced-separation argument. *Answer:* the
same shape: with no observations (here, no instances) every pair is
equivalent, so a required difference needs new judgement structure.

## Lesson 5. Two readings and the separation demand

**After this lesson you can** state Readings L and F and what a valid response
to a separation demand must do.

- Reading L: only explicit retention admits; two data, `R2L = ⟨2, [], [], [], [(0, 1)]⟩`.
- Reading F: the initial inscription is admitted at genesis; three data,
  `R2F = ⟨3, [], [], [], [(1, 2)]⟩`. The text does not decide between them, so
  both are carried (paper §11 clause (h)).
- Candidate items: `NewDatum`, `NewForm(n)`, `NewInst(f, a⃗)`, `NewRuleAll(f)`.
  A valid response applies, separates the target pair, and keeps every earlier
  requirement separated.

**Exercise.** Why do the readings have different data counts? *Answer:* F
counts the initial inscription as admitted at genesis; L does not.

## Lesson 6. The price of separation is two

**After this lesson you can** prove that one item cannot separate on a regime
with no forms and no instances, and give a cost-two response.

- μ1(Δ) = |Δ|; μ2(Δ) = (|Δ|, sum of new-form arities), compared lexicographically.
- `cost1_insufficient_general`: no response of zero or one item is valid when
  there are no forms and no instances. A form alone observes nothing; an
  instance needs a form.
- `deltaU0 = [newForm 1, newInst 0 [0]]` gives `U0 = ⟨2, [1], [(0, [0])], [], [(0, 1)]⟩`,
  separated by the context `⟨0, [none]⟩`: datum 0 has the mark, datum 1 does not.
- The value 2 "is a property of the declare-then-assert grammar" (WDP CH03-P03),
  not a universal constant.

**Exercise.** Why is "declare a unary form and assert it of datum 0" cost 2 and
not 1? *Answer:* the form and the instance are separate items; bundling them
into one "step" hides one of them.

## Lesson 7. Ties, isomorphism and a declared choice

**After this lesson you can** reproduce the class counts and explain why choosing μ2 is a premise, while uniqueness under that measure is a result.

- Under μ1, within `max_items 2, max_arity 2`: Reading L has 6 valid deltas in 3
  isomorphism classes (unary mark, binary link, binary self-loop); Reading F has
  10 in 5. For every arity k the k-ary mark is also minimal, so the μ1 tie class
  is countably infinite.
- Under μ2 the minimum is (2, 1), the unary mark, unique up to isomorphism. The
  two μ2 deltas mark datum 0 or datum 1; swapping the data makes them one class,
  so no swap-respecting rule can prefer one.
- Choosing μ2 is a declared act. The soundness of the isomorphism canonicalizer
  in general is open (`CL-ISO-SOUND`).

**Exercise.** Replay the enumeration with 19L57G1's
`code/derivation/engine.challenge3_report` for both readings at bounds (2, 2)
and match: L μ1 → 6 valid, 3 classes; L μ2 → 2 valid, 1 class; F μ1 → 10 valid,
5 classes; F μ2 → 2 valid, 1 class.

## Lesson 8. What was declared, and what the evidence is worth

**After this lesson you can** list what the study declared rather than derived,
read the evidence grades, and state the irreflexivity law.

- Declared, not derived: the cost measures, the candidate grammar, the
  isomorphism relation, the persistence of requirements, the pair-separation
  closure policy and the external continuation policy. "No object-language
  endogenous demand generator was derived." No unboundedness is claimed.
- `irrefl_witness_ne`: if R is irreflexive and R(a, b) then a ≠ b. One point
  with R(a, a) shows the law is needed; two points with the empty relation show
  the exhibit is needed. The direction of an edge is an extra input.
- Evidence grades: NATIVE SEALED, SEALED SUPPLEMENTARY, ABSENT /
  METHODOLOGICAL FENCE, POST-SEAL THEOREM / GATED, FINITE COMPUTATION / LOCAL
  RECEIPT. Axiom census: 1,314 reports at the seal, 1,530 at `f1d56c01`, no
  `Classical.choice`, no `sorryAx`. `#print axioms` covers printed theorems only.

**Exercises.**
1. Which of these is post-seal: `supply_no_op`, `closedRun_round_bound_from_empty`,
   `cost1_insufficient_general`? *Answer:* `closedRun_round_bound_from_empty`.
2. A form contract says `verification_status: executable`. Did a check run?
   *Answer:* not necessarily; that is draft metadata (`wdp_integration.md`).

---

## What this strand does not claim

- That `<>` generates or contains structure.
- That every current engine implementation has a proved formal correspondence to the original source. Genesis remains part of the project's mathematical and engineering foundation.
- That the minimum is "the natural answer", or that μ2's uniqueness was found
  rather than chosen.
- That the 19 primitive families are a complete or faithful extraction, or that
  their Python and Lean versions are dual implementations.
- That the demos compute Čech cohomology, or prove sheaf, HoTT, Regge, Bell or
  quantum-gravity results. They run supplied illustrations.
- That historical test receipts establish current test results. The October 6 stale projection pin is repaired in this edition; fresh checks and unrun suites are recorded separately in the education audit.
