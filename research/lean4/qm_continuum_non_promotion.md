/-!
LT-S — finite shadows ⊬ continuum authority (the GTTC → Level-Q membrane).

Paper: `12_gtta_feynman_finite_shadow_histories.md` Parts 3–4; `27_…`; the
GTTC continuum layer; `11_…` T2 `exp(tH)` branch.

A finite-shadow family does **not** construct a `ContinuumKernel` without a declared
`ConvergenceCertificate` (cofinal shadows + certified refinement + declared topology
+ convergence). The intake returns `oracleNeeded` absent the certificate, and only
`promoted` once it is supplied — this is exactly the membrane Level Q (`Ω_Q`,
`research/published/9999_Q/`) consumes: continuum *monsters* are quarantined until a
finite-shadow certificate descends them through GTTC.

No continuum existence theorem is asserted; no authority minted (continuum
membership ⊬ authority). Mathlib-free.
-/

namespace QM

/-- A cofinal finite-shadow family (toy index). -/
structure ShadowFamily where
  idx : Nat

/-- A continuum object/kernel — the "monster" Level Q holds. -/
structure ContinuumKernel where
  val : Nat

/-- The four-ingredient exit certificate: declared topology + convergence data. -/
structure ConvergenceCertificate where
  topology : Nat
  refinement : Nat
  rate : Nat

/-- Intake outcome: either a licensed continuum kernel, or a refusal. -/
inductive ContinuumOutcome where
  | promoted (k : ContinuumKernel)
  | oracleNeeded

/-- The GTTC → Q intake: a shadow family promotes to a continuum kernel **only** with
a convergence certificate; absent it, the outcome is `oracleNeeded`. -/
def intake (sf : ShadowFamily) : Option ConvergenceCertificate → ContinuumOutcome
  | none     => ContinuumOutcome.oracleNeeded
  | some _   => ContinuumOutcome.promoted ⟨sf.idx⟩

/-- **Membrane firewall.** Without a convergence certificate a finite-shadow family
lands in `oracleNeeded` — it does not construct a continuum kernel. -/
theorem shadow_no_cert_oracleNeeded (sf : ShadowFamily) :
    intake sf none = ContinuumOutcome.oracleNeeded := rfl

/-- No continuum kernel is produced from shadows alone (no certificate). -/
theorem shadow_no_cert_not_promoted (sf : ShadowFamily) (k : ContinuumKernel) :
    intake sf none ≠ ContinuumOutcome.promoted k := by
  simp [intake]

/-- With a declared convergence certificate, promotion is licensed. -/
theorem shadow_with_cert_promotes (sf : ShadowFamily) (c : ConvergenceCertificate) :
    ∃ k, intake sf (some c) = ContinuumOutcome.promoted k :=
  ⟨⟨sf.idx⟩, rfl⟩

end QM

#print axioms QM.shadow_no_cert_oracleNeeded
#print axioms QM.shadow_no_cert_not_promoted
#print axioms QM.shadow_with_cert_promotes
