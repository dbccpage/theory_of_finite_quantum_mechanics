# Native owner decomposition and the Genesis contract boundary

AuthorityEffect: None. This source increment extracts three existing finite
implementations from `omega_wdp`; it does not change the canonical claim count,
close the five Genesis obligations, or assert a new publication/deposit.

## Implementations and compatibility

| Owner | Implementation | Retained WDP surface |
| --- | --- | --- |
| CODA | `omega_coda/src/diagnostic_routing.rs`: exact certificate replay, trichotomy, explicit policy and proposal receipts | `omega_wdp::diagnostic_routing` re-exports identical types and functions. |
| Prime Algos | `omega_prime_algos/src/finite_routing.rs`: commuting lift checks, strict descent/closure guard, finite fixed-point and partial terminal policy | `omega_wdp::finite_routing` re-exports identical types and functions. |
| LGGR (`omega_epk`) | `omega_local_green_global_red_lggr/src/matrix_path_kernel.rs`: rational matrix paths, closed-walk checks, supplied overlap residual and declared residual sequence | `omega_wdp::path_kernel_gluing` adapts public matrix/graph fields and preserves serialized shape, `WdpError` and the None-only authority type. |

There is one algorithm implementation for each row. The owners never depend
on WDP. Graph resolution remains in `omega_homology`, and matrix multiplication
and determinants remain in `omega_holonomy`. This preserves the previously
established linear-algebra, category, cochain, solver, arithmetic, quantum and
measurement ownership rather than introducing parallel algorithms.

The extracted CODA profile is mathematical diagnostic/proposal routing. It is
not a call to the full nine-layer operational pipeline or an authority grant.
The extracted Prime profile is a finite mathematical specialization; it does
not replace Prime 002's nine continuation conjuncts or sealed operational
terminalizer. Its existing DDC dependency remains the deformation owner.
WDP retains source custody, original-function adapters, observer assembly and
paper-specific receipt interpretation. Renaming those adapters into another
crate would not, by itself, establish a mathematical bridge.

## Validation scope

The original matrix-path regression cases move with their implementation.
Existing WDP diagnostic and finite-routing integration tests now exercise the
native CODA/Prime owners through the retained imports. A new compatibility
fixture checks a literal three-shear product and norm, serialization round-trip,
typed errors, post-deserialization validation, and the actual cross-crate
identity of packet and policy types. Exact observed results and native input
digests are recorded in `evidence/genesis_owner_receipt.json` after replay.

The initial four-crate batch records 681 passing tests at its original input
snapshot. After integrating the subsequent DDC/Prime cleanup from main, 32
checks in seven affected integration targets pass. The receipt preserves the
initial native input map and separately binds the new command and input delta;
it does not describe the earlier full batch as rerun on the new snapshot.
After a further main merge of solver cleanups and additive tolerance helpers,
all four selected libraries pass a separate offline, locked compile check.
That compilation does not refresh either earlier runtime-test count. The
incoming canonical PDF is preserved as an author asset; it was not rebuilt
or publication-verified in this source increment.

```sh
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_epk --lib matrix_path_kernel::tests
cargo test --offline --locked -j1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_wdp --test diagnostic_routing --test finite_routing --test native_owner_compatibility
```

These checks cover the extraction and its declared profiles. They are not a
new compiler, general sheaf/cohomology theorem, workspace-wide test result,
fresh Lean elaboration or a rebuilt publication artifact.

## Education and the central paper

The [Genesis/WDP crosswalk](../../../../../../omega_engine_education/documentation/020_genesis/wdp_integration.md) accounts for all 14
existing educational form contracts and points to the corresponding central
chapters and appendices. It preserves native, declared, metatheoretic and
optional-domain grades. The [shared language boundary](../../../../../../omega_engine_education/documentation/020_genesis/normal_forms/shared_language_boundary.md)
recommends extending the existing AutoP/PTIR compiler around versioned
reconstruction, protected-query and certificate contracts, with SQL as the
first proposed target. A proof hash or supplied flag is not a verified theorem;
a quotient key alone does not recover original labels or omitted history.

## Model-specific time refinement has a quantum owner

`omega_quantum_physics::meron_time_refinement` constructs the declared U=t
projectors using the existing `majorana_fock_algebra::FockCarrier` and the
exact linear-algebra matrix functions. It owns transfer multiplication and
the rational time/volume bounds. `omega_wdp::meron_time_adapter` retains its
immutable plan and computed trace with None authority; it duplicates neither
CAR nor matrix arithmetic. The existing native Fock ceiling still refuses
six-site evaluation. A bound object for a larger declared size does not erase
that refusal. The [model supplement](meron_time_and_volume_refinement.md)
states the written universal model theorem and the separate finite execution
and resource scopes.

