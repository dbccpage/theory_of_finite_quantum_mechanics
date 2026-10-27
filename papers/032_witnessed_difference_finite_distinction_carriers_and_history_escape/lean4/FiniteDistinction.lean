/-
Finite horizon relations for a deterministic Moore machine.

R_0 is the kernel of the observation. R_{n+1} keeps a pair only when the
observations agree and every one-step update lands in one R_n class.
-/

namespace Wd2

def related (observe : Nat → Nat) (update : Nat → Nat → Nat) (alphabet : List Nat) :
    Nat → Nat → Nat → Bool
  | 0, s, t => observe s == observe t
  | n + 1, s, t =>
      (observe s == observe t) &&
        alphabet.all fun σ => related observe update alphabet n (update s σ) (update t σ)

theorem related_refl (observe : Nat → Nat) (update : Nat → Nat → Nat)
    (alphabet : List Nat) (n s : Nat) :
    related observe update alphabet n s s = true := by
  induction n generalizing s with
  | zero => simp [related]
  | succ n ih =>
      simp [related, List.all_eq_true, ih]

theorem related_symm (observe : Nat → Nat) (update : Nat → Nat → Nat)
    (alphabet : List Nat) (n s t : Nat)
    (h : related observe update alphabet n s t = true) :
    related observe update alphabet n t s = true := by
  induction n generalizing s t with
  | zero =>
      simp [related] at h
      simpa [related] using h.symm
  | succ n ih =>
      simp [related, List.all_eq_true] at h
      simp [related, List.all_eq_true]
      refine ⟨h.1.symm, ?_⟩
      intro σ hσ
      exact ih (update s σ) (update t σ) (h.2 σ hσ)

theorem related_trans (observe : Nat → Nat) (update : Nat → Nat → Nat)
    (alphabet : List Nat) (n s t u : Nat)
    (h1 : related observe update alphabet n s t = true)
    (h2 : related observe update alphabet n t u = true) :
    related observe update alphabet n s u = true := by
  induction n generalizing s t u with
  | zero =>
      simp [related] at h1 h2
      simpa [related] using h1.trans h2
  | succ n ih =>
      simp [related, List.all_eq_true] at h1 h2
      simp [related, List.all_eq_true]
      refine ⟨h1.1.trans h2.1, ?_⟩
      intro σ hσ
      exact ih (update s σ) (update t σ) (update u σ) (h1.2 σ hσ) (h2.2 σ hσ)

theorem related_mono (observe : Nat → Nat) (update : Nat → Nat → Nat)
    (alphabet : List Nat) (n s t : Nat)
    (h : related observe update alphabet (n + 1) s t = true) :
    related observe update alphabet n s t = true := by
  induction n generalizing s t with
  | zero =>
      simp [related, List.all_eq_true] at h
      simpa [related] using h.1
  | succ n ih =>
      unfold related at h
      simp only [Bool.and_eq_true, List.all_eq_true] at h
      unfold related
      simp only [Bool.and_eq_true, List.all_eq_true]
      refine ⟨h.1, ?_⟩
      intro σ hσ
      exact ih (update s σ) (update t σ) (h.2 σ hσ)

theorem list_all_congr {α : Type} (p q : α → Bool) (l : List α)
    (h : ∀ a, a ∈ l → p a = q a) : l.all p = l.all q := by
  induction l with
  | nil => rfl
  | cons head tail ih =>
      show (p head && tail.all p) = (q head && tail.all q)
      rw [h head (List.mem_cons_self), ih]
      intro item member
      exact h item (List.mem_cons_of_mem head member)

theorem related_stable (observe : Nat → Nat) (update : Nat → Nat → Nat)
    (alphabet : List Nat) (n : Nat)
    (hfix : ∀ s t, related observe update alphabet (n + 1) s t =
      related observe update alphabet n s t)
    (k s t : Nat) :
    related observe update alphabet (n + k) s t = related observe update alphabet n s t := by
  induction k generalizing s t with
  | zero => rfl
  | succ k ih =>
      rw [(Nat.add_assoc n k 1).symm]
      have step : related observe update alphabet (n + k + 1) s t =
          related observe update alphabet (n + 1) s t := by
        simp only [related]
        apply congrArg (fun bits => (observe s == observe t) && bits)
        exact list_all_congr _ _ alphabet fun σ _ => ih (update s σ) (update t σ)
      rw [step, hfix]

def sharpUpdate (size : Nat) (state symbol : Nat) : Nat :=
  if symbol = 0 then min (state + 1) (size - 1) else state

def sharpObserve (size state : Nat) : Nat :=
  if size = 0 then 0 else if state + 1 = size then 1 else 0

theorem sharp_m5_bound :
    let observe := sharpObserve 5
    let update := sharpUpdate 5
    let alphabet : List Nat := [0]
    (∀ s, s < 5 → related observe update alphabet 3 s s = true) ∧
      related observe update alphabet 0 0 1 = true ∧
      related observe update alphabet 3 0 1 = false ∧
      related observe update alphabet 3 0 4 = false := by
  decide

end Wd2
