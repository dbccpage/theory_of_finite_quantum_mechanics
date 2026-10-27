




import HWKernel
import FreeLinearization
import TensorCompositionBoundary
import BilinearProduct

namespace HilbertWalk.Interface

open HilbertWalk.HWKernel
open HilbertWalk.FreeLinearization (delta)
open HilbertWalk.TensorCompositionBoundary (tensor)
open HilbertWalk.BilinearProduct (bool_vec_expand)

structure CombiningEmbed where
  embed : (Bool → Int) → (Bool → Int) → (Bool × Bool → Int)
  tag : Bool → Bool → Bool × Bool
  add_left :
    ∀ u1 u2 v p,
      embed (fun q => u1 q + u2 q) v p = embed u1 v p + embed u2 v p
  add_right :
    ∀ u v1 v2 p,
      embed u (fun q => v1 q + v2 q) p = embed u v1 p + embed u v2 p
  smul_left :
    ∀ (c : Int) u v p,
      embed (fun q => c * u q) v p = c * embed u v p
  smul_right :
    ∀ (c : Int) u v p,
      embed u (fun q => c * v q) p = c * embed u v p
  kronecker :
    ∀ i j p,
      embed (delta intPack i) (delta intPack j) p =
        delta intPack (tag i j) p

def tensorComb : CombiningEmbed where
  embed := tensor
  tag := fun i j => (i, j)
  add_left := fun u1 u2 v p => Int.add_mul (u1 p.1) (u2 p.1) (v p.2)
  add_right := fun u v1 v2 p => Int.mul_add (u p.1) (v1 p.2) (v2 p.2)
  smul_left := fun c u v p => by
    unfold tensor
    rw [Int.mul_assoc]
  smul_right := fun c u v p => by
    unfold tensor
    rw [← Int.mul_assoc, Int.mul_comm (u p.1) c, Int.mul_assoc]
  kronecker := fun i j p => by
    rcases p with ⟨a, b⟩
    unfold tensor delta
    cases i <;> cases j <;> cases a <;> cases b <;> simp [intPack]

#print axioms tensorComb

def dumpRight (u v : Bool → Int) : Bool × Bool → Int
  | (a, false) => u a * (v false + v true)
  | (_, true) => 0

theorem dumpRight_add_left
    (u1 u2 v : Bool → Int) (p : Bool × Bool) :
    dumpRight (fun q => u1 q + u2 q) v p =
      dumpRight u1 v p + dumpRight u2 v p := by
  rcases p with ⟨a, b⟩
  cases b
  · exact Int.add_mul (u1 a) (u2 a) (v false + v true)
  · rfl

theorem dumpRight_add_right
    (u v1 v2 : Bool → Int) (p : Bool × Bool) :
    dumpRight u (fun q => v1 q + v2 q) p =
      dumpRight u v1 p + dumpRight u v2 p := by
  rcases p with ⟨a, b⟩
  cases b
  · have hsum :
        (v1 false + v2 false) + (v1 true + v2 true) =
          (v1 false + v1 true) + (v2 false + v2 true) := by
      omega
    change
      u a * ((v1 false + v2 false) + (v1 true + v2 true)) =
        u a * (v1 false + v1 true) + u a * (v2 false + v2 true)
    rw [hsum, Int.mul_add]
  · rfl

theorem dumpRight_smul_left
    (c : Int) (u v : Bool → Int) (p : Bool × Bool) :
    dumpRight (fun q => c * u q) v p = c * dumpRight u v p := by
  rcases p with ⟨a, b⟩
  cases b
  · exact Int.mul_assoc c (u a) (v false + v true)
  · exact (Int.mul_zero c).symm

theorem dumpRight_smul_right
    (c : Int) (u v : Bool → Int) (p : Bool × Bool) :
    dumpRight u (fun q => c * v q) p = c * dumpRight u v p := by
  rcases p with ⟨a, b⟩
  cases b
  · change
        u a * (c * v false + c * v true) =
          c * (u a * (v false + v true))
    rw [← Int.mul_add, ← Int.mul_assoc, Int.mul_comm (u a) c,
      Int.mul_assoc]
  · exact (Int.mul_zero c).symm

