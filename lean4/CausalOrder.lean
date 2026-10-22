

namespace CausalOrder

structure FiniteStrictPoset (n : Nat) where
  rel : Fin n → Fin n → Prop
  decRel : DecidableRel rel
  irrefl : ∀ x, ¬ rel x x
  trans : ∀ x y z, rel x y → rel y z → rel x z

instance (n : Nat) (P : FiniteStrictPoset n) : DecidableRel P.rel := P.decRel

def le {n : Nat} (P : FiniteStrictPoset n) (x y : Fin n) : Prop :=
  x = y ∨ P.rel x y

instance {n : Nat} (P : FiniteStrictPoset n) (x y : Fin n) : Decidable (le P x y) :=
  match decEq x y with
  | isTrue h => isTrue (Or.inl h)
  | isFalse hne =>
    match P.decRel x y with
    | isTrue hr => isTrue (Or.inr hr)
    | isFalse hnr => isFalse (fun h => match h with | Or.inl e => hne e | Or.inr r => hnr r)

def isSpacelike {n : Nat} (P : FiniteStrictPoset n) (x y : Fin n) : Prop :=
  x ≠ y ∧ ¬ P.rel x y ∧ ¬ P.rel y x

instance {n : Nat} (P : FiniteStrictPoset n) (x y : Fin n) : Decidable (isSpacelike P x y) :=
  inferInstanceAs (Decidable (x ≠ y ∧ ¬ P.rel x y ∧ ¬ P.rel y x))

theorem spacelike_symm {n : Nat} (P : FiniteStrictPoset n) (x y : Fin n) :
    isSpacelike P x y ↔ isSpacelike P y x := by
  dsimp [isSpacelike]
  constructor
  · intro ⟨hne, hxy, hyx⟩
    exact ⟨Ne.symm hne, hyx, hxy⟩
  · intro ⟨hne, hyx, hxy⟩
    exact ⟨Ne.symm hne, hxy, hyx⟩

theorem spacelike_irrefl {n : Nat} (P : FiniteStrictPoset n) (x : Fin n) :
    ¬ isSpacelike P x x := by
  dsimp [isSpacelike]
  intro ⟨hne, _⟩
  exact hne rfl


def c1_rel_bool (x y : Fin 3) : Bool :=
  (x.val == 0 && y.val == 1) || (x.val == 0 && y.val == 2)

def c1_rel (x y : Fin 3) : Prop :=
  c1_rel_bool x y = true

instance : DecidableRel c1_rel := fun x y =>
  inferInstanceAs (Decidable (c1_rel_bool x y = true))

def C1 : FiniteStrictPoset 3 where
  rel := c1_rel
  decRel := inferInstance
  irrefl := by
    intro ⟨x, hx⟩
    revert x hx
    decide
  trans := by
    intro ⟨x, hx⟩ ⟨y, hy⟩ ⟨z, hz⟩
    revert x hx y hy z hz
    decide

def e0 : Fin 3 := ⟨0, by decide⟩
def e1 : Fin 3 := ⟨1, by decide⟩
def e2 : Fin 3 := ⟨2, by decide⟩

theorem c1_spacelike_1_2 : isSpacelike C1 e1 e2 := by
  decide

theorem c1_not_spacelike_0_1 : ¬ isSpacelike C1 e0 e1 := by
  decide

theorem c1_not_spacelike_0_2 : ¬ isSpacelike C1 e0 e2 := by
  decide

theorem c1_spacelike_symm_irrefl :
    isSpacelike C1 e1 e2 ∧ isSpacelike C1 e2 e1 ∧ ¬ isSpacelike C1 e1 e1 := by
  decide

@[deprecated c1_spacelike_symm_irrefl (since := "2026-10-22")] theorem incomparability_not_transitive_c1 :
    isSpacelike C1 e1 e2 ∧ isSpacelike C1 e2 e1 ∧ ¬ isSpacelike C1 e1 e1 :=
  c1_spacelike_symm_irrefl


def c2_rel_bool (x y : Fin 4) : Bool :=
  (x.val == 0 && (y.val == 1 || y.val == 2 || y.val == 3)) ||
  (x.val == 1 && y.val == 3) ||
  (x.val == 2 && y.val == 3)

def c2_rel (x y : Fin 4) : Prop :=
  c2_rel_bool x y = true

instance : DecidableRel c2_rel := fun x y =>
  inferInstanceAs (Decidable (c2_rel_bool x y = true))

def C2 : FiniteStrictPoset 4 where
  rel := c2_rel
  decRel := inferInstance
  irrefl := by
    intro ⟨x, hx⟩
    revert x hx
    decide
  trans := by
    intro ⟨x, hx⟩ ⟨y, hy⟩ ⟨z, hz⟩
    revert x hx y hy z hz
    decide

