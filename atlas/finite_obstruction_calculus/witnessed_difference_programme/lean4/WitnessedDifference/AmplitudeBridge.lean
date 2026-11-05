import Mathlib
import WitnessedDifference.ClassicalCorner

/-!
# From integer cochains to two-path amplitudes, with the readout left free

`WDP-CH19-O03` asks to relate the real cochain quotient and the declared phase
exponentiation of Chapter 5 to an operational amplitude model without assuming
the Born readout. The bridge of §19.4 has six slots: amplitude carrier,
addition of alternatives, transformation law, effect pairing, probability
readout, empirical interpretation. This module fills the first three from
cochain data over the Gaussian rationals `ℚ(i)` and proves what the
remaining slots can and cannot depend on. It does not fill the readout slot.

* `WDP-CH19-P11` (gauge descent). Two pairs `(z₁, z₂)`, `(w₁, w₂)` of
  amplitudes, with `z₁ ≠ 0`, differ by one common unit-norm phase exactly when
  `N z₁ = N w₁`, `N z₂ = N w₂` and `z₁ z̄₂ = w₁ w̄₂`. So a phase-blind readout of
  a pair of amplitudes is a function of `|z₁|²`, `|z₂|²` and the cross term
  `z₁ z̄₂`. For amplitudes built from an integer cochain `a` by the fixed rational
  phase `u = (3 + 4i)/5`, the cross term of two walks with common endpoints is
  the product of the magnitudes and the ratio of the two walk amplitudes (the
  loop holonomy when `a` is antisymmetric, which the statements do not use), and
  it does not change when `a` changes by a coboundary. The quadratic readout `N (z₁ + z₂)` and the quartic readout
  `N (z₁ + z₂)²` are both gauge invariant and differ, so gauge invariance does
  not select the Born readout.
* `WDP-CH19-P12` (exponentiation obstruction). The phase `u` has no square root
  among the unit-norm Gaussian rationals, so no group homomorphism from `(ℚ, +)`
  to the rational unit circle sends `1` to `u`: the exponentiation `exp(iαa)` of
  §5.4 is not available on rational cochains. Integer cochains do exponentiate,
  `a ↦ u^a`, and the exponentiation sends coboundaries to gauge
  transformations.

No declaration here derives the Born rule, unitarity as dynamics, or the
continuum field. Every statement is finite and exact.
-/

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace WitnessedDifference.AmplitudeBridge

/-- The Gaussian rationals `ℚ(i)`. -/
abbrev G := ClassicalCorner.GaussRat

/-- The norm `re² + im²`. -/
abbrev N (z : G) : ℚ := QuadraticAlgebra.norm z

theorem N_def (z : G) : N z = z.re * z.re + z.im * z.im := by
  simp [N, QuadraticAlgebra.norm_def]

theorem N_mul (z w : G) : N (z * w) = N z * N w :=
  map_mul QuadraticAlgebra.norm z w

theorem star_mul_self (z : G) : star z * z = algebraMap ℚ G (N z) := by
  rw [mul_comm]
  exact (QuadraticAlgebra.algebraMap_norm_eq_mul_star z).symm

theorem star_algebraMap (r : ℚ) : star (algebraMap ℚ G r) = algebraMap ℚ G r := by
  apply QuadraticAlgebra.ext
  · simp only [QuadraticAlgebra.re_star, QuadraticAlgebra.algebraMap_re,
      QuadraticAlgebra.algebraMap_im, mul_zero, add_zero]
  · simp only [QuadraticAlgebra.im_star, QuadraticAlgebra.algebraMap_im, neg_zero]

theorem N_eq_zero {z : G} (h : N z = 0) : z = 0 := by
  rw [N_def] at h
  have h1 : z.re = 0 := by nlinarith [mul_self_nonneg z.re, mul_self_nonneg z.im]
  have h2 : z.im = 0 := by nlinarith [mul_self_nonneg z.re, mul_self_nonneg z.im]
  ext <;> simp [h1, h2]

/-- A unit-norm phase: `ḡ g = 1`. -/
theorem isPhase_iff {g : G} : star g * g = 1 ↔ N g = 1 := by
  rw [star_mul_self]
  constructor
  · intro h
    have := congrArg QuadraticAlgebra.re h
    simpa only [QuadraticAlgebra.algebraMap_re, QuadraticAlgebra.re_one] using this
  · intro h
    rw [h]
    simp

/-! ## `WDP-CH19-P11`: gauge descent of phase-blind readouts -/