theorem dumpRight_kronecker (i j : Bool) (p : Bool × Bool) :
    dumpRight (delta intPack i) (delta intPack j) p =
      delta intPack (i, false) p := by
  rcases p with ⟨a, b⟩
  cases b
  · have hsum :
        delta intPack j false + delta intPack j true = 1 := by
      cases j <;> simp [delta, intPack]
    change
      delta intPack i a *
          (delta intPack j false + delta intPack j true) =
        delta intPack (i, false) (a, false)
    rw [hsum, Int.mul_one]
    cases i <;> cases a <;> simp [delta, intPack]
  · change (0 : Int) = delta intPack (i, false) (a, true)
    cases i <;> cases a <;> simp [delta, intPack]

def dumpRightComb : CombiningEmbed where
  embed := dumpRight
  tag := fun i _ => (i, false)
  add_left := dumpRight_add_left
  add_right := dumpRight_add_right
  smul_left := dumpRight_smul_left
  smul_right := dumpRight_smul_right
  kronecker := dumpRight_kronecker

#print axioms dumpRightComb

theorem dumpRight_misses_off_slice :
    dumpRight (delta intPack false) (delta intPack true)
      (false, true) = 0 :=
  rfl

#print axioms dumpRight_misses_off_slice

theorem tensor_hits_named_pair :
    tensor (delta intPack false) (delta intPack true)
      (false, true) = 1 := by
  unfold tensor delta
  simp [intPack]

#print axioms tensor_hits_named_pair

theorem dumpRight_not_tensor :
    ¬ ∀ u v p, dumpRight u v p = tensor u v p := by
  intro h
  have ht :=
    h (delta intPack false) (delta intPack true) (false, true)
  rw [dumpRight_misses_off_slice, tensor_hits_named_pair] at ht
  exact Int.zero_ne_one ht

#print axioms dumpRight_not_tensor

theorem dumpRight_tag_not_injective :
    dumpRightComb.tag false false = dumpRightComb.tag false true :=
  rfl

#print axioms dumpRight_tag_not_injective

theorem tensor_tag_injective :
    ∀ i1 j1 i2 j2,
      tensorComb.tag i1 j1 = tensorComb.tag i2 j2 →
        i1 = i2 ∧ j1 = j2 :=
  fun _ _ _ _ h => Prod.mk.inj h

#print axioms tensor_tag_injective

theorem delta_prod_eq (q r : Bool × Bool) :
    delta intPack q r = if q = r then (1 : Int) else 0 := by
  rcases q with ⟨a, b⟩
  rcases r with ⟨c, d⟩
  cases a <;> cases b <;> cases c <;> cases d <;> simp [delta, intPack]

#print axioms delta_prod_eq

theorem embed_expands (C : CombiningEmbed)
    (u v : Bool → Int) (p : Bool × Bool) :
    C.embed u v p =
      u false * v false * delta intPack (C.tag false false) p +
        u false * v true * delta intPack (C.tag false true) p +
          u true * v false * delta intPack (C.tag true false) p +
            u true * v true * delta intPack (C.tag true true) p := by
  have hu : u = fun q =>
      u false * delta intPack false q +
        u true * delta intPack true q :=
    funext (bool_vec_expand u)
  have hv : v = fun q =>
      v false * delta intPack false q +
        v true * delta intPack true q :=
    funext (bool_vec_expand v)
  conv => lhs; rw [hu, hv]
  have hL :=
    C.add_left
      (fun q => u false * delta intPack false q)
      (fun q => u true * delta intPack true q)
      (fun q =>
        v false * delta intPack false q +
          v true * delta intPack true q) p
  rw [hL]
  have hf :=
    C.smul_left (u false) (delta intPack false)
      (fun q =>
        v false * delta intPack false q +
          v true * delta intPack true q) p
  have ht :=
    C.smul_left (u true) (delta intPack true)
      (fun q =>
        v false * delta intPack false q +
          v true * delta intPack true q) p
  rw [hf, ht]
  have hfR :=
    C.add_right (delta intPack false)
      (fun q => v false * delta intPack false q)
      (fun q => v true * delta intPack true q) p
  have htR :=
    C.add_right (delta intPack true)
      (fun q => v false * delta intPack false q)
      (fun q => v true * delta intPack true q) p
  rw [hfR, htR]
  have hf0 :=
    C.smul_right (v false) (delta intPack false)
      (delta intPack false) p
  have hf1 :=
    C.smul_right (v true) (delta intPack false)
      (delta intPack true) p
  have ht0 :=
    C.smul_right (v false) (delta intPack true)
      (delta intPack false) p
  have ht1 :=
    C.smul_right (v true) (delta intPack true)
      (delta intPack true) p
  rw [hf0, hf1, ht0, ht1]
  rw [C.kronecker false false p, C.kronecker false true p,
    C.kronecker true false p, C.kronecker true true p]
  rw [Int.mul_add, Int.mul_add]
  rw [← Int.mul_assoc, ← Int.mul_assoc, ← Int.mul_assoc,
    ← Int.mul_assoc]
  exact
    (Int.add_assoc
        (u false * v false * delta intPack (C.tag false false) p +
          u false * v true * delta intPack (C.tag false true) p)
        (u true * v false * delta intPack (C.tag true false) p)
        (u true * v true * delta intPack (C.tag true true) p)).symm

