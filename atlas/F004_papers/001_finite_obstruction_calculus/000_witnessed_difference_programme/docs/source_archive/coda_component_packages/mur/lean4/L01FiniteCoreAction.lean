/-!
Lean 4 proof kernel for GTMUR-L01 and PL-995-1.

AuthorityEffect: None.

GTMUR-L01 says that a representation map induces a finite-core action on the
live accepted core exactly when target descent is total on accepted
representatives and invariant on accepted descent fibers.

PL-995-1 asks for the next functoriality step: once finite-core actions are
induced in this L01 sense, the composite action is not extra declared data. It
is the pointwise composite of the induced actions on live cores.
-/

namespace CODA_MUR

universe uA uB uC vA vB vC

/-- The live finite core is the image of accepted descent. -/
abbrev LiveCore {Rep : Type uA} {Core : Type vA}
    (D : Rep -> Option Core) : Type vA :=
  { c : Core // ∃ x : Rep, D x = some c }

/-- Target packet totality on accepted representatives. -/
def TargetPacketTotal
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    (D_A : RepA -> Option CoreA) (D_B : RepB -> Option CoreB)
    (F : RepA -> RepB) : Prop :=
  ∀ x cA, D_A x = some cA -> ∃ cB, D_B (F x) = some cB

/-- Descent-fiber invariance for accepted representatives. -/
def DescentFiberInvariant
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    (D_A : RepA -> Option CoreA) (D_B : RepB -> Option CoreB)
    (F : RepA -> RepB) : Prop :=
  ∀ x x' cA,
    D_A x = some cA ->
    D_A x' = some cA ->
    D_B (F x) = D_B (F x')

/-- A finite-core action induced by a representation map. -/
structure FiniteCoreAction
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    (D_A : RepA -> Option CoreA) (D_B : RepB -> Option CoreB)
    (F : RepA -> RepB) where
  act : LiveCore D_A -> CoreB
  spec :
    ∀ x cA, (hx : D_A x = some cA) ->
      D_B (F x) = some (act ⟨cA, ⟨x, hx⟩⟩)

theorem FiniteCoreAction.target_total
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB}
    (A : FiniteCoreAction D_A D_B F) :
    TargetPacketTotal D_A D_B F := by
  intro x cA hx
  exact ⟨A.act ⟨cA, ⟨x, hx⟩⟩, A.spec x cA hx⟩

theorem FiniteCoreAction.fiber_invariant
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB}
    (A : FiniteCoreAction D_A D_B F) :
    DescentFiberInvariant D_A D_B F := by
  intro x x' cA hx hx'
  let c₁ : LiveCore D_A := ⟨cA, ⟨x, hx⟩⟩
  let c₂ : LiveCore D_A := ⟨cA, ⟨x', hx'⟩⟩
  have hact : A.act c₁ = A.act c₂ := by
    exact congrArg A.act (Subtype.ext rfl)
  calc
    D_B (F x) = some (A.act c₁) := A.spec x cA hx
    _ = some (A.act c₂) := congrArg some hact
    _ = D_B (F x') := (A.spec x' cA hx').symm

noncomputable def chosenLiveRep
    {Rep : Type uA} {Core : Type vA}
    {D : Rep -> Option Core} (c : LiveCore D) : Rep :=
  Classical.choose c.property

theorem chosenLiveRep_spec
    {Rep : Type uA} {Core : Type vA}
    {D : Rep -> Option Core} (c : LiveCore D) :
    D (chosenLiveRep c) = some c.val :=
  Classical.choose_spec c.property

noncomputable def inducedCoreValue
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB}
    (hTot : TargetPacketTotal D_A D_B F)
    (c : LiveCore D_A) : CoreB :=
  Classical.choose (hTot (chosenLiveRep c) c.val (chosenLiveRep_spec c))

theorem inducedCoreValue_spec
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB}
    (hTot : TargetPacketTotal D_A D_B F)
    (c : LiveCore D_A) :
    D_B (F (chosenLiveRep c)) = some (inducedCoreValue hTot c) :=
  Classical.choose_spec (hTot (chosenLiveRep c) c.val (chosenLiveRep_spec c))

/-- Construct the induced finite-core action from totality and fiber invariance. -/
noncomputable def inducedFiniteCoreAction
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB}
    (hTot : TargetPacketTotal D_A D_B F)
    (hInv : DescentFiberInvariant D_A D_B F) :
    FiniteCoreAction D_A D_B F where
  act := inducedCoreValue hTot
  spec := by
    intro x cA hx
    let c : LiveCore D_A := ⟨cA, ⟨x, hx⟩⟩
    have hChosen :
        D_B (F (chosenLiveRep c)) = some (inducedCoreValue hTot c) :=
      inducedCoreValue_spec hTot c
    have hSame : D_B (F (chosenLiveRep c)) = D_B (F x) :=
      hInv (chosenLiveRep c) x cA (chosenLiveRep_spec c) hx
    change D_B (F x) = some (inducedCoreValue hTot c)
    exact hSame.symm.trans hChosen

