# Research-Library Routing Blueprint for the Solver of Solvers

- **Document status:** architecture blueprint with explicit `IMPLEMENTED` and
  `PROPOSED` labels
- **Runtime status:** no research-library router is implemented by this document
- **AuthorityEffect:** `None`
- **Scope:** finite, corpus-bound adapter selection and candidate routing

This blueprint lowers the research-library flow in the central
[Atlas upgrade blueprint](../../../../omega_engine_pfp/documentation/atlas/10_research_library_system_upgrade_blueprint.md)
onto the current solver-of-solvers seams. It does not turn papers into executable
plans, expose a general solver RPC, or infer that a change of representation is
a valid carrier lift.

## 1. Governing Atlas contracts

The local design depends on these central documents rather than restating their
authority and transport rules:

- [object language, metatheory, and admission](../../../../omega_engine_pfp/documentation/atlas/00.2_object_language_metatheory_and_admission.md);
- [finite board declarations](../../../../omega_engine_pfp/documentation/atlas/02.1_symbol_game_board_contract.md);
- [same-level moves and carrier reframes](../../../../omega_engine_pfp/documentation/atlas/03.1_fibred_polarity_and_carrier_lifts.md);
- [cross-domain move transfer and anomaly records](../../../../omega_engine_pfp/documentation/atlas/05_cross_domain_move_transfer_atlas_and_anomaly_cartography.md);
- [transport certificates, typed holes, and loss ledgers](../../../../omega_engine_pfp/documentation/atlas/05.1_transport_certificates_and_loss_ledgers.md);
- [counterexample-guided candidate admission](../../../../omega_engine_pfp/documentation/atlas/07_skill_pharmacy_counterexample_admission.md); and
- [proposed receipt catalog and lowering](../../../../omega_engine_pfp/documentation/atlas/12_receipt_catalog_and_clean_architecture_lowering.md).

The required order is:

```text
source artifact
  -> corpus identity and disposition
  -> admitted mathematical spine
  -> typed research problem
  -> admitted adapter-capability query
  -> explicit finite candidate declaration
  -> independent candidate evaluation
  -> finite plan frontier
```

Corpus admission precedes adapter selection. A source-only record, a failed
identity check, or an empty mathematical spine must stop before the adapter
registry is queried.

## 2. Current implementation boundary

### 2.1 `IMPLEMENTED`: Python finite plan frontier

[`omega_engine.crates.kernel.solver_of_solvers`](../../kernel/solver_of_solvers.py)
implements a pure router for one explicit finite batch:

- `SearchDeclarationV1` binds a grammar digest, policy digest, cost order,
  cost dimension, and candidate cap;
- `CandidatePlanV1` binds a normalized term, plan kind, cost vector, and
  provenance digest;
- `PlanEvaluationV1` binds a caller-declared status, residual vector, verifier,
  replay-receipt reference, and environment;
- `DeclaredPlanEvaluationV1` is deliberately a structural binding with no
  replay claim;
- `route_declared_batch` partitions verified, rejected, and inconclusive
  candidates, removes only cost-dominated verified candidates, and preserves
  co-minimal frontier classes; and
- `route_declared_finite_grammar` additionally requires an exact, complete
  declared grammar batch.

The scope is exactly `EXPLICIT_FINITE_BATCH`. The module does not execute a
solver, replay a receipt, prove exhaustiveness outside the declared grammar,
select an arbitrary first winner, or mint authority. Existing behavior is
covered by
[`test_solver_of_solvers_frontier.py`](../../../_tests_unit/test_solver_of_solvers_frontier.py).

### 2.2 `IMPLEMENTED`: OESOS compatibility registry and cascade

The local [`SolverRegistry`](registry.py) is only a map from a residual-class
string to an ordered list of solver IDs. [`ObstructionProblem`](problem.py)
currently carries `problem_id`, `carrier_ref`, `residual_class`, `scope`, a
numeric budget/window, metadata, and `AuthorityEffect: None`.

