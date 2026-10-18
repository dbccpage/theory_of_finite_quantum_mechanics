# Fable work order: Primitive Difference to the finite Hilbert boundary

**AuthorityEffect:** None.

## Binding author decisions

1. Do not edit, rewrite, supersede, or "repair" Paper 0:
   `002_projection_obstruction/000_projection_obstruction/projection_obstruction.md`.
2. Paper 0 is an application host, not the definition of the Primitive
   Difference spine and not the sole destination of the walk.
3. The quantum route is an optional research branch. It must not become the
   engine's only optimization target.
4. Reuse existing papers and proofs before inventing replacements.
5. Every lift must state what was imported, what invariant survives, what new
   expression becomes possible, and what finite countermodel prevents a
   stronger claim.

This is a bounded research order for Fable. It does not license publication,
promotion, authority changes, or claims that Primitive Difference uniquely
forces quantum mechanics.

## Mission

Build a replayable walk from the repaired Primitive Difference trunk to the
existing finite quantum-mechanics ladder. The walk should answer:

> How far can the finite presentation calculus reach toward Hilbert-space
> language, one explicit lift at a time, before phase, complex scalars, Born
> semantics, tensor composition, or continuous dynamics must be imported?

The goal is not to produce another broad essay. The goal is a spine of named,
typed invariants with Lean witnesses and finite separating models.

## Starting point: the repaired trunk

The admissible set-theoretic trunk is the J011 mini spine:

```text
carrier and unequal marks
  -> declared presentation map
  -> raw same-report relation
  -> paid equivalence closure when needed
  -> quotient/fiber presentation
  -> optional section
  -> induced idempotent
  -> ambient dynamics
  -> descent test and selected dynamics
  -> escape, motion, descent failure, and composition defect
```

The binding prose sources are in:

```text
coda_university/coda_research/_support/
  projection_obstruction_primitive_difference_walk/
```

Start with these files:

- `J011_mini_spine.md`
- `J011_minimal_publication.md`
- `J011_vs_estate_paper.md`
- `J011_receipt.md`
- `B001` through `B016`
- `E001` through `E025`
- `D014_split_projection_obstruction_claims.md`

The candidate Lean replay is in:

```text
lean4/genx/_work_review_queue/grok_pd_night_20260814/
```

Begin with `J001_set_theoretic_spine.lean`,
`J011_minimal_publication.lean`, and the `B*` and `E*` modules they actually
import. Do not treat the whole review queue as admitted merely because one
aggregate target builds.

## Existing quantum route to walk, not rediscover

The present papers already contain most of the conceptual route:

```text
finite L1 sector weights
  -> QM_020 conditional Hilbert lift
  -> QM_060 phase content as quotient fiber
  -> QM_061 equal L1 data with unequal interference
  -> QM_062 conditional U(1)/complex selector
  -> QM_121 finite-QM ingredient ladder and import ceiling
```

Read these papers and their local claim ledgers, tests, Lean files, nonclaims,
and mutation audits as packets:

- `020_born_normalization_and_conditional_hilbert_lift`
- `060_superposition_as_the_quotient_fiber`
- `061_interference_as_the_non_l1_resource`
- `062_the_u1_selector`
- `121_the_finite_qm_ingredient_ladder`

Then audit the newer proposed continuation rather than assuming it is sound:

- `200_inner_product_admission`
- `201_braket_section_admission`
- `202_operator_algebra_shadow`
- `203_measurement_problem_obstruction`
- `204_born_uniqueness_import_boundary`
- `205_pointer_basis_obstruction`
- `206_universal_boundary_synthesis_and_cochain_lift`
- `207_complex_phase_fiber_and_u1_transport_lift`
- `208_quadratic_l2_readout_and_interference_boundary`
- `209_non_commutative_operator_algebra_and_contextuality`
- `210_born_rule_postulate_and_state_effect_pairing`
- `211_continuous_unitary_dynamics_and_l1_to_qm_synthesis`

These papers are evidence and proposals, not an authority source. For each,
identify which claims are proved, computed, conditional, imported, or merely
suggested. A local test that cannot fail, a historical Lean reference, or a
generic claim-code map is not a theorem binding.

## The candidate lift spine

