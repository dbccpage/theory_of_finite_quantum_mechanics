/-!
Track-A boundary firewalls (papers 22–25) — Deutsch / Everett / Wolfram.

Three scoped typed non-implications, each a special case of the general firewall
`OmegaCosmology.Primitives.AuthorityNonPromotion` (LT-A): *formal coherence does not by itself
construct world/physical authority*. Each is modelled (as in LT-G) by a situation
carrying the formal property and, **independently**, the authority-bearing evidence;
the formal property never forces the evidence.

* **Deutsch (POSS-TASK, paper 23):** a formally `PossibleTask` does not construct a
  `QCRealizationPacket` (the repair-capacity evidence is separate).
* **Everett (EVERETT, paper 24):** a `BranchRepresentation` does not construct an
  `OntologyTerminal` (a packet-distinguishable ontology claim is separate).
* **Wolfram (WOLFRAM, paper 25):** `RuleGeneratesPatterns` does not construct
  `WorldAuthority` (finite-descent terminalization is separate).

Scope guard: these say *"X does not by itself terminalize authority"*, **never**
"Deutsch/Everett/Wolfram is refuted". No authority minted. Mathlib-free.
-/

namespace QM

/-! ## Deutsch boundary -/

structure QCSituation where
  possible : Bool
  capacity : Bool
deriving DecidableEq

def PossibleTask (s : QCSituation) : Prop := s.possible = true
def QCRealizationPacket (s : QCSituation) : Prop := s.capacity = true

theorem possible_task_not_packet : ∃ s, PossibleTask s ∧ ¬ QCRealizationPacket s := by
  refine ⟨⟨true, false⟩, rfl, ?_⟩
  show ¬ (false = true); decide

theorem not_possible_implies_packet : ¬ (∀ s, PossibleTask s → QCRealizationPacket s) := by
  intro h; obtain ⟨s, hp, hn⟩ := possible_task_not_packet; exact hn (h s hp)

/-! ## Everett boundary -/

structure EverettSituation where
  branchRepr : Bool
  ontologyTerminal : Bool
deriving DecidableEq

def BranchRepresentation (s : EverettSituation) : Prop := s.branchRepr = true
def OntologyTerminal (s : EverettSituation) : Prop := s.ontologyTerminal = true

theorem branch_not_ontology : ∃ s, BranchRepresentation s ∧ ¬ OntologyTerminal s := by
  refine ⟨⟨true, false⟩, rfl, ?_⟩
  show ¬ (false = true); decide

theorem not_branch_implies_ontology : ¬ (∀ s, BranchRepresentation s → OntologyTerminal s) := by
  intro h; obtain ⟨s, hb, hn⟩ := branch_not_ontology; exact hn (h s hb)

/-! ## Wolfram boundary -/

structure WolframSituation where
  generates : Bool
  worldAuthority : Bool
deriving DecidableEq

def RuleGeneratesPatterns (s : WolframSituation) : Prop := s.generates = true
def WorldAuthority (s : WolframSituation) : Prop := s.worldAuthority = true

theorem rule_not_world_authority : ∃ s, RuleGeneratesPatterns s ∧ ¬ WorldAuthority s := by
  refine ⟨⟨true, false⟩, rfl, ?_⟩
  show ¬ (false = true); decide

theorem not_rule_implies_world_authority :
    ¬ (∀ s, RuleGeneratesPatterns s → WorldAuthority s) := by
  intro h; obtain ⟨s, hg, hn⟩ := rule_not_world_authority; exact hn (h s hg)

/-! ## General authority firewall — the §1 non-implication, mechanized honestly

The bare `StructureDerived ⇏ IsAuth` firewall, proved the genuine way: two
INDEPENDENT decidable atoms plus a witness situation that IS structure-derived
but is NOT authority. This is a real countermodel, exactly like the three
per-program boundaries above — and unlike the vacuously-gated lemma in
`OmegaCosmology/Primitives/AuthorityNonPromotion.lean`
(`no_formal_to_authority_when_no_terminalizer`), which gates on the never-true
hypothesis `TerminalizerEvidence → False` and therefore proves nothing about the
actual model. Here `structure_not_auth` exhibits the gap directly.

Scope: this mechanizes the bare non-implication (the boxed `StructureDerived ⇏
IsAuth` claim). The STRONGER claim "authority factors only through the Π♯
terminalizer (no constructor that skips the packet)" is NOT mechanized here and
stays prose/open — do not tag it MECHANIZED. -/

structure AuthSituation where
  structureDerived : Bool
  isAuth : Bool
deriving DecidableEq

def StructureDerived (s : AuthSituation) : Prop := s.structureDerived = true
def IsAuth (s : AuthSituation) : Prop := s.isAuth = true

/-- A situation that IS structure-derived but is NOT authority: structure
    derivation does not, by itself, mint authority. -/
theorem structure_not_auth : ∃ s, StructureDerived s ∧ ¬ IsAuth s := by
  refine ⟨⟨true, false⟩, rfl, ?_⟩
  show ¬ (false = true); decide

/-- **The firewall, mechanized:** it is NOT the case that every structure-derived
    situation is authority — `StructureDerived ⇏ IsAuth`. Genuine (witness-backed),
    not vacuously gated. -/
theorem not_structureDerived_implies_isAuth :
    ¬ (∀ s, StructureDerived s → IsAuth s) := by
  intro h
  obtain ⟨s, hsd, hna⟩ := structure_not_auth
  exact hna (h s hsd)

end QM

#print axioms QM.not_possible_implies_packet
#print axioms QM.not_branch_implies_ontology
#print axioms QM.not_rule_implies_world_authority
#print axioms QM.structure_not_auth
#print axioms QM.not_structureDerived_implies_isAuth
