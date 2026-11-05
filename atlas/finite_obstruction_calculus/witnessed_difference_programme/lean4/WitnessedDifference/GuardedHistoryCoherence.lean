/- Local steps of the guarded-history coherence theorem (Appendix P.20). Core Lean.
   The simple-connectivity argument itself is a written proof; these declarations
   check its two local inputs: moving a helper event earlier preserves a guarded
   run, and a cochain closed on the declared faces is unchanged by local moves. -/
import Init

namespace WitnessedDifference.GuardedHistoryCoherence

/-- Partial execution of a word of events; `none` records a guard refusal. -/
def run {S E : Type} (step : S → E → Option S) : S → List E → Option S
  | s, [] => some s
  | s, e :: es =>
    match step s e with
    | none => none
    | some t => run step t es

theorem run_cons_some {S E : Type} (step : S → E → Option S) {s t : S} {e : E}
    (h : step s e = some t) (es : List E) : run step s (e :: es) = run step t es := by
  simp [run, h]

theorem run_cons_none {S E : Type} (step : S → E → Option S) {s : S} {e : E}
    (h : step s e = none) (es : List E) : run step s (e :: es) = none := by
  simp [run, h]

/-- If `a` then `x` reaches every state that `x` then `a` reaches, the adjacent swap
    that moves `a` earlier preserves every complete run and its final state, under
    any prefix and suffix. -/
