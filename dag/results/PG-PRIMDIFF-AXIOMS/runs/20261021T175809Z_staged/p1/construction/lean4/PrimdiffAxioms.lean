import Mathlib.GroupTheory.QuotientGroup.Defs
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Finset.Basic
import Mathlib.Logic.Relation
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Abel
import Mathlib.Order.Lattice.Nat
import Mathlib.Algebra.Order.Field.Rat

/-!
# Primitive-difference axioms A1-A10, the admission kernel, and what small models say about independence

AuthorityEffect: None.  This node is a DEFINITION: the Rust enum `PrimitiveDifferenceAxiom`
(`code/rust/src/wdp/primitive_axiomatics.rs`, line 24) lists ten axiom NAMES with no predicate attached, and
`GenesisAdmissionKernel::admit_difference` (line 38) enforces only A1 (`a != b`) and carrier membership.
The paper pin (tfq_0394) records the list as UNDERIVED: nothing here derives it, and independence or
consistency on tiny carriers is not a derivation.

What is proved here, for arbitrary types: the kernel's accept/refuse behaviour (the token is stored but never
checked; A1 is checked before carrier membership; duplicates and both orientations are accepted); the
cochain identity `d1 (d0 phi) = 0`; the exact condition under which a PARTIAL face boundary composes to zero
with `d0` (all three boundary edges present or all absent); that a coboundary `d1` descends to the quotient by
the image of `d0` iff `d1 o d0 = 0` (A7, read as `d1 vanishes on im d0`, is A5 again; that reading is ours); gauge invariance of any Nat-valued defect of the form `inf_phi N(h - d0 phi)` (A6; the rational-valued Phi1 of the source is not covered);
the exact/closed trichotomy and the one cell, `exact but not closed`, that is empty under nilpotency and
nonempty otherwise (where the TRANSCRIBED `R_cl` rule refuses; the source complex constructor rejects `d1 o d0 != 0`, so its None branch is not reachable through `compute_triad_signature`); and that the reflexive-transitive closure is
the least preorder containing a relation (A3).  Small concrete models are labelled instances.
-/

namespace PrimdiffAxioms

/-! ## The admission kernel -/

inductive KErr where
  | a1
  | carrier
  deriving DecidableEq

structure Kernel (N T : Type) where
  carrier : Finset N
  admitted : List (N × N × T)

variable {N T : Type} [DecidableEq N]

/-- Faithful transcription of `GenesisAdmissionKernel::admit_difference`: A1 is checked first, then carrier
membership; the token is stored and never inspected; duplicates are appended. -/
def Kernel.admit (k : Kernel N T) (a b : N) (tok : T) : Except KErr (Kernel N T) :=
  if a = b then .error .a1
  else if a ∈ k.carrier ∧ b ∈ k.carrier then .ok { k with admitted := k.admitted ++ [(a, b, tok)] }
  else .error .carrier

theorem admit_error_a1 (k : Kernel N T) (a : N) (tok : T) : k.admit a a tok = .error .a1 := by
  simp [Kernel.admit]

theorem admit_ok_iff (k : Kernel N T) (a b : N) (tok : T) :
    (∃ k', k.admit a b tok = .ok k') ↔ (a ≠ b ∧ a ∈ k.carrier ∧ b ∈ k.carrier) := by
  unfold Kernel.admit
  by_cases hab : a = b
  · simp [hab]
  · by_cases hc : a ∈ k.carrier ∧ b ∈ k.carrier
    · simp [hab, hc]
    · simp [hab, hc]

