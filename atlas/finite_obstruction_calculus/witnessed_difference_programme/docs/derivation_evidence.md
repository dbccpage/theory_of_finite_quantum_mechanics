# Three derivations: proof and evidence map

This increment binds GEN-WDP-55–57 and §§20.10–20.12. AuthorityEffect: None.
The 154 canonical rows retain their scopes. The two supplied drafts are retained
as original bytes; corrected mathematical statements are separate artifacts.

| Deliverable | Written result | Lean model | Concrete Python evidence |
|---|---|---|---|
| [Locality and observer completion](meron_field_limit_derivations/unified_lieb_robinson_observer_completion_derivation.md) | Exact finite recovery/completion, conditional physical readout and conditioning bounds; corrected CAR/gauge and upper-bound counterexamples | [LocalObservationCompletion](../lean4/WitnessedDifference/LocalObservationCompletion.lean): 11 selected declarations | Exact binary decoder and lower collision, rational Bell states, submitted positivity/norm witnesses, actual six-hop exchange |
| [Trotter and cochain extinction](meron_field_limit_derivations/trotter_cochain_extinction_derivation.md) | Sharp temporal pairing; all-M compressed-channel extinction; explicit fixed-four-site A/M time-consistency estimate, thermal positivity and strict margins; exact cochain descent | [TrotterObservableFiltering](../lean4/WitnessedDifference/TrotterObservableFiltering.lean): 15 selected declarations; [CARResponseWitness](../lean4/WitnessedDifference/CARResponseWitness.lean): five integer matrix/basis/eigenvalue declarations with no axioms | Four source-reconstructed rational matrices and independent congruence certificates; exact finite filters, periods, weighted subdivision and a rational time threshold |
| [Sharp certified progress](sharp_certified_progress_theorem.md) | Self-contained attractor/certificate/cost theorem; necessary and sufficient structural quotient conditions and coarsest refinement; actual bounded calculus reconstruction | Existing CertifiedProgress/BeliefGameQuotient: 39 selected declarations; [ExactProgressQuotient](../lean4/WitnessedDifference/ExactProgressQuotient.lean): seven new structural iff/budget/refinement declarations | Independent strategy/table checks; actual unchanged calculus checker; source/task/witness mutations and all requested adverse cases |

The four new core-only modules add **38 selected audited declarations**. The
standalone spine contains **37 modules and 531 selected declarations**. The
new finite reference tests and existing progress tests are run together by
[`verify_locality_smearing_progress.py`](../scripts/verify_locality_smearing_progress.py).
The exact test total and source hashes are retained in
[`locality_smearing_progress_verification.json`](../manifests/locality_smearing_progress_verification.json).

## What each evidence type establishes

The imported analytic Lieb–Robinson hypothesis, finite operator exponential
estimates, spectral Fourier argument and C¹ mean-value/quadrature reasoning
have written proofs or identified imports. They are **not** advertised as
Lean formalization of analytic quantum evolution. Lean verifies the finite
and rational theorem consequences, plus the actual M=1 integer response's
orthogonal eigenbasis and negative-energy witness. Python independently
binds that integer table to the reconstructed CAR input; Lean does not verify
the Python construction. This distinction is part of the accepted claim.

The first three retained matrices' values agree with the supplied draft at
fixed total θ=1/10, meaning step r=θ/M. M=4 is a new reconstructed instance.
Independent congruence checks certify inertias (4M,1,4M−1) only for M=1–4.
An all-M rank-one negative-spectrum classification is not inferred. The
all-M smearing theorem instead uses a directly proved growth envelope.

The full time-limit theorem fixes the spatial carrier at four sites. Its
constant-profile positive margin follows from source symmetry and the finite
thermal trace, not from declaring every nonzero sampled field positive.
No joint spatial limit, Gaussianity, device realization, MUB6 resolution or
new physical repair operation is included.

