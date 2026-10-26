---
documentation_contract: education-documentation/v1
title: 'Lesson 710.04: Admission and transport'
kind: pedagogical-lesson
track: 710
status: active
claim_status: conditional-theorems-and-finite-examples
authority_effect: 'None'
---

# Admission and transport

Start with the [laboratory notebook](../notebooks/lesson_710_04_admission_and_transport.ipynb).
This lesson assumes elementary functions, directed relations and exact
rational arithmetic. It introduces no new Genesis stage.

## A difference needs evidence

[Proved] If R(a,b) holds and R(x,x) is forbidden for every admitted x, then
a and b differ. Replacing b by a would exhibit precisely the forbidden fact.
The [formal proof and countermodels](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/primitive_admission_and_transport.md)
state every input. The opaque inscription supplies no relation or law.

Work this example first. Declare `{a,b}`, R=`{(a,b)}`, and the irreflexivity
law. Then compare `{a}`, R=`{(a,a)}`: the second example has an instance but
fails the law. The empty relation on `{a}` passes the law but has no exhibit.
Neither singleton is a witnessed cut. Reverse the first edge; the result
still passes. The cut conditions do not select an orientation.

Predict whether admitting only a law can produce an exhibited difference.
Explain your answer before executing the first two notebook checks.

## Three equations, two quotients

[Declared] Consider rational coordinates with
`d0(t)=(t,0)` and `d1(a,b)=b`. Applying d1 after d0 always gives zero.
Repairs can change the first coordinate; the second survives. Thus the raw
repair quotient `C1/im(d0)` is described by b. Closed elements have b=0, so
`ker(d1)/im(d0)` is zero in this example.

[Proved] A linear map descends to the repair quotient when its degree-1
action transports every repair into a repair. A commuting cochain triple
provides that witness. Commuting with the next differential additionally
preserves closedness. Composition and supplied retractions are checked by
the [native matrix owner](../../../../../../omega_engine/crates_rs/omega_linear_algebra/src/finite_cochain_map.rs).
Identity and doubling both commute here. They need not preserve the same
norm value.

## A filler does not identify every class

[Proved] Set `H1(a,b)=a`, `H2(t)=(0,t)`. Then
`d0 H1 + H2 d1` is the identity on `(a,b)`: it equals `(a,0)+(0,b)`.
This is the middle homotopy equation between identity and zero.

On closed elements, H2 d1 vanishes, so the two images differ by a repair.
On `(0,1)`, that term is `(0,1)` and cannot be produced by d0. Identity and
zero therefore give different raw repair classes despite the supplied
homotopy. Altering H2 to `(0,2t)` breaks the equation and is refused.

## A raw source change can break quotient agreement

[Source-specific proof and finite checks] The new
[execution supplement](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/source_execution_refinement.md)
implements every canonical seed-25 change using the complete assertion
state. Identifying vertices adds counts from their endpoint fibers in
each relation separately. The matrix owner computes P M P^T, and a
universal Lean finite-sum proof establishes that formula.

On two terms, start with zero and with excess given by potential (1,0):
the second has r(0,1)=1 and s(1,0)=1. They agree modulo repairs. Add
a new term with no incident assertions to both. Around 0->1->2->0,
their excess sums are now 0 and 1. They have different repair classes.
The pinned original functions and the native kernel agree on this
counterexample. Equality before a change does not force equality after it.

Also compare an empty run on two terms with adding r(0,1) then removing
it. Their complete final states agree, but their histories and addition
prices differ. The new run type retains those differences. A disabled
change is refused, so it supplies no admitted occurrence.

Run the native comparison from the repository root:

```powershell
cargo test --manifest-path omega_engine/crates_rs/Cargo.toml --locked --offline -j1 -p omega_wdp --test source_execution_oracle
```

That test matches all 3,770 original transitions in the declared finite
corpus. The all-finite-sum theorem has a broader mathematical domain;
the test count alone does not prove an all-source execution theorem.

## Retrieval and transfer

1. Replace R(a,b) with a statement that a and b have different printed names.
   Does that establish a protected relation law? Explain the additional input.
2. Compute the two images of `(3,0)` and `(0,1)` under identity and zero.
   Which differences are repairs? State which elements are closed.
3. If down(up(x))=x, must up(down(y))=y? Use inclusion `(x,0)` and projection
   to the first coordinate to construct a counterexample.
4. Which extra source data would a claim about actual Genesis dynamic
   transitions require? A commuting matrix fixture does not bind a source run.
5. Why does the two-term gradient counterexample become an obstruction
   after adding a term? List the three directed excesses around the new cycle.
6. Which question distinguishes an empty run from addition followed by
   removal when the final assertion states agree?

The notebook answers questions 2 and 3 through exact calculations. For
question 1, names alone supply no admitted law. For question 4, bind source
states, every event, the transition rule, costs, protected observations and
the actual refinement maps. For question 5 the new cycle has excesses
1,0,0; the zero state has 0,0,0. For question 6 use the ordered occurrences
or the assertion-addition price. These source obligations remain open at
their full scopes. Continue with the
[source replay supplement](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/source_replay_and_remaining_derivations.md)
to compare the six versus two minimum-response alternatives and the 32
actually executed source changes with native readouts. Observational
separation and an admitted irreflexivity law answer different questions.