/-- `WDP-CH19-P11`. Two pairs of amplitudes differ by a common unit-norm phase
exactly when their norms agree and their cross terms agree. -/
theorem common_phase_iff (z1 z2 w1 w2 : G) (hz1 : z1 ≠ 0) :
    (∃ g : G, star g * g = 1 ∧ w1 = g * z1 ∧ w2 = g * z2) ↔
      N z1 = N w1 ∧ N z2 = N w2 ∧ z1 * star z2 = w1 * star w2 := by
  constructor
  · rintro ⟨g, hg, rfl, rfl⟩
    have hN : N g = 1 := isPhase_iff.1 hg
    refine ⟨by rw [N_mul, hN, one_mul], by rw [N_mul, hN, one_mul], ?_⟩
    have hg' : g * star g = 1 := by rw [mul_comm]; exact hg
    calc z1 * star z2 = (g * star g) * (z1 * star z2) := by rw [hg', one_mul]
      _ = g * z1 * star (g * z2) := by rw [star_mul]; ring
  · rintro ⟨h1, h2, hc⟩
    have hn : N z1 ≠ 0 := fun h => hz1 (N_eq_zero h)
    set A : ℚ →+* G := algebraMap ℚ G with hAdef
    set n : ℚ := N z1 with hndef
    have hA : A n⁻¹ * A n = 1 := by rw [← map_mul, inv_mul_cancel₀ hn, map_one]
    have hz : star z1 * z1 = A n := star_mul_self z1
    have hw : star w1 * w1 = A n := by rw [star_mul_self, ← h1]
    have hc' : z2 * star z1 = w2 * star w1 := by
      have := congrArg star hc
      simpa [star_mul, star_star] using this
    have hsA : star (A n⁻¹) = A n⁻¹ := star_algebraMap _
    refine ⟨A n⁻¹ * w1 * star z1, ?_, ?_, ?_⟩
    · have hsg : star (A n⁻¹ * w1 * star z1) = z1 * star w1 * A n⁻¹ := by
        rw [star_mul, star_mul, star_star, hsA]
        ring
      rw [hsg]
      linear_combination (A n⁻¹ ^ 2 * (star w1 * w1)) * hz + (A n⁻¹ ^ 2 * A n) * hw +
        (A n⁻¹ * A n + 1) * hA
    · linear_combination (-w1) * hA + (-(A n⁻¹) * w1) * hz
    · linear_combination (-w2) * hA + (-(A n⁻¹) * w2) * hw + (-(A n⁻¹) * w1) * hc'

/-- `WDP-CH19-P11`. A phase-blind readout of two amplitudes, one that a common
unit-norm phase does not change, takes the same value on any two pairs with the
same norms and the same cross term. -/
theorem phaseBlind_readout_factors {α : Type*} (R : G → G → α)
    (hR : ∀ g z1 z2, star g * g = 1 → R (g * z1) (g * z2) = R z1 z2)
    (z1 z2 w1 w2 : G) (hz1 : z1 ≠ 0)
    (h : N z1 = N w1 ∧ N z2 = N w2 ∧ z1 * star z2 = w1 * star w2) :
    R z1 z2 = R w1 w2 := by
  obtain ⟨g, hg, rfl, rfl⟩ := (common_phase_iff z1 z2 w1 w2 hz1).2 h
  exact (hR g z1 z2 hg).symm

/-- The quadratic readout of two alternatives. -/
def quadReadout (z1 z2 : G) : ℚ := N (z1 + z2)

/-- The quartic readout of two alternatives. -/
def quarticReadout (z1 z2 : G) : ℚ := N (z1 + z2) ^ 2

theorem quadReadout_phaseBlind (g z1 z2 : G) (hg : star g * g = 1) :
    quadReadout (g * z1) (g * z2) = quadReadout z1 z2 := by
  unfold quadReadout
  rw [← mul_add, N_mul, isPhase_iff.1 hg, one_mul]

theorem quarticReadout_phaseBlind (g z1 z2 : G) (hg : star g * g = 1) :
    quarticReadout (g * z1) (g * z2) = quarticReadout z1 z2 := by
  unfold quarticReadout
  rw [← mul_add, N_mul, isPhase_iff.1 hg, one_mul]

/-- The cross term of the quadratic readout: `N (z₁ + z₂)` is `N z₁ + N z₂`
plus the real part of `2 z₁ z̄₂`, here written as `z₁ z̄₂ + conj (z₁ z̄₂)`. -/
theorem quadReadout_expansion (z1 z2 : G) :
    algebraMap ℚ G (N (z1 + z2)) =
      algebraMap ℚ G (N z1) + algebraMap ℚ G (N z2) +
        (z1 * star z2 + star (z1 * star z2)) := by
  simp only [N, QuadraticAlgebra.algebraMap_norm_eq_mul_star, star_add, star_mul, star_star]
  ring

/-- `WDP-CH19-P11`. Both readouts are unchanged by a common phase, and they
differ: gauge invariance does not select the quadratic readout. -/
theorem gauge_invariance_does_not_select_the_readout :
    (∀ g z1 z2, star g * g = 1 → quadReadout (g * z1) (g * z2) = quadReadout z1 z2) ∧
      (∀ g z1 z2, star g * g = 1 →
        quarticReadout (g * z1) (g * z2) = quarticReadout z1 z2) ∧
      quadReadout 1 1 ≠ quarticReadout 1 1 := by
  refine ⟨quadReadout_phaseBlind, quarticReadout_phaseBlind, ?_⟩
  have h : N ((1 : G) + 1) = 4 := by
    rw [N_def, QuadraticAlgebra.re_add, QuadraticAlgebra.im_add, QuadraticAlgebra.re_one,
      QuadraticAlgebra.im_one]
    norm_num
  unfold quadReadout quarticReadout
  rw [h]
  norm_num

/-! ## The rational phase and integer cochains -/

/-- The fixed rational phase `u = (3 + 4i)/5`. -/
def phaseU : unitary G :=
  ⟨⟨3 / 5, 4 / 5⟩,
    QuadraticAlgebra.norm_eq_one_iff_mem_unitary.1 (by norm_num [QuadraticAlgebra.norm_def])⟩

section Walks

variable {V : Type*}

/-- The amplitude of a walk given as a list of vertices, for the antisymmetric
integer cochain `a`: the product of `u ^ a(v, w)` over its steps. -/
def amp (a : V → V → ℤ) : List V → unitary G
  | [] => 1
  | [_] => 1
  | v :: w :: rest => phaseU ^ a v w * amp a (w :: rest)

/-- Gauge covariance. If `a` changes by the coboundary of `f`, the amplitude of
a walk changes by the phase `u ^ (f end - f start)`. -/
theorem amp_gauge (a : V → V → ℤ) (f : V → ℤ) :
    ∀ (v : V) (rest : List V),
      amp (fun x y => a x y + (f y - f x)) (v :: rest) =
        phaseU ^ (f ((v :: rest).getLast (List.cons_ne_nil _ _)) - f v) *
          amp a (v :: rest) := by
  intro v rest
  induction rest generalizing v with
  | nil => simp [amp]
  | cons w rest ih =>
    have hlast : (v :: w :: rest).getLast (List.cons_ne_nil _ _) =
        (w :: rest).getLast (List.cons_ne_nil _ _) := by
      rw [List.getLast_cons_cons]
    simp only [amp, ih w, hlast]
    have e : f ((w :: rest).getLast (List.cons_ne_nil _ _)) - f v =
        (f ((w :: rest).getLast (List.cons_ne_nil _ _)) - f w) + (f w - f v) := by ring
    rw [e, zpow_add, zpow_add]
    ac_rfl

theorem holonomy_key (g x y : unitary G) : (g * x) * (g * y)⁻¹ = x * y⁻¹ := by
  rw [mul_inv_rev]
  calc g * x * (y⁻¹ * g⁻¹) = x * y⁻¹ * (g * g⁻¹) := by ac_rfl
    _ = x * y⁻¹ := by rw [mul_inv_cancel, mul_one]

/-- `WDP-CH19-P11`. The holonomy of two walks with common endpoints, the phase
between their amplitudes, is unchanged when the cochain changes by a
coboundary. It is a function of the cochain class. -/
theorem holonomy_gauge_invariant (a : V → V → ℤ) (f : V → ℤ) (v : V)
    (r1 r2 : List V)
    (hlast : (v :: r1).getLast (List.cons_ne_nil _ _) =
      (v :: r2).getLast (List.cons_ne_nil _ _)) :
    amp (fun x y => a x y + (f y - f x)) (v :: r1) *
        (amp (fun x y => a x y + (f y - f x)) (v :: r2))⁻¹ =
      amp a (v :: r1) * (amp a (v :: r2))⁻¹ := by
  rw [amp_gauge, amp_gauge, hlast]
  exact holonomy_key _ _ _

/-- Path amplitudes with magnitudes `r₁`, `r₂` have the cross term
`r₁ r₂` times the holonomy of the loop. -/
theorem cross_eq_holonomy (a : V → V → ℤ) (p q : List V) (r1 r2 : ℚ) :
    (algebraMap ℚ G r1 * ((amp a p : unitary G) : G)) *
        star (algebraMap ℚ G r2 * ((amp a q : unitary G) : G)) =
      algebraMap ℚ G (r1 * r2) * (((amp a p * (amp a q)⁻¹ : unitary G)) : G) := by
  have hinv : ((amp a q)⁻¹ : unitary G) = star (amp a q) := (Unitary.star_eq_inv _).symm
  rw [hinv, star_mul, star_algebraMap]
  simp only [Submonoid.coe_mul, Unitary.coe_star, map_mul]
  ring

/-- `WDP-CH19-P11`. A phase-blind readout of the two path amplitudes of an
integer cochain takes the same value on `a` and on `a + d₀f`: it depends on
the cochain only through its class modulo coboundaries. -/
theorem readout_depends_on_cochain_class {α : Type*} (R : G → G → α)
    (hR : ∀ g z1 z2, star g * g = 1 → R (g * z1) (g * z2) = R z1 z2)
    (a : V → V → ℤ) (f : V → ℤ) (v : V) (r1 r2 : List V) (m1 m2 : ℚ)
    (hlast : (v :: r1).getLast (List.cons_ne_nil _ _) =
      (v :: r2).getLast (List.cons_ne_nil _ _)) :
    R (algebraMap ℚ G m1 * ((amp (fun x y => a x y + (f y - f x)) (v :: r1) :
          unitary G) : G))
      (algebraMap ℚ G m2 * ((amp (fun x y => a x y + (f y - f x)) (v :: r2) :
          unitary G) : G)) =
      R (algebraMap ℚ G m1 * ((amp a (v :: r1) : unitary G) : G))
        (algebraMap ℚ G m2 * ((amp a (v :: r2) : unitary G) : G)) := by
  rw [amp_gauge, amp_gauge, ← hlast]
  simp only [Submonoid.coe_mul]
  have h1 : ∀ (x : ℚ) (y : G) (P : G), algebraMap ℚ G x * (P * y) =
      P * (algebraMap ℚ G x * y) := fun x y P => by ring
  rw [h1, h1]
  exact hR _ _ _ (Unitary.star_mul_self_of_mem (SetLike.coe_mem _))

end Walks

/-! ## `WDP-CH19-P12`: the exponentiation obstruction -/

theorem no_rational_with_square_four_fifths : ¬ ∃ x : ℚ, x * x = 4 / 5 := by
  rintro ⟨x, hx⟩
  have h5 : (5 * x) * (5 * x) = (20 : ℚ) := by linear_combination 25 * hx
  have hsq : IsSquare (((20 : ℤ)) : ℚ) := ⟨5 * x, by push_cast; linarith⟩
  rw [Rat.isSquare_intCast_iff] at hsq
  obtain ⟨r, hr⟩ := hsq
  have hle : r ≤ 5 := by nlinarith
  have hge : -5 ≤ r := by nlinarith
  interval_cases r <;> omega

/-- `WDP-CH19-P12`. The phase `u = (3 + 4i)/5` has no square root among the
unit-norm Gaussian rationals. -/
theorem phaseU_no_square_root : ¬ ∃ w : unitary G, w * w = phaseU := by
  rintro ⟨w, hw⟩
  have hN : N (w : G) = 1 := isPhase_iff.1 (Unitary.star_mul_self_of_mem w.2)
  have hmul : (w : G) * (w : G) = ⟨3 / 5, 4 / 5⟩ := by
    have := congrArg Subtype.val hw
    simpa [phaseU] using this
  have hre := congrArg QuadraticAlgebra.re hmul
  rw [N_def] at hN
  simp only [QuadraticAlgebra.re_mul] at hre
  apply no_rational_with_square_four_fifths
  refine ⟨(w : G).re, ?_⟩
  linarith

/-- `WDP-CH19-P12`. No group homomorphism from `(ℚ, +)` to the unit-norm
Gaussian rationals sends `1` to `u`. -/
theorem no_rational_exponentiation :
    ¬ ∃ φ : Multiplicative ℚ →* unitary G, φ (Multiplicative.ofAdd 1) = phaseU := by
  rintro ⟨φ, h1⟩
  apply phaseU_no_square_root
  refine ⟨φ (Multiplicative.ofAdd (1 / 2)), ?_⟩
  rw [← map_mul, ← h1]
  congr 1
  rw [← ofAdd_add]
  norm_num

/-- The Gaussian integer `2 + i` inside `ℚ(i)`. Its ratio to its conjugate is
the phase `u`. -/
def w2 : G := ⟨2, 1⟩

theorem phaseU_mul_star : (phaseU : G) * star w2 = w2 := by
  have h : (phaseU : G) = ⟨3 / 5, 4 / 5⟩ := rfl
  rw [h]
  ext <;> simp [w2, QuadraticAlgebra.star_mk] <;> norm_num

/-- The components of `(2 + i)ⁿ`. -/
def wc : ℕ → ℤ × ℤ
  | 0 => (1, 0)
  | n + 1 => (2 * (wc n).1 - (wc n).2, (wc n).1 + 2 * (wc n).2)

theorem w2_pow (n : ℕ) : w2 ^ n = ⟨((wc n).1 : ℚ), ((wc n).2 : ℚ)⟩ := by
  induction n with
  | zero =>
    ext <;> simp [wc, QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]
  | succ n ih =>
    rw [pow_succ, ih]
    ext <;> simp [wc, w2, QuadraticAlgebra.re_mul, QuadraticAlgebra.im_mul] <;> ring

theorem wc_dvd_one (n : ℕ) : (5 : ℤ) ∣ (wc (n + 1)).1 + 3 * (wc (n + 1)).2 := by
  simp only [wc]
  exact ⟨(wc n).1 + (wc n).2, by ring⟩

theorem wc_dvd_two (n : ℕ) : (5 : ℤ) ∣ (wc n).1 - 3 * (wc n).2 - (-1) ^ n := by
  induction n with
  | zero => simp [wc]
  | succ n ih =>
    have hp : ((-1 : ℤ) ^ (n + 1)) = -((-1 : ℤ) ^ n) := by rw [pow_succ]; ring
    rw [hp]
    simp only [wc]
    generalize ((-1 : ℤ) ^ n) = t at ih ⊢
    omega

/-- `WDP-CH19-P12`. No positive power of `u` is `1`: the phase `u` has infinite
order, so `n ↦ uⁿ` is injective on the integer cochains' exponents. -/
theorem phaseU_pow_ne_one (n : ℕ) (hn : 0 < n) : phaseU ^ n ≠ 1 := by
  intro h
  have h1 : ((phaseU : G)) ^ n = 1 := by
    have := congrArg Subtype.val h
    simpa using this
  have h2 : w2 ^ n = (star w2) ^ n := by
    calc w2 ^ n = ((phaseU : G) * star w2) ^ n := by rw [phaseU_mul_star]
      _ = (phaseU : G) ^ n * (star w2) ^ n := mul_pow _ _ _
      _ = (star w2) ^ n := by rw [h1, one_mul]
  have h3 : (w2 ^ n).im = 0 := by
    have := congrArg QuadraticAlgebra.im h2
    rw [← star_pow, QuadraticAlgebra.im_star] at this
    linarith
  rw [w2_pow] at h3
  have hb : (wc n).2 = 0 := by
    have : (((wc n).2 : ℤ) : ℚ) = 0 := h3
    exact_mod_cast this
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  have d1 := wc_dvd_one m
  have d2 := wc_dvd_two (m + 1)
  rw [hb] at d1 d2
  have hpm : ((-1 : ℤ) ^ (m + 1)) = 1 ∨ ((-1 : ℤ) ^ (m + 1)) = -1 := neg_one_pow_eq_or ℤ _
  generalize ((-1 : ℤ) ^ (m + 1)) = t at hpm d2
  omega

/-- `WDP-CH19-P12`. `u ^ n = 1` only for `n = 0`. -/
theorem phaseU_zpow_ne_one (n : ℤ) (hn : n ≠ 0) : phaseU ^ n ≠ 1 := by
  rcases Int.eq_nat_or_neg n with ⟨m, rfl | rfl⟩
  · rw [zpow_natCast]
    exact phaseU_pow_ne_one m (by omega)
  · rw [zpow_neg, zpow_natCast, Ne, inv_eq_one]
    exact phaseU_pow_ne_one m (by omega)

/-- `WDP-CH19-P12`, bundled. There is no exponentiation on rational cochains
with scale `u`, while integer exponents compose and send coboundaries to gauge
transformations. -/
theorem exponentiation_obstruction :
    (¬ ∃ w : unitary G, w * w = phaseU) ∧
      (¬ ∃ φ : Multiplicative ℚ →* unitary G, φ (Multiplicative.ofAdd 1) = phaseU) ∧
      (∀ m n : ℤ, phaseU ^ (m + n) = phaseU ^ m * phaseU ^ n) ∧
      (∀ n : ℤ, n ≠ 0 → phaseU ^ n ≠ 1) :=
  ⟨phaseU_no_square_root, no_rational_exponentiation, fun m n => zpow_add _ m n,
    phaseU_zpow_ne_one⟩

end WitnessedDifference.AmplitudeBridge