[`OesosCascade`](cascade.py) runs the existing Prime 000 declaration gate,
optionally checks Prime 002 continuation, and then invokes explicitly installed
stage handlers. A handler-free stage records a declarative registry choice; it
does not demonstrate adapter capability or solver correctness. Tests at
[`test_prime_triad_oesos.py`](../../../_tests_unit/test_prime_triad_oesos.py)
exercise refusal before admission and the explicitly supplied-handler path.

These compatibility types are not the proposed research adapter registry. In
particular, ordered solver IDs are not evidence, ranking is not evaluation, and
choosing the first registered ID is not a validity claim.

### 2.3 `IMPLEMENTED`: Rust exact finite-carrier seam

[`omega_solvers::solver_of_solvers`](../../../crates_rs/omega_wdp/src/solver_of_solvers.rs)
is the canonical exact mathematical seam currently available. Its public
`solve(&FiniteCarrier2, &[i128])` path:

- accepts one declared finite 2-complex with positive edge weights;
- works over exact rational coefficients, with integral and torsion semantics
  explicitly outside scope;
- computes exact weighted-L1 projection certificates;
- binds carrier and evidence manifests;
- returns a typed diagnostic and `AuthorityEffect::None`; and
- runs aggregate `replay_solve` before returning on the final full-projection
  branch. Early returns for a face-empty or gauge-exact carrier, and for the
  zero joint projection, rely on their sealed inner evaluations and do not run
  that aggregate replay inside `solve`.

The same module contains `lift` and `probe_lifts`, but only for a caller-declared
finite list of added triangular faces on the same one-skeleton. Those functions
retain before/after receipts, typed refusals, and budget-relative
irreducibility. They do **not** establish a general carrier-lift operation,
cross-domain transport, or permission for this research router to invent a
carrier change. The Rust module also records cross-process receipt
serialization as open work; therefore it is not a general solver RPC.

## 3. Proposed typed problem contract

### 3.1 `PROPOSED`: `TypedResearchProblemV1`

Adapter selection must consume a problem typed by carrier, input
representation, coefficient domain, witness, checker, and evidence ceiling—not
a paper title or keyword match.

```yaml
schema_version: omega.typed-research-problem.v1
problem_id: research-problem-001
corpus_admission_ref: corpus-admission/full-sha256
math_spine_ref: math-spine/full-sha256
claim_ref: claim/full-sha256
carrier:
  kind: FINITE_2_COMPLEX
  artifact_ref: carrier/full-sha256
  identity_digest: sha256/full-64-hex
  orientation_profile: directed-weighted-edges-triangular-faces/v1
input_representation:
  edge_weight: I128_STRICTLY_POSITIVE
  residual_coordinate: I128
  exact_embedding: I128_TO_Q
coefficient:
  domain: Q
  arithmetic_mode: EXACT_RATIONAL
witness:
  kind: L1_PRIMAL_DUAL
  required_artifact_schema: omega.exact-phi1-certificate.v1
  required_obligations:
    - primal_feasibility
    - dual_feasibility
    - exact_zero_gap
checker:
  checker_ref: omega_solvers::solver_of_solvers::replay_solve
  checker_digest: sha256/full-64-hex
  replay_profile: in-process-rust-exact/v1
  environment_digest: sha256/full-64-hex
evidence_ceiling:
  maximum: LOCAL_REPLAY
  forbidden_promotions:
    - GLOBAL_THEOREM
    - ADAPTER_ADMISSION
    - AUTHORIZATION
budget:
  max_candidates: 16
  cost_dimension: 3
authority_effect: None
```

All six type axes are mandatory. An unknown carrier, unsupported input
representation, coefficient coercion, missing witness schema, checker mismatch,
or requested ceiling above the adapter's admitted ceiling produces a typed
`NO_CAPABILITY_MATCH`; it never falls back to a generic model or free-form RPC.

### 3.2 `PROPOSED`: `AdapterCapabilityV1`

