# From witnessed reasoning to Bell tests and quantum computation

Route map after integration with remote main `880eabfd2`, 2026-10-05.
This is a development path, not a claim of quantum reconstruction.

## What the reasoning model supplies

Reasoning is controlled exploration of admitted operations with independent
evaluation. Knowing a result means possessing a checked witness **for the
original question**, with its assumptions, carrier, observer, provenance and
evidence scope retained. A guaranteed way to obtain such a witness is a further
property, characterized by the finite progress theorem. Authorization remains
independent of both. This is conditional, task-relative knowledge; checker
soundness and faithful source interpretation still need evidence.

## The finite Bell bridge already in the paper

Chapter 19 / CH19-P05 expresses the classical CHSH bound through nonnegative
global distributions on the four measurement variables. Existing
[`EmpiricalModel.lean`](../lean4/WitnessedDifference/EmpiricalModel.lean) contains
`chsh_le_two_of_noncontextual` and the PR-box counterexample. That older
Mathlib-based module is separate from this increment's core-only Lean audit.

For outcomes in {−1,+1}, every deterministic assignment satisfies

\[
 a_0b_0+a_0b_1+a_1b_0-a_1b_1
 =a_0(b_0+b_1)+a_1(b_0-b_1)\in\{-2,2\}.
\]

Every nonnegative normalized mixture therefore has CHSH ≤ 2. Equivalently,
four local probability tables exceeding that bound cannot be restrictions of
one such global distribution. This is the probabilistic LGGR connection:
local compatibility does not imply a nonnegative global extension. It is
not merely a failure to glue the *supports* of the local relations. If every
local outcome has positive probability, support gluing alone can miss it.

The interpretation assumes local response functions and a setting-independent
hidden-variable distribution. Setting-dependent distributions, communication
or outcome-dependent sample selection change that declared problem. The
standard Bell-polytope formulation is explained in
[Preskill's lecture](https://www.preskill.caltech.edu/ph219/Ph-CS-219A-Slides-2020/Ph-CS-219A-Lecture-7-Bell-Polytope.pdf);
the global-extension viewpoint is imported from
[Abramsky–Brandenburger](https://arxiv.org/abs/1102.0264).

## The next quantum bridge must carry the actual matrices

The Bell-marginal fixture in the corrected locality derivation verifies density
matrices and joint readouts. It is not by itself a Bell test. Chapter 19.11's
existing rational CHSH=14/5 correlation fixture likewise does not establish a
Hilbert realization just by lying below 2√2.

A small, explicit **different** Hilbert example is available. Declare
ρ=|Φ+⟩⟨Φ+| on two qubits, with |Φ+⟩=(|00⟩+|11⟩)/√2; its density entries
are rational. Take A₀=Z, A₁=X, B₀=(3Z+4X)/5 and B₁=(3Z−4X)/5.
Each observable squares to identity. Direct trace evaluation gives

\[
 (E_{00},E_{01},E_{10},E_{11})=(3/5,3/5,4/5,-4/5),
 \qquad S=14/5>2.
\]

All one-party means vanish; the full tables are
p(α,β|x,y)=(1+αβE_xy)/4. The finite task is to independently verify the
state, operators, probabilities, marginals and CHSH separating witness, then
bind the *same* tables to the WDP global-extension checker. The matrices and
Born trace rule are declared inputs, not consequences of a primitive mark.
This target needs Python and Lean evidence before being registered as a new
discharged theorem. Equal CHSH values do not identify the two different models.

## From carriers to executable computation

| Step | Existing foundation | Remaining concrete obligation |
|---|---|---|
| Original-task evidence | Faithful representation and independent replay | Bind a physical or mathematical source to the declared model |
| Bell obstruction | Finite global-extension/CHSH formulation | Replay the explicit Hilbert realization and the identical empirical tables |
| Quantum carrier | Declared finite Hilbert branch and rational instrument adapters | Specify tensor factors, allowed coefficient field, states and each actual instrument |
| Quantum program | Instrument probabilities and post-state replay | Supply gate semantics, composition maps and a bounded circuit with decoded original output |
| Certified control | Sure-winning beliefs, exact costs and observation quotient | Build the arena from the actual instruments and retain every possible outcome |
| Physical computation | Conditional locality and admitted-error recovery | Supply device operations, calibration/noise assumptions and realizable recovery evidence |

The current
[`quantum_measurement_replay.py`](../code/witnessed_difference/quantum_measurement_replay.py)
is an existing evidence owner. Equal POVM probabilities do not imply equal
post-states or future capabilities; Chapter 19's two-instrument example and the
new exact operation quotient make that distinction central. A compiler must
preserve those semantics rather than only the current answer.

For finite quantum measurements, the progress theorem quantifies over every
declared possible outcome. Almost-sure or high-probability success requires a
separate probabilistic theorem. A finite experiment also gives statistical
evidence under a declared sampling model, not an exact table by assumption.
Neither a density-matrix calculation nor a receipt authenticates laboratory
data. A bounded quantum circuit and this Bell bridge require no spatial
continuum, but universal gate approximation and scalable fault tolerance have
additional approximation and resource obligations.

The useful Bell connection is precision about what a model explains and what
the observations exclude. WDP can make that boundary executable. It need not
pretend that quantum physics is forced by the finite reasoning calculus.
