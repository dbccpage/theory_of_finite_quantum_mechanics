import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
# `DFM-HIERARCHICAL-BOREL`: rooted-tree two-stage Borel dressing

AuthorityEffect: None.

The diamond control fixes five edges. This module states the same B₂(ℚ) = T ⋉ N
identities for every rooted tree given by a parent map and a strictly decreasing
depth, and the incidence curvature identities for the operators
`(bA)(u,_,_,w) = -A(u,w)` and `(A ⌣ A)(u,v,w) = A(u,v) * A(v,w)`.
The cochain is extra data: `RootedTree` has no cochain field.
-/

namespace DressingFieldHierarchicalBorel

/-- Upper-triangular matrix `[[d1, b], [0, d2]]` over ℚ. -/
@[ext]
structure UpperTri2 where
  d1 : ℚ
  b  : ℚ
  d2 : ℚ
  deriving DecidableEq, Repr

namespace UpperTri2

instance : Mul UpperTri2 where
  mul x y := ⟨x.d1 * y.d1, x.d1 * y.b + x.b * y.d2, x.d2 * y.d2⟩

instance : One UpperTri2 where
  one := ⟨1, 0, 1⟩

@[simp] theorem mul_d1 (x y : UpperTri2) : (x * y).d1 = x.d1 * y.d1 := rfl
@[simp] theorem mul_b (x y : UpperTri2) : (x * y).b = x.d1 * y.b + x.b * y.d2 := rfl
@[simp] theorem mul_d2 (x y : UpperTri2) : (x * y).d2 = x.d2 * y.d2 := rfl
@[simp] theorem one_d1 : (1 : UpperTri2).d1 = 1 := rfl
@[simp] theorem one_b : (1 : UpperTri2).b = 0 := rfl
@[simp] theorem one_d2 : (1 : UpperTri2).d2 = 1 := rfl

theorem mul_assoc (x y z : UpperTri2) : (x * y) * z = x * (y * z) := by
  ext <;> dsimp <;> ring

theorem one_mul (x : UpperTri2) : 1 * x = x := by
  ext <;> dsimp <;> ring

theorem mul_one (x : UpperTri2) : x * 1 = x := by
  ext <;> dsimp <;> ring

lemma mul_sandwich_assoc (A B C D E : UpperTri2) :
    A * (B * C * D) * E = (A * B) * C * (D * E) := by
  ext <;> dsimp <;> ring

def IsInvertible (x : UpperTri2) : Prop := x.d1 ≠ 0 ∧ x.d2 ≠ 0

def inv (x : UpperTri2) : UpperTri2 :=
  ⟨x.d1⁻¹, -x.b / (x.d1 * x.d2), x.d2⁻¹⟩

theorem mul_inv_cancel (x : UpperTri2) (h : IsInvertible x) : x * inv x = 1 := by
  rcases h with ⟨hd1, hd2⟩
  ext
  · rw [mul_d1]; dsimp [inv]; exact mul_inv_cancel₀ hd1
  · rw [mul_b]; dsimp [inv]
    have h1 : x.d1 * (-x.b / (x.d1 * x.d2)) = -x.b / x.d2 := by
      calc x.d1 * (-x.b / (x.d1 * x.d2))
        _ = (x.d1 * (-x.b)) / (x.d1 * x.d2) := by ring
        _ = (-x.b) / x.d2 := mul_div_mul_left (-x.b) x.d2 hd1
        _ = -x.b / x.d2 := rfl
    rw [h1]
    have h2 : x.b * x.d2⁻¹ = x.b / x.d2 := by ring
    rw [h2]
    ring
  · rw [mul_d2]; dsimp [inv]; exact mul_inv_cancel₀ hd2

theorem inv_mul_cancel (x : UpperTri2) (h : IsInvertible x) : inv x * x = 1 := by
  rcases h with ⟨hd1, hd2⟩
  ext
  · rw [mul_d1]; dsimp [inv]; exact inv_mul_cancel₀ hd1
  · rw [mul_b]; dsimp [inv]
    have h1 : (-x.b / (x.d1 * x.d2)) * x.d2 = -x.b / x.d1 := by
      calc (-x.b / (x.d1 * x.d2)) * x.d2
        _ = (-x.b * x.d2) / (x.d1 * x.d2) := by ring
        _ = (-x.b) / x.d1 := mul_div_mul_right (-x.b) x.d1 hd2
        _ = -x.b / x.d1 := rfl
    rw [h1]
    have h2 : x.d1⁻¹ * x.b = x.b / x.d1 := by ring
    rw [h2]
    ring
  · rw [mul_d2]; dsimp [inv]; exact inv_mul_cancel₀ hd2

theorem inv_isInvertible (x : UpperTri2) (h : IsInvertible x) : IsInvertible (inv x) := by
  constructor
  · exact inv_ne_zero h.1
  · exact inv_ne_zero h.2

theorem one_isInvertible : IsInvertible (1 : UpperTri2) := by
  dsimp [IsInvertible]
  norm_num

theorem mul_isInvertible (x y : UpperTri2) (hx : IsInvertible x) (hy : IsInvertible y) :
    IsInvertible (x * y) :=
  ⟨mul_ne_zero hx.1 hy.1, mul_ne_zero hx.2 hy.2⟩

