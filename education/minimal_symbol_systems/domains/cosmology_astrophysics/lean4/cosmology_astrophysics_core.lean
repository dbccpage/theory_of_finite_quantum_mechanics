/-!
  Cosmology, Gravitation & Astrophysics — Lean 4 Formal Core
  AuthorityEffect: None
  Gate: Lean 4 (version 4.34.0)
-/

namespace CosmologyDomainSetting

/-- Base setting for cosmology_astrophysics: Carrier, asserted relation, endpoints, and irreflexivity. -/
structure Setting where
  X : Type
  r : X → X → Prop
  a : X
  b : X
  irrefl : ∀ x, ¬ r x x

/-- The fundamental theorem of distinctness: irreflexive witnessed difference implies endpoints are distinct. -/
theorem irrefl_distinct {X : Type} {r : X → X → Prop} (irrefl : ∀ x, ¬ r x x) {a b : X} (h : r a b) : a ≠ b :=
  fun heq => irrefl a (heq ▸ h)

/-- In this domain setting, designated endpoints S.a and S.b are formally distinct under the witnessed relation. -/
theorem setting_endpoints_distinct (S : Setting) (h : S.r S.a S.b) : S.a ≠ S.b :=
  irrefl_distinct S.irrefl h

/-- Cotransitivity: an asserted difference splits against every third candidate. -/
def Cotrans {X : Type} (r : X → X → Prop) : Prop :=
  ∀ x y, r x y → ∀ z, r x z ∨ r z y

/-- A discrete causal set: irreflexive, transitive, and acyclic. -/
structure CausalSet (X : Type) where
  prec : X → X → Prop
  irrefl : ∀ x, ¬ prec x x
  trans : ∀ x y z, prec x y → prec y z → prec x z
  acyclic : ∀ x y, prec x y → ¬ prec y x

/-- Theorem: In any causal set, an asserted causal relation implies distinct endpoints. -/
theorem causal_endpoints_distinct {X : Type} (C : CausalSet X) {x y : X} (h : C.prec x y) : x ≠ y :=
  fun heq => C.irrefl x (heq ▸ h)

/-- Alexandrov causal interval definition: I(x, y) = {z | x prec z ∧ z prec y}. -/
def in_alexandrov_interval {X : Type} (C : CausalSet X) (x y z : X) : Prop :=
  C.prec x z ∧ C.prec z y

-- Physical recovery obligations are open metadata, not theorems of this finite setting.

end CosmologyDomainSetting
