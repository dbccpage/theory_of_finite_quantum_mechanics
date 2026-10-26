/-
Tape theorems of the Discrete Deformation Calculus. AuthorityEffect: None.
-/
import Ddc.Law

namespace Ddc

/-- Replay composes: running `t₁ ++ t₂` runs `t₂` from where `t₁` stopped. -/
theorem run_append (t₁ t₂ : List Step) :
    ∀ c s, run c s (t₁ ++ t₂) = (run c s t₁).bind (fun p => run p.1 p.2 t₂) := by
  induction t₁ with
  | nil => intro c s; simp [run]
  | cons st rest ih =>
    intro c s
    simp only [List.cons_append, run]
    split
    · exact ih _ _
    · rfl

/-- OE010-03: lawful tapes compose; the empty tape is the identity. -/
theorem lawful_append (c : Control) (s : State) (t₁ t₂ : List Step) :
    Lawful c s (t₁ ++ t₂) ↔ ∃ c' s', run c s t₁ = some (c', s') ∧ Lawful c' s' t₂ := by
  unfold Lawful
  rw [run_append]
  cases h : run c s t₁ with
  | none => simp
  | some p =>
    obtain ⟨c', s'⟩ := p
    simp only [Option.bind_some]
    constructor
    · intro h₂; exact ⟨c', s', rfl, h₂⟩
    · rintro ⟨c'', s'', hp, h₂⟩
      cases hp
      exact h₂

theorem lawful_nil (c : Control) (s : State) : Lawful c s [] := rfl

/-- Law 2: nothing is admitted after T. -/
theorem terminal_absorbing (s : State) (st : Step) (t : List Step) :
    run .terminalized s (st :: t) = none := by
  simp [run, ctrlOk]

theorem run_last_T (c : Control) (s : State) (t : List Step) (st : Step) (hT : st.letter = .T) :
    ∀ c' s', run c s (t ++ [st]) = some (c', s') → c' = .terminalized := by
  intro c' s' h
  rw [run_append] at h
  cases h₁ : run c s t with
  | none => simp [h₁] at h
  | some p =>
    simp only [h₁, Option.bind_some, run] at h
    split at h
    · simp [hT, nextCtrl] at h
      exact h.1.symm
    · simp at h

/-- Law 2 at tape level: in a lawful tape, T is the last letter. -/
theorem lawful_T_is_last (c : Control) (s : State) (t₁ t₂ : List Step) (st : Step)
    (hT : st.letter = .T) (h : Lawful c s (t₁ ++ st :: t₂)) : t₂ = [] := by
  cases t₂ with
  | nil => rfl
  | cons st₂ rest =>
    exfalso
    have hsplit : t₁ ++ st :: st₂ :: rest = (t₁ ++ [st]) ++ st₂ :: rest := by simp
    rw [hsplit] at h
    obtain ⟨c', s', h₁, h₂⟩ := (lawful_append c s _ _).1 h
    have := run_last_T c s t₁ st hT c' s' h₁
    subst this
    simp [Lawful, terminal_absorbing] at h₂

/-- Law 3: after a refusal only C, Λ or T may follow. -/
theorem refusal_absorbing (s : State) (st : Step) (t : List Step)
    (hl : st.letter ≠ .C ∧ st.letter ≠ .L ∧ st.letter ≠ .T) :
    run .refused s (st :: t) = none := by
  obtain ⟨h1, h2, h3⟩ := hl
  simp [run, ctrlOk, h1, h2, h3]

/-- Every step of a lawful tape satisfies its letter's law. -/
theorem well_typed_step (c : Control) (s : State) (t₁ t₂ : List Step) (st : Step)
    (h : Lawful c s (t₁ ++ st :: t₂)) :
    ∃ c' s', run c s t₁ = some (c', s') ∧ stepLaw st.letter s' st.after st.witness = true := by
  obtain ⟨c', s', h₁, h₂⟩ := (lawful_append c s _ _).1 h
  refine ⟨c', s', h₁, ?_⟩
  unfold Lawful at h₂
  simp only [run] at h₂
  split at h₂
  · rename_i hc
    simp only [Bool.and_eq_true] at hc
    exact hc.2
  · simp at h₂

