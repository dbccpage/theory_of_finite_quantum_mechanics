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

/-!
## WD2-L1: Word-Kernel Characterization (TFQ-0559)
-/

/-- Execute an input word from left to right on a concrete `Nat` state space. -/
def runWord (update : Nat → Nat → Nat) : Nat → List Nat → Nat
  | s, [] => s
  | s, σ :: w => runWord update (update s σ) w

/-- Every symbol of `w` belongs to the declared finite alphabet. -/
def WordInAlphabet (alphabet : List Nat) (w : List Nat) : Prop :=
  ∀ σ, σ ∈ w → σ ∈ alphabet

theorem wordInAlphabet_nil (alphabet : List Nat) : WordInAlphabet alphabet [] := by
  intro _ h
  cases h

theorem wordInAlphabet_cons {alphabet : List Nat} {σ : Nat} {w : List Nat} :
    WordInAlphabet alphabet (σ :: w) ↔ σ ∈ alphabet ∧ WordInAlphabet alphabet w := by
  constructor
  · intro h
    refine ⟨h σ List.mem_cons_self, ?_⟩
    intro τ hτ
    exact h τ (List.mem_cons_of_mem σ hτ)
  · rintro ⟨hσ, hw⟩ τ hτ
    rcases List.mem_cons.mp hτ with rfl | hτ'
    · exact hσ
    · exact hw τ hτ'