Use the identifiers below provisionally. Renaming is allowed, but do not merge
two different imports under one name.

### H000 — finite presented carrier

- Input: a finite carrier `X` and a presentation `p : X -> Q`.
- Construction: the report quotient or an explicitly supplied finite `Q`.
- Invariant: equality of reports; quotient classes are the observable states.
- New capacity: finite state dynamics can be stated on `Q`.
- Refusal: finiteness is an assumption unless derived for the chosen window.
- Countermodel: an infinite carrier with the same presentation laws.

### H001 — probability simplex over reports

- Added structure: nonnegative weights on finite `Q` with total mass one.
- Construction: `Prob(Q)` with its L1 normalization.
- Invariant: total mass and total-variation/L1 distance where licensed.
- New capacity: mixtures and observable outcome distributions.
- Forgotten information: any data internal to a report fiber.
- Refusal: probability semantics are not supplied by bare unequal marks.
- Countermodel: signed weights or unnormalized nonnegative weights.

### H002 — deterministic report dynamics

- Added structure: `tau : Q -> Q`.
- Construction: push-forward of distributions along `tau`.
- Invariant: total probability mass.
- New capacity: time-step evolution on report states.
- Refusal: `tau` descends from `T : X -> X` only if `T` preserves `p`-fibers.
- Countermodel: use the J011 descent-failure model.

### H003 — reversibility gate

- Added structure: a proof that `tau` is bijective, or a specified inverse.
- Construction: permutation action on basis states.
- Invariant: counting measure and L1 norm under permutation.
- New capacity: reversible finite dynamics.
- Refusal: determinism does not imply reversibility.
- Countermodel: a two-state map collapsing both states to one.

### H004 — free linearization

- Added structure: a coefficient semiring or field `K`.
- Construction: the free finite module `K[Q]` with basis indexed by `Q`.
- Invariant: basis labels and linear extension of the permutation.
- New capacity: formal linear combinations and superposition syntax.
- Refusal: the coefficient carrier is imported; Primitive Difference does not
  select `R` or `C` by itself.
- Countermodel: perform the same construction over `F2`, `R`, and `C`.

### H005 — inner-product admission

- Added structure: positive-definite sesquilinear form, normally declaring the
  report basis orthonormal.
- Construction: a finite inner-product space.
- Invariant: norm and orthogonality under operators proved isometric.
- New capacity: angles, orthogonal projections, adjoints, and L2 geometry.
- Refusal: free linearization does not canonically supply this form without a
  basis/weighting choice.
- Countermodel: two unequal positive-definite Gram matrices on the same module.

### H006 — permutation unitary

- Input: H003 plus H004 and H005 with the declared orthonormal report basis.
- Construction: linear extension `U_tau |q> = |tau q>`.
- Invariant: inner product and L2 norm.
- New capacity: a finite unitary representation of reversible report dynamics.
- Refusal: this proves a permutation-unitary envelope, not general unitary
  dynamics and not quantum mechanics.
- Countermodel: a non-permutation unitary unavailable from `tau` alone.

### H007 — complexification

- Added structure: complex scalars or a justified complex structure.
- Construction: `C tensor_R V`, or the finite complex coordinate space.
- Invariant: the real subspace embeds; admitted operators extend linearly.
- New capacity: continuous phase and complex interference.
- Refusal: complexification is available but not thereby forced.
- Countermodel: real Hilbert space supports H000-H006.

### H008 — phase-blind presentation

- Added structure: amplitude vectors and a declared sector basis.
- Construction: map amplitudes to diagonal weights, coordinatewise
  `psi_i |-> |psi_i|^2`, with normalization handled explicitly.
- Invariant: normalized total probability.
- New capacity: compare amplitude presentations with L1 reports.
- Forgotten information: global phase and, for fixed diagonal readout, relative
  phase.
- Refusal: call this the Born presentation only after the quadratic rule is
  explicitly imported or conditionally derived.
- Countermodel: amplitudes with equal moduli and different phases.

### H009 — phase-fiber invariant

- Input: H008.
- Construction: fiber of the phase-blind presentation.
- Invariant: all vectors in a fiber have the same diagonal L1 weights.
- New capacity: name phase as hidden information relative to that report.
- Refusal: superposition is not identical to a quotient fiber without fixing
  carrier, basis, normalization, and equivalence.
