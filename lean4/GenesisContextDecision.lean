import GenesisComputation
import Mathlib.Tactic

/-!
AuthorityEffect: None. Complete slot-tuple observation for a finite Genesis
regime, including arbitrary admitted arities, multiple holes and uniform rules.
This extends the existing token-erased Regime; it does not verify Python replay.
-/

namespace GenesisContextDecision

open GenesisComputation.GenesisCopy

abbrev Slot := Option Nat
abbrev Context := Nat × List Slot

def slotValid (n : Nat) : Slot → Prop
  | none => True
  | some d => d < n

instance (n : Nat) (s : Slot) : Decidable (slotValid n s) := by
  cases s <;> unfold slotValid <;> infer_instance

def options (n : Nat) : List Slot := none :: (List.range n).map some

/-- Hole first, then datum index, with the last slot varying fastest. -/
def slotTuples (n : Nat) : Nat → List (List Slot)
  | 0 => [[]]
  | k + 1 => (options n).flatMap fun s => (slotTuples n k).map (s :: ·)

theorem mem_options (n : Nat) (s : Slot) : s ∈ options n ↔ slotValid n s := by
  cases s <;> simp [options, slotValid]

theorem mem_slotTuples (n k : Nat) (xs : List Slot) :
    xs ∈ slotTuples n k ↔ xs.length = k ∧ ∀ s ∈ xs, slotValid n s := by
  induction k generalizing xs with
  | zero => cases xs <;> simp [slotTuples]
  | succ k ih =>
    cases xs with
    | nil => simp [slotTuples]
    | cons a xs => simp [slotTuples, List.mem_flatMap, mem_options, ih, and_assoc, and_left_comm, and_comm]

def WellFormed (r : Regime) (c : Context) : Prop :=
  c.1 < r.forms.length ∧ c.2.length = r.forms.getD c.1 0 ∧
    none ∈ c.2 ∧ ∀ s ∈ c.2, slotValid r.data s

def contexts (r : Regime) : List Context :=
  (List.range r.forms.length).flatMap fun f =>
    ((slotTuples r.data (r.forms.getD f 0)).filter (fun xs => none ∈ xs)).map (f, ·)

/-- Completeness over all raw well-formed contexts, not a unary or arity-bound mirror. -/
theorem mem_contexts (r : Regime) (c : Context) : c ∈ contexts r ↔ WellFormed r c := by
  rcases c with ⟨f, xs⟩
  simp [contexts, WellFormed, List.mem_flatMap, mem_slotTuples, and_assoc, and_left_comm, and_comm]

def plug (c : Context) (d : Nat) : Inst := (c.1, c.2.map (fun s => s.getD d))
def Derivable (r : Regime) (inst : Inst) : Prop := inst.1 ∈ r.rules ∨ inst ∈ r.insts
instance (r : Regime) (inst : Inst) : Decidable (Derivable r inst) := by
  unfold Derivable; infer_instance

def Collapsed (r : Regime) (i j : Nat) : Prop :=
  ∀ c, WellFormed r c → (Derivable r (plug c i) ↔ Derivable r (plug c j))
def Separable (r : Regime) (i j : Nat) : Prop :=
  ∃ c, WellFormed r c ∧ ¬ (Derivable r (plug c i) ↔ Derivable r (plug c j))

def collapseTest (r : Regime) (i j : Nat) : Bool :=
  (contexts r).all fun c => decide (Derivable r (plug c i) ↔ Derivable r (plug c j))

theorem collapseTest_correct (r : Regime) (i j : Nat) :
    collapseTest r i j = true ↔ Collapsed r i j := by
  simp [collapseTest, List.all_eq_true, mem_contexts, Collapsed]

instance (r : Regime) (i j : Nat) : Decidable (Collapsed r i j) :=
  decidable_of_iff (collapseTest r i j = true) (collapseTest_correct r i j)

theorem separable_iff_not_collapsed (r : Regime) (i j : Nat) :
    Separable r i j ↔ ¬ Collapsed r i j := by
  simp [Separable, Collapsed, not_forall, not_imp]

instance (r : Regime) (i j : Nat) : Decidable (Separable r i j) :=
  decidable_of_iff (¬ Collapsed r i j) (separable_iff_not_collapsed r i j).symm

/-- Returns the first distinguishing context in the source's deterministic order. -/
def witness (r : Regime) (i j : Nat) : Option Context :=
  (contexts r).find? fun c => decide (¬ (Derivable r (plug c i) ↔ Derivable r (plug c j)))

