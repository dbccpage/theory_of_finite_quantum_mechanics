/-!
# Faithful representation, coverage, and relative search completeness

The maps below are data, not a claim that arbitrary programs can be certified
by finite tests. Soundness and forward coverage are separate hypotheses.
The companion module constructs the constraint-system instance. Fuel counts
declared operations, not time; admission and institutional meaning remain input.
-/
namespace WitnessedDifference.FaithfulRepresentation

universe u v

structure System (Answer : Type u) where
  Witness : Type v
  accepts : Witness → Prop
  decode : Witness → Answer

def Sound {Answer : Type u} (good : Answer → Prop) (S : System Answer) : Prop :=
  ∀ w, S.accepts w → good (S.decode w)

structure Coverage {Answer : Type u} (good : Answer → Prop) (S : System Answer) where
  lift : Answer → S.Witness
  valid : ∀ x, good x → S.accepts (lift x)
  recovers : ∀ x, good x → S.decode (lift x) = x

structure Transport {Answer : Type u} (S T : System Answer) where
  back : T.Witness → S.Witness
  forth : S.Witness → T.Witness
  back_valid : ∀ w, T.accepts w → S.accepts (back w)
  forth_valid : ∀ w, S.accepts w → T.accepts (forth w)
  back_answer : ∀ w, T.accepts w → S.decode (back w) = T.decode w
  forth_answer : ∀ w, S.accepts w → T.decode (forth w) = S.decode w

def Transport.identity {Answer : Type u} (S : System Answer) : Transport S S where
  back := id
  forth := id
  back_valid := fun _ h => h
  forth_valid := fun _ h => h
  back_answer := fun _ _ => rfl
  forth_answer := fun _ _ => rfl

def Transport.comp {Answer : Type u} {S T U : System Answer}
    (a : Transport S T) (b : Transport T U) : Transport S U where
  back := a.back ∘ b.back
  forth := b.forth ∘ a.forth
  back_valid := fun w h => a.back_valid _ (b.back_valid w h)
  forth_valid := fun w h => b.forth_valid _ (a.forth_valid w h)
  back_answer := fun w h => (a.back_answer _ (b.back_valid w h)).trans (b.back_answer w h)
  forth_answer := fun w h => (b.forth_answer _ (a.forth_valid w h)).trans (a.forth_answer w h)

theorem transported_sound {Answer : Type u} {good : Answer → Prop} {S T : System Answer}
    (h : Sound good S) (t : Transport S T) : Sound good T := by
  intro w hw
  rw [← t.back_answer w hw]
  exact h _ (t.back_valid w hw)

def transported_coverage {Answer : Type u} {good : Answer → Prop} {S T : System Answer}
    (h : Coverage good S) (t : Transport S T) : Coverage good T where
  lift := t.forth ∘ h.lift
  valid := fun x hx => t.forth_valid _ (h.valid x hx)
  recovers := fun x hx => (t.forth_answer _ (h.valid x hx)).trans (h.recovers x hx)

inductive History {Answer : Type u} : System.{u,v} Answer → System.{u,v} Answer → Type (max u (v+1))
  | nil (S) : History S S
  | snoc {S T U : System.{u,v} Answer} : History S T → Transport T U → History S U

def History.transport {Answer : Type u} {S T : System.{u,v} Answer}
    (h : History S T) : Transport S T :=
  match h with
  | .nil _ => Transport.identity _
  | .snoc prior step => prior.transport.comp step

theorem every_history_sound {Answer : Type u} {good : Answer → Prop} {S T : System Answer}
    (initial : Sound good S) (h : History S T) : Sound good T :=
  transported_sound initial h.transport

theorem solution_iff_certificate {Answer : Type u} {good : Answer → Prop} {S T : System Answer}
    (sound : Sound good S) (covered : Coverage good S) (h : History S T) :
    (∃ x, good x) ↔ ∃ w, T.accepts w := by
  constructor
  · rintro ⟨x, hx⟩
    let c := transported_coverage covered h.transport
    exact ⟨c.lift x, c.valid x hx⟩
  · rintro ⟨w, hw⟩
    exact ⟨T.decode w, every_history_sound sound h w hw⟩

/-- A negative target result transports only with the forward coverage law. -/
theorem reflected_exhaustion {Answer : Type u} {good : Answer → Prop} {S T : System Answer}
    (covered : Coverage good S) (h : History S T) (empty : ∀ w, ¬T.accepts w) :
    ∀ x, ¬good x := by
  intro x hx
  let c := transported_coverage covered h.transport
  exact empty _ (c.valid x hx)

