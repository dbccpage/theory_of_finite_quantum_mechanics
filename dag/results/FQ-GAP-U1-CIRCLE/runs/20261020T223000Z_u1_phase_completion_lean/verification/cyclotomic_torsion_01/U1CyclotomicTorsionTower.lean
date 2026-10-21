import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Data.Rat.Lemmas

/-!
# U(1) Cyclotomic N-Torsion Tower, Rational Phase Quotient Q/Z, and Discrete Haar Orthogonality

This module mechanizes the algebraic properties of the finite $N$-torsion phase tower
$\varinjlim \mathbb{Z}/N\mathbb{Z} \cong \mathbb{Q}/\mathbb{Z}$ and discrete Haar character
sums on $N$-th roots of unity $\mu_N$:

1. **Finite $N$-Torsion Phase Tower & Directed Refinement Embeddings**:
   Rational phase representation `torsionPhase N a = a / N` and directed index refinement
   `refineIndex k a = k * a` for $N \to kN$, together with functoriality and exact
   invariance `torsionPhase (k * N) (refineIndex k a) = torsionPhase N a`.
2. **Rational Phase Quotient $\mathbb{Q}/\mathbb{Z}$ (`phaseEquiv`) & Universal $m$-Divisibility**:
   Modulo-$1$ phase equivalence on $\mathbb{Q}$, its `Setoid ℚ` structure, congruence under
   group operations, $N$-periodicity, universal $m$-divisibility (`rat_phase_divisible`),
   and the theorem that every element of $\mathbb{Q}/\mathbb{Z}$ is torsion
   (`rat_phase_every_element_torsion`).
   This contrasts with $S^1(\mathbb{Q})$, which lacks $m$-divisibility (e.g., $(3/5, 4/5)$ has
   no $2$-division in $S^1(\mathbb{Q})$) yet contains infinite-order aperiodic elements.
3. **Exact Finite Haar Character Orthogonality on $\mu_N$**:
   Polynomial identity $(1 - z) \sum_{j=0}^{N-1} z^j = 1 - z^N$, exact cancellation
   `geomSum z N = 0` for every non-trivial $N$-th root of unity ($z^N = 1, z \neq 1$) in any
   integral domain, normalized trivial-character average `geomSum 1 N / N = 1`, and explicit
   4th-root Gaussian unit cancellation in $\mathbb{Z} \times \mathbb{Z}$.
-/

namespace U1Fable.CyclotomicTorsionTower

/-! ## 1. Finite $N$-Torsion Phase Tower & Directed Refinement Embeddings -/

/-- Rational phase associated with integer numerator `a` at torsion level `N`. -/
def torsionPhase (N : ℕ) (a : ℤ) : ℚ :=
  (a : ℚ) / (N : ℚ)

/-- Directed refinement map on integer phase numerators for level transition `N → k * N`. -/
def refineIndex (k : ℕ) (a : ℤ) : ℤ :=
  (k : ℤ) * a

/-- Identity refinement (`k = 1`) acts as the identity on phase numerators. -/
theorem refineIndex_one (a : ℤ) : refineIndex 1 a = a := by
  unfold refineIndex
  ring

/-- Directed refinement composes multiplicatively across divisibility levels `N → kN → mkN`. -/
theorem refineIndex_comp (m k : ℕ) (a : ℤ) :
    refineIndex m (refineIndex k a) = refineIndex (m * k) a := by
  unfold refineIndex
  push_cast
  ring

/-- Directed refinement is an additive homomorphism on phase numerators. -/
theorem refineIndex_add (k : ℕ) (a b : ℤ) :
    refineIndex k (a + b) = refineIndex k a + refineIndex k b := by
  unfold refineIndex
  ring

/-- Directed refinement preserves zero phase numerator. -/
theorem refineIndex_zero (k : ℕ) : refineIndex k 0 = 0 := by
  unfold refineIndex
  ring

/-- Directed refinement preserves negation of phase numerators. -/
theorem refineIndex_neg (k : ℕ) (a : ℤ) :
    refineIndex k (-a) = -refineIndex k a := by
  unfold refineIndex
  ring

