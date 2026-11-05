import WitnessedDifference.Succession

/-!
# Finite history decomposition
-/

namespace WitnessedDifference.History

abbrev FiniteHistory (Event : Type _) := List Event

def decomposeAt {Event : Type _} (cut : Nat)
    (history : FiniteHistory Event) :
    FiniteHistory Event × FiniteHistory Event :=
  (history.take cut, history.drop cut)

theorem decomposeAt_reconstruct {Event : Type _} (cut : Nat)
    (history : FiniteHistory Event) :
    (decomposeAt cut history).1 ++ (decomposeAt cut history).2 = history := by
  change history.take cut ++ history.drop cut = history
  exact List.take_append_drop cut history

def historyWeight {Event Weight : Type _} [AddMonoid Weight]
    (weight : Event → Weight) (history : FiniteHistory Event) : Weight :=
  (history.map weight).sum

theorem historyWeight_append
    {Event Weight : Type _} [AddMonoid Weight]
    (weight : Event → Weight)
    (first second : FiniteHistory Event) :
    historyWeight weight (first ++ second) =
      historyWeight weight first + historyWeight weight second := by
  unfold historyWeight
  rw [List.map_append]
  exact List.sum_append (first.map weight) (second.map weight)

end WitnessedDifference.History
