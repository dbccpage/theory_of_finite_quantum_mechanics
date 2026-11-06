import Foundations

/-!
CodaReconstruction.A

Reconstruction A Algebra: Residuals of Projections, Kernels, and Cokernels.
Theorems A-T1 through A-T7 and the induced quotient section.
Zero external dependencies; ordinary Lean 4 kernel only ({propext, Quot.sound}).
AuthorityEffect: None.
-/

namespace Coda.A

universe u v

/-- Additive commutative group structure. -/
class AddCommGroup (V : Type u) extends Add V, Neg V, Sub V, Zero V where
  add_assoc : ∀ a b c : V, (a + b) + c = a + (b + c)
  zero_add : ∀ a : V, 0 + a = a
  add_zero : ∀ a : V, a + 0 = a
  add_left_neg : ∀ a : V, -a + a = 0
  add_comm : ∀ a b : V, a + b = b + a
  sub_eq_add_neg : ∀ a b : V, a - b = a + -b

variable {V : Type u} [AddCommGroup V]

theorem add_right_neg (a : V) : a + -a = 0 := by
  rw [AddCommGroup.add_comm, AddCommGroup.add_left_neg]

theorem neg_zero : (-0 : V) = 0 := by
  have h : -(0 : V) + 0 = 0 := AddCommGroup.add_left_neg (0 : V)
  rw [AddCommGroup.add_zero] at h
  exact h

theorem sub_self (a : V) : a - a = 0 := by
  rw [AddCommGroup.sub_eq_add_neg, add_right_neg]

theorem sub_zero (a : V) : a - 0 = a := by
  rw [AddCommGroup.sub_eq_add_neg, neg_zero, AddCommGroup.add_zero]

theorem zero_sub (a : V) : 0 - a = -a := by
  rw [AddCommGroup.sub_eq_add_neg, AddCommGroup.zero_add]

theorem neg_neg (a : V) : -(-a) = a := by
  have h : -(-a) + -a = 0 := AddCommGroup.add_left_neg (-a)
  have h2 : (-(-a) + -a) + a = 0 + a := by rw [h]
  rw [AddCommGroup.add_assoc, AddCommGroup.add_left_neg, AddCommGroup.add_zero, AddCommGroup.zero_add] at h2
  exact h2

theorem add_left_cancel {a b c : V} (h : a + b = a + c) : b = c := by
  have h2 : -a + (a + b) = -a + (a + c) := by rw [h]
  rw [← AddCommGroup.add_assoc, ← AddCommGroup.add_assoc, AddCommGroup.add_left_neg, AddCommGroup.zero_add, AddCommGroup.zero_add] at h2
  exact h2

theorem add_right_cancel {a b c : V} (h : b + a = c + a) : b = c := by
  rw [AddCommGroup.add_comm b a, AddCommGroup.add_comm c a] at h
  exact add_left_cancel h

theorem neg_add (a b : V) : -(a + b) = -b + -a := by
  apply add_right_cancel (a := a + b)
  rw [AddCommGroup.add_left_neg]
  rw [AddCommGroup.add_assoc (-b) (-a) (a + b)]
  rw [← AddCommGroup.add_assoc (-a) a b]
  rw [AddCommGroup.add_left_neg, AddCommGroup.zero_add, AddCommGroup.add_left_neg]

theorem sub_add_cancel (a b : V) : a - b + b = a := by
  rw [AddCommGroup.sub_eq_add_neg, AddCommGroup.add_assoc, AddCommGroup.add_left_neg, AddCommGroup.add_zero]

theorem add_sub_cancel (a b : V) : a + b - b = a := by
  rw [AddCommGroup.sub_eq_add_neg, AddCommGroup.add_assoc, add_right_neg, AddCommGroup.add_zero]

theorem sub_eq_zero_iff {a b : V} : a - b = 0 ↔ a = b := by
  constructor
  · intro h
    have h2 : a - b + b = 0 + b := by rw [h]
    rw [sub_add_cancel, AddCommGroup.zero_add] at h2
    exact h2
  · intro h
    rw [h, sub_self]