```yaml
schema_version: omega.adapter-capability.v1
adapter_id: rust.finite-2-complex-q-l1.v1
implementation_ref: omega_solvers::solver_of_solvers::solve
implementation_digest: sha256/full-64-hex
admission_record_ref: adapter-admission/full-sha256
supported_carriers: [FINITE_2_COMPLEX]
supported_input_representations:
  - edge_weight: I128_STRICTLY_POSITIVE
    residual_coordinate: I128
    exact_embedding: I128_TO_Q
supported_coefficients:
  - {domain: Q, arithmetic_mode: EXACT_RATIONAL}
supported_witnesses: [L1_PRIMAL_DUAL]
checker_refs:
  - omega_solvers::solver_of_solvers::replay_solve
maximum_evidence_ceiling: LOCAL_REPLAY
fixture_refs:
  - fixture/filled-triangle-q
  - fixture/bare-cycle-q
authority_effect: None
```

The proposed registry query is an exact capability-subsumption check. It runs
only over adapter entries with a live external admission record. Corpus
admission says the source has a usable, source-bound mathematical object;
adapter admission says one implementation may evaluate one declared class of
objects. Neither implies the other.

## 4. Corpus admission before routing

### 4.1 `PROPOSED`: admission gate

The `CorpusAdmissionPort` must return a host-created record containing:

- source artifact identity and full digest;
- source spans for definitions, carrier data, coefficient declarations,
  witnesses, bounds, and counterexamples;
- identity/disposition result;
- nonempty mathematical spine or a typed absence;
- requested domain and contamination findings;
- maximum evidence ceiling supported by the source record; and
- verifier and replay references for admitted extracted objects.

Only `ADMITTED_FOR_ADAPTER_QUERY` may proceed. At minimum these outcomes stop:

```text
SOURCE_ONLY
IDENTITY_MISMATCH
IDENTITY_NOT_FOUND
EMPTY_MATH_SPINE
DOMAIN_CONTAMINATED
CORPUS_ADMISSION_BOUNDED
```

The adapter registry must not be called speculatively and then used to justify
corpus admission after the fact. This ordering prevents a familiar laundering
loop: choose a convenient adapter, reinterpret the paper to match it, and report
the adapter's local success as support for the paper.

## 5. Proposed finite search and regret semantics

### 5.1 `PROPOSED`: `SearchDeclarationV2`

`SearchDeclarationV2` extends, but does not replace, the implemented V1 finite
frontier semantics.

```yaml
schema_version: omega.search-declaration.v2
canonicalization_profile: omega-canonical-v1
numeric_profile: normalized-rational-string-v1
problem_ref: research-problem/full-sha256
grammar_id: grammar.research-plan.v2
grammar_digest: sha256/full-64-hex
policy_digest: sha256/full-64-hex
explicit_candidate_ids: [candidate-a, candidate-b, candidate-c]
max_candidates: 3
cost_order: PARETO
cost_dimension: 3
oracle:
  oracle_type: FULL_INFORMATION_DECLARED_PAYOFF
  oracle_ref: oracle/regret-ranker/v1
  oracle_digest: sha256/full-64-hex
regret_budget:
  N: 3
  T: 100
  eta: "1/20"
  delta: "1/100"
  perturbation_count: 16
  seeds: [7, 11]
  support_cap: 3
reported_metrics:
  external_regret: "3/25"
  internal_regret: "19/100"
  fixed_point_residual: "3/100"
ranked_candidate_ids: [candidate-b, candidate-a, candidate-c]
authority_effect: None
```

The implemented V1 canonicalizer admits null, booleans, integers, strings,
maps, and lists, and rejects floats. V2 therefore serializes every non-integral
quantity as a reduced `numerator/denominator` string with positive denominator;
parsing, reduction, and denominator checks precede hashing. All fields shown,
including reported metrics and ranked candidate IDs, are identity-bearing in
this proposed replay envelope. An implementation may split the pre-run
declaration from a post-run ordering record, but each record must have its own
digest and the evaluation batch must bind both.

Regret metrics rank or schedule candidates only. They may not:

