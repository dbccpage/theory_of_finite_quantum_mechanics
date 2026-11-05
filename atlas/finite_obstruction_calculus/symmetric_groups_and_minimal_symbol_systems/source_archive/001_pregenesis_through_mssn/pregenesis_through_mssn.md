---
documentation_contract: symbol-game-documentation/v1
title: "Pre-Genesis Through MSS-N: An Architectural Walkthrough of the Four-Layer Epistemic Hierarchy"
kind: mathematical-reference
audience:
  - researchers
  - engineers
  - coding-agents
status: active
maturity: research
claim_status: review_required
authority_effect: "None"
source_paths:
  - ../../../000_pre_genesis/grammar/pre_genesis.ebnf
  - ../../../001_genesis/grammar/genesis.ebnf
  - ../../../002_s_n/grammar/sn.ebnf
  - ../../grammar/mssn.ebnf
prerequisites:
  - ../../../000_pre_genesis/README.md
  - ../../../001_genesis/README.md
  - ../../../002_s_n/README.md
  - ../../README.md
  - ../000_mssn/paper.md
aliases:
  - pregenesis_through_mssn
  - four_layer_architecture_monograph
related:
  - ../000_mssn/paper.md
  - ../../../002_s_n/papers/000_sn/paper.md
  - ../../../001_genesis/levels/level_15_progress_licensing_contract.md
  - ../../levels/level_11_polygraph_confluence_peaks.md
  - ../../levels/level_15_rbg_authority_separation.md
  - ../../levels/level_28_homotopy_type_equivalence.md
  - ../../levels/level_58_contextuality_scenarios.md
  - ../../levels/level_75_incremental_views.md
  - ../../levels/level_76_topological_database_cells.md
  - ../../levels/level_100_open_horizon_and_release.md
last_verified: 2026-10-08
---

# Pre-Genesis Through MSS-N: Architecture and Evidence Boundaries

AuthorityEffect: None. GenesisEffect: None.

## Abstract

This paper describes the relationship between four repository strands: Pre-Genesis,
Genesis, the S(n) presentation tower, and the MSS-N specification atlas. It separates
declared architectural rules from proved mathematical statements and executed tests.
The mathematical reference is [MSS-N](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/papers/000_mssn/paper.md). An atlas entry, parser
acceptance, numerical residual, or successful fixture is not a derivation of that
entry from Genesis. No physical theory is derived by this walkthrough.

The earlier physics-verification catalogue is withdrawn. Its audit found prescribed
outputs presented as measurements, scalar identities presented as physical theorems,
and SQL checks that could pass absent evidence. The removal record and retained scope
are in [the cleanup review](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/physics_claim_cleanup.md).

## 1. Four different starting objects

Keep these representations distinct:

| Object | Meaning |
| --- | --- |
| Absent input | The host received no payload. |
| Empty word epsilon | The length-zero word of a declared free monoid. |
| Literal `<>` | A concrete inscription interpreted under a specified grammar. |
| Admitted ground carrier | A mathematical object admitted by a declared rule. |

A host's representation of absence already presupposes that host. A printed token
does not establish an empty set, a singleton type, a terminal object, or a universe.
The [Pre-Genesis grammar](../../../../../../../omega_engine_education/documentation/000_pre_genesis/grammar/pre_genesis.ebnf) is a
syntax boundary. Supply inertia is an architectural requirement on the state
transition semantics; syntax checking alone does not establish it.

## 2. Genesis and the presentation tower

The two governing architectural rules are:

1. An extension needs an unresolved obstruction relative to declared protected laws.
2. A mathematical realization has no authority to extend the native derivation.

An obstruction must name its carrier, witnesses, protected law, and activity test.
The [obstruction detector](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/code/rust/src/obstruction_detector.rs) and its
[Lean model](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/lean4/MssnObstructionDetector.lean) are specific finite encodings
of those requirements. Their scope is the statements represented in those files.

The [S(n) paper](../../../../../../../omega_engine_education/documentation/002_s_n/papers/000_sn/paper.md) defines the native
presentation stages. It must remain the source for their meaning. Neither a new
alphabet character nor an atlas row silently creates a new native stage.

### Active demands and recorded history

