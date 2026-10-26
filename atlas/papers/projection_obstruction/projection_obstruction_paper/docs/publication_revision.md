# PO-000 research revision, 2026-10-13

Manuscript/release 6.9.15; Python code 6.9.5. AuthorityEffect: None.

Written proofs of the Edge-Decomposed TDVP Duhamel Master Theorem (Theorem 5.10.A / §5.10.2)
and the Cut-Edge Pythagorean Cluster Rate Law (Theorem 5.10.B / §5.10.3), the Quantum Partial-Trace
Poset Cochain Adapter (Theorem 4.3.A / §4.3.2), and the Higher-Degree Graph-State Minimax Theorem
(Theorem 7.12 / §7.8) with root equation $r_d^{d+1}+r_d-1=0$. Factor-of-2 scaling repaired in §5.10.1,
jump operator support definition repaired in §5.4.1, formal references [32]--[35] populated,
and measurement setting symbol collision disambiguated.

**Scope correction from the publication audit:** the integration fixture uses
floating-point Krylov evolution on an eight-site hexagon-plus-square graph.
Sampled quadrature does not certify the analytic Duhamel bound, and the
theorems listed above are written proofs rather than general Lean results.
Earlier historical receipts remain bound to their original source bytes.

## Previous research revision, 2026-10-11

Manuscript/release 6.9.14; Python code 6.9.5. AuthorityEffect: None.

Proposition E.6 constructs the positive invariant trace form under explicit
real spectral and Jordan--Lie premises. Proposition E.7 quantifies the central
obstruction to purification, including the ancilla condition for attainment.
Countermodel fixtures now separate computed facts from imported classification:
real purification holds, quaternions are associative, and sector probabilities
can change under channels. Exact fixture inputs refuse floats and booleans.

The earlier external `po000_research_qualification_2026-10-11.json` receipt
adjacent to this package records focused Python checks, fresh replay and
certificate verification, the scoped three-module Lean build, rendered paper
inspection and deterministic archive custody. Only these named checks are
claimed. Historical receipts are unchanged; no full repository/package test
sweep, native measurement run, notebook recertification, whole historical Lean
build, or external deposit is asserted. Partial integrity is not a full
standalone-profile pass.

The post-merge review on 2026-10-11 found ten stale checksum entries while
those source files still matched the reviewed research branch. The current
manifest/archive are rebuilt from the actual tree; the earlier receipt remains
bound to its earlier snapshot and is not rewritten as evidence for these bytes.
The review record is retained separately in the repository's internal review
records. E.6/E.7 and their stated proof scope are unchanged.

The following section retains the preceding revision's execution scope.

## Previous publication revision, 2026-10-10

Manuscript/release 6.9.13; Python code 6.9.4. AuthorityEffect: None.

The two supplied reviews assessed commit
`79fd9db728055deb001b7618e321f86e9ed4f97c`. This repair starts from remote main
`df84a59644c2a6837756273ccedd7b1233525407` and keeps PR #673's benchmark work
separate. Reviewer execution counts are not receipts for this revision.

The §5.16 future-observer criterion now quantifies uniformly over the full
lifted linear carrier. For an admitted subset Z it uses the difference-set
criterion; the ambient measurement count need not be minimal on Z. Existing
claim statuses remain unchanged; this is written mathematics, not a new Lean
mechanization.

Standalone verification deselects the native integration tests and records
native capability refusals. The native profile opts into the repository host
and fails on unavailable measurement coverage. The renamed Lean source scan
cannot establish elaboration or an axiom census. Release identity is explicit
and independent of the Python package's older code version.

## Execution scope

Focused Python checks, fresh replay/certificate verification, deterministic
archive rebuilding, exact extracted-archive integrity, and rendered PDF
inspection are recorded in the external release receipt adjacent to this
package. No full repository or complete package test run is requested or claimed.
No fresh Lean compilation, Rust build/native measurement run, or full notebook
execution is claimed. A partial integrity pass is not a full standalone profile
pass. Publication approval and Zenodo upload remain human actions.

The generated ZIP and its sidecar remain derived files in ignored `dist/`.
The external receipt binds their exact bytes without a self-referential hash.
Local XeLaTeX log, auxiliary and TOC outputs are retained alongside the PDF;
they keep the package's existing transient-output exclusion policy.
