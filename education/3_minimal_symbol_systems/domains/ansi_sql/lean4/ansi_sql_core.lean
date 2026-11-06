/-!
  Relational Algebra & Database Theory — Lean 4 Formal Core
  AuthorityEffect: None
  Compiler results are recorded separately; this header is not a verification receipt.
-/

namespace SqlDomainSetting

/-- Base setting for ansi_sql: Carrier, asserted relation, endpoints, and irreflexivity. -/
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

/-- Every endomap fixes the designated root. This is a singleton condition,
    not a theorem about continuum, computation, SQL or physical recovery. -/
def EveryEndomapFixesRoot (S : Setting) : Prop :=
  ∀ f : S.X → S.X, f S.a = S.a

theorem every_endomap_fixes_root_iff (S : Setting) :
    EveryEndomapFixesRoot S ↔ ∀ x : S.X, x = S.a := by
  constructor
  · intro h x
    exact h (fun _ => x)
  · intro h f
    exact h (f S.a)

theorem witnessed_pair_refutes_fixed_root (S : Setting) (h : S.r S.a S.b) :
    ¬ EveryEndomapFixesRoot S := by
  intro fixed
  have hb : S.b = S.a := fixed (fun _ => S.b)
  exact setting_endpoints_distinct S h hb.symm


end SqlDomainSetting