/-- Soundness alone can discard the source's sole solution. -/
theorem soundness_does_not_give_coverage :
    let S : System Bool := ⟨Bool, fun b => b = true, id⟩
    let T : System Bool := ⟨Bool, fun _ => False, id⟩
    Sound (fun b => b = true) T ∧ (∃ w, S.accepts w) ∧ ¬(∃ w, T.accepts w) := by
  exact ⟨fun _ h => False.elim h, ⟨true, rfl⟩, fun ⟨_, h⟩ => h⟩

def scan {W : Type u} (accept : W → Bool) : List W → Option W
  | [] => none
  | x :: xs => if accept x then some x else scan accept xs

theorem scan_sound {W : Type u} (accept : W → Bool) (xs : List W) {w : W}
    (h : scan accept xs = some w) : accept w = true := by
  induction xs with
  | nil => simp [scan] at h
  | cons x xs ih =>
    cases hx : accept x with
    | false => exact ih (by simpa [scan, hx] using h)
    | true =>
      have e : x = w := by simpa [scan, hx] using h
      simpa [← e] using hx

theorem scan_none_iff {W : Type u} (accept : W → Bool) (xs : List W) :
    scan accept xs = none ↔ ∀ w, w ∈ xs → accept w = false := by
  induction xs with
  | nil => simp [scan]
  | cons x xs ih =>
    cases hx : accept x <;> simp [scan, hx, ih]

theorem finite_exhaustion {W : Type u} (accept : W → Bool) (xs : List W)
    (coverage : ∀ w, w ∈ xs) (none : scan accept xs = none) :
    ∀ w, accept w = false := by
  intro w
  exact (scan_none_iff accept xs).mp none w (coverage w)

def Fair {W : Type u} (enumerate : Nat → W) : Prop := ∀ w, ∃ n, enumerate n = w

def enumerationPrefix {W : Type u} (enumerate : Nat → W) (n : Nat) : List W :=
  (List.range n).map enumerate

theorem enumeration_prefix_contains {W : Type u} (enumerate : Nat → W) (n : Nat) :
    enumerate n ∈ enumerationPrefix enumerate (n+1) := by
  simp only [enumerationPrefix, List.mem_map]
  exact ⟨n, by simp, rfl⟩

theorem fair_certificate_eventually_tested {W : Type u} (accept : W → Bool)
    (enumerate : Nat → W) (fair : Fair enumerate) {w : W} (valid : accept w = true) :
    ∃ n, accept (enumerate n) = true := by
  obtain ⟨n, hn⟩ := fair w
  exact ⟨n, hn ▸ valid⟩

/-- Prefix coverage is independent of acceptance; both hypotheses are explicit. -/
theorem fair_finite_prefix_discovery {W : Type u} (accept : W → Bool)
    (enumerate : Nat → W) (fair : Fair enumerate) (initialSegment : Nat → List W)
    (contains : ∀ n, enumerate n ∈ initialSegment (n+1)) {w : W} (valid : accept w = true) :
    ∃ n, scan accept (initialSegment n) ≠ none := by
  obtain ⟨n, hn⟩ := fair_certificate_eventually_tested accept enumerate fair valid
  refine ⟨n+1, ?_⟩
  intro h
  have bad := (scan_none_iff accept (initialSegment (n+1))).mp h _ (contains n)
  simp [hn] at bad

theorem faithful_fair_search_complete {Answer : Type u} {good : Answer → Prop}
    {S T : System Answer} (sound : Sound good S) (covered : Coverage good S)
    (history : History S T) (accept : T.Witness → Bool)
    (checker : ∀ w, accept w = true ↔ T.accepts w)
    (enumerate : Nat → T.Witness) (fair : Fair enumerate) (existsSolution : ∃ x, good x) :
    ∃ n, scan accept (enumerationPrefix enumerate n) ≠ none := by
  obtain ⟨w, hw⟩ := (solution_iff_certificate sound covered history).mp existsSolution
  exact fair_finite_prefix_discovery accept enumerate fair (enumerationPrefix enumerate)
    (enumeration_prefix_contains enumerate) ((checker w).mpr hw)

/-- One optional proposal per canonical item cannot remove any canonical item. -/
def interleave {W : Type u} (proposals canonical : List W) : List W :=
  match proposals, canonical with
  | _, [] => []
  | [], xs => xs
  | p :: ps, c :: cs => p :: c :: interleave ps cs

theorem interleave_retains {W : Type u} (proposals canonical : List W) {w : W}
    (h : w ∈ canonical) : w ∈ interleave proposals canonical := by
  induction canonical generalizing proposals with
  | nil => simp at h
  | cons c cs ih =>
    cases proposals with
    | nil => simpa [interleave] using h
    | cons p ps =>
      simp only [List.mem_cons] at h
      rcases h with h | h
      · simp [interleave, h]
      · exact List.mem_cons_of_mem p (List.mem_cons_of_mem c (ih ps h))

