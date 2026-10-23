import Derivation.Basic
import Mathlib.Data.List.Range

/-! AuthorityEffect: None. A declared extension, not a reconstruction of Alpha.
The admitted policy is a controller field; SEEK computes and records a demand.
The lexicographic tie rule is part of this extension, not inferred from glyphs. -/
namespace CampaignGenesisDemandPolicy

def options (n : Nat) : List (Option Nat) := none :: (List.range n).map some

def tuples (n : Nat) : Nat → List (List (Option Nat))
  | 0 => [[]]
  | k + 1 => (options n).flatMap fun s => (tuples n k).map (s :: ·)

theorem mem_options (n : Nat) (s : Option Nat) :
    s ∈ options n ↔ Derivation.slotOk n s := by
  cases s <;> simp [options, Derivation.slotOk]

theorem mem_tuples (n k : Nat) (xs : List (Option Nat)) :
    xs ∈ tuples n k ↔ xs.length = k ∧ ∀ s ∈ xs, Derivation.slotOk n s := by
  induction k generalizing xs with
  | zero => cases xs <;> simp [tuples]
  | succ k ih =>
    cases xs with
    | nil => simp [tuples]
    | cons a xs => simp [tuples, List.mem_flatMap, mem_options, ih, and_assoc, and_left_comm, and_comm]

def contexts (r : Derivation.Regime) : List Derivation.Ctx :=
  (List.range r.forms.length).flatMap fun f =>
    ((tuples r.data (r.forms.getD f 0)).filter (fun xs => none ∈ xs)).map (⟨f, ·⟩)

theorem mem_contexts (r : Derivation.Regime) (c : Derivation.Ctx) :
    c ∈ contexts r ↔ Derivation.wfCtx r c := by
  rcases c with ⟨f, xs⟩
  simp [contexts, Derivation.wfCtx, List.mem_flatMap, mem_tuples,
    and_assoc, and_left_comm, and_comm]

def collapseTest (r : Derivation.Regime) (i j : Nat) : Bool :=
  (contexts r).all fun c => decide
    (Derivation.derivable r (Derivation.plug c i) ↔ Derivation.derivable r (Derivation.plug c j))

theorem collapseTest_correct (r : Derivation.Regime) (i j : Nat) :
    collapseTest r i j = true ↔ Derivation.collapsed r i j := by
  simp [collapseTest, List.all_eq_true, mem_contexts, Derivation.collapsed]

def candidates (r : Derivation.Regime) : List (Nat × Nat) :=
  (List.range r.data).flatMap fun i =>
    ((List.range r.data).filter (fun j => i < j)).map (i, ·)

theorem mem_candidates (r : Derivation.Regime) (q : Nat × Nat) :
    q ∈ candidates r ↔ q.1 < q.2 ∧ q.2 < r.data := by
  rcases q with ⟨i,j⟩
  simp [candidates, List.mem_flatMap, and_assoc, and_left_comm, and_comm]
  omega

def agenda (r : Derivation.Regime) : List (Nat × Nat) :=
  (candidates r).filter fun q => collapseTest r q.1 q.2 && decide (q ∉ r.reqs)

theorem mem_agenda (r : Derivation.Regime) (q : Nat × Nat) :
    q ∈ agenda r ↔ q.1 < q.2 ∧ q.2 < r.data ∧
      Derivation.collapsed r q.1 q.2 ∧ q ∉ r.reqs := by
  simp [agenda, mem_candidates, collapseTest_correct, and_assoc]

inductive Policy where | halt | separateAll deriving DecidableEq, Repr

structure Controller where
  regime : Derivation.Regime
  policy : Policy
deriving Repr, DecidableEq

def next (s : Controller) : Option (Nat × Nat) :=
  match s.policy with
  | .halt => none
  | .separateAll => (agenda s.regime).head?

theorem next_sound {s : Controller} {q : Nat × Nat} (h : next s = some q) :
    q.1 < q.2 ∧ q.2 < s.regime.data ∧
      Derivation.collapsed s.regime q.1 q.2 ∧ q ∉ s.regime.reqs := by
  cases hp : s.policy with
  | halt => simp [next, hp] at h
  | separateAll =>
    simp only [next, hp] at h
    exact (mem_agenda _ _).mp (List.mem_of_head? h)

theorem next_none_iff (r : Derivation.Regime) :
    next ⟨r, .separateAll⟩ = none ↔
      ∀ i j, i < j → j < r.data → Derivation.collapsed r i j → (i,j) ∈ r.reqs := by
  simp only [next, List.head?_eq_none_iff]
  rw [List.eq_nil_iff_forall_not_mem]
  constructor
  · intro h i j hij hj hc
    by_contra hn
    exact h (i,j) ((mem_agenda _ _).mpr ⟨hij,hj,hc,hn⟩)
  · intro h q hq
    obtain ⟨hij,hj,hc,hn⟩ := (mem_agenda _ _).mp hq
    exact hn (h q.1 q.2 hij hj hc)