theorem mul_right_cancel (a b c : UpperTri2) (hc : IsInvertible c) (h : a * c = b * c) : a = b := by
  have h1 : a * c * inv c = b * c * inv c := congrArg (fun x => x * inv c) h
  rw [mul_assoc, mul_assoc] at h1
  rw [mul_inv_cancel c hc, mul_one, mul_one] at h1
  exact h1

theorem inv_mul_rev (x y : UpperTri2) (hx : IsInvertible x) (hy : IsInvertible y) :
    inv (x * y) = inv y * inv x := by
  apply mul_right_cancel (inv (x * y)) (inv y * inv x) (x * y) (mul_isInvertible x y hx hy)
  rw [inv_mul_cancel (x * y) (mul_isInvertible x y hx hy)]
  symm
  calc inv y * inv x * (x * y)
    _ = inv y * (inv x * (x * y)) := by rw [mul_assoc]
    _ = inv y * ((inv x * x) * y) := by rw [← mul_assoc (inv x) x y]
    _ = inv y * ((1 : UpperTri2) * y) := by rw [inv_mul_cancel x hx]
    _ = inv y * y := by rw [one_mul]
    _ = 1 := inv_mul_cancel y hy

/-- `(a * c⁻¹) * (c * b) = a * b`. -/
theorem mul_inv_cancel_middle (a b c : UpperTri2) (hc : IsInvertible c) :
    (a * inv c) * (c * b) = a * b := by
  calc (a * inv c) * (c * b)
    _ = a * (inv c * (c * b)) := by rw [mul_assoc]
    _ = a * ((inv c * c) * b) := by rw [← mul_assoc (inv c) c b]
    _ = a * ((1 : UpperTri2) * b) := by rw [inv_mul_cancel c hc]
    _ = a * b := by rw [one_mul]

/-- `(a * b⁻¹) * b = a`. -/
theorem mul_inv_right_cancel (a b : UpperTri2) (hb : IsInvertible b) :
    (a * inv b) * b = a := by
  calc (a * inv b) * b
    _ = a * (inv b * b) := by rw [← mul_assoc]
    _ = a * 1 := by rw [inv_mul_cancel b hb]
    _ = a := mul_one a

/-- `a * (a⁻¹ * g * b) = g * b`. -/
theorem left_inv_mul_cancel_right (a g b : UpperTri2) (ha : IsInvertible a) :
    a * (inv a * g * b) = g * b := by
  calc a * (inv a * g * b)
    _ = (a * (inv a * g)) * b := by rw [← mul_assoc]
    _ = ((a * inv a) * g) * b := by rw [← mul_assoc]
    _ = ((1 : UpperTri2) * g) * b := by rw [mul_inv_cancel a ha]
    _ = g * b := by rw [one_mul]

/-- `a⁻¹ * (a * b⁻¹) * b = 1`. -/
theorem inv_mul_mul_inv_mul (a b : UpperTri2) (ha : IsInvertible a) (hb : IsInvertible b) :
    inv a * (a * inv b) * b = 1 := by
  calc inv a * (a * inv b) * b
    _ = ((inv a * a) * inv b) * b := by rw [← mul_assoc]
    _ = ((1 : UpperTri2) * inv b) * b := by rw [inv_mul_cancel a ha]
    _ = (1 : UpperTri2) * (inv b * b) := by rw [mul_assoc]
    _ = (1 : UpperTri2) * 1 := by rw [inv_mul_cancel b hb]
    _ = 1 := by rw [one_mul]

theorem inv_inv (x : UpperTri2) (hx : IsInvertible x) : inv (inv x) = x := by
  apply mul_right_cancel (inv (inv x)) x (inv x) (inv_isInvertible x hx)
  rw [inv_mul_cancel (inv x) (inv_isInvertible x hx), mul_inv_cancel x hx]

def IsTorus (x : UpperTri2) : Prop := x.b = 0

def IsUnipotent (x : UpperTri2) : Prop := x.d1 = 1 ∧ x.d2 = 1

def torusProj (x : UpperTri2) : UpperTri2 := ⟨x.d1, 0, x.d2⟩

def unipotentPart (x : UpperTri2) : UpperTri2 := ⟨1, x.b / x.d1, 1⟩

theorem torusProj_isTorus (x : UpperTri2) : IsTorus (torusProj x) := rfl

theorem torusProj_isInvertible (x : UpperTri2) (h : IsInvertible x) : IsInvertible (torusProj x) := h

theorem unipotentPart_isUnipotent (x : UpperTri2) : IsUnipotent (unipotentPart x) := ⟨rfl, rfl⟩

theorem unipotentPart_isInvertible (x : UpperTri2) : IsInvertible (unipotentPart x) := by
  dsimp [IsInvertible, unipotentPart]
  norm_num

theorem torus_mul_torus (x y : UpperTri2) (hx : IsTorus x) (hy : IsTorus y) : IsTorus (x * y) := by
  dsimp [IsTorus] at *
  calc (x * y).b = x.d1 * y.b + x.b * y.d2 := rfl
    _ = x.d1 * 0 + 0 * y.d2 := by rw [hx, hy]
    _ = 0 := by ring

