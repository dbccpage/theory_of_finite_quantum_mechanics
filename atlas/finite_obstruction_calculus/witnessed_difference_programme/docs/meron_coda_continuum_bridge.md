# Meron, CODA-CS/Q and the continuum interface

The later [actual time/volume derivation](meron_time_and_volume_refinement.md)
supplies a proved common thermodynamic log-density target for the declared
full-Fock U=t chain. It restores the removed scalar and uses fixed-temperature
rational refinements with explicit errors. The historical source review below
retains its own checkpoint; its Neville receipt is not promoted by that new
method. The new analytic proof is written, with separate finite native/source
execution and resource scopes.

AuthorityEffect: None. Reviewed 2026-10-02 against merged
revision `3bec3e2dd5659b53c33889d967fcd2b09689043c` from
PR #401.
The written results are in [Appendix M](../witnessed_difference_programme.md#appendix-m-meron-characters-coda-shadows-and-conditional-limits).
The [separate bridge register](genesis_bridge_register.md) records their
scope. The five enlarged Genesis obligations remain open.

## Source and actual verification

The primary source is
`omega_engine_projects/finite_to_continuum`.
Its project tests and demo regression were freshly replayed after the sync:

```powershell
py -3.12 -m pytest -q omega_engine_projects/finite_to_continuum/tests omega_engine_projects/finite_to_continuum/demos/tests
```

All 47 selected checks passed. This verifies the stated test cases, rather
than all physical statements printed by the package. The reviewed project
has no Lean corpus. Existing WDP Lean and native receipts remain separate
earlier evidence and were not recompiled for this manuscript-only update.

An independent call of the original
`meron_transfer_trace`
recomputed 912, 33012 and 973824 at L=4,6,8, repetitions=2, q=3. This bypasses
the bridge's cached canonical values. All 28 tracked project files and the
FSP transfer source were bound to the merged revision and their raw hashes
were checked before and after the calls. Those hashes establish custody;
the original occupation-basis multiplication establishes these finite
values at its declared arithmetic scope.

The transfer trace sums every diagonal in the 2^L occupation basis. It
does not project onto the fixed N=L/2 particle sector. The declared chemical
potential and any half-filling interpretation must retain that distinction.
The time depth is fixed at four checkerboard steps. Neither a time-mesh
limit nor a higher-dimensional lattice model follows from these three calls.

## Component meanings

| Component at the reviewed revision | What is implemented | Additional evidence needed |
| --- | --- | --- |
| `interval_calculus.py` | Rational endpoints, interval operations and specific series/iteration bounds for declared functions | General domains, resource/termination guarantees and physical input calibration remain separate. Float display fields do not serve as exact endpoints. |
| `discretization_defect.py`, `coda_2d_discretization_defect.py` | Expansion by supplied C a^p bounds, interval overlap and a reported contraction flag; quadrature/cubature fixtures | A proof of the supplied constants for the actual function or physical model. Overlap alone does not establish a common continuum value. |
| `wilsonian_extrapolator.py` | Exact interval Neville interpolation at x=0 from x=L^-p samples | A model-derived scaling law and a remainder bound that controls the difference between the interpolation and the actual limit. |
| `meron_wilsonian_bridge.py` | Cached finite traces, log-density enclosures and the three-size interpolation | Independently bind the selected Hamiltonian/ensemble, observables, scaling error, limit existence and time discretization. |
| `pontryagin_duality.py`, `coda_2d_pontryagin.py` | Staged finite data, unbounded-group declaration, literature import, normalization and host evaluation | Actual refinement maps/topologies; proof or imported continuous-character theorem at its correct carrier. |
| `symbol_game_coda_meron_ladder.py` | Five candidate specifications, wire/hygiene checks and mixed-scope example receipts | Actual dimensional models, configurations, invariants, sign involutions and analytical limits. |

The Fourier methods named `character_matrix_exact_orthogonality` and
`character_tensor_exact_orthogonality` assign the expected Kronecker-delta
values and test those assigned values. They do not construct and independently
sum character matrices. Appendix M.2 supplies a written geometric-series
proof under explicit root-of-unity hypotheses. This separates mathematical
soundness of that criterion from the scope of the status-returning functions.

The staged programme's `MODELLING_DECLARATION`, `LITERATURE_IMPORT`,
`NORMALIZATION` and `HOST_FLOAT` labels retain their source meanings. Its
`REFUSED` spine fields are declarative status metadata. The named guard
functions and their tested refusal cases establish their own code behavior;
a printed refusal field does not verify every caller or every numerical
domain. The special sinc(pi/6) host calculation also needs its declared
sector; its source accepts a sector parameter while using the fixed 3/pi
formula.

## The Meron/CODA preservation bridge

An orientation orbit (Z/2Z)^k carries a finite character. Equal-weight
opposite-sign pairing cancels the signed partition contribution. For an
observable O, cancellation of its numerator instead requires the vanishing
of its Fourier coefficient at that character. The explicit two-orientation
countermodel in Appendix M.1 has partition sum zero and numerator two.

Apply the CODA-CS-Q image-factor criterion to the actual compression report
and each protected query. If two admitted source packets have the same
report and different query values, no decoder from that report recovers the
query. Appending the missing coefficient, or a separately verified improved
estimator, supplies an explicit candidate completion. Its preservation must
be checked against the source model. Partition equality does not imply
history, cost, observable or future-transition equality.

The existing source
[CODA-CS-Q paper](source_archive/coda_component_packages/cs_q/coda_cs_q_bridge.md)
proves factorization on the actual profile image, and
[CODA-CS](source_archive/coda_component_packages/cs/coda_cs.md)
distinguishes refinement from a limit claim. These interfaces fit the WDP
report/descent criterion without selecting its physical carrier or an
institutional authority rule.

## Extrapolation precision and model error

Fresh calls of the original Neville implementation on the three unit
input vectors return the exact weights 4/15, -81/35 and 64/21. Original
Meron bridge calls give an interpolation near 1.6941183355 with width below
10^-19. The receipt propagates the logarithm intervals; it has no scaling
remainder input or independent limit certificate.

The polynomial H(x)=(x-1/16)(x-1/36)(x-1/64) vanishes at all sample nodes
and has H(0)=-1/36864. The source returns [0,0] on three zero samples,
which is an exact interpolation result for both zero and H at those nodes.
It is not a limit enclosure for H. This is a written non-identifiability
proof with an original-function observation, not a new replacement solver.

Appendix M.4 gives the conditional remedy: if the actual model satisfies
g(L_i)=f+c1/L_i^2+c2/L_i^4+r_i with proved |r_i| <= b_i, expand the
interpolated interval by B=sum |w_i| b_i. Gapped/conformal terminology or an
asymptotic expansion without a quantitative remainder does not supply b_i.
The positive quantity ln(Z)/L is called log-partition density here; free
energy requires its temperature and sign conventions.

## Higher-dimensional candidate audit

The following classifications come from the actual `compute_t*` functions,
rather than their receipt labels.

| Target | Current source behavior | Outstanding proof or correction |
| --- | --- | --- |
| T1, 2D Meron torus | Assigns Z=912 and sites=16, together with fixed winding counts | Construct the actual 16-site 2D ensemble and verify its orbit sums/observables. The 1D trace is not that calculation. |
| T2, deficit angle | Calculates an interval for the declared pi/3 toy deficit | Derive metric/nondegeneracy and error claims from actual geometry. The displayed unit-triangle Cayley-Menger matrix has determinant -3; the receipt assigns +3. |
| T3, 3D strings | Records winding/linking descriptions, a supplied residual bound and `odd_winding_cancellation=True` | Supply configurations, compute their invariants and prove a weight-preserving sign-changing action. |
| T4, 4D simplices | Assigns simplicity and Bianchi defects zero; encloses a declared pi/6 angle | Compute bivectors, frame transports, action and the analytical defect from actual simplicial data. |
| T5, field-theoretic Meron | Assigns Q=1/2, opposite charge and opposite sign | Its formula (-1)^(2Q) gives -1 for both charges +1/2 and -1/2. Prove a distinct physical sign mechanism or correct the candidate rule. |

Cluster Merons in a finite fermion ensemble and field-theoretic Meron
configurations require an explicit bridge. A shared name, assigned charge
or Gamma38 serialization cannot supply a determinant identity. A completed
field-theory route requires compatible carrier refinements, fields/action,
uniform model-error bounds and preserved observables/dynamics in the chosen
limit. Appendix M records this productive frontier at its present scope.

## Manuscript and release custody

The later PR 407 source is audited separately in
[the dyadic refinement supplement](dyadic_refinement_and_duality.md),
pinned at 4061122d1d4f8cf679bbd28c3bf2ef7a74bd9b7a. It supplies actual
doubling inclusions and interval character sums. Its Lean source file is
not credited as elaborated by this audit; the newly compiled core WDP
module has its own stated residue scope. Written dual/completion results
depend on the explicitly chosen topology. Original-function replay also
retains the enclosure flag's no-common-target counterexample. These newer
findings do not change the historical PR 401 classifications above.

This is a source update to the v0.5.0 research manuscript and its bridge
documentation. The earlier republication PDF, archive and historical Lean
receipts keep their earlier identities. The regenerated live package
checksums bind current sources; they do not assert a new deposit, a freshly
built PDF or completion of the enlarged programme.
