# [TFQ-0415] Binary effects and explicit effect saturation

**Stage:** `TENSOR_COMPOSITION` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0412](tfq_0412_tensor_controlled_shift_reconstruction.md)
**DAG node:** `TENSOR-BINARY-EFFECT-INTERVAL`

For the state cone K reconstructed by `quantum_state_cone`, define a valid linear
effect by 0<=f(x)<=u(x) for every unnormalized x in K. The deterministic effect is
the product unit test and represents matrix trace. The dual tomography equivalence
`effectRepresentation` is constructed from J and the nondegenerate trace pairing;
no separate effect-coordinate representation is assumed.

## Checked theorem

An effect f is valid if and only if its Hermitian representative E satisfies
E>=0 and I-E>=0, equivalently 0<=E<=I. Trace self-duality proves each positivity
condition. `binary_iff_normalized` also checks that these homogeneous bounds are
equivalent to probabilities in [0,1] on every trace-one PSD state. Its proof handles
zero separately and rescales each nonzero PSD state by its strictly positive trace.

Let Available be an arbitrary set of operational linear effects. Supply two
distinct premises:

- Soundness: every available effect satisfies the bounds on K.
- `EffectSaturated D K Available`: every linear functional satisfying those bounds
  is an available binary effect.

Then `available_effects_eq_interval` identifies the represented available set
with the entire interval [0,I]. The reverse inclusion uses `EffectSaturated`
explicitly. Soundness alone gives only containment. This saturation is the
no-restriction assumption for individual effects; it is not inferred from state
reconstruction or from equality of the generated effect cone with PSD.

## Proof custody and limits

- [TensorEffectOrder](../../../lean4/TensorEffectOrder.lean): `binary_iff_bounds`,
  `binary_iff_interval`, `binary_iff_normalized`.
- [TensorMeasurements](../../../lean4/TensorMeasurements.lean): `effectRepresentation`,
  `effectRepresentation_unit`, `effectRepresentation_product`, `validEffect_iff_binary`,
  `available_effects_eq_interval`.
- [Validation receipt](../../research/tensor_measurement_validation.json).

The proof accepts exactly the image-cone conclusion of `quantum_state_cone`.
The end-to-end `quantum_measurements` theorem calls that state-cone theorem with
all original operational premises explicit. Individual effect availability does
not establish joint test availability; see [TFQ-0416](tfq_0416_tensor_finite_povm_availability.md).
