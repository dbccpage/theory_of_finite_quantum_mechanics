# [TFQ-0410] Composite coordinates from local operational statistics

**Stage:** `TENSOR_COMPOSITION` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0127](../21_implementation_core/tfq_0127_hilbert_carriers_and_tensor_index.md)
**DAG node:** `TENSOR-TOMOGRAPHIC-COORDINATES`
**Required DAG inputs:** `FQ-DECLARED-QUANTUM-INTERFACE`, `FQ-GAP-TENSOR-UNIQUENESS`

## Hypotheses

Fix positive integers n and m. Local systems are finite-dimensional complex
quantum systems: their real ordered vector spaces are Herm(n) and Herm(m),
positive cones are PSD, deterministic effects are trace, and local probabilities
are trace pairings. Complex scalars and this local state/effect rule are imports.

The composite is initially an unspecified finite-dimensional real vector space V
spanned by its unnormalized physical states K. Mixing and scaling are respected.
There are independently preparable product states and independently performable
product effects, bilinear on the local spaces. They satisfy the factorization
rule (e product f)(a product b) = e(a) f(b). The deterministic composite effect
is the product of local deterministic effects. Product effects separate V
(local tomography). Probabilities are nonnegative. No composite positive cone,
Hilbert inner product, or global unitary group is specified.

## Theorem and proof

There is a unique real linear identification J: V -> Herm(nm) satisfying

    (E product F)(x) = Tr[(E tensor F) J(x)]

for every local Hermitian E,F. It sends independent preparations A product B to
the ordinary Kronecker matrix A tensor B. Its image is all of Herm(nm), and the
deterministic effect becomes Tr. This identifies coordinates, not positivity.

For dimension d, take the following d^2 normalized rank-one projectors:

    P_i = |i><i|,
    P^+_ij = (|i>+|j>)(<i|+<j|)/2,
    P^i_ij = (|i>+i|j>)(<i|-i<j|)/2,       i<j.

The first family spans the diagonal matrices. Subtracting the diagonal terms
from the other two families gives the real symmetric and imaginary
antisymmetric off-diagonal matrix units. Thus they are a real basis of Herm(d).
They are both legal states and legal effects. The trace pairing is nondegenerate:
Tr(H^2)>0 for a nonzero Hermitian H, by its real eigenvalues. Hence this basis has
a trace-dual basis, denoted D_a.

Let P_a and Q_b be the local projector bases. For x in V, define

    J(x) = sum_ab (P_a product Q_b)(x) D_a tensor D_b.

The trace factorization identity for Kronecker matrices gives the displayed
pairing rule on the basis, then on all E,F by linearity. Local tomography makes
J injective. Independent preparation and probability factorization give
J(A product B)=A tensor B. Products of the projector bases span Herm(nm): their
trace-duals are the products of the local dual bases, so the n^2 m^2 products
are independent, and dim_R Herm(nm)=(nm)^2. Thus J is also surjective. These same
pairing identities establish its uniqueness and identify the trace effect.

The lower and upper bounds on the transported cone are therefore

    SEP(n,m) subset J(K) subset BP(n,m),

where SEP is the conic hull of product positive matrices and BP consists of
Hermitian X with <a tensor b|X|a tensor b> >= 0 for all local vectors a,b.
The first inclusion uses preparation and mixing; the second uses product tests.
Neither inclusion is generally equality with PSD(nm).

## Custody and next step

This is a proof for every finite n,m over C, with exact finite-dimensional
linear algebra. The finite number of coordinates does not derive C, real
square roots, local Born probabilities, or the local quantum state spaces from
primitive difference. The dimension argument relies on operational separation,
not an assumed joint carrier.

The [exact witness code](../../../code/python/src/qm/tensor_composition.py) checks
the projector bases and their products on retained small dimensions. It is not
the all-dimension proof. Continue with the
[cone-selection kernel](tfq_0411_tensor_cone_orbit_kernel.md) and
[controlled-shift theorem](tfq_0412_tensor_controlled_shift_reconstruction.md).

## Verified Lean boundary

[TensorTomography](../../../lean4/TensorTomography.lean) proves the real span of
Hermitian products using matrix units and real/imaginary Hermitian parts, and
proves nondegeneracy of the trace pairing. Thus the formal proof does not assume
the dimension of a joint carrier.
[TensorCoordinates](../../../lean4/TensorCoordinates.lean) constructs
`tomographicEquiv` from `TomographicData`: bilinear preparation, bilinear tests,
product factorization, and local tomography. Its finite dual-frame sum is proved
injective and surjective; `tomographicEquiv_prepare`, `tomographicEquiv_test`,
and `tomographicEquiv_unique` prove product preservation, preservation of every
product probability, and uniqueness. These statements cover arbitrary finite
local index types and an arbitrary real operational vector space.

The formal frame uses arbitrary local Hermitian bases and their trace duals.
It is equivalent to the displayed dual-projector formula; the explicit positive
projector-basis construction and the SEP/BP corollaries above remain prose.
`product_calibration` proves that agreement on all Hermitian products fixes a
real linear process. `finite_frame_calibration` checks that the finite table
on a product preparation frame and its dual test frame fixes the process.
The operational passage from physical positive tests to
their bilinear extension is a premise, not a derived physical law.
[TensorComposition](../../../lean4/TensorComposition.lean) chooses finite bases,
connects this representation to the cone theorem, and checks `unit_test_is_trace`.
See the [formalization receipt](../../research/tensor_formalization_validation.json).
