# Track 2: exact finite evidence and explicit continuum boundaries

AuthorityEffect: None. This implementation addresses CDX-2.1, CDX-2.2, and
CDX-2.3 in the [Codex plan](../../../omega_engine_product_planning_office/plans/codex.md).
The claim dossier is [track2_claim](track2_claim/claim.md).
The local check results and existing limitations are in [verification.md](verification.md).

## Cyclic inclusions and Haar limits

For every positive integer N, the map j_N: Z_N -> R/Z sends k to k/N modulo
one turn. Addition is preserved, and its kernel is zero. When N divides M,
the refinement k -> (M/N)k commutes with these inclusions. The native kernel
stores exact rational turns; the formal model uses Mathlib's injective
`ZMod.toAddCircle` and the actual map `AddCircle.toCircle` into U(1).

The dyadic direct limit is Z[1/2]/Z, the Prüfer 2-group. It is dense in the
circle: a nearest point on the N-grid is at circle distance at most 1/(2N).
Its metric completion is the circle. The direct limit itself is countable;
it must not be identified with the completed compact group. Likewise,
compatible finite characters without a continuity condition include 2-adic
characters that do not extend to continuous circle characters. Continuous
circle characters are the integer frequencies x -> exp(2 pi i k x).
This implementation does not classify every compatible finite character.

The normalized N-grid character sum is 1 if N divides k and 0 otherwise.
Rust independently executes that sum in the existing exact cyclotomic field
Q(zeta_N). For a finite Laurent polynomial P(x) = sum c_k chi_k(x), its
finite average is sum_{N divides k} c_k. Every N > max |k| gives c_0 exactly.
The sum for chi_4 on N=4 is 1, while its continuous Haar integral is 0;
on N=8 the computed finite average is 0. This separating example prevents
premature recovery from being reported as success.

`lean4/circle_haar.lean` links an actual finite character sum to Mathlib's
normalized continuous Haar integral. It proves exact recovery beyond the
aliasing bound, convergence along dyadic grids for each integer character,
and convergence of every finite linear combination of those averages.
The existing project toolchain was inconsistent with the pinned Mathlib
revision; both now use Lean 4.34.0-rc1. No floating-point integral is used.

General continuous observables require a further argument: approximate f
uniformly by a Laurent polynomial P, use that normalized grid averaging and
normalized Haar integration each change by at most ||f-P||_infinity, and use
exact eventual recovery for P. This proves weak Haar convergence by Fourier
polynomial density. The density extension to every continuous f and the full
Pontryagin dual classification are research obligations in the ledger; this
package mechanizes the character and finite-polynomial portion.

For rational samples of a real periodic L-Lipschitz function, Rust verifies
every dyadic sample count, consistency at inherited points, and every cyclic
adjacent inequality, including the wrap-around seam. The resulting exact
average R_N has conditional integral enclosure R_N +/- L/(2N): on each
cell, integrate |f(x)-f(k/N)| <= L(x-k/N) and sum the N cell bounds.
The final cyclic samples have a piecewise-linear L-Lipschitz extension, so
these finite checks are consistent evidence. They do not establish a unique
all-level sampling family or prove an arbitrary caller supplied sequence of
Riemann sums came from a function. The legacy sum-only receipt now states
that limitation explicitly.

The production owner is `omega_number_theory::circle_haar`, delegating to
the existing rational-turn, dyadic-presentation, and cyclotomic owners. Native execution is
bounded to orders 1..128, at most 64 polynomial terms, or eight dyadic sample
levels. The mathematical inclusions and formal character theorem have no
such fixed execution ceiling.

## Finite presentation meta-theory and Genesis

A directed graph supplies an incidence difference map D. A bijection of its
vertices is an observable symmetry only if it preserves actual adjacency;
it then induces an edge permutation with P_1 D = D P_0. Since permutation
matrices are orthogonal, the graph Laplacian D^T D commutes with P_0. Thus
Dirichlet energy is preserved when a state is transformed. This does not
assert that the original state is fixed by the permutation.

For C^0 --d0--> C^1 --d1--> C^2, the native cochain owner first checks d1*d0=0.
Each proposed signed basis permutation must be a bijection of exactly the
declared carrier with signs +/-1. The checker verifies P_(i+1)d_i=d_iP_i.
If d_i x=0, then d_iP_i x=P_(i+1)d_i x=0; if x=d_(i-1)y, then
P_i x=d_(i-1)P_(i-1)y. Hence kernels and images are preserved and an
automorphism descends to cohomology. A separately supplied square difference
operator is checked for DP=PD. This profile covers signed permutation
symmetries; it does not enumerate all invertible rational chain maps.
`lean4/finite_presentation.lean` mechanizes cocycle and coboundary preservation
for commuting finite rational linear equivalences, and preservation of a
difference operator's kernel.