/-- OE010-04: every receipt a replay emits carries AuthorityEffect.none. -/
theorem authority_effect_none (t : List Step) :
    ∀ i c s, ∀ r ∈ receipts i c s t, r.authority = .none := by
  induction t with
  | nil => intro i c s r hr; simp [receipts] at hr
  | cons st rest ih =>
    intro i c s r hr
    simp only [receipts] at hr
    split at hr
    · simp only [List.mem_cons] at hr
      rcases hr with hr | hr
      · subst hr; rfl
      · exact ih _ _ _ r hr
    · simp at hr

/-- The receipt tape only grows: an earlier replay is a prefix of a later one. -/
theorem receipts_prefix (t₁ t₂ : List Step) :
    ∀ i c s, ∃ rest, receipts i c s (t₁ ++ t₂) = receipts i c s t₁ ++ rest := by
  induction t₁ with
  | nil => intro i c s; exact ⟨receipts i c s t₂, by simp [receipts]⟩
  | cons st more ih =>
    intro i c s
    simp only [List.cons_append, receipts]
    split
    · obtain ⟨rest, h⟩ := ih (i + 1) (nextCtrl c st.letter) st.after
      exact ⟨rest, by simp [h]⟩
    · exact ⟨[], by simp⟩

/-- Every paper-lawful step passes the engine's `verify_step`. -/
theorem paper_refines_engine (l : Letter) (b a : State) (w : Witness)
    (h : stepLaw l b a w = true) : engineLaw l b a = true := by
  cases l with
  | E =>
    obtain ⟨hc, -, hp, hg, -, -⟩ := law_E.1 h
    simp only [engineLaw, Bool.and_eq_true, beq_iff_eq]
    exact ⟨⟨hc, hp⟩, hg⟩
  | R =>
    obtain ⟨hc, hp, -, -⟩ := law_R.1 h
    simp only [engineLaw, Bool.and_eq_true, beq_iff_eq]
    exact ⟨hc, hp⟩
  | C => exact bne_iff_ne.2 (law_C.1 h).1
  | I => obtain ⟨hab, -⟩ := law_I.1 h; subst hab; exact beq_self_eq_true _
  | L => exact bne_iff_ne.2 (law_L.1 h).1
  | D => exact bne_iff_ne.2 (law_D.1 h).1
  | M => obtain ⟨hab, -⟩ := law_M.1 h; subst hab; exact beq_self_eq_true _
  | T =>
    obtain ⟨hab, hg, -⟩ := law_T.1 h
    subst hab
    simp only [engineLaw, Bool.and_eq_true, beq_iff_eq]
    exact ⟨trivial, hg⟩

/-- §23.3 residual-progress guard: only D or Λ may lower Φ₁ or Γ₂. -/
theorem no_free_decrease (l : Letter) (b a : State) (w : Witness)
    (h : stepLaw l b a w = true) (hdec : a.phi < b.phi ∨ a.gamma < b.gamma) :
    l = .D ∨ l = .L := by
  cases l with
  | E =>
    obtain ⟨-, hcls, hp, hg, -, -⟩ := law_E.1 h
    have := (cls_exact_iff b).1 hcls
    omega
  | R => obtain ⟨-, hp, hg, -⟩ := law_R.1 h; omega
  | C => obtain ⟨-, hp, hg⟩ := law_C.1 h; omega
  | I => obtain ⟨hab, -⟩ := law_I.1 h; subst hab; omega
  | L => exact Or.inr rfl
  | D => exact Or.inl rfl
  | M => obtain ⟨hab, -⟩ := law_M.1 h; subst hab; omega
  | T => obtain ⟨hab, -, -⟩ := law_T.1 h; subst hab; omega

