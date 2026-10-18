/-!
# LT-A — typed authority non-implications + Π♯ factorization (cycle 003, QM_010 / PL-QM014-1)

`PossibilityBoundaries.lean` mechanizes the bare firewall `StructureDerived ⊬ IsAuth` and the three
program boundaries (Deutsch / Everett / Wolfram), and explicitly leaves the further LT-A targets
open. This file closes them:

* `ValidTransport ⊬ Authority` — a valid transport does not by itself mint authority;
* `LocalReplay ⊬ SealedAuthority` — a local replay does not mint sealed authority;
* `ScopedTerminal ≠ ExactAuthority` — a scoped-empirical terminal is not an exact-authority terminal;
* **factorization** — authority arises only through the sealed Π♯ terminalizer.

Each non-implication is a genuine countermodel: two INDEPENDENT decidable atoms and a witness that
carries the formal property but NOT the authority (the same honest pattern as
`PossibilityBoundaries.lean`, not a vacuously-gated lemma). Mathlib-free; `decide` / explicit.

No authority minted (LGGR). The factorization is a *typed-firewall* structural fact — the authority
type is sealed by design (its sole constructor is the Π♯ terminalizer) — tagged accordingly, not a
deep theorem.
-/

namespace QM.LTA

/-! ## ValidTransport ⊬ Authority -/

structure TransportSituation where
  validTransport : Bool
  authority : Bool
deriving DecidableEq

def ValidTransport (s : TransportSituation) : Prop := s.validTransport = true
def Authority (s : TransportSituation) : Prop := s.authority = true

theorem validTransport_not_authority : ∃ s, ValidTransport s ∧ ¬ Authority s := by
  refine ⟨⟨true, false⟩, rfl, ?_⟩; show ¬ (false = true); decide

theorem not_validTransport_implies_authority :
    ¬ (∀ s, ValidTransport s → Authority s) := by
  intro h; obtain ⟨s, hv, hn⟩ := validTransport_not_authority; exact hn (h s hv)

/-! ## LocalReplay ⊬ SealedAuthority -/

structure ReplaySituation where
  localReplay : Bool
  sealedAuthority : Bool
deriving DecidableEq

def LocalReplay (s : ReplaySituation) : Prop := s.localReplay = true
def SealedAuthority (s : ReplaySituation) : Prop := s.sealedAuthority = true

theorem localReplay_not_sealed : ∃ s, LocalReplay s ∧ ¬ SealedAuthority s := by
  refine ⟨⟨true, false⟩, rfl, ?_⟩; show ¬ (false = true); decide

theorem not_localReplay_implies_sealed :
    ¬ (∀ s, LocalReplay s → SealedAuthority s) := by
  intro h; obtain ⟨s, hr, hn⟩ := localReplay_not_sealed; exact hn (h s hr)

/-! ## ScopedTerminal ≠ ExactAuthority -/

structure TerminalSituation where
  scopedTerminal : Bool
  exactAuthority : Bool
deriving DecidableEq

def ScopedTerminal (s : TerminalSituation) : Prop := s.scopedTerminal = true
def ExactAuthority (s : TerminalSituation) : Prop := s.exactAuthority = true

theorem scopedTerminal_not_exact : ∃ s, ScopedTerminal s ∧ ¬ ExactAuthority s := by
  refine ⟨⟨true, false⟩, rfl, ?_⟩; show ¬ (false = true); decide

theorem not_scopedTerminal_implies_exact :
    ¬ (∀ s, ScopedTerminal s → ExactAuthority s) := by
  intro h; obtain ⟨s, ht, hn⟩ := scopedTerminal_not_exact; exact hn (h s ht)

/-! ## Authority factors only through the sealed Π♯ terminalizer

The authority terminal is *sealed*: its sole constructor is the Π♯ terminalizer. Hence every
authority terminal factors through Π♯ evidence — no transport / replay / scope constructor skips it.
A typed-firewall structural fact (true by the type's design), not a deep theorem. -/

/-- Abstract Π♯ (sealed-terminalizer) evidence. -/
structure PiSharpEvidence where
  certified : Bool

/-- The authority terminal, sealed: the only producer is the Π♯ terminalizer. -/
inductive AuthorityTerminal where
  | sealed : PiSharpEvidence → AuthorityTerminal

/-- **Factorization.** Every authority terminal arises from Π♯ evidence; authority does not arise
from any constructor that skips the sealed terminalizer. -/
theorem authority_only_via_piSharp (t : AuthorityTerminal) :
    ∃ e : PiSharpEvidence, t = .sealed e := by
  cases t with | sealed e => exact ⟨e, rfl⟩

end QM.LTA

#print axioms QM.LTA.not_validTransport_implies_authority
#print axioms QM.LTA.not_localReplay_implies_sealed
#print axioms QM.LTA.not_scopedTerminal_implies_exact
#print axioms QM.LTA.authority_only_via_piSharp
