# WitnessedDifference Lean package

Current audit scope (2026-10-08): 50 core-only modules and 691 selected declaration reports were replayed under Lean 4.33.1; 25 additional named module compilations include overlaps with that set. Counts below describe their dated receipts. Fresh compilation of the full Mathlib-backed root remains unverified because the pinned cache download is blocked in this environment. Source review and historical receipts are not a substitute for that build.

This package mechanizes a bounded finite spine for the witnessed-difference
programme. It separates primitive difference, observation, measurement,
succession, normalized finite multiplicity, history decomposition, and relative
status routing.

It does not prove quantum reconstruction, phenomenology, continuum time, Born
uniqueness, or cosmogenesis. Those topics occur only as labels in the `OPEN` and
`NONCLAIM` namespaces.

## Toolchain and build

The package pins Lean `v4.33.1` and one dependency: Mathlib at revision
`0df444a360eaa60ab8c11dca51a86af692955474`, the pin used by the repository's
`lean4/quantum_mechanics` and `lean4/research_programs/mub6` workspaces.
`WitnessedDifference.ClassicalCorner`, `WitnessedDifference.EmpiricalModel` and
the five modules of the quantum route (`ClassicalPackage`, `ToleranceAdapter`,
`Composition`, `AmplitudeBridge`, `InstrumentAdapter`) import Mathlib, and
`WitnessedDifference.PacketAdapter` imports `EmpiricalModel` together with the
core `Measurement` module. The separate `PresentationCompletion` module
imports Mathlib metric completion; its own axiom report is outside both
historical roots and the core-only finite spine. The other modules described
in the historical graph use Lean core only, and rationals there are core `Rat`. Lake writes build products
to the short local directory `b/`; no generated cache belongs in the source
package.

```text
lake exe cache get
lake build
lake env lean WitnessedDifference/AxiomReport.lean
```

On Windows, Lean's tools cannot open paths longer than 260 characters. This
package sits about 150 characters deep in the repository, so Mathlib's nested
build paths overflow when it is built in place. Build from a copy at a short
path instead:

```powershell
robocopy . C:\lk\r\lean4 /E /XD .lake b
Push-Location C:\lk\r\lean4
lake exe cache get
lake build
Pop-Location
```

A `subst` drive or a junction does not help, because Lake resolves it back to
the long path.

The default target has two roots: `WitnessedDifference` and
`WitnessedDifference.AxiomReport`. The latter prints the axiom dependencies of
the 202 selected principal theorems listed in it, not of every declaration.

## Module order

1. `Core` imports only Lean core (`Init`).
2. `Symmetry` and `Difference` depend only on `Core`.
3. `Observer` depends on `Difference`.
4. `Measurement` depends on `Observer`.
5. `Succession`, `Probability`, `Routing`, `Descent`, `Boundaries`,
   `SemiringTransport`, `Obstruction`, `ObserverResolution`,
   `PointedRelation`, and `Interference` depend on `Core`.
6. `QuantumImports` depends on `Core` and `Difference`.
7. `History` depends on `Succession`.
8. `ComplexGrowth` depends on `Obstruction`.
9. `ClassicalCorner` and `EmpiricalModel` import Mathlib and nothing from this
   package, so the core notations (`ℚ`, `∅`, `∑`, `≃`) never meet Mathlib's in
   those files.
10. `PacketAdapter` depends on `EmpiricalModel` and `Measurement`. It is the one
    file where the core and Mathlib notations meet, so it writes `Rat`, never
    uses `∅`, and names Mathlib's `Fintype` as `_root_.Fintype`.
11. `ClassicalPackage` depends on `ClassicalCorner` and `EmpiricalModel`;
    `ToleranceAdapter` on `EmpiricalModel`; `Composition` on `ClassicalPackage`
    and `EmpiricalModel`; `AmplitudeBridge` on `ClassicalCorner` (for the
    Gaussian rationals `GaussRat`); and `InstrumentAdapter` on `AmplitudeBridge`
    and `EmpiricalModel`. All five import Mathlib and none imports a core-only
    module, so the notations never meet.
12. The package root imports the public modules; `AxiomReport` imports the root.

This graph is acyclic. Definitions and theorem hypotheses carry all assumptions;
the package declares no custom axioms.

## Standalone finite derivation supplement

The 2026-10-04 faithful-representation increment adds
`FaithfulRepresentation` and `FiniteConstraintRepresentation`: 46 audited
declarations for original-goal transport, solution coverage, fair search,
shared-fuel re-entry, constraint gluing and constructive finite enumeration.
Before the Appendix S increment, the combined standalone spine had **31 modules and 454 audited
declarations**, all checked with Lean 4.33.1. Use the pinned toolchain's
binary explicitly, or invoke the harness from this `lean4` directory so
the elan wrapper selects the correct version. These results model the stated
mathematical interfaces; they do not formally verify the Python checker.

