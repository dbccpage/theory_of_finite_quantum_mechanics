/-!
# Component quantum: finite matrix identities for DP-9, DP-8, DP-7

Lean-core statements for the finite algebraic parts of the derivation
proposals DP-9, DP-8 and DP-7 (`coda_wdp_derivations_20261006`). Only `Init`
is imported. Matrices are integer tables; exact rationals are Lean core
`Rat`. Nothing here constructs a Hilbert space, a trace norm, a matrix
exponential or a channel; those parts are named residuals.

* DP-9. `Z = diag(1,-1)` and `X = [[0,1],[1,0]]` are involutions and
  anticommute. On one qubit the CHSH-shaped operator
  `A0B0 + A0B1 + A1B0 - A1B1` is `2I + 2ZX` for `A1 = -X` and `0` for
  `A1 = X`; the first is not symmetric. The two-qubit sum-of-squares identity
  `F0² + F1² = 4I - 2(Z⊗Z + X⊗X)` with `F0 = Z⊗I - I⊗Z`,
  `F1 = X⊗I - I⊗X` holds over the integers, and the quadratic form of
  `Bs = Z⊗Z + X⊗X` is at most `2|v|²` on `Rat⁴`, with equality at
  `v = (1,0,0,1)`. Deterministic CHSH values are `±2`; no deterministic
  assignment reproduces the PR-box relation.
* DP-8. The transpose Choi matrix on dimension two has value `-2` on
  `(0,1,-1,0)`; `diag(0,2,-1)` has all leading principal minors zero and a
  negative value on `e3`; the integer `H` of the report has `HᵀH = 3I₄`, and
  `3(a²+b²) = d²` forces `a = b = d = 0` (mod-three descent).
* DP-7. The coefficient comparison `4k(k+1) ≤ 6k²` holds exactly for
  `k = 0` or `k ≥ 2` (fails at `k = 1`); the quadratic envelope `νt - ct²` is
  at least `νt/2` and monotone on `0 ≤ t`, `2ct ≤ ν`; coefficient relaxation
  under certified bounds; the replayed values `11/625`, `173/20000`,
  `11/1250`; the rational sine enclosure comparison; the integer identities
  `(X⊗X + 100 Z⊗I)² = 10001·I` and `9999² + 200² = 10001²`.

Scope: the analytic chain of DP-7 (support counting of commutators, trace
norm duality, the Taylor remainder for the matrix exponential) and the scale
`r = √2` in DP-9 (`B = r·Bs`) are not formalized; the bound `B ≤ 2√2` is
represented by `Bs ≤ 2` with `r` a positive scalar outside `Rat`.
AuthorityEffect: None.
-/
namespace WitnessedDifference.ComponentQuantum

/-! ## Integer `2×2` matrices -/

/-- An integer `2×2` matrix `[[a,b],[c,d]]`. -/
structure M2 where
  a : Int
  b : Int
  c : Int
  d : Int
  deriving DecidableEq, Repr

namespace M2

def mul (x y : M2) : M2 :=
  ⟨x.a * y.a + x.b * y.c, x.a * y.b + x.b * y.d,
   x.c * y.a + x.d * y.c, x.c * y.b + x.d * y.d⟩

def add (x y : M2) : M2 := ⟨x.a + y.a, x.b + y.b, x.c + y.c, x.d + y.d⟩

def neg (x : M2) : M2 := ⟨-x.a, -x.b, -x.c, -x.d⟩

def sub (x y : M2) : M2 := add x (neg y)

def smul (k : Int) (x : M2) : M2 := ⟨k * x.a, k * x.b, k * x.c, k * x.d⟩

def transpose (x : M2) : M2 := ⟨x.a, x.c, x.b, x.d⟩

def one : M2 := ⟨1, 0, 0, 1⟩

def zero : M2 := ⟨0, 0, 0, 0⟩

/-- Entry `(r, c)`, zero outside the table. -/
def entry (x : M2) : Nat → Nat → Int
  | 0, 0 => x.a
  | 0, 1 => x.b
  | 1, 0 => x.c
  | 1, 1 => x.d
  | _, _ => 0

end M2

/-- `Z = diag(1,-1)`. -/
def pauliZ : M2 := ⟨1, 0, 0, -1⟩

