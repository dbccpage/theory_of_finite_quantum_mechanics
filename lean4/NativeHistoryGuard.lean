import NativeHistoryCost

/-!
Exact future-legality quotient of Source-25's one fixed assertion cell.
The event alphabet is only add/remove on that cell. Carrier changes, fillings,
other cells, costs and endpoint reconstruction are outside this theorem.
The embedding into the actual native source is checked separately in Rust.
-/
namespace NativeHistoryGuard
open NativeHistoryCost

def legal (n : Nat) : List Event → Bool
  | [] => true
  | e :: es => match step n e with
    | none => false
    | some m => legal m es

theorem legal_eq_replay (n : Nat) (w : List Event) :
    legal n w = (replay n w).isSome := by
  induction w generalizing n with
  | nil => rfl
  | cons e es ih =>
    simp only [legal, replay]
    cases h : step n e with
    | none => rfl
    | some m => exact ih m

/-- Equal clipped multiplicities give exactly the same answers for every
word within the stated remaining depth, not just sampled words. -/
theorem legal_depth_congr (r m n : Nat) (h : min m r = min n r)
    (w : List Event) (hw : w.length ≤ r) : legal m w = legal n w := by
  induction w generalizing r m n with
  | nil => rfl
  | cons e es ih =>
    cases r with
    | zero => simp at hw
    | succ r =>
      have he : es.length ≤ r := by simpa using hw
      cases e with
      | add =>
        simp only [legal, step]
        exact ih r (m + 1) (n + 1) (by omega) he
      | remove =>
        cases m with
        | zero =>
          have hn : n = 0 := by omega
          subst n
          rfl
        | succ m =>
          cases n with
          | zero => omega
          | succ n =>
            simp only [legal, step]
            exact ih r m n (by omega) he

theorem legal_clip (r n : Nat) (w : List Event) (hw : w.length ≤ r) :
    legal (min n r) w = legal n w :=
  legal_depth_congr r (min n r) n (by omega) w hw

theorem legal_removals (n k : Nat) :
    legal n (List.replicate k Event.remove) = decide (k ≤ n) := by
  induction k generalizing n with
  | zero => simp [legal]
  | succ k ih =>
    cases n with
    | zero => simp [List.replicate_succ, legal, step]
    | succ n => simpa [List.replicate_succ, legal, step] using ih n

def DepthEquivalent (r m n : Nat) : Prop :=
  ∀ w : List Event, w.length ≤ r → legal m w = legal n w

theorem removals_separate {r m n : Nat} (hmn : m < n) (hmr : m < r) :
    ¬ DepthEquivalent r m n := by
  intro h
  have hs := h (List.replicate (m + 1) Event.remove) (by simp; omega)
  simp only [legal_removals] at hs
  have hn : m + 1 ≤ n := by omega
  simp [hn] at hs
  omega

/-- Complete characterization, hence minimality of the r+1 classes. -/
theorem depth_equivalent_iff (r m n : Nat) :
    DepthEquivalent r m n ↔ min m r = min n r := by
  constructor
  · intro h
    by_cases hmn : m ≤ n
    · by_cases he : min m r = min n r
      · exact he
      · exact False.elim (removals_separate (by omega : m < n) (by omega : m < r) h)
    · by_cases he : min m r = min n r
      · exact he
      · have hn : DepthEquivalent r n m := fun w hw => (h w hw).symm
        exact False.elim (removals_separate (by omega : n < m) (by omega : n < r) hn)
  · intro h w hw
    exact legal_depth_congr r m n h w hw

/-- Any sufficient report separates the canonical r+1 representatives.
The cardinal lower bound is this injection plus finite pigeonhole. -/
theorem sufficient_report_injective {Q : Type} (r : Nat) (q : Nat → Q)
    (hq : ∀ m n, q m = q n → DepthEquivalent r m n) :
    ∀ i j : Fin (r + 1), q i.val = q j.val → i = j := by
  intro i j hij
  have hm := (depth_equivalent_iff r i.val j.val).mp (hq i.val j.val hij)
  have hi := i.isLt
  have hj := j.isLt
  apply Fin.ext
  omega

/-- Preserving every finite continuation forces injectivity on Nat.
Consequently no finite-valued report can preserve unrestricted legality. -/
theorem all_depths_force_injective {Q : Type} (q : Nat → Q)
    (hq : ∀ m n, q m = q n → ∀ w, legal m w = legal n w) :
    ∀ m n, q m = q n → m = n := by
  intro m n h
  have hm := (depth_equivalent_iff (m + n + 1) m n).mp
    (fun w _ => hq m n h w)
  omega

/-- Exact clipped successors use a decreasing depth. Keeping r fixed would
fail: counts r and r+1 agree initially but their removals no longer agree. -/
theorem clipped_add_transition (r n : Nat) :
    min (min n (r + 1) + 1) r = min (n + 1) r := by omega

theorem clipped_remove_transition (r n : Nat) :
    min (min (n + 1) (r + 1) - 1) r = min n r := by omega

theorem fixed_depth_is_not_stable (r : Nat) :
    min (r + 1) (r + 1) = min (r + 2) (r + 1) ∧
    min r (r + 1) ≠ min (r + 1) (r + 1) := by
  constructor
  · omega
  · intro h; omega

/-- The adequate quotient exists for every depth; it is not an empty
contract or a hypothesis that already assumes all native states coincide. -/
theorem clipped_report_inhabitant (r : Nat) :
    ∀ m n, min m r = min n r → DepthEquivalent r m n := by
  intro m n h
  exact (depth_equivalent_iff r m n).mpr h

theorem sufficient_reserve (n : Nat) (w : List Event) (h : w.length ≤ n) :
    legal n w = true := by
  induction w generalizing n with
  | nil => rfl
  | cons e es ih =>
    cases n with
    | zero => simp at h
    | succ n =>
      have he : es.length ≤ n := by simpa using h
      cases e with
      | add => exact ih (n + 1 + 1) (by omega)
      | remove => exact ih n he

/-- The witnesses may depend on the test horizon. -/
theorem every_finite_depth_has_a_safe_state (r : Nat) :
    ∃ n, ∀ w : List Event, w.length ≤ r → legal n w = true := by
  exact ⟨r, fun w h => sufficient_reserve r w h⟩

/-- Swapping those quantifiers would add a state absent from Nat. -/
theorem no_unrestricted_safe_native_state :
    ¬ ∃ n, ∀ w : List Event, legal n w = true := by
  rintro ⟨n, h⟩
  have hh := h (List.replicate (n + 1) Event.remove)
  rw [legal_removals] at hh
  have hn : ¬n + 1 ≤ n := by omega
  simp [hn] at hh

theorem clipped_depth_restriction (n r : Nat) :
    min (min n (r + 1)) r = min n r := by omega

theorem saturated_profile_has_no_native_representative (n : Nat) :
    ∃ r, min n r ≠ r := by
  refine ⟨n + 1, ?_⟩
  intro h
  omega

#print axioms legal_eq_replay
#print axioms legal_depth_congr
#print axioms legal_clip
#print axioms legal_removals
#print axioms removals_separate
#print axioms depth_equivalent_iff
#print axioms sufficient_report_injective
#print axioms all_depths_force_injective
#print axioms clipped_add_transition
#print axioms clipped_remove_transition
#print axioms fixed_depth_is_not_stable
#print axioms clipped_report_inhabitant
#print axioms sufficient_reserve
#print axioms every_finite_depth_has_a_safe_state
#print axioms no_unrestricted_safe_native_state
#print axioms clipped_depth_restriction
#print axioms saturated_profile_has_no_native_representative

end NativeHistoryGuard
