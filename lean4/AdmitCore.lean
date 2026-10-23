/-!
# Admit core

AuthorityEffect: None.

Deep embedding of a finite fragment of the Genesis regime calculus as recorded in
this repository: admitted data, forms, and distinction-cuts; state changes by
admission steps; supply does not change the regime (TFQ-0378, TFQ-0379).
The irreflexive ban on a cut is part of the admission rule, not a consequence of
having two names (TFQ-0387, `lean4/AdmissionFloor.lean`). Positive form arity and
deduplicating re-admission are not rules here (TFQ-0378). Rules, requirements,
readings L and F, impose, S(n), and MSS-N are not core constructors.
-/

namespace AdmitCore

inductive Kind where
  | dataK
  | distK

inductive Expr where
  | token : Nat → Expr
  | datum : Nat → Expr
  | form : Nat → List Nat → Expr
  | cut : Nat → Nat → Expr

inductive Event where
  | supply : Nat → Event
  | admitData : Nat → Event
  | admitForm : Nat → Nat → Event
  | admitCut : Nat → Nat → Event
  | impose : Event

inductive Judg where
  | typed : Expr → Kind → Judg
  | admittedData : Nat → Judg
  | admittedForm : Nat → Nat → Judg
  | admittedCut : Nat → Nat → Judg
  | apart : Nat → Nat → Judg

/-- Three of the five regime fields. Rules and requirements are not stored. -/
structure Regime where
  data : List Nat
  forms : List (Nat × Nat)
  cuts : List (Nat × Nat)

def Regime.empty : Regime where
  data := []
  forms := []
  cuts := []

inductive Step : Regime → Event → Regime → Prop where
  | supply : Step Γ (.supply n) Γ
  | admitData : Step Γ (.admitData n) { Γ with data := n :: Γ.data }
  | admitForm : Step Γ (.admitForm i k) { Γ with forms := (i, k) :: Γ.forms }
  | admitCut :
      a ∈ Γ.data → b ∈ Γ.data → a ≠ b →
        Step Γ (.admitCut a b) { Γ with cuts := (a, b) :: Γ.cuts }

inductive Typed : Regime → Expr → Kind → Prop where
  | datum : n ∈ Γ.data → Typed Γ (.datum n) .dataK
  | formApp :
      (i, idx.length) ∈ Γ.forms →
        (∀ n, n ∈ idx → n ∈ Γ.data) →
          Typed Γ (.form i idx) .dataK
  | cut :
      a ∈ Γ.data → b ∈ Γ.data → (a, b) ∈ Γ.cuts → a ≠ b →
        Typed Γ (.cut a b) .distK

inductive Holds : Regime → Judg → Prop where
  | typed : Typed Γ e k → Holds Γ (.typed e k)
  | admittedData : n ∈ Γ.data → Holds Γ (.admittedData n)
  | admittedForm : (i, k) ∈ Γ.forms → Holds Γ (.admittedForm i k)
  | admittedCut : (a, b) ∈ Γ.cuts → a ≠ b → Holds Γ (.admittedCut a b)
  | apart : (a, b) ∈ Γ.cuts → a ≠ b → Holds Γ (.apart a b)

inductive Reaches : Regime → Regime → Prop where
  | refl : Reaches Γ Γ
  | step : Step Γ e Γ' → Reaches Γ' Δ → Reaches Γ Δ

theorem supply_noop {Γ Γ' : Regime} {n : Nat} (h : Step Γ (.supply n) Γ') : Γ' = Γ := by
  cases h
  rfl