/-- Witness dominance on tapes: from Γ₂ > 0, without a D or Λ step, a lawful
tape keeps Γ₂ > 0 and never terminalizes. -/
theorem open_needs_priced_move (t : List Step) :
    ∀ c s, c ≠ .terminalized → s.gamma ≠ 0 →
      (∀ st ∈ t, st.letter ≠ .D ∧ st.letter ≠ .L) →
      ∀ c' s', run c s t = some (c', s') → c' ≠ .terminalized ∧ s'.gamma ≠ 0 := by
  induction t with
  | nil =>
    intro c s hc hs _ c' s' h
    simp [run] at h
    obtain ⟨rfl, rfl⟩ := h
    exact ⟨hc, hs⟩
  | cons st rest ih =>
    intro c s hc hs hpriced c' s' h
    simp only [run] at h
    split at h
    · rename_i hok
      simp only [Bool.and_eq_true] at hok
      have hnp := hpriced st (List.mem_cons_self ..)
      have hrest : ∀ x ∈ rest, x.letter ≠ .D ∧ x.letter ≠ .L :=
        fun x hx => hpriced x (List.mem_cons_of_mem _ hx)
      have key : nextCtrl c st.letter ≠ .terminalized ∧ st.after.gamma ≠ 0 := by
        have hlaw := hok.2
        have keep : ∀ l, l ≠ Letter.T → l ≠ Letter.M → nextCtrl c l ≠ .terminalized := by
          intro l hT hM
          cases c <;> cases l <;> simp_all [nextCtrl]
        cases hl : st.letter with
        | E =>
          rw [hl] at hlaw
          obtain ⟨-, hcls, -, -, -, -⟩ := law_E.1 hlaw
          exact absurd ((cls_exact_iff s).1 hcls).1 hs
        | R =>
          rw [hl] at hlaw
          obtain ⟨-, -, hg, -⟩ := law_R.1 hlaw
          exact ⟨keep _ (by simp) (by simp), by rw [hg]; exact hs⟩
        | C =>
          rw [hl] at hlaw
          obtain ⟨-, -, hg⟩ := law_C.1 hlaw
          exact ⟨keep _ (by simp) (by simp), by omega⟩
        | I =>
          rw [hl] at hlaw
          obtain ⟨hab, -⟩ := law_I.1 hlaw
          exact ⟨keep _ (by simp) (by simp), by rw [hab]; exact hs⟩
        | L => exact absurd hl hnp.2
        | D => exact absurd hl hnp.1
        | M =>
          rw [hl] at hlaw
          obtain ⟨hab, -⟩ := law_M.1 hlaw
          exact ⟨by simp [nextCtrl], by rw [hab]; exact hs⟩
        | T =>
          rw [hl] at hlaw
          obtain ⟨hab, hg, -⟩ := law_T.1 hlaw
          rw [hab] at hg
          exact absurd hg hs
      exact ih _ _ key.1 key.2 hrest c' s' h
    · simp at h

/-- The six-letter tape C·R·E·D·I·T ("CREDIT" is only a mnemonic). -/
def credit (s1 s2 s3 s4 s5 s6 : State) (w1 w2 w3 w4 w5 w6 : Witness) : List Step :=
  [⟨.C, s1, w1⟩, ⟨.R, s2, w2⟩, ⟨.E, s3, w3⟩, ⟨.D, s4, w4⟩, ⟨.I, s5, w5⟩, ⟨.T, s6, w6⟩]

theorem credit_lawful_iff (s0 s1 s2 s3 s4 s5 s6 : State) (w1 w2 w3 w4 w5 w6 : Witness) :
    Lawful .ongoing s0 (credit s1 s2 s3 s4 s5 s6 w1 w2 w3 w4 w5 w6) ↔
      stepLaw .C s0 s1 w1 = true ∧ stepLaw .R s1 s2 w2 = true ∧ stepLaw .E s2 s3 w3 = true ∧
      stepLaw .D s3 s4 w4 = true ∧ stepLaw .I s4 s5 w5 = true ∧ stepLaw .T s5 s6 w6 = true := by
  simp only [Lawful, credit, run, ctrlOk, nextCtrl, Bool.true_and]
  by_cases h1 : stepLaw .C s0 s1 w1 = true <;> simp only [h1] <;>
  by_cases h2 : stepLaw .R s1 s2 w2 = true <;> simp only [h2] <;>
  by_cases h3 : stepLaw .E s2 s3 w3 = true <;> simp only [h3] <;>
  by_cases h4 : stepLaw .D s3 s4 w4 = true <;> simp only [h4] <;>
  by_cases h5 : stepLaw .I s4 s5 w5 = true <;> simp only [h5] <;>
  by_cases h6 : stepLaw .T s5 s6 w6 = true <;> simp [h6] <;> simp_all

