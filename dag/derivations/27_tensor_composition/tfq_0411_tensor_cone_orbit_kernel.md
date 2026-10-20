# [TFQ-0411] Positive cone selection by preparations and transported tests

**Stage:** `TENSOR_COMPOSITION` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0410](tfq_0410_tensor_tomographic_coordinates.md)
**DAG node:** `TENSOR-CONE-ORBIT-KERNEL`
**Required DAG inputs:** `TENSOR-TOMOGRAPHIC-COORDINATES`

## Theorem

Let K be a set of Hermitian matrices of any finite size over C, containing zero
and closed under addition. Suppose a family of seed vectors S and operations
have these properties:

1. Every ss* for s in S belongs to K, and every X in K satisfies s*Xs >= 0.
2. Forward and backward operations preserve K.
3. Forward operations transport ss* to (g s)(g s)*; backward operations obey
   s* backward_g(X) s = (g s)* X (g s).
4. Every vector v is g s for some operation and seed s in S.

Then K is exactly the positive-semidefinite cone. Seeds may be unnormalized;
their scale accounts for unnormalized preparations. The zero vector is allowed.
The hypotheses concern actual matrices and quadratic forms, not status flags.

## Proof

For any X in K and vector v, write v=g s. Backward preservation and seed
positivity give v*Xv=s* backward_g(X) s>=0. Since X is Hermitian, X is PSD.
Conversely, forward preservation makes every vv* preparable. Every positive
matrix has a Gram factorization B*B and equals the finite sum of outer products
of the conjugated rows of B. Closure under addition puts every such matrix in K.
Both inclusions give equality. No topological limit or density assertion is used.

## Lean statement boundary

[TensorConeReconstruction.lean](../../../lean4/TensorConeReconstruction.lean)
contains `positive_mem_of_rankOne`, `cone_eq_positive`, and
`operational_orbit_selects_positive`. The finite index type is arbitrary.
`OrbitData` exposes seed preparation, positivity, preservation, transport, and
reachability as hypotheses. The Gram factorization uses the pinned Mathlib
finite complex matrix order theory. Its foundations include classical choice;
it is not an integer-only construction of complex spectral theory.

The original module checks the general cone kernel. The subsequent
[TensorOperationalCone](../../../lean4/TensorOperationalCone.lean) instantiates
its seed preparation, transport and reachability fields using the proved
[Schmidt construction](../../../lean4/TensorSchmidt.lean) and
[controlled-shift reachability](../../../lean4/TensorReachability.lean).
[TensorComposition](../../../lean4/TensorComposition.lean) connects that result
to the constructed tomographic equivalence. Operational preservation of the
calibrated local and shift conjugations is still explicit; full global-unitary
availability is not assumed. The
[formalization receipt](../../research/tensor_formalization_validation.json)
records the scoped replay. A full-project `lake build` is a separate check.

The operational instantiation follows in
[TFQ-0412](tfq_0412_tensor_controlled_shift_reconstruction.md).
