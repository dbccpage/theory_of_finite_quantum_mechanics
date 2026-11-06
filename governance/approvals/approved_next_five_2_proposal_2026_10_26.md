# Five proposed exact-source support exceptions

These are five new derivations, separate from the earlier five already merged. They were selected from the refreshed DAG queue after excluding recorded attempts, nonmathematical records and targets reserved by open PRs.

All five PRs are drafts. No new proof exception has been authorized or applied. CONTRIBUTING.md line 19 requires a completed L4/D score, "except for explicitly authorized, exact-source support exceptions." The prior approvals cover 48 other exact hashes.

Approval would authorize only the five `finite_proof_example` path/digest pairs below. Their actual L2–L3/D scores, existing DAG statuses, original broad obligations, previous 48 pins and global L4/D floor remain unchanged. The campaign outcome is **Narrowed** for each target, not completion of its original broad physics claim.

| PR / node | Scoped result | Score | Regression tests passed |
|---|---|---|---:|
| [FSP-BF-2GROUP-SIGN-CLAIM](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/396) | a normalized Z2 cocycle with an unavoidable generator sign | L3D | 191 |
| [FSP-COBORDISM-INTRINSIC-SIGN](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/397) | classification of vertex-sign switching on a triangle | L2D | 191 |
| [PGW-IDENTITY-CONVENTION-UNDECIDABLE](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/398) | observational identity and incompatible novelty conventions | L2D | 193 |
| [FSP-REGGE-DEFICIT-ACTION](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/399) | finite deficit-action expansion and area dependence | L2D | 191 |
| [FSP-DISCRETE-WDW-CONSTRAINT](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/400) | an indefinite constraint and its distinct kernel projector | L2D | 191 |

Each proof builds in Lean 4.35.0, its explicit declarations pass the axiom audit, and its independent exact Python checker passes. All five modules also build and import together. No full repository Lean workspace build is claimed. Individually, every required local check passes except the policy floor for that one new proof source; the same governance check passes with its proposed exact pin temporarily applied and then restored.

The identity PR has one existing external-citation test skipped because the external repository is unavailable. Its changed record's local citations and declarations were separately verified against the published branch; three unchanged external citations were skipped.

### PR #396: FSP-BF-2GROUP-SIGN-CLAIM

- Path: `lean4/BfCocycleObstruction.lean`
- SHA-256: `882c2767c327fb2be146c2069898bea71eac43e6c1adf5b61c044475feb4eddc`
- Assessed score: **L3D**; retained node status: `OPEN`.
- Proposed category: `finite_proof_example`.
- Scope: For the additive group Z2 with trivial Z2 coefficient action, the Boolean 3-cochain omega(a,b,c)=a*b*c is normalized and satisfies the cocycle identity. Every normalized 2-cochain beta has coboundary zero at (1,1,1), whereas omega is one there. Thus omega is not a normalized coboundary, and normalized 2-cochain rephasing leaves a negative sign at that triple.
- Remaining boundary: The result concerns the explicitly defined Z2 cochain model and normalized rephasings. It constructs no BF state sum, 2-group gauge dynamics, knotted-worldsheet amplitude or three-loop braiding observable. No general cancellation or sign-free theorem follows.

### PR #397: FSP-COBORDISM-INTRINSIC-SIGN

- Path: `lean4/SignedTriangleSwitching.lean`
- SHA-256: `dee0cbf7bf415fd8202e0668f45757288dbf4bbce05aba16e8aaffd080ab57c1`
- Assessed score: **L2D**; retained node status: `OPEN`.
- Proposed category: `finite_proof_example`.
- Scope: For every assignment of Boolean edge signs to a triangle and every Boolean vertex switching, the XOR of the three edge signs is invariant. A switching makes all three edge signs positive exactly when their XOR is zero. An explicit switching gives the normal form (0,0,parity), and the product of integer edge signs equals the sign of that parity. A negative-parity triangle is obstructed within this switching class, whereas a balanced triangle with two negative edges can be made positive.
- Remaining boundary: Only diagonal vertex-sign switching on one three-cycle is classified. No spin bordism group, eta invariant, fermion representation, bulk cancellation or obstruction over all representations is computed. The original cobordism-based intrinsic-sign claim remains open.

### PR #398: PGW-IDENTITY-CONVENTION-UNDECIDABLE

- Path: `lean4/IdentityConvention.lean`
- SHA-256: `fa42557ad55d2b9150bea0a4c9d38a205d41e2d688115bb71091d0b96c6f8ff6`
- Assessed score: **L2D**; retained node status: `CONDITIONAL`.
- Proposed category: `finite_proof_example`.
- Scope: For arbitrary observer families, equality of all observations is an equivalence relation. Forgetting observers preserves indistinguishability, an empty observer family identifies every pair, and adjoining an exact-identity observer makes indistinguishability equivalent to equality. The supplied inscription `<a>` after `<>` is new relative to the exact observer and not new relative to the empty observer family. No single proposition agrees with both novelty answers.
- Remaining boundary: The observer family and interpretation of identity are declared. This is logical dependence on a convention, not a computability undecidability theorem, a preferred identity convention, or a replay of the historical model responses. It grants no operational or physical authority.

### PR #399: FSP-REGGE-DEFICIT-ACTION

- Path: `lean4/ReggeFiniteAction.lean`
- SHA-256: `dd1ccb8b8bc8e402055f561c46b161f41d2c3b007203e9716c5f067c4e131089`
- Assessed score: **L2D**; retained node status: `IMPORTED_ASSUMPTION`.
- Proposed category: `finite_proof_example`.
- Scope: For any commutative ring and finite hinge set, the action S=sum_h A_h*(tau-sum_j theta_hj) equals tau*sum_h A_h-sum_h A_h*sum_j theta_hj. For fixed deficits it is linear in the declared areas, and splitting an area while keeping its deficit fixed preserves its contribution. Zero deficits imply zero action. Declared integer data also show that zero total action need not mean zero deficits, and changing areas can change the action on the same finite index set.
- Remaining boundary: Areas, angles and the full-turn parameter are declared algebraic data. Geometric realizability, actual triangulation moves, Lorentzian signature, convergence to the Einstein-Hilbert action, and fermion-sign consequences are not established.

### PR #400: FSP-DISCRETE-WDW-CONSTRAINT

- Path: `lean4/ConstraintKernelProjector.lean`
- SHA-256: `4a01928ee24ba7b0f5432ede8b95a1c974f09ba942a596f849a6df520946b0d6`
- Assessed score: **L2D**; retained node status: `OPEN`.
- Proposed category: `finite_proof_example`.
- Scope: On integer triples, the declared constraint H(x,y,z)=(0,2y,-z) is symmetric for the usual dot product and has kernel exactly the vectors with y=z=0. The map P(x,y,z)=(x,0,0) is idempotent, maps into that kernel, fixes exactly the kernel, and has residual orthogonal to every kernel vector. H has a nonzero kernel but is indefinite and is not idempotent. Thus this finite-dimensional constraint and its kernel projector are distinct operators.
- Remaining boundary: This is a declared finite-dimensional integer model; its set of integer triples is infinite. It constructs no discrete Wheeler-DeWitt operator, triangulation dynamics, diffeomorphism action, physical state space or continuum limit. Its counterexample concerns an inference from symmetry and a nonzero kernel to positivity or idempotence, not a specified gravitational model.