/-- Directed refinement preserves subtraction of phase numerators. -/
theorem refineIndex_sub (k : ℕ) (a b : ℤ) :
    refineIndex k (a - b) = refineIndex k a - refineIndex k b := by
  unfold refineIndex
  ring

/-- The refined numerator `k * a` at level `k * N` represents the exact same rational phase
as `a` at level `N`. -/
theorem torsionPhase_refine_eq (N k : ℕ) (hN : 0 < N) (hk : 0 < k) (a : ℤ) :
    torsionPhase (k * N) (refineIndex k a) = torsionPhase N a := by
  unfold torsionPhase refineIndex
  have hN0 : (N : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.ne_of_gt hN)
  have hkN0 : ((k * N : ℕ) : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.ne_of_gt (Nat.mul_pos hk hN))
  rw [div_eq_div_iff hkN0 hN0]
  push_cast
  ring

/-- At fixed level `N`, `torsionPhase N` is an additive homomorphism from `ℤ` to `ℚ`. -/
theorem torsionPhase_add (N : ℕ) (a b : ℤ) :
    torsionPhase N (a + b) = torsionPhase N a + torsionPhase N b := by
  unfold torsionPhase
  push_cast
  ring

/-- At fixed level `N`, `torsionPhase N 0 = 0`. -/
theorem torsionPhase_zero (N : ℕ) : torsionPhase N 0 = 0 := by
  unfold torsionPhase
  ring

/-- At fixed level `N`, `torsionPhase N` commutes with negation. -/
theorem torsionPhase_neg (N : ℕ) (a : ℤ) :
    torsionPhase N (-a) = -torsionPhase N a := by
  unfold torsionPhase
  push_cast
  ring

/-- At fixed level `N`, `torsionPhase N` commutes with subtraction. -/
theorem torsionPhase_sub (N : ℕ) (a b : ℤ) :
    torsionPhase N (a - b) = torsionPhase N a - torsionPhase N b := by
  unfold torsionPhase
  push_cast
  ring

/-! ## 2. Rational Phase Quotient $\mathbb{Q}/\mathbb{Z}$ (`phaseEquiv`) & Universal $m$-Divisibility -/

/-- Modulo-1 phase equivalence on `ℚ`: two rational phases are equivalent in `ℚ/ℤ`
if and only if their difference is an integer. -/
def phaseEquiv (p q : ℚ) : Prop :=
  ∃ k : ℤ, p - q = (k : ℚ)

/-- Reflexivity of modulo-1 phase equivalence. -/
theorem phaseEquiv_refl (p : ℚ) : phaseEquiv p p := by
  refine ⟨0, ?_⟩
  push_cast
  ring

/-- Symmetry of modulo-1 phase equivalence. -/
theorem phaseEquiv_symm {p q : ℚ} (h : phaseEquiv p q) : phaseEquiv q p := by
  rcases h with ⟨k, hk⟩
  refine ⟨-k, ?_⟩
  push_cast
  linarith

/-- Transitivity of modulo-1 phase equivalence. -/
theorem phaseEquiv_trans {p q r : ℚ} (hpq : phaseEquiv p q) (hqr : phaseEquiv q r) :
    phaseEquiv p r := by
  rcases hpq with ⟨j, hj⟩
  rcases hqr with ⟨k, hk⟩
  refine ⟨j + k, ?_⟩
  push_cast
  linarith

/-- `Setoid ℚ` instance packaging the equivalence relation of `ℚ/ℤ`. -/
def phaseEquiv_setoid : Setoid ℚ where
  r := phaseEquiv
  iseqv := ⟨phaseEquiv_refl, phaseEquiv_symm, phaseEquiv_trans⟩

/-- Modulo-1 phase equivalence is a congruence with respect to rational addition. -/
theorem phaseEquiv_add {p₁ q₁ p₂ q₂ : ℚ}
    (h₁ : phaseEquiv p₁ q₁) (h₂ : phaseEquiv p₂ q₂) :
    phaseEquiv (p₁ + p₂) (q₁ + q₂) := by
  rcases h₁ with ⟨k₁, hk₁⟩
  rcases h₂ with ⟨k₂, hk₂⟩
  refine ⟨k₁ + k₂, ?_⟩
  push_cast
  linarith