- set `EvaluationStatus`;
- rewrite a candidate cost or provenance record;
- remove a declared candidate's final disposition;
- raise the evidence ceiling;
- admit an adapter, witness, paper, or skill;
- convert a partial run into `NO_VERIFIED_PLAN`; or
- authorize a carrier change or external effect.

Independent checker-bound evaluations remain the only inputs to the implemented
finite frontier. If the budget ends before every declared finite-grammar member
is evaluated, the proposed host outcome is `BOUNDED_WITH_OPEN_FRONTIER`, not
`NO_VERIFIED_PLAN`, `EXHAUSTED`, or global `UNSAT`.

## 6. Typed-hole trace routing

### 6.1 `PROPOSED`: target refilling contract

A typed-hole trace is an adapter-search hint, not a reusable proof. Structural
steps may be shared only with their typed input/output boundaries. Every
domain-oracle hole must be refilled by a target-domain artifact and a target
checker before the trace becomes an evaluable candidate.

```yaml
schema_version: omega.typed-hole-trace.v1
source_corpus_admission_ref: corpus/source/full-sha256
structural_steps:
  - step_id: s1
    operation_ref: refine_declared_partition
    source_type: finite-cover/v1
    target_type: finite-cover/v1
holes:
  - hole_id: h1
    required_fact_type: target-locality-witness/v1
    target_artifact_ref: null
    target_checker_ref: null
collision_key: sha256/full-64-hex
transport_loss_ledger_ref: loss-ledger/full-sha256
status: NEEDS_TARGET_REFILL
authority_effect: None
```

The transition to `READY_FOR_LOCAL_REPLAY` requires all holes to name target
artifacts, target checkers, and target replay results. Source-domain admission,
an isomorphic group, a shared move list, or an equal hole-pattern digest does
not fill a target hole. Transported artifacts remain proposed and retain their
loss ledger.

If refilling changes the carrier, coefficient domain, objective, rules, or
assumptions, the host creates a child reframe proposal. It must not dispatch the
Rust finite-face `lift` as a generic repair or describe the result as a general
carrier lift.

## 7. Concrete routing fixture

### 7.1 Positive finite-Q fixture

1. Admit a source artifact whose extracted spine explicitly declares a finite
   directed triangle, triangular face, strictly positive `i128` edge weights,
   an `i128` residual vector to be embedded exactly in `Q`, and an L1
   primal/dual witness obligation.
2. Build `TypedResearchProblemV1` with the Rust `FiniteCarrier2` profile, the
   `CarrierEdge.weight: i128` / `solve(..., omega: &[i128])` input
   representation, `EXACT_RATIONAL`, `L1_PRIMAL_DUAL`, `replay_solve`, and
   `LOCAL_REPLAY`.
3. Query the proposed capability registry and select only the admitted
   finite-2-complex/Q adapter.
4. Declare two normalized Python candidate plans: direct exact solve and one
   explicitly declared same-carrier preprocessing plan.
5. Allow `SearchDeclarationV2` regret metrics to choose evaluation order.
6. Evaluate both candidates through their named checker and bind both
   evaluation records.
7. Route the complete finite batch through `route_declared_finite_grammar`.
8. Preserve every evaluation and every co-minimal class. Report only the local
   fixture result under `AuthorityEffect: None`.

### 7.2 Required negative and near-miss fixtures

| Fixture | Expected result |
| --- | --- |
| Source identity passes but mathematical spine is empty | stop `EMPTY_MATH_SPINE`; registry not queried |
| Finite carrier requests `F2`, only finite-Q adapter is admitted | `NO_CAPABILITY_MATCH`; no coefficient coercion |
| Witness kind matches but checker digest differs | `CHECKER_BINDING_MISMATCH` |
| Typed-hole trace lacks target locality artifact | `NEEDS_TARGET_REFILL`; no candidate evaluation |
| Same trace after target artifact/checker/replay are supplied | candidate becomes `READY_FOR_LOCAL_REPLAY`, not admitted truth |
| Regret ranking is reversed while evaluation records are fixed | frontier identity and dispositions remain unchanged |
| One declared grammar member remains unevaluated | `BOUNDED_WITH_OPEN_FRONTIER`, not no-plan or exhaustive |
| Candidate changes carrier while marked same-level repair | `REFRAME_REQUIRED` |
| Rust lift candidate refuses | retain typed refusal; do not infer irreducibility |
| Candidate or model supplies `VERIFIED`, receipt, or authority fields | reject before routing |