## Derivative algebra and model readouts have different owners

`linear_algebra::exact_field::second_order_jet` owns generic noncommuting
value/first/second derivative multiplication and its whole-product resource
preflight. Quantum physics owns the staggered unitary, actual spin/parity
blocks and time-integrated insertion query in `meron_time_refinement`.
WDP's existing retained time adapter requests that query and compares its
partition with the previously computed owner partition. It introduces no
private derivative or spin solver. The [model/query proof](meron_spin_and_observable_transport.md)
states the boundary, normalization, finite resource and analytic scopes.

## Relational normal-form mathematics has a native owner

`omega_category_theory::finite_functional_dependencies` owns exact FD closure,
projected dependency covers, BCNF decisions, binary lossless join, dependency
preservation and bounded instance projection/join. It does not use WDP.
`auto_p::compiler::sql_normal_form` admits the existing contract AST, constructs
actual PTIR and emits the selected SQLite profile. `omega_wdp::sql_normal_form`
retains declared data and reconstruction targets and delegates those operations.
The [finite presentation proof](sql_normal_form_presentation.md) states the
universal schema and finite replay scopes; no solver is copied into WDP.

## Source fields and generic response error have separate owners

`omega_quantum_physics::meron_source_field` owns the declared temperature/
field plan and exact exponential majorant; its existing finite chain owns
the source generating trace and reuses generic matrix powers. The WDP time
adapter retains that plan and trace. `omega_measurement::finite_response`
uses existing bounded readings and kernel intervals to propagate three
pressure enclosures. Its optional third-derivative widening is conditional
on a supplied mathematical bound; it certifies no function regularity.
The [source proof](meron_source_field_response.md) keeps infinite-family
analysis, bounded computation, derivative control and authority separate.

## Analytic model bounds stay with the quantum owner

`omega_quantum_physics::meron_source_field::AnalyticResponsePlan` retains
the admitted temperature interval, exact time plan, source radius and
resolution. Its AR-7/AR-9 bounds are exact rational upper bounds derived
from the [written analytic theorem](meron_analytic_response.md).
`omega_wdp::meron_time_adapter::DeclaredMeronResponse` calls the existing
actual-chain moment owner and divides the time-averaged square by the site
count. It retains the original moments and plan, with AuthorityEffect None.
No second CAR, matrix, interval or polymer solver is introduced. The code
retains existing finite work caps and cannot execute the infinite schedule.

## Spatial test functions have a generic mathematical owner

`omega_functional::circle_piecewise_linear::CirclePiecewiseLinear` owns
immutable exact periodic knots, circle evaluation, uniform samples, derived
supremum/Lipschitz bounds and the squared integral. It chooses no Meron model.
`omega_quantum_physics::meron_spatial_source::SpatialSourcePlan` owns the
SG-6/SG-7 bounds and source-disk admission. Its actual chain owns weighted
moments and reuses the existing generic second-order matrix jet.
`omega_wdp::meron_field_adapter::DeclaredMeronField` retains the profile,
plan, original moments and bounded quadratic/finite-log/continuum-log readings.
Existing measurement and kernel interval owners supply the enclosures.
No second CAR, matrix, integration or interval solver is introduced in WDP.

## Consolidated CODA meanings and the retained carrier adapter

The [mathematical decomposition](coda_mathematical_decomposition.md) distinguishes
the primary finite CODA pipeline, its independent diagnostic/proposal profile,
canonical `omega_coda::q` and the `omega_q` compatibility re-export. Public
continuum-shadow strings and supplied grant metadata are not verified proofs.
The Rust FDA stage refuses unverified wire grants; the Python application
uses its configured one-use HMAC contract. Neither creates grantor standing.

`linear_algebra::gauge_pair_transport` owns generic exact pair aggregation,
the full fiber-size descent criterion and cycle-counterwitness replay.
`omega_wdp::genesis_transport_descent` binds that operation to actual
Source25 AddTerm/Identify execution and retains the complete source and target.
These are new mathematics and an adapter; no existing module is moved or split.

## Complete balance-edit profile

`linear_algebra::row_constraint_implication` owns homogeneous rational equation
implication and integer realization by exact denominator clearing. It calls the
existing `exact_field::elimination::solve_with_limits`; replay checks equations
directly and refuses malformed coefficients or separating vectors.

`omega_wdp::genesis_balance_transition` retains raw source/event/target and
implements Appendix P.7's five-case balance classification. Negative verdicts
include an actual legal balanced source and unbalanced edited target with the
same original carrier and marks. They do not replace the submitted state.
The native example `balance_preserving_edits` supplies the teaching fixtures.
No existing Rust module is moved or split.
