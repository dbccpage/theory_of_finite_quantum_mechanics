import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.Group.Defs
import CausalOrder

/-!
# Isotony, locality, and non-transitivity of spacelike separation on a finite poset net
(CQFT-FINITE-POSET-NET-TARGET)

AuthorityEffect: None.
Scope: Kinematical tensor-product net of local qubit operators indexed by subsets `O : Finset (Fin n)`
of a `FiniteStrictPoset n`, plus the four-element N poset (`0 < 2`, `1 < 2`, `1 < 3`).
Proves:
(a) Isotony: `O₁ ⊆ O₂ → LocalAlgebra O₁ ⊆ LocalAlgebra O₂`.
(b) Locality: If every `x ∈ O₁` and `y ∈ O₂` are spacelike separated in `P`, then `O₁` and `O₂`
    are disjoint (`Disjoint O₁ O₂`), and any two site-factorized operators (or n-qubit Pauli strings)
    localized in `O₁` and `O₂` commute (`mulSiteOp A B = mulSiteOp B A`).
(c) Non-transitivity of spacelike separation: on the 4-element N poset (`0 < 2`, `1 < 2`, `1 < 3`),
    `spacelike posetN 1 0` and `spacelike posetN 0 3` hold, while `1 < 3` is causally related
    so `¬ spacelike posetN 1 3`.
-/

namespace FrontierPosetNet

open CausalOrder

/-- Single-site operator algebra `M` (any monoid, e.g. `2x2` matrices over `Q(i)`); an `n`-site
tensor operator `Fin n → M` is localized in `O : Finset (Fin n)` when it acts as `1` (identity)
at every site outside `O`. -/
def LocalizedIn {n : Nat} {M : Type*} [One M] (O : Finset (Fin n)) (A : Fin n → M) : Prop :=
  ∀ i : Fin n, i ∉ O → A i = 1

/-- Sitewise product `(A * B)_i = A_i * B_i` of two site-factorized operators on `n` qubits. -/
def mulSiteOp {n : Nat} {M : Type*} [Mul M] (A B : Fin n → M) : Fin n → M :=
  fun i => A i * B i

/-- (a) Isotony: if `O₁ ⊆ O₂`, then every operator localized in `O₁` is localized in `O₂`. -/
theorem isotony {n : Nat} {M : Type*} [One M] {O₁ O₂ : Finset (Fin n)}
    (hsub : O₁ ⊆ O₂) {A : Fin n → M} (hA : LocalizedIn O₁ A) :
    LocalizedIn O₂ A := by
  intro i hi₂
  apply hA i
  intro hi₁
  exact hi₂ (hsub hi₁)

/-- Spacelike-separated regions are disjoint, because `isSpacelike P x x` is irreflexive. -/
theorem disjoint_of_all_spacelike {n : Nat} (P : FiniteStrictPoset n)
    {O₁ O₂ : Finset (Fin n)} (hsp : ∀ x ∈ O₁, ∀ y ∈ O₂, isSpacelike P x y) :
    Disjoint O₁ O₂ := by
  rw [Finset.disjoint_left]
  intro x hx₁ hx₂
  exact spacelike_irrefl P x (hsp x hx₁ x hx₂)

/-- (b) Locality: if every `x ∈ O₁` and `y ∈ O₂` are spacelike separated in `P`, then any two
operators `A` localized in `O₁` and `B` localized in `O₂` commute (`mulSiteOp A B = mulSiteOp B A`). -/
theorem locality_commute_of_spacelike {n : Nat} {M : Type*} [MulOneClass M]
    (P : FiniteStrictPoset n) {O₁ O₂ : Finset (Fin n)}
    (hsp : ∀ x ∈ O₁, ∀ y ∈ O₂, isSpacelike P x y)
    {A B : Fin n → M} (hA : LocalizedIn O₁ A) (hB : LocalizedIn O₂ B) :
    mulSiteOp A B = mulSiteOp B A := by
  funext i
  dsimp [mulSiteOp]
  by_cases hi₁ : i ∈ O₁
  · have hi₂ : i ∉ O₂ := Finset.disjoint_left.mp (disjoint_of_all_spacelike P hsp) hi₁
    rw [hB i hi₂, mul_one, one_mul]
  · rw [hA i hi₁, one_mul, mul_one]

/-- (c) The four-element N poset with relations `0 < 2`, `1 < 2`, `1 < 3`. -/
def n_rel_bool (i j : Fin 4) : Bool :=
  (i.val == 0 && j.val == 2) ||
  (i.val == 1 && j.val == 2) ||
  (i.val == 1 && j.val == 3)

def n_rel (i j : Fin 4) : Prop :=
  n_rel_bool i j = true

instance : DecidableRel n_rel := fun x y =>
  inferInstanceAs (Decidable (n_rel_bool x y = true))

def posetN : FiniteStrictPoset 4 where
  rel := n_rel
  decRel := inferInstance
  irrefl := by
    intro ⟨x, hx⟩
    revert x hx
    decide
  trans := by
    intro ⟨x, hx⟩ ⟨y, hy⟩ ⟨z, hz⟩
    revert x hx y hy z hz
    decide

def n0 : Fin 4 := ⟨0, by decide⟩
def n1 : Fin 4 := ⟨1, by decide⟩
def n2 : Fin 4 := ⟨2, by decide⟩
def n3 : Fin 4 := ⟨3, by decide⟩

theorem posetN_spacelike_0_1 : isSpacelike posetN n0 n1 := by
  decide

theorem posetN_spacelike_1_0 : isSpacelike posetN n1 n0 := by
  decide

theorem posetN_spacelike_0_3 : isSpacelike posetN n0 n3 := by
  decide

theorem posetN_causal_1_3 : posetN.rel n1 n3 := by
  decide

theorem posetN_not_spacelike_1_3 : ¬ isSpacelike posetN n1 n3 := by
  decide

/-- Spacelike separation is not transitive: on `posetN`, `n1` is spacelike to `n0` and `n0` is
spacelike to `n3`, while `n1 < n3` are causally related (`¬ isSpacelike posetN n1 n3`). -/
theorem spacelike_not_transitive_on_posetN :
    isSpacelike posetN n1 n0 ∧ isSpacelike posetN n0 n3 ∧ ¬ isSpacelike posetN n1 n3 :=
  ⟨posetN_spacelike_1_0, posetN_spacelike_0_3, posetN_not_spacelike_1_3⟩

end FrontierPosetNet

#print axioms FrontierPosetNet.isotony
#print axioms FrontierPosetNet.disjoint_of_all_spacelike
#print axioms FrontierPosetNet.locality_commute_of_spacelike
#print axioms FrontierPosetNet.posetN_spacelike_0_1
#print axioms FrontierPosetNet.posetN_spacelike_0_3
#print axioms FrontierPosetNet.posetN_causal_1_3
#print axioms FrontierPosetNet.spacelike_not_transitive_on_posetN

private def l5aProvenance : String :=
  "Origin: lean4/FrontierPosetNet.lean Claim: locality_commute_of_spacelike AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