theorem helper_swap_preserves_run {S E : Type} (step : S → E → Option S) (x a : E)
    (helps : ∀ s u, run step s [x, a] = some u → run step s [a, x] = some u)
    (pre post : List E) (s r : S)
    (legal : run step s (pre ++ x :: a :: post) = some r) :
    run step s (pre ++ a :: x :: post) = some r := by
  induction pre generalizing s with
  | nil =>
    simp only [List.nil_append] at legal ⊢
    cases hx : step s x with
    | none => rw [run_cons_none step hx] at legal; cases legal
    | some t =>
      rw [run_cons_some step hx] at legal
      cases ha : step t a with
      | none => rw [run_cons_none step ha] at legal; cases legal
      | some u =>
        rw [run_cons_some step ha] at legal
        have two : run step s [x, a] = some u := by
          rw [run_cons_some step hx, run_cons_some step ha]; rfl
        have swapped := helps s u two
        cases ha' : step s a with
        | none => rw [run_cons_none step ha'] at swapped; cases swapped
        | some v =>
          rw [run_cons_some step ha'] at swapped
          cases hx' : step v x with
          | none => rw [run_cons_none step hx'] at swapped; cases swapped
          | some w =>
            rw [run_cons_some step hx'] at swapped
            have wu : w = u := by
              simp [run] at swapped; exact swapped
            rw [run_cons_some step ha', run_cons_some step hx', wu]
            exact legal
  | cons e es ih =>
    simp only [List.cons_append] at legal ⊢
    cases he : step s e with
    | none => rw [run_cons_none step he] at legal; cases legal
    | some t =>
      rw [run_cons_some step he] at legal
      rw [run_cons_some step he]
      exact ih t legal

/-- Two events whose composites agree in both orders can be exchanged anywhere. -/
theorem commuting_swap_preserves_run {S E : Type} (step : S → E → Option S) (x y : E)
    (commute : ∀ s, run step s [x, y] = run step s [y, x])
    (pre post : List E) (s r : S)
    (legal : run step s (pre ++ x :: y :: post) = some r) :
    run step s (pre ++ y :: x :: post) = some r :=
  helper_swap_preserves_run step x y
    (fun s u h => by rw [← commute s]; exact h) pre post s r legal

/-- One count key: `true` adds an assertion, `false` removes one and needs a positive
    count. This is the native `AddAssertion`/`Remove` guard on a single key. -/
def countStep (c : Nat) : Bool → Option Nat
  | true => some (c + 1)
  | false => if 0 < c then some (c - 1) else none

/-- A remove immediately followed by an add on the same key may be reordered with
    the add first; the run stays legal and ends in the same count. -/
theorem add_before_remove_helps (c u : Nat)
    (h : run countStep c [false, true] = some u) :
    run countStep c [true, false] = some u := by
  by_cases pos : 0 < c
  · have : u = c := by
      simp [run, countStep, pos] at h; omega
    subst this
    simp [run, countStep]
  · simp [run, countStep, pos] at h

/-- The count-kernel local lemma: swapping an adjacent remove-then-add on one key to
    add-then-remove preserves every complete legal run and its final count. -/
theorem count_kernel_swap (pre post : List Bool) (c r : Nat)
    (legal : run countStep c (pre ++ false :: true :: post) = some r) :
    run countStep c (pre ++ true :: false :: post) = some r :=
  helper_swap_preserves_run countStep false true add_before_remove_helps pre post c r legal

/-- The converse fails: from count zero, add-then-remove is legal and
    remove-then-add is refused. Moving a remove earlier is not a legal swap in
    general. -/
theorem remove_first_refused_at_zero :
    run countStep 0 [true, false] = some 0 ∧ run countStep 0 [false, true] = none := by
  constructor <;> simp [run, countStep]

/-- Integer value of a 1-cochain along a word of oriented edges. -/
def total {E : Type} (φ : E → Int) : List E → Int
  | [] => 0
  | e :: es => φ e + total φ es

theorem total_append {E : Type} (φ : E → Int) (xs ys : List E) :
    total φ (xs ++ ys) = total φ xs + total φ ys := by
  induction xs with
  | nil => simp [total]
  | cons e es ih => simp [total, ih]; omega

/-- A backtrack `e` then its reverse contributes nothing when the cochain is
    antisymmetric. -/
theorem backtrack_invariant {E : Type} (φ : E → Int) (rev : E → E)
    (antisymmetric : ∀ e, φ (rev e) = -φ e) (pre post : List E) (e : E) :
    total φ (pre ++ e :: rev e :: post) = total φ (pre ++ post) := by
  rw [total_append, total_append]
  simp only [total, antisymmetric]
  omega

/-- Replacing one side of a face boundary by the other leaves the value unchanged
    when the cochain takes the same value on both sides (closedness on that face). -/
theorem face_move_invariant {E : Type} (φ : E → Int) (pre side side' post : List E)
    (closed : total φ side = total φ side') :
    total φ (pre ++ side ++ post) = total φ (pre ++ side' ++ post) := by
  rw [total_append, total_append, total_append, total_append, closed]

/-- The local moves on words: insert or delete a backtrack, or replace one side of
    a declared face boundary by the other. -/
inductive Move {E : Type} (rev : E → E) (faces : List (List E × List E)) :
    List E → List E → Prop
  | insert (pre post : List E) (e : E) :
      Move rev faces (pre ++ post) (pre ++ e :: rev e :: post)
  | delete (pre post : List E) (e : E) :
      Move rev faces (pre ++ e :: rev e :: post) (pre ++ post)
  | face (pre post side side' : List E) (declared : (side, side') ∈ faces) :
      Move rev faces (pre ++ side ++ post) (pre ++ side' ++ post)

/-- Finite sequences of local moves. -/
inductive Moves {E : Type} (rev : E → E) (faces : List (List E × List E)) :
    List E → List E → Prop
  | refl (w : List E) : Moves rev faces w w
  | tail {w v u : List E} : Moves rev faces w v → Move rev faces v u → Moves rev faces w u

/-- A cochain that is antisymmetric and closed on every declared face has the same
    value on any two words related by local moves. So unequal values separate two
    words: no sequence of backtracks and face moves joins them. -/
theorem moves_preserve_total {E : Type} (φ : E → Int) (rev : E → E)
    (faces : List (List E × List E))
    (antisymmetric : ∀ e, φ (rev e) = -φ e)
    (closed : ∀ p ∈ faces, total φ p.1 = total φ p.2)
    {w w' : List E} (path : Moves rev faces w w') : total φ w = total φ w' := by
  induction path with
  | refl => rfl
  | tail _ move ih =>
    rw [ih]
    cases move with
    | insert pre post e => exact (backtrack_invariant φ rev antisymmetric pre post e).symm
    | delete pre post e => exact backtrack_invariant φ rev antisymmetric pre post e
    | face pre post side side' declared =>
      exact face_move_invariant φ pre side side' post (closed (side, side') declared)

#print axioms run_cons_some
#print axioms helper_swap_preserves_run
#print axioms commuting_swap_preserves_run
#print axioms add_before_remove_helps
#print axioms count_kernel_swap
#print axioms remove_first_refused_at_zero
#print axioms total_append
#print axioms backtrack_invariant
#print axioms face_move_invariant
#print axioms moves_preserve_total
end WitnessedDifference.GuardedHistoryCoherence