theorem torus_inv (x : UpperTri2) (hx : IsTorus x) : IsTorus (inv x) := by
  dsimp [IsTorus] at *
  dsimp [inv]
  rw [hx]
  ring

theorem torusProj_mul (x y : UpperTri2) : torusProj (x * y) = torusProj x * torusProj y := by
  ext <;> dsimp [torusProj] <;> ring

theorem b2_semidirect_factorization (x : UpperTri2) (h : IsInvertible x) :
    x = torusProj x * unipotentPart x := by
  ext
  · rw [mul_d1]; dsimp [torusProj, unipotentPart]; ring
  · rw [mul_b]; dsimp [torusProj, unipotentPart]
    have : x.d1 * (x.b / x.d1) + 0 * 1 = x.b := by
      rw [zero_mul, add_zero, mul_div_cancel₀ _ h.1]
    exact this.symm
  · rw [mul_d2]; dsimp [torusProj, unipotentPart]; ring

theorem b2_factorization_unique (x D n : UpperTri2) (hD : IsTorus D) (hn : IsUnipotent n)
    (h_prod : x = D * n) (hx : IsInvertible x) :
    D = torusProj x ∧ n = unipotentPart x := by
  have hd1 : x.d1 = D.d1 * n.d1 := by rw [h_prod, mul_d1]
  have h_b : x.b = D.d1 * n.b + D.b * n.d2 := by rw [h_prod, mul_b]
  have hd2 : x.d2 = D.d2 * n.d2 := by rw [h_prod, mul_d2]
  rcases hn with ⟨hn1, hn2⟩
  have hd1_eq : D.d1 * n.d1 = D.d1 := by rw [hn1, _root_.mul_one]
  have hd2_eq : D.d2 * n.d2 = D.d2 := by rw [hn2, _root_.mul_one]
  rw [hd1_eq] at hd1
  rw [hd2_eq] at hd2
  rw [hD, zero_mul, add_zero] at h_b
  constructor
  · ext
    · exact hd1.symm
    · dsimp [torusProj]; exact hD
    · exact hd2.symm
  · ext
    · dsimp [unipotentPart]; exact hn1
    · dsimp [unipotentPart]
      rw [← hd1] at h_b
      calc n.b = (x.d1 * n.b) / x.d1 := (mul_div_cancel_left₀ n.b hx.1).symm
        _ = x.b / x.d1 := by rw [← h_b]
    · dsimp [unipotentPart]; exact hn2

theorem unipotent_subgroup_normal (M n : UpperTri2) (hM : IsInvertible M) (hn : IsUnipotent n) :
    IsUnipotent (M * n * inv M) := by
  rcases hn with ⟨hn1, hn2⟩
  constructor
  · rw [mul_d1, mul_d1]; dsimp [inv]
    calc M.d1 * n.d1 * M.d1⁻¹ = M.d1 * 1 * M.d1⁻¹ := by rw [hn1]
      _ = M.d1 * M.d1⁻¹ := by ring
      _ = 1 := mul_inv_cancel₀ hM.1
  · rw [mul_d2, mul_d2]; dsimp [inv]
    calc M.d2 * n.d2 * M.d2⁻¹ = M.d2 * 1 * M.d2⁻¹ := by rw [hn2]
      _ = M.d2 * M.d2⁻¹ := by ring
      _ = 1 := mul_inv_cancel₀ hM.2

theorem inv_unipotent (x : UpperTri2) (hx : IsUnipotent x) : inv x = ⟨1, -x.b, 1⟩ := by
  rcases hx with ⟨h1, h2⟩
  ext
  · dsimp [inv]; rw [h1]; norm_num
  · dsimp [inv]; rw [h1, h2]; ring
  · dsimp [inv]; rw [h2]; norm_num

theorem torusProj_unipotent_invariance (M u1 u2 : UpperTri2)
    (hu1 : IsUnipotent u1) (hu2 : IsUnipotent u2) :
    torusProj (u1 * M * u2) = torusProj M := by
  rcases hu1 with ⟨hu1_d1, hu1_d2⟩
  rcases hu2 with ⟨hu2_d1, hu2_d2⟩
  ext
  · rw [torusProj, torusProj, mul_d1, mul_d1]
    calc u1.d1 * M.d1 * u2.d1 = 1 * M.d1 * 1 := by rw [hu1_d1, hu2_d1]
      _ = M.d1 := by ring
  · rfl
  · rw [torusProj, torusProj, mul_d2, mul_d2]
    calc u1.d2 * M.d2 * u2.d2 = 1 * M.d2 * 1 := by rw [hu1_d2, hu2_d2]
      _ = M.d2 := by ring

/-- Replacing the bottom-right entry by 1 does not preserve multiplication. -/
def badProj (x : UpperTri2) : UpperTri2 := ⟨x.d1, x.b, 1⟩

theorem badProj_not_homomorphism :
    badProj (⟨2, 1, 3⟩ * ⟨2, 1, 3⟩) ≠ badProj ⟨2, 1, 3⟩ * badProj ⟨2, 1, 3⟩ := by
  intro h
  have hb := congrArg UpperTri2.b h
  simp [badProj, mul_b] at hb

