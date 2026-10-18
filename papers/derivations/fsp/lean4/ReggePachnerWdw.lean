


namespace ReggePachnerWdw

universe u

def sumDeficits : List Nat → Nat
  | [] => 0
  | d :: ds => d + sumDeficits ds

structure SimplicialVertex where
  incidentBoneDeficits : List Nat

def evaluateH_Wdw (v : SimplicialVertex) : Nat :=
  sumDeficits v.incidentBoneDeficits

def isFlatVertex (v : SimplicialVertex) : Prop :=
  ∀ d ∈ v.incidentBoneDeficits, d = 0

theorem flat_vertex_wdw_closure (v : SimplicialVertex) (h_flat : isFlatVertex v) :
    evaluateH_Wdw v = 0 := by
  dsimp [evaluateH_Wdw]
  have h_sum : ∀ (l : List Nat), (∀ d ∈ l, d = 0) → sumDeficits l = 0 := by
    intro l
    induction l with
    | nil => intros; rfl
    | cons head tail ih =>
      intro h_all
      dsimp [sumDeficits]
      have h_head : head = 0 := h_all head (List.Mem.head tail)
      have h_tail : ∀ d ∈ tail, d = 0 := fun d hd => h_all d (List.Mem.tail head hd)
      rw [h_head, ih h_tail]
  exact h_sum v.incidentBoneDeficits h_flat

theorem curved_pachner_induces_positive_defect (deficits : List Nat) (d : Nat)
    (h_in : d ∈ deficits) (h_pos : d > 0) :
    sumDeficits deficits > 0 := by
  induction deficits with
  | nil => nomatch h_in
  | cons head tail ih =>
    dsimp [sumDeficits]
    cases h_in with
    | head =>
      omega
    | tail _ h_tail =>
      have : sumDeficits tail > 0 := ih h_tail
      omega

theorem wdw_defect_unscreenable (p alpha h_wdw : Nat) (h_pos : h_wdw > 0) :
    (p - alpha) + h_wdw > 0 := by
  omega

end ReggePachnerWdw
