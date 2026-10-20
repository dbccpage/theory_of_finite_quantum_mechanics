# [TFQ-0416] Finite POVMs and separate test saturation

**Stage:** `TENSOR_COMPOSITION` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0415](tfq_0415_tensor_binary_effect_interval.md)
**DAG node:** `TENSOR-FINITE-POVM-AVAILABILITY`

Fix any finite outcome type. A matrix POVM is a family of PSD Hermitian matrices
whose sum is I. An operational test is a family of linear effects. In addition to
the reconstructed state cone and sound effects, supply:

- Test soundness: every available test has individually available outcomes and
  their sum is the deterministic effect.
- `EffectSaturated`: every cone-bounded linear effect is individually available.
- `FiniteTestSaturated`: every finite family of individually available effects
  summing to the deterministic effect is jointly available as a test.

The final two premises are independent operational requirements in the formal
statement. Neither is hidden in the definition of a POVM or derived from the
state-cone theorem.

## Checked proof

`test_iff_povm` identifies available tests with all matrix POVMs under the supplied
premises. Forward: effect soundness gives positive representatives, and linearity
of the dual representation sends the sum of outcomes to I. Reverse: positivity
of all POVM entries and their identity sum imply each entry lies in [0,I]. Indeed
on a positive state each term has a nonnegative trace pairing, and each individual
term is bounded above by their sum, which is the state's trace. Effect saturation
then makes every outcome available; finite-test saturation makes the family
jointly available. No assumption that individually available effects are always
jointly measurable is used without the stated unit-sum condition.

`quantum_measurements` first calls `quantum_state_cone` and then returns all three
conclusions: generated effect cone = PSD, available binary interval = [0,I], and
available finite tests = POVMs. The separately callable `operational_effect_cone`
has no saturation hypothesis, while `available_effects_eq_interval` needs only
effect saturation. The separate `test_povm_of_sound` theorem requires soundness only.

## Proof custody and limits

- [TensorMeasurements](../../../lean4/TensorMeasurements.lean): `povm_binary`,
  `test_povm_of_sound`, `test_iff_povm`, `quantum_measurements`.
- [State-cone theorem](../../../lean4/TensorComposition.lean): `quantum_state_cone`.
- [Validation receipt](../../research/tensor_measurement_validation.json).

All finite outcome types are covered; infinite outcome spaces are outside the
statement. No instrument, post-measurement state, channel classification, or
primitive derivation of the operational assumptions is asserted. The primitive
composition gap remains conditional.
