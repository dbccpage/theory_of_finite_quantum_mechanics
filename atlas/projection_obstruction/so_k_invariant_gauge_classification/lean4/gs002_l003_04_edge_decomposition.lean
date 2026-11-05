import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Fintype.Basic

open scoped BigOperators

/-!
Finite edge-decomposition kernel (PL-003-A).

For a finite edge-indexed cochain, strong disjoint-support additivity lets a
global diagnostic split into singleton-edge contributions. This is the precise
finite support-splitting theorem used by the PaperGS002 aggregation boundary.
-/

variable {E V R : Type*} [DecidableEq E] [Zero V] [AddCommMonoid R]

def edgeSingle (e₀ : E) (x : V) : E → V :=
  fun e => if e = e₀ then x else 0

def restrictEdges (S : Finset E) (ω : E → V) : E → V :=
  fun e => if e ∈ S then ω e else 0

@[simp]
lemma restrictEdges_empty (ω : E → V) :
    restrictEdges (∅ : Finset E) ω = 0 := by
  funext e
  simp [restrictEdges]

@[simp]
lemma restrictEdges_univ [Fintype E] (ω : E → V) :
    restrictEdges Finset.univ ω = ω := by
  funext e
  simp [restrictEdges]

lemma edge_decomposition_on_finset
    (J : (E → V) → R)
    (hzero : J 0 = 0)
    (hsplit :
      ∀ (S : Finset E) (e : E) (ω : E → V),
        e ∉ S →
        J (restrictEdges (insert e S) ω) =
          J (edgeSingle e (ω e)) + J (restrictEdges S ω))
    (S : Finset E) (ω : E → V) :
    J (restrictEdges S ω) = S.sum (fun e => J (edgeSingle e (ω e))) := by
  refine Finset.induction_on S ?empty ?insert
  · simp [hzero]
  · intro e S he ih
    calc
      J (restrictEdges (insert e S) ω)
          = J (edgeSingle e (ω e)) + J (restrictEdges S ω) := hsplit S e ω he
      _ = J (edgeSingle e (ω e)) + S.sum (fun x => J (edgeSingle x (ω x))) := by
            rw [ih]
      _ = (insert e S).sum (fun x => J (edgeSingle x (ω x))) := by
            rw [Finset.sum_insert he]

theorem separable_of_finite_disjoint_additive
    [Fintype E]
    (J : (E → V) → R)
    (hzero : J 0 = 0)
    (hsplit :
      ∀ (S : Finset E) (e : E) (ω : E → V),
        e ∉ S →
        J (restrictEdges (insert e S) ω) =
          J (edgeSingle e (ω e)) + J (restrictEdges S ω)) :
    ∃ j : E → V → R, ∀ ω : E → V, J ω = ∑ e : E, j e (ω e) := by
  refine ⟨fun e x => J (edgeSingle e x), ?_⟩
  intro ω
  have h := edge_decomposition_on_finset J hzero hsplit Finset.univ ω
  simpa using h

#print axioms restrictEdges_empty
#print axioms restrictEdges_univ
#print axioms edge_decomposition_on_finset
#print axioms separable_of_finite_disjoint_additive