theorem interleave_length_bound {W : Type u} (proposals canonical : List W) :
    (interleave proposals canonical).length ≤ 2 * canonical.length := by
  induction canonical generalizing proposals with
  | nil => simp [interleave]
  | cons c cs ih =>
    cases proposals with
    | nil => simp [interleave]; omega
    | cons p ps =>
      have h := ih ps
      simp only [interleave, List.length_cons]
      omega

structure Anchor where
  problem : String
  assumptions : List String
  authorization : List String
  witnessRoot : String
  deriving DecidableEq

structure Frame where
  anchor : Anchor
  spent : Nat
  ceiling : Nat

def GuardedStep (a b : Frame) : Prop :=
  b.anchor = a.anchor ∧ b.ceiling = a.ceiling ∧ b.spent = a.spent + 1 ∧ b.spent ≤ b.ceiling

inductive Reentry : Frame → Frame → Nat → Prop
  | nil (a) : Reentry a a 0
  | snoc : Reentry a b n → GuardedStep b c → Reentry a c (n+1)

theorem reentry_invariants {a b : Frame} {n : Nat} (h : Reentry a b n) :
    b.anchor = a.anchor ∧ b.ceiling = a.ceiling ∧ b.spent = a.spent + n := by
  induction h with
  | nil => simp
  | snoc prior step ih =>
    rcases ih with ⟨ha, hc, hs⟩
    rcases step with ⟨sa, sc, ss, _⟩
    exact ⟨sa.trans ha, sc.trans hc, by omega⟩

theorem reentry_budget_bound {a b : Frame} {n : Nat} (h : Reentry a b n)
    (initial : a.spent ≤ a.ceiling) : a.spent + n ≤ a.ceiling := by
  have inv := reentry_invariants h
  have final : b.spent ≤ b.ceiling := by
    cases h with
    | nil => exact initial
    | snoc _ step => exact step.2.2.2
  omega

theorem changed_anchor_refused {a b : Frame} (changed : b.anchor ≠ a.anchor) :
    ¬GuardedStep a b := fun h => changed h.1

theorem reentry_cannot_reset {a b : Frame} {n : Nat} (h : Reentry a b n)
    (nonempty : 0 < n) : a.spent < b.spent := by
  have inv := reentry_invariants h
  omega

/-- The whole integer defect space supplies a formal repair, even with no solution. -/
theorem whole_space_repair_does_not_solve :
    (∃ b : Int, 1 - b = 0) ∧ ¬(∃ _ : Unit, False) := by
  exact ⟨⟨1, by decide⟩, fun ⟨_, h⟩ => h⟩

theorem realized_repair_is_sound {Candidate Answer : Type u}
    (good : Answer → Prop) (zero : Candidate → Prop) (decode : Candidate → Answer)
    (sound : ∀ c, zero c → good (decode c)) {c : Candidate}
    (realized : zero c) : good (decode c) := sound c realized

end WitnessedDifference.FaithfulRepresentation

#print axioms WitnessedDifference.FaithfulRepresentation.transported_sound
#print axioms WitnessedDifference.FaithfulRepresentation.every_history_sound
#print axioms WitnessedDifference.FaithfulRepresentation.solution_iff_certificate
#print axioms WitnessedDifference.FaithfulRepresentation.reflected_exhaustion
#print axioms WitnessedDifference.FaithfulRepresentation.soundness_does_not_give_coverage
#print axioms WitnessedDifference.FaithfulRepresentation.scan_sound
#print axioms WitnessedDifference.FaithfulRepresentation.scan_none_iff
#print axioms WitnessedDifference.FaithfulRepresentation.finite_exhaustion
#print axioms WitnessedDifference.FaithfulRepresentation.fair_certificate_eventually_tested
#print axioms WitnessedDifference.FaithfulRepresentation.enumeration_prefix_contains
#print axioms WitnessedDifference.FaithfulRepresentation.fair_finite_prefix_discovery
#print axioms WitnessedDifference.FaithfulRepresentation.faithful_fair_search_complete
#print axioms WitnessedDifference.FaithfulRepresentation.interleave_retains
#print axioms WitnessedDifference.FaithfulRepresentation.interleave_length_bound
#print axioms WitnessedDifference.FaithfulRepresentation.reentry_invariants
#print axioms WitnessedDifference.FaithfulRepresentation.reentry_budget_bound
#print axioms WitnessedDifference.FaithfulRepresentation.changed_anchor_refused
#print axioms WitnessedDifference.FaithfulRepresentation.reentry_cannot_reset
#print axioms WitnessedDifference.FaithfulRepresentation.whole_space_repair_does_not_solve
#print axioms WitnessedDifference.FaithfulRepresentation.realized_repair_is_sound
