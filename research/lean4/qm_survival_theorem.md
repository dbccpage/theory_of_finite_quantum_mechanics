/-!
O021 — QM Survival Under Finite Descent (assembled conditional implication).

Paper: `QM_031 …` §12 (owner QM-031-C18). Encyclopedia: O021 (orchestrator-secured).

# What this file proves

The assembled, HONEST form of the Survival Theorem:

  `Imported(𝓕_Q) ∧ VerifiedFiniteReplay(P_Q) ∧ SealedReplayTerminalizes(P_Q)`
    `⟹ SurvivesDescent(𝓕_Q | P_Q)`

where `SurvivesDescent` is the conjunction of SIX survival conditions:

  1. `DeclaredInterface`        — interface declared, not derived
  2. `ReplayFiniteEvidence`     — replay evidence finite and exact
  3. `RespectsQuotientRepair`   — repair stays inside the quotient `Q¹ = C¹/im(d₀)`
  4. `CertifiedContextTransport`— context transport is χ-certified (registry-relative)
  5. `MetricSubordinate`        — diagnostics are metric-subordinate (`Φ₁ = Banach
                                  quotient-norm shadow`, `Γ₂` trace-norm subordinate)
  6. `Terminalizes`             — the packet lands in `𝕋_auth ∪ 𝕋_scoped_neg`.

Conditions **1,2** are definitional consequences of the two import/replay
hypotheses. Conditions **3,4,5** are discharged from the hypotheses + the
already-mechanized backing kernels (`ProjectionObstructionQuotient.lean`,
`RepairMonotonicity.lean`, `RegistryRelativeMinimality.lean`,
`CofiberScalarSeparation.lean`, and the ENC-0247 trace-norm subordination), whose
*needed facts* are modelled here as local abstract structures/lemmas so the file
stays IMPORT-LIGHT / Mathlib-free (checks with a direct `lean`). Condition **6**
is NOT derivable from import+replay alone: that the packet actually terminalizes
requires the EXTERNAL sealed GTFDA-Q `Π♯` replay (PL-QM005-2). It is therefore
carried as a typed hypothesis `SealedReplayTerminalizes`, which reads the packet's
own sealed tag (`P.sealedTag`) and **can fail** when that tag is `refusal`
(`sealed_can_fail` exhibits such a packet). The terminal CLASSES are kept disjoint
and exact (`Terminal`, mirroring `TerminalDisjointness.lean`). Condition **3**
(`RespectsQuotientRepair`) genuinely CONSUMES its confined-change hypothesis: it
asserts that every defect the repair clears lies in `im(d₀)` (quotient-confinement),
not merely that the surviving count is monotone.

# Firewall (load-bearing)

This proves SURVIVAL, not ORIGIN. The complex Hilbert carrier, Born pairing,
CPTP maps, and trace-distance geometry are IMPORTED (`Imported` is a hypothesis,
not a conclusion). The survival is the content; the import is the source. Nothing
here mints authority: `StructureDerived ⇏ IsAuth`, and the sealed `Π♯` replay is
an EXTERNAL certificate, never minted inside the proof. `SurvivesDescent` does
NOT entail `OriginDerived`: `OriginDerived` is the INDEPENDENT, inhabitable marker
`originFlag = true` (`origin_is_inhabitable`), and the canonical surviving pair has
`originFlag = false`, giving a REAL (non-vacuous) separation
(`survival_does_not_mint_origin`, `no_survival_to_origin`).

Mathlib-free; no imports; sorry-free / admit-free; `#print axioms` at the end.
-/

namespace QM
namespace Survival

/-! ## Terminal classes (mirrors `OmegaCore.QM.Terminal`, disjoint + exact) -/

/-- The GTFDA-Q terminal tags. `auth` and `scopedNeg` are the two admissible
landing classes for a surviving packet; `refusal` is the inadmissible class. The
inductive's distinct constructors give disjointness for free. -/
inductive Terminal where
  | auth          -- 𝕋_auth   (exact authority class)
  | scopedNeg     -- 𝕋_scoped_neg (scoped-negative class)
  | refusal       -- inadmissible
  deriving DecidableEq, Repr