/-- The right factorization identity fails for `[[0, 1], [0, 1]]`. -/
theorem factorization_fails_if_singular :
    (⟨0, 1, 1⟩ : UpperTri2) ≠ torusProj ⟨0, 1, 1⟩ * unipotentPart ⟨0, 1, 1⟩ := by
  intro h
  have hb := congrArg UpperTri2.b h
  simp [torusProj, unipotentPart, mul_b] at hb

end UpperTri2

/-!
### Rooted trees

A rooted tree is a parent pointer whose depth strictly decreases off the root.
Tree labels are read on the left: the transport at a non-root vertex is
`U(v) * transport(parent v)`.
-/

structure RootedTree (V : Type) where
  root : V
  parent : V → V
  depth : V → ℕ
  parent_root : parent root = root
  depth_root : depth root = 0
  depth_step : ∀ v, v ≠ root → depth (parent v) < depth v

variable {V : Type}

open UpperTri2

/-!
Equality of an arbitrary vertex with the root is decided by `Classical.propDecidable`.
The resulting transport is noncomputable. `Classical.choice` is an allowed axiom.
-/
noncomputable section
attribute [local instance] Classical.propDecidable

def transportFuel (T : RootedTree V) (U : V → UpperTri2) : ℕ → V → UpperTri2
  | 0, _ => 1
  | n + 1, v => if v = T.root then 1 else U v * transportFuel T U n (T.parent v)

def treeTransport (T : RootedTree V) (U : V → UpperTri2) (v : V) : UpperTri2 :=
  transportFuel T U (T.depth v) v

theorem transportFuel_zero (T : RootedTree V) (U : V → UpperTri2) (v : V) :
    transportFuel T U 0 v = 1 := rfl

theorem transportFuel_succ_root (T : RootedTree V) (U : V → UpperTri2) (n : ℕ) :
    transportFuel T U (n + 1) T.root = 1 := by
  conv_lhs => unfold transportFuel
  rw [ite_eq_left rfl]

theorem transportFuel_succ_of_ne (T : RootedTree V) (U : V → UpperTri2) (n : ℕ) (v : V)
    (hv : v ≠ T.root) :
    transportFuel T U (n + 1) v = U v * transportFuel T U n (T.parent v) := by
  conv_lhs => unfold transportFuel
  rw [ite_eq_right hv]

theorem depth_zero_root (T : RootedTree V) {v : V} (h : T.depth v = 0) : v = T.root := by
  by_contra hv
  have hlt := T.depth_step v hv
  rw [h] at hlt
  exact Nat.not_lt_zero _ hlt

theorem treeTransport_root (T : RootedTree V) (U : V → UpperTri2) :
    treeTransport T U T.root = 1 := by
  unfold treeTransport
  rw [T.depth_root, transportFuel_zero]

/-- Extra fuel does not change transport once it meets the depth. -/
theorem transportFuel_stable (T : RootedTree V) (U : V → UpperTri2) :
    ∀ n k v, k ≤ n → T.depth v ≤ k →
      transportFuel T U k v = transportFuel T U (T.depth v) v := by
  intro n
  induction n with
  | zero =>
      intro k v hk hdepth
      have hk0 : k = 0 := Nat.eq_zero_of_le_zero hk
      subst hk0
      have hd0 : T.depth v = 0 := Nat.eq_zero_of_le_zero hdepth
      rw [hd0]
  | succ n ih =>
      intro k v hk hdepth
      by_cases hkn : k ≤ n
      · exact ih k v hkn hdepth
      · have hkEq : k = n + 1 :=
          Nat.le_antisymm hk (Nat.succ_le_of_lt ((Nat.not_le).mp hkn))
        subst hkEq
        by_cases hv : v = T.root
        · subst hv
          rw [T.depth_root, transportFuel_zero, transportFuel_succ_root]
        · have hltp := T.depth_step v hv
          cases hd : T.depth v with
          | zero => exact absurd (depth_zero_root T hd) hv
          | succ d =>
              have hdn : d ≤ n := by
                have hsucc : d + 1 ≤ n + 1 := by simpa [hd] using hdepth
                exact Nat.le_of_succ_le_succ hsucc
              rw [transportFuel_succ_of_ne T U n v hv]
              rw [transportFuel_succ_of_ne T U d v hv]
              congr 1
              have hp : T.depth (T.parent v) ≤ d := by
                have : T.depth (T.parent v) < d + 1 := by simpa [hd] using hltp
                exact Nat.le_of_lt_succ this
              have hpn : T.depth (T.parent v) ≤ n := Nat.le_trans hp hdn
              rw [ih n (T.parent v) (Nat.le_refl n) hpn]
              exact (ih d (T.parent v) hdn hp).symm

theorem transportFuel_of_le (T : RootedTree V) (U : V → UpperTri2) (v : V) (n : ℕ)
    (h : T.depth v ≤ n) :
    transportFuel T U n v = transportFuel T U (T.depth v) v :=
  transportFuel_stable T U n n v (Nat.le_refl n) h

theorem treeTransport_step (T : RootedTree V) (U : V → UpperTri2) (v : V) (hv : v ≠ T.root) :
    treeTransport T U v = U v * treeTransport T U (T.parent v) := by
  have hlt := T.depth_step v hv
  unfold treeTransport
  cases hdepth : T.depth v with
  | zero => exact absurd (depth_zero_root T hdepth) hv
  | succ d =>
      rw [transportFuel_succ_of_ne T U d v hv]
      congr 1
      have hp : T.depth (T.parent v) ≤ d := by
        have : T.depth (T.parent v) < d + 1 := by simpa [hdepth] using hlt
        exact Nat.le_of_lt_succ this
      exact transportFuel_of_le T U (T.parent v) d hp

