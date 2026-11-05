import Init

namespace RealizableObservation

def Update {X O : Type} (z step : X → X → Prop) (report : X → O)
    (o : O) (x y' : X) : Prop :=
  ∃ y, z x y ∧ step y y' ∧ report y' = o

def Good {X K : Type} (k : X → K) (z : X → X → Prop) (c : K) : Prop :=
  ∀ x y, z x y → k x = c ∧ k y = c

theorem original_coordinate_retained {X O : Type} (z step : X → X → Prop)
    (report : X → O) (o : O) (x y' : X)
    (h : Update z step report o x y') : ∃ y, z x y := by
  obtain ⟨y, hz, _, _⟩ := h
  exact ⟨y, hz⟩

theorem update_twice {X O P : Type} (z s t : X → X → Prop)
    (r : X → O) (q : X → P) (o : O) (p : P) (x w : X) :
    Update (Update z s r o) t q p x w ↔
      ∃ u v, z x u ∧ s u v ∧ r v = o ∧ t v w ∧ q w = p := by
  constructor
  · intro h
    obtain ⟨v, ⟨u, hzu, hsv, hrv⟩, htw, hqw⟩ := h
    exact ⟨u, v, hzu, hsv, hrv, htw, hqw⟩
  · intro h
    obtain ⟨u, v, hzu, hsv, hrv, htw, hqw⟩ := h
    exact ⟨v, ⟨u, hzu, hsv, hrv⟩, htw, hqw⟩

theorem decoded_original_and_current {X K : Type} (k : X → K)
    (z : X → X → Prop) (c : K) (h : Good k z c) (x y : X) (hz : z x y) :
    k x = c ∧ k y = c := h x y hz

theorem decoder_unique_on_nonempty_relation {X K : Type} (k : X → K)
    (z : X → X → Prop) (c d : K) (hc : Good k z c) (hd : Good k z d)
    (nonempty : ∃ x y, z x y) : c = d := by
  obtain ⟨x, y, hz⟩ := nonempty
  exact (hc x y hz).1.symm.trans (hd x y hz).1

theorem same_current_set_need_not_decode_original :
    (∀ y : Bool, (∃ x, x = false ∧ y = false) ↔
      (∃ x, (x = false ∨ x = true) ∧ y = false)) ∧
    Good id (fun x y : Bool => x = false ∧ y = false) false ∧
    ¬ (∃ c, Good id (fun x y : Bool => (x = false ∨ x = true) ∧ y = false) c) := by
  constructor
  · intro y
    constructor
    · intro h
      obtain ⟨x, hx, hy⟩ := h
      exact ⟨x, Or.inl hx, hy⟩
    · intro h
      obtain ⟨_, _, hy⟩ := h
      exact ⟨false, rfl, hy⟩
  constructor
  · intro x y h
    exact h
  · intro h
    obtain ⟨c, hc⟩ := h
    have hf : false = c := (hc false false ⟨Or.inl rfl, rfl⟩).1
    have ht : true = c := (hc true false ⟨Or.inr rfl, rfl⟩).1
    cases hf.trans ht.symm

end RealizableObservation

#print axioms RealizableObservation.original_coordinate_retained
#print axioms RealizableObservation.update_twice
#print axioms RealizableObservation.decoded_original_and_current
#print axioms RealizableObservation.decoder_unique_on_nonempty_relation
#print axioms RealizableObservation.same_current_set_need_not_decode_original
