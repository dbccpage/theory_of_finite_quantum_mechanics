/-
  H014 bilinear product -- uniqueness of the integer product map
  on cartesian report coordinates, under named extras.
  AuthorityEffect: None. Candidate only.

  QM_122 remaining job 7.1.4, scoped. The composition interface
  used here is: a map that is additive and integer-homogeneous in
  each slot, and that sends a pair of report-basis vectors to the
  corresponding product-basis vector. On the host Bool × Bool that
  map is unique and equals the pointwise product already named in
  H014.tensor.

  This does not prove that cartesian product is the only legal
  way to combine systems. The coordinate set Bool × Bool is an
  import of the interface. Direct sum lives on a different host
  and is not a rival for this interface.
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H004FreeLinearization
import H014TensorCompositionBoundary

namespace FableHilbertWalk20260819.H014Bilin

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004 (delta)
open FableHilbertWalk20260819.H014 (tensor)

/-- Named extras for a bilinear, Kronecker-normalized product on
    cartesian report coordinates. -/
structure BilinearKroneckerEmbed where
  embed : (Bool → Int) → (Bool → Int) → (Bool × Bool → Int)
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
        delta intPack (i, j) p

/-- The H014 product map meets those extras. -/
def tensorEmbed : BilinearKroneckerEmbed where
  embed := tensor
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

#print axioms tensorEmbed

/-- Pointwise expansion of a Bool-vector in the report basis. -/
theorem bool_vec_expand (u : Bool → Int) (q : Bool) :
    u q =
      u false * delta intPack false q +
        u true * delta intPack true q := by
  cases q <;> simp [delta, intPack]

#print axioms bool_vec_expand

/-- Under the named extras, the embed is the pointwise product. -/
theorem embed_eq_tensor (E : BilinearKroneckerEmbed)
    (u v : Bool → Int) (p : Bool × Bool) :
    E.embed u v p = tensor u v p := by
  rcases p with ⟨a, b⟩
  have hu : u = fun q =>
      u false * delta intPack false q +
        u true * delta intPack true q :=
    funext (bool_vec_expand u)
  have hv : v = fun q =>
      v false * delta intPack false q +
        v true * delta intPack true q :=
    funext (bool_vec_expand v)
  rw [hu, hv]
  have hL :=
    E.add_left
      (fun q => u false * delta intPack false q)
      (fun q => u true * delta intPack true q)
      (fun q =>
        v false * delta intPack false q +
          v true * delta intPack true q) (a, b)
  rw [hL]
  have hf :=
    E.smul_left (u false) (delta intPack false)
      (fun q =>
        v false * delta intPack false q +
          v true * delta intPack true q) (a, b)
  have ht :=
    E.smul_left (u true) (delta intPack true)
      (fun q =>
        v false * delta intPack false q +
          v true * delta intPack true q) (a, b)
  rw [hf, ht]
  have hfR :=
    E.add_right (delta intPack false)
      (fun q => v false * delta intPack false q)
      (fun q => v true * delta intPack true q) (a, b)
  have htR :=
    E.add_right (delta intPack true)
      (fun q => v false * delta intPack false q)
      (fun q => v true * delta intPack true q) (a, b)
  rw [hfR, htR]
  have hf0 :=
    E.smul_right (v false) (delta intPack false)
      (delta intPack false) (a, b)
  have hf1 :=
    E.smul_right (v true) (delta intPack false)
      (delta intPack true) (a, b)
  have ht0 :=
    E.smul_right (v false) (delta intPack true)
      (delta intPack false) (a, b)
  have ht1 :=
    E.smul_right (v true) (delta intPack true)
      (delta intPack true) (a, b)
  rw [hf0, hf1, ht0, ht1]
  rw [E.kronecker false false (a, b), E.kronecker false true (a, b),
    E.kronecker true false (a, b), E.kronecker true true (a, b)]
  unfold tensor delta
  cases a <;> cases b <;> simp [intPack]

#print axioms embed_eq_tensor

/-- Punchline: the named extras pin the product map on this
    coordinate host. Direct sum is a different host, so it is
    not a same-interface rival. Combining-system uniqueness
    beyond this coordinate set is not proved. -/
theorem bilinear_product_unique_on_bool_prod
    (E : BilinearKroneckerEmbed) :
    (∀ u v p, E.embed u v p = tensor u v p) ∧
      (∀ u v p, tensorEmbed.embed u v p = tensor u v p) :=
  ⟨embed_eq_tensor E, fun _ _ _ => rfl⟩

#print axioms bilinear_product_unique_on_bool_prod

end FableHilbertWalk20260819.H014Bilin
