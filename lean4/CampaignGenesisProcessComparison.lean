import Derivation.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fin.Basic

/-! AuthorityEffect: None. Explicit comparison-class extension.
A process has a root, one total challenge action and a readout. Arbitrary
finite readout types and finite carriers are permitted. Hidden clocks are
permitted: they do not change any observed challenge answer. Morphisms must
preserve the root, action and readout. These are declared choices. -/
namespace CampaignGenesisProcessComparison

structure Process (S O : Type) where
  root : S
  step : S → S
  read : S → O

def run {S O : Type} (p : Process S O) : Nat → S
  | 0 => p.root
  | k + 1 => p.step (run p k)

def advance {S O : Type} (p : Process S O) : Nat → S → S
  | 0, x => x
  | k + 1, x => p.step (advance p k x)

theorem run_add {S O : Type} (p : Process S O) (n k : Nat) :
    run p (n+k) = advance p k (run p n) := by
  induction k with
  | zero => rfl
  | succ k ih => simpa [run,advance] using congrArg p.step ih

structure Hom {S T O : Type} (p : Process S O) (q : Process T O) where
  map : S → T
  root : map p.root = q.root
  step : ∀ x, map (p.step x) = q.step (map x)
  read : ∀ x, q.read (map x) = p.read x

theorem hom_run {S T O : Type} {p : Process S O} {q : Process T O}
    (f : Hom p q) (n : Nat) : f.map (run p n) = run q n := by
  induction n with
  | zero => exact f.root
  | succ n ih => simpa [run, f.step, ih]

def clockStep (n : Nat) (x : Fin (n+1)) : Fin (n+1) :=
  ⟨(x.val+1) % (n+1), Nat.mod_lt _ (by omega)⟩

def clockLift {S O : Type} (p : Process S O) (n : Nat) : Process (S × Fin (n+1)) O where
  root := (p.root,0)
  step x := (p.step x.1, clockStep n x.2)
  read x := p.read x.1

def projection {S O : Type} (p : Process S O) (n : Nat) : Hom (clockLift p n) p where
  map := Prod.fst
  root := rfl
  step _ := rfl
  read _ := rfl

theorem every_challenge_answer_agrees {S O : Type} (p : Process S O) (n k : Nat) :
    (clockLift p n).read (run (clockLift p n) k) = p.read (run p k) := by
  have h := hom_run (projection p n) k
  exact congrArg p.read h

/-- No finite process is initial in a class containing its unobserved clock
lift of period one greater than its carrier size. No observational premise
is missing: the previous theorem proves agreement at every finite time. -/
theorem no_map_to_clock_lift {S O : Type} [Fintype S] (p : Process S O) :
    ¬ Nonempty (Hom p (clockLift p (Fintype.card S))) := by
  rintro ⟨f⟩
  let n := Fintype.card S
  have hval : ∀ k (hk : k < n+1), (f.map (run p k)).2 = ⟨k,hk⟩ := by
    intro k
    induction k with
    | zero => intro hk; simpa [run,clockLift] using congrArg Prod.snd f.root
    | succ k ih =>
      intro hk
      have hi := ih (by omega)
      rw [run, f.step]
      change clockStep n (f.map (run p k)).2 = _
      rw [hi]
      apply Fin.ext
      exact Nat.mod_eq_of_lt hk
  have hs : Function.Surjective (fun x => (f.map x).2) := by
    intro y
    exact ⟨run p y.val, hval y.val y.isLt⟩
  have hcard := Fintype.card_le_of_surjective _ hs
  simp only [Fintype.card_fin] at hcard
  omega

def Reachable {S O : Type} (p : Process S O) : Prop := ∀ x, ∃ n, run p n = x

def Reduced {S O : Type} (p : Process S O) : Prop :=
  ∀ x y, (∀ k, p.read (advance p k x) = p.read (advance p k y)) → x = y

def SameChallenges {S T O : Type} (p : Process S O) (q : Process T O) : Prop :=
  ∀ n, p.read (run p n) = q.read (run q n)

