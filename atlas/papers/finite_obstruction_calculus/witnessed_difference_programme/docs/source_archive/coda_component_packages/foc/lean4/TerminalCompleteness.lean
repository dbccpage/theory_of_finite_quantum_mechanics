/-!
# Native terminal completeness, decidable kernel

A native obstruction element is either an exact repair, a closed non-exact
coherent residual, or a nonclosed defect.  Typed refusals live outside this
mathematical classifier and are emitted when the declared finite data needed to
run the classifier is absent.
-/

namespace FOC.TerminalCompleteness

variable {C0 C1 C2 : Type}

/-- Image membership predicate. -/
def InImage (f : C0 → C1) (x : C1) : Prop :=
  ∃ c0 : C0, f c0 = x

/-- Exact means membership in the declared repair image. -/
def Exact (d0 : C0 → C1) (x : C1) : Prop :=
  InImage d0 x

/-- CoherentResidual means closed but not exact. -/
def CoherentResidual (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2) (x : C1) : Prop :=
  ¬ Exact d0 x ∧ d1 x = z2

/-- NonclosedDefect means not exact and not closed. -/
def NonclosedDefect (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2) (x : C1) : Prop :=
  ¬ Exact d0 x ∧ d1 x ≠ z2

/-- The cochain condition makes exact repairs closed. -/
theorem exact_implies_closed
    (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2)
    (hcomplex : ∀ c0 : C0, d1 (d0 c0) = z2) (x : C1) :
    Exact d0 x → d1 x = z2 := by
  intro h
  rcases h with ⟨c0, rfl⟩
  exact hcomplex c0

/-- Decidable totality for the exact/coherent residual/nonclosed defect classifier. -/
theorem native_trichotomy_total_decidable
    (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2) (x : C1)
    [Decidable (Exact d0 x)] [Decidable (d1 x = z2)] :
    Exact d0 x ∨ CoherentResidual d0 d1 z2 x ∨ NonclosedDefect d0 d1 z2 x := by
  by_cases hx : Exact d0 x
  · exact Or.inl hx
  · by_cases hd : d1 x = z2
    · exact Or.inr (Or.inl ⟨hx, hd⟩)
    · exact Or.inr (Or.inr ⟨hx, hd⟩)

theorem exact_excludes_coherent_residual
    (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2) (x : C1) :
    Exact d0 x → CoherentResidual d0 d1 z2 x → False := by
  intro hx hs
  exact hs.1 hx

theorem coherent_residual_excludes_nonclosed_defect
    (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2) (x : C1) :
    CoherentResidual d0 d1 z2 x → NonclosedDefect d0 d1 z2 x → False := by
  intro hs ho
  exact ho.2 hs.2

theorem exact_excludes_nonclosed_defect
    (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2) (x : C1) :
    Exact d0 x → NonclosedDefect d0 d1 z2 x → False := by
  intro hx ho
  exact ho.1 hx

/-- Cochain coherence: exact and nonclosed are incompatible even if nonclosed is read
only through non-closure. -/
theorem exact_excludes_nonclosed
    (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2)
    (hcomplex : ∀ c0 : C0, d1 (d0 c0) = z2) (x : C1) :
    Exact d0 x → d1 x ≠ z2 → False := by
  intro hx hnonclosed
  exact hnonclosed (exact_implies_closed d0 d1 z2 hcomplex x hx)

/-- Three-tag terminal classification. -/
inductive Terminal where
  | exactRepair : Terminal
  | coherentResidual : Terminal
  | nonclosedDefect : Terminal
  deriving DecidableEq

theorem classify_unique (Tri : C1 → Terminal) (x : C1) :
    ∃ t : Terminal, Tri x = t ∧ ∀ y : Terminal, Tri x = y → y = t := by
  refine ⟨Tri x, rfl, ?_⟩
  intro y hy
  exact hy.symm

/-- A fixed classifier always lands in a unique terminal tag. -/
theorem terminal_tag_unique (Tri : C1 → Terminal) (x : C1) :
    ∃ t : Terminal,
      Tri x = t ∧ ∀ y : Terminal, Tri x = y → y = t :=
  classify_unique Tri x

#print axioms exact_implies_closed
#print axioms native_trichotomy_total_decidable
#print axioms exact_excludes_coherent_residual
#print axioms coherent_residual_excludes_nonclosed_defect
#print axioms exact_excludes_nonclosed_defect
#print axioms exact_excludes_nonclosed
#print axioms terminal_tag_unique

end FOC.TerminalCompleteness
