import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Exact finite argmin with strict improvements, first
ties and zero-score early termination. Candidate costs are natural violation
counts. Rust Cartesian coverage, literal edge indexes, ordered admission and
owned buffer reuse are separate source/native obligations. -/
namespace TFQM.MinimumColors
variable {α : Type}

def Undirected (forbidden : α → α → Prop) (left right : α) : Prop :=
  forbidden left right ∨ forbidden right left

theorem undirected_symmetric (forbidden : α → α → Prop) (left right : α) :
    Undirected forbidden left right ↔ Undirected forbidden right left := by
  exact or_comm

def update (best : Option (α × Nat)) (candidate : α × Nat) : Option (α × Nat) :=
  match best with
  | none => some candidate
  | some previous => if candidate.2 < previous.2 then some candidate else some previous

theorem new_candidate (candidate : α × Nat) : update none candidate = some candidate := rfl

theorem strict_improvement (previous candidate : α × Nat) (h : candidate.2 < previous.2) :
    update (some previous) candidate = some candidate := by simp [update, h]

theorem tie_keeps_first (previous candidate : α × Nat) (h : candidate.2 = previous.2) :
    update (some previous) candidate = some previous := by simp [update, h]

def Good (seen : List (α × Nat)) : Option (α × Nat) → Prop
  | none => seen = []
  | some best => best ∈ seen ∧ ∀ candidate ∈ seen, best.2 ≤ candidate.2

theorem update_good (seen : List (α × Nat)) (best : Option (α × Nat))
    (candidate : α × Nat) (hb : Good seen best) :
    Good (seen ++ [candidate]) (update best candidate) := by
  cases best with
  | none =>
    have he : seen = [] := hb
    subst seen
    simp [Good, update]
  | some previous =>
    obtain ⟨hm, hmin⟩ := hb
    by_cases h : candidate.2 < previous.2
    · simp only [update, h, ↓reduceIte, Good]
      refine ⟨by simp, ?_⟩
      intro item hi
      simp only [List.mem_append, List.mem_singleton] at hi
      rcases hi with hi | rfl
      · exact le_trans (Nat.le_of_lt h) (hmin item hi)
      · exact le_rfl
    · simp only [update, h, ↓reduceIte, Good]
      refine ⟨by simp [hm], ?_⟩
      intro item hi
      simp only [List.mem_append, List.mem_singleton] at hi
      rcases hi with hi | rfl
      · exact hmin item hi
      · omega

theorem fold_good (seen rest : List (α × Nat)) (best : Option (α × Nat))
    (hb : Good seen best) : Good (seen ++ rest) (rest.foldl update best) := by
  induction rest generalizing seen best with
  | nil => simpa using hb
  | cons candidate rest ih =>
    have hs := ih (seen ++ [candidate]) (update best candidate) (update_good seen best candidate hb)
    simpa [List.foldl, List.append_assoc] using hs

def minimum (candidates : List (α × Nat)) : Option (α × Nat) := candidates.foldl update none

theorem minimum_good (candidates : List (α × Nat)) : Good candidates (minimum candidates) := by
  simpa [minimum] using fold_good [] candidates none (by rfl)

theorem minimum_none_iff (candidates : List (α × Nat)) : minimum candidates = none ↔ candidates = [] := by
  constructor
  · intro h
    have hg := minimum_good candidates
    simpa [h, Good] using hg
  · intro h
    subst candidates
    rfl

theorem minimum_optimal (candidates : List (α × Nat)) (best : α × Nat)
    (h : minimum candidates = some best) :
    best ∈ candidates ∧ ∀ candidate ∈ candidates, best.2 ≤ candidate.2 := by
  have hg := minimum_good candidates
  simpa [h, Good] using hg

theorem zero_stays (rest : List (α × Nat)) (best : α × Nat) (hz : best.2 = 0) :
    rest.foldl update (some best) = some best := by
  induction rest with
  | nil => rfl
  | cons candidate rest ih =>
    have hu : update (some best) candidate = some best := by simp [update, hz]
    simpa [List.foldl, hu] using ih

theorem zero_global (seen rest : List (α × Nat)) (best : α × Nat)
    (hg : Good seen (some best)) (hz : best.2 = 0) : Good (seen ++ rest) (some best) := by
  refine ⟨by simp [hg.1], ?_⟩
  intro candidate _
  simp [hz]

theorem positive_word_count (colors vertices : Nat) (hc : 0 < colors) : 0 < colors ^ vertices :=
  pow_pos hc vertices

theorem work_bound (count edges limit bound : Nat)
    (hc : count * edges ≤ limit) (hl : limit ≤ bound) : count * edges ≤ bound := le_trans hc hl

#print axioms undirected_symmetric
#print axioms new_candidate
#print axioms strict_improvement
#print axioms tie_keeps_first
#print axioms update_good
#print axioms fold_good
#print axioms minimum_good
#print axioms minimum_none_iff
#print axioms minimum_optimal
#print axioms zero_stays
#print axioms zero_global
#print axioms positive_word_count
#print axioms work_bound
end TFQM.MinimumColors