theorem witness_none_iff (r : Regime) (i j : Nat) :
    witness r i j = none ↔ Collapsed r i j := by
  simp [witness, List.find?_eq_none, mem_contexts, Collapsed]

theorem witness_sound {r : Regime} {i j : Nat} {c : Context} (h : witness r i j = some c) :
    WellFormed r c ∧ ¬ (Derivable r (plug c i) ↔ Derivable r (plug c j)) := by
  have hm := List.mem_of_find?_eq_some h
  have hp := List.find?_some h
  exact ⟨(mem_contexts r c).mp hm, by simpa using hp⟩

def profile (r : Regime) (d : Nat) : Finset Context :=
  ((contexts r).filter (fun c => decide (Derivable r (plug c d)))).toFinset

theorem mem_profile (r : Regime) (d : Nat) (c : Context) :
    c ∈ profile r d ↔ WellFormed r c ∧ Derivable r (plug c d) := by
  simp [profile, mem_contexts]

theorem profile_eq_iff (r : Regime) (i j : Nat) :
    profile r i = profile r j ↔ Collapsed r i j := by
  constructor
  · intro h c hc
    have := Finset.ext_iff.mp h c
    simpa [mem_profile, hc] using this
  · intro h
    ext c
    simp only [mem_profile]
    by_cases hc : WellFormed r c
    · simp [hc, h c hc]
    · simp [hc]

def HoldsTwo (r : Regime) : Prop :=
  ∃ i ∈ List.range r.data, ∃ j ∈ List.range r.data, Separable r i j
instance (r : Regime) : Decidable (HoldsTwo r) := by
  unfold HoldsTwo; infer_instance

def Exhausted (r : Regime) (f : Nat) : Prop :=
  ∀ c, WellFormed r c → c.1 = f → ∀ i ∈ List.range r.data, ∀ j ∈ List.range r.data,
    (Derivable r (plug c i) ↔ Derivable r (plug c j))
def exhaustionTest (r : Regime) (f : Nat) : Bool :=
  ((contexts r).filter (fun c => c.1 = f)).all fun c =>
    (List.range r.data).all fun i => (List.range r.data).all fun j =>
      decide (Derivable r (plug c i) ↔ Derivable r (plug c j))

theorem exhaustionTest_correct (r : Regime) (f : Nat) :
    exhaustionTest r f = true ↔ Exhausted r f := by
  simp only [exhaustionTest, List.all_eq_true, List.mem_filter, mem_contexts, decide_eq_true_eq]
  constructor
  · intro h c hc hcf i hi j hj
    exact h c ⟨hc, hcf⟩ i hi j hj
  · intro h c hc i hi j hj
    exact h c hc.1 hc.2 i hi j hj

instance (r : Regime) (f : Nat) : Decidable (Exhausted r f) :=
  decidable_of_iff (exhaustionTest r f = true) (exhaustionTest_correct r f)

theorem uniform_rule_exhausted (r : Regime) (f : Nat) (hf : f ∈ r.rules) : Exhausted r f := by
  intro c _ hcf i _ j _
  have hi : Derivable r (plug c i) := Or.inl (by simpa [plug, hcf] using hf)
  have hj : Derivable r (plug c j) := Or.inl (by simpa [plug, hcf] using hf)
  exact iff_of_true hi hj

/-- Explicit finite image, so no classical quotient representation is needed to run it. -/
def classes (r : Regime) : Finset (Finset Context) :=
  ((List.range r.data).map (profile r)).toFinset
def classCount (r : Regime) : Nat := (classes r).card

theorem mem_classes (r : Regime) (p : Finset Context) :
    p ∈ classes r ↔ ∃ i, i < r.data ∧ profile r i = p := by
  simp [classes]

theorem holdsTwo_iff_classCount (r : Regime) : HoldsTwo r ↔ 2 ≤ classCount r := by
  constructor
  · rintro ⟨i, hi, j, hj, hsep⟩
    have hne : profile r i ≠ profile r j := fun h =>
      (separable_iff_not_collapsed r i j).mp hsep ((profile_eq_iff r i j).mp h)
    have hcard : 1 < (classes r).card := Finset.one_lt_card.mpr
      ⟨profile r i, (mem_classes r _).mpr ⟨i, List.mem_range.mp hi, rfl⟩,
       profile r j, (mem_classes r _).mpr ⟨j, List.mem_range.mp hj, rfl⟩, hne⟩
    exact hcard
  · intro h
    obtain ⟨a, ha, b, hb, hne⟩ := Finset.one_lt_card.mp (show 1 < (classes r).card from h)
    obtain ⟨i, hi, hia⟩ := (mem_classes r a).mp ha
    obtain ⟨j, hj, hjb⟩ := (mem_classes r b).mp hb
    refine ⟨i, List.mem_range.mpr hi, j, List.mem_range.mpr hj,
      (separable_iff_not_collapsed r i j).mpr ?_⟩
    intro hc
    apply hne
    rw [← hia, ← hjb]
    exact (profile_eq_iff r i j).mpr hc