theorem treeTransport_invertible (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) :
    IsInvertible (treeTransport T U v) := by
  suffices ∀ n v, T.depth v ≤ n → IsInvertible (treeTransport T U v) from
    this (T.depth v) v (Nat.le_refl _)
  intro n
  induction n with
  | zero =>
      intro v hv
      have hz : T.depth v = 0 := Nat.eq_zero_of_le_zero hv
      have hr := depth_zero_root T hz
      subst hr
      rw [treeTransport_root]
      exact one_isInvertible
  | succ n ih =>
      intro v hv
      by_cases hr : v = T.root
      · subst hr
        rw [treeTransport_root]
        exact one_isInvertible
      · rw [treeTransport_step T U v hr]
        have hp : T.depth (T.parent v) ≤ n :=
          Nat.le_of_lt_succ (Nat.lt_of_lt_of_le (T.depth_step v hr) hv)
        exact mul_isInvertible (U v) (treeTransport T U (T.parent v)) (hU v hr)
          (ih (T.parent v) hp)

def D_tree (T : RootedTree V) (U : V → UpperTri2) (v : V) : UpperTri2 :=
  torusProj (treeTransport T U v)

/-- Stage-one field, the matrix `[[1, -b(v)/d2(v)], [0, 1]]`. -/
def u_N (T : RootedTree V) (U : V → UpperTri2) (v : V) : UpperTri2 :=
  ⟨1, -(treeTransport T U v).b / (treeTransport T U v).d2, 1⟩

def u_T (T : RootedTree V) (U : V → UpperTri2) (v : V) : UpperTri2 :=
  inv (D_tree T U v)

theorem u_N_isUnipotent (T : RootedTree V) (U : V → UpperTri2) (v : V) :
    IsUnipotent (u_N T U v) := ⟨rfl, rfl⟩

theorem u_N_isInvertible (T : RootedTree V) (U : V → UpperTri2) (v : V) :
    IsInvertible (u_N T U v) := by
  dsimp [IsInvertible, u_N]
  norm_num

theorem inv_u_N_isUnipotent (T : RootedTree V) (U : V → UpperTri2) (v : V) :
    IsUnipotent (inv (u_N T U v)) := by
  rw [inv_unipotent _ (u_N_isUnipotent T U v)]
  exact ⟨rfl, rfl⟩

theorem u_N_mul_treeTransport (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) :
    u_N T U v * treeTransport T U v = D_tree T U v := by
  have hd2 := (treeTransport_invertible T U hU v).2
  ext
  · rw [mul_d1]; dsimp [u_N, D_tree, torusProj]; ring
  · rw [mul_b]; dsimp [u_N, D_tree, torusProj]
    have : (-(treeTransport T U v).b / (treeTransport T U v).d2) * (treeTransport T U v).d2
        = -(treeTransport T U v).b := div_mul_cancel₀ _ hd2
    calc 1 * (treeTransport T U v).b
          + (-(treeTransport T U v).b / (treeTransport T U v).d2) * (treeTransport T U v).d2
      _ = (treeTransport T U v).b + -(treeTransport T U v).b := by rw [this, _root_.one_mul]
      _ = 0 := by ring
  · rw [mul_d2]; dsimp [u_N, D_tree, torusProj]; ring

theorem stage1_tree_edge (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) (hv : v ≠ T.root) :
    u_N T U v * U v * inv (u_N T U (T.parent v))
      = D_tree T U v * inv (D_tree T U (T.parent v)) := by
  set p := T.parent v
  have hstep : treeTransport T U v = U v * treeTransport T U p := treeTransport_step T U v hv
  have hDp : IsInvertible (D_tree T U p) :=
    torusProj_isInvertible _ (treeTransport_invertible T U hU p)
  apply mul_right_cancel _ _ (D_tree T U p) hDp
  nth_rw 1 [← u_N_mul_treeTransport T U hU p]
  nth_rw 2 [← u_N_mul_treeTransport T U hU p]
  conv_lhs =>
    rw [mul_inv_cancel_middle (u_N T U v * U v) (treeTransport T U p) (u_N T U p)
      (u_N_isInvertible T U p)]
    rw [UpperTri2.mul_assoc]
    rw [← hstep]
    rw [u_N_mul_treeTransport T U hU v]
  conv_rhs =>
    rw [u_N_mul_treeTransport T U hU p]
    rw [mul_inv_right_cancel (D_tree T U v) (D_tree T U p) hDp]

theorem stage1_preserves_quotient (T : RootedTree V) (U : V → UpperTri2)
    (g : UpperTri2) (s t : V) :
    torusProj (u_N T U t * g * inv (u_N T U s)) = torusProj g :=
  torusProj_unipotent_invariance g (u_N T U t) (inv (u_N T U s))
    (u_N_isUnipotent T U t) (inv_u_N_isUnipotent T U s)