The newly merged Chapter 23 source is retained with an explicit import fence.
Its claims that the stabilizer commutation kernel equals the stabilizer space,
or that every restricted low-weight problem needs all independent detector
rows, are not inherited. The full kernel is the symplectic orthogonal space;
the exact restricted-error criterion is the admitted-fiber test, not a global
rank count. At t=0, no detector is necessary. These imported claims remain
source-specific correction obligations under GEN-WDP-O02.

The progress theorem's table target truth remains conditional until original
task payload checks are actually supplied. The generic binding adapter demands
literal boolean acceptance from that separately supplied checker and a common
checked resolution for each target. It does not infer source-negative coverage
from an under-advertised witness menu. The actual calculus reconstruction binds
the retained antiderivative to its original checker; it does not validate
missing prompt stages, source quotations, a full demo campaign or a native
Woland runtime. Operation costs are declared units, with setup and replay
verification cost accounted separately from the operating comparison.

## Offline commands and certificate custody

From the paper's `code` directory with the repository on `PYTHONPATH`:

```sh
python -m locality_smearing.replay check
python -m certified_progress.calculus
python -m certified_progress.replay
```

The first replays
[`examples.json`](../code/locality_smearing/examples.json); the second replays
[`bound_calculus.json`](../code/certified_progress/evidence/bound_calculus.json).
Replay never invokes strategy production or a model. Generation has separate
`generate`/`--write` entry points. Wrong supplied witnesses, changed task/source
bindings, incomplete closure, inappropriate coefficient values and stale
receipts are rejection cases, not invitations to substitute a new answer.

Run the standalone Lean spine and the integrated verifier with the installed
Lean 4.33.1 binary:

```sh
python scripts/verify_finite_derivations.py --lean PATH_TO_LEAN_4_33_1
python scripts/verify_locality_smearing_progress.py --lean PATH_TO_LEAN_4_33_1
```

No `sorry`, custom axioms, model calls, paid requests, native bindings or release
publication are required. Verification snapshots source/witness bytes before
and after its subprocesses and refuses nonregular replay inputs. Intentional
source changes require intentional regeneration and fresh verification.

The source archive manifest pins the original locality draft to
`b815fd18dc0ea571897c10e668aadfba6c9fbeaad6aa14468f15cab579f9d6dc`
and the original Trotter draft to
`3d5d77164466d2f176e2270970bcf1fe75462a5a48e841e375104f225143257a`.
Those bytes are preserved through Git; they are not corrected in place.

GEN-WDP-O01–O05 remain open at their full scopes. General source refinement,
guarded-history coherence, institutional standing, native Rust bindings and
spatial continuum foundations still need their own witnesses and proofs.

## Distinct-image closure and Chapter 23 corrections

Written, executable, and mechanized scopes are separate.

| Claim | Written proof | Executable replay | Lean |
|---|---|---|---|
| WDP-DIM-1 | Appendix T of the manuscript. A submitted `lower_columns` field is accepted only when its columns are an obstruction basis for the claimed target. | `python -m observer_completion.distinct_replay` from `code/`, with that directory and the repository root on `PYTHONPATH` | `DistinctImageCompletion.lean`: the three inclusion counts, both kernel criteria on the supplied matrices, the annihilator obstruction, and one admissible preimage. Not a postulate of the general theorem. The obstruction-basis acceptance rule is executable, not a Lean theorem. |
| WDP-CH23-P01C through P18C | Appendix U. Full stabilizer rank \(2L^2-2\) is sufficient for \(1\le t\), \(2t<L\), and \(B=S\). The claim that separation holds if and only if the checks have that rank is withdrawn. The \(L=3\) face rows \(\{0,1,3,5,7,8\}\) and the \(L=4\) rank-\(29\) suite are the counterexamples. | the same replay, plus `code/toric_code_observer_completion.py` | `ToricSyndromeCorrespondence.lean`: \(L=3\) ranks, logical vector, weight, flux, and the quotient identity. The general-\(L\) flux proof and the rank-\(29\) counterexample are written and executable, not Lean theorems. |
| L1–L4 and T1–T4 | Appendices V and W, copied in full | `python -m locality_smearing.replay check` | Existing finite/rational modules. Analytic Lieb–Robinson, exponential, spectral, and \(C^1\) arguments stay written-only. |
| Gate E | Appendix W.8, values taken from the historical receipt | receipt file read by the replay; the writer `main()` is not run | none |