/-- A general minimum-size criterion, with reachable and behaviorally
reduced hypotheses explicit. It is not an engine certification. -/
theorem reduced_reachable_is_minimal {S T O : Type} [Fintype S] [Fintype T]
    (p : Process S O) (q : Process T O) (hr : Reachable p) (hd : Reduced p)
    (hc : SameChallenges p q) : Fintype.card S ≤ Fintype.card T := by
  classical
  choose time ht using hr
  let f : S → T := fun x => run q (time x)
  apply Fintype.card_le_of_injective f
  intro x y hxy
  apply hd x y
  intro k
  calc
    p.read (advance p k x) = p.read (run p (time x+k)) := by rw [run_add,ht]
    _ = q.read (run q (time x+k)) := hc _
    _ = q.read (advance q k (f x)) := by rw [run_add]
    _ = q.read (advance q k (f y)) := by rw [hxy]
    _ = q.read (run q (time y+k)) := by rw [run_add]
    _ = p.read (run p (time y+k)) := (hc _).symm
    _ = p.read (advance p k y) := by rw [run_add,ht]

def oneState : Process Unit Unit := ⟨(), id, fun _ => ()⟩
def hiddenState : Process Bool Unit := ⟨false, Bool.not, fun _ => ()⟩

theorem nonminimal_adequate_process :
    SameChallenges hiddenState oneState ∧ Fintype.card Unit < Fintype.card Bool := by
  exact ⟨fun _ => rfl, by decide⟩

theorem oneState_is_reduced_reachable : Reachable oneState ∧ Reduced oneState := by
  constructor
  · intro x; exact ⟨0, Subsingleton.elim _ _⟩
  · intro x y _; exact Subsingleton.elim _ _

/-! Arbitrary action alphabets. A distinguished action suffices for the
clock obstruction, while agreement and the size criterion quantify over
every finite action word. -/
structure LabelledProcess (A S O : Type) where
  root : S
  step : A → S → S
  read : S → O

def labelledAdvance {A S O : Type} (p : LabelledProcess A S O) : List A → S → S
  | [], x => x
  | a :: h, x => labelledAdvance p h (p.step a x)

def labelledRun {A S O : Type} (p : LabelledProcess A S O) (h : List A) : S :=
  labelledAdvance p h p.root

theorem labelled_append {A S O : Type} (p : LabelledProcess A S O)
    (h k : List A) (x : S) :
    labelledAdvance p (h++k) x = labelledAdvance p k (labelledAdvance p h x) := by
  induction h generalizing x with
  | nil => rfl
  | cons a h ih => exact ih (p.step a x)

structure LabelledHom {A S T O : Type} (p : LabelledProcess A S O)
    (q : LabelledProcess A T O) where
  map : S → T
  root : map p.root = q.root
  step : ∀ a x, map (p.step a x) = q.step a (map x)
  read : ∀ x, q.read (map x) = p.read x

def labelledClockLift {A S O : Type} (p : LabelledProcess A S O) (n : Nat) :
    LabelledProcess A (S × Fin (n+1)) O where
  root := (p.root,0)
  step a x := (p.step a x.1,clockStep n x.2)
  read x := p.read x.1

theorem all_words_agree {A S O : Type} (p : LabelledProcess A S O)
    (n : Nat) (h : List A) :
    (labelledClockLift p n).read (labelledRun (labelledClockLift p n) h) =
      p.read (labelledRun p h) := by
  have hp : ∀ (x : S) (k : Fin (n+1)),
      (labelledAdvance (labelledClockLift p n) h (x,k)).1 = labelledAdvance p h x := by
    induction h with
    | nil => intro x k; rfl
    | cons a h ih => intro x k; exact ih (p.step a x) (clockStep n k)
  exact congrArg p.read (hp p.root 0)

theorem no_initial_in_clock_closed_class {A S O : Type} [Fintype S]
    (p : LabelledProcess A S O) (a : A) :
    ¬ Nonempty (LabelledHom p (labelledClockLift p (Fintype.card S))) := by
  rintro ⟨f⟩
  let unary : Process S O := ⟨p.root,p.step a,p.read⟩
  apply no_map_to_clock_lift unary
  exact ⟨{map := f.map,root := f.root,step := f.step a,read := f.read}⟩