/-- CREDIT is lawful only from an exact start: C cannot lower Φ₁ or Γ₂ and R keeps them. -/
theorem credit_starts_exact (s0 s1 s2 s3 s4 s5 s6 : State) (w1 w2 w3 w4 w5 w6 : Witness)
    (h : Lawful .ongoing s0 (credit s1 s2 s3 s4 s5 s6 w1 w2 w3 w4 w5 w6)) :
    s0.phi = 0 ∧ s0.gamma = 0 := by
  obtain ⟨hC, hR, hE, -, -, -⟩ := (credit_lawful_iff ..).1 h
  obtain ⟨-, hp1, hg1⟩ := law_C.1 hC
  obtain ⟨-, hp2, hg2, -⟩ := law_R.1 hR
  obtain ⟨-, hcls, -, -, -, -⟩ := law_E.1 hE
  have := (cls_exact_iff s2).1 hcls
  exact ⟨by omega, by omega⟩

/-- Without a loss ledger at D, CREDIT is not lawful (Law 6). -/
theorem credit_needs_ledger (s0 s1 s2 s3 s4 s5 s6 : State) (w1 w2 w3 w4 w5 w6 : Witness)
    (hw : w4.ledger = false) :
    ¬ Lawful .ongoing s0 (credit s1 s2 s3 s4 s5 s6 w1 w2 w3 w4 w5 w6) := by
  intro h
  obtain ⟨-, -, -, hD, -, -⟩ := (credit_lawful_iff ..).1 h
  have := (law_D.1 hD).2
  rw [hw] at this
  exact Bool.false_ne_true this

/-- CREDIT is realizable: an exact defect on one carrier, repaired, then a booked descent. -/
theorem credit_realizable :
    Lawful .ongoing ⟨0, [], 0, 0, true⟩
      (credit ⟨1, [1, 2, -3], 0, 0, true⟩ ⟨1, [1, 2, -3], 0, 0, true⟩ ⟨1, [0, 0, 0], 0, 0, true⟩
        ⟨2, [0], 0, 0, true⟩ ⟨2, [0], 0, 0, true⟩ ⟨2, [0], 0, 0, true⟩
        ⟨false, false, false, none⟩ ⟨false, false, false, none⟩ ⟨false, false, false, none⟩
        ⟨false, true, false, none⟩ ⟨true, false, false, none⟩ ⟨false, false, false, none⟩) := by
  unfold Lawful
  decide

/-- The §23 driver never proposes T on an open or blind state. -/
theorem driver_never_seals_open (s : State) (h : Letter.T ∈ driverLetters s) :
    s.adequate = true ∧ s.gamma = 0 := by
  unfold driverLetters at h
  by_cases ha : s.adequate = true
  · simp only [ha, ↓reduceIte] at h
    cases hc : s.cls with
    | exact => exact ⟨ha, ((cls_exact_iff s).1 hc).1⟩
    | closed => exact ⟨ha, ((cls_closed_iff s).1 hc).1⟩
    | active => rw [hc] at h; simp at h
  · simp [ha] at h

/-- The driver proposes E only on an exact class. -/
theorem driver_repairs_only_exact (s : State) (h : Letter.E ∈ driverLetters s) :
    s.cls = .exact := by
  unfold driverLetters at h
  by_cases ha : s.adequate = true
  · simp only [ha, ↓reduceIte] at h
    cases hc : s.cls <;> rw [hc] at h <;> simp at h ⊢
  · simp [ha] at h

/-- The driver proposes Λ only from a closed residual or a blind detector (Law 4). -/
theorem driver_lift_trigger (s : State) (h : Letter.L ∈ driverLetters s) :
    s.cls = .closed ∨ s.adequate = false := by
  unfold driverLetters at h
  by_cases ha : s.adequate = true
  · simp only [ha, ↓reduceIte] at h
    cases hc : s.cls <;> rw [hc] at h <;> simp at h ⊢
  · simp at ha; exact Or.inr ha

end Ddc