/-- The token plays no role in acceptance: with or without (any) token the same pairs are admitted. -/
theorem admit_token_irrelevant (k : Kernel N T) (a b : N) (t t' : T) :
    (∃ k', k.admit a b t = .ok k') ↔ (∃ k', k.admit a b t' = .ok k') := by
  rw [admit_ok_iff, admit_ok_iff]

/-- Invariant: every admitted pair is irreflexive (A1) and inside the carrier. -/
def Kernel.Inv (k : Kernel N T) : Prop :=
  ∀ x ∈ k.admitted, x.1 ≠ x.2.1 ∧ x.1 ∈ k.carrier ∧ x.2.1 ∈ k.carrier

theorem admit_preserves_inv (k k' : Kernel N T) (a b : N) (tok : T) (hk : k.Inv) (h : k.admit a b tok = .ok k') :
    k'.Inv := by
  have hok := (admit_ok_iff k a b tok).mp ⟨k', h⟩
  unfold Kernel.admit at h
  simp only [hok.1, hok.2.1, hok.2.2, and_self, ite_false, ite_true] at h
  cases h
  intro x hx
  simp only [List.mem_append, List.mem_singleton] at hx
  rcases hx with hx | rfl
  · exact hk x hx
  · exact hok

/-- Instance: the same ordered pair twice is stored twice. -/
theorem duplicates_stored :
    ((((⟨{0, 1}, []⟩ : Kernel Nat Nat).admit 0 1 0).toOption.bind (fun k1 => (k1.admit 0 1 0).toOption)).map
      (fun k => k.admitted.length)) = some 2 := by
  decide

/-- Instance: both orientations of a pair are accepted. -/
theorem reverse_orientation_accepted :
    ((((⟨{0, 1}, []⟩ : Kernel Nat Nat).admit 0 1 0).toOption.bind (fun k1 => (k1.admit 1 0 0).toOption)).isSome) = true := by
  decide

/-! ## A3: the reflexive-transitive closure is the least preorder containing the relation -/

theorem rtc_preorder {V : Type} (r : V → V → Prop) :
    (∀ a, Relation.ReflTransGen r a a) ∧ (∀ a b c, Relation.ReflTransGen r a b → Relation.ReflTransGen r b c → Relation.ReflTransGen r a c) ∧
      ∀ a b, r a b → Relation.ReflTransGen r a b :=
  ⟨fun _ => Relation.ReflTransGen.refl, fun _ _ _ h1 h2 => Relation.ReflTransGen.trans h1 h2,
    fun _ _ h => Relation.ReflTransGen.single h⟩

theorem rtc_least {V : Type} (r P : V → V → Prop) (hr : ∀ a, P a a) (ht : ∀ a b c, P a b → P b c → P a c)
    (hsub : ∀ a b, r a b → P a b) : ∀ a b, Relation.ReflTransGen r a b → P a b := by
  intro a b h
  induction h with
  | refl => exact hr _
  | tail _ hbc ih => exact ht _ _ _ ih (hsub _ _ hbc)

/-! ## Cochains: A5 (nilpotence), A6 (gauge), A7 (descent) -/

section Cochain

variable {V : Type}

def d0 (φ : V → ℤ) (u v : V) : ℤ := φ v - φ u

/-- Degree-one coboundary on a face `(a, b, c)` with all three boundary edges present. -/
def d1 (ψ : V → V → ℤ) (a b c : V) : ℤ := ψ b c - ψ a c + ψ a b

theorem d1_d0 (φ : V → ℤ) (a b c : V) : d1 (d0 φ) a b c = 0 := by
  simp only [d1, d0]; ring

/-- Coboundary when only the edges flagged by `p` are present (absent edges contribute nothing). -/
def d1E (p : V → V → Bool) (ψ : V → V → ℤ) (a b c : V) : ℤ :=
  (if p b c then ψ b c else 0) - (if p a c then ψ a c else 0) + (if p a b then ψ a b else 0)

def unit [DecidableEq V] (x : V) : V → ℤ := fun v => if v = x then 1 else 0

/-- For a face with distinct vertices, `d1 o d0 = 0` holds exactly when the three boundary edges are all
present or all absent (a floating face composes to zero; a half-attached face does not). -/
theorem face_nilpotent_iff [DecidableEq V] (p : V → V → Bool) {a b c : V} (hab : a ≠ b) (hbc : b ≠ c) (hac : a ≠ c) :
    (∀ φ : V → ℤ, d1E p (d0 φ) a b c = 0) ↔ (p a b = p b c ∧ p b c = p a c) := by
  constructor
  · intro h
    have ea := h (unit a)
    have eb := h (unit b)
    have ec := h (unit c)
    simp only [d1E, d0, unit, hab, hbc, hac, hab.symm, hbc.symm, hac.symm] at ea eb ec
    revert ea eb ec
    cases p a b <;> cases p b c <;> cases p a c <;> simp
  · rintro ⟨h1, h2⟩ φ
    have h3 : p a b = p a c := h1.trans h2
    simp only [d1E, d0, h3, h2]
    rcases Bool.eq_false_or_eq_true (p a c) with h | h <;> simp [h]

/-- A7 is A5 again: a coboundary map `d1` factors through the quotient by the image of `d0` iff `d1 o d0 = 0`. -/
theorem descends_iff {A B C : Type} [AddCommGroup A] [AddCommGroup B] [AddCommGroup C] (d0 : A →+ B) (d1 : B →+ C) :
    (∃ g : (B ⧸ d0.range) →+ C, ∀ b : B, g (b : B ⧸ d0.range) = d1 b) ↔ d1.comp d0 = 0 := by
  constructor
  · rintro ⟨g, hg⟩
    ext a
    have h1 := hg (d0 a)
    have h2 : ((d0 a : B) : B ⧸ d0.range) = 0 := (QuotientAddGroup.eq_zero_iff _).mpr ⟨a, rfl⟩
    rw [h2, map_zero] at h1
    simpa using h1.symm
  · intro h
    refine ⟨QuotientAddGroup.lift d0.range d1 ?_, fun b => rfl⟩
    rintro x ⟨a, rfl⟩
    exact DFunLike.congr_fun h a

/-- A6: any defect defined as an infimum over gauge shifts is invariant under a gauge shift of its argument. -/
theorem defect_gauge_invariant {A B : Type} [AddCommGroup A] [AddCommGroup B] (d0 : A →+ B) (N : B → ℕ) (h : B) (ψ : A) :
    sInf (Set.range fun φ : A => N (h + d0 ψ - d0 φ)) = sInf (Set.range fun φ : A => N (h - d0 φ)) := by
  congr 1
  ext x
  constructor
  · rintro ⟨φ, rfl⟩
    exact ⟨φ - ψ, by simp only [map_sub]; congr 1; abel⟩
  · rintro ⟨φ, rfl⟩
    exact ⟨φ + ψ, by simp only [map_add]; congr 1; abel⟩

/-! ## The exact / closed trichotomy and the refusal of `R_cl` -/

def Exact {A B : Type} [AddCommGroup A] [AddCommGroup B] (d0 : A →+ B) (h : B) : Prop := ∃ φ, h = d0 φ

/-- Under nilpotence the cell "exact but not closed" is empty. -/
theorem exact_closed {A B C : Type} [AddCommGroup A] [AddCommGroup B] [AddCommGroup C] (d0 : A →+ B) (d1 : B →+ C)
    (hn : d1.comp d0 = 0) (h : B) (he : Exact d0 h) : d1 h = 0 := by
  obtain ⟨φ, rfl⟩ := he
  exact DFunLike.congr_fun hn φ

/-- Without nilpotence that cell is nonempty. -/
theorem exact_not_closed {A B C : Type} [AddCommGroup A] [AddCommGroup B] [AddCommGroup C] (d0 : A →+ B) (d1 : B →+ C)
    (hn : d1.comp d0 ≠ 0) : ∃ h : B, Exact d0 h ∧ d1 h ≠ 0 := by
  by_contra hcon
  apply hn
  ext a
  by_contra hne
  exact hcon ⟨d0 a, ⟨a, rfl⟩, hne⟩

/-- Trichotomy under nilpotence: every degree-one cochain is exact, or closed and not exact, or not closed. -/
theorem trichotomy {A B C : Type} [AddCommGroup A] [AddCommGroup B] [AddCommGroup C] (d0 : A →+ B) (d1 : B →+ C)
    (hn : d1.comp d0 = 0) (h : B) :
    (Exact d0 h ∧ d1 h = 0) ∨ (¬ Exact d0 h ∧ d1 h = 0) ∨ (¬ Exact d0 h ∧ d1 h ≠ 0) := by
  by_cases he : Exact d0 h
  · exact Or.inl ⟨he, exact_closed d0 d1 hn h he⟩
  · by_cases hc : d1 h = 0
    · exact Or.inr (Or.inl ⟨he, hc⟩)
    · exact Or.inr (Or.inr ⟨he, hc⟩)

/-- The `R_cl` rule of `TriadSignature::r_cl`: gamma/phi when phi is nonzero, zero when both vanish, refusal
(none) when phi vanishes and gamma does not. -/
def rcl (φ γ : ℚ) : Option ℚ := if φ ≠ 0 then some (γ / φ) else if γ = 0 then some 0 else none

theorem rcl_eq_none_iff (φ γ : ℚ) : rcl φ γ = none ↔ (φ = 0 ∧ γ ≠ 0) := by
  unfold rcl
  by_cases h1 : φ = 0 <;> by_cases h2 : γ = 0 <;> simp [h1, h2]

/-- If the two numbers vanish exactly on exact and on closed cochains (hypotheses about the functionals, not
claims about them), nilpotence makes `R_cl` defined for every cochain. -/
theorem rcl_defined_of_nilpotent {A B C : Type} [AddCommGroup A] [AddCommGroup B] [AddCommGroup C]
    (d0 : A →+ B) (d1 : B →+ C) (hn : d1.comp d0 = 0) (h : B) (Φ Γ : ℚ)
    (hΦ : Φ = 0 ↔ Exact d0 h) (hΓ : Γ = 0 ↔ d1 h = 0) : rcl Φ Γ ≠ none := by
  intro hnone
  obtain ⟨h1, h2⟩ := (rcl_eq_none_iff Φ Γ).mp hnone
  exact h2 (hΓ.mpr (exact_closed d0 d1 hn h (hΦ.mp h1)))

/-- Without nilpotence the refusal cell is reachable: phi = 0 and gamma = 1 refuses. -/
theorem rcl_refuses_zero_one : rcl 0 1 = none := by
  rw [rcl_eq_none_iff]; norm_num

end Cochain

/-! ## Instances: small models of the transcribed predicates (labelled instances, not general) -/

def A1 {n : ℕ} (D : Fin n → Fin n → Bool) : Prop := ∀ a, D a a = false

def A4 {n : ℕ} (E : Fin n → Fin n → Bool) : Prop := (∀ a, E a a = false) ∧ ∀ a b, E a b = true → E b a = false

/-- A5 for the single face (0,1,2) on three vertices, in the equivalent form of `face_nilpotent_iff`. -/
def A5 (E : Fin 3 → Fin 3 → Bool) (F : Bool) : Prop := F = true → (E 0 1 = E 1 2 ∧ E 1 2 = E 0 2)

/-- The decidable form `A5` of the instance section is the nilpotence of the partial coboundary on the face (0,1,2). -/
theorem a5_iff_nilpotent (E : Fin 3 → Fin 3 → Bool) :
    A5 E true ↔ ∀ φ : Fin 3 → ℤ, d1E E (d0 φ) 0 1 2 = 0 := by
  rw [face_nilpotent_iff E (by decide) (by decide) (by decide)]
  unfold A5
  simp

instance {n : ℕ} (D : Fin n → Fin n → Bool) : Decidable (A1 D) := by unfold A1; infer_instance
instance {n : ℕ} (E : Fin n → Fin n → Bool) : Decidable (A4 E) := by unfold A4; infer_instance
instance (E : Fin 3 → Fin 3 → Bool) (F : Bool) : Decidable (A5 E F) := by unfold A5; infer_instance

/-- Instance: A1, A4, A5 are pairwise independent on three vertices: for each one there is a structure that
violates it and satisfies the other two.  (A5 can only be violated from three vertices on.) -/
theorem a1_a4_a5_independent_on_three_vertices :
    (∃ (D E : Fin 3 → Fin 3 → Bool) (F : Bool), ¬ A1 D ∧ A4 E ∧ A5 E F) ∧
    (∃ (D E : Fin 3 → Fin 3 → Bool) (F : Bool), A1 D ∧ ¬ A4 E ∧ A5 E F) ∧
    (∃ (D E : Fin 3 → Fin 3 → Bool) (F : Bool), A1 D ∧ A4 E ∧ ¬ A5 E F) := by
  refine ⟨⟨fun _ _ => true, fun _ _ => false, false, by decide⟩,
          ⟨fun _ _ => false, fun _ _ => true, false, by decide⟩,
          ⟨fun _ _ => false, fun a b => decide (a = 0 ∧ b = 1), true, by decide⟩⟩

/-- Instance: the empty structure satisfies every transcribed predicate, so nothing in them forces an admission. -/
theorem empty_structure_is_a_model :
    A1 (fun (_ _ : Fin 3) => false) ∧ A4 (fun (_ _ : Fin 3) => false) ∧ A5 (fun _ _ => false) true :=
  ⟨by decide, by decide, by decide⟩

end PrimdiffAxioms

#print axioms PrimdiffAxioms.admit_error_a1
#print axioms PrimdiffAxioms.admit_ok_iff
#print axioms PrimdiffAxioms.admit_token_irrelevant
#print axioms PrimdiffAxioms.admit_preserves_inv
#print axioms PrimdiffAxioms.duplicates_stored
#print axioms PrimdiffAxioms.reverse_orientation_accepted
#print axioms PrimdiffAxioms.rtc_preorder
#print axioms PrimdiffAxioms.rtc_least
#print axioms PrimdiffAxioms.d1_d0
#print axioms PrimdiffAxioms.face_nilpotent_iff
#print axioms PrimdiffAxioms.descends_iff
#print axioms PrimdiffAxioms.defect_gauge_invariant
#print axioms PrimdiffAxioms.exact_closed
#print axioms PrimdiffAxioms.exact_not_closed
#print axioms PrimdiffAxioms.trichotomy
#print axioms PrimdiffAxioms.rcl_eq_none_iff
#print axioms PrimdiffAxioms.rcl_defined_of_nilpotent
#print axioms PrimdiffAxioms.rcl_refuses_zero_one
#print axioms PrimdiffAxioms.a5_iff_nilpotent
#print axioms PrimdiffAxioms.a1_a4_a5_independent_on_three_vertices
#print axioms PrimdiffAxioms.empty_structure_is_a_model
