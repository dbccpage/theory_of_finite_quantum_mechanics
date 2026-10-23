import D01D02Records

/-!
# CODA-A T02: Pure Residual Non-Creation Firewall (GTLA-03 / GTLA-14 Toy Level)

Formalizes:
1. GTLA-03 / GTLA-14: Residual terminals cannot be authority terminals.
2. Emptiness of authority extractors: `AuthExtractor → False`.
3. Authority only via finite descent evidence (`authority_only_via_evidence`).
4. Toy level firewall: `anomalon_toy_exists` and `firewall_toy` (axiom-free in toy).

AuthorityEffect: None.
-/

namespace CodaA

open CodaA

set_option linter.unusedVariables false

/-- A dependent family attempting to extract authority from residual terminals. -/
def AuthExtractor : Prop := ∀ r : ResidualTerminal, IsAuth (residualTerminal r)

/-- Emptiness of authority extractor at any declared residual terminal. -/
theorem nat_residual_auth_empty (r0 : ResidualTerminal) : AuthExtractor → False := by
  intro α
  exact residual_not_auth r0 (α r0)

/-- Since the residual layer is concretely inhabited, no authority extractor exists. -/
theorem authExtractor_empty : AuthExtractor → False := by
  intro α
  exact residual_not_auth .closedResidual (α .closedResidual)

/-- Authority is only reachable via finite descent evidence in the auth summand. -/
theorem authority_only_via_evidence (t : Terminal) (h : IsAuth t) :
    ∃ e : AuthEvidence, t = Terminal.auth e := by
  cases t with
  | auth e => exact ⟨e, rfl⟩
  | residual r => contradiction

/-- Pure-residual existence in the toy type (axiom-free). -/
theorem anomalon_toy_exists : ∃ X : GtlaObject, HasResidual X ∧ ¬ ObjAuth X :=
  ⟨anomalonToy, anomalonToy_hasResidual, anomalonToy_no_auth⟩

/-- Toy firewall — axiom-free: no map sends every residual object to authority. -/
theorem firewall_toy : ¬ (∀ X : GtlaObject, HasResidual X → ObjAuth X) := by
  intro α
  exact anomalonToy_no_auth (α anomalonToy anomalonToy_hasResidual)

end CodaA
