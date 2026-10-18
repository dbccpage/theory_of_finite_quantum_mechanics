import «finite_obstruc»
/-!
LT-I — Finite quantum packet: decidable obstruction classification (M₂ skeleton).

Paper: `09_finite_quantum_packet_theorem_m2.md` (PO-D19a–e).

This lifts the general finite-obstruction trichotomy (`OmegaCore.QM`, TRI-001 /
LT-C) to a **decidable** classifier `triQ` for an *accepted* finite quantum
packet: a 2-truncated cochain triple `d0 : C0 → C1`, `d1 : C1 → C2`, `z2 : C2`
whose coboundary-membership `InImage d0` is decidable (a finite carrier supplies
this) and whose `C2` has decidable equality.

The classifier returns exactly one of the three diagnostic `Terminal` tags,
**never** `refusal` (a well-formed packet always classifies), each branch is
characterised exactly (`triQ_*_iff`), the landing is unique (`classify_unique`),
and under the cochain condition `d1 ∘ d0 = z2` an `exactRepair` classification is
*closed* (`triQ_exact_closed`, via `exact_implies_closed`) — so the exact and open
cases are coherent.

No Hilbert space, Born rule, or CPTP dynamics is derived; those enter as declared
finite packet fields. No authority is minted — GTFOC-Q is a diagnostic classifier.
Mathlib-free; builds on `OmegaCore` only.
-/

namespace QM

open OmegaCore.QM

variable {C0 C1 C2 : Type}

/-- Decidable obstruction classifier for an accepted finite quantum packet. -/
def triQ (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2)
    [∀ x, Decidable (InImage d0 x)] [DecidableEq C2] (x : C1) : Terminal :=
  if InImage d0 x then Terminal.exactRepair
  else if d1 x = z2 then Terminal.stabilizedSurvivor
  else Terminal.openObstruction

/-- `triQ` returns `exactRepair` exactly on coboundaries. -/
theorem triQ_exact_iff (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2)
    [∀ x, Decidable (InImage d0 x)] [DecidableEq C2] (x : C1) :
    triQ d0 d1 z2 x = Terminal.exactRepair ↔ InImage d0 x := by
  unfold triQ
  by_cases h : InImage d0 x
  · simp [h]
  · by_cases h2 : d1 x = z2 <;> simp [h, h2]

/-- `triQ` returns `stabilizedSurvivor` exactly on closed non-coboundaries. -/
theorem triQ_survivor_iff (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2)
    [∀ x, Decidable (InImage d0 x)] [DecidableEq C2] (x : C1) :
    triQ d0 d1 z2 x = Terminal.stabilizedSurvivor ↔ (¬ InImage d0 x ∧ d1 x = z2) := by
  unfold triQ
  by_cases h : InImage d0 x
  · simp [h]
  · by_cases h2 : d1 x = z2 <;> simp [h, h2]

/-- `triQ` returns `openObstruction` exactly on non-closed non-coboundaries. -/
theorem triQ_open_iff (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2)
    [∀ x, Decidable (InImage d0 x)] [DecidableEq C2] (x : C1) :
    triQ d0 d1 z2 x = Terminal.openObstruction ↔ (¬ InImage d0 x ∧ d1 x ≠ z2) := by
  unfold triQ
  by_cases h : InImage d0 x
  · simp [h]
  · by_cases h2 : d1 x = z2 <;> simp [h, h2]

/-- An accepted packet never classifies to `refusal`: `triQ` lands in one of the
three diagnostic tags for every `x`. -/
theorem triQ_never_refusal (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2)
    [∀ x, Decidable (InImage d0 x)] [DecidableEq C2] (x : C1) :
    triQ d0 d1 z2 x ≠ Terminal.refusal := by
  unfold triQ
  by_cases h : InImage d0 x
  · simp [h]
  · by_cases h2 : d1 x = z2 <;> simp [h, h2]

/-- Uniqueness: `triQ` lands in exactly one terminal (reuses `classify_unique`). -/
theorem triQ_unique (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2)
    [∀ x, Decidable (InImage d0 x)] [DecidableEq C2] (x : C1) :
    ∃ t : Terminal, triQ d0 d1 z2 x = t ∧ ∀ y : Terminal, triQ d0 d1 z2 x = y → y = t :=
  classify_unique (triQ d0 d1 z2) x

/-- Coherence: under the cochain condition `d1 ∘ d0 = z2`, an `exactRepair`
classification is closed (`d1 x = z2`); hence no `x` is simultaneously an exact
coboundary and an open obstruction. -/
theorem triQ_exact_closed (d0 : C0 → C1) (d1 : C1 → C2) (z2 : C2)
    [∀ x, Decidable (InImage d0 x)] [DecidableEq C2]
    (hcomplex : ∀ c0 : C0, d1 (d0 c0) = z2) (x : C1) :
    triQ d0 d1 z2 x = Terminal.exactRepair → d1 x = z2 := by
  intro hx
  exact exact_implies_closed d0 d1 z2 hcomplex x ((triQ_exact_iff d0 d1 z2 x).mp hx)

/-- Concrete seal: the identity coboundary over `Bool` — every element is an exact
coboundary, so `triQ` returns `exactRepair`. -/
instance instDecInImageIdBool : ∀ x : Bool, Decidable (InImage (id : Bool → Bool) x) :=
  fun x => isTrue ⟨x, rfl⟩

example (x : Bool) :
    triQ (id : Bool → Bool) (fun _ => false) false x = Terminal.exactRepair :=
  (triQ_exact_iff _ _ _ x).mpr ⟨x, rfl⟩

end QM

#print axioms QM.triQ_exact_iff
#print axioms QM.triQ_survivor_iff
#print axioms QM.triQ_open_iff
#print axioms QM.triQ_never_refusal
#print axioms QM.triQ_unique
#print axioms QM.triQ_exact_closed