/-- Modulo-1 phase equivalence is a congruence with respect to negation. -/
theorem phaseEquiv_neg {p q : ℚ} (h : phaseEquiv p q) : phaseEquiv (-p) (-q) := by
  rcases h with ⟨k, hk⟩
  refine ⟨-k, ?_⟩
  push_cast
  linarith

/-- Modulo-1 phase equivalence is a congruence with respect to subtraction. -/
theorem phaseEquiv_sub {p₁ q₁ p₂ q₂ : ℚ}
    (h₁ : phaseEquiv p₁ q₁) (h₂ : phaseEquiv p₂ q₂) :
    phaseEquiv (p₁ - p₂) (q₁ - q₂) := by
  rcases h₁ with ⟨k₁, hk₁⟩
  rcases h₂ with ⟨k₂, hk₂⟩
  refine ⟨k₁ - k₂, ?_⟩
  push_cast
  linarith

/-- Fundamental `N`-periodicity of `torsionPhase N`: shifting the integer index by `N`
shifts the rational phase by `1`, hence represents the same class in `ℚ/ℤ`. -/
theorem torsionPhase_period (N : ℕ) (hN : 0 < N) (a : ℤ) :
    phaseEquiv (torsionPhase N (a + N)) (torsionPhase N a) := by
  refine ⟨1, ?_⟩
  unfold torsionPhase
  have hN0 : (N : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.ne_of_gt hN)
  have hsub : ((a + (N : ℤ) : ℤ) : ℚ) / (N : ℚ) - (a : ℚ) / (N : ℚ) = (N : ℚ) / (N : ℚ) := by
    push_cast
    ring
  rw [hsub, div_self hN0]
  norm_num

/-- Multi-periodicity of `torsionPhase N`: shifting the integer index by `m * N`
produces an equivalent phase in `ℚ/ℤ`. -/
theorem torsionPhase_multi_period (N : ℕ) (hN : 0 < N) (a m : ℤ) :
    phaseEquiv (torsionPhase N (a + m * N)) (torsionPhase N a) := by
  refine ⟨m, ?_⟩
  unfold torsionPhase
  have hN0 : (N : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.ne_of_gt hN)
  have hsub :
      ((a + m * (N : ℤ) : ℤ) : ℚ) / (N : ℚ) - (a : ℚ) / (N : ℚ) =
        (m : ℚ) * ((N : ℚ) / (N : ℚ)) := by
    push_cast
    ring
  rw [hsub, div_self hN0, mul_one]

/-- Universal `m`-divisibility of rational phases: for every `q : ℚ` and every `m > 0`,
there exists a rational phase `r = q / m` such that `m * r = q`.
This contrasts with the rational unit circle `S¹(ℚ)`, where `u = (3/5, 4/5)` has no
2-division point. -/
theorem rat_phase_divisible (q : ℚ) (m : ℕ) (hm : 0 < m) :
    ∃ r : ℚ, (m : ℚ) * r = q := by
  refine ⟨q / (m : ℚ), ?_⟩
  have hm0 : (m : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.ne_of_gt hm)
  exact mul_div_cancel₀ q hm0

/-- Universal `m`-divisibility in the quotient `ℚ/ℤ`. -/
theorem rat_phase_divisible_mod_one (q : ℚ) (m : ℕ) (hm : 0 < m) :
    ∃ r : ℚ, phaseEquiv ((m : ℚ) * r) q := by
  rcases rat_phase_divisible q m hm with ⟨r, hr⟩
  refine ⟨r, ?_⟩
  rw [hr]
  exact phaseEquiv_refl q

/-- Every rational number arises at some finite level `N > 0` of the torsion phase tower. -/
theorem rat_in_torsion_tower (q : ℚ) :
    ∃ (N : ℕ) (a : ℤ), 0 < N ∧ torsionPhase N a = q := by
  refine ⟨q.den, q.num, q.den_pos, ?_⟩
  unfold torsionPhase
  exact Rat.num_div_den q

