import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. State-relative enabled swaps compare complete
future observations, not raw endpoint identity. Rust finite quotients, search,
storage/admission and test-only method alpha renaming are separate refinements. -/
namespace TFQM.FiniteIndependence

variable {S I A W : Type}

def FutureEq (observe : S → List I → Option A) (x y : S) : Prop :=
  ∀ w, observe x w = observe y w

theorem future_refl (observe : S → List I → Option A) (x : S) : FutureEq observe x x :=
  fun _ => rfl
theorem future_symm (observe : S → List I → Option A) (x y : S)
    (h : FutureEq observe x y) : FutureEq observe y x := fun w => (h w).symm
theorem future_trans (observe : S → List I → Option A) (x y z : S)
    (h : FutureEq observe x y) (k : FutureEq observe y z) : FutureEq observe x z :=
  fun w => (h w).trans (k w)

theorem witness_refuses_future (observe : S → List I → Option A) (x y : S)
    (w : List I) (different : observe x w ≠ observe y w) : ¬ FutureEq observe x y :=
  fun h => different (h w)

theorem unequal_can_share_futures :
    FutureEq (fun (_ : Bool) (_ : List Nat) => some (0 : Nat)) false true := fun _ => rfl

def afterTwo (step : S → I → Option S) (s : S) (a b : I) : Option S :=
  (step s a).bind (fun t => step t b)

theorem defined_order_has_first_step (step : S → I → Option S) (s : S) (a b : I)
    (x : S) (defined : afterTwo step s a b = some x) : step s a ≠ none := by
  intro missing
  simp [afterTwo, missing] at defined

def Enabled (a b ab ba : Option S) : Prop := a ≠ none ∧ b ≠ none ∧ ab ≠ none ∧ ba ≠ none

theorem final_orders_enable_singles (step : S → I → Option S) (s : S) (a b : I)
    (x y : S) (ab : afterTwo step s a b = some x) (ba : afterTwo step s b a = some y) :
    Enabled (step s a) (step s b) (afterTwo step s a b) (afterTwo step s b a) := by
  exact ⟨defined_order_has_first_step step s a b x ab,
    defined_order_has_first_step step s b a y ba, by simp [ab], by simp [ba]⟩

theorem unavailable_never_enabled (a b ba : Option S) : ¬ Enabled a b none ba := by
  simp [Enabled]

def ValidWitness (observe : S → List I → Option A) (x y : S) (w : List I)
    (left right : Option A) : Prop :=
  observe x w = left ∧ observe y w = right ∧ left ≠ right

theorem witness_sound (observe : S → List I → Option A) (x y : S) (w : List I)
    (left right : Option A) (h : ValidWitness observe x y w left right) :
    ¬ FutureEq observe x y := by
  intro eq
  exact h.2.2 (h.1.symm.trans ((eq w).trans h.2.1))

theorem witness_uses_saved_answers (observe : S → List I → Option A) (x y : S)
    (w : List I) (left right : Option A) (h : ValidWitness observe x y w left right) :
    left = observe x w ∧ right = observe y w := ⟨h.1.symm, h.2.1.symm⟩

def endpointReplay [DecidableEq S] (expected claimed : S × S) (equivalent : Bool) : Bool :=
  decide (expected = claimed) && equivalent

theorem endpoint_replay [DecidableEq S] (expected claimed : S × S) (eq : Bool) :
    endpointReplay expected claimed eq = true ↔ expected = claimed ∧ eq = true := by
  simp [endpointReplay]

theorem endpoint_mismatch [DecidableEq S] (expected claimed : S × S) (ne : expected ≠ claimed)
    (eq : Bool) : endpointReplay expected claimed eq = false := by simp [endpointReplay, ne]

inductive Outcome (W : Type) where
  | unavailable | independent | distinguished (witness : W)
  deriving DecidableEq

def classify (enabled equivalent : Bool) (search : Except Unit W) : Except Unit (Outcome W) :=
  if !enabled then .ok .unavailable
  else if equivalent then .ok .independent
  else search.map Outcome.distinguished

theorem unavailable_ignores_search (eq : Bool) (search : Except Unit W) :
    classify false eq search = .ok .unavailable := by simp [classify]
theorem equivalent_ignores_search (search : Except Unit W) :
    classify true true search = .ok .independent := by simp [classify]
theorem distinction_requires_success (w : W) :
    classify true false (.ok w) = .ok (.distinguished w) := rfl
theorem resource_refusal_preserved :
    classify true false (.error () : Except Unit W) = .error () := rfl

end TFQM.FiniteIndependence

#print axioms TFQM.FiniteIndependence.future_refl
#print axioms TFQM.FiniteIndependence.future_symm
#print axioms TFQM.FiniteIndependence.future_trans
#print axioms TFQM.FiniteIndependence.witness_refuses_future
#print axioms TFQM.FiniteIndependence.unequal_can_share_futures
#print axioms TFQM.FiniteIndependence.defined_order_has_first_step
#print axioms TFQM.FiniteIndependence.final_orders_enable_singles
#print axioms TFQM.FiniteIndependence.unavailable_never_enabled
#print axioms TFQM.FiniteIndependence.witness_sound
#print axioms TFQM.FiniteIndependence.witness_uses_saved_answers
#print axioms TFQM.FiniteIndependence.endpoint_replay
#print axioms TFQM.FiniteIndependence.endpoint_mismatch
#print axioms TFQM.FiniteIndependence.unavailable_ignores_search
#print axioms TFQM.FiniteIndependence.equivalent_ignores_search
#print axioms TFQM.FiniteIndependence.distinction_requires_success
#print axioms TFQM.FiniteIndependence.resource_refusal_preserved
