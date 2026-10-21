import Mathlib.SetTheory.Cardinal.Free
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Discrete.Basic
import Mathlib.Data.Fintype.BigOperators
import Mathlib.SetTheory.Cardinal.Finite

/-!
# Free monoids on alphabets of different sizes are not isomorphic

AuthorityEffect: None.  Scope: free monoids (`FreeMonoid`, i.e. words) over arbitrary alphabets, monoid
isomorphisms between them, and equivalences of discrete categories.  Nothing here concerns numerals,
language restriction, partial recovery, Ext, or any physical reading; it proves only the structural claim of
node PG-FREE-MONOID-NONISO and its sharp boundary.

* `FreeMonoid α ≃* FreeMonoid β` forces a bijection `α ≃ β` (the atoms are the one-letter words, and a
  monoid isomorphism permutes atoms).  Hence unequal finite alphabets give non-isomorphic free monoids.
* `Discrete α ≌ Discrete β` forces `α ≃ β`; with `Fin n`, `Fin m` this is `n = m`.
* The boundary: the underlying SETS of `FreeMonoid (Fin n)` and `FreeMonoid (Fin m)` are in bijection for all
  `n, m ≥ 1` (both countably infinite), so "different cardinality" is NOT the content; the content is that no
  bijection respects multiplication.  For `n = 0` the free monoid is a single point.
* The source's `WordIso` (list maps with inverse and append laws) is the same thing as a `MulEquiv`.
-/

namespace FreeMonoidNoniso

open CategoryTheory

/-- An atom of a monoid: not the unit, and any factorization has a trivial factor. -/
def IsAtom {M : Type*} [Monoid M] (x : M) : Prop := x ≠ 1 ∧ ∀ y z, x = y * z → y = 1 ∨ z = 1

theorem isAtom_iff {α : Type*} (x : FreeMonoid α) : IsAtom x ↔ ∃ a, x = FreeMonoid.of a := by
  constructor
  · rintro ⟨hne, hfac⟩
    match hl : FreeMonoid.toList x with
    | [] => exact absurd (by
        have : x = FreeMonoid.ofList (FreeMonoid.toList x) := rfl
        rw [this, hl]; rfl) hne
    | a :: t =>
      have hx : x = FreeMonoid.of a * FreeMonoid.ofList t := by
        have : x = FreeMonoid.ofList (FreeMonoid.toList x) := rfl
        rw [this, hl]; rfl
      rcases hfac _ _ hx with h | h
      · exfalso
        have := congrArg FreeMonoid.toList h
        simp at this
      · refine ⟨a, ?_⟩
        rw [hx, h, mul_one]
  · rintro ⟨a, rfl⟩
    refine ⟨?_, ?_⟩
    · intro h
      have := congrArg FreeMonoid.toList h
      exact List.cons_ne_nil a [] this
    · intro y z h
      have hl := congrArg FreeMonoid.length h
      rw [FreeMonoid.length_mul, FreeMonoid.length_of] at hl
      have : y.length = 0 ∨ z.length = 0 := by omega
      rcases this with h0 | h0
      · exact Or.inl (FreeMonoid.length_eq_zero.mp h0)
      · exact Or.inr (FreeMonoid.length_eq_zero.mp h0)

/-- A monoid isomorphism maps atoms to atoms. -/
theorem isAtom_map {M N : Type*} [Monoid M] [Monoid N] (e : M ≃* N) {x : M} :
    IsAtom x → IsAtom (e x) := by
  rintro ⟨hne, hfac⟩
  refine ⟨?_, ?_⟩
  · intro h
    exact hne (e.injective (by rw [h, map_one]))
  · intro y z h
    have h' : x = e.symm y * e.symm z := by
      apply e.injective
      rw [map_mul, MulEquiv.apply_symm_apply, MulEquiv.apply_symm_apply]
      exact h
    rcases hfac _ _ h' with h1 | h1
    · left
      have := congrArg e h1
      rwa [MulEquiv.apply_symm_apply, map_one] at this
    · right
      have := congrArg e h1
      rwa [MulEquiv.apply_symm_apply, map_one] at this

/-- A monoid isomorphism preserves and reflects atoms. -/
theorem isAtom_map_iff {M N : Type*} [Monoid M] [Monoid N] (e : M ≃* N) (x : M) :
    IsAtom (e x) ↔ IsAtom x := by
  constructor
  · intro h
    have := isAtom_map e.symm h
    rwa [MulEquiv.symm_apply_apply] at this
  · exact isAtom_map e

