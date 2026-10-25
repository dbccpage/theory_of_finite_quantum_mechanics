-- Campaign: OPS-OBSERVER-DECLARATION-REFUSAL. Not a default target.
-- Five-field classifier for one Bell label. No defect is read.


namespace CampaignOpsObserverDeclarationRefusal
inductive ObserverField where
  | kernel
  | admissibility
  | norm
  | terminal
  | layer
  deriving DecidableEq, Repr

inductive ObserverClass where
  | undeclared (field : ObserverField)
  | unsupported (field : ObserverField) (declared : String)
  | accepted
  deriving DecidableEq, Repr

def bellKernel : String :=
  "support presheaf over the maximal-context cover {0,2}|{0,3}|{1,2}|{1,3} with arities 2,2,2,2"

def acceptedAdmissibility : String := "noncontextual polytope conv(A)"

def acceptedNorm : String := "L1"

def acceptedTerminal : String :=
  "defect = 0 -> ExactRepair; defect > 0 and a support-level global section exists -> ClosedResidual; defect > 0 and none exists -> OpenObstruction"

def acceptedLayer : String := "WDP-CH10-D01 diagnostic"

def authorityNone : String := "None"

def acceptedText : ObserverField → String
  | .kernel => bellKernel
  | .admissibility => acceptedAdmissibility
  | .norm => acceptedNorm
  | .terminal => acceptedTerminal
  | .layer => acceptedLayer

structure ObserverDraft where
  kernel : Option String
  admissibility : Option String
  norm : Option String
  terminal : Option String
  layer : Option String

def ObserverDraft.get : ObserverDraft → ObserverField → Option String
  | d, .kernel => d.kernel
  | d, .admissibility => d.admissibility
  | d, .norm => d.norm
  | d, .terminal => d.terminal
  | d, .layer => d.layer

def setField (d : ObserverDraft) (field : ObserverField) (value : Option String) : ObserverDraft :=
  match field with
  | .kernel => { d with kernel := value }
  | .admissibility => { d with admissibility := value }
  | .norm => { d with norm := value }
  | .terminal => { d with terminal := value }
  | .layer => { d with layer := value }

def blankText : Option String → Bool
  | none => true
  | some s => s = "" || s = " "

def step (expected : String) (field : ObserverField) (value : Option String) (rest : ObserverClass) :
    ObserverClass :=
  match value with
  | none => .undeclared field
  | some s =>
    if s = "" || s = " " then .undeclared field
    else if s ≠ expected then .unsupported field s
    else rest

def classify (d : ObserverDraft) : ObserverClass :=
  step bellKernel .kernel d.kernel
    (step acceptedAdmissibility .admissibility d.admissibility
      (step acceptedNorm .norm d.norm
        (step acceptedTerminal .terminal d.terminal
          (step acceptedLayer .layer d.layer .accepted))))

theorem step_blank (expected : String) (field : ObserverField) (value : Option String) (rest : ObserverClass)
    (h : blankText value = true) : step expected field value rest = .undeclared field := by
  cases value with
  | none => rfl
  | some s =>
    simp [step, blankText] at h ⊢
    rcases h with h | h <;> simp [h]

theorem step_mismatch (expected : String) (field : ObserverField) (text : String) (rest : ObserverClass)
    (h0 : text ≠ "") (h1 : text ≠ " ") (hs : text ≠ expected) :
    step expected field (some text) rest = .unsupported field text := by
  simp [step, h0, h1, hs]

theorem step_pass (expected : String) (field : ObserverField) (rest : ObserverClass)
    (h0 : expected ≠ "") (h1 : expected ≠ " ") :
    step expected field (some expected) rest = rest := by
  simp [step, h0, h1]

section
set_option maxRecDepth 20000
set_option maxHeartbeats 0

theorem accepted_not_blank :
    bellKernel ≠ "" ∧ bellKernel ≠ " " ∧
      acceptedAdmissibility ≠ "" ∧ acceptedAdmissibility ≠ " " ∧
      acceptedNorm ≠ "" ∧ acceptedNorm ≠ " " ∧
      acceptedTerminal ≠ "" ∧ acceptedTerminal ≠ " " ∧
      acceptedLayer ≠ "" ∧ acceptedLayer ≠ " " := by
  decide

end

def authorityOf : ObserverClass → Option String
  | .accepted => some authorityNone
  | .undeclared _ => none
  | .unsupported _ _ => none

def acceptedDraft : ObserverDraft where
  kernel := some bellKernel
  admissibility := some acceptedAdmissibility
  norm := some acceptedNorm
  terminal := some acceptedTerminal
  layer := some acceptedLayer

