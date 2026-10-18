namespace QM.GOMC11

/-- Runtime authority status for a diagnostic representation state. -/
inductive AuthorityStatus
  | Licensed
  | Null
  deriving DecidableEq

/-- A finite diagnostic state carries residual mass plus an authority effect. -/
structure DiagState (E : Type) where
  mass : E → Nat
  authority_effect : AuthorityStatus

/--
Finite QM hosting records imported Hilbert/Born/channel structure abstractly.
The channel constraint is the GOMC firewall: hosted QM updates are diagnostic
and produce authority-null states unless a separate descent gate rewrites
authority.
-/
structure FiniteQMHosting (E : Type) where
  HilbertCarrier : Type
  POVMs : Type
  BornRule : POVMs → DiagState E → Nat
  Channels : Type
  UpdateTrace : Channels → DiagState E → DiagState E
  cptp_authority_null :
    ∀ (c : Channels) (s : DiagState E),
      (UpdateTrace c s).authority_effect = AuthorityStatus.Null

def HasAuthority {E : Type} (s : DiagState E) : Prop :=
  s.authority_effect = AuthorityStatus.Licensed

/--
GOMC-11: hosting finite Hilbert/Born/CPTP structure does not bypass the
authority firewall. Channel-produced diagnostic states remain authority-null by
the hosting contract itself.
-/
theorem qm_structures_are_authority_null
    {E : Type}
    (QMH : FiniteQMHosting E)
    (c : QMH.Channels)
    (s : DiagState E) :
    ¬ HasAuthority (QMH.UpdateTrace c s) := by
  intro h_auth
  have h_null :
      (QMH.UpdateTrace c s).authority_effect = AuthorityStatus.Null :=
    QMH.cptp_authority_null c s
  rw [HasAuthority, h_null] at h_auth
  contradiction

#print axioms QM.GOMC11.qm_structures_are_authority_null

end QM.GOMC11