`omega_homology::presentation_symmetry` owns these checks, using the existing
canonical graph, cochain complex, and exact matrix owners. The host validates
dimensions and bounded carriers before producing evidence. Duplicate image
indices, adjacency-changing permutations, a nonzero d1*d0, and a difference
operator that fails to commute are separating refusals.

Genesis's [Two Boxed Laws](../../../omega_engine_education/documentation/002_s_n/README.md)
remain the boundary. Only an unresolved native Genesis obstruction in the
current active register W_n can force the next scale S_(n+1). The persistent
history H_n retains prior obstruction events; its existence does not imply
that those obstructions remain active. A model realization R(S_n) cannot
extend S_n. A failed symmetry, aliasing example, or incomplete SQL carrier
is a downstream model defect, never an insertion into W_n.

Every bridge receipt therefore has `authority_effect: "None"`,
`genesis_effect: "None"`, `realizes: null`, and
`genesis_register_access: "not_performed"`. No empty global Genesis register
is inferred. The claim ledger records research obligations separately from
native active obstructions and from the persistent Genesis history.

The `continuum_evaluate` action is advertised by the existing native runtime
dispatcher. Python calls it solely through the canonical Rust-host adapter,
retains the entire runtime outcome, and recomputes its input commitment.
Native rejection is `Ok` with `success: false`; transport/integrity failures
are `Err(Refusal)`. Caller supplied verification or authority fields are refused.

## All relational schema sources

The inventory covers the governance storage schema, governance normal-form
schema, both education SQL copies, the closed-candidate schema, and the
embedded append-only receipt ledger: 84 table declarations across six sources.
`schema_pipeline.py` checks the exhaustive source list, each heading, total
SQL keys, explicit optional domains, and minimal candidate keys under the
declared key-to-heading FD theory. New text primary keys are explicitly
NOT NULL. Integer rowid keys retain SQLite's allocation behavior.

For legacy databases, INSERT and UPDATE triggers fence required facts after
the existing additive migrations. A pre-existing null protected fact raises
`SchemaContractError`; no stored row is rewritten or silently coerced. The
normal-form evaluator installs the same guards. CDC INSERT, DELETE, and
UPDATE rows require their appropriate before/after images, and binary flags
reject NULL or values outside 0 and 1.

The projection pipeline chooses a minimal total key K and emits K union {a}
for each nonkey attribute a, plus exact reconstruction SQL. The existing
FD chase checks losslessness and dependency preservation separately. The
education examples additionally declare student_id -> student_name,
course_code -> course_title, and instructor_id -> instructor_office. Their
2NF/3NF/BCNF diagnoses, Bernstein 3NF synthesis, BCNF decomposition, and
key-plus-one-attribute refinements use those actual dependencies. The input
instance is checked for FD violations with null-safe comparisons.

JSON and CSV storage scalars do not establish semantic 1NF. Complete MVD and
JD declarations are still required before asserting semantic 4NF, 5NF, or
unrestricted 6NF. Educational REAL aggregate tables retain their approximate
numeric scope. The new SQL-TOTAL YAML contract states the four normal-form
pillars and this qualification gap; certification does not imply authorization.

Closed-candidate coverage uses stable unique IDs, the exact declared
cardinality, set differences in both directions, and an input-digest foreign
key. It rejects empty, missing, duplicate, foreign, or input-mismatched
carriers. Negative checked outcomes still count toward exhaustiveness.
Structural coverage does not certify the truth of an externally supplied
verdict or the derivation of a caller declared carrier.

## Reproduce the evidence

Use Python 3.12 and the local Rust workspace. From the repository root:

```bash
cargo test --locked -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_number_theory circle_haar --lib
cargo test --locked -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_homology presentation_symmetry --lib
cargo test --locked -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_symbol_game --lib invoke::
cargo build --locked -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_symbol_game --bin omega_symbol_game
python -m pytest -q omega_engine_projects/finite_to_continuum/tests/test_native_bridge.py omega_engine_projects/finite_to_continuum/tests/test_continuous_haar_limit.py omega_engine_projects/finite_to_continuum/tests/test_presentation_closure_examples.py
python -m pytest -q omega_engine_education/tests/normal_forms/test_schema_pipeline.py omega_engine_governance/tests/unit/test_sqlite_governance_unit_of_work.py omega_engine_governance/tests/unit/test_sqlite_repositories.py
python -m omega_engine_pfp.infrastructure.normal_forms.schema_pipeline
python omega_engine_projects/finite_to_continuum/_docs/track2_claim/checker.py
cd omega_engine_projects/finite_to_continuum/lean4
lake --no-cache build
```

The local source build works without Mathlib's external cache. In restricted
cloud environments, cache downloads may be denied, and elan's release index
may also be denied. The official Lean 4.34.0-rc1 Linux archive has SHA-256
`41dc6a6ec143ece8ed4ba4c4c6978c91f21ad5cbe3c4e7728ad31b869961dc17`;
an extracted, checksum-verified toolchain can be linked with elan.
