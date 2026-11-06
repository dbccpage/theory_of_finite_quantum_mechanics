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

/-!
## 6. Minimal Deterministic Quotient (WD2-T6)
-/

/-- The stabilized asymptotic equivalence relation `R_∞`, defined as agreement at every
finite horizon `n`. -/
def RInfinity {S A Y : Type} (observe : S → Y) (update : S → A → S) (s t : S) : Prop :=
  ∀ n : Nat, PolyRelated observe update n s t

/-- `RInfinity` is equivalent to agreement of `observe (polyRunWord update · w)` on all finite
words `w : List A`. -/
theorem rInfinity_iff_word_kernel {S A Y : Type}
    (observe : S → Y) (update : S → A → S) (s t : S) :
    RInfinity observe update s t ↔
      ∀ w : List A, observe (polyRunWord update s w) = observe (polyRunWord update t w) := by
  constructor
  · intro h w
    exact (poly_word_kernel_agreement observe update w.length s t).mp (h w.length) w (Nat.le_refl _)
  · intro h n
    apply (poly_word_kernel_agreement observe update n s t).mpr
    intro w _
    exact h w

/-- Theorem WD2-T6 (part 1): `RInfinity` is an observation-preserving update congruence and
contains every observation-preserving update congruence on `S` (it is the coarsest such relation). -/
theorem rInfinity_coarsest_congruence {S A Y : Type}
    (observe : S → Y) (update : S → A → S) :
    (∀ s t, RInfinity observe update s t → observe s = observe t) ∧
    (∀ a s t, RInfinity observe update s t →
      RInfinity observe update (update s a) (update t a)) ∧
    (∀ (R : S → S → Prop),
      (∀ s t, R s t → observe s = observe t) →
      (∀ a s t, R s t → R (update s a) (update t a)) →
      ∀ s t, R s t → RInfinity observe update s t) := by
  refine ⟨?_, ?_, ?_⟩
  · intro s t h
    exact h 0
  · intro a s t h n
    exact (h (n + 1)).2 a
  · intro R hobs hupd s t hR n
    induction n generalizing s t with
    | zero => exact hobs s t hR
    | succ n ih => exact ⟨hobs s t hR, fun a => ih (update s a) (update t a) (hupd a s t hR)⟩

/-- When `PolyRelated` stabilizes at horizon `N`, `PolyRelated observe update N` coincides with
`RInfinity observe update`. -/
theorem stabilized_polyRelated_iff_rInfinity {S A Y : Type}
    (observe : S → Y) (update : S → A → S) (N : Nat)
    (hstab : ∀ s t, PolyRelated observe update N s t → PolyRelated observe update (N + 1) s t)
    (s t : S) :
    PolyRelated observe update N s t ↔ RInfinity observe update s t := by
  constructor
  · intro hN
    apply (rInfinity_coarsest_congruence observe update).2.2 (PolyRelated observe update N)
    · intro x y hxy
      exact polyRelated_observe hxy
    · intro a x y hxy
      exact (hstab x y hxy).2 a
    · exact hN
  · intro hInf
    exact hInf N

/-- `RInfinity` forms a `Setoid` on `S`. -/
def rInfinitySetoid {S A Y : Type} (observe : S → Y) (update : S → A → S) : Setoid S where
  r := RInfinity observe update
  iseqv := {
    refl := fun x n => by
      rw [poly_word_kernel_agreement]
      intro _ _
      rfl
    symm := fun h n => by
      rw [poly_word_kernel_agreement]
      intro w hw
      exact ((poly_word_kernel_agreement observe update n _ _).mp (h n) w hw).symm
    trans := fun h1 h2 n => by
      rw [poly_word_kernel_agreement]
      intro w hw
      exact ((poly_word_kernel_agreement observe update n _ _).mp (h1 n) w hw).trans
        ((poly_word_kernel_agreement observe update n _ _).mp (h2 n) w hw)
  }

/-- The minimal deterministic quotient carrier `S / R_∞`. -/
abbrev MinimalQuotient {S A Y : Type} (observe : S → Y) (update : S → A → S) :=
  Quotient (rInfinitySetoid observe update)

/-- Descended observation map on `S / R_∞`. -/
def minimalObserve {S A Y : Type} (observe : S → Y) (update : S → A → S) :
    MinimalQuotient observe update → Y :=
  Quotient.lift observe (fun s t h => (rInfinity_coarsest_congruence observe update).1 s t h)

/-- Descended update map on `S / R_∞`. -/
def minimalUpdate {S A Y : Type} (observe : S → Y) (update : S → A → S) :
    MinimalQuotient observe update → A → MinimalQuotient observe update :=
  fun q a =>
    Quotient.lift
      (fun s => Quotient.mk (rInfinitySetoid observe update) (update s a))
      (fun s t h => Quotient.sound ((rInfinity_coarsest_congruence observe update).2.1 a s t h))
      q

