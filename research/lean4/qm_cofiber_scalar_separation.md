/-!
LT-H — Φ₁ (scalar) vs R_Λ (cofiber object): a bridge, not an identity.

Paper: `07_cofiber_to_banach_quotient_bridge.md`; `20_…` §7 (O022a).

The quotient diagnostic `Φ₁` is scalar-valued (`C1 → ℕ` here), while the cofiber
object `R_Λ` is a structured object carrying a scalar shadow PLUS extra categorical
data. The legitimate finite bridge is the *scalar* identity
`Φ₁ x = ‖R_Λ x‖_BanachShadow` (`phi1_eq_banachShadow`). The firewall: the cofiber
object is **not** recovered from its scalar shadow — two distinct cofiber objects
can share a Banach-shadow norm — so `Φ₁ = R_Λ` (scalar = object) is a conflation
that discards the extra structure. No authority; Mathlib-free.
-/

namespace QM

/-- The cofiber object `R_Λ`: a Banach-shadow scalar plus extra categorical data. -/
structure CofiberObj where
  shadow : Nat
  extra  : Nat
deriving DecidableEq

/-- The Banach-shadow norm extracts the scalar from the cofiber object. -/
def banachShadowNorm (o : CofiberObj) : Nat := o.shadow

variable {C1 : Type}

/-- The scalar quotient diagnostic Φ₁. -/
def Phi1 (φ : C1 → Nat) (x : C1) : Nat := φ x

/-- The cofiber object carrying Φ₁ as its shadow plus declared extra data. -/
def RLambda (φ ext : C1 → Nat) (x : C1) : CofiberObj := ⟨φ x, ext x⟩

/-- **The finite bridge (scalar level).** Φ₁ equals the Banach-shadow norm of the
cofiber object: the legitimate identity is scalar = scalar. -/
theorem phi1_eq_banachShadow (φ ext : C1 → Nat) (x : C1) :
    banachShadowNorm (RLambda φ ext x) = Phi1 φ x := rfl

/-- **Firewall (no scalar/object conflation).** The cofiber object is not recovered
from its scalar shadow: two distinct cofiber objects share a Banach-shadow norm.
Hence `Φ₁ = R_Λ` would discard the extra structure; only the scalar identity holds. -/
theorem cofiber_richer_than_scalar :
    ∃ a b : CofiberObj, a ≠ b ∧ banachShadowNorm a = banachShadowNorm b :=
  ⟨⟨5, 0⟩, ⟨5, 1⟩, by decide, rfl⟩

end QM

#print axioms QM.phi1_eq_banachShadow
#print axioms QM.cofiber_richer_than_scalar