For finite active demand sets, let
\[
W_{n+1}=(W_n\setminus D_{n+1})\sqcup B_{n+1},
\]
where \(D_{n+1}\subseteq W_n\) and \(B_{n+1}\cap(W_n\setminus D_{n+1})=\varnothing\).
Then, writing \(s_n=|W_n|\), \(d_{n+1}=|D_{n+1}|\), and \(b_{n+1}=|B_{n+1}|\),
\[
s_{n+1}=s_n-d_{n+1}+b_{n+1}.
\]
This is a finite-set accounting identity under the stated premises. It does not
prove that any particular engine uses this demand representation. History length,
active demand count, and added-generator count are separate measurements.

## 3. Three indices and a grammar

| Index | Object being counted | What it does not establish |
| --- | --- | --- |
| Alphabet index k | Available terminal symbols | Admitted operations or semantic power |
| Genesis stage n | Native admitted presentation | Atlas coverage |
| MSS row m | A specification target | A completed derivation or working evaluator |

In particular, MSS-2 is not S(2). The old table using one index for all three
objects has been removed.

With repetition admitted, a singleton alphabet supports unary counting. Adding a
second letter permits a free noncommutative monoid under concatenation. Free monoids
on two and ten generators are not isomorphic: an isomorphism preserves the
indecomposable nonidentity elements, which are exactly their letters. Binary and
decimal numeral systems may encode the same natural numbers after a decoding rule
is declared; that is a different statement.

A directional glyph does not by itself supply a directed relation, an interval
type, or an opposite category. Each interpretation needs a carrier, formation rules,
identity rules, and operations. Grammar conformance establishes well-formedness in
the [MSS grammar](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/grammar/mssn.ebnf), not the mathematical claims attached to
the resulting strings.

## 4. Retractions and conservative extensions

The central theorem from the companion paper supplies a useful restriction. For
chain maps \(i:C\to D\) and \(r:D\to C\) with \(ri=\mathrm{id}_C\), the induced
map \(H_k(i)\) is injective. Indeed, if \(i(z)=\partial b\), then
\(z=r(i(z))=\partial r(b)\). Thus an extension cannot kill a nonzero original
homology class while retaining that chain-map retraction.

Every proposed bridge must therefore state which structure its retraction preserves.
A syntactic erasure map, a set retraction, and a chain-map retraction are different
contracts. A lift that fills a protected cycle cannot claim all three merely because
a string round-trip succeeds.

For each bridge record: source and target types; inclusion and down-map; the
retraction equation; preserved laws; rejection cases; and the executable or formal
evidence. An unimplemented bridge remains an obligation.

## 5. Proposal, evaluation, and authorization

The intended roles remain separate:

| Role | Output | Required evidence |
| --- | --- | --- |
| Proposer | Candidate data | No execution authority follows from generation. |
| Evaluator | A scoped result and evidence | Recompute the property of the submitted candidate. |
| Authorizer | A scoped execution decision | A declared authority rule bound to the intended action. |

The [authority-separation target](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/levels/level_15_rbg_authority_separation.md)
describes this boundary. A theorem that replay leaves an already halted state
unchanged establishes halted-state inertness. By itself it does not prove independent
authorization, cryptographic binding, or safety of transitions from active states.
Those need their own implementation and verification obligations.

Normal-form YAML declarations state contracts. Schema validation establishes their
shape. A contract becomes enforced behavior only through a checker and tests of its
acceptance and refusal cases. `AuthorityEffect: None` is a scope declaration; it
cannot substitute for checking the result.

## 6. Correct scope of selected mathematical examples

### Equivalence and univalence

Forward and backward maps with two-sided inverse witnesses establish equivalence
of the declared carriers. They do not establish univalence
\(\operatorname{Id}_{\mathcal U}(A,B)\simeq(A\simeq B)\).
Ordinary Lean equality is proof-irrelevant; a univalent universe would require an
explicit alternative encoding and its own proof. The earlier finite-univalence
verification claim is withdrawn.

### Contextuality

For a normalized binary Bell model with compatible marginals, a test based on CHSH
must check all relevant inequality orientations. The earlier single-expression
criterion misses the uniform-marginal correlators \((1,1,-1,1)\): its selected
expression is zero, while another orientation is four. There is no deterministic
global assignment satisfying all four signs.

A nonnegative Bell-violation score is not, without further construction, a Cech
cohomology class. No presheaf/cochain construction establishing that identification
is supplied here. The asserted universal curvature-to-CHSH relation is also withdrawn.

### Finite matrix trace and the new algebra examples