/-- Descended observation on any compatible deterministic quotient `Quotient R`. -/
def congruenceObserve {S Y : Type} (observe : S → Y) (R : Setoid S)
    (hobserve : ∀ s t, R.r s t → observe s = observe t) : Quotient R → Y :=
  Quotient.lift observe hobserve

/-- Descended update on any compatible deterministic quotient `Quotient R`. -/
def congruenceUpdate {S A : Type} (update : S → A → S) (R : Setoid S)
    (hupdate : ∀ a s t, R.r s t → R.r (update s a) (update t a)) :
    Quotient R → A → Quotient R :=
  fun q a =>
    Quotient.lift (fun s => Quotient.mk R (update s a))
      (fun s t h => Quotient.sound (hupdate a s t h)) q

/-- Canonical comparison map from any compatible deterministic quotient `Quotient R` to `S / R_∞`. -/
def comparisonMap {S A Y : Type} (observe : S → Y) (update : S → A → S)
    (R : Setoid S)
    (hobserve : ∀ s t, R.r s t → observe s = observe t)
    (hupdate : ∀ a s t, R.r s t → R.r (update s a) (update t a)) :
    Quotient R → MinimalQuotient observe update :=
  Quotient.lift (Quotient.mk (rInfinitySetoid observe update))
    (fun s t h => Quotient.sound
      ((rInfinity_coarsest_congruence observe update).2.2 R.r hobserve hupdate s t h))

theorem minimal_runWord {S A Y : Type} (observe : S → Y) (update : S → A → S)
    (s : S) (w : List A) :
    polyRunWord (minimalUpdate observe update)
      (Quotient.mk (rInfinitySetoid observe update) s) w =
      Quotient.mk (rInfinitySetoid observe update) (polyRunWord update s w) := by
  induction w generalizing s with
  | nil => rfl
  | cons a w' ih => exact ih (update s a)

/-- Theorem WD2-T6 (part 2, minimal deterministic quotient factorization):
For any observation-preserving update congruence `R : Setoid S`, the canonical comparison map
`comparisonMap` from `Quotient R` to the minimal deterministic quotient `MinimalQuotient` (`S / R_∞`):
(1) commutes with the quotient projections,
(2) preserves the descended observation map,
(3) intertwines all descended update actions,
(4) is surjective onto `S / R_∞`,
(5) is the unique map commuting with the quotient projections, and
(6) `S / R_∞` itself has no distinct `RInfinity`-indistinguishable classes. -/
theorem minimal_deterministic_quotient_factorization {S A Y : Type}
    (observe : S → Y) (update : S → A → S)
    (R : Setoid S)
    (hobserve : ∀ s t, R.r s t → observe s = observe t)
    (hupdate : ∀ a s t, R.r s t → R.r (update s a) (update t a)) :
    let π := comparisonMap observe update R hobserve hupdate
    (∀ x : S,
      π (Quotient.mk R x) = Quotient.mk (rInfinitySetoid observe update) x) ∧
    (∀ q : Quotient R,
      minimalObserve observe update (π q) = congruenceObserve observe R hobserve q) ∧
    (∀ a : A, ∀ q : Quotient R,
      π (congruenceUpdate update R hupdate q a) =
        minimalUpdate observe update (π q) a) ∧
    (∀ q : MinimalQuotient observe update, ∃ p : Quotient R, π p = q) ∧
    (∀ g : Quotient R → MinimalQuotient observe update,
      (∀ x : S, g (Quotient.mk R x) = Quotient.mk (rInfinitySetoid observe update) x) →
      g = π) ∧
    (∀ p q : MinimalQuotient observe update,
      RInfinity (minimalObserve observe update) (minimalUpdate observe update) p q →
      p = q) := by
  dsimp only
  refine ⟨fun _ => rfl, ?_, ?_, ?_, ?_, ?_⟩
  · intro q
    refine Quotient.inductionOn q (fun _ => rfl)
  · intro a q
    refine Quotient.inductionOn q (fun _ => rfl)
  · intro q
    refine Quotient.inductionOn q (fun x => ⟨Quotient.mk R x, rfl⟩)
  · intro g hg
    funext q
    refine Quotient.inductionOn q (fun x => hg x)
  · intro p q
    refine Quotient.inductionOn₂ p q ?_
    intro x y hxy
    apply Quotient.sound
    apply (rInfinity_iff_word_kernel observe update x y).mpr
    intro w
    have hw := (rInfinity_iff_word_kernel
      (minimalObserve observe update) (minimalUpdate observe update)
      (Quotient.mk (rInfinitySetoid observe update) x)
      (Quotient.mk (rInfinitySetoid observe update) y)).mp hxy w
    rw [minimal_runWord, minimal_runWord] at hw
    exact hw

end Wd2