At the 2026-10-02 checkpoint, the independent `WitnessedDifference.FiniteDerivations` import root combined 27 core-only modules from Appendices H–L and the bridge supplements, with 379 audited declarations. `scripts/verify_finite_derivations.py --lean /path/to/lean-4.33.1` compiles the current spine in an external scratch directory and verifies source-bound axiom receipts. Use `--write` only when intentionally refreshing those reports. The whitelist is Classical.choice, propext and Quot.sound; compilation errors or admitted proofs fail the check.

These modules have partial canonical bindings in claim_map.md. They do not extend the historical 202-theorem Mathlib census or formalize all analytic, probabilistic, tensor, Kraus/trace, simplex or enumeration arguments. Complete arguments and exact native/Python evidence are in Appendix J and docs/derivation_review.md. The historical package root remains separate from this standalone import spine.

The source-bound completion adds ObserverAdapterCompleteness (34 selected declarations), OriginalGenesisObserver (54), and PolicyObserverAdapter (8). Their algebraic/whole-history criteria are proved at the stated types; source custody, native transducer correctness and the complete operator-analysis theorem remain separately bound evidence.

The later `PrimitiveAdmissionFloor` and `CochainTransport` modules add twelve selected declarations about protected cuts, nonselection, commuting maps and explicit homotopies. Their hypotheses and remaining source obligations are recorded in [the admission and transport supplement](../docs/primitive_admission_and_transport.md).

`Source25PairTransport` adds ten selected declarations proving exact
matrix/fiber aggregation and equality of the declared partial execution
formulas at all finite history lengths. Concrete Python/Rust custody,
sorting and storage correspondence remain separately audited in the
[source execution supplement](../docs/source_execution_refinement.md).

`AdmissionCount` adds twelve selected declarations for COUNT aggregate
step/run laws and the exact minimum n+sum(r+s)+2*sum(leftovers). Its
cellwise realization, canonicalization and concrete source/native comparison
have distinct scopes in the [admission execution supplement](../docs/admission_execution_refinement.md).

`PrimitiveContextFloor` adds eleven selected declarations for actual
one-instance profiles and their requirement-cover criterion, over arbitrary
carriers and finite tuples. The item-shape classification, minimum-cover
optimization and concrete programs have separate scopes in the
[primitive execution supplement](../docs/primitive_execution_refinement.md).

`RootGaugeNormalization` adds sixteen selected declarations for root-loop
preservation, complete integer gradient equality, idempotence, loop/pair/
cycle preservation, the complete ascending obstruction criterion at all
finite sizes, raising and pullback/re-normalization. Its orbit enumeration,
raw programs and source correspondence have separate evidence scopes in
the [raising-result supplement](../docs/gauge_result_refinement.md).

`MarkedGaugeTransport` adds nineteen selected declarations for cyclic
diagnostics, fixed-mark gradient classification, balance descent and the
actual raw source AddTerm/Identify formulas. Its concrete countermodels
prove that those edits need not descend to result marks and can change
future balance answers. The [marked-result supplement](../docs/marked_result_refinement.md)
separates that formal scope from written orbit completeness and finite
original/native program comparison.

## Certified progress and belief-game quotients

`CertifiedProgress` adds 23 selected declarations for reachability, losing traps,
ranked certificates and exact upper/lower rational budget laws.
`BeliefGameQuotient` adds 16 for two-sided reachability/budget transport,
optional-action monotonicity, a constructive finite greatest stable relation,
and preservation of equivalence from an equivalence seed. Their source-bound
axiom receipts are [progress](certified_progress_axioms.txt) and
[quotient](belief_game_quotient_axioms.txt).

