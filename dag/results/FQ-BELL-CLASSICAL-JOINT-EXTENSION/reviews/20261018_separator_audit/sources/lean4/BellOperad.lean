import BellClassicalJointExtension

/- Finite coloured endomorphism operations, in simultaneous-substitution form.
   Sigma indexing makes the ordered block flattening explicit. Restrict I,J,K to
   finite ordered carriers for the nonsymmetric operad. No symmetric action or
   arbitrary syntactic quotient presentation is claimed. AuthorityEffect: None. -/
namespace QuantumMechanics.BellOperad

abbrev Op (I : Type) (A : I → Type) (B : Type) := ((i : I) → A i) → B

def identity (A : Type) : Op Unit (fun _ => A) A := fun x => x ()

def substitute {I : Type} {B : I → Type} {C : Type}
    {J : I → Type} {A : (i : I) → J i → Type}
    (f : Op I B C) (g : (i : I) → Op (J i) (A i) (B i)) :
    Op (Sigma J) (fun ij => A ij.1 ij.2) C :=
  fun x => f (fun i => g i (fun j => x ⟨i, j⟩))

theorem substitute_left_unit {I : Type} {A : I → Type} {B : Type}
    (g : Op I A B) (x : (i : I) → A i) :
    substitute (identity B) (fun _ => g) (fun ij => x ij.2) = g x := rfl

theorem substitute_right_unit {I : Type} {A : I → Type} {B : Type}
    (f : Op I A B) (x : (i : I) → A i) :
    substitute f (fun i => identity (A i)) (fun ij => x ij.1) = f x := rfl

theorem substitute_assoc {I : Type} {B : I → Type} {C : Type}
    {J : I → Type} {A : (i : I) → J i → Type}
    {K : (i : I) → J i → Type} {X : (i : I) → (j : J i) → K i j → Type}
    (f : Op I B C) (g : (i : I) → Op (J i) (A i) (B i))
    (h : (i : I) → (j : J i) → Op (K i j) (X i j) (A i j))
    (x : (i : I) → (j : J i) → (k : K i j) → X i j k) :
    substitute (substitute f g) (fun ij => h ij.1 ij.2)
      (fun ijk => x ijk.1.1 ijk.1.2 ijk.2) =
    substitute f (fun i => substitute (g i) (h i))
      (fun ijk => x ijk.1 ijk.2.1 ijk.2.2) := rfl

-- Semantic equality of operations is stable under all well-typed graftings.
-- This is not a completeness claim for a finitely presented syntactic quotient.
theorem substitute_congr {I : Type} {B : I → Type} {C : Type}
    {J : I → Type} {A : (i : I) → J i → Type}
    (f f' : Op I B C) (g g' : (i : I) → Op (J i) (A i) (B i))
    (hf : f = f') (hg : ∀ i, g i = g' i) : substitute f g = substitute f' g' := by
  cases hf
  have hgg : g = g' := funext hg
  rw [hgg]

open BellClassicalJointExtension

abbrev Four := Fin 4 → Int
def chsh (x : Four) : Int := x 0 + x 1 + x 2 - x 3

def products (a : Assignment) : Four := fun j => match j.val with
  | 0 => sign a.a0 * sign a.b0
  | 1 => sign a.a0 * sign a.b1
  | 2 => sign a.a1 * sign a.b0
  | _ => sign a.a1 * sign a.b1

def expect4 (table : Assignment → Four) : List (Nat × Assignment) → Four
  | [] => fun _ => 0
  | (w,a)::rest => fun j => (w : Int) * table a j + expect4 table rest j

def weighted (f : Assignment → Int) : List (Nat × Assignment) → Int
  | [] => 0
  | (w,a)::rest => (w : Int) * f a + weighted f rest

