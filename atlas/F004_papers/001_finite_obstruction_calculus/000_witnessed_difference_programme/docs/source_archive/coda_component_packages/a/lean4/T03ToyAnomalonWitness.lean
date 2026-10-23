import D01D02Records
import T02ResidualNonCreation

/-!
# CODA-A T03: Constructible Toy Anomalon Witness & Taxonomy Firewall

Formalizes:
1. Constructible pure-residual toy witness `toy_anomalon_exists`.
   Constructed explicitly within the declared finite taxonomy via `anomalonToy`.
   This is a finite toy-model witness, not an unproved foundational axiom.
2. Derivation of the taxonomy firewall `firewall_from_toy_anomalon`.
   Transparent witness via `toy_anomalon_exists` under `#print axioms`.

AuthorityEffect: None.
-/

namespace CodaA

open CodaA

set_option linter.unusedVariables false

/-- **TOY ANOMALON EXISTENCE — constructible pure-residual witness.**
    In this declared finite taxonomy, a genuine pure-residual object exists:
    typed residue that is NOT authority-bearing, witnessed by `anomalonToy`. -/
theorem toy_anomalon_exists : ∃ X : GtlaObject, HasResidual X ∧ ¬ ObjAuth X :=
  ⟨anomalonToy, anomalonToy_hasResidual, anomalonToy_no_auth⟩

/-- **Taxonomy Authority Firewall — derived from the constructible `toy_anomalon_exists` witness.**
    No map sends every residual object to authority, the toy anomalon being an explicit counterexample.
    `#print axioms` shows standard Lean axioms only (`propext`, `Quot.sound`). -/
theorem firewall_from_toy_anomalon :
    ¬ (∀ X : GtlaObject, HasResidual X → ObjAuth X) := by
  intro α
  obtain ⟨X, hres, hno⟩ := toy_anomalon_exists
  exact hno (α X hres)

end CodaA
