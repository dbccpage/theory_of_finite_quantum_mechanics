# [TFQ-0402] Exact projector contract for mutually unbiased bases

**Stage:** `MUTUALLY_UNBIASED_BASES` | **Status:** `DEFINITION` | **AuthorityEffect:** None.

**Parent:** [TFQ-0315](../09_finite_hilbert/tfq_0315_exact_density_ray_and_population_shadow.md)
**DAG node:** `MUB-EXACT-PROJECTORS`
**Required DAG inputs:** `GP-FIN-GAUSS-MATRIX-ALGEBRA`, `GP-IMPORT-COMPLEX-FIELD`

## Statement and derivation

For d>1 fix a supplied d-dimensional complex Hilbert carrier. A basis b is
represented by d Hermitian rank-one projectors P_{b,j} satisfying
P_{b,j}P_{b,k}=0 for j≠k and ∑_j P_{b,j}=I. Distinct bases are mutually unbiased
when tr(P_{b,j}P_{c,k})=1/d for every j,k. Projectors avoid arbitrary vector phases.

An exact witness must declare its coefficient field, adjoint and equality test.
Gaussian rationals do not contain every needed root of unity or normalization.
Adjoining a cyclotomic or algebraic extension is an explicit additional carrier
choice, not something implied by the Gaussian-integer matrix recovery node.

This branch attaches to finite-Hilbert TFQ-0315 and the existing MUB custody
entries TFQ-0176–0180. It adds mathematical targets without replacing their
evidence boundaries.

## Evidence and next obligation

- [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)

Check the scalar field, adjoint, rank, resolutions and all cross-basis trace equalities before accepting a MUB witness.