The preceding recorded core-only import spine checked **49 modules and 670 selected
declarations** with Lean 4.33.1 (2026-10-06, run from a short-path copy because
the worktree path exceeds Lean's Windows path limit). The historical Mathlib
census is separate. `GuardedHistoryCoherence` (10 declarations, axioms
`propext` and `Quot.sound`; [receipt](guarded_history_coherence_axioms.txt))
checks the two local inputs of Appendix P.20: moving a helper event earlier
preserves every guarded run and its final state, with the single-key count
kernel as the instance; and a cochain closed on the declared faces is
unchanged by backtrack and face moves. The simple-connectivity argument of
P.20 is a written proof and has no Lean counterpart here.
The [supplement](../docs/certified_progress_proof_and_evidence.md) distinguishes
written horizon and block-count proofs from the formal certificate/transport
laws and concrete Python tests. No Python program or native Rust binding is
claimed verified by these Lean models.

## Generative histories and additive tensor completion

`GenerativeHistoryCompression` adds 16 selected declarations for free typed
histories, deterministic transition replay, the greatest two-sided
question-preserving contextual congruence, quotient composition and the
derived endpoint-boundary law.

`AdditiveTensorCompletion` adds 12 selected declarations for the unique fold
from finite commutative alternatives, the free signed group and Grothendieck
extension, canonical biadditive extension, and universal tensor
factorization/uniqueness. Its tensor object is algebraic over free abelian
groups. It does not formalize scalar selection, dagger, positivity, Hilbert
completion or probability readout. The source-bound receipts are
[generative history](generative_history_compression_axioms.txt) and
[additive tensor](additive_tensor_completion_axioms.txt).

`DaggerObserverPairing` adds 12 selected declarations for involutive additive
dagger extension, componentwise tensor dagger, exact integer Gram positivity,
the equality between the Gram self-null space and observer kernel, and two
nonselection theorems. Its [axiom receipt](dagger_observer_pairing_axioms.txt)
records only `propext` and `Quot.sound`. It does not select the involution,
observer, positive form or complex structure.

`FiniteHermitianization` adds 17 selected declarations binding
GEN-WDP-62/63. A supplied rational-linear $J$ with $J^2=-I$ defines the exact
Gaussian-rational scalar action. When $J$ is skew-adjoint for a supplied
positive-semidefinite rational form, the constructed pairing is conjugate
symmetric, sesquilinear and positive on the diagonal, and its radical equals
the real-form radical. The concrete rational plane is positive definite. A
second admitted orientation on the same form establishes nonselection of $J$.
The [derivation](../docs/derivations/finite_hermitianization_derivation.md) and
[axiom receipt](finite_hermitianization_axioms.txt) separate this finite
algebraic carrier from complex completion, state/effect cones, Born readout,
dynamics and physical interpretation.

`FiniteStateEffectReadout` adds 13 selected declarations binding
GEN-WDP-64/65's constructive side. In the exact two-dimensional
Gaussian-rational class, it establishes the trace/Gram-factor numerator identity,
Frobenius positivity, partition of state mass by a complete binary factor
pair, rational normalization and the unit-interval bound. The sharp basis
fixture is constructive. The [derivation](../docs/derivations/finite_state_effect_readout_derivation.md)
and [receipt](finite_state_effect_readout_axioms.txt) keep this formal state and
effect certificate class distinct from readout uniqueness, physical
interpretation, process dynamics, Bell assumptions and continuum claims.

`FiniteProcessComposition` adds 12 selected declarations for the constructive
side of GEN-WDP-66–68. Complete binary process factors partition state mass,
sequential branch factors compose in operator order, and a supplied unitary
factor preserves mass and is reversible. The exact bit-flip fixture establishes
basis transport and round trip. The
[derivation](../docs/derivations/finite_process_composition_derivation.md) and
[receipt](finite_process_composition_axioms.txt) keep this finite algebraic
model separate from process selection, outcome semantics, subsystem
realization, approximate gate synthesis, Bell locality and universal quantum
computation.

## Separate metric presentation completion

The R12 increment is registered in the finite spine:
`CertifiedPreservers` (17 selected audits),
`RationalUnitaryReachability` (six), and
`ProjectiveFrameRigidity` (three). Their
[bindings](claim_map.md#preserver-supplement-bindings) and source-bound
receipts distinguish exact theorem scopes, the explicit two-squares
premise, and partial classification/uniqueness coverage.
This does not change the separate metric-completion result below.

`WitnessedDifference.PresentationCompletion` formalizes Appendix O.1 for
arbitrary source types, metric presentations and metric answers, with explicit
complete answers for recovery. It establishes image factorization, unique uniformly
continuous recovery on the actual image's completion, and commuting completed
maps when the source presentation is uniformly continuous.

```text
lake build +WitnessedDifference.PresentationCompletion +WitnessedDifference.PresentationCompletionAxiomReport
lake env lean WitnessedDifference/PresentationCompletionAxiomReport.lean
```

These targets were built separately on 2026-10-03 in an isolated short-path
copy using existing local vendors at every declared manifest revision and
offline cached dependencies. The fifteen selected declarations have axiom
union Classical.choice, propext and Quot.sound, without admitted proofs or
custom axioms. This is classical existence, not effective construction. The
total `Completion.extension` construction has an agreement theorem here only
under relative query control. The module does not formalize character duality,
Haar integration, field operations or physical continuum transport.

The historical default root, 202-theorem report and separate 29-module,
408-declaration finite census are unchanged. A scoped target success does
not report a fresh full-package build.