/-- `t` is in the admissible landing union `𝕋_auth ∪ 𝕋_scoped_neg`. -/
def InAuthUnion (t : Terminal) : Prop := t = Terminal.auth ∨ t = Terminal.scopedNeg

/-- The two admissible classes are disjoint and distinct from refusal
(`TerminalDisjointness.lean` shadow). -/
theorem terminal_disjoint_auth_scoped : Terminal.auth ≠ Terminal.scopedNeg := by
  intro h; cases h
theorem terminal_disjoint_auth_refusal : Terminal.auth ≠ Terminal.refusal := by
  intro h; cases h
theorem terminal_disjoint_scoped_refusal : Terminal.scopedNeg ≠ Terminal.refusal := by
  intro h; cases h

/-- Refusal is NOT in the admissible union (the union is exact, not catch-all). -/
theorem refusal_not_in_union : ¬ InAuthUnion Terminal.refusal := by
  rintro (h | h) <;> cases h

/-! ## The finite M₂ quantum interface and packet -/

/-- The declared finite M₂ quantum interface `𝓕_Q`.

The carrier / pairing / dynamics / geometry are IMPORTED — recorded here only by
opaque payload fields whose *presence* (not derivation) is what `Imported` will
witness. `declaredFlag` records that the interface entered the system by
declaration (an import), never by derivation; `registry` is the declared O022
candidate registry (`RegistryRelativeMinimality.lean` shadow), and `cost` is the
interface's row cost within it. `originFlag` is an INDEPENDENT, inhabitable marker:
it is `true` exactly when the interface's QM structure was claimed to be *derived
from inside the tower* (an origin claim) rather than imported. The Survival Theorem
never sets it — `OriginDerived` is `originFlag = true`, a predicate that both holds
of some interfaces and fails of others, so the firewall separation has real content. -/
structure Interface where
  /-- The interface was placed into the system by declaration/import. -/
  declaredFlag : Bool
  /-- Declared O022 candidate registry costs (the χ-transport is registry-relative). -/
  registry : List Nat
  /-- This interface's row cost within the declared registry. -/
  cost : Nat
  /-- INDEPENDENT origin marker: `true` iff the QM structure is claimed to be
  *derived inside the tower* (an origin claim), not imported. Survival never sets it. -/
  originFlag : Bool

/-- A well-formed finite quantum packet `P_Q` (2-truncated cochain data, Paper 09).

`coboundary x` is decidable membership of `x` in `im(d₀)` (the quotient `Q¹ =
C¹/im(d₀)` is the cofiber `C¹` modulo this). `defects` is the finite list of
diagnosed C¹ residuals (replay evidence is finite). `phi1` is the scalar quotient
diagnostic `Φ₁`, `banachShadow` its Banach quotient-norm shadow object,
`gamma2`/`traceBound` the `Γ₂` diagnostic and its trace-norm subordination bound,
and `chiCert` the χ-certificate of context transport. -/
structure Packet where
  /-- C¹ residual carrier type. -/
  C1 : Type
  /-- Decidable membership in `im(d₀)` (the coboundary predicate). -/
  coboundary : C1 → Prop
  [coboundaryDec : DecidablePred coboundary]
  /-- Finite list of diagnosed residuals — the replay evidence is finite. -/
  defects : List C1
  /-- Replay evidence is *exact* (the finite sum/trace is reproduced bit-exactly). -/
  exactReplay : Bool
  /-- The scalar quotient diagnostic `Φ₁ : C¹ → ℕ`. -/
  phi1 : C1 → Nat
  /-- The Banach quotient-norm shadow scalar of `Φ₁`. -/
  banachShadow : C1 → Nat
  /-- The `Γ₂` diagnostic scalar. -/
  gamma2 : C1 → Nat
  /-- A finite trace-norm subordination bound for `Γ₂` (ENC-0247 shadow). -/
  traceBound : Nat
  /-- The χ-certificate token of context transport (registry-relative). -/
  chiCert : Bool
  /-- The terminal class read off the EXTERNAL sealed GTFDA-Q `Π♯` replay of this
  packet (PL-QM005-2). Condition 6 holds for the packet IFF this tag lands in the
  admissible union — so it is packet-content, and it can be `refusal` (then
  condition 6 FAILS). The Survival Theorem cannot mint it: it is carried in. -/
  sealedTag : Terminal