theorem blank_on_accepted (field : ObserverField) (value : Option String) (h : blankText value = true) :
    classify (setField acceptedDraft field value) = .undeclared field := by
  have ⟨hk0, hk1, ha0, ha1, hn0, hn1, ht0, ht1, hl0, hl1⟩ := accepted_not_blank
  cases field with
  | kernel =>
    simp only [classify, setField, acceptedDraft]
    exact step_blank bellKernel .kernel value _ h
  | admissibility =>
    simp only [classify, setField, acceptedDraft]
    rw [step_pass bellKernel .kernel _ hk0 hk1]
    exact step_blank acceptedAdmissibility .admissibility value _ h
  | norm =>
    simp only [classify, setField, acceptedDraft]
    rw [step_pass bellKernel .kernel _ hk0 hk1]
    rw [step_pass acceptedAdmissibility .admissibility _ ha0 ha1]
    exact step_blank acceptedNorm .norm value _ h
  | terminal =>
    simp only [classify, setField, acceptedDraft]
    rw [step_pass bellKernel .kernel _ hk0 hk1]
    rw [step_pass acceptedAdmissibility .admissibility _ ha0 ha1]
    rw [step_pass acceptedNorm .norm _ hn0 hn1]
    exact step_blank acceptedTerminal .terminal value _ h
  | layer =>
    simp only [classify, setField, acceptedDraft]
    rw [step_pass bellKernel .kernel _ hk0 hk1]
    rw [step_pass acceptedAdmissibility .admissibility _ ha0 ha1]
    rw [step_pass acceptedNorm .norm _ hn0 hn1]
    rw [step_pass acceptedTerminal .terminal _ ht0 ht1]
    exact step_blank acceptedLayer .layer value _ h

theorem mismatch_on_accepted (field : ObserverField) (text : String)
    (h0 : text ≠ "") (h1 : text ≠ " ") (hs : text ≠ acceptedText field) :
    classify (setField acceptedDraft field (some text)) = .unsupported field text := by
  have ⟨hk0, hk1, ha0, ha1, hn0, hn1, ht0, ht1, hl0, hl1⟩ := accepted_not_blank
  cases field with
  | kernel =>
    simp only [acceptedText] at hs
    simp only [classify, setField, acceptedDraft]
    exact step_mismatch bellKernel .kernel text _ h0 h1 hs
  | admissibility =>
    simp only [acceptedText] at hs
    simp only [classify, setField, acceptedDraft]
    rw [step_pass bellKernel .kernel _ hk0 hk1]
    exact step_mismatch acceptedAdmissibility .admissibility text _ h0 h1 hs
  | norm =>
    simp only [acceptedText] at hs
    simp only [classify, setField, acceptedDraft]
    rw [step_pass bellKernel .kernel _ hk0 hk1]
    rw [step_pass acceptedAdmissibility .admissibility _ ha0 ha1]
    exact step_mismatch acceptedNorm .norm text _ h0 h1 hs
  | terminal =>
    simp only [acceptedText] at hs
    simp only [classify, setField, acceptedDraft]
    rw [step_pass bellKernel .kernel _ hk0 hk1]
    rw [step_pass acceptedAdmissibility .admissibility _ ha0 ha1]
    rw [step_pass acceptedNorm .norm _ hn0 hn1]
    exact step_mismatch acceptedTerminal .terminal text _ h0 h1 hs
  | layer =>
    simp only [acceptedText] at hs
    simp only [classify, setField, acceptedDraft]
    rw [step_pass bellKernel .kernel _ hk0 hk1]
    rw [step_pass acceptedAdmissibility .admissibility _ ha0 ha1]
    rw [step_pass acceptedNorm .norm _ hn0 hn1]
    rw [step_pass acceptedTerminal .terminal _ ht0 ht1]
    exact step_mismatch acceptedLayer .layer text _ h0 h1 hs

theorem accepted_draft_class : classify acceptedDraft = .accepted := by
  have ⟨hk0, hk1, ha0, ha1, hn0, hn1, ht0, ht1, hl0, hl1⟩ := accepted_not_blank
  simp only [classify, acceptedDraft]
  rw [step_pass bellKernel .kernel _ hk0 hk1]
  rw [step_pass acceptedAdmissibility .admissibility _ ha0 ha1]
  rw [step_pass acceptedNorm .norm _ hn0 hn1]
  rw [step_pass acceptedTerminal .terminal _ ht0 ht1]
  rw [step_pass acceptedLayer .layer _ hl0 hl1]

theorem accepted_authority : authorityOf (classify acceptedDraft) = some authorityNone := by
  simp [accepted_draft_class, authorityOf]

#print axioms blank_on_accepted
#print axioms mismatch_on_accepted
#print axioms accepted_draft_class
#print axioms accepted_authority

end CampaignOpsObserverDeclarationRefusal