## 8. Acceptance tests

### 8.1 Existing regression floor (`IMPLEMENTED`)

The implementation must continue to pass:

- Python frontier tests for order invariance, co-minimal preservation, Pareto
  incomparability, candidate/evaluation binding, grammar completeness, policy
  binding, mutation refusal, plan-kind separation, and no authority minting;
- OESOS tests proving Prime 000 refusal occurs before cascade execution and
  that only an explicitly installed handler executes; and
- Rust tests for representation refusals, exact carrier identity, replay
  tamper refusal, canonical status under nonunique optima, declared-lift
  effects, refused-candidate retention, and budget-relative irreducibility.

### 8.2 New routing tests (`PROPOSED`)

1. `test_corpus_refusal_prevents_adapter_registry_query` uses a spy registry and
   shows in this setup that its query count remains zero.
2. `test_adapter_match_requires_all_six_problem_axes` mutates carrier, input
   representation, coefficient, witness, checker, and evidence ceiling
   independently.
3. `test_f2_problem_never_falls_back_to_q_adapter` shows in this setup that there is no implicit
   coefficient conversion.
4. `test_unadmitted_adapter_is_invisible_to_selection` distinguishes catalog
   presence from external admission.
5. `test_regret_reorders_only` changes all regret fields and ranking while
   retaining identical evaluation and frontier dispositions.
6. `test_partial_ranked_batch_keeps_open_frontier` forbids no-plan, exhaustive,
   and UNSAT statuses.
7. `test_typed_hole_requires_target_artifact_checker_and_replay` mutates each
   refilling component independently.
8. `test_transport_does_not_inherit_source_admission` requires a target loss
   ledger and independent replay.
9. `test_carrier_change_forks_reframe` rejects a carrier mutation in a
   same-level plan.
10. `test_router_has_no_general_rpc_fallback` asserts that an unmatched problem
    returns a typed refusal without model-client, network-client, or subprocess
    dispatch.
11. `test_rust_lift_is_not_registered_as_generic_carrier_lift` limits its
    capability entry to the declared finite-face profile.
12. `test_authority_effect_none_end_to_end` checks corpus, problem, capability,
    search, evaluation, and frontier records.

## 9. Proposed implementation slices

1. Add frozen domain value objects for `TypedResearchProblemV1` and
   `AdapterCapabilityV1`; do not modify the existing compatibility registry.
2. Add a `CorpusAdmissionPort` and exact capability-query port. The application
   use case calls them in that order.
3. Add a read-only adapter-catalog implementation populated only from external
   admission records and pinned implementation/checker digests.
4. Add a pure `SearchDeclarationV2` ranker that emits an ordering record and
   then delegates evaluated candidates to the existing V1 finite frontier.
5. Add typed-hole completeness and reframe guards before candidate creation.
6. Register the Rust exact finite-Q seam with its narrow capability profile;
   expose no catch-all entry and no general RPC endpoint.
7. Add the fixtures above, canonical serialization vectors, and a link checker
   for the Atlas references in this document.

## 10. Claim ceiling and explicit nonclaims

This blueprint supports a design for routing source-bound, admitted finite
problems to narrow, admitted adapter capabilities and then ranking an explicit
finite candidate set. It does not establish or propose:

- a general solver RPC;
- automatic paper-to-solver compilation;
- title-, embedding-, or vocabulary-based adapter admission;
- a universal solver or complete search over undeclared candidates;
- a general carrier-lift operation;
- transport of evidence or admission across a carrier/domain change;
- validity from low regret, low cost, model consensus, or registry order;
- global UNSAT from no verified plan in one declared batch; or
- authority, policy admission, or external effects.

Every implemented and proposed record in this flow remains evidence-only with
`AuthorityEffect: None`.