/-- The object-language extension instruction. Its only primitive action is
the already declared source impose event. Nothing chooses an observation. -/
def seek (s : Controller) : Controller :=
  match next s with
  | none => s
  | some q => {s with regime := {s.regime with reqs := s.regime.reqs ++ [q]}}

theorem seek_is_recorded_source_step {s : Controller} {q : Nat × Nat}
    (h : next s = some q) :
    Derivation.stepE s.regime (.impose q.1 q.2) = some (seek s).regime := by
  obtain ⟨hij,hj,_,hn⟩ := next_sound h
  simp [Derivation.stepE, Derivation.insertNew, hij, hj, hn, seek, h]

theorem seek_grows_one {s : Controller} {q : Nat × Nat} (h : next s = some q) :
    (seek s).regime.reqs.length = s.regime.reqs.length + 1 := by
  simp [seek,h]

theorem seek_preserves_observations (s : Controller) :
    (seek s).regime.data = s.regime.data ∧
    (seek s).regime.forms = s.regime.forms ∧
    (seek s).regime.insts = s.regime.insts ∧
    (seek s).regime.rules = s.regime.rules := by
  unfold seek
  cases next s <;> simp

theorem no_immediate_repeat {s : Controller} {q : Nat × Nat} (h : next s = some q) :
    next (seek s) ≠ some q := by
  intro h'
  have hn := (next_sound h').2.2.2
  apply hn
  simp [seek,h]

theorem policy_is_not_forced :
    next ⟨⟨2,[],[],[],[]⟩, .halt⟩ = none ∧
    next ⟨⟨2,[],[],[],[]⟩, .separateAll⟩ = some (0,1) := by decide

theorem fixed_data_saturates :
    next (seek ⟨⟨2,[],[],[],[]⟩, .separateAll⟩) = none := by decide

inductive Instruction where
  | seek
  | source (event : Derivation.Event)
  | setPolicy (policy : Policy)
deriving Repr, DecidableEq

/-- Policy and SEEK are syntax in the declared extended language. Its source
instruction retains the original partiality rather than totalizing refusal. -/
def execute (s : Controller) : Instruction → Option Controller
  | .seek => some (seek s)
  | .source e => (Derivation.stepE s.regime e).map (fun r => {s with regime := r})
  | .setPolicy p => some {s with policy := p}

def program : List Instruction → Controller → Option Controller
  | [],s => some s
  | e::h,s => (execute s e).bind (program h)

theorem seek_preserves_policy (s : Controller) : (seek s).policy = s.policy := by
  unfold seek; cases next s <;> rfl

theorem instruction_records_demand {s : Controller} {q : Nat × Nat}
    (h : next s = some q) :
    execute s .seek = execute s (.source (.impose q.1 q.2)) := by
  simp only [execute,seek_is_recorded_source_step h,Option.map_some]
  congr 1
  simp [seek,h]

theorem no_host_target_in_program :
    program [.setPolicy .separateAll,.seek] ⟨⟨2,[],[],[],[]⟩,.halt⟩ =
      some ⟨⟨2,[],[],[],[(0,1)]⟩,.separateAll⟩ := by decide

end CampaignGenesisDemandPolicy

#print axioms CampaignGenesisDemandPolicy.mem_options
#print axioms CampaignGenesisDemandPolicy.mem_tuples
#print axioms CampaignGenesisDemandPolicy.mem_contexts
#print axioms CampaignGenesisDemandPolicy.collapseTest_correct
#print axioms CampaignGenesisDemandPolicy.mem_candidates
#print axioms CampaignGenesisDemandPolicy.mem_agenda
#print axioms CampaignGenesisDemandPolicy.next_sound
#print axioms CampaignGenesisDemandPolicy.next_none_iff
#print axioms CampaignGenesisDemandPolicy.seek_is_recorded_source_step
#print axioms CampaignGenesisDemandPolicy.seek_grows_one
#print axioms CampaignGenesisDemandPolicy.seek_preserves_observations
#print axioms CampaignGenesisDemandPolicy.no_immediate_repeat
#print axioms CampaignGenesisDemandPolicy.policy_is_not_forced
#print axioms CampaignGenesisDemandPolicy.fixed_data_saturates
#print axioms CampaignGenesisDemandPolicy.seek_preserves_policy
#print axioms CampaignGenesisDemandPolicy.instruction_records_demand
#print axioms CampaignGenesisDemandPolicy.no_host_target_in_program