- Countermodel: global-phase-equivalent vectors versus vectors with distinct
  relative phase.

### H010 — interference non-descent

- Added structure: a mixing basis or operator followed by readout.
- Construction: the QM_061 witness based on `(1,1)` and `(1,-1)`.
- Invariant: input diagonal weights agree.
- Obstruction: mixed-basis output does not factor through the phase-blind L1
  quotient.
- New capacity: a finite, exact witness that phase can become observable after
  a change of presentation.
- Refusal: this does not prove that every physical interference experiment is
  represented or that complex amplitudes are unique.
- Countermodel: diagonal-only measurements, where phase remains invisible.

### H011 — U(1) transport selector

- Added structure: the exact assumptions used by QM_062, written as imports.
- Construction: conditional narrowing of the phase carrier.
- Invariant: composition law for phase transport.
- New capacity: distinguish a theorem under selector assumptions from a bare
  choice of `C`.
- Refusal: do not say `C` or `U(1)` is forced until rival carriers are excluded
  under a stated theorem.
- Countermodel: any rival scalar/phase carrier satisfying the weaker prior
  rungs.

### H012 — operator-algebra host

- Added structure: linear operators, adjoint, identity, composition, and the
  selected observable class.
- Construction: finite matrix/operator algebra over the admitted Hilbert host.
- Invariant: algebraic laws actually proved in the host.
- New capacity: noncommuting contexts and state transformations.
- Refusal: noncommutativity is not present in the original L1 simplex alone.
- Countermodel: the commutative algebra of diagonal observables.

### H013 — Born state-effect pairing

- Added structure: states/effects and a quadratic or trace pairing.
- Construction: probabilities such as `Tr(rho E)` in the finite host.
- Invariant: positivity and normalization, each with explicit hypotheses.
- New capacity: general finite measurement statistics.
- Refusal: existence is not uniqueness. Gleason-type or other uniqueness
  results require their own dimensional and regularity imports.
- Countermodel: alternative normalized readout rules allowed by weaker axioms.

### H014 — tensor composition

- Added structure: tensor product and a rule relating composite and component
  systems.
- Construction: finite composite state space.
- Invariant: normalization and product-state embedding.
- New capacity: entanglement, locality questions, and quantum information.
- Refusal: Cartesian composition of report sets does not force Hilbert tensor
  composition.
- Countermodel: direct-sum or classical Cartesian composite satisfying earlier
  rungs.

### H015 — irreversible dynamics fork

- Input: a non-bijective report update or noisy evolution.
- Options: refuse unitary realization on the same host; add an environment and
  dilation; or import a CPTP map.
- Invariant: trace/probability preservation where proved.
- New capacity: open-system dynamics.
- Refusal: a selected dilation is not canonical without additional structure.
- Countermodel: two inequivalent dilations inducing the same reduced channel.

### H016 — continuous dynamics fork

- Added structure: topology, continuity, one-parameter group, and differentiable
  structure as required.
- Construction: unitary flow and, conditionally, a Hamiltonian generator.
- Invariant: norm under the flow.
- New capacity: continuous-time quantum dynamics.
- Refusal: finite permutation steps do not force a continuum parameter or
  Stone's theorem hypotheses.
- Countermodel: discrete reversible dynamics with no preferred interpolation.

### H017 — finite Hilbert boundary theorem

Assemble the strongest statement licensed by the preceding proofs. A likely
ceiling is:

> A finite presented carrier with reversible report dynamics admits, after
> explicit coefficient and inner-product choices, a permutation-unitary
> representation. A phase-blind quadratic presentation has fibers containing
> states with equal L1 data, and a supplied mixing presentation can distinguish
> members of such a fiber. Complex phase, Born uniqueness, tensor composition,
> general quantum channels, and continuous unitary dynamics remain separate
> imports unless discharged by additional theorems.

Do not strengthen this sentence by style. Strengthen it only by closing a named
proof obligation.

## Required invariant record for every rung

Emit one machine-readable record per lift with these fields:

```yaml
id: H000
name: finite_presented_carrier
input_claims: []
input_modules: []
added_structure: []
construction: ""
preserved_invariants: []
new_expressive_capacity: []
forgotten_information: []
proof_status: proposed
lean_theorems: []
finite_witnesses: []
separating_countermodels: []
physical_contacts: []
imports: []
nonclaims: []
```

Allowed `proof_status` values are:

```text
proposed
defined
computed
proved
proved_conditional
refuted
quarantined
```

Do not use `verified`, `forced`, `canonical`, `unique`, `universal`, or
`complete` as an untyped status.

## Hard proof obligations

Prioritize these. If one fails, preserve the failure as a result.

1. Prove that a bijection of finite report states extends to a unitary operator
   after the report basis and standard inner product are supplied.
2. Prove that the phase-blind weight map identifies the selected equal-modulus
   examples.
3. Prove that the selected mixing/readout map separates `(1,1)` and `(1,-1)`
   after normalization conventions are fixed.
4. State the non-factorization theorem explicitly: no function of the
   phase-blind report alone reproduces that mixed readout.
5. Separate global-phase invariance from relative-phase information.
6. Show by model that H000-H006 can be carried over `R`; therefore `C` has not
   yet been selected.
7. Show by model that deterministic dynamics need not be reversible.
8. Show that a non-bijective update has no unitary implementation on the same
   orthonormal basis preserving its action on basis states.
9. Identify the exact hypotheses of any Born-uniqueness claim and bind each to
   a local theorem or mark it imported.
10. Identify the exact assumptions needed to pass from discrete unitary steps
    to continuous one-parameter dynamics.

## Required paper audit

For QM_020, QM_060, QM_061, QM_062, QM_121, and QM_200-QM_211, produce a table
with one row per substantive claim:

```text
claim id
paper and section
plain-language claim
status
assumptions
Lean declaration
test or finite certificate
countermodel
ENC link if present
reused rung
repair required
```

Apply these checks:

- A title-only quick-start card is incomplete documentation.
- A claim-code map pointing several claims to one generic module is not a
  claim-to-theorem bijection.
- A test ending in a tautology such as `or True` supplies no evidence.
- A Lean theorem mentioned historically but absent from the packet is not local
  mechanization.
- A successful build proves elaboration, not that prose and theorem match.
- Numerical agreement in one finite fixture does not prove uniqueness.
- A receipt describes commands and bytes; it is not a mathematical verdict.

## Relationship to Paper 0

Paper 0 remains untouched. Record contact rather than editing it:

```text
Primitive Difference trunk
  -> quotient/fiber presentation
  -> split/retraction calculus
       +-> Paper 0 application
       +-> finite Hilbert envelope
            -> phase-blind fibers
            -> interference non-descent
            -> operator and information hosts
```

The new walk may cite Paper 0's projection, retraction, escape, and obstruction
language. It may not claim that Paper 0 derives every later Hilbert structure.
If a mismatch is found, write a separate contact note or countermodel.

## Deliverables

Produce these in a new review-queue folder; do not modify estate papers during
the exploratory pass:

1. `HILBERT_WALK.md` — readable lift-by-lift account.
2. `hilbert_walk.yaml` — invariant/import/nonclaim records.
3. `PAPER_CLAIM_MAP.md` — audit of QM_020, 060, 061, 062, 121, and 200-211.
4. `COUNTERMODEL_REGISTER.md` — one finite separator for every non-forced lift.
5. Lean modules `H000_*.lean` onward, with a small root importing only admitted
   modules.
6. `AXIOM_REPORT.txt` — declarations checked and their printed axioms.
7. `BUILD_RECEIPT.md` — exact command, revision, result, and file inventory.
8. `FRONTIER.md` — strongest proved theorem, exact open residues, and next
   cheapest separating experiment.

Each Lean file must contain:

```text
claim identifier
source-paper contact
imports added at this rung
theorem or counterexample
nonclaim boundary
AuthorityEffect: None
```

## Four-hour execution order

### Hour 1 — reconcile and bind

- Build the J011 admitted root.
- Inventory exact Lean declarations used by the five core quantum papers.
- Audit QM_200-QM_211 for duplication and stronger/weaker restatements.
- Draft the claim map; do not prove new mathematics yet.

### Hour 2 — construct the finite envelope

