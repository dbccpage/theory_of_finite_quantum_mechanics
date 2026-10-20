# [TFQ-0414] Generated operational effect cone

**Stage:** `TENSOR_COMPOSITION` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0412](tfq_0412_tensor_controlled_shift_reconstruction.md)
**DAG node:** `TENSOR-GENERATED-EFFECT-CONE`

Let J be the constructed tomography equivalence and let K be the operational
state cone. Use the conclusion J(K)=PSD of `quantum_state_cone`, rather than
postulating joint quantum coordinates or a state cone. A linear effect f has a
unique Hermitian representative E defined by f(x)=Re Tr(E J(x)). The deterministic
effect represents I, and an independent product test represents the Kronecker
product of its local effects.

Assume available effects are sound: 0<=f(x)<=u(x) for x in K. Assume every product
of local binary effects is available, and the available effects are closed under
calibrated conjugations by local unitaries and the controlled shift C. The latter
is the effect pullback along the inverse physical state transformation. These
availability and calibration hypotheses are explicit in `operational_effect_cone`.

Then the nonnegative real conic hull of the represented available effects is
exactly PSD. Neither `EffectSaturated` nor `FiniteTestSaturated` is used.

## Checked proof

1. Finite Gram decomposition gives nonnegative trace pairing of two PSD matrices.
   Rank-one vector tests give the converse: PSD is self-dual under the trace pairing.
   Soundness on J(K)=PSD therefore places each available effect inside PSD.
2. For every PSD matrix A, set r=||A||+1 and E=A/r. The matrix C*-order norm
   inequality gives 0<=E<=I, so A is a nonnegative multiple of a binary effect.
   Apply this independently to two local rank-one matrices. Local binary-product
   availability therefore puts every product rank-one ray in the generated cone.
3. Conjugation distributes over sums and nonnegative real scaling, so availability
   closure extends to the entire conic hull. The already verified Schmidt theorem
   reaches every joint vector with one controlled shift and local unitaries.
   Rank-one transport puts every joint rank-one matrix in the generated cone.
4. Finite Gram decomposition supplies every PSD matrix. Conversely PSD is closed
   under nonnegative scaling and addition, so the generated cone contains nothing else.

The hull includes zero, uses finite sums, and requires no topological closure.
The theorem holds for every finite n<=m with m nonzero, including zero vectors
and rectangular local dimensions. Positive-dimensional systems can be relabelled
so the smaller subsystem controls the gate.

## Proof custody and limits

- [TensorEffectOrder](../../../lean4/TensorEffectOrder.lean): `positive_iff_pairing`, `positive_ray_binary`.
- [TensorEffectCone](../../../lean4/TensorEffectCone.lean): `effect_cone_eq_positive`.
- [TensorMeasurements](../../../lean4/TensorMeasurements.lean): the dual representation,
  product-test identification and `operational_effect_cone`.
- [Validation receipt](../../research/tensor_measurement_validation.json).

Equality of conic hulls does not assert that every matrix in [0,I] is itself
available. That separate claim is [TFQ-0415](tfq_0415_tensor_binary_effect_interval.md).
No primitive derivation of local quantum systems or physical calibration is asserted.