/-- Linear map between additive commutative groups. -/
structure LinearMap (V : Type u) (W : Type v) [AddCommGroup V] [AddCommGroup W] where
  toFun : V → W
  map_add : ∀ x y : V, toFun (x + y) = toFun x + toFun y

instance {V : Type u} {W : Type v} [AddCommGroup V] [AddCommGroup W] :
    CoeFun (LinearMap V W) (fun _ => V → W) where
  coe f := f.toFun

theorem map_zero {V W : Type _} [AddCommGroup V] [AddCommGroup W] (f : LinearMap V W) :
    f 0 = 0 := by
  have h1 : f 0 = f 0 + f 0 := by
    have h := f.map_add 0 0
    rw [AddCommGroup.add_zero] at h
    exact h
  have h2 := congrArg (· + -(f 0)) h1
  rw [add_right_neg, AddCommGroup.add_assoc, add_right_neg, AddCommGroup.add_zero] at h2
  exact h2.symm

theorem map_neg {V W : Type _} [AddCommGroup V] [AddCommGroup W] (f : LinearMap V W) (x : V) :
    f (-x) = -f x := by
  apply add_right_cancel (a := f x)
  rw [← f.map_add, AddCommGroup.add_left_neg, map_zero, AddCommGroup.add_left_neg]

theorem map_sub {V W : Type _} [AddCommGroup V] [AddCommGroup W] (f : LinearMap V W) (x y : V) :
    f (x - y) = f x - f y := by
  rw [AddCommGroup.sub_eq_add_neg, f.map_add, map_neg, AddCommGroup.sub_eq_add_neg]

/-- Definition A-D1: Residual of a linear map. -/
def residual (C : LinearMap V V) (x : V) : V :=
  x - C x

theorem decomposition (C : LinearMap V V) (x : V) :
    x = C x + residual C x := by
  dsimp [residual]
  rw [AddCommGroup.add_comm (C x) (x - C x)]
  rw [sub_add_cancel]

/-- Theorem A-T1: Residual zero iff fixed. -/
theorem residual_zero_iff (C : LinearMap V V) (x : V) :
    residual C x = 0 ↔ C x = x := by
  dsimp [residual]
  rw [sub_eq_zero_iff (a := x) (b := C x)]
  exact ⟨Eq.symm, Eq.symm⟩

/-- Theorem A-T2: Leftover in kernel for projection. -/
theorem residual_in_kernel (C : LinearMap V V)
    (hC : ∀ y, C (C y) = C y) (x : V) : C (residual C x) = 0 := by
  dsimp [residual]
  rw [map_sub, hC, sub_self]

/-- Theorem A-T3: Residual operator idempotent for projection. -/
theorem residual_idempotent (C : LinearMap V V)
    (hC : ∀ y, C (C y) = C y) (x : V) :
    residual C (residual C x) = residual C x := by
  change residual C x - C (residual C x) = residual C x
  rw [residual_in_kernel C hC x, sub_zero]

/-- Theorem A-T4: Image of projection equals fixed set. -/
theorem range_fixed_iff (C : LinearMap V V)
    (hC : ∀ y, C (C y) = C y) (x : V) : (∃ y, x = C y) ↔ C x = x := by
  constructor
  · rintro ⟨y, rfl⟩
    exact hC y
  · intro h
    exact ⟨x, h.symm⟩

/-- Direct sum splitting existence: every x in V decomposes into im(C) and ker(C). -/
theorem direct_sum_decomposition (C : LinearMap V V)
    (hC : ∀ y, C (C y) = C y) (x : V) :
    x = C x + residual C x ∧ (∃ y, C x = C y) ∧ C (residual C x) = 0 := by
  refine ⟨decomposition C x, ⟨x, rfl⟩, residual_in_kernel C hC x⟩