/-- `X = [[0,1],[1,0]]`. -/
def pauliX : M2 := ⟨0, 1, 1, 0⟩

/-- DP-9: `Z² = I`, `X² = I` and `ZX = -XZ`. -/
theorem pauli_relations :
    pauliZ.mul pauliZ = M2.one ∧ pauliX.mul pauliX = M2.one ∧
      pauliZ.mul pauliX = (pauliX.mul pauliZ).neg := by
  decide

/-- The one-carrier CHSH-shaped operator `A0B0 + A0B1 + A1B0 - A1B1`. -/
def chsh1 (A0 A1 B0 B1 : M2) : M2 :=
  ((A0.mul B0).add (A0.mul B1)).add ((A1.mul B0).sub (A1.mul B1))

/-- DP-9: with `A1 = -X` the operator is `2I + 2ZX`. -/
theorem single_qubit_minus_x :
    chsh1 pauliZ pauliX.neg pauliZ pauliX =
      (M2.smul 2 M2.one).add (M2.smul 2 (pauliZ.mul pauliX)) := by
  decide

/-- DP-9: with `A1 = X` the operator is `0`. -/
theorem single_qubit_plus_x :
    chsh1 pauliZ pauliX pauliZ pauliX = M2.zero := by
  decide

/-- DP-9: the `A1 = -X` operator is not symmetric, so its expectation on a
state need not be real (the report's value `2 + 2i`). -/
theorem single_qubit_minus_x_not_symmetric :
    (chsh1 pauliZ pauliX.neg pauliZ pauliX).transpose ≠
      chsh1 pauliZ pauliX.neg pauliZ pauliX := by
  decide

/-! ## Integer `4×4` matrices as tables on indices below four -/

/-- A `4×4` integer table (entries outside `0..3` are ignored). -/
abbrev M4 := Nat → Nat → Int

/-- Equality on the index box `0..3 × 0..3`. -/
def M4.Eq (x y : M4) : Prop := ∀ i, i < 4 → ∀ j, j < 4 → x i j = y i j

instance (x y : M4) : Decidable (M4.Eq x y) := by
  unfold M4.Eq; exact inferInstance

def kron (x y : M2) : M4 := fun i j => x.entry (i / 2) (j / 2) * y.entry (i % 2) (j % 2)

def mul4 (x y : M4) : M4 := fun i j =>
  x i 0 * y 0 j + x i 1 * y 1 j + x i 2 * y 2 j + x i 3 * y 3 j

def add4 (x y : M4) : M4 := fun i j => x i j + y i j

def sub4 (x y : M4) : M4 := fun i j => x i j - y i j

def smul4 (k : Int) (x : M4) : M4 := fun i j => k * x i j

def transpose4 (x : M4) : M4 := fun i j => x j i

def one4 : M4 := fun i j => if i = j then 1 else 0

/-- `F0 = Z⊗I - I⊗Z`. -/
def sosF0 : M4 := sub4 (kron pauliZ M2.one) (kron M2.one pauliZ)

/-- `F1 = X⊗I - I⊗X`. -/
def sosF1 : M4 := sub4 (kron pauliX M2.one) (kron M2.one pauliX)

/-- `Bs = Z⊗Z + X⊗X`, the CHSH operator divided by `r = √2`. -/
def chshBs : M4 := add4 (kron pauliZ pauliZ) (kron pauliX pauliX)

/-- DP-9: the integer sum-of-squares identity
`F0² + F1² = 4I - 2(Z⊗Z + X⊗X)`. -/
theorem sos_identity :
    M4.Eq (add4 (mul4 sosF0 sosF0) (mul4 sosF1 sosF1))
      (sub4 (smul4 4 one4) (smul4 2 chshBs)) := by
  decide

/-- DP-9: `F0` and `F1` are symmetric. -/
theorem sos_factors_symmetric :
    M4.Eq (transpose4 sosF0) sosF0 ∧ M4.Eq (transpose4 sosF1) sosF1 := by
  decide

/-- The explicit table of `Bs`. -/
def bsTable : Nat → Nat → Int
  | 0, 0 => 1 | 0, 3 => 1 | 1, 1 => -1 | 1, 2 => 1
  | 2, 1 => 1 | 2, 2 => -1 | 3, 0 => 1 | 3, 3 => 1
  | _, _ => 0

/-- DP-9: `Bs` equals its explicit table. -/
theorem chshBs_table : M4.Eq chshBs bsTable := by decide

/-- The quadratic form of an integer table on `Rat⁴`. -/
def quad4 (m : Nat → Nat → Int) (v : Nat → Rat) : Rat :=
  v 0 * ((m 0 0 : Rat) * v 0 + (m 0 1 : Rat) * v 1 + (m 0 2 : Rat) * v 2 + (m 0 3 : Rat) * v 3) +
  v 1 * ((m 1 0 : Rat) * v 0 + (m 1 1 : Rat) * v 1 + (m 1 2 : Rat) * v 2 + (m 1 3 : Rat) * v 3) +
  v 2 * ((m 2 0 : Rat) * v 0 + (m 2 1 : Rat) * v 1 + (m 2 2 : Rat) * v 2 + (m 2 3 : Rat) * v 3) +
  v 3 * ((m 3 0 : Rat) * v 0 + (m 3 1 : Rat) * v 1 + (m 3 2 : Rat) * v 2 + (m 3 3 : Rat) * v 3)

/-- The squared Euclidean norm on `Rat⁴`. -/
def normSq4 (v : Nat → Rat) : Rat := v 0 * v 0 + v 1 * v 1 + v 2 * v 2 + v 3 * v 3

theorem sq_nonneg (x : Rat) : 0 ≤ x * x := by
  by_cases h : 0 ≤ x
  · exact Rat.mul_nonneg h h
  · have h' : 0 ≤ -x := by grind
    have := Rat.mul_nonneg h' h'
    grind

/-- DP-9: the quadratic form of `Bs` is at most `2|v|²` (the operator bound
`Bs ≤ 2I`, so `B = r·Bs ≤ 2r`). -/
theorem bs_quad_le (v : Nat → Rat) : quad4 bsTable v ≤ 2 * normSq4 v := by
  unfold quad4 normSq4 bsTable
  have h1 := sq_nonneg (v 0 - v 3)
  have h2 := sq_nonneg (v 1 - v 2)
  have h3 := sq_nonneg (v 1)
  have h4 := sq_nonneg (v 2)
  grind

/-- The vector `(1,0,0,1)`. -/
def bellVec : Nat → Rat
  | 0 => 1 | 3 => 1 | _ => 0

/-- DP-9: equality at `v = (1,0,0,1)`: `vᵀBs v = 4 = 2|v|²`, i.e.
`Tr(2ρ·Bs) = 4` for `ρ = vvᵀ/2`. -/
theorem bs_quad_bell : quad4 bsTable bellVec = 4 ∧ normSq4 bellVec = 2 := by
  unfold quad4 normSq4 bsTable bellVec
  constructor <;> grind

/-- `±1` sign of a Boolean outcome. -/
def sgn (b : Bool) : Int := if b then 1 else -1

/-- DP-9: every deterministic CHSH value is `2` or `-2`. -/
theorem deterministic_chsh :
    ∀ a0 a1 b0 b1 : Bool,
      sgn a0 * sgn b0 + sgn a0 * sgn b1 + sgn a1 * sgn b0 - sgn a1 * sgn b1 = 2 ∨
      sgn a0 * sgn b0 + sgn a0 * sgn b1 + sgn a1 * sgn b0 - sgn a1 * sgn b1 = -2 := by
  decide

/-- DP-9: no deterministic assignment satisfies the PR-box relation
`a(x) xor b(y) = x and y` on all four inputs. -/
theorem pr_box_not_deterministic :
    ∀ a0 a1 b0 b1 : Bool,
      ¬ ((a0 ^^ b0) = (false && false) ∧ (a0 ^^ b1) = (false && true) ∧
         (a1 ^^ b0) = (true && false) ∧ (a1 ^^ b1) = (true && true)) := by
  decide

/-! ## DP-8: separating controls -/

/-- The transpose Choi matrix on dimension two (the swap). -/
def choiTranspose : Nat → Nat → Int
  | 0, 0 => 1 | 1, 2 => 1 | 2, 1 => 1 | 3, 3 => 1
  | _, _ => 0

/-- The vector `(0,1,-1,0)`. -/
def swapVec : Nat → Rat
  | 1 => 1 | 2 => -1 | _ => 0

/-- DP-8: `vᵀ J_T v = -2`, so the transpose map is not completely
positive. -/
theorem choi_transpose_negative : quad4 choiTranspose swapVec = -2 := by
  unfold quad4 choiTranspose swapVec
  grind

/-- DP-8: `J_T` is symmetric and its trace over the output factor is `I₂`
(entries `J[2i+r][2j+r]` summed over `r`). -/
theorem choi_transpose_tp :
    M4.Eq (transpose4 choiTranspose) choiTranspose ∧
      (∀ i, i < 2 → ∀ j, j < 2 →
        choiTranspose (2 * i) (2 * j) + choiTranspose (2 * i + 1) (2 * j + 1) =
          if i = j then 1 else 0) := by
  decide

/-- DP-8 leading-minor trap: `diag(0,2,-1)` has trace one, leading minors
`0, 0, 0`, and value `-1` on `e3`. -/
theorem leading_minor_trap :
    (0 : Int) + 2 + -1 = 1 ∧ (0 : Int) = 0 ∧ (0 : Int) * 2 = 0 ∧
      (0 : Int) * 2 * -1 = 0 ∧ (1 : Int) * -1 * 1 = -1 := by
  decide

/-- The integer matrix `H` of the report. -/
def kraussH : Nat → Nat → Int
  | 0, 0 => 1 | 0, 1 => -1 | 0, 2 => -1 | 0, 3 => 0
  | 1, 0 => 1 | 1, 1 => 1 | 1, 2 => 0 | 1, 3 => 1
  | 2, 0 => 1 | 2, 1 => 0 | 2, 2 => 1 | 2, 3 => -1
  | 3, 0 => 0 | 3, 1 => -1 | 3, 2 => 1 | 3, 3 => 1
  | _, _ => 0

/-- DP-8: `HᵀH = 3I₄`. -/
theorem kraus_h_orthogonal :
    M4.Eq (mul4 (transpose4 kraussH) kraussH) (smul4 3 one4) := by
  decide

/-- DP-8: three copies of `H/3` are complete: `3·(HᵀH)/9 = I` entrywise. -/
theorem three_copies_complete :
    ∀ i, i < 4 → ∀ j, j < 4 →
      (3 : Rat) * ((mul4 (transpose4 kraussH) kraussH i j : Int) : Rat) / 9 =
        ((one4 i j : Int) : Rat) := by
  intro i hi j hj
  have h := kraus_h_orthogonal i hi j hj
  rw [h]
  unfold smul4
  have : ((3 * one4 i j : Int) : Rat) = 3 * ((one4 i j : Int) : Rat) := by
    rw [Rat.intCast_mul]; rfl
  rw [this]
  grind

theorem sq_mod_three (n : Nat) : n * n % 3 = 0 ∨ n * n % 3 = 1 := by
  rw [Nat.mul_mod]
  have : n % 3 < 3 := Nat.mod_lt _ (by decide)
  match n % 3, this with
  | 0, _ => decide
  | 1, _ => decide
  | 2, _ => decide

theorem three_dvd_of_sq (n : Nat) (h : n * n % 3 = 0) : n % 3 = 0 := by
  rw [Nat.mul_mod] at h
  have : n % 3 < 3 := Nat.mod_lt _ (by decide)
  match hm : n % 3, this with
  | 0, _ => rfl
  | 1, _ => rw [hm] at h; contradiction
  | 2, _ => rw [hm] at h; contradiction

/-- DP-8: `3(a²+b²) = d²` forces `a = b = d = 0`. With `a, b, d` the absolute
values of a Gaussian-rational scalar `c = (a+ib)/d` written in lowest terms,
`|c|² = 1/3` has no solution, so the rank-one Choi matrix `vec(H)vec(H)ᵀ/3`
has no single Gaussian-rational Kraus operator. -/
theorem mod_three_descent :
    ∀ d a b : Nat, 3 * (a * a + b * b) = d * d → a = 0 ∧ b = 0 ∧ d = 0 := by
  intro d
  induction d using Nat.strongRecOn with
  | _ d ih =>
    intro a b h
    by_cases hd : d = 0
    · subst hd
      have ha : a * a = 0 := by omega
      have hb : b * b = 0 := by omega
      exact ⟨by rcases Nat.mul_eq_zero.mp ha with h | h <;> exact h,
        by rcases Nat.mul_eq_zero.mp hb with h | h <;> exact h, rfl⟩
    · have h1 : d * d % 3 = 0 := by omega
      have h2 := three_dvd_of_sq d h1
      obtain ⟨e, he⟩ : ∃ e, d = 3 * e := ⟨d / 3, by omega⟩
      subst he
      have h3 : a * a + b * b = 3 * (e * e) := by
        have : 3 * (a * a + b * b) = 3 * (3 * (e * e)) := by
          rw [h]; simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
        omega
      have ha := sq_mod_three a
      have hb := sq_mod_three b
      have ha0 : a * a % 3 = 0 := by omega
      have hb0 : b * b % 3 = 0 := by omega
      obtain ⟨a', rfl⟩ : ∃ a', a = 3 * a' :=
        ⟨a / 3, by have := three_dvd_of_sq a ha0; omega⟩
      obtain ⟨b', rfl⟩ : ∃ b', b = 3 * b' :=
        ⟨b / 3, by have := three_dvd_of_sq b hb0; omega⟩
      have h4 : 3 * (a' * a' + b' * b') = e * e := by
        have : 9 * (3 * (a' * a' + b' * b')) = 9 * (e * e) := by
          have := h3; grind
        omega
      have hlt : e < 3 * e := by omega
      obtain ⟨_, _, _⟩ := ih e hlt a' b' h4
      exact ⟨by omega, by omega, by omega⟩

/-! ## DP-7: exact envelope algebra -/

/-- DP-7: `4k(k+1) ≤ 6k²` for `k ≥ 2`. -/
theorem coefficient_relax (k : Nat) (hk : 2 ≤ k) : 4 * k * (k + 1) ≤ 6 * k * k := by
  have : 2 * k ≤ k * k := Nat.mul_le_mul_right k hk
  grind

/-- DP-7: the comparison holds exactly for `k = 0` or `k ≥ 2`. -/
theorem coefficient_relax_iff (k : Nat) :
    4 * k * (k + 1) ≤ 6 * k * k ↔ k = 0 ∨ 2 ≤ k := by
  constructor
  · intro h
    apply Classical.byContradiction
    intro hn
    have hk : k = 1 := by omega
    subst hk
    exact absurd h (by decide)
  · rintro (rfl | hk)
    · decide
    · exact coefficient_relax k hk

/-- DP-7: the comparison fails at `k = 1` (`8 > 6`). -/
theorem coefficient_relax_fails_at_one : ¬ (4 * 1 * (1 + 1) ≤ 6 * 1 * 1) := by
  decide

/-- DP-7: on `0 ≤ t`, `2ct ≤ ν`, the envelope `νt - ct²` is at least
`νt/2`. -/
theorem half_slope_window (ν c t : Rat) (ht : 0 ≤ t) (hw : 2 * c * t ≤ ν) :
    ν * t / 2 ≤ ν * t - c * t * t := by
  have := Rat.mul_nonneg ht (show 0 ≤ ν - 2 * c * t by grind)
  grind

/-- DP-7: the envelope is monotone on `s ≤ t`, `2ct ≤ ν` (in particular on
the window `0 ≤ s ≤ t`). -/
theorem envelope_monotone (ν c s t : Rat) (hc : 0 ≤ c) (hst : s ≤ t)
    (hw : 2 * c * t ≤ ν) : ν * s - c * s * s ≤ ν * t - c * t * t := by
  have h1 : c * s ≤ c * t := Rat.mul_le_mul_of_nonneg_left hst hc
  have h2 := Rat.mul_nonneg (show 0 ≤ t - s by grind)
    (show 0 ≤ ν - c * t - c * s by grind)
  grind

/-- DP-7: the weak envelope at its vertex `t* = ν/(2c)` equals `ν t*/2`
(here with `c t* = ν/2` as hypothesis). -/
theorem vertex_value (ν c t : Rat) (hv : 2 * c * t = ν) :
    ν * t - c * t * t = ν * t / 2 := by
  have : c * t * t = (ν / 2) * t := by
    have : c * t = ν / 2 := by grind
    rw [this]
  grind

/-- DP-7: coefficient relaxation under certified bounds `0 ≤ g² ≤ G²` and
`0 ≤ K₁ ≤ K₂`: `νt - K₁g²t² ≥ νt - K₂G²t²`. -/
theorem envelope_relax (ν t K₁ K₂ g2 G2 : Rat) (hK₁ : 0 ≤ K₁) (hK : K₁ ≤ K₂)
    (hg : 0 ≤ g2) (hG : g2 ≤ G2) :
    ν * t - K₂ * G2 * (t * t) ≤ ν * t - K₁ * g2 * (t * t) := by
  have hK₂ : 0 ≤ K₂ := by grind
  have h1 : K₁ * g2 ≤ K₂ * g2 := by
    have := Rat.mul_le_mul_of_nonneg_left hK hg
    grind
  have h2 : K₂ * g2 ≤ K₂ * G2 := Rat.mul_le_mul_of_nonneg_left hG hK₂
  have htt := sq_nonneg t
  have h3 := Rat.mul_le_mul_of_nonneg_left (show K₁ * g2 ≤ K₂ * G2 by grind) htt
  grind

/-- DP-7 replay, `k = 2`, `ν = 2`, `G = 1`, `t = 1/100`: coefficient `24`,
value `11/625`; the vertex is `1/24`. -/
theorem replay_k2 : (2 : Rat) * (1 / 100) - 24 * (1 / 100) * (1 / 100) = 11 / 625 ∧
    (6 * 2 * 2 : Nat) = 24 ∧ (4 * 2 * (2 + 1) : Nat) = 24 ∧
    2 * (12 : Rat) * (1 / 24) = 1 := by
  refine ⟨?_, by decide, by decide, ?_⟩ <;> grind

/-- DP-7 replay, `k = 3`, `ν = 2`, `G = 1`, `t = 1/200`: weak coefficient `54`
gives `173/20000`, strong coefficient `48` gives `11/1250`. -/
theorem replay_k3 :
    (2 : Rat) * (1 / 200) - 54 * (1 / 200) * (1 / 200) = 173 / 20000 ∧
      (2 : Rat) * (1 / 200) - 48 * (1 / 200) * (1 / 200) = 11 / 1250 ∧
      (6 * 3 * 3 : Nat) = 54 ∧ (4 * 3 * (3 + 1) : Nat) = 48 := by
  refine ⟨?_, ?_, by decide, by decide⟩ <;> grind

/-- DP-7: the rational sine enclosure at `x = 1/50`: the lower value
`x - x³/6 = 14999/750000` exceeds `11/625 = 13200/750000`. The enclosure
`x - x³/6 ≤ sin x` itself is an analytic residual. -/
theorem sine_enclosure_comparison :
    (1 / 50 : Rat) - (1 / 50) * (1 / 50) * (1 / 50) / 6 = 14999 / 750000 ∧
      (11 / 625 : Rat) = 13200 / 750000 ∧ (13200 / 750000 : Rat) < 14999 / 750000 := by
  refine ⟨?_, ?_, ?_⟩ <;> grind

/-- `H = X⊗X + 100·(Z⊗I)` from the DP-7 full-incident-norm control. -/
def fieldControlH : M4 := add4 (kron pauliX pauliX) (smul4 100 (kron pauliZ M2.one))

/-- DP-7 control: `H² = 10001·I` (the terms anticommute). -/
theorem field_control_square :
    M4.Eq (mul4 fieldControlH fieldControlH) (smul4 10001 one4) := by
  decide

/-- DP-7 control: `9999² + 200² = 10001²` normalizes the correlated
Gaussian-rational vector exactly. -/
theorem correlated_control_normalization :
    9999 * 9999 + 200 * 200 = (10001 * 10001 : Nat) := by
  decide

/-- DP-7 control: the time-dependent return time `ε = 1/100` has
`2ε - 24ε² = 11/625 > 0`, inside the window `ε < 1/24`. -/
theorem time_dependent_control :
    (2 : Rat) * (1 / 100) - 24 * (1 / 100) * (1 / 100) = 11 / 625 ∧
      (0 : Rat) < 11 / 625 ∧ (1 / 100 : Rat) < 1 / 24 := by
  refine ⟨?_, ?_, ?_⟩ <;> grind

end WitnessedDifference.ComponentQuantum