Targets 2–5 of `five_outstanding_derivations.md` remain open. So do guarded-history coherence, unrestricted source refinement, physical reconstruction, and joint continuum foundations. The G3/G4 model-response closures of Theorems A and B and Gates D, F, and G remain open. The Gate E checker stays at `meron_field_limit_derivations/code/gate_e_exact_counterexample.py`.

## Certified preservers and algebraic generators

[Chapter 19A](../witnessed_difference_programme.md#chapter-19a) and the
[full supplement](derivations/certified_preserver_derivation.md) derive R12
and R13 under their declared field, positive form, readout, operation and
linearity hypotheses. The supplement corrects the proposed four-phase
claim, the identification of similarities with unitary operations, the
postselection cost assertion and the stabilizer/information-completeness
equivalence. It also proves the full-probability qubit statement rather
than leaving that proposed conjecture open.

The original brief's standard algebraic imports are distinguished from
their WDP use. REF-NORM-001 supplies integer two-squares theory; the
preserver classification has a complete native coordinate proof.
REF-PRES-001 is a related-work record with publisher abstract consultation,
not an imported proof. The contribution here is the typed connection
among observation, admissible transformations, arithmetic reachability
and independently checked certificates.

### Written and formal scopes

The separate [supplement rows](../witnessed_difference_programme_claim_ledger.md#preserver-and-generator-supplement-r12r13)
and [Lean bindings](../lean4/claim_map.md#preserver-supplement-bindings)
record each claim individually.
`CertifiedPreservers` proves representative independence in both
arguments, bounds, full-table separation, exact rational phase formulas and
the named projection laws. `RationalUnitaryReachability` constructs
the isometry and its inverse before proving the iff criterion.
Its arithmetic corollary names primality and even multiplicities in both
the reduced numerator and denominator; the two-squares equivalence is an
explicit premise. `ProjectiveFrameRigidity` proves the basis/sum/mixed
ray steps used in projective uniqueness.

Together the three new modules print 26 selected declaration audits.
They use Lean core and the existing finite-derivation axiom whitelist;
the historical Mathlib declaration census is unchanged. The complete
global collineation classification, finite tomography reconstruction,
torsion-subgroup assertion, qubit classification, bicommutant theorem and
inner-generator theorem remain written proofs where the ledger says so.
Their written status is not a claim of Lean or native implementation coverage.

### Executable scope and commands

The [Python reference](../code/certified_preservers/) has separate
`propose` and `check` functions. A certificate binds the original
problem digest, including its field, positive Gram matrix and actual
source/target or full frame. Checking uses the submitted witness; it never
substitutes a separately discovered solution. The generator task supplies
every matrix-unit image, and the checker evaluates every basis-pair
Leibniz identity and adjoint identity before accepting the generator.

The retained [replay examples](../code/certified_preservers/replay_examples.json)
contain eight named tasks, two graph pockets and hashes of eight source
files. Same-byte symlink substitutions for every bound source and the replay
control are refused; source/control bytes are checked again before success.
Replay checks the retained candidate first and separately reproduces
the declared proposal accounting. There are no model calls. A mathematical
obstruction has a verified negative claim; malformed data, invalid
candidates and exhausted fuel remain distinct.

From the paper root, with its `code` directory on `PYTHONPATH`:

```sh
python -m certified_preservers.replay --check code/certified_preservers/replay_examples.json
python -m pytest code/unit_tests/test_certified_preservers.py -q -o addopts=
python scripts/verify_finite_derivations.py --lean PATH_TO_LEAN_4_33_1
python scripts/build_preserver_notebook.py
```

The [notebook](../jupyter_notebooks/supplements/110_certified_preservers.ipynb)
has eight executed cells; its builder uses the invoking Python interpreter
and compares outputs from the paper root and the notebook's directory.
It is a separate supplement, leaving the historical ten-lesson curriculum
and its receipt unchanged. The older top-level Trotter notebook was already
outside that curriculum manifest; this increment does not claim to repair
or validate that unrelated notebook catalog.

The native owners are `omega_number_theory::gaussian_norm` and
`omega_quantum_physics::projective_preservers`. From the repository
root, using the shared Cargo cache for a worktree:

```sh
cargo test --offline --locked -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_number_theory --lib gaussian_norm::tests
cargo test --offline --locked -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_quantum_physics --test projective_preservers
```

The scoped checks comprise 44 Python tests, two native norm tests and seven
native preserver tests. The latter include all nonzero Gaussian vectors
with real/imaginary coordinate height at most one in dimensions three
and four: 728 and 6,560 vectors. These are bounded tests of norm-class
stability, not a census of the infinite rational ray carrier.
Wrong original tasks, fields, Gram matrices, witnesses, projection targets
and zero branches are explicit rejection tests.

Python fuel counts the operations explicitly charged by its arithmetic
search/check routines; it is not a CPU, instruction or billing meter.
Rust `NormBudget` bounds each factorization/construction call.
Neither accounting model proves a worst-case cost theorem for the entire
paper or grants authorization. No Python-to-Rust binding or extraction
from Lean is claimed.

### Release checks that remain separate

The historical canonical ledger still has 154 rows, and this increment does
not add or remove a canonical WDP-CH ID. The existing
`verify_claim_map.py` nevertheless fails its whole-manuscript census:
the published base and the integrated manuscript both yield 196 distinct
regex matches and 213 occurrences after the earlier Chapter 23 additions.
That unchanged failure must be reconciled before claiming a fresh full-paper
claim-map pass. The ten-lesson notebook catalog issue above is also
pre-existing. Neither has been hidden by relaxing its verifier.

### R12/R13 brief completion audit

This audit was completed on 2026-10-05 against the requested preserver and
generator brief, SHA-256
`338b428191db523a3920d0611d858c4ac78b526fee7cfc24f97e47a67db87b79`.
The acceptance scope is that brief's written derivations and four-media
evidence plan. Its false statements are replaced by proved corrections,
with the failures retained explicitly in the supplement.

| Requested obligation | Current evidence and disposition |
| --- | --- |
| Declared Gaussian field, involution, positive Hermitian form, pure readout and separation | Supplement §1 and Chapter 19A.1 state the inputs. Positivity plus zero radical is distinguished from nondegeneracy alone. Python and Rust reject indefinite and singular Gram matrices. |
| P01: representative independence, rationality and injective ray table | Supplement §2 proves the complete statement. `CertifiedPreservers` proves both rescalings, bounds and full-table separation; its return scalar is an exact Gaussian rational. The additional sufficient finite tomography menu is a written corollary. |
| O01: classification, unique projective representative and two field branches | Supplement §3 supplies a complete native coordinate proof, discharging the named fallback. The registered frame-rigidity and rational-scalar-hom lemmas supply the brief's explicitly partial Lean uniqueness/branch evidence. REF-PRES-001 is positioning, not an unchecked proof import. |
| P02: phase group and cocycle consequences | Supplement §4 refutes the proposed four-phase group and proves the infinite rational-circle classification. Lean proves its parametrization, inverse, injectivity and multiplier criterion. The torsion subgroup is proved separately in prose. The explicit swap-lift cocycle refutes the proposed universal `mu_4` restriction. |
| P03: exact norm realization and named gates | Supplement §4 proves the rational parity criterion from the cited integer two-squares theorem, including negative valuations. Lean uses that arithmetic equivalence as the premise expressly permitted by the brief. Native witnesses verify the Gaussian Hadamard; a retained prime-3 obstruction rejects the order-three Fourier normalization. |
| O02: complete computable unitary reachability obstruction | Supplement §5 and `RationalUnitaryReachability` give the root-free isometry and its inverse. Native positive/negative certificates bind the original source and target. The dimension-four multiplier-3 example disproves identification with the whole similarity group. |
| P04: exact irreversible branch and three policy outcomes | Supplement §6 and the registered projection lemmas prove the specified projector, its complement, probability, positive target ray and zero branch. Replay preserves unitary success, positive postselection and zero-branch refusal separately. The two-step `3/16` example rejects the claimed universal cost/reachability trichotomy. |
| O03: Galois pair, finite bicommutant and sharp observation count | Supplement §8 proves all three with their separate domains. It provides the exact noninjective-menu/trivial-stabilizer counterexample and restricts linear completion counts to a declared linear carrier. The final audit also records the dimension-one action kernel; faithful semilinear ray action requires dimension at least two or passage to the faithful image. |
| CM-W1 and the full-probability dimension-two question | Supplement §7 gives a complement-closed six-ray permutation, a global extension argument and the `1/2` to `4/5` counterexample. Both implementations check the pocket. The four-reference-ray proof settles the proposed probability-preserver conjecture for the supplied positive form. |
| R13 compatible generators | Supplement §9 and Chapter 19A.6 prove the matrix-unit formula, skew-adjoint adjustment and Hermitian generator modulo rational scalars. The independent Python checker tests every supplied basis image, basis-pair Leibniz law and adjoint law. No Stone or exponential-flow conclusion is substituted. |
| Prose placement, status grammar and dependencies | Chapter 19A is between Parts IV and V. The theorem map, dependency table, separate supplement ledger and outstanding-claims register identify the results and their assumptions. The historical canonical status inventory is preserved. |
| Native certificate engine and bounded enumeration | The two named Rust owners implement exact submitted-witness checks, norm-class computation and budget exhaustion. Both scoped targets passed again on the integrated branch: 2 norm tests and 7 preserver tests, including all 728 and 6,560 stated height-one vectors. |
| Notebook and executable replay | The eight-cell notebook reproduces Hadamard, projection, dimension-three/four pockets and the generator example from both supported directories. Eight task-bound episodes replay without model calls. The 44 Python tests and 15 source-custody tests cover the stated witness/admission and retained-file boundaries. |
| Mechanized evidence and its limits | The registered run compiled 48 core-only modules and audited 660 selected declarations, including 26 new audits, with the standard axiom whitelist and no admitted proofs. This is the requested partial/conditional formal scope, not a total theorem census or verification of Rust/Python semantics. |
| Nonclaims and authorization | Every mathematical conclusion retains its supplied carrier/readout hypotheses. No branch selection, Born-rule derivation, continuum phase group, time evolution, physical instrument, universal gate set or authorization is inferred. |

The dimension-one correction changes no executable or Lean source: the
global classification already requires dimension at least three, and the
full-probability qubit result requires dimension two. The correction
clarifies the scope of the ray-cardinality and stabilizer consequences.
The registered source hashes and replay bindings were checked unchanged
after the final manuscript edits.

These obligations complete the corrected R12/R13 derivation brief.
Full-paper editorial consolidation, the historical release issues above,
and the programme's separately listed open mathematical targets remain
separate work; none is represented as resolved by this audit.

## Guarded-history coherence (GEN-WDP-69, Appendix P.20)

Written, mechanized, native and independent-replay scopes are separate.

| Scope | Evidence | What it does not establish |
| --- | --- | --- |
| Written theorem | Appendix P.20: star-shaped legality gives a connected, simply connected legal swap complex, with a constructive descent reduction; the native corollary for kind-ordered precedences, by case analysis over the five edit kinds. | No necessary-and-sufficient guard condition; no 4-cells, source covers or authority. |
| Lean | `lean4/WitnessedDifference/GuardedHistoryCoherence.lean`, 11 theorems, of which the 10 in the axiom report use axioms `propext` and `Quot.sound` ([receipt](../lean4/guarded_history_coherence_axioms.txt)): the abstract helper-swap step, its count-key instance, the failure of the converse swap at count zero, and invariance of a closed cochain under backtrack and face moves. | The van Kampen attachment argument and the Identify/Fill case analysis are not mechanized. |
| Native owner | `omega_engine/crates_rs/omega_wdp/src/genesis_guarded_history.rs`: legal-set enumeration through `Source25Run::replay`, legal swap complex, star-base search, exact rational first homology (spanning-tree contraction, then `exact_field` rank and left kernel; cross-checked against `homology_basis` on small components), separating cocycle, and constructive replacement lists. `cargo test -j 1 -p omega_wdp --test genesis_guarded_history`: 8 passed (rustc 1.98.0). | Finite families only; H1 = 0 over Q is a consistency check, not simple connectivity. |
| Bounded search | `wdp_guarded_search` (release build): 132,278 families in five declared tiers, 38,158 kind-compatible families with a legal history, 0 corollary or theorem failures, 65,253 witness lists replayed, 126 disconnected families, 1 family with H1 > 0 (three Remove-before-Add pairs, count two). Tiers B and C at six events: 184,593 families, no failure, no H1 > 0. | A bounded menu supports, and does not prove, the corollary. |
| Retained certificates | `code/causal_certificates/guarded_{compatible,p18,three_pairs}_{problem,certificate}.json`, schema `wdp-guarded-coherence-v1`, each bound to its problem bytes by SHA-256. | Certificates cover their stated problems only. |
| Independent replay | `scripts/check_guarded_coherence.py` re-executes every linear extension through the explicitly configured native adapter, recomputes edges, faces, components, kind compatibility and each component's rational H1 rank by exact elimination, checks a submitted star base or confirms that no legal history is one, replays each coherence witness, and checks cocycle closure on every legal face. Tests: `code/unit_tests/test_guarded_coherence.py`. On 2026-10-06 (Python 3.12.10, pytest 8.3.5) all three retained certificates passed with fresh native replay of all 24, 30 and 90 linear extensions against the adapter bound by `code/causal_certificates/native_build_receipt_guarded_2026_10_06.json` (rustc 1.98.0, offline, one job), and the two test files ran 114 tests with the native profile set, 0 skipped. After the review fixes (exact H1 rank, star-base absence), the same three certificates passed again and the two files ran 117 tests, 0 skipped. | The Python checker replays the three retained certificates only; the bounded-search witness lists are replayed by the native owner itself. Edges are checked for framed boundaries, not protected totals. |

## Native future retention (GEN-WDP-73, Appendix P.21)

Written, mechanized, native and independent-replay scopes are separate.

| Scope | Evidence | What it does not establish |
| --- | --- | --- |
| Written theorem | Appendix P.21 and [native future retention](derivations/native_future_retention.md): under either terminal convention, horizon-two signature equality is raw equality on the declared carrier (at most three terms, count total at most four, oriented filled triples), so an adequate report needs 29,771 classes; the report of mark, faces and counts capped at two attains it. The count 1 + 15 + 495 + 29,260 is derived combinatorially. | A minimum number of classes, not of fields, bits or instruments; no result beyond total four, three terms or two edits. |
| Lean | `lean4/WitnessedDifference/NativeFutureCompression.lean`, 21 audited declarations, axiom union `propext`, `Quot.sound`, `Classical.choice` ([receipt](../lean4/native_future_compression_axioms.txt)): signed-sum invariance, clipped reconstruction, removal answers, step projection and reflection, path lifting and composition. | A model of the guards; not verification of the Rust or Python source, the orbit enumeration or the carrier count. |
| Native owner | `omega_engine/crates_rs/omega_wdp/src/genesis_future_compression.rs`, test `cargo test -j 1 -p omega_wdp --test test_genesis_future_compression`. | Bounded carrier only. |
| Independent replay | `code/native_future_compression/` and `code/tests/python/e2e_tests/test_native_future_compression.py`: all 29,771 raw states and 1,250,382 offers compared with the bound native adapter and with the pinned original source closure (19 files). | The original-source comparison runs only when `WDP_ORIGINAL_SOURCE_ROOT` is set; otherwise that test is skipped. |