/-- Direct sum splitting uniqueness: im(C) and ker(C) intersect only at 0. -/
theorem direct_sum_unique (C : LinearMap V V)
    (hC : ∀ y, C (C y) = C y) (x : V)
    (u v : V) (hu : ∃ y, u = C y) (hv : C v = 0) (hx : x = u + v) :
    u = C x ∧ v = residual C x := by
  rcases hu with ⟨y, rfl⟩
  have hCu : C (C y) = C y := hC y
  have h1 : C x = C (C y + v) := by rw [hx]
  rw [C.map_add, hCu, hv, AddCommGroup.add_zero] at h1
  have hu_eq : C y = C x := h1.symm
  have hv_eq : residual C x = v := by
    dsimp [residual]
    rw [hx]
    rw [C.map_add, hCu, hv, AddCommGroup.add_zero]
    rw [AddCommGroup.add_comm (C y) v, add_sub_cancel]
  exact ⟨hu_eq, hv_eq.symm⟩

/-- Theorem A-T5: Commuting linear map transports residuals. -/
theorem residual_transport {W : Type v} [AddCommGroup W]
    (C : LinearMap V V) (D : LinearMap W W) (T : LinearMap V W)
    (hcomm : ∀ x, T (C x) = D (T x)) (x : V) :
    T (residual C x) = residual D (T x) := by
  dsimp [residual]
  rw [map_sub, hcomm]

theorem sub_diff_eq_diff_sub (a b c d : V) :
    (a - b = c - d) ↔ (a - c = b - d) := by
  constructor
  · intro h
    have h1 : a - b + b = c - d + b := by rw [h]
    rw [sub_add_cancel] at h1
    have h2 : a - c = (c - d + b) - c := by rw [h1]
    rw [AddCommGroup.sub_eq_add_neg (c - d + b) c] at h2
    rw [AddCommGroup.sub_eq_add_neg c d] at h2
    rw [AddCommGroup.add_assoc (c + -d) b (-c)] at h2
    rw [AddCommGroup.add_comm b (-c)] at h2
    rw [← AddCommGroup.add_assoc (c + -d) (-c) b] at h2
    rw [AddCommGroup.add_comm c (-d)] at h2
    rw [AddCommGroup.add_assoc (-d) c (-c)] at h2
    rw [add_right_neg, AddCommGroup.add_zero] at h2
    rw [AddCommGroup.add_comm (-d) b] at h2
    rw [← AddCommGroup.sub_eq_add_neg] at h2
    exact h2
  · intro h
    have h1 : a - c + c = b - d + c := by rw [h]
    rw [sub_add_cancel] at h1
    have h2 : a - b = (b - d + c) - b := by rw [h1]
    rw [AddCommGroup.sub_eq_add_neg (b - d + c) b] at h2
    rw [AddCommGroup.sub_eq_add_neg b d] at h2
    rw [AddCommGroup.add_assoc (b + -d) c (-b)] at h2
    rw [AddCommGroup.add_comm c (-b)] at h2
    rw [← AddCommGroup.add_assoc (b + -d) (-b) c] at h2
    rw [AddCommGroup.add_comm b (-d)] at h2
    rw [AddCommGroup.add_assoc (-d) b (-b)] at h2
    rw [add_right_neg, AddCommGroup.add_zero] at h2
    rw [AddCommGroup.add_comm (-d) c] at h2
    rw [← AddCommGroup.sub_eq_add_neg] at h2
    exact h2

/-- Theorem A-T6: Residual classes match the cokernel. -/
theorem quotient_residual_iff (C : LinearMap V V)
    (hC : ∀ y, C (C y) = C y) (x y : V) :
    (∃ z, x - y = C z) ↔ residual C x = residual C y := by
  constructor
  · rintro ⟨z, hz⟩
    have hz_fixed : C (x - y) = x - y := by
      rw [hz, hC]
    rw [map_sub] at hz_fixed
    dsimp [residual]
    have hsw : (x - C x = y - C y) ↔ (x - y = C x - C y) := sub_diff_eq_diff_sub x (C x) y (C y)
    exact hsw.mpr hz_fixed.symm
  · intro h
    dsimp [residual] at h
    have hsw : (x - y = C x - C y) := (sub_diff_eq_diff_sub x (C x) y (C y)).mp h
    rw [← map_sub] at hsw
    exact ⟨x - y, hsw⟩