/-- GTMUR-L01: finite-core actions exist exactly under totality and fiber invariance. -/
theorem finiteCoreAction_exists_iff_total_and_fiberInvariant
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB} :
    Nonempty (FiniteCoreAction D_A D_B F) ↔
      TargetPacketTotal D_A D_B F ∧ DescentFiberInvariant D_A D_B F := by
  constructor
  · intro h
    rcases h with ⟨A⟩
    exact ⟨A.target_total, A.fiber_invariant⟩
  · intro h
    exact ⟨inducedFiniteCoreAction h.1 h.2⟩

/-- Induced actions are unique on the live core. -/
theorem finiteCoreAction_unique
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB}
    (A B : FiniteCoreAction D_A D_B F) :
    A.act = B.act := by
  funext c
  rcases c.property with ⟨x, hx⟩
  have hA := A.spec x c.val hx
  have hB := B.spec x c.val hx
  have hSome : some (A.act c) = some (B.act c) := hA.symm.trans hB
  exact Option.some.inj hSome

/-- A target refusal on an accepted representative blocks any induced action. -/
theorem finiteCoreAction_refusal_blocks
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB}
    (x : RepA) (cA : CoreA)
    (hx : D_A x = some cA)
    (hRefuse : D_B (F x) = none) :
    ¬ Nonempty (FiniteCoreAction D_A D_B F) := by
  intro h
  rcases h with ⟨A⟩
  have hSpec := A.spec x cA hx
  rw [hRefuse] at hSpec
  cases hSpec

/-- A descent-fiber mismatch blocks any induced action. -/
theorem finiteCoreAction_fiber_mismatch_blocks
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB}
    (x x' : RepA) (cA : CoreA)
    (hx : D_A x = some cA)
    (hx' : D_A x' = some cA)
    (hMismatch : D_B (F x) ≠ D_B (F x')) :
    ¬ Nonempty (FiniteCoreAction D_A D_B F) := by
  intro h
  rcases h with ⟨A⟩
  exact hMismatch (A.fiber_invariant x x' cA hx hx')

/-- An induced finite-core action maps live cores to live cores. -/
def FiniteCoreAction.liveMap
    {RepA : Type uA} {RepB : Type uB}
    {CoreA : Type vA} {CoreB : Type vB}
    {D_A : RepA -> Option CoreA} {D_B : RepB -> Option CoreB}
    {F : RepA -> RepB}
    (A : FiniteCoreAction D_A D_B F)
    (c : LiveCore D_A) : LiveCore D_B :=
  ⟨A.act c, by
    rcases c.property with ⟨x, hx⟩
    exact ⟨F x, A.spec x c.val hx⟩⟩

/-- PL-995-1: induced finite-core actions compose without extra declared data. -/
def FiniteCoreAction.comp
    {RepA : Type uA} {RepB : Type uB} {RepC : Type uC}
    {CoreA : Type vA} {CoreB : Type vB} {CoreC : Type vC}
    {D_A : RepA -> Option CoreA}
    {D_B : RepB -> Option CoreB}
    {D_C : RepC -> Option CoreC}
    {F : RepA -> RepB} {G : RepB -> RepC}
    (GAction : FiniteCoreAction D_B D_C G)
    (FAction : FiniteCoreAction D_A D_B F) :
    FiniteCoreAction D_A D_C (fun x => G (F x)) where
  act := fun c => GAction.act (FAction.liveMap c)
  spec := by
    intro x cA hx
    let c : LiveCore D_A := ⟨cA, ⟨x, hx⟩⟩
    have hF : D_B (F x) = some (FAction.act c) :=
      FAction.spec x cA hx
    have hG :
        D_C (G (F x)) =
          some (GAction.act ⟨FAction.act c, ⟨F x, hF⟩⟩) :=
      GAction.spec (F x) (FAction.act c) hF
    have hLive :
        (⟨FAction.act c, ⟨F x, hF⟩⟩ : LiveCore D_B) =
          FAction.liveMap c := by
      exact Subtype.ext rfl
    change D_C (G (F x)) = some (GAction.act (FAction.liveMap c))
    exact hG.trans (congrArg some (congrArg GAction.act hLive))

/-- Any separately supplied composite action agrees with the derived composite. -/
theorem finiteCoreAction_functoriality
    {RepA : Type uA} {RepB : Type uB} {RepC : Type uC}
    {CoreA : Type vA} {CoreB : Type vB} {CoreC : Type vC}
    {D_A : RepA -> Option CoreA}
    {D_B : RepB -> Option CoreB}
    {D_C : RepC -> Option CoreC}
    {F : RepA -> RepB} {G : RepB -> RepC}
    (FAction : FiniteCoreAction D_A D_B F)
    (GAction : FiniteCoreAction D_B D_C G)
    (GFAction : FiniteCoreAction D_A D_C (fun x => G (F x))) :
    GFAction.act = (GAction.comp FAction).act :=
  finiteCoreAction_unique GFAction (GAction.comp FAction)

end CODA_MUR

#print axioms CODA_MUR.finiteCoreAction_exists_iff_total_and_fiberInvariant
#print axioms CODA_MUR.finiteCoreAction_unique
#print axioms CODA_MUR.finiteCoreAction_refusal_blocks
#print axioms CODA_MUR.finiteCoreAction_fiber_mismatch_blocks
#print axioms CODA_MUR.finiteCoreAction_functoriality