/-- The one-letter words are exactly the atoms: a bijection between the alphabet and the atoms. -/
noncomputable def atomEquiv (α : Type*) : α ≃ {x : FreeMonoid α // IsAtom x} :=
  Equiv.ofBijective (fun a => ⟨FreeMonoid.of a, (isAtom_iff _).mpr ⟨a, rfl⟩⟩)
    ⟨fun a b h => by
        have := congrArg (fun p : {x : FreeMonoid α // IsAtom x} => FreeMonoid.toList p.1) h
        simpa using this,
     fun ⟨x, hx⟩ => by
        obtain ⟨a, rfl⟩ := (isAtom_iff x).mp hx
        exact ⟨a, rfl⟩⟩

/-- Any monoid isomorphism of free monoids yields a bijection of the alphabets (general, arbitrary alphabets). -/
noncomputable def alphabetEquiv {α β : Type*} (e : FreeMonoid α ≃* FreeMonoid β) : α ≃ β :=
  ((atomEquiv α).trans (e.toEquiv.subtypeEquiv (fun x => (isAtom_map_iff e x).symm))).trans (atomEquiv β).symm

/-- Unequal finite alphabets: no monoid isomorphism between the free monoids. -/
theorem no_free_monoid_iso {n m : Nat} (h : n ≠ m) : IsEmpty (FreeMonoid (Fin n) ≃* FreeMonoid (Fin m)) :=
  ⟨fun e => h (by simpa using Fintype.card_congr (alphabetEquiv e))⟩

/-- The converse: the free monoids are isomorphic exactly when the alphabets are in bijection. -/
theorem freeMonoid_iso_iff_equiv {α β : Type*} :
    Nonempty (FreeMonoid α ≃* FreeMonoid β) ↔ Nonempty (α ≃ β) := by
  constructor
  · rintro ⟨e⟩; exact ⟨alphabetEquiv e⟩
  · rintro ⟨f⟩
    refine ⟨MonoidHom.toMulEquiv (FreeMonoid.map f) (FreeMonoid.map f.symm) ?_ ?_⟩
    · apply FreeMonoid.hom_eq; intro x; simp [FreeMonoid.map_of]
    · apply FreeMonoid.hom_eq; intro x; simp [FreeMonoid.map_of]

/-! ## Discrete categories -/

theorem discrete_equivalence_card {α β : Type*} (E : Discrete α ≌ Discrete β) : Nonempty (α ≃ β) := by
  refine ⟨⟨fun a => (E.functor.obj ⟨a⟩).as, fun b => (E.inverse.obj ⟨b⟩).as, ?_, ?_⟩⟩
  · intro a
    exact (Discrete.eq_of_hom (E.unitIso.app (Discrete.mk a)).hom).symm
  · intro b
    exact Discrete.eq_of_hom (E.counitIso.app (Discrete.mk b)).hom

theorem no_discrete_equivalence {n m : Nat} (h : n ≠ m) : IsEmpty (Discrete (Fin n) ≌ Discrete (Fin m)) :=
  ⟨fun E => by
    obtain ⟨f⟩ := discrete_equivalence_card E
    exact h (by simpa using Fintype.card_congr f)⟩

theorem discrete_equivalence_iff {n m : Nat} : Nonempty (Discrete (Fin n) ≌ Discrete (Fin m)) ↔ n = m := by
  constructor
  · rintro ⟨E⟩
    by_contra h
    exact (no_discrete_equivalence h).false E
  · rintro rfl
    exact ⟨CategoryTheory.Equivalence.refl⟩

/-! ## The boundary: a set bijection exists, a monoid isomorphism does not -/

/-- For nonempty alphabets the free monoids are countably infinite, hence in bijection as bare sets. -/
theorem set_bijection_exists {n m : Nat} (hn : 0 < n) (hm : 0 < m) :
    Nonempty (FreeMonoid (Fin n) ≃ FreeMonoid (Fin m)) := by
  have : Nonempty (Fin n) := ⟨⟨0, hn⟩⟩
  have : Nonempty (Fin m) := ⟨⟨0, hm⟩⟩
  exact nonempty_equiv_of_countable

/-- The sharp statement: for `n ≠ m`, both `≥ 1`, bare-set bijection yes, monoid isomorphism no. -/
theorem bijection_but_not_isomorphic {n m : Nat} (hn : 0 < n) (hm : 0 < m) (h : n ≠ m) :
    Nonempty (FreeMonoid (Fin n) ≃ FreeMonoid (Fin m)) ∧ IsEmpty (FreeMonoid (Fin n) ≃* FreeMonoid (Fin m)) :=
  ⟨set_bijection_exists hn hm, no_free_monoid_iso h⟩

/-- The free monoid on the empty alphabet is a single point. -/
theorem free_monoid_zero_subsingleton : Subsingleton (FreeMonoid (Fin 0)) :=
  ⟨fun x y => by
    have hx : x = FreeMonoid.ofList [] := by
      match hl : FreeMonoid.toList x with
      | [] => exact (by have : x = FreeMonoid.ofList (FreeMonoid.toList x) := rfl
                        rw [this, hl])
      | a :: _ => exact a.elim0
    have hy : y = FreeMonoid.ofList [] := by
      match hl : FreeMonoid.toList y with
      | [] => exact (by have : y = FreeMonoid.ofList (FreeMonoid.toList y) := rfl
                        rw [this, hl])
      | a :: _ => exact a.elim0
    rw [hx, hy]⟩

/-- Exact counts: words of length `k` over `Fin n` number `n ^ k`; the atoms (length one) number `n`. -/
theorem card_words_of_length (n k : Nat) :
    Nat.card {w : FreeMonoid (Fin n) // FreeMonoid.length w = k} = n ^ k := by
  have e : {w : FreeMonoid (Fin n) // FreeMonoid.length w = k} ≃ List.Vector (Fin n) k := Equiv.refl _
  rw [Nat.card_congr e, Nat.card_eq_fintype_card, card_vector, Fintype.card_fin]

theorem card_atoms (n : Nat) : Nat.card {x : FreeMonoid (Fin n) // IsAtom x} = n := by
  rw [← Nat.card_congr (atomEquiv (Fin n)), Nat.card_eq_fintype_card, Fintype.card_fin]

/-! ## The source's `WordIso` is a `MulEquiv` -/

/-- The source structure of `Paper.lean` (`WordIso`), reproduced as a labelled definition. -/
structure WordIso (A B : Type) where
  forward : List A → List B
  backward : List B → List A
  forward_empty : forward [] = []
  backward_empty : backward [] = []
  forward_append : ∀ u v, forward (u ++ v) = forward u ++ forward v
  backward_append : ∀ u v, backward (u ++ v) = backward u ++ backward v
  left_inverse : ∀ w, backward (forward w) = w
  right_inverse : ∀ w, forward (backward w) = w

def WordIso.toMulEquiv {A B : Type} (e : WordIso A B) : FreeMonoid A ≃* FreeMonoid B where
  toFun x := FreeMonoid.ofList (e.forward (FreeMonoid.toList x))
  invFun y := FreeMonoid.ofList (e.backward (FreeMonoid.toList y))
  left_inv x := congrArg FreeMonoid.ofList (e.left_inverse (FreeMonoid.toList x))
  right_inv y := congrArg FreeMonoid.ofList (e.right_inverse (FreeMonoid.toList y))
  map_mul' x y := congrArg FreeMonoid.ofList (e.forward_append (FreeMonoid.toList x) (FreeMonoid.toList y))

/-- The source theorem `unequal_finite_alphabets_not_iso`, recovered through the bridge. -/
theorem unequal_finite_alphabets_not_wordiso {n m : Nat} (h : n ≠ m) : ¬ Nonempty (WordIso (Fin n) (Fin m)) :=
  fun ⟨e⟩ => (no_free_monoid_iso h).false e.toMulEquiv

end FreeMonoidNoniso

#print axioms FreeMonoidNoniso.isAtom_iff
#print axioms FreeMonoidNoniso.isAtom_map_iff
#print axioms FreeMonoidNoniso.alphabetEquiv
#print axioms FreeMonoidNoniso.no_free_monoid_iso
#print axioms FreeMonoidNoniso.freeMonoid_iso_iff_equiv
#print axioms FreeMonoidNoniso.discrete_equivalence_card
#print axioms FreeMonoidNoniso.no_discrete_equivalence
#print axioms FreeMonoidNoniso.discrete_equivalence_iff
#print axioms FreeMonoidNoniso.set_bijection_exists
#print axioms FreeMonoidNoniso.bijection_but_not_isomorphic
#print axioms FreeMonoidNoniso.free_monoid_zero_subsingleton
#print axioms FreeMonoidNoniso.card_words_of_length
#print axioms FreeMonoidNoniso.card_atoms
#print axioms FreeMonoidNoniso.unequal_finite_alphabets_not_wordiso
