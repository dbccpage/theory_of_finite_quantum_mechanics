/- CH10 semantic adapter laws and a genuine field-erasure countermodel.
   AuthorityEffect: None. No archival vocabulary is invented by these proofs. -/
namespace WitnessedDifference.LegacyObserverAdapters

universe u v w

/-- A linear report descends through repairs exactly when it annihilates them.
    Additivity and identity laws are explicit; no numerical approximation. -/
theorem repair_invariance_iff_annihilates
    {V : Type u} {W : Type v} {A : Type w}
    (addV : V → V → V) (zeroV : V)
    (addW : W → W → W) (zeroW : W)
    (leftZeroV : ∀ x, addV zeroV x = x)
    (rightZeroW : ∀ x, addW x zeroW = x)
    (report : V → W) (repair : A → V)
    (reportZero : report zeroV = zeroW)
    (reportAdd : ∀ x y, report (addV x y) = addW (report x) (report y)) :
    (∀ x a, report (addV x (repair a)) = report x) ↔
      (∀ a, report (repair a) = zeroW) := by
  constructor
  · intro invariant a
    have h := invariant zeroV a
    rw [leftZeroV, reportZero] at h
    exact h
  · intro annihilates x a
    rw [reportAdd, annihilates, rightZeroW]

/-- Semantic retention data, separating actual update and report functions. -/
structure MemoryPacket (M : Type u) (I : Type v) (R : Type w) where
  update : M → I → M
  report : M → R

def staticMemory : MemoryPacket Bool Unit Unit :=
  ⟨fun m _ => m, fun _ => ()⟩

def togglingMemory : MemoryPacket Bool Unit Unit :=
  ⟨fun m _ => !m, fun _ => ()⟩

def eraseUpdates (p : MemoryPacket Bool Unit Unit) : Bool → Unit := p.report

theorem erased_packets_identical : eraseUpdates staticMemory = eraseUpdates togglingMemory := rfl

theorem actual_packets_distinct : staticMemory ≠ togglingMemory := by
  intro equal
  have impossible := congrArg (fun p : MemoryPacket Bool Unit Unit => p.update false ()) equal
  cases impossible

/-- No faithful recovery of the full semantic memory packet from erased
    reports exists. This is a quantified inverse claim, not a string example. -/
theorem no_recovery_after_update_erasure :
    ¬ ∃ recover : (Bool → Unit) → MemoryPacket Bool Unit Unit,
      ∀ p, recover (eraseUpdates p) = p := by
  intro h
  obtain ⟨recover, inverse⟩ := h
  have hs := inverse staticMemory
  have ht := inverse togglingMemory
  rw [← erased_packets_identical] at ht
  exact actual_packets_distinct (hs.symm.trans ht)

/-- A declared store/readout interface witnesses reaccess only through its
    explicit comparison relation; no equality or injectivity is manufactured. -/
theorem reaccess_uses_declared_comparison
    {P : Type u} {M : Type v} (store : P → M) (readout : M → P)
    (compare : P → P → Prop)
    (interface : ∀ p, compare (readout (store p)) p) :
    ∀ p, ∃ m, m = store p ∧ compare (readout m) p := by
  intro p
  exact ⟨store p, rfl, interface p⟩

#print axioms repair_invariance_iff_annihilates
#print axioms no_recovery_after_update_erasure
#print axioms reaccess_uses_declared_comparison

end WitnessedDifference.LegacyObserverAdapters