-- Generic linearity, not just the fixed +/-1 product table. No bound is implied
-- for an arbitrary table. Divide by the common positive denominator externally.
theorem expect_chsh (table : Assignment → Four) (law : List (Nat × Assignment)) :
    chsh (expect4 table law) = weighted (fun a => chsh (table a)) law := by
  induction law with
  | nil => rfl
  | cons p rest ih =>
    rcases p with ⟨w,a⟩
    simp only [expect4, weighted]
    simp only [chsh, Int.mul_add, Int.mul_sub] at ih ⊢
    omega

theorem products_score (a : Assignment) : chsh (products a) = score a := by
  rcases a with ⟨a0,a1,b0,b1⟩
  cases a0 <;> cases a1 <;> cases b0 <;> cases b1 <;> decide

theorem bell_evaluation (law : List (Nat × Assignment)) :
    chsh (expect4 products law) = numerator law := by
  rw [expect_chsh]
  induction law with
  | nil => rfl
  | cons p rest ih =>
    rcases p with ⟨w,a⟩
    change (w : Int) * chsh (products a) + weighted (fun a => chsh (products a)) rest =
      (w : Int) * score a + numerator rest
    rw [products_score, ih]

theorem bell_bound (law : List (Nat × Assignment)) (D : Nat)
    (hD : 0 < D) (hmass : mass law = (D : Int)) :
    (0 : Int) < (D : Int) ∧
    (-2 * (D : Int) ≤ chsh (expect4 products law) ∧
      chsh (expect4 products law) ≤ 2 * (D : Int)) := by
  rw [bell_evaluation]
  exact normalized_joint_bound law D hD hmass

-- The actual heterogeneous Bell operations, including the nullary product map.
def productsOp : Op Empty (fun _ => Unit) (Assignment → Four) := fun _ => products
def expectationOp : Op Bool
    (fun b => if b then Assignment → Four else List (Nat × Assignment)) Four :=
  fun x => expect4 (x true) (x false)
def chshOp : Op Unit (fun _ => Four) Int := fun x => chsh (x ())

def bellInputs (law : List (Nat × Assignment)) :
    (b : Bool) → (if b then Assignment → Four else List (Nat × Assignment))
  | false => law
  | true => products

theorem bell_graft (law : List (Nat × Assignment)) :
    substitute chshOp (fun _ => expectationOp)
      (fun ij => bellInputs law ij.2) =
    numerator law := by
  change chsh (expect4 products law) = numerator law
  exact bell_evaluation law


-- Actual nullary graft: the false input gets the law identity, while the true
-- input gets productsOp with NO input. This closes the fixed table as a tree,
-- rather than supplying it through a captured ordinary value.
def productSlots : Bool → Type
  | false => Unit
  | true => Empty

def productColours : (b : Bool) → productSlots b → Type
  | false => fun _ => List (Nat × Assignment)
  | true => fun _ => Unit

def productGenerators : (b : Bool) → Op (productSlots b) (productColours b)
    (if b then Assignment → Four else List (Nat × Assignment))
  | false => identity (List (Nat × Assignment))
  | true => productsOp

def productLawInputs (law : List (Nat × Assignment)) :
    (ij : Sigma productSlots) → productColours ij.1 ij.2
  | ⟨false, ()⟩ => law
  | ⟨true, e⟩ => nomatch e

theorem bell_nullary_graft (law : List (Nat × Assignment)) :
    substitute chshOp (fun _ => substitute expectationOp productGenerators)
      (fun ij => productLawInputs law ij.2) = numerator law := by
  change chsh (expect4 products law) = numerator law
  exact bell_evaluation law

end QuantumMechanics.BellOperad

#print axioms QuantumMechanics.BellOperad.substitute_left_unit
#print axioms QuantumMechanics.BellOperad.substitute_right_unit
#print axioms QuantumMechanics.BellOperad.substitute_assoc
#print axioms QuantumMechanics.BellOperad.substitute_congr
#print axioms QuantumMechanics.BellOperad.expect_chsh
#print axioms QuantumMechanics.BellOperad.bell_evaluation
#print axioms QuantumMechanics.BellOperad.bell_bound

#print axioms QuantumMechanics.BellOperad.bell_nullary_graft
