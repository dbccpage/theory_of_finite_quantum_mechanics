# [TFQ-0407] Meron character cancellation on a supplied flip orbit

**Stage:** `FERMION_SIGN` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0406](../26_fsp/tfq_0406_fsp_switching_normal_form.md)
**DAG node:** `FSP-MERON-CHARACTER-CANCELLATION`
**Required DAG inputs:** `FSP-SWITCHING-NORMAL-FORM`

## Statement and derivation

For flags m∈{0,1}^k the raw orbit character is χ_m(x)=(-1)^{∑m_i x_i}.
Its sum over x∈{0,1}^k factors as ∏_i(1+(-1)^{m_i}). It is zero if any flag
is one, otherwise 2^k. `MeronCharacter.orbitSigns` enumerates this character,
and its sign sum and compression identity are mechanized for arbitrary lists.

To multiply this identity by a common nonnegative weight w, every orbit member
must have the same absolute weight. For an observable, its insertion must also
respect the required orbit averaging. Neither property follows from graph sign
switching alone. Unequal orbit magnitudes or a sign-sensitive observable can
invalidate an attempted physical reduction despite the raw character identity.
The existing exact meron model is a finite example with explicit reconstruction.

## Evidence and next obligation

- [papers/core/fsp/README.md](../../../papers/core/fsp/README.md)
- [lean4/MeronCharacter.lean::meron_orbit_cancels](../../../lean4/MeronCharacter.lean)
- [lean4/MeronCharacter.lean::zero_meron_orbit_positive](../../../lean4/MeronCharacter.lean)
- [lean4/MeronCharacter.lean::compression_preserves_partition](../../../lean4/MeronCharacter.lean)

Supply invariant weight magnitudes, valid flip action and compatible observables before using the sign identity as a model reduction.