theorem impose_no_step (Γ Γ' : Regime) : ¬ Step Γ .impose Γ' := by
  intro h
  cases h

theorem self_cut_refused {Γ Γ' : Regime} {n : Nat} : ¬ Step Γ (.admitCut n n) Γ' := by
  intro h
  cases h with
  | admitCut _ _ ne => exact ne rfl

theorem data_mono {Γ Γ' : Regime} {ev : Event} (hS : Step Γ ev Γ') {n : Nat}
    (h : n ∈ Γ.data) : n ∈ Γ'.data := by
  cases hS with
  | supply => exact h
  | admitData => exact List.Mem.tail _ h
  | admitForm => exact h
  | admitCut _ _ _ => exact h

theorem forms_mono {Γ Γ' : Regime} {ev : Event} (hS : Step Γ ev Γ') {p : Nat × Nat}
    (h : p ∈ Γ.forms) : p ∈ Γ'.forms := by
  cases hS with
  | supply => exact h
  | admitData => exact h
  | admitForm => exact List.Mem.tail _ h
  | admitCut _ _ _ => exact h

theorem cuts_mono {Γ Γ' : Regime} {ev : Event} (hS : Step Γ ev Γ') {p : Nat × Nat}
    (h : p ∈ Γ.cuts) : p ∈ Γ'.cuts := by
  cases hS with
  | supply => exact h
  | admitData => exact h
  | admitForm => exact h
  | admitCut _ _ _ => exact List.Mem.tail _ h

theorem typed_preserved {Γ Γ' : Regime} {ev : Event} (hS : Step Γ ev Γ') {e : Expr} {k : Kind}
    (h : Typed Γ e k) : Typed Γ' e k := by
  cases h with
  | datum hm => exact Typed.datum (data_mono hS hm)
  | formApp hf hall =>
    exact Typed.formApp (forms_mono hS hf) (fun n hn => data_mono hS (hall n hn))
  | cut ha hb hc ne =>
    exact Typed.cut (data_mono hS ha) (data_mono hS hb) (cuts_mono hS hc) ne

theorem holds_preserved {Γ Γ' : Regime} {ev : Event} (hS : Step Γ ev Γ') {J : Judg}
    (h : Holds Γ J) : Holds Γ' J := by
  cases h with
  | typed ht => exact Holds.typed (typed_preserved hS ht)
  | admittedData hm => exact Holds.admittedData (data_mono hS hm)
  | admittedForm hf => exact Holds.admittedForm (forms_mono hS hf)
  | admittedCut hc ne => exact Holds.admittedCut (cuts_mono hS hc) ne
  | apart hc ne => exact Holds.apart (cuts_mono hS hc) ne

theorem holds_reaches : ∀ {Γ Δ : Regime}, Reaches Γ Δ → ∀ {J : Judg}, Holds Γ J → Holds Δ J
  | _, _, .refl, _, h => h
  | _, _, .step hS hRest, _, h => holds_reaches hRest (holds_preserved hS h)

theorem typed_reaches : ∀ {Γ Δ : Regime}, Reaches Γ Δ → ∀ {e : Expr} {k : Kind},
    Typed Γ e k → Typed Δ e k
  | _, _, .refl, _, _, h => h
  | _, _, .step hS hRest, _, _, h => typed_reaches hRest (typed_preserved hS h)

theorem endpoints_apart {Γ : Regime} {a b : Nat} (h : Holds Γ (.admittedCut a b)) : a ≠ b := by
  cases h with
  | admittedCut _ ne => exact ne

theorem apart_iff_cut {Γ : Regime} {a b : Nat} :
    Holds Γ (.apart a b) ↔ Holds Γ (.admittedCut a b) := by
  constructor
  · intro h
    cases h with
    | apart hm ne => exact Holds.admittedCut hm ne
  · intro h
    cases h with
    | admittedCut hm ne => exact Holds.apart hm ne

/-- Preserving an admitted cut into an irreflexive target separates the images.
The target relation is supplied data. -/
theorem identification_breaks_law {Γ : Regime} {a b : Nat} (f : Nat → Nat)
    (target : Nat → Nat → Prop) (h : Holds Γ (.admittedCut a b))
    (pres : Holds Γ (.admittedCut a b) → target (f a) (f b))
    (law : ∀ x, ¬ target x x) : f a ≠ f b := by
  intro same
  have htarget : target (f a) (f b) := pres h
  rw [same] at htarget
  exact law (f b) htarget

theorem token_not_typed (Γ : Regime) (n : Nat) (k : Kind) : ¬ Typed Γ (.token n) k := by
  intro h
  cases h

def twoData : Regime where
  data := [0, 1]
  forms := []
  cuts := []

theorem distinct_not_cut : ¬ Holds twoData (.admittedCut 0 1) := by
  intro h
  cases h with
  | admittedCut hm _ => cases hm

def forwardCut : Regime where
  data := [0, 1]
  forms := []
  cuts := [(0, 1)]

theorem reverse_not_held : ¬ Holds forwardCut (.admittedCut 1 0) := by
  intro h
  cases h with
  | admittedCut hm _ =>
    cases hm with
    | tail _ hm => cases hm

theorem empty_not_apart : ¬ Holds Regime.empty (.apart 0 1) := by
  intro h
  cases h with
  | apart hm _ => cases hm

theorem supply_not_admit (n : Nat) {Γ' : Regime} (h : Step Regime.empty (.supply n) Γ') :
    ¬ Holds Γ' (.admittedData n) := by
  cases h with
  | supply =>
    intro hH
    cases hH with
    | admittedData hm => cases hm

def nullary : Regime := { Regime.empty with forms := [(0, 0)] }

theorem zero_arity_step : Step Regime.empty (.admitForm 0 0) nullary := Step.admitForm

theorem zero_arity_types : Typed nullary (.form 0 []) .dataK := by
  refine Typed.formApp ?_ ?_
  · exact List.Mem.head []
  · intro n hn
    cases hn

theorem readmit_present (Γ : Regime) (n : Nat) (h : n ∈ Γ.data) :
    Step Γ (.admitData n) { Γ with data := n :: Γ.data } ∧ n ∈ Γ.data :=
  ⟨Step.admitData, h⟩

def regime1 : Regime := { Regime.empty with data := 0 :: Regime.empty.data }

def regime2 : Regime := { regime1 with data := 1 :: regime1.data }

def regime3 : Regime := { regime2 with cuts := (0, 1) :: regime2.cuts }

theorem regime2_mem0 : 0 ∈ regime2.data :=
  List.Mem.tail 1 (List.Mem.head (a := 0) [])

theorem regime2_mem1 : 1 ∈ regime2.data := List.Mem.head regime1.data

theorem regime3_mem_cut : (0, 1) ∈ regime3.cuts := List.Mem.head []

theorem reaches_example : Reaches Regime.empty regime3 :=
  Reaches.step (Step.admitData (n := 0))
    (Reaches.step (Step.admitData (Γ := regime1) (n := 1))
      (Reaches.step
        (Step.admitCut (a := 0) (b := 1) regime2_mem0 regime2_mem1 Nat.zero_ne_one)
        Reaches.refl))

theorem example_apart : Holds regime3 (.apart 0 1) :=
  Holds.apart regime3_mem_cut Nat.zero_ne_one

theorem example_admitted_cut : Holds regime3 (.admittedCut 0 1) :=
  Holds.admittedCut regime3_mem_cut Nat.zero_ne_one

theorem example_typed_cut : Typed regime3 (.cut 0 1) .distK :=
  Typed.cut regime2_mem0 regime2_mem1 regime3_mem_cut Nat.zero_ne_one

theorem wrong_arity_not_typed : ¬ Typed nullary (.form 0 [1]) .dataK := by
  intro h
  cases h with
  | formApp hf _ =>
    cases hf with
    | tail _ hf => cases hf

end AdmitCore

#print axioms AdmitCore.supply_noop
#print axioms AdmitCore.impose_no_step
#print axioms AdmitCore.self_cut_refused
#print axioms AdmitCore.data_mono
#print axioms AdmitCore.forms_mono
#print axioms AdmitCore.cuts_mono
#print axioms AdmitCore.typed_preserved
#print axioms AdmitCore.holds_preserved
#print axioms AdmitCore.holds_reaches
#print axioms AdmitCore.typed_reaches
#print axioms AdmitCore.endpoints_apart
#print axioms AdmitCore.apart_iff_cut
#print axioms AdmitCore.identification_breaks_law
#print axioms AdmitCore.token_not_typed
#print axioms AdmitCore.distinct_not_cut
#print axioms AdmitCore.reverse_not_held
#print axioms AdmitCore.empty_not_apart
#print axioms AdmitCore.supply_not_admit
#print axioms AdmitCore.zero_arity_step
#print axioms AdmitCore.zero_arity_types
#print axioms AdmitCore.readmit_present
#print axioms AdmitCore.regime2_mem0
#print axioms AdmitCore.regime2_mem1
#print axioms AdmitCore.regime3_mem_cut
#print axioms AdmitCore.reaches_example
#print axioms AdmitCore.example_apart
#print axioms AdmitCore.example_admitted_cut
#print axioms AdmitCore.example_typed_cut
#print axioms AdmitCore.wrong_arity_not_typed
