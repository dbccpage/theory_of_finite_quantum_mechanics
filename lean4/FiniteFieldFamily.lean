import Mathlib.FieldTheory.Finite.GaloisField

/-!
Finite-field family witnesses for the MUB odd-prime-power route.

This module packages mathlib's `GaloisField p k` construction into a small
MUB-facing witness: for every prime `p` and nonzero exponent `k`, there is a
finite field of characteristic `p` with `p^k` elements. The odd-prime-power
variant records the extra `p != 2` boundary needed by the current Weyl/Gauss
lane. This still does not prove the quadratic Gauss-norm theorem or any
Hilbert/GTMUR transport.
-/

namespace MUB

structure PrimePowerFiniteFieldFamily (p k : Nat) where
  carrier : Type
  field : Field carrier
  finite : Finite carrier
  charP : CharP carrier p
  card_eq : Nat.card carrier = p ^ k

noncomputable def primePowerFiniteFieldFamily
    (p k : Nat) [Fact p.Prime] (hk : k ≠ 0) :
    PrimePowerFiniteFieldFamily p k := by
  refine {
    carrier := GaloisField p k
    field := inferInstance
    finite := inferInstance
    charP := inferInstance
    card_eq := ?_
  }
  exact GaloisField.card p k hk

theorem prime_power_finite_field_family_exists
    (p k : Nat) [Fact p.Prime] (hk : k ≠ 0) :
    Nonempty (PrimePowerFiniteFieldFamily p k) := by
  exact ⟨primePowerFiniteFieldFamily p k hk⟩

theorem prime_power_finite_field_family_ringChar_eq
    {p k : Nat} (W : PrimePowerFiniteFieldFamily p k) :
    letI := W.field
    ringChar W.carrier = p := by
  letI := W.field
  letI := W.charP
  exact ringChar.eq W.carrier p

structure OddPrimePowerFiniteFieldFamily (p k : Nat)
    extends PrimePowerFiniteFieldFamily p k where
  prime_odd : p ≠ 2
  exponent_nonzero : k ≠ 0

noncomputable def oddPrimePowerFiniteFieldFamily
    (p k : Nat) [Fact p.Prime] (hpodd : p ≠ 2) (hk : k ≠ 0) :
    OddPrimePowerFiniteFieldFamily p k := {
  toPrimePowerFiniteFieldFamily := primePowerFiniteFieldFamily p k hk
  prime_odd := hpodd
  exponent_nonzero := hk
}

theorem odd_prime_power_finite_field_family_exists
    (p k : Nat) [Fact p.Prime] (hpodd : p ≠ 2) (hk : k ≠ 0) :
    Nonempty (OddPrimePowerFiniteFieldFamily p k) := by
  exact ⟨oddPrimePowerFiniteFieldFamily p k hpodd hk⟩

end MUB

#print axioms MUB.prime_power_finite_field_family_exists
#print axioms MUB.prime_power_finite_field_family_ringChar_eq
#print axioms MUB.odd_prime_power_finite_field_family_exists