/-- Lemma WD2-L1 (computational `Bool` form): `related observe update alphabet n s t = true`
holds if and only if `s` and `t` have identical readouts after every word over `alphabet`
of length at most `n`. -/
theorem word_kernel_agreement (observe : Nat → Nat) (update : Nat → Nat → Nat)
    (alphabet : List Nat) (n s t : Nat) :
    related observe update alphabet n s t = true ↔
      ∀ w : List Nat, WordInAlphabet alphabet w → w.length ≤ n →
        observe (runWord update s w) = observe (runWord update t w) := by
  induction n generalizing s t with
  | zero =>
      simp only [related, beq_iff_eq]
      constructor
      · intro h w _ hwlen
        cases w with
        | nil => exact h
        | cons _ _ => cases hwlen
      · intro h
        exact h [] (wordInAlphabet_nil alphabet) (Nat.le_refl 0)
  | succ n ih =>
      simp only [related, Bool.and_eq_true, beq_iff_eq, List.all_eq_true]
      constructor
      · rintro ⟨h0, hstep⟩ w hw hlen
        cases w with
        | nil => exact h0
        | cons σ w' =>
            have ⟨hσ, hw'⟩ := wordInAlphabet_cons.mp hw
            have hlen' : w'.length ≤ n := Nat.le_of_succ_le_succ hlen
            exact (ih (update s σ) (update t σ)).mp (hstep σ hσ) w' hw' hlen'
      · intro h
        refine ⟨h [] (wordInAlphabet_nil alphabet) (Nat.zero_le (n + 1)), ?_⟩
        intro σ hσ
        apply (ih (update s σ) (update t σ)).mpr
        intro w' hw' hlen'
        have hw : WordInAlphabet alphabet (σ :: w') :=
          wordInAlphabet_cons.mpr ⟨hσ, hw'⟩
        have hlen : (σ :: w').length ≤ n + 1 := Nat.succ_le_succ hlen'
        exact h (σ :: w') hw hlen

/-- Polymorphic horizon relation `R_n` over arbitrary state, symbol, and output types. -/
def PolyRelated {State Symbol Output : Type} (observe : State → Output)
    (update : State → Symbol → State) : Nat → State → State → Prop
  | 0, s, t => observe s = observe t
  | n + 1, s, t =>
      observe s = observe t ∧
        ∀ σ : Symbol, PolyRelated observe update n (update s σ) (update t σ)

/-- Polymorphic left-to-right word execution. -/
def polyRunWord {State Symbol : Type} (update : State → Symbol → State) :
    State → List Symbol → State
  | s, [] => s
  | s, σ :: w => polyRunWord update (update s σ) w

theorem polyRelated_observe {State Symbol Output : Type}
    {observe : State → Output} {update : State → Symbol → State}
    {n : Nat} {s t : State} (h : PolyRelated observe update n s t) :
    observe s = observe t := by
  cases n with
  | zero => exact h
  | succ _ => exact h.1

theorem polyRelated_mono {State Symbol Output : Type}
    {observe : State → Output} {update : State → Symbol → State}
    {n : Nat} {s t : State} (h : PolyRelated observe update (n + 1) s t) :
    PolyRelated observe update n s t := by
  induction n generalizing s t with
  | zero => exact h.1
  | succ _ ih =>
      refine ⟨h.1, ?_⟩
      intro σ
      exact ih (h.2 σ)

/-- Lemma WD2-L1 (polymorphic form): `PolyRelated` at horizon `n` coincides with
the intersection of word readout kernels of length at most `n`. -/
theorem poly_word_kernel_agreement {State Symbol Output : Type}
    (observe : State → Output) (update : State → Symbol → State)
    (n : Nat) (s t : State) :
    PolyRelated observe update n s t ↔
      ∀ w : List Symbol, w.length ≤ n →
        observe (polyRunWord update s w) = observe (polyRunWord update t w) := by
  induction n generalizing s t with
  | zero =>
      constructor
      · intro h w hw
        cases w with
        | nil => exact h
        | cons _ _ => cases hw
      · intro h
        exact h [] (Nat.le_refl 0)
  | succ n ih =>
      constructor
      · rintro ⟨h0, hstep⟩ w hw
        cases w with
        | nil => exact h0
        | cons σ w' =>
            exact (ih (update s σ) (update t σ)).mp (hstep σ) w' (Nat.le_of_succ_le_succ hw)
      · intro h
        refine ⟨h [] (Nat.zero_le (n + 1)), ?_⟩
        intro σ
        apply (ih (update s σ) (update t σ)).mpr
        intro w' hw'
        exact h (σ :: w') (Nat.succ_le_succ hw')

/-!
## WD2-T2: Finite Stabilization Pigeonhole Bound and Sharp Chain (TFQ-0561)
-/

/-- If each strict refinement step `k < N` increases the partition class count `b k` by at least
one, then at step `N` the class count is at least `b 0 + N`. -/
theorem strict_refinement_count_lower_bound (b : Nat → Nat) (N : Nat)
    (hstrict : ∀ k, k < N → b k + 1 ≤ b (k + 1)) :
    b 0 + N ≤ b N := by
  induction N with
  | zero => simp
  | succ N ih =>
      have ih' : b 0 + N ≤ b N := ih (fun k hk => hstrict k (Nat.lt_succ_of_lt hk))
      have hstep : b N + 1 ≤ b (N + 1) := hstrict N (Nat.lt_succ_self N)
      omega

/-- Theorem WD2-T2 (general partition-cardinality pigeonhole bound):
Any sequence of partition class counts `b` that strictly increases for `N` consecutive steps
and is bounded above by the finite state cardinality `cardS` satisfies `N ≤ cardS - b 0`. -/
theorem stabilization_horizon_le_card_sub_b0 (b : Nat → Nat) (cardS N : Nat)
    (hstrict : ∀ k, k < N → b k + 1 ≤ b (k + 1))
    (hbound : b N ≤ cardS) :
    N ≤ cardS - b 0 := by
  have hlow : b 0 + N ≤ b N := strict_refinement_count_lower_bound b N hstrict
  omega

/-- Executing `k` steps of symbol `0` on `sharpUpdate size` advances any state `s ≤ size - 1`
to `min (s + k) (size - 1)`. -/
theorem runWord_sharpUpdate_replicate (size s k : Nat) (hs : s ≤ size - 1) :
    runWord (sharpUpdate size) s (List.replicate k 0) = min (s + k) (size - 1) := by
  induction k generalizing s with
  | zero =>
      simp only [List.replicate, runWord]
      omega
  | succ k ih =>
      simp only [List.replicate_succ, runWord, sharpUpdate, ↓reduceIte]
      have hs' : min (s + 1) (size - 1) ≤ size - 1 := Nat.min_le_right (s + 1) (size - 1)
      rw [ih (min (s + 1) (size - 1)) hs']
      omega

/-- Theorem WD2-T2 (general sharpness witness): for every chain size `m ≥ 2`, the word of length
`m - 2` consisting of `m - 2` copies of symbol `0` separates state `0` (readout `0`) from state `1`
(readout `1`), witnessing the sharp stabilization depth `N = m - 2 = |S| - b_0`. -/
theorem sharp_chain_general_witness (m : Nat) (hm : 2 ≤ m) :
    let observe := sharpObserve m
    let update := sharpUpdate m
    let w := List.replicate (m - 2) 0
    w.length = m - 2 ∧
      observe (runWord update 0 w) = 0 ∧
      observe (runWord update 1 w) = 1 ∧
      observe (runWord update 0 w) ≠ observe (runWord update 1 w) := by
  dsimp only
  have h0 : runWord (sharpUpdate m) 0 (List.replicate (m - 2) 0) = m - 2 := by
    rw [runWord_sharpUpdate_replicate m 0 (m - 2) (by omega)]
    omega
  have h1 : runWord (sharpUpdate m) 1 (List.replicate (m - 2) 0) = m - 1 := by
    rw [runWord_sharpUpdate_replicate m 1 (m - 2) (by omega)]
    omega
  have hobs0 : sharpObserve m (m - 2) = 0 := by
    unfold sharpObserve
    split
    · omega
    · split
      · omega
      · rfl
  have hobs1 : sharpObserve m (m - 1) = 1 := by
    unfold sharpObserve
    split
    · omega
    · split
      · rfl
      · omega
  refine ⟨List.length_replicate, ?_, ?_, ?_⟩
  · rw [h0, hobs0]
  · rw [h1, hobs1]
  · rw [h0, h1, hobs0, hobs1]
    decide

/-!
## WD2-T3: Four-Way No-Escape Update-Congruence Equivalence (TFQ-0562)
-/

/-- `R_0 = ker observe` is an update congruence when every one-step transition preserves
observation equality. -/
def IsUpdateCongruence {State Symbol Output : Type}
    (observe : State → Output) (update : State → Symbol → State) : Prop :=
  ∀ s t σ, observe s = observe t → observe (update s σ) = observe (update t σ)

theorem isUpdateCongruence_iff_r1_eq_r0 {State Symbol Output : Type}
    (observe : State → Output) (update : State → Symbol → State) :
    IsUpdateCongruence observe update ↔
      (∀ s t, PolyRelated observe update 1 s t ↔ PolyRelated observe update 0 s t) := by
  constructor
  · intro hcong s t
    simp only [PolyRelated]
    constructor
    · intro h
      exact h.1
    · intro h0
      exact ⟨h0, fun σ => hcong s t σ h0⟩
  · intro hr1 s t σ h0
    exact ((hr1 s t).mpr h0).2 σ

theorem r1_eq_r0_iff_forall_rn_eq_r0 {State Symbol Output : Type}
    (observe : State → Output) (update : State → Symbol → State) :
    (∀ s t, PolyRelated observe update 1 s t ↔ PolyRelated observe update 0 s t) ↔
      (∀ n s t, PolyRelated observe update n s t ↔ PolyRelated observe update 0 s t) := by
  constructor
  · intro hr1 n
    induction n with
    | zero =>
        intro s t
        exact Iff.rfl
    | succ n ih =>
        intro s t
        simp only [PolyRelated]
        have hstep :
            (∀ σ, PolyRelated observe update n (update s σ) (update t σ)) ↔
              (∀ σ, observe (update s σ) = observe (update t σ)) := by
          constructor
          · intro h σ
            exact (ih (update s σ) (update t σ)).mp (h σ)
          · intro h σ
            exact (ih (update s σ) (update t σ)).mpr (h σ)
        rw [hstep]
        exact hr1 s t
  · intro hall s t
    exact hall 1 s t

theorem forall_rn_eq_r0_iff_no_separating_word {State Symbol Output : Type}
    (observe : State → Output) (update : State → Symbol → State) :
    (∀ n s t, PolyRelated observe update n s t ↔ PolyRelated observe update 0 s t) ↔
      (∀ s t, observe s = observe t →
        ∀ w : List Symbol, observe (polyRunWord update s w) = observe (polyRunWord update t w)) := by
  constructor
  · intro hall s t h0 w
    have hrel : PolyRelated observe update w.length s t := (hall w.length s t).mpr h0
    exact (poly_word_kernel_agreement observe update w.length s t).mp hrel w (Nat.le_refl w.length)
  · intro hnoword n s t
    constructor
    · intro hrel
      exact polyRelated_observe hrel
    · intro h0
      apply (poly_word_kernel_agreement observe update n s t).mpr
      intro w _
      exact hnoword s t h0 w

/-- Theorem WD2-T3 (four-way no-escape equivalence):
(1) `R_0` is an update congruence;
(2) `R_1 = R_0`;
(3) `R_n = R_0` for all `n ≥ 0`;
(4) no pair in `R_0` admits a separating word. -/
theorem no_escape_equivalence {State Symbol Output : Type}
    (observe : State → Output) (update : State → Symbol → State) :
    (IsUpdateCongruence observe update ↔
      (∀ s t, PolyRelated observe update 1 s t ↔ PolyRelated observe update 0 s t)) ∧
    ((∀ s t, PolyRelated observe update 1 s t ↔ PolyRelated observe update 0 s t) ↔
      (∀ n s t, PolyRelated observe update n s t ↔ PolyRelated observe update 0 s t)) ∧
    ((∀ n s t, PolyRelated observe update n s t ↔ PolyRelated observe update 0 s t) ↔
      (∀ s t, observe s = observe t →
        ∀ w : List Symbol, observe (polyRunWord update s w) = observe (polyRunWord update t w))) :=
  ⟨isUpdateCongruence_iff_r1_eq_r0 observe update,
   r1_eq_r0_iff_forall_rn_eq_r0 observe update,
   forall_rn_eq_r0_iff_no_separating_word observe update⟩

/-!
## WD2-T4: Shortest Separating Word Construction (TFQ-0563)
-/

theorem exists_of_list_all_eq_false {α : Type} (p : α → Bool) (l : List α)
    (h : l.all p = false) : ∃ a, a ∈ l ∧ p a = false := by
  induction l with
  | nil => cases h
  | cons head tail ih =>
      simp only [List.all_cons] at h
      cases hhead : p head with
      | false =>
          exact ⟨head, List.mem_cons_self, hhead⟩
      | true =>
          rw [hhead, Bool.true_and] at h
          rcases ih h with ⟨a, ha, hpa⟩
          exact ⟨a, List.mem_cons_of_mem head ha, hpa⟩

theorem related_observe_eq (observe : Nat → Nat) (update : Nat → Nat → Nat)
    (alphabet : List Nat) (n s t : Nat)
    (h : related observe update alphabet n s t = true) :
    (observe s == observe t) = true := by
  cases n with
  | zero => exact h
  | succ _ =>
      simp only [related, Bool.and_eq_true] at h
      exact h.1

/-- Theorem WD2-T4 (shortest separating word length and recursive witness construction):
If `(s, t)` lies in `R_n \ R_{n+1}`, then no word over `alphabet` of length at most `n`
separates `s` and `t`, and there exists a separating word over `alphabet` of length `n + 1`. -/
theorem shortest_separating_word (observe : Nat → Nat) (update : Nat → Nat → Nat)
    (alphabet : List Nat) (n s t : Nat)
    (hin : related observe update alphabet n s t = true)
    (hout : related observe update alphabet (n + 1) s t = false) :
    (∀ w : List Nat, WordInAlphabet alphabet w → w.length ≤ n →
      observe (runWord update s w) = observe (runWord update t w)) ∧
    (∃ w : List Nat, WordInAlphabet alphabet w ∧ w.length = n + 1 ∧
      observe (runWord update s w) ≠ observe (runWord update t w)) := by
  refine ⟨(word_kernel_agreement observe update alphabet n s t).mp hin, ?_⟩
  induction n generalizing s t with
  | zero =>
      have h0 : (observe s == observe t) = true := hin
      simp only [related, h0, Bool.true_and] at hout
      rcases exists_of_list_all_eq_false _ alphabet hout with ⟨σ, hσ, hsep⟩
      simp only [beq_eq_false_iff_ne] at hsep
      refine ⟨[σ], ?_, rfl, hsep⟩
      exact wordInAlphabet_cons.mpr ⟨hσ, wordInAlphabet_nil alphabet⟩
  | succ n ih =>
      have h0 : (observe s == observe t) = true :=
        related_observe_eq observe update alphabet (n + 1) s t hin
      have hin_step : ∀ σ, σ ∈ alphabet →
          related observe update alphabet n (update s σ) (update t σ) = true := by
        simp only [related, Bool.and_eq_true, List.all_eq_true] at hin
        exact hin.2
      have hout_all :
          (alphabet.all fun σ =>
            related observe update alphabet (n + 1) (update s σ) (update t σ)) = false := by
        unfold related at hout
        rw [h0, Bool.true_and] at hout
        exact hout
      rcases exists_of_list_all_eq_false _ alphabet hout_all with ⟨σ, hσ, hout_σ⟩
      rcases ih (update s σ) (update t σ) (hin_step σ hσ) hout_σ with ⟨v, hv_alpha, hv_len, hv_sep⟩
      refine ⟨σ :: v, wordInAlphabet_cons.mpr ⟨hσ, hv_alpha⟩, ?_, hv_sep⟩
      simp [hv_len]

/-!
## WD2-T5: Factored Report Preservation and Unfactored Counterexample (TFQ-0564)
-/

/-- Step-by-step report sequence emitted along a word `w` starting from state `s`. -/
def reportTrace {State Symbol Report : Type}
    (update : State → Symbol → State) (report : State → Symbol → Report) :
    State → List Symbol → List Report
  | _, [] => []
  | s, σ :: w => report s σ :: reportTrace update report (update s σ) w

/-- Theorem WD2-T5 (polymorphic form): If a step report `r(s, σ) = g(p(s), σ, p(u_σ(s)))`
factors through the before-update and after-update state observations, then any pair `(s, t)`
in `R_n` emits identical report sequences along every word of length at most `n`. -/
theorem factored_report_preserves_polyRelated {State Symbol Output Report : Type}
    (observe : State → Output) (update : State → Symbol → State)
    (g : Output → Symbol → Output → Report)
    (n : Nat) (s t : State)
    (hrel : PolyRelated observe update n s t)
    (w : List Symbol) (hw : w.length ≤ n) :
    let report := fun x σ => g (observe x) σ (observe (update x σ))
    reportTrace update report s w = reportTrace update report t w := by
  dsimp only
  induction w generalizing n s t with
  | nil => rfl
  | cons σ w' ih =>
      cases n with
      | zero => cases hw
      | succ m =>
          have h0 : observe s = observe t := hrel.1
          have hstep : PolyRelated observe update m (update s σ) (update t σ) := hrel.2 σ
          have h1 : observe (update s σ) = observe (update t σ) := polyRelated_observe hstep
          have htail := ih m (update s σ) (update t σ) hstep (Nat.le_of_succ_le_succ hw)
          simp only [reportTrace, h0, h1, htail]

/-- Theorem WD2-T5 (computational `Bool` form): Endpoint-factored step reports preserve
`Wd2.related` across all words over `alphabet` of length at most `n`. -/
theorem factored_report_preserves_related {Report : Type}
    (observe : Nat → Nat) (update : Nat → Nat → Nat) (alphabet : List Nat)
    (g : Nat → Nat → Nat → Report)
    (n s t : Nat)
    (hrel : related observe update alphabet n s t = true)
    (w : List Nat) (hw : WordInAlphabet alphabet w) (hlen : w.length ≤ n) :
    let report := fun x σ => g (observe x) σ (observe (update x σ))
    reportTrace update report s w = reportTrace update report t w := by
  dsimp only
  induction w generalizing n s t with
  | nil => rfl
  | cons σ w' ih =>
      cases n with
      | zero => cases hlen
      | succ m =>
          have ⟨hσ, hw'⟩ := wordInAlphabet_cons.mp hw
          have h0 : observe s = observe t := by
            have hbeq := related_observe_eq observe update alphabet (m + 1) s t hrel
            exact beq_iff_eq.mp hbeq
          have hstep : related observe update alphabet m (update s σ) (update t σ) = true := by
            simp only [related, Bool.and_eq_true, List.all_eq_true] at hrel
            exact hrel.2 σ hσ
          have h1 : observe (update s σ) = observe (update t σ) := by
            have hbeq := related_observe_eq observe update alphabet m (update s σ) (update t σ) hstep
            exact beq_iff_eq.mp hbeq
          have htail := ih m (update s σ) (update t σ) hstep hw' (Nat.le_of_succ_le_succ hlen)
          simp only [reportTrace, h0, h1, htail]

/-- Theorem WD2-T5 (unfactored report counterexample, §7): On `S = {0, 1}` with constant
observation `p = 0` and identity update `u_a(s) = s`, states `0` and `1` are related at every
horizon `n`, yet the unfactored report `r(s, a) = s` separates them on a one-letter word. -/
theorem unfactored_report_splits_r0 :
    let observe : Nat → Nat := fun _ => 0
    let update : Nat → Nat → Nat := fun s _ => s
    let alphabet : List Nat := [0]
    let unfactoredReport : Nat → Nat → Nat := fun s _ => s
    (∀ n : Nat, related observe update alphabet n 0 1 = true) ∧
      reportTrace update unfactoredReport 0 [0] ≠ reportTrace update unfactoredReport 1 [0] := by
  dsimp only
  refine ⟨?_, by decide⟩
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
      simp [related, ih]

end Wd2

