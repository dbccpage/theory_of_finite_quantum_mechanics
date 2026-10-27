import BornGaussRat
import Mathlib.Data.Rat.Cast.Defs
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-
Field automorphisms of ℚ(i).  AuthorityEffect: None.

Every ring homomorphism `ℚ(i) →+* ℚ(i)` is the identity or complex conjugation
(`ringHom_eq_id_or_star`): it fixes ℚ (`map_ratCast`), sends `i` to a square root of `−1`, and the
only square roots of `−1` in ℚ(i) are `± i` (`mul_self_eq_neg_one_iff`).  This is the algebraic fact
behind the two-case form of the finite exact Wigner theorem (`FiniteWignerTheorem`): over the exact
Born carrier ℚ(i)ⁿ the semilinear maps of the fundamental theorem of projective geometry can only be
linear or conjugate-linear, with no continuity hypothesis.  (The Wigner module itself does not use
this result; its coordinate dichotomy is forced directly by modulus equations.)

Nothing physical is claimed; exact arithmetic over ℚ throughout.
-/

namespace WignerFinite.GaussRatAut

open BornFinite

theorem mul_self_eq_neg_one_iff (z : GaussRat) :
    z * z = -1 ↔ z = GaussRat.I ∨ z = -GaussRat.I := by
  constructor
  · intro h
    have hre : z.re * z.re - z.im * z.im = -1 := by
      have := congrArg GaussRat.re h
      simpa [GaussRat.re_mul] using this
    have him : z.re * z.im + z.im * z.re = 0 := by
      have := congrArg GaussRat.im h
      simpa [GaussRat.im_mul] using this
    have hprod : z.re * z.im = 0 := by linarith
    rcases mul_eq_zero.mp hprod with h0 | h0
    · have h1 : z.im * z.im = 1 := by rw [h0] at hre; linarith
      rcases mul_self_eq_one_iff.mp h1 with h2 | h2
      · left
        ext <;> simp [h0, h2]
      · right
        ext <;> simp [h0, h2]
    · exfalso
      rw [h0] at hre
      nlinarith [mul_self_nonneg z.re]
  · rintro (rfl | rfl)
    · exact GaussRat.I_mul_I
    · rw [neg_mul_neg]
      exact GaussRat.I_mul_I

theorem ringHom_apply_I (φ : GaussRat →+* GaussRat) :
    φ GaussRat.I = GaussRat.I ∨ φ GaussRat.I = -GaussRat.I := by
  rw [← mul_self_eq_neg_one_iff, ← map_mul, GaussRat.I_mul_I, map_neg, map_one]

theorem ringHom_apply (φ : GaussRat →+* GaussRat) (z : GaussRat) :
    φ z = (z.re : GaussRat) + (z.im : GaussRat) * φ GaussRat.I := by
  have hz : z = (z.re : GaussRat) + (z.im : GaussRat) * GaussRat.I := by
    ext <;> simp
  conv_lhs => rw [hz]
  rw [map_add, map_mul, map_ratCast, map_ratCast]

/-- The automorphisms of ℚ(i): identity or conjugation. -/
theorem ringHom_eq_id_or_star (φ : GaussRat →+* GaussRat) :
    (∀ z, φ z = z) ∨ (∀ z, φ z = star z) := by
  rcases ringHom_apply_I φ with h | h
  · left
    intro z
    rw [ringHom_apply, h]
    ext <;> simp
  · right
    intro z
    rw [ringHom_apply, h]
    ext <;> simp

theorem id_ringHom_apply (z : GaussRat) : (RingHom.id GaussRat) z = z := rfl

theorem star_ringHom_apply (z : GaussRat) : (starRingEnd GaussRat) z = star z := rfl

/-- Both candidates occur: the identity and `starRingEnd`. -/
theorem id_and_star_are_ringHoms :
    (∀ z, (RingHom.id GaussRat) z = z) ∧ (∀ z, (starRingEnd GaussRat) z = star z) :=
  ⟨id_ringHom_apply, star_ringHom_apply⟩

/-- Conjugation is not the identity: the two cases are distinct. -/
theorem star_ne_id : ∃ z : GaussRat, star z ≠ z :=
  ⟨GaussRat.I, by
    rw [GaussRat.star_I]
    intro h
    have := congrArg GaussRat.im h
    norm_num at this⟩

end WignerFinite.GaussRatAut

#print axioms WignerFinite.GaussRatAut.mul_self_eq_neg_one_iff
#print axioms WignerFinite.GaussRatAut.ringHom_apply_I
#print axioms WignerFinite.GaussRatAut.ringHom_apply
#print axioms WignerFinite.GaussRatAut.ringHom_eq_id_or_star
#print axioms WignerFinite.GaussRatAut.id_ringHom_apply
#print axioms WignerFinite.GaussRatAut.star_ringHom_apply
#print axioms WignerFinite.GaussRatAut.id_and_star_are_ringHoms
#print axioms WignerFinite.GaussRatAut.star_ne_id