- Implement H000-H006.
- Prove permutation linearization and unitarity under explicit imports.
- Add real, complex, and finite-field comparison models where type support
  permits.

### Hour 3 — expose the phase obstruction

- Implement H007-H010.
- Replay the QM_061 separating example exactly.
- State and prove the finite non-factorization theorem.
- Add mutation tests that fail when either phase witness is made equal.

### Hour 4 — price the frontier

- Attempt H011-H017 only as far as local evidence supports.
- Classify every residue as theorem work, finite search, literature import, or
  author choice.
- Build the admitted root, print axioms, and write `FRONTIER.md`.
- Stop on time with honest open obligations rather than filling gaps with prose.

## Gates

The work order passes only if all applicable gates pass:

### G1 — provenance

Every imported theorem, definition, paper claim, and candidate GenX module has
an exact local path and stable claim identifier.

### G2 — trunk separation

The set-theoretic J011 trunk builds without optional cohomology, Banach, or
quantum branches. Each optional host declares its first new import.

### G3 — paper preservation

Paper 0 is byte-identical before and after the run.

### G4 — theorem binding

Every statement marked `proved` names a local Lean declaration. Every
conditional proof lists its assumptions in prose and code.

### G5 — countermodel coverage

Every claim that a lift is not forced has a finite separating model, or is
marked as an open obligation rather than asserted.

### G6 — mutation sensitivity

At least the phase/interference witness and the descent witness fail when their
distinguishing data are removed.

### G7 — axiom disclosure

Print axioms for the publication-facing declarations. Do not silently accept
`sorry`, custom axioms, or classical choice beyond the stated policy.

### G8 — no authority lift

All outputs retain `AuthorityEffect: None`. No dashboard, receipt, build, or
paper count changes that status.

## Refusal conditions

Refuse or quarantine any output that does one of the following:

- says Primitive Difference uniquely derives complex Hilbert-space quantum
  mechanics;
- treats an arbitrary section, basis, Gram matrix, phase carrier, tensor
  product, measurement rule, or dilation as canonical;
- turns L1/L2 compatibility into Born-rule uniqueness;
- turns a permutation representation into all unitary dynamics;
- derives continuous time from a finite step without topology and regularity;
- identifies a selected projected map with descended dynamics without the fiber
  law;
- imports P0's later host structures back into the raw mark;
- edits Paper 0 as a shortcut;
- treats generated tests, receipts, or aggregate builds as semantic review;
- deletes an orphan before its paper, claim-ledger, ENC, and Lean provenance
  have been reconstructed.

## Success levels

### Level A — useful reconciliation

The paper/Lean claim map is exact, duplicate proposals are identified, broken
tests are named, and the strongest existing theorem is clear.

### Level B — finite Hilbert envelope

H000-H006 are mechanized with explicit coefficient and inner-product imports,
including reversibility countermodels.

### Level C — phase obstruction

H007-H010 are mechanized and the interference non-descent theorem has a finite,
mutation-sensitive witness.

### Level D — narrowed frontier

At least one of complex-phase selection, Born uniqueness, tensor composition,
irreversible dynamics, or continuous unitary dynamics is either discharged
under exact hypotheses or reduced to a smaller named import boundary.

A negative result at Level D is success if it proves that the earlier data do
not determine the later structure.

## Final report format

Fable's final report must begin with exactly one of:

```text
RESULT: RECONCILED
RESULT: FINITE_HILBERT_ENVELOPE
RESULT: PHASE_NON_DESCENT
RESULT: FRONTIER_NARROWED
RESULT: BLOCKED
```

Then report:

1. exact revision and dirty-state disclosure;
2. files added or modified;
3. build/test commands and results;
4. theorem names and printed axioms;
5. finite countermodels and mutation results;
6. paper claims reused, corrected, superseded, or quarantined;
7. strongest licensed mathematical statement;
8. remaining imports, ordered by estimated cost;
9. confirmation that Paper 0 is unchanged;
10. `AuthorityEffect: None`.

The desired outcome is a reusable derivational instrument: one lift, one named
invariant, one import ledger entry, and one falsifier at a time. If the route
reaches only permutation unitaries plus a phase non-descent obstruction, that
is already a sharp result. If it reaches farther, the additional hypotheses
must remain visible in every theorem that uses them.