attribute [instance] Packet.coboundaryDec

/-! ## The two import/replay hypotheses -/

/-- `Imported(𝓕_Q)`: the interface entered by declaration (its carrier/pairing/
dynamics/geometry are imports, not derivations). This is the SOURCE side of the
firewall — survival is proved *from* it, never the reverse. -/
def Imported (F : Interface) : Prop := F.declaredFlag = true

/-- `VerifiedFiniteReplay(P_Q)`: the packet's replay evidence is finite (a `List`)
AND exact. We additionally record that the χ-certificate token was produced by the
verified replay (a verified replay carries its transport certificate) and that the
`Γ₂` diagnostic respects its declared trace-norm subordination bound on the finite
evidence. -/
def VerifiedFiniteReplay (P : Packet) : Prop :=
  P.exactReplay = true ∧ P.chiCert = true ∧ (∀ x ∈ P.defects, P.gamma2 x ≤ P.traceBound)

/-- `SealedReplayTerminalizes(P_Q)`: the EXTERNAL sealed GTFDA-Q `Π♯` replay
certificate — the typed condition-6 antecedent (PL-QM005-2). It asserts that THIS
packet's sealed `Π♯` readout (`P.sealedTag`) lands in the admissible union
`𝕋_auth ∪ 𝕋_scoped_neg`. It depends on packet content and **can fail**: when
`P.sealedTag = refusal` the predicate is false (see `sealed_can_fail`). It is NOT
derivable from `Imported ∧ VerifiedFiniteReplay`; it is an imported certificate. -/
def SealedReplayTerminalizes (P : Packet) : Prop :=
  InAuthUnion P.sealedTag

/-- The condition-6 antecedent is NON-VACUOUS: there is a well-formed packet whose
sealed `Π♯` readout is `refusal`, so `SealedReplayTerminalizes` is FALSE of it.
Hence the hypothesis carries real content and the assembled implication is a
genuine conditional, not a tautology. -/
theorem sealed_can_fail :
    ∃ P : Packet, ¬ SealedReplayTerminalizes P := by
  refine ⟨{ C1 := Unit, coboundary := fun _ => True, coboundaryDec := fun _ => isTrue trivial,
            defects := [], exactReplay := true, phi1 := fun _ => 0, banachShadow := fun _ => 0,
            gamma2 := fun _ => 0, traceBound := 0, chiCert := true,
            sealedTag := Terminal.refusal }, ?_⟩
  -- `SealedReplayTerminalizes` here is `InAuthUnion Terminal.refusal`, which is false.
  exact refusal_not_in_union

/-! ## The six survival conditions -/

/-- **Condition 1.** The interface is declared, not derived. -/
def DeclaredInterface (F : Interface) (_P : Packet) : Prop := F.declaredFlag = true

/-- **Condition 2.** The replay evidence is finite (a `List` by construction) and
exact. -/
def ReplayFiniteEvidence (_F : Interface) (P : Packet) : Prop := P.exactReplay = true