def d0 : Fin 4 := ⟨0, by decide⟩
def d1 : Fin 4 := ⟨1, by decide⟩
def d2 : Fin 4 := ⟨2, by decide⟩
def d3 : Fin 4 := ⟨3, by decide⟩

theorem c2_spacelike_1_2 : isSpacelike C2 d1 d2 := by
  decide

theorem c2_causal_0_3 : C2.rel d0 d3 := by
  decide

theorem c2_past_common : C2.rel d0 d1 ∧ C2.rel d0 d2 := by
  decide

theorem c2_future_common : C2.rel d1 d3 ∧ C2.rel d2 d3 := by
  decide


def n4_rel_bool (x y : Fin 4) : Bool :=
  (x.val == 0 && y.val == 2) ||
  (x.val == 1 && y.val == 2) ||
  (x.val == 1 && y.val == 3)

def n4_rel (x y : Fin 4) : Prop :=
  n4_rel_bool x y = true

instance : DecidableRel n4_rel := fun x y =>
  inferInstanceAs (Decidable (n4_rel_bool x y = true))

def N4 : FiniteStrictPoset 4 where
  rel := n4_rel
  decRel := inferInstance
  irrefl := by
    intro ⟨x, hx⟩
    revert x hx
    decide
  trans := by
    intro ⟨x, hx⟩ ⟨y, hy⟩ ⟨z, hz⟩
    revert x hx y hy z hz
    decide

theorem n4_spacelike_not_transitive :
    d0 ≠ d3 ∧ d3 ≠ d2 ∧ d0 ≠ d2 ∧
    isSpacelike N4 d0 d3 ∧ isSpacelike N4 d3 d2 ∧ N4.rel d0 d2 ∧ ¬ isSpacelike N4 d0 d2 := by
  decide

theorem spacelike_not_transitive :
    ¬ (∀ (n : Nat) (P : FiniteStrictPoset n) (x y z : Fin n),
        x ≠ y → y ≠ z → x ≠ z → isSpacelike P x y → isSpacelike P y z → isSpacelike P x z) := by
  intro h
  have hn := n4_spacelike_not_transitive
  exact hn.2.2.2.2.2.2 (h 4 N4 d0 d3 d2 hn.1 hn.2.1 hn.2.2.1 hn.2.2.2.1 hn.2.2.2.2.1)


def c1_dual_rel_bool (x y : Fin 3) : Bool :=
  (x.val == 1 && y.val == 0) || (x.val == 2 && y.val == 0)

def c1_dual_rel (x y : Fin 3) : Prop :=
  c1_dual_rel_bool x y = true

instance : DecidableRel c1_dual_rel := fun x y =>
  inferInstanceAs (Decidable (c1_dual_rel_bool x y = true))

def C1_Dual : FiniteStrictPoset 3 where
  rel := c1_dual_rel
  decRel := inferInstance
  irrefl := by
    intro ⟨x, hx⟩
    revert x hx
    decide
  trans := by
    intro ⟨x, hx⟩ ⟨y, hy⟩ ⟨z, hz⟩
    revert x hx y hy z hz
    decide

theorem order_independence_witness :
    C1.rel e0 e1 ∧ ¬ C1_Dual.rel e0 e1 ∧ C1_Dual.rel e1 e0 ∧ ¬ C1.rel e1 e0 := by
  decide


def c1_mu (x y : Fin 3) : Int :=
  match x.val, y.val with
  | 0, 0 => 1
  | 1, 1 => 1
  | 2, 2 => 1
  | 0, 1 => -1
  | 0, 2 => -1
  | _, _ => 0

theorem c1_mu_diagonal (x : Fin 3) : c1_mu x x = 1 := by
  rcases x with ⟨val, h⟩
  revert val h
  decide

theorem c1_mu_spacelike_vanishes : c1_mu e1 e2 = 0 := by
  decide

def c2_mu (x y : Fin 4) : Int :=
  match x.val, y.val with
  | 0, 0 => 1
  | 1, 1 => 1
  | 2, 2 => 1
  | 3, 3 => 1
  | 0, 1 => -1
  | 0, 2 => -1
  | 1, 3 => -1
  | 2, 3 => -1
  | 0, 3 => 1
  | _, _ => 0

theorem c2_mu_top_bottom : c2_mu d0 d3 = 1 := by
  decide

#print axioms spacelike_symm
#print axioms spacelike_irrefl
#print axioms c1_spacelike_symm_irrefl
#print axioms n4_spacelike_not_transitive
#print axioms spacelike_not_transitive
#print axioms order_independence_witness
#print axioms c1_mu_diagonal
#print axioms c1_mu_spacelike_vanishes
#print axioms c2_mu_top_bottom

end CausalOrder

private def l5aProvenance : String :=
  "Origin: lean4/CausalOrder.lean Claim: spacelike_symm AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