def observationSetoid (r : Regime) : Setoid (Fin r.data) where
  r i j := Collapsed r i.val j.val
  iseqv := by
    constructor
    · intro i; exact (profile_eq_iff r i.val i.val).mp rfl
    · intro i j h
      exact (profile_eq_iff r j.val i.val).mp ((profile_eq_iff r i.val j.val).mpr h).symm
    · intro i j k h₁ h₂
      exact (profile_eq_iff r i.val k.val).mp
        (((profile_eq_iff r i.val j.val).mpr h₁).trans ((profile_eq_iff r j.val k.val).mpr h₂))

def quotientProfile (r : Regime) : Quotient (observationSetoid r) → Finset Context :=
  Quotient.lift (fun i => profile r i.val)
    (fun i j h => (profile_eq_iff r i.val j.val).mpr h)

theorem quotientProfile_injective (r : Regime) : Function.Injective (quotientProfile r) := by
  intro x y
  induction x using Quotient.inductionOn with
  | h x =>
    induction y using Quotient.inductionOn with
    | h y =>
      intro h
      exact Quotient.sound ((profile_eq_iff r x.val y.val).mp h)

/-- The computed natural number counts the actual observational quotient of admitted data. -/
theorem classCount_eq_quotient_card (r : Regime) :
    classCount r = Nat.card (Quotient (observationSetoid r)) := by
  classical
  let : Fintype (Quotient (observationSetoid r)) := Fintype.ofFinite _
  have image_eq : (Finset.univ.image (quotientProfile r)) = classes r := by
    ext p
    simp only [Finset.mem_image, Finset.mem_univ, true_and, mem_classes]
    constructor
    · rintro ⟨q, hq⟩
      induction q using Quotient.inductionOn with
      | h d => exact ⟨d.val, d.isLt, hq⟩
    · rintro ⟨i, hi, hp⟩
      exact ⟨Quotient.mk _ ⟨i, hi⟩, hp⟩
  unfold classCount
  rw [← image_eq, Finset.card_image_of_injective _ (quotientProfile_injective r)]
  simp [Nat.card_eq_fintype_card]

def binaryOnly : Regime := ⟨2, [2], [(0, [0, 1])], [], []⟩
def multiHoleOnly : Regime := ⟨2, [2], [(0, [0, 0])], [], []⟩
def ruledBinary : Regime := ⟨2, [2], [(0, [0, 1])], [0], []⟩

theorem binary_separation : witness binaryOnly 0 1 = some (0, [none, some 1]) := by decide
theorem multi_hole_witness : witness multiHoleOnly 0 1 = some (0, [none, none]) := by decide
theorem uniform_rule_merges : Collapsed ruledBinary 0 1 := by decide
theorem explicit_class_counts : classCount binaryOnly = 2 ∧ classCount ruledBinary = 1 ∧
    classCount ⟨0, [], [], [], []⟩ = 0 := by decide
theorem full_context_decides_holding : HoldsTwo binaryOnly ∧ ¬ HoldsTwo ruledBinary := by decide

end GenesisContextDecision

#print axioms GenesisContextDecision.mem_options
#print axioms GenesisContextDecision.mem_slotTuples
#print axioms GenesisContextDecision.mem_contexts
#print axioms GenesisContextDecision.collapseTest_correct
#print axioms GenesisContextDecision.separable_iff_not_collapsed
#print axioms GenesisContextDecision.witness_none_iff
#print axioms GenesisContextDecision.witness_sound
#print axioms GenesisContextDecision.mem_profile
#print axioms GenesisContextDecision.profile_eq_iff
#print axioms GenesisContextDecision.exhaustionTest_correct
#print axioms GenesisContextDecision.uniform_rule_exhausted
#print axioms GenesisContextDecision.mem_classes
#print axioms GenesisContextDecision.holdsTwo_iff_classCount
#print axioms GenesisContextDecision.quotientProfile_injective
#print axioms GenesisContextDecision.classCount_eq_quotient_card
#print axioms GenesisContextDecision.binary_separation
#print axioms GenesisContextDecision.multi_hole_witness
#print axioms GenesisContextDecision.uniform_rule_merges
#print axioms GenesisContextDecision.explicit_class_counts
#print axioms GenesisContextDecision.full_context_decides_holding
