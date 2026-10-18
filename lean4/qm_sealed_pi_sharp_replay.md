import «authority_non_implications_lta»

/-!
# Operational Π♯ seal — the GTFDA-Q authority gate (cycle 004, QM_012/QM_016 O021 / PL-QM005-2)

Cycle 003 (`QM.LTA`) showed authority factors *structurally* through the sealed Π♯ terminalizer
(`authority_only_via_piSharp`), but left the seal abstract. This cycle gives it **operational
content**: the Π♯ evidence is sealed iff its replay checks, and authority is conferred **exactly** by
a valid sealed Π♯ replay — not by a proposer, a score, or an unverified replay.

This is the minimal mechanization of the O021 / `PL-QM005-2` "sealed external Π♯ replay" obligation:
the gate is non-vacuous (a passing replay confers authority) and firewalled (everything else does not).

No authority minted (LGGR) — this is a *model* of the gate, not a physical sealing. Mathlib-free;
`decide` / explicit. Builds on cycle-003 `QM.LTA`.
-/

namespace QM.LTA

/-- The Π♯ seal is valid iff the sealed replay reproduced the certified output. -/
def Sealed (e : PiSharpEvidence) : Prop := e.certified = true

/-- An authority terminal **confers authority** iff its Π♯ evidence is sealed (the replay checked).
This is the operational reading of `AuthorityTerminal`. -/
def ConfersAuthority : AuthorityTerminal → Prop
  | .sealed e => Sealed e

/-- **The GTFDA-Q authority gate.** Authority is conferred *exactly* by a valid sealed Π♯ replay:
`ConfersAuthority t ↔ ∃ e, t = .sealed e ∧ Sealed e`. -/
theorem confersAuthority_iff_sealed_replay (t : AuthorityTerminal) :
    ConfersAuthority t ↔ ∃ e, t = .sealed e ∧ Sealed e := by
  cases t with
  | sealed e =>
    constructor
    · intro h; exact ⟨e, rfl, h⟩
    · rintro ⟨e', he, hs⟩; rw [he]; exact hs

/-- **Non-vacuous.** A passing sealed replay does confer authority — the gate is reachable. -/
theorem sealed_true_confers : ConfersAuthority (.sealed ⟨true⟩) := rfl

/-- **Unsealed mints nothing.** An unverified replay confers no authority. -/
theorem unsealed_confers_nothing : ¬ ConfersAuthority (.sealed ⟨false⟩) := by
  show ¬ (false = true); decide

/-! ## Proposers and scores do not seal -/

/-- A situation pairing "emits a candidate" (proposer / LLM / high score) with "the replay checked". -/
structure ProposerSituation where
  proposes : Bool
  sealed   : Bool
deriving DecidableEq

def Proposes (s : ProposerSituation) : Prop := s.proposes = true
def SealOf (s : ProposerSituation) : Prop := s.sealed = true

/-- **Proposer firewall (operational).** Emitting a candidate — a proposer, an LLM, or a high score —
does not seal the replay: `Proposes ⊬ SealOf`. The two are independent. -/
theorem proposes_not_seal : ¬ (∀ s, Proposes s → SealOf s) := by
  intro h; exact absurd (h ⟨true, false⟩ rfl) (by show ¬ (false = true); decide)

end QM.LTA

#print axioms QM.LTA.confersAuthority_iff_sealed_replay
#print axioms QM.LTA.sealed_true_confers
#print axioms QM.LTA.unsealed_confers_nothing
#print axioms QM.LTA.proposes_not_seal
