import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.Field.ZMod
import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.Nat.Prime.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.IntervalCases

/-!
# What finite phase carriers can and cannot select inside the Gaussian rationals

AuthorityEffect: None.  Scope: the node L1-U1-SELECTOR-OTHER-SEGMENT ("Selection of C and U(1) from finite
carriers") is a pointer to a derivation owned by another segment.  This module does NOT establish that
selection.  It proves one exact, general finite-carrier statement about the rational unit circle
`S1(Q) = {(x, y) in Q^2 | x^2 + y^2 = 1}` (the unit Gaussian rationals, with complex multiplication):

* `circle_torsion`: a point of `S1(Q)` has finite order (`z^n = 1` for some `n > 0`) only if it is one of the four
  points `(+-1, 0)`, `(0, +-1)` (the unit group `mu_4`); equivalently `circle_torsion_iff`.  Every other rational
  phase has infinite order (`not_torsion_of_den`: whenever `2x` is not an integer), so a FINITE phase group inside
  the Gaussian rationals has order dividing 4 and cannot contain an order-3, 5, 6 or 8 phase
  (`cube_root_trivial`, `no_point_with_x_half`);
* the Cayley parametrisation `cayley_on_circle` / `every_point_is_cayley` / `cayley_reaches_south_pole` shows that
  every point of the circle is a Cayley point (`(m, n) = (y, 1 + x)` for `x != -1`, and `(m, 0)` gives `(-1, 0)`); the
  Cayley points include the four points of `mu_4`, and the infinite-order points are exactly the Cayley points with
  `2x` not an integer, i.e. the circle minus `mu_4` (a kernel statement through `circle_torsion_iff`; that there are
  infinitely many of them is not a kernel statement here, only the instance `u345_infinite_order`);
* instance corollary: `(3/5, 4/5)` has infinite order (`u345_infinite_order`).

The proof is elementary: with `2x = a / c` in lowest terms and `c >= 2`, the integers `W_n = c^n * 2 Re(z^n)` satisfy
`W_{n+2} = a W_{n+1} - c^2 W_n`; modulo a prime `p | c` this gives `W_n = a^n != 0`, while `z^n = 1` would force
`W_n = 2 c^n = 0 (mod p)`.

This is a no-go for finite phase subgroups of the unit Gaussian rationals only.  Finite carriers in the sense of finite
fields `F_p` have unit circles of order `p - 1` or `p + 1` (native table in the certificate, not a kernel statement), and
cyclotomic extensions of `Q(i)` contain larger finite phase groups; neither is treated.

Not claimed: any construction of the circle or the complex field from finite carriers, completion or continuity of
phases, the compact group U(1), the rival split-complex hyperbola, or any physical reading.  The Lean `selector_not_free`
in `H011U1SelectorBoundary` is `rfl` on a Boolean record whose `rival_excluded` field is set to `false` by hand; it
records a bookkeeping flag, not a derivation.
-/

namespace U1SelectorSegment

/-- Complex multiplication on pairs (real part, imaginary part). -/
def cmul (z w : ℚ × ℚ) : ℚ × ℚ := (z.1 * w.1 - z.2 * w.2, z.1 * w.2 + z.2 * w.1)

/-- Complex power. -/
def cpow (z : ℚ × ℚ) : ℕ → ℚ × ℚ
  | 0 => (1, 0)
  | n + 1 => cmul (cpow z n) z

@[simp] theorem cpow_zero (z : ℚ × ℚ) : cpow z 0 = (1, 0) := rfl
theorem cpow_succ (z : ℚ × ℚ) (n : ℕ) : cpow z (n + 1) = cmul (cpow z n) z := rfl

/-- The three-term recurrence of the real parts on the unit circle. -/
theorem re_rec (x y : ℚ) (h : x * x + y * y = 1) (n : ℕ) :
    (cpow (x, y) (n + 2)).1 = 2 * x * (cpow (x, y) (n + 1)).1 - (cpow (x, y) n).1 := by
  simp only [cpow_succ, cmul]
  linear_combination (-(cpow (x, y) n).1) * h

/-- The integer sequence `W_n = c^n * 2 Re z^n` for `2x = a / c`. -/
def Wseq (a c : ℤ) : ℕ → ℤ
  | 0 => 2
  | 1 => a
  | n + 2 => a * Wseq a c (n + 1) - c ^ 2 * Wseq a c n

theorem Wseq_cast (x y : ℚ) (h : x * x + y * y = 1) (a c : ℤ) (hac : (a : ℚ) = c * (2 * x)) (n : ℕ) :
    ((Wseq a c n : ℤ) : ℚ) = (c : ℚ) ^ n * (2 * (cpow (x, y) n).1) ∧
    ((Wseq a c (n + 1) : ℤ) : ℚ) = (c : ℚ) ^ (n + 1) * (2 * (cpow (x, y) (n + 1)).1) := by
  induction n with
  | zero =>
    refine ⟨by simp [Wseq], ?_⟩
    simp [Wseq, cpow_succ, cmul, hac]
  | succ n ih =>
    refine ⟨ih.2, ?_⟩
    have e : Wseq a c (n + 2) = a * Wseq a c (n + 1) - c ^ 2 * Wseq a c n := rfl
    rw [e]
    push_cast
    rw [ih.1, ih.2, re_rec x y h n, hac]
    ring

/-- Modulo a prime `p` dividing `c` but not `a`, `W_{n+1} = a^{n+1} != 0`. -/
theorem Wseq_mod (a c : ℤ) (p : ℕ) [Fact p.Prime] (hc : (c : ZMod p) = 0) (n : ℕ) :
    ((Wseq a c (n + 1) : ℤ) : ZMod p) = (a : ZMod p) ^ (n + 1) ∧
    ((Wseq a c (n + 2) : ℤ) : ZMod p) = (a : ZMod p) ^ (n + 2) := by
  induction n with
  | zero =>
    refine ⟨by simp [Wseq], ?_⟩
    have e : Wseq a c 2 = a * Wseq a c 1 - c ^ 2 * Wseq a c 0 := rfl
    rw [e]; push_cast; simp [Wseq, hc]; ring
  | succ n ih =>
    refine ⟨ih.2, ?_⟩
    have e : Wseq a c (n + 3) = a * Wseq a c (n + 2) - c ^ 2 * Wseq a c (n + 1) := rfl
    rw [e]; push_cast
    rw [ih.2, hc]; ring

/-- If `2x` is not an integer, no positive power of `(x, y)` is `1`: the point has infinite order. -/
theorem not_torsion_of_den (x y : ℚ) (h : x * x + y * y = 1) (hd : (2 * x).den ≠ 1) (n : ℕ) (hn : 0 < n) :
    cpow (x, y) n ≠ (1, 0) := by
  intro hz
  obtain ⟨p, hp, hpd⟩ := Nat.exists_prime_and_dvd hd
  haveI : Fact p.Prime := ⟨hp⟩
  have hac0 : (((2 * x).num : ℤ) : ℚ) = (((2 * x).den : ℤ) : ℚ) * (2 * x) := by
    have h1 := Rat.mul_den_eq_num (2 * x)
    push_cast
    rw [← h1]; ring
  have hcop : Nat.gcd (2 * x).num.natAbs (2 * x).den = 1 := (2 * x).reduced
  set a : ℤ := (2 * x).num with ha
  set c : ℤ := ((2 * x).den : ℤ) with hcdef
  have hac : (a : ℚ) = c * (2 * x) := hac0
  have hc0 : (c : ZMod p) = 0 := by
    rw [hcdef, Int.cast_natCast]
    exact (ZMod.natCast_eq_zero_iff _ _).mpr hpd
  have ha0 : (a : ZMod p) ≠ 0 := by
    intro h0
    rw [ZMod.intCast_zmod_eq_zero_iff_dvd] at h0
    have h1 : p ∣ a.natAbs := Int.natCast_dvd.mp h0
    have h2 : p ∣ Nat.gcd a.natAbs (2 * x).den := Nat.dvd_gcd h1 hpd
    rw [hcop] at h2
    exact hp.one_lt.ne' (Nat.dvd_one.mp h2)
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  have hW := (Wseq_cast x y h a c hac m).2
  rw [hz] at hW
  have hW' : Wseq a c (m + 1) = c ^ (m + 1) * 2 := by
    have : ((Wseq a c (m + 1) : ℤ) : ℚ) = ((c ^ (m + 1) * 2 : ℤ) : ℚ) := by
      rw [hW]; push_cast; ring
    exact_mod_cast this
  have h1 := (Wseq_mod a c p hc0 m).1
  rw [hW'] at h1
  push_cast at h1
  rw [hc0, zero_pow (Nat.succ_ne_zero m), zero_mul] at h1
  exact pow_ne_zero _ ha0 h1.symm

/-- `y^2 = 3/4` has no rational solution: there is no rational point with `x = +-1/2`. -/
theorem no_point_with_x_half (y : ℚ) : y * y ≠ 3 / 4 := by
  intro h
  have hsq : IsSquare (3 / 4 : ℚ) := ⟨y, h.symm⟩
  rw [Rat.isSquare_iff] at hsq
  obtain ⟨⟨r, hr⟩, -⟩ := hsq
  have hnum : ((3 : ℚ) / 4).num = 3 := by decide +kernel
  rw [hnum] at hr
  have : r ≤ -2 ∨ (-1 ≤ r ∧ r ≤ 1) ∨ 2 ≤ r := by omega
  rcases this with h1 | ⟨h1, h2⟩ | h1
  · nlinarith [hr]
  · nlinarith [hr]
  · nlinarith [hr]

/-- If `2x` is an integer the point is one of the four unit points, or it is excluded (`x = +-1/2`). -/
theorem circle_integral_case (x y : ℚ) (h : x * x + y * y = 1) (hd : (2 * x).den = 1) :
    (x, y) = (1, 0) ∨ (x, y) = (-1, 0) ∨ (x, y) = (0, 1) ∨ (x, y) = (0, -1) := by
  have hk : 2 * x = ((2 * x).num : ℚ) := by
    have := Rat.num_div_den (2 * x)
    rw [hd] at this
    simpa using this.symm
  set k : ℤ := (2 * x).num with hkdef
  have hkb : k * k ≤ 4 := by
    have h1 : (k : ℚ) * k ≤ 4 := by
      have : (k : ℚ) * k = 4 * (x * x) := by rw [← hk]; ring
      nlinarith [mul_self_nonneg y]
    exact_mod_cast h1
  have hk2 : -2 ≤ k ∧ k ≤ 2 := by constructor <;> nlinarith
  obtain ⟨hlo, hhi⟩ := hk2
  interval_cases k
  · -- k = -2: x = -1
    have hx : x = -1 := by push_cast at hk; linarith
    subst hx
    have hy : y = 0 := by nlinarith [mul_self_nonneg y]
    subst hy; right; left; rfl
  · exfalso
    have hx : x = -1 / 2 := by push_cast at hk; linarith
    subst hx
    exact no_point_with_x_half y (by linarith)
  · have hx : x = 0 := by push_cast at hk; linarith
    subst hx
    have hy : y * y = 1 := by linarith
    have : (y - 1) * (y + 1) = 0 := by ring_nf; linarith
    rcases mul_eq_zero.mp this with h1 | h1
    · right; right; left; have : y = 1 := by linarith
      rw [this]
    · right; right; right; have : y = -1 := by linarith
      rw [this]
  · exfalso
    have hx : x = 1 / 2 := by push_cast at hk; linarith
    subst hx
    exact no_point_with_x_half y (by linarith)
  · have hx : x = 1 := by push_cast at hk; linarith
    subst hx
    have hy : y = 0 := by nlinarith [mul_self_nonneg y]
    subst hy; left; rfl

/-- The unit group `mu_4 = {1, -1, i, -i}` in `S1(Q)`. -/
def mu4 (z : ℚ × ℚ) : Prop := z = (1, 0) ∨ z = (-1, 0) ∨ z = (0, 1) ∨ z = (0, -1)

/-- Torsion of the rational unit circle is exactly `mu_4`. -/
theorem circle_torsion (x y : ℚ) (h : x * x + y * y = 1) (n : ℕ) (hn : 0 < n) (hz : cpow (x, y) n = (1, 0)) :
    mu4 (x, y) := by
  by_cases hd : (2 * x).den = 1
  · exact circle_integral_case x y h hd
  · exact absurd hz (not_torsion_of_den x y h hd n hn)

theorem mu4_pow_four (z : ℚ × ℚ) (hz : mu4 z) : cpow z 4 = (1, 0) := by
  rcases hz with rfl | rfl | rfl | rfl <;> simp [cpow, cmul]

theorem circle_torsion_iff (x y : ℚ) (h : x * x + y * y = 1) :
    (∃ n : ℕ, 0 < n ∧ cpow (x, y) n = (1, 0)) ↔ mu4 (x, y) :=
  ⟨fun ⟨n, hn, hz⟩ => circle_torsion x y h n hn hz, fun hz => ⟨4, by norm_num, mu4_pow_four _ hz⟩⟩

/-- A finite phase group inside the Gaussian rationals has exponent dividing 4. -/
theorem torsion_exponent_divides_four (x y : ℚ) (h : x * x + y * y = 1) (n : ℕ) (hn : 0 < n)
    (hz : cpow (x, y) n = (1, 0)) : cpow (x, y) 4 = (1, 0) :=
  mu4_pow_four _ (circle_torsion x y h n hn hz)

/-- There is no nontrivial cube root of unity on the rational circle. -/
theorem cube_root_trivial (x y : ℚ) (h : x * x + y * y = 1) (hz : cpow (x, y) 3 = (1, 0)) : (x, y) = (1, 0) := by
  rcases circle_torsion x y h 3 (by norm_num) hz with h1 | h1 | h1 | h1
  · exact h1
  all_goals (rw [h1] at hz; norm_num [cpow, cmul] at hz)

/-- INSTANCE (corollary of the general theorem): `(3/5, 4/5)` has infinite order. -/
theorem u345_infinite_order (n : ℕ) (hn : 0 < n) : cpow (3 / 5, 4 / 5) n ≠ (1, 0) := by
  have hd : (2 * (3 / 5 : ℚ)).den ≠ 1 := by
    have : (2 * (3 / 5 : ℚ)).den = 5 := by decide +kernel
    omega
  exact not_torsion_of_den _ _ (by norm_num) hd n hn

/-- The Cayley parametrisation lands on the circle. -/
theorem cayley_on_circle (m n : ℚ) (h : m * m + n * n ≠ 0) :
    ((n * n - m * m) / (n * n + m * m)) * ((n * n - m * m) / (n * n + m * m)) +
      ((2 * m * n) / (n * n + m * m)) * ((2 * m * n) / (n * n + m * m)) = 1 := by
  have h' : n * n + m * m ≠ 0 := by intro e; apply h; linarith
  rw [div_mul_div_comm, div_mul_div_comm, ← add_div, div_eq_one_iff_eq (mul_ne_zero h' h')]
  ring

/-- Every point of the rational circle other than `(-1, 0)` is a Cayley point. -/
theorem every_point_is_cayley (x y : ℚ) (h : x * x + y * y = 1) (hx : x ≠ -1) :
    ∃ m n : ℚ, n * n + m * m ≠ 0 ∧ x = (n * n - m * m) / (n * n + m * m) ∧ y = (2 * m * n) / (n * n + m * m) := by
  have h1 : (1 + x) ≠ 0 := fun e => hx (by linarith)
  refine ⟨y, 1 + x, ?_, ?_, ?_⟩
  · have : (1 + x) * (1 + x) + y * y = 2 * (1 + x) := by nlinarith
    rw [this]; exact mul_ne_zero two_ne_zero h1
  · have : (1 + x) * (1 + x) + y * y = 2 * (1 + x) := by nlinarith
    rw [this, eq_div_iff (mul_ne_zero two_ne_zero h1)]
    nlinarith
  · have : (1 + x) * (1 + x) + y * y = 2 * (1 + x) := by nlinarith
    rw [this, eq_div_iff (mul_ne_zero two_ne_zero h1)]
    ring

/-- `(-1, 0)` is also a Cayley point: `n = 0` and `m != 0`. -/
theorem cayley_reaches_south_pole (m : ℚ) (hm : m ≠ 0) :
    ((0 * 0 - m * m) / (0 * 0 + m * m) = -1) ∧ ((2 * m * 0) / (0 * 0 + m * m) = 0) := by
  have h : m * m ≠ 0 := mul_ne_zero hm hm
  refine ⟨?_, by simp⟩
  field_simp
  ring

end U1SelectorSegment

#print axioms U1SelectorSegment.re_rec
#print axioms U1SelectorSegment.Wseq_cast
#print axioms U1SelectorSegment.Wseq_mod
#print axioms U1SelectorSegment.not_torsion_of_den
#print axioms U1SelectorSegment.no_point_with_x_half
#print axioms U1SelectorSegment.circle_integral_case
#print axioms U1SelectorSegment.circle_torsion
#print axioms U1SelectorSegment.circle_torsion_iff
#print axioms U1SelectorSegment.torsion_exponent_divides_four
#print axioms U1SelectorSegment.cube_root_trivial
#print axioms U1SelectorSegment.u345_infinite_order
#print axioms U1SelectorSegment.cayley_on_circle
#print axioms U1SelectorSegment.every_point_is_cayley
#print axioms U1SelectorSegment.cayley_reaches_south_pole