theorem stage1_residual_torus (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v))
    (tfun : V → UpperTri2) (ht : ∀ v, IsTorus (tfun v))
    (v : V) (hv : v ≠ T.root) :
    IsTorus (tfun v * (u_N T U v * U v * inv (u_N T U (T.parent v)))
      * inv (tfun (T.parent v))) := by
  have hdiag : IsTorus (u_N T U v * U v * inv (u_N T U (T.parent v))) := by
    rw [stage1_tree_edge T U hU v hv]
    exact torus_mul_torus _ _ (torusProj_isTorus _) (torus_inv _ (torusProj_isTorus _))
  exact torus_mul_torus _ _ (torus_mul_torus _ _ (ht v) hdiag)
    (torus_inv _ (ht (T.parent v)))

theorem u_N_eq_D_mul_invTransport (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) :
    u_N T U v = D_tree T U v * inv (treeTransport T U v) := by
  apply mul_right_cancel _ _ (treeTransport T U v) (treeTransport_invertible T U hU v)
  rw [UpperTri2.mul_assoc]
  rw [inv_mul_cancel _ (treeTransport_invertible T U hU v)]
  rw [UpperTri2.mul_one]
  exact u_N_mul_treeTransport T U hU v

theorem u_N_eq_conjugate (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) :
    u_N T U v = torusProj (treeTransport T U v)
      * inv (unipotentPart (treeTransport T U v))
      * inv (torusProj (treeTransport T U v)) := by
  have ht := treeTransport_invertible T U hU v
  have hfac := b2_semidirect_factorization (treeTransport T U v) ht
  have hinv : inv (treeTransport T U v) =
      inv (unipotentPart (treeTransport T U v)) * inv (torusProj (treeTransport T U v)) := by
    conv_lhs => rw [hfac]
    exact inv_mul_rev (torusProj (treeTransport T U v)) (unipotentPart (treeTransport T U v))
      (torusProj_isInvertible _ ht) (unipotentPart_isInvertible _)
  rw [u_N_eq_D_mul_invTransport T U hU v, hinv, ← UpperTri2.mul_assoc]
  unfold D_tree
  rfl

theorem u_N_conjugate_in_N (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) :
    IsUnipotent (torusProj (treeTransport T U v)
      * inv (unipotentPart (treeTransport T U v))
      * inv (torusProj (treeTransport T U v))) := by
  rw [← u_N_eq_conjugate T U hU v]
  exact u_N_isUnipotent T U v

theorem u_T_isTorus (T : RootedTree V) (U : V → UpperTri2) (v : V) : IsTorus (u_T T U v) :=
  torus_inv _ (torusProj_isTorus _)

theorem u_T_isInvertible (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) : IsInvertible (u_T T U v) :=
  inv_isInvertible _ (torusProj_isInvertible _ (treeTransport_invertible T U hU v))

theorem two_stage_factorization (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) :
    u_T T U v * u_N T U v = inv (treeTransport T U v) := by
  rw [u_N_eq_D_mul_invTransport T U hU v]
  unfold u_T
  rw [← UpperTri2.mul_assoc]
  rw [inv_mul_cancel (D_tree T U v)
    (torusProj_isInvertible _ (treeTransport_invertible T U hU v))]
  rw [UpperTri2.one_mul]

theorem inv_u_N_mul_inv_u_T (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) :
    inv (u_N T U v) * inv (u_T T U v) = treeTransport T U v := by
  have hfac := two_stage_factorization T U hU v
  have hinv : inv (u_T T U v * u_N T U v) = treeTransport T U v := by
    rw [hfac, inv_inv _ (treeTransport_invertible T U hU v)]
  rw [inv_mul_rev (u_T T U v) (u_N T U v) (u_T_isInvertible T U hU v) (u_N_isInvertible T U v)] at hinv
  exact hinv

