# [TFQ-0412] Quantum composition from a calibrated reversible controlled shift

**Stage:** `TENSOR_COMPOSITION` | **Status:** `PROVED_PROSE` | **AuthorityEffect:** None.

**Parent:** [TFQ-0411](tfq_0411_tensor_cone_orbit_kernel.md)
**DAG node:** `TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION`
**Required DAG inputs:** `TENSOR-TOMOGRAPHIC-COORDINATES`, `TENSOR-CONE-ORBIT-KERNEL`

## Operational assumptions

This is a sufficient-assumption theorem for every pair of positive finite
dimensions. No minimality or derivation of the assumptions from primitive
difference is asserted.

- **L: Local quantum systems.** Herm(n), Herm(m), their full local states,
  effects, trace probabilities and local unitary transformations are available.
- **P: Independent composition and mixing.** Products of local preparations and
  effects are available with factorized probabilities. The unnormalized state
  set is a cone closed under finite sums. Transformations respect mixing,
  deterministic effects, and sequential composition. Tests give nonnegative
  probabilities. Products of deterministic effects give the composite unit.
- **T: Local tomography.** Product effects separate the real span of states.
- **C: One coherent reversible interaction with a complete calibration.**
  Relabel the smaller subsystem as the control, n<=m. There is an available
  reversible transformation whose product-preparation/product-test probability
  table equals that of

      C|a,b> = |a,(b+a) mod m>,       0<=a<n, 0<=b<m.

  Require agreement for every input and test from the n^2 m^2 product projector
  basis in TFQ-0410. Thus a finite table of n^4 m^4 exact probabilities specifies
  this map. Both the gate and its inverse are physical. This is a calibration
  assumption about coherent experiments, stronger than a classical truth table.
  These are ideal exact equalities; a finite experimental sample does not certify
  them without a separate error analysis and robustness theorem.
- **E, for the full effect-interval conclusion only:** every linear functional
  between zero and the deterministic effect on all normalized states is an
  available binary effect. This is the no-restriction assumption for effects.
  Availability of an arbitrary POVM additionally requires that every finite
  collection of these effects summing to the unit is an available test.

For n=1 the shift is the identity and the conclusion reduces to the local theory.
If the original first subsystem is larger, exchange the two labels before
defining the gate; the final identification respects the corresponding swap.

## Theorem

Under L,P,T,C the composite ordered state space, with its distinguished product
maps and normalization, is uniquely isomorphic to

    (Herm(nm), PSD(nm), Tr),       (A,B) |-> A tensor B.

Its positive effect cone is also PSD(nm). Under E its available binary effects
are exactly 0<=E<=I. With the additional finite-test clause in E its measurements
are exactly the quantum POVMs. This is state/effect composition uniqueness;
availability or exclusion of all channel types is not part of this theorem.

## Proof: coordinates and the gate

TFQ-0410 constructs the unique linear identification J from product statistics
and shows SEP subset J(K) subset BP. No positive cone on Herm(nm) is assumed.
For each fixed control a, addition by a modulo m permutes the target labels;
therefore C is a permutation unitary with inverse C*.
Let F be the transported physical gate. Both F and X |-> CXC* are real linear.
Their output pairings agree with every product test on a basis of product
preparations by C. Product tests separate Herm(nm), so they agree on the input
basis, hence on every X. Therefore F(X)=CXC*. Reversibility gives the inverse
map X |-> C*XC, and the composite state cone is preserved in both directions.
Local transformations likewise act by conjugation with U tensor V: this follows
from independent local action and the same spanning argument.

## Proof: all rank-one directions are reachable

For any unit vector psi in C^n tensor C^m, finite-dimensional singular value
decomposition of its coefficient matrix gives its Schmidt form

    psi = sum_(i=0)^(r-1) s_i u_i tensor v_i,
    s_i >= 0, sum_i s_i^2 = 1, r <= n <= m.

For completeness, diagonalize the positive matrix of coefficients times its
adjoint. For every positive eigenvalue s_i^2, apply the adjoint coefficient map
to its unit eigenvector and divide by s_i; these vectors are orthonormal.
Conjugate the right vectors when passing from the matrix factorization to tensor
coefficients. Zero eigenspaces contribute no summand. Complete both orthonormal
families to local bases. This yields local unitaries U,V with U|i>=u_i and
V|i>=v_i and the displayed decomposition. This finite complex spectral step is
an admitted mathematical toolkit, not a selection of local C from primitives.

Prepare the local state with vector alpha=sum_i s_i |i> and the target |0>.
The controlled shift sends alpha tensor |0> to sum_i s_i |i,i>. Apply U tensor V
to obtain psi. This is a single use of C followed by local operations, with a
locally prepared input. It is not an assumption that every global unitary is
available. Rescaling covers every unnormalized vector, including zero.

## Proof: both cone inclusions

Write R=(U tensor V) C. Each psi above has the form R(alpha tensor |0>).
The physical preparation and transformation give |psi><psi| in J(K).
Mixing and scaling then give PSD(nm) subset J(K), using a spectral decomposition
of a positive matrix into finitely many nonnegative rank-one summands.

Conversely take X in J(K). R*XR belongs to J(K) by reversibility. The product
test |alpha><alpha| tensor |0><0| gives a nonnegative probability on it. Hence

    <psi|X|psi> = <alpha,0|R*XR|alpha,0> >= 0.

Every unit vector psi is covered. Hermiticity and this quadratic-form criterion
give X>=0. This establishes J(K)=PSD(nm) and instantiates the general cone
argument in TFQ-0411. Normalized states are exactly positive trace-one matrices.
No-signalling follows for product tests by summing a complete remote test to I.

Pulling back the product test through R* makes every rank-one projector an
available binary effect. Their conic hull is PSD. Every allowed effect has a
nonnegative pairing with every positive state, so its representing Hermitian
matrix is PSD; its complement is also PSD. The generated effect cone is exactly
PSD, while effect saturation E supplies the entire interval [0,I] and its
separate finite-test clause supplies all POVMs.

Finally, any two operational composites satisfying the hypotheses have the
same unique map J fixed by product statistics. Composing these maps gives the
normalization- and product-preserving order isomorphism between the composites.
This is uniqueness up to that operational isomorphism, not a preferred naming
of Hilbert basis vectors.

## Scope and validation

This result replaces a supplied composite host by derived tomographic
coordinates and replaces assumed covariance under all global unitaries by one
fully calibrated reversible interaction and available local operations. The
coherent gate remains a substantive, explicit physical assumption. Removing it
allows the countermodels in [TFQ-0413](tfq_0413_tensor_assumption_countermodels.md).

The all-dimension proof is prose. The cone kernel is checked in
[Lean](../../../lean4/TensorConeReconstruction.lean). The
[exact Python witnesses](../../../code/python/src/qm/tensor_composition.py) and
[tests](../../../code/python/tests/test_tensor_composition.py) verify finite
projector bases, rectangular-dimension shift gates, coherent preparation,
min/max separation, and two calibration mutations. They do not compute a
general SVD or replace the proof. Local complex QM, L,P,T,C,E, and their origin
from the primitive theory remain visible imports; the primitive-to-QM gap is
not relabelled as closed.