theorem all_words_minimum_size {A S T O : Type} [Fintype S] [Fintype T]
    (p : LabelledProcess A S O) (q : LabelledProcess A T O)
    (hr : ∀ x, ∃ h, labelledRun p h = x)
    (hd : ∀ x y, (∀ h, p.read (labelledAdvance p h x) =
      p.read (labelledAdvance p h y)) → x = y)
    (hc : ∀ h, p.read (labelledRun p h) = q.read (labelledRun q h)) :
    Fintype.card S ≤ Fintype.card T := by
  classical
  choose word hw using hr
  let f : S → T := fun x => labelledRun q (word x)
  apply Fintype.card_le_of_injective f
  intro x y hxy
  apply hd x y
  intro h
  have hx : labelledAdvance p h x = labelledRun p (word x++h) := by
    simpa only [labelledRun,labelled_append] using (congrArg (labelledAdvance p h) (hw x)).symm
  have hy : labelledAdvance p h y = labelledRun p (word y++h) := by
    simpa only [labelledRun,labelled_append] using (congrArg (labelledAdvance p h) (hw y)).symm
  calc
    p.read (labelledAdvance p h x) = q.read (labelledRun q (word x++h)) := by rw [hx,hc]
    _ = q.read (labelledAdvance q h (f x)) := by rw [labelledRun,labelled_append]; rfl
    _ = q.read (labelledAdvance q h (f y)) := by rw [hxy]
    _ = q.read (labelledRun q (word y++h)) := by rw [labelledRun,labelled_append]; rfl
    _ = p.read (labelledAdvance p h y) := by rw [hy,hc]

/-- A self-loop blocks the invisible two-clock lift even for an infinite
state type. This is independent of the finite-cardinality obstruction. -/
theorem no_clock_hom_of_self_loop {A S O : Type} (p : LabelledProcess A S O)
    (a : A) (x : S) (hx : p.step a x = x) :
    ¬ Nonempty (LabelledHom p (labelledClockLift p 1)) := by
  rintro ⟨f⟩
  have he := congrArg (fun y => y.2.val) (f.step a x)
  rw [hx] at he
  change (f.map x).2.val = ((f.map x).2.val + 1) % 2 at he
  have hv : (f.map x).2.val = 0 ∨ (f.map x).2.val = 1 := by
    have hh := (f.map x).2.isLt
    omega
  rcases hv with hv | hv <;> simp [hv] at he

/-- Actual partial Genesis replay, totalized by its absorbing failure state.
The readout retains the whole optional source regime, not only a scalar. -/
def sourceModel : LabelledProcess Derivation.Event (Option Derivation.Regime)
    (Option Derivation.Regime) where
  root := some Derivation.R2L
  step e r := r.bind (fun t => Derivation.stepE t e)
  read := id

theorem source_advance_matches (h : List Derivation.Event) (r : Option Derivation.Regime) :
    labelledAdvance sourceModel h r = r.bind (Derivation.replayE h) := by
  induction h generalizing r with
  | nil => cases r <;> rfl
  | cons e h ih =>
    cases r with
    | none => simpa [labelledAdvance,sourceModel] using ih none
    | some r =>
      rw [labelledAdvance]
      change labelledAdvance sourceModel h (Derivation.stepE r e) = _
      rw [ih]
      rfl

theorem source_run_matches (h : List Derivation.Event) :
    labelledRun sourceModel h = Derivation.replayE h Derivation.R2L := by
  change labelledAdvance sourceModel h (some Derivation.R2L) = _
  simpa using source_advance_matches h (some Derivation.R2L)

theorem source_supply_self_loop :
    sourceModel.step (.supply 0) sourceModel.root = sourceModel.root := rfl

theorem no_source_initial_in_clock_closed_class :
    ¬ Nonempty (LabelledHom sourceModel (labelledClockLift sourceModel 1)) :=
  no_clock_hom_of_self_loop sourceModel (.supply 0) sourceModel.root source_supply_self_loop

end CampaignGenesisProcessComparison

#print axioms CampaignGenesisProcessComparison.run_add
#print axioms CampaignGenesisProcessComparison.hom_run
#print axioms CampaignGenesisProcessComparison.every_challenge_answer_agrees
#print axioms CampaignGenesisProcessComparison.no_map_to_clock_lift
#print axioms CampaignGenesisProcessComparison.reduced_reachable_is_minimal
#print axioms CampaignGenesisProcessComparison.nonminimal_adequate_process
#print axioms CampaignGenesisProcessComparison.oneState_is_reduced_reachable
#print axioms CampaignGenesisProcessComparison.labelled_append
#print axioms CampaignGenesisProcessComparison.all_words_agree
#print axioms CampaignGenesisProcessComparison.no_initial_in_clock_closed_class
#print axioms CampaignGenesisProcessComparison.all_words_minimum_size

#print axioms CampaignGenesisProcessComparison.no_clock_hom_of_self_loop
#print axioms CampaignGenesisProcessComparison.source_advance_matches
#print axioms CampaignGenesisProcessComparison.source_run_matches
#print axioms CampaignGenesisProcessComparison.source_supply_self_loop
#print axioms CampaignGenesisProcessComparison.no_source_initial_in_clock_closed_class