theorem stage2_reproduces (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (s t : V) (g : UpperTri2) :
    u_T T U t * (u_N T U t * g * inv (u_N T U s)) * inv (u_T T U s)
      = inv (treeTransport T U t) * g * treeTransport T U s := by
  rw [mul_sandwich_assoc]
  rw [two_stage_factorization T U hU t, inv_u_N_mul_inv_u_T T U hU s]

theorem tree_edge_is_coboundary (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (v : V) (hv : v ≠ T.root) :
    U v = treeTransport T U v * inv (treeTransport T U (T.parent v)) := by
  have hp := treeTransport_invertible T U hU (T.parent v)
  calc U v
    _ = U v * 1 := (UpperTri2.mul_one _).symm
    _ = U v * (treeTransport T U (T.parent v) * inv (treeTransport T U (T.parent v))) := by
        rw [mul_inv_cancel _ hp]
    _ = (U v * treeTransport T U (T.parent v)) * inv (treeTransport T U (T.parent v)) := by
        rw [← UpperTri2.mul_assoc]
    _ = treeTransport T U v * inv (treeTransport T U (T.parent v)) := by
        rw [← treeTransport_step T U v hv]

theorem dressed_one_iff (T : RootedTree V) (U : V → UpperTri2)
    (hU : ∀ v, v ≠ T.root → IsInvertible (U v)) (s t : V) (g : UpperTri2) :
    inv (treeTransport T U t) * g * treeTransport T U s = 1 ↔
      g = treeTransport T U t * inv (treeTransport T U s) := by
  constructor
  · intro h
    have ht := treeTransport_invertible T U hU t
    have hs := treeTransport_invertible T U hU s
    apply mul_right_cancel g (treeTransport T U t * inv (treeTransport T U s))
      (treeTransport T U s) hs
    have hbc : g * treeTransport T U s = treeTransport T U t := by
      have h1 : treeTransport T U t * (inv (treeTransport T U t) * g * treeTransport T U s)
          = treeTransport T U t := by
        rw [h, UpperTri2.mul_one]
      rw [left_inv_mul_cancel_right (treeTransport T U t) g (treeTransport T U s) ht] at h1
      exact h1
    rw [hbc]
    exact (mul_inv_right_cancel (treeTransport T U t) (treeTransport T U s) hs).symm
  · intro h
    have ht := treeTransport_invertible T U hU t
    have hs := treeTransport_invertible T U hU s
    rw [h]
    exact inv_mul_mul_inv_mul (treeTransport T U t) (treeTransport T U s) ht hs

theorem anchored_transport_unique (T : RootedTree V) (U g : V → UpperTri2)
    (hg : ∀ v, IsInvertible (g v))
    (hroot : g T.root = 1)
    (hedge : ∀ v, v ≠ T.root → U v = g v * inv (g (T.parent v)))
    (v : V) : g v = treeTransport T U v := by
  suffices ∀ n v, T.depth v ≤ n → g v = treeTransport T U v from
    this (T.depth v) v (Nat.le_refl _)
  intro n
  induction n with
  | zero =>
      intro v hv
      have hz : T.depth v = 0 := Nat.eq_zero_of_le_zero hv
      have hr := depth_zero_root T hz
      subst hr
      rw [hroot, treeTransport_root]
  | succ n ih =>
      intro v hv
      by_cases hr : v = T.root
      · subst hr
        rw [hroot, treeTransport_root]
      · have hp : T.depth (T.parent v) ≤ n :=
          Nat.le_of_lt_succ (Nat.lt_of_lt_of_le (T.depth_step v hr) hv)
        have ihp := ih (T.parent v) hp
        calc g v
          _ = g v * 1 := (UpperTri2.mul_one _).symm
          _ = g v * (inv (g (T.parent v)) * g (T.parent v)) := by
              rw [← inv_mul_cancel _ (hg (T.parent v))]
          _ = (g v * inv (g (T.parent v))) * g (T.parent v) := by rw [← UpperTri2.mul_assoc]
          _ = U v * g (T.parent v) := by rw [← hedge v hr]
          _ = U v * treeTransport T U (T.parent v) := by rw [ihp]
          _ = treeTransport T U v := by rw [← treeTransport_step T U v hr]

end

/-!
### Incidence operators

These operators are not fields of `RootedTree`. They are the specified differential
and cup product of the diamond control, stated for an arbitrary commutative ring.
-/

section PosetCurvature

variable {R : Type} [CommRing R]

def b1 (A : R → R → R) (u _ w : R) : R := - A u w

def cup11 (A : R → R → R) (u v w : R) : R := A u v * A v w

def curvature1 (A : R → R → R) (u v w : R) : R :=
  b1 A u v w + cup11 A u v w

theorem curvature_formula (A : R → R → R) (u v w : R) :
    curvature1 A u v w = A u v * A v w - A u w := by
  dsimp [curvature1, b1, cup11]
  ring

def b2 (K : R → R → R → R) (u v w z : R) : R :=
  - K u w z + K u v z

def cup12 (A : R → R → R) (K : R → R → R → R) (u v w z : R) : R :=
  A u v * K v w z

def cup21 (K : R → R → R → R) (A : R → R → R) (u v w z : R) : R :=
  K u v w * A w z

def covariantDiff2 (A : R → R → R) (K : R → R → R → R) (u v w z : R) : R :=
  b2 K u v w z + cup12 A K u v w z - cup21 K A u v w z

theorem b_squared_zero (A : R → R → R) (u v w z : R) :
    b2 (b1 A) u v w z = 0 := by
  dsimp [b2, b1]
  ring

theorem discrete_bianchi_identity (A : R → R → R) (u v w z : R) :
    covariantDiff2 A (curvature1 A) u v w z = 0 := by
  dsimp [covariantDiff2, b2, cup12, cup21, curvature1, b1, cup11]
  ring

theorem curvature_gauge_covariance (A : R → R → R) (g g_inv : R → R)
    (h_inv : ∀ v, g v * g_inv v = 1)
    (A_gauge : R → R → R)
    (hA : ∀ x y, A_gauge x y = g x * A x y * g_inv y)
    (u v w : R) :
    curvature1 A_gauge u v w = g u * curvature1 A u v w * g_inv w := by
  rw [curvature_formula, curvature_formula]
  rw [hA u v, hA v w, hA u w]
  have h1 : g u * A u v * g_inv v * (g v * A v w * g_inv w) =
      g u * (A u v * A v w) * g_inv w := by
    calc g u * A u v * g_inv v * (g v * A v w * g_inv w)
      _ = (g u * A u v * A v w * g_inv w) * (g v * g_inv v) := by ring
      _ = (g u * A u v * A v w * g_inv w) * 1 := by rw [h_inv v]
      _ = g u * (A u v * A v w) * g_inv w := by ring
  rw [h1]
  ring

end PosetCurvature

/-- Source-only multiplication with values `A01=1`, `A12=1`, `A02=0`, `g0=1`, `g1=2`
    does not reproduce left multiplication of the curvature by `g0`. -/
theorem source_only_dressing_breaks_curvature :
    ((1 : ℚ) * (1 : ℚ)) * ((2 : ℚ) * (1 : ℚ)) - ((1 : ℚ) * (0 : ℚ))
      ≠ (1 : ℚ) * ((1 : ℚ) * (1 : ℚ) - (0 : ℚ)) := by
  norm_num

/-- The same values, dressed on both endpoints with `g2 = 1` and `g1⁻¹ = 1/2`,
    do satisfy the endpoint covariance identity. -/
theorem endpoint_dressing_matches_curvature :
    (((1 : ℚ) * (1 : ℚ) * (2 : ℚ)⁻¹) * ((2 : ℚ) * (1 : ℚ) * (1 : ℚ))
        - ((1 : ℚ) * (0 : ℚ) * (1 : ℚ)))
      = (1 : ℚ) * ((1 : ℚ) * (1 : ℚ) - (0 : ℚ)) * (1 : ℚ) := by
  norm_num

/-- Arithmetic comparison of the matrix size 2 with 3. This declaration does not
    mention a color group. -/
theorem carrier_dimension_two_ne_three : (2 : ℕ) ≠ 3 := by
  decide

def diamondParent : Fin 4 → Fin 4
  | 0 => 0
  | 1 => 0
  | 2 => 0
  | 3 => 2

def diamondDepth : Fin 4 → ℕ
  | 0 => 0
  | 1 => 1
  | 2 => 1
  | 3 => 2

def diamondTree : RootedTree (Fin 4) where
  root := 0
  parent := diamondParent
  depth := diamondDepth
  parent_root := rfl
  depth_root := rfl
  depth_step := by
    intro v hv
    match v with
    | 0 => exact absurd rfl hv
    | 1 => decide
    | 2 => decide
    | 3 => decide

theorem diamond_transport_three (U : Fin 4 → UpperTri2) :
    treeTransport diamondTree U 3 = U 3 * U 2 := by
  rw [treeTransport_step diamondTree U 3 (by decide)]
  rw [show diamondTree.parent 3 = 2 from rfl]
  rw [treeTransport_step diamondTree U 2 (by decide)]
  rw [show diamondTree.parent 2 = 0 from rfl]
  rw [show treeTransport diamondTree U 0 = 1 from treeTransport_root diamondTree U]
  rw [UpperTri2.mul_one]

theorem diamond_stage1_vertex_three_diagonal (U : Fin 4 → UpperTri2)
    (hU : ∀ v, v ≠ (0 : Fin 4) → IsInvertible (U v)) :
    IsTorus (u_N diamondTree U 3 * U 3 * inv (u_N diamondTree U (diamondTree.parent 3))) := by
  rw [stage1_tree_edge diamondTree U hU 3 (by decide)]
  exact torus_mul_torus _ _ (torusProj_isTorus _) (torus_inv _ (torusProj_isTorus _))

end DressingFieldHierarchicalBorel

#print axioms DressingFieldHierarchicalBorel.UpperTri2.b2_semidirect_factorization
#print axioms DressingFieldHierarchicalBorel.UpperTri2.b2_factorization_unique
#print axioms DressingFieldHierarchicalBorel.UpperTri2.unipotent_subgroup_normal
#print axioms DressingFieldHierarchicalBorel.UpperTri2.torusProj_mul
#print axioms DressingFieldHierarchicalBorel.UpperTri2.badProj_not_homomorphism
#print axioms DressingFieldHierarchicalBorel.UpperTri2.factorization_fails_if_singular
#print axioms DressingFieldHierarchicalBorel.u_N_eq_conjugate
#print axioms DressingFieldHierarchicalBorel.u_N_conjugate_in_N
#print axioms DressingFieldHierarchicalBorel.stage1_tree_edge
#print axioms DressingFieldHierarchicalBorel.stage1_preserves_quotient
#print axioms DressingFieldHierarchicalBorel.stage1_residual_torus
#print axioms DressingFieldHierarchicalBorel.two_stage_factorization
#print axioms DressingFieldHierarchicalBorel.stage2_reproduces
#print axioms DressingFieldHierarchicalBorel.tree_edge_is_coboundary
#print axioms DressingFieldHierarchicalBorel.dressed_one_iff
#print axioms DressingFieldHierarchicalBorel.anchored_transport_unique
#print axioms DressingFieldHierarchicalBorel.b_squared_zero
#print axioms DressingFieldHierarchicalBorel.discrete_bianchi_identity
#print axioms DressingFieldHierarchicalBorel.curvature_gauge_covariance
#print axioms DressingFieldHierarchicalBorel.source_only_dressing_breaks_curvature
#print axioms DressingFieldHierarchicalBorel.endpoint_dressing_matches_curvature
#print axioms DressingFieldHierarchicalBorel.carrier_dimension_two_ne_three
#print axioms DressingFieldHierarchicalBorel.diamond_transport_three
#print axioms DressingFieldHierarchicalBorel.diamond_stage1_vertex_three_diagonal
