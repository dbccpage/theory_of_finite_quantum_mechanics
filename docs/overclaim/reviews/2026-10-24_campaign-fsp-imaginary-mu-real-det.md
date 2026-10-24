# Review of campaign FSP-IMAGINARY-MU-REAL-DET

AuthorityEffect: None.

Scope: one campaign target, based on main `5759edab096c0b7eb3fa2e63694b47f269d33241`.
The node's full original statement and status are retained. Source bindings and
the status/statement/protected-source audit are in the campaign replay and scope receipts.

Method: source-level statement review under the overclaim-hunter skill, plus the
separate fresh Lean build and independent exact replay recorded in this change.
This is the drafting agent's review, not independent human approval. Mathlib imports
were reused at the pinned commit; no whole-library rebuild or full Rust workspace
build is claimed. The strict scanner result is recorded in the campaign checks receipt.

Result: **0 FULL nodes, 1 NARROWED node, 0 OVERCLAIM nodes**. No node is raised.

Corrections to the PR's own text:

- Unit fugacity is the explicit hypothesis `star z * z = 1`, not merely
  `z^-1 = star z`, which would also admit zero (`CampaignFspImaginaryMuRealDet.lean:52`).
- Single-flavor positivity is attributed to the positive-mass bipartite staggered
  class, not to gamma Hermiticity alone (`CampaignFspImaginaryMuRealDet.lean:124`).
- Center periodicity is attributed to the declared finite orbit sum; the full QCD
  measure theorem remains imported (`CampaignFspImaginaryMuRealDet.lean:144`).

## Per-node statement-versus-theorem table

All Lean references below are in `lean4/CampaignFspImaginaryMuRealDet.lean`.

| Atomic claim in the original node | Declaration and exact scope | Verdict |
|---|---|---|
| Imaginary chemical potential restores gamma5 Hermiticity | `staggered_adjoint:69`, for the declared finite transport blocks and unit fugacity; G is staggered site parity. No exponential or spin-taste reconstruction theorem. | NARROWED |
| The determinant is real | `det_real_of_involution:76`, for arbitrary finite D and an involution G with G D G = D adjoint; `staggered_det_real:85` instantiates it. | FULL algebraic implication |
| Two identical flavors have nonnegative determinant | `two_flavor_nonneg:91`, for a determinant fixed by conjugation, using unrooted repeated diagonal blocks. | FULL finite implication |
| Positive-mass staggered determinant is nonnegative | `bipartite_one_det:100`, `bipartite_det_pos:119`, `staggered_det_pos:124` give strict positivity in the declared bipartite class, including arbitrary finite block sizes. | NARROWED to that class |
| Gamma Hermiticity alone suffices for positivity | The source's stronger reading fails: `gamma_hermitian_negative:133` has determinant -1 with a nontrivial involution. This does not contradict positive-mass staggered positivity. | NOT PROVED; counterexample supplied |
| QCD partition function has Roberge-Weiss periodicity | `centerSum_periodic:146` concerns any function averaged over a declared three-term center-orbit sum. No full gauge measure, temperature parameterization, or QCD partition function is formalized. | NOT PROVED for the full node |
| Imaginary-mu data provide controlled real-mu continuation | No such declaration; the original bottleneck and the independent note's open obligations retain this fence. | NOT PROVED |

The independent SU(3) cycle implementation is not a proved extraction from Lean.
Its parity split has the displayed block formula in the derivation note; concrete
matrix identities and Schur determinants are independently checked. No operator,
gauge-measure, continuum, or physical statement beyond those scopes is inferred.

## Numbers recomputed

| Claim | Exact recomputation | Result |
|---|---|---|
| Queue rank 19, with rank 18 occupied | Queue JSON and the existing rank-18 branch/worktree and derivation files, read before selection. | Match |
| 27 lattice cases | Three declared sizes times three unit fugacities times three masses, all enumerated by the independent checker. | Match |
| Three colors, coefficient 1/2, cycle sizes 2/4/6, masses 0, 1/3, 1 | Explicit independent matrix construction and admission checks. | Match |
| Determinants 209/100, 209/50, 149281/62500 | Dense exact determinants and positive-mass Schur complements in Q(i). | Match |
| Determinants -1, 1 and 0 in the boundary witnesses | Exact single-flavor, doubled-flavor and zero-mass determinants. | Match |
| Real-fugacity determinant 2457/4096 + (315/256)i | Direct exact determinant at z = 2, distinct from the imaginary-fugacity class. | Match |
| Center root has cube one and orbit sum 345/32 | Exact calculation in Q(zeta_12), including the Laurent-polynomial coefficient identity. | Match |
| 16 axiom reports | Replay parser matches every final `#print axioms` line to its permitted-axiom output. | Match |

The 2 pi/3 physical period is retained only as an explicitly imported symbolic
literature statement, not as a locally computed constant or theorem.
Version numbers, dates, hashes and node identifiers are custody metadata.

## Scoring and acceptance

The finite proof and independent checker are honestly **L3D**. The declarative
registration is **L1D**. The human approved the exact source hashes recorded in
`dag/research/campaign_fsp-imaginary-mu-real-det_exact_source_exception.json`.
The proof baseline exception and existing registration support pin are exact-byte
exceptions; the global L4/D floor is unchanged. Existing Functor/FullFunctor
exceptions are untouched. A passing acceptance check does not raise these scores.

## What the scanner cannot decide

The scanner cannot establish the source-regime refinement, identify staggered site
parity with a reconstructed spin gamma5, certify the QCD measure theorem, prove
analytic continuation, or replace an independent human mathematical review.
The node therefore stays `IMPORTED_ASSUMPTION`, and the note stays AI-drafted.