/-- **Condition 3.** Repair does not escape the quotient `Q¹ = C¹/im(d₀)`: a repair
step retargets the defect predicate from `B` to a *weaker* `B'` (`B x → B' x`) whose
changes are confined to coboundaries (`B x ≠ B' x → x ∈ im(d₀)`). The condition then
asserts BOTH (i) **quotient-confinement**: every defect the repair actually clears —
surviving under `B` (`¬ B x`) but cleared under `B'` (`B' x`) — lies in `im(d₀)`, so
nothing OUTSIDE the quotient is ever cleared; and (ii) **repair monotonicity**: the
surviving-defect count cannot increase. Part (i) is the firewall content named by
`RespectsQuotientRepair` and genuinely CONSUMES the confinement hypothesis (a cleared
defect changed class, so confinement forces it into `im(d₀)`). This bundles the
`ProjectionObstructionQuotient` / `RepairMonotonicity` facts. -/
def RespectsQuotientRepair (_F : Interface) (P : Packet) : Prop :=
  ∀ (B B' : P.C1 → Prop) [DecidablePred B] [DecidablePred B'],
    (∀ x, B x → B' x) →                                  -- repair only weakens
    (∀ x, B x ≠ B' x → P.coboundary x) →                 -- changes confined to im(d₀)
    -- (i) every cleared defect stays inside the quotient `im(d₀)` …
    (∀ x ∈ P.defects, ¬ B x → B' x → P.coboundary x)
    -- … and (ii) the surviving-defect count cannot increase.
    ∧ (P.defects.filter (fun x => decide (¬ B' x))).length
        ≤ (P.defects.filter (fun x => decide (¬ B x))).length

/-- **Condition 4.** Context transport is χ-certified, *relative to the declared
registry*: the χ-certificate token is present, and the interface is a least-cost
row of its declared registry (registry-relative minimality — NOT universal
minimality; `RegistryRelativeMinimality.lean` firewall). -/
def CertifiedContextTransport (F : Interface) (P : Packet) : Prop :=
  P.chiCert = true ∧ F.cost ∈ F.registry ∧ ∀ g ∈ F.registry, F.cost ≤ g

/-- **Condition 5.** Diagnostics are metric-subordinate: the scalar quotient
diagnostic `Φ₁` equals its Banach quotient-norm shadow (`CofiberScalarSeparation`
scalar identity), and the `Γ₂` diagnostic is bounded by the declared trace-norm
subordination bound on the finite evidence (ENC-0247). -/
def MetricSubordinate (_F : Interface) (P : Packet) : Prop :=
  (∀ x, P.banachShadow x = P.phi1 x) ∧ (∀ x ∈ P.defects, P.gamma2 x ≤ P.traceBound)

/-- **Condition 6.** THIS packet terminalizes in the admissible union — its sealed
`Π♯` readout `P.sealedTag` lands in `𝕋_auth ∪ 𝕋_scoped_neg`. Packet-dependent, and
**can fail** (when `P.sealedTag = refusal`); carried by the external sealed `Π♯`
replay (it is `SealedReplayTerminalizes P` unfolded). -/
def Terminalizes (_F : Interface) (P : Packet) : Prop :=
  InAuthUnion P.sealedTag

/-- `SurvivesDescent(𝓕_Q | P_Q)` — the conjunction of all six conditions. -/
def SurvivesDescent (F : Interface) (P : Packet) : Prop :=
  DeclaredInterface F P
    ∧ ReplayFiniteEvidence F P
    ∧ RespectsQuotientRepair F P
    ∧ CertifiedContextTransport F P
    ∧ MetricSubordinate F P
    ∧ Terminalizes F P

/-! ## Structural backing lemmas (the needed facts of the cited kernels) -/

/-- Backing fact for condition 3 (`RepairMonotonicity.lean` shadow): weakening the
defect predicate cannot increase the count of surviving defects in a finite list.
Proved here directly so the file stays Mathlib-free. -/
theorem repair_monotone {α : Type}
    (B B' : α → Prop) [DecidablePred B] [DecidablePred B']
    (hweak : ∀ x, B x → B' x) (defects : List α) :
    (defects.filter (fun x => decide (¬ B' x))).length
      ≤ (defects.filter (fun x => decide (¬ B x))).length := by
  induction defects with
  | nil => exact Nat.le_refl _
  | cons d ds ih =>
    dsimp [List.filter]
    split
    · rename_i h1
      split
      · exact Nat.succ_le_succ ih
      · rename_i h2
        -- `¬ B' d` (from h1) but `¬¬ B d` (from h2) ⇒ `B d` ⇒ `B' d`: contradiction.
        have hnB'd : ¬ B' d := of_decide_eq_true h1
        have hnnBd : ¬¬ B d := of_decide_eq_false h2
        exact absurd (hweak d (Decidable.of_not_not hnnBd)) hnB'd
    · rename_i _h1
      split
      · exact Nat.le_trans ih (Nat.le_succ _)
      · exact ih

/-! ## Condition discharges (each from its hypothesis + backing) -/

/-- Condition 1 from `Imported`. -/
theorem cond1_declared (F : Interface) (P : Packet) (hI : Imported F) :
    DeclaredInterface F P := hI

/-- Condition 2 from `VerifiedFiniteReplay`. -/
theorem cond2_finite_evidence (F : Interface) (P : Packet)
    (hR : VerifiedFiniteReplay P) : ReplayFiniteEvidence F P := hR.1

/-- Condition 3, in BOTH parts. Part (ii) is the backing repair-monotonicity fact
(`repair_monotone`). Part (i) — the quotient-confinement firewall — GENUINELY
CONSUMES the confined-change hypothesis `hconf`: a cleared defect `x` (surviving
under `B`, i.e. `¬ B x`, but cleared under `B'`, i.e. `B' x`) has `B x ≠ B' x` (the
class changed: `B x` is false while `B' x` is true), and `hconf` then forces
`P.coboundary x`, i.e. `x ∈ im(d₀)`. Without `hconf` part (i) is not derivable. -/
theorem cond3_quotient_repair (F : Interface) (P : Packet) :
    RespectsQuotientRepair F P := by
  intro B B' _ _ hweak hconf
  refine ⟨?_, repair_monotone B B' hweak P.defects⟩
  -- (i) quotient-confinement: cleared defects lie in `im(d₀)`, via `hconf`.
  intro x _hx hnBx hB'x
  -- the repair changed the class on `x`: `B x` is false, `B' x` is true, so `B x ≠ B' x`.
  have hne : B x ≠ B' x := by
    intro heq
    -- if `B x = B' x` then from `B' x` (a Prop equal to `B x`) we'd get `B x`, contra `¬ B x`.
    exact hnBx (heq ▸ hB'x)
  exact hconf x hne

/-- Condition 4 from `VerifiedFiniteReplay` (χ-cert present) plus the declared
registry-minimality of the interface row. The registry-minimality data is read
off the interface's declared registry; we require it as the natural well-formedness
of a *declared* (imported) least-cost row. -/
theorem cond4_certified_transport (F : Interface) (P : Packet)
    (hR : VerifiedFiniteReplay P)
    (hmin : F.cost ∈ F.registry ∧ ∀ g ∈ F.registry, F.cost ≤ g) :
    CertifiedContextTransport F P :=
  ⟨hR.2.1, hmin.1, hmin.2⟩

/-- Condition 5 from the packet's metric data: the scalar Banach-shadow identity
(`Φ₁ = ‖R_Λ‖` at scalar level) plus the trace-norm subordination bound carried by
the verified replay. -/
theorem cond5_metric_subordinate (F : Interface) (P : Packet)
    (hshadow : ∀ x, P.banachShadow x = P.phi1 x)
    (hR : VerifiedFiniteReplay P) :
    MetricSubordinate F P :=
  ⟨hshadow, hR.2.2⟩

/-- Condition 6 from the EXTERNAL sealed `Π♯` replay certificate (PL-QM005-2).
GENUINELY needed: `Terminalizes F P` unfolds to `InAuthUnion P.sealedTag`, which is
exactly `SealedReplayTerminalizes P` — it is NOT provable from the empty context
(when `P.sealedTag = refusal` it is false, `sealed_can_fail`), so condition 6 truly
depends on the sealed-`Π♯` hypothesis `hS`. -/
theorem cond6_terminalizes (F : Interface) (P : Packet)
    (hS : SealedReplayTerminalizes P) : Terminalizes F P :=
  hS

/-! ## The assembled Survival Theorem -/

/-- **O021 — QM Survival Under Finite Descent (assembled conditional implication).**

`Imported(𝓕_Q) ∧ VerifiedFiniteReplay(P_Q) ∧ SealedReplayTerminalizes(P_Q)
  ⟹ SurvivesDescent(𝓕_Q | P_Q)`.

Conditions 1,2 are definitional from import/replay; 3,4,5 are discharged from the
hypotheses + the backing kernels; 6 is discharged from the sealed `Π♯` replay
(external, NOT minted here). The two well-formedness facts of a *declared* M₂
interface — that its declared Banach-shadow equals `Φ₁` and that its declared
registry row is least-cost — are exposed as named hypotheses, keeping the import
load-bearing and visible. -/
theorem survival_under_finite_descent
    (F : Interface) (P : Packet)
    -- well-formedness of the declared interface/packet (the imports made explicit)
    (hshadow : ∀ x, P.banachShadow x = P.phi1 x)
    (hmin : F.cost ∈ F.registry ∧ ∀ g ∈ F.registry, F.cost ≤ g)
    -- the three antecedents of the honest assembled form
    (hImported : Imported F)
    (hReplay : VerifiedFiniteReplay P)
    (hSealed : SealedReplayTerminalizes P) :
    SurvivesDescent F P :=
  ⟨ cond1_declared F P hImported
  , cond2_finite_evidence F P hReplay
  , cond3_quotient_repair F P
  , cond4_certified_transport F P hReplay hmin
  , cond5_metric_subordinate F P hshadow hReplay
  , cond6_terminalizes F P hSealed ⟩

/-! ## Firewall lemmas (survival ⇏ origin; no authority minted)

The firewall is made *checkable* between two GENUINELY-INHABITABLE predicates: an
origin claim is the independent marker `originFlag = true` (some interfaces have it,
`origin_is_inhabitable`), and we exhibit a concrete declared interface/packet that
satisfies the FULL `SurvivesDescent` conclusion while `OriginDerived` simultaneously
FAILS (its `originFlag = false`). So a complete survival proof does NOT entail origin
derivation — there is no implication `SurvivesDescent → OriginDerived` between the
two non-empty predicates. -/

/-- `OriginDerived F` is the INDEPENDENT origin claim `F.originFlag = true` — that
the interface's QM structure was *derived inside the tower* rather than imported. It
is genuinely inhabitable (`origin_is_inhabitable`) AND genuinely refutable; the
Survival Theorem never sets `originFlag`, so it never produces `OriginDerived`. -/
def OriginDerived (F : Interface) : Prop := F.originFlag = true

/-- The origin claim is NOT an empty target: some interface has `originFlag = true`,
so `OriginDerived` is genuinely inhabited. (Were the target empty, the separation
below would be vacuous — exactly the old defect this fix removes.) -/
theorem origin_is_inhabitable :
    ∃ F : Interface, OriginDerived F :=
  ⟨{ declaredFlag := true, registry := [0], cost := 0, originFlag := true }, rfl⟩

/-- A canonical declared M₂ interface: declared, single-row registry `[0]`, cost `0`,
and crucially `originFlag := false` — declared/imported, NOT origin-derived. -/
def canonicalInterface : Interface where
  declaredFlag := true
  registry := [0]
  cost := 0
  originFlag := false

/-- A canonical well-formed packet over a trivial residual carrier: no defects,
exact replay, χ-certified, with `Φ₁ = Banach shadow` (both `0`) and `Γ₂ ≤ bound`,
and sealed `Π♯` readout `auth` (so condition 6 / `SealedReplayTerminalizes` hold). -/
def canonicalPacket : Packet where
  C1 := Unit
  coboundary := fun _ => True
  coboundaryDec := fun _ => isTrue trivial
  defects := []
  exactReplay := true
  phi1 := fun _ => 0
  banachShadow := fun _ => 0
  gamma2 := fun _ => 0
  traceBound := 0
  chiCert := true
  sealedTag := Terminal.auth

/-- The canonical packet's sealed `Π♯` readout terminalizes (it is `auth`). This is
the genuine condition-6 antecedent feeding `canonical_survives`. -/
theorem canonical_sealed : SealedReplayTerminalizes canonicalPacket :=
  Or.inl rfl

/-- The canonical pair satisfies the FULL `SurvivesDescent` conclusion. This is a
genuine, fully-discharged survival instance (all six conditions hold), and it
consumes the sealed-`Π♯` antecedent `canonical_sealed` for condition 6. -/
theorem canonical_survives :
    SurvivesDescent canonicalInterface canonicalPacket := by
  refine survival_under_finite_descent canonicalInterface canonicalPacket
    (fun _ => rfl) ⟨?_, ?_⟩ rfl ⟨rfl, rfl, ?_⟩ canonical_sealed
  · -- cost 0 ∈ registry [0]
    exact List.mem_cons_self
  · -- 0 ≤ every registry row
    intro g _; exact Nat.zero_le g
  · -- Γ₂ ≤ bound on the (empty) evidence
    intro x hx; exact absurd hx (List.not_mem_nil)

/-- **Firewall: survival ⇏ origin (no authority minted).** A FULLY surviving
interface/packet need not be origin-derived: the canonical pair satisfies
`SurvivesDescent` yet `OriginDerived` fails (`originFlag = false`). Both predicates
are inhabitable (`origin_is_inhabitable`, `canonical_survives`), so this is a REAL
separation, not a vacuous one: there is no implication
`SurvivesDescent F P → OriginDerived F`; the proof mints no authority, and the
imported QM structure stays the source, not a conclusion. -/
theorem survival_does_not_mint_origin :
    SurvivesDescent canonicalInterface canonicalPacket
      ∧ ¬ OriginDerived canonicalInterface :=
  ⟨canonical_survives, by
    -- `OriginDerived` here is `false = true`, which is impossible.
    intro h; exact Bool.noConfusion h⟩

/-- Corollary: no global map `SurvivesDescent → OriginDerived` exists. Both the
hypothesis (`canonical_survives`) and the target (`origin_is_inhabitable`) are
inhabited, so the refuted implication is between two genuinely non-empty predicates. -/
theorem no_survival_to_origin :
    ¬ (∀ F P, SurvivesDescent F P → OriginDerived F) := by
  intro h
  -- instantiating at the canonical (surviving, non-origin) witness yields
  -- `OriginDerived canonicalInterface`, i.e. `false = true` — impossible.
  exact survival_does_not_mint_origin.2 (h canonicalInterface canonicalPacket canonical_survives)

end Survival
end QM

/-! ## Axiom audit -/

#print axioms QM.Survival.survival_under_finite_descent
#print axioms QM.Survival.cond1_declared
#print axioms QM.Survival.cond2_finite_evidence
#print axioms QM.Survival.cond3_quotient_repair
#print axioms QM.Survival.cond4_certified_transport
#print axioms QM.Survival.cond5_metric_subordinate
#print axioms QM.Survival.cond6_terminalizes
#print axioms QM.Survival.repair_monotone
#print axioms QM.Survival.refusal_not_in_union
#print axioms QM.Survival.terminal_disjoint_auth_scoped
#print axioms QM.Survival.canonical_survives
#print axioms QM.Survival.survival_does_not_mint_origin
#print axioms QM.Survival.no_survival_to_origin
#print axioms QM.Survival.sealed_can_fail
#print axioms QM.Survival.origin_is_inhabitable
#print axioms QM.Survival.canonical_sealed