For square matrices over a commutative field, trace cyclicity gives
\(\operatorname{Tr}([A,B])=0\). If the field has characteristic zero, \(N>0\),
and \([A,B]=cI_N\), then \(Nc=0\), hence \(c=0\).
The retained Lean statement treats 2-by-2 integer matrices. The Rust tests
exercise particular Gaussian-rational matrices and three real skew-symmetric
so(3) generators; they do not quantify over every matrix.

The code also evaluates the declared nonnegative quantity
\(\tfrac14\sum_{i<j}\|[X_i,X_j]\|_F^2\). The supplied three-generator example
has value \(3/2\); commuting identity matrices give zero. This calculation does
not implement BFSS/IKKT dynamics or establish a fuzzy-sphere physical solution.
The former paper displayed a SQL action view without a corresponding checked
schema implementation; no SQL/Lean/Rust bisimulation result is retained.

### Finite executable examples

| Retained computation | Evidence location | Scope |
| --- | --- | --- |
| Boundary products and finite complexes | [physics kernel](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/domains/physics/code/domain_physics_kernel.py), [higher-order complexes](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/domains/physics/code/higher_order_regge_cohomology.py) | Declared finite incidence data; numerical ranks need numerical qualifications. |
| Matrix determinants, signed pairs and commutators | [Rust finite algebra](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/code/rust/src/finite_algebra.rs), [Lean finite algebra](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/lean4/MssnFiniteAlgebra.lean) | Finite algebra; Rust arithmetic has representation limits. |
| Stored anyon-model matrices | [matrix evaluator](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/domains/ansi_sql/code/nonabelian_anyon_evaluator.py) | Fusion counts, complete F-matrix involution and B3 checks; no full pentagon/hexagon certificate. |
| Finite graph diffusion | [diffusion code](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/domains/physics/code/cdt_spectral_dimension.py) | Return probabilities and numerical slopes of a declared graph; no inferred Planck scale. |
| Finite overlap matrices | [operator code](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/domains/physics/code/cdt_overlap_evaluator.py) | Numerical Ginsparg-Wilson residual and nullspace chirality; no gravitational or locality theorem. |
| Scalar and link-gauge examples | [gauge code](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/domains/physics/code/cdt_matter_coupling.py) | Declared finite-field calculations; no matter-backreaction or collapse prediction. |

Some retained filenames have historical `cdt` names for import continuity. Their
documented scope is the finite numerical calculation, not a CDT implementation.
SQL `REAL` values and tolerance checks are floating-point computations, not exact
rational or algebraic proofs. A successful comparison with fixtures is not a proved
SQL/Lean bisimulation.

## 7. Withdrawn physical claims

This revision withdraws certification of supersymmetric CDT, Nicolai sign suppression,
Super-WDW solutions, instanton tunnelling, Kähler-Dirac doubling resolution, classical
Einstein convergence from the supplied quadratic sampler, and Weyl-superconductor
surface/anomaly results. The corresponding fabricated implementations and dependent
tests are removed where identified. It also removes the analytical AJL reproduction,
hard-coded sub-cubic benchmark, and simulated measured Berry phase.

These withdrawals apply to finite-model claims as well as continuum claims. A
disclaimer about not deriving the Universe does not validate a smaller unsupported
statement about a finite physical model. Passing a test of a supplied flag or of an
expected value copied into the result does not establish the advertised computation.

## 8. Joining the two papers

Use the companion MSS-N paper as the mathematical backbone. This walkthrough
contributes the architectural crosswalk, typed bridge obligations, and evidence
boundaries. Preserve one authoritative statement of each theorem and link to it
from the architecture. Application examples belong in separately scoped appendices.

Before consolidating the manuscripts, each accepted claim must identify its exact
proposition, premises, representation, evidence symbol, arithmetic model, and a
negative test where executable checking is claimed. Distinguish a proved statement,
a checked finite instance, a numerical experiment, an architectural requirement,
and an open obligation. Test counts measure exercised cases, not derivational depth.

## 9. Verification and open work

[Counterexample regressions](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/code/tests/test_physics_claim_regressions.py)
exercise missing/malformed anyon data, the overlap-index sign and basis-independent
chirality, probability preservation at isolated graph vertices, relabelling
invariance, and graph-dependent diffusion. [Rust regressions](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/code/tests/rust/test_signed_pairing_regressions.rs)
check cancellation, malformed signs, duplicate identifiers and empty ensembles.

The [cleanup record](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/physics_claim_cleanup.md) gives the pinned baseline,
removal reasons, retained scope and actual validation results. No repository-wide
physical recovery, complete atlas realization, or end-to-end PFP correctness claim
is made by this paper.