/-- Submodule (subgroup) definition. -/
structure Submodule (V : Type u) [AddCommGroup V] where
  carrier : V → Prop
  zero_mem : carrier 0
  add_mem : ∀ {x y}, carrier x → carrier y → carrier (x + y)
  neg_mem : ∀ {x}, carrier x → carrier (-x)

def QuotientRel (R : Submodule V) (x y : V) : Prop :=
  R.carrier (x - y)

def Quotient (R : Submodule V) : Type u :=
  Quot (QuotientRel R)

def quotientMap (R : Submodule V) : V → Quotient R :=
  Quot.mk (QuotientRel R)

/-- Theorem A-T7: Quotient universal property (unique factorization). -/
theorem quotient_universal {W : Type v} [AddCommGroup W]
    (R : Submodule V) (f : LinearMap V W) (hf : ∀ x, R.carrier x → f x = 0) :
    ∃ g : Quotient R → W, (∀ x : V, g (quotientMap R x) = f x) ∧
      (∀ g' : Quotient R → W, (∀ x : V, g' (quotientMap R x) = f x) → g' = g) := by
  have hwell : ∀ x y, QuotientRel R x y → f x = f y := by
    intro x y hxy
    dsimp [QuotientRel] at hxy
    have hzero := hf (x - y) hxy
    rw [map_sub] at hzero
    exact sub_eq_zero_iff.mp hzero
  let g : Quotient R → W := Quot.lift f hwell
  refine ⟨g, by intro x; rfl, ?_⟩
  intro g' hg'
  ext q
  induction q using Quot.ind with
  | mk x => exact hg' x

/-- Image submodule of a linear endomorphism. -/
def imageSubmodule (C : LinearMap V V) : Submodule V where
  carrier x := ∃ y, x = C y
  zero_mem := ⟨0, (map_zero C).symm⟩
  add_mem := by
    rintro x y ⟨a, rfl⟩ ⟨b, rfl⟩
    exact ⟨a + b, (C.map_add a b).symm⟩
  neg_mem := by
    rintro x ⟨a, rfl⟩
    exact ⟨-a, (map_neg C a).symm⟩

/-- Section 4: Induced residual section of the quotient map. -/
theorem quotient_section (C : LinearMap V V)
    (hC : ∀ y, C (C y) = C y) :
    ∃ s : Quotient (imageSubmodule C) → V,
      (∀ x, s (quotientMap (imageSubmodule C) x) = residual C x) ∧
      (∀ q, quotientMap (imageSubmodule C) (s q) = q) ∧
      (∀ q, C (s q) = 0) := by
  have hwell : ∀ x y, QuotientRel (imageSubmodule C) x y → residual C x = residual C y := by
    intro x y hxy
    dsimp [QuotientRel, imageSubmodule] at hxy
    exact (quotient_residual_iff C hC x y).mp hxy
  let s : Quotient (imageSubmodule C) → V := Quot.lift (residual C) hwell
  refine ⟨s, by intro x; rfl, ?_, ?_⟩
  · intro q
    induction q using Quot.ind with
    | mk x =>
      dsimp [s]
      apply Quot.sound
      dsimp [QuotientRel, imageSubmodule]
      refine ⟨-x, ?_⟩
      dsimp [residual]
      rw [AddCommGroup.sub_eq_add_neg (x - C x) x]
      rw [AddCommGroup.sub_eq_add_neg x (C x)]
      rw [AddCommGroup.add_assoc x (-C x) (-x)]
      rw [AddCommGroup.add_comm (-C x) (-x)]
      rw [← AddCommGroup.add_assoc x (-x) (-C x)]
      rw [add_right_neg, AddCommGroup.zero_add]
      exact (map_neg C x).symm
  · intro q
    induction q using Quot.ind with
    | mk x =>
      dsimp [s]
      exact residual_in_kernel C hC x

end Coda.A