/-- Every element of `ℚ/ℤ` is torsion: for every `q : ℚ`, there exists `N > 0`
(specifically `N = q.den`) such that `N * q ≡ 0 (mod 1)`.
Together with `rat_phase_divisible`, this shows that the direct limit `ℚ/ℤ` achieves full
divisibility while consisting exclusively of torsion elements, unlike `S¹(ℚ)`. -/
theorem rat_phase_every_element_torsion (q : ℚ) :
    ∃ N : ℕ, 0 < N ∧ phaseEquiv ((N : ℚ) * q) 0 := by
  refine ⟨q.den, q.den_pos, q.num, ?_⟩
  have hden : (q.den : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.ne_of_gt q.den_pos)
  have hmul : (q.den : ℚ) * q = (q.num : ℚ) :=
    (congrArg ((q.den : ℚ) * ·) (Rat.num_div_den q).symm).trans
      (mul_div_cancel₀ (q.num : ℚ) hden)
  linarith

/-! ## 3. Exact Finite Haar Character Orthogonality on $\mu_N$ -/

/-- Finite geometric character sum $\sum_{j=0}^{N-1} z^j$ in any commutative ring `R`. -/
def geomSum {R : Type*} [CommRing R] (z : R) : ℕ → R
  | 0 => 0
  | n + 1 => geomSum z n + z ^ n

/-- Base value `geomSum z 0 = 0`. -/
theorem geomSum_zero {R : Type*} [CommRing R] (z : R) : geomSum z 0 = 0 :=
  rfl

/-- Step recurrence `geomSum z (n + 1) = geomSum z n + z ^ n`. -/
theorem geomSum_succ {R : Type*} [CommRing R] (z : R) (n : ℕ) :
    geomSum z (n + 1) = geomSum z n + z ^ n :=
  rfl

/-- Single-term geometric sum `geomSum z 1 = 1`. -/
theorem geomSum_one {R : Type*} [CommRing R] (z : R) : geomSum z 1 = 1 := by
  simp [geomSum]

/-- Left telescopic polynomial identity `(1 - z) * geomSum z N = 1 - z ^ N`. -/
theorem one_sub_mul_geomSum {R : Type*} [CommRing R] (z : R) (N : ℕ) :
    (1 - z) * geomSum z N = 1 - z ^ N := by
  induction N with
  | zero =>
    simp [geomSum]
  | succ n ih =>
    calc
      (1 - z) * geomSum z (n + 1) = (1 - z) * (geomSum z n + z ^ n) := rfl
      _ = (1 - z) * geomSum z n + (1 - z) * z ^ n := by ring
      _ = (1 - z ^ n) + (1 - z) * z ^ n := by rw [ih]
      _ = 1 - z ^ (n + 1) := by ring

/-- Right telescopic polynomial identity `geomSum z N * (1 - z) = 1 - z ^ N`. -/
theorem geomSum_mul_one_sub {R : Type*} [CommRing R] (z : R) (N : ℕ) :
    geomSum z N * (1 - z) = 1 - z ^ N := by
  rw [mul_comm, one_sub_mul_geomSum]

/-- Exact discrete Haar phase cancellation: for any non-trivial `N`-th root of unity
(`z ^ N = 1` and `z ≠ 1`) in a commutative ring without zero divisors, the character sum
`geomSum z N` vanishes identically. -/
theorem haar_sum_root_of_unity {R : Type*} [CommRing R] [NoZeroDivisors R]
    (z : R) (N : ℕ) (hroot : z ^ N = 1) (hne : z ≠ 1) :
    geomSum z N = 0 := by
  have hprod : (1 - z) * geomSum z N = 0 := by
    rw [one_sub_mul_geomSum, hroot, sub_self]
  have hsub : 1 - z ≠ 0 := sub_ne_zero.mpr (Ne.symm hne)
  rcases mul_eq_zero.mp hprod with hzero | hgeom
  · exact False.elim (hsub hzero)
  · exact hgeom

/-- Unnormalized Haar sum of the trivial character `z = 1` over `N` points equals `N`. -/
theorem haar_sum_trivial (N : ℕ) : geomSum (1 : ℚ) N = (N : ℚ) := by
  induction N with
  | zero =>
    simp [geomSum]
  | succ n ih =>
    simp [geomSum, ih]