#print axioms embed_expands

theorem tag_delta_eq (C : CombiningEmbed)
    (hinj : ∀ i1 j1 i2 j2, C.tag i1 j1 = C.tag i2 j2 →
      i1 = i2 ∧ j1 = j2)
    (i j i' j' : Bool) :
    delta intPack (C.tag i j) (C.tag i' j') =
      delta intPack (i, j) (i', j') := by
  rw [delta_prod_eq, delta_prod_eq]
  by_cases hpair : (i, j) = (i', j')
  · have hi : i = i' := congrArg Prod.fst hpair
    have hj : j = j' := congrArg Prod.snd hpair
    subst hi
    subst hj
    simp
  · have htag : C.tag i j ≠ C.tag i' j' := by
      intro ht
      exact hpair
        (Prod.ext (hinj i j i' j' ht).1 (hinj i j i' j' ht).2)
    simp [hpair, htag]

#print axioms tag_delta_eq

theorem injective_tag_recovers_product (C : CombiningEmbed)
    (hinj : ∀ i1 j1 i2 j2, C.tag i1 j1 = C.tag i2 j2 →
      i1 = i2 ∧ j1 = j2)
    (u v : Bool → Int) (i j : Bool) :
    C.embed u v (C.tag i j) = tensor u v (i, j) := by
  rw [embed_expands]
  rw [tag_delta_eq C hinj false false i j,
    tag_delta_eq C hinj false true i j,
    tag_delta_eq C hinj true false i j,
    tag_delta_eq C hinj true true i j]
  unfold tensor delta
  cases i <;> cases j <;> simp [intPack]

#print axioms injective_tag_recovers_product

theorem two_combinings_share_interface_and_disagree :
    (∀ u v p, tensorComb.embed u v p = tensor u v p) ∧
      (∀ u v p, dumpRightComb.embed u v p = dumpRight u v p) ∧
      dumpRight (delta intPack false) (delta intPack true)
          (false, true) ≠
        tensor (delta intPack false) (delta intPack true)
          (false, true) ∧
      dumpRightComb.tag false false =
        dumpRightComb.tag false true ∧
      (∀ i1 j1 i2 j2,
        tensorComb.tag i1 j1 = tensorComb.tag i2 j2 →
          i1 = i2 ∧ j1 = j2) ∧
      (∀ u v i j,
        tensorComb.embed u v (tensorComb.tag i j) =
          tensor u v (i, j)) :=
  ⟨fun _ _ _ => rfl, fun _ _ _ => rfl, by
    have h0 := dumpRight_misses_off_slice
    have h1 := tensor_hits_named_pair
    omega, rfl, tensor_tag_injective,
    injective_tag_recovers_product tensorComb tensor_tag_injective⟩

#print axioms two_combinings_share_interface_and_disagree

end HilbertWalk.Interface

private def l5aProvenance : String :=
  "Origin: lean4/HilbertWalkInterface.lean Claim: dumpRight_add_left AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