/-- Normalized Haar average of the trivial character `z = 1` over `N > 0` points equals `1`. -/
theorem haar_avg_trivial (N : ℕ) (hN : 0 < N) :
    geomSum (1 : ℚ) N / (N : ℚ) = 1 := by
  rw [haar_sum_trivial]
  have hN0 : (N : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.ne_of_gt hN)
  exact div_self hN0

/-- Explicit instantiation of discrete Haar cancellation on the 4th roots of unity
`{ (1,0), (0,1), (-1,0), (0,-1) }` in the Gaussian integer plane `ℤ × ℤ`. -/
theorem gauss_fourth_roots_haar_sum_zero :
    ((1 : ℤ), (0 : ℤ)) + ((0 : ℤ), (1 : ℤ)) + ((-1 : ℤ), (0 : ℤ)) + ((0 : ℤ), (-1 : ℤ)) =
      ((0 : ℤ), (0 : ℤ)) := by
  ext <;> simp

end U1Fable.CyclotomicTorsionTower

#print axioms U1Fable.CyclotomicTorsionTower.torsionPhase
#print axioms U1Fable.CyclotomicTorsionTower.refineIndex
#print axioms U1Fable.CyclotomicTorsionTower.refineIndex_one
#print axioms U1Fable.CyclotomicTorsionTower.refineIndex_comp
#print axioms U1Fable.CyclotomicTorsionTower.refineIndex_add
#print axioms U1Fable.CyclotomicTorsionTower.refineIndex_zero
#print axioms U1Fable.CyclotomicTorsionTower.refineIndex_neg
#print axioms U1Fable.CyclotomicTorsionTower.refineIndex_sub
#print axioms U1Fable.CyclotomicTorsionTower.torsionPhase_refine_eq
#print axioms U1Fable.CyclotomicTorsionTower.torsionPhase_add
#print axioms U1Fable.CyclotomicTorsionTower.torsionPhase_zero
#print axioms U1Fable.CyclotomicTorsionTower.torsionPhase_neg
#print axioms U1Fable.CyclotomicTorsionTower.torsionPhase_sub
#print axioms U1Fable.CyclotomicTorsionTower.phaseEquiv
#print axioms U1Fable.CyclotomicTorsionTower.phaseEquiv_refl
#print axioms U1Fable.CyclotomicTorsionTower.phaseEquiv_symm
#print axioms U1Fable.CyclotomicTorsionTower.phaseEquiv_trans
#print axioms U1Fable.CyclotomicTorsionTower.phaseEquiv_setoid
#print axioms U1Fable.CyclotomicTorsionTower.phaseEquiv_add
#print axioms U1Fable.CyclotomicTorsionTower.phaseEquiv_neg
#print axioms U1Fable.CyclotomicTorsionTower.phaseEquiv_sub
#print axioms U1Fable.CyclotomicTorsionTower.torsionPhase_period
#print axioms U1Fable.CyclotomicTorsionTower.torsionPhase_multi_period
#print axioms U1Fable.CyclotomicTorsionTower.rat_phase_divisible
#print axioms U1Fable.CyclotomicTorsionTower.rat_phase_divisible_mod_one
#print axioms U1Fable.CyclotomicTorsionTower.rat_in_torsion_tower
#print axioms U1Fable.CyclotomicTorsionTower.rat_phase_every_element_torsion
#print axioms U1Fable.CyclotomicTorsionTower.geomSum
#print axioms U1Fable.CyclotomicTorsionTower.geomSum_zero
#print axioms U1Fable.CyclotomicTorsionTower.geomSum_succ
#print axioms U1Fable.CyclotomicTorsionTower.geomSum_one
#print axioms U1Fable.CyclotomicTorsionTower.one_sub_mul_geomSum
#print axioms U1Fable.CyclotomicTorsionTower.geomSum_mul_one_sub
#print axioms U1Fable.CyclotomicTorsionTower.haar_sum_root_of_unity
#print axioms U1Fable.CyclotomicTorsionTower.haar_sum_trivial
#print axioms U1Fable.CyclotomicTorsionTower.haar_avg_trivial
#print axioms U1Fable.CyclotomicTorsionTower.gauss_fourth_roots_haar_sum_zero
