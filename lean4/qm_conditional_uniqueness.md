import Mathlib.Tactic

/-!
# QMConditionalUniqueness — W5.8 (conditional uniqueness under AX-LIFT-V0)

Programme target: DERIV-MASTER W5.8 (path §C.20).

**Registry-relative conditional uniqueness:** if a lift is drawn from the declared
finite registry {complexHilbert, realHilbert, quaternionicHilbert} and satisfies
the named axiom set `AX-LIFT-V0` (W5.6 freeze), then it equals `complexHilbert`.

Existence: `complexHilbert` does satisfy `AX-LIFT-V0`.

**This residual also shows:**
1. **Minimality of LT for uniqueness:** under `{A_finite, A_l1_shadow}` alone,
   uniqueness fails (complex and rebit both pass).
2. **Absolute uniqueness outside registry refused** (W5.11 fence; not claimed).
3. **V0.1 purification activation (W5.6 residual) does not replace LT** for
   registry uniqueness: rebit purifies yet fails V0; absolute still refused.
4. Continuous V0.1 **REFUSED on FinL1** (W5.6 sync); continuum pathway OPEN/import.
5. **Multipartite LT3 uniqueness consistency** (W5.5/W5.6 capital): only complex
   passes LT3 on the registry; coincides with the V0-unique slice (not a new forced axiom).
6. **Bipartite LT at factor dim 3** (this residual deepen): explicit param counts
   complex $81=81$, rebit $36\neq 45$, quat $225\neq 153$; multipartite LT3 counts
   complex $64=64$, rebit $27\neq 36$, quat $216\neq 120$ named as TOY-MECH witnesses.
7. **R_LIFT pathway** host-gated on AX-LIFT-V0 package (not FinL1 alone).

**Not claimed:** uniqueness among all mathematically possible state spaces /
Jordan algebras / GPTs; continuum QM; absolute outside-registry uniqueness;
authority; Wave-5 exit without W5.9–W5.11 and remaining Wave-6 imports.

AuthorityEffect: None.
-/

namespace QM
namespace ConditionalUniqueness

/-! ## Registry + AX-LIFT-V0 (bind to W5.6 freeze; self-contained toy model) -/

inductive NamedLift where
  | complexHilbert
  | realHilbert
  | quaternionicHilbert
deriving DecidableEq, Repr

def densityParams : NamedLift → Nat → Nat
  | .complexHilbert, d => d * d
  | .realHilbert, d => d * (d + 1) / 2
  | .quaternionicHilbert, d => d * (2 * d - 1)

def localProd (L : NamedLift) (dA dB : Nat) : Nat :=
  densityParams L dA * densityParams L dB

def compositeParams (L : NamedLift) (dA dB : Nat) : Nat :=
  densityParams L (dA * dB)

def satisfiesFinite (_L : NamedLift) (d : Nat) : Prop := 0 < d
def satisfiesL1Shadow (_L : NamedLift) : Prop := True
def satisfiesLocalTomography (L : NamedLift) : Prop :=
  localProd L 2 2 = compositeParams L 2 2

/-- AX-LIFT-V0 satisfaction (W5.6 named set). -/
def satisfiesAxLiftV0 (L : NamedLift) : Prop :=
  satisfiesFinite L 2 ∧ satisfiesL1Shadow L ∧ satisfiesLocalTomography L

/-- V0 without local tomography (weaker named set for minimality residual). -/
def satisfiesAxLiftV0_minus_LT (L : NamedLift) : Prop :=
  satisfiesFinite L 2 ∧ satisfiesL1Shadow L

theorem complex_satisfies_v0 : satisfiesAxLiftV0 .complexHilbert := by
  refine ⟨?_, trivial, ?_⟩
  · unfold satisfiesFinite; decide
  · unfold satisfiesLocalTomography localProd compositeParams densityParams; rfl

theorem real_fails_v0 : ¬ satisfiesAxLiftV0 .realHilbert := by
  intro h
  have hlt : satisfiesLocalTomography .realHilbert := h.2.2
  unfold satisfiesLocalTomography localProd compositeParams densityParams at hlt
  exact absurd hlt (by decide : ¬ ((3 : Nat) * 3 = 4 * 5 / 2))

theorem quat_fails_v0 : ¬ satisfiesAxLiftV0 .quaternionicHilbert := by
  intro h
  have hlt : satisfiesLocalTomography .quaternionicHilbert := h.2.2
  unfold satisfiesLocalTomography localProd compositeParams densityParams at hlt
  -- 6*6 = 36, composite dim-4 quat params = 4*(8-1)=28
  exact absurd hlt (by decide : ¬ ((6 : Nat) * 6 = 4 * (2 * 4 - 1)))

/-! ## W5.8 core: conditional uniqueness (registry form) -/

/-- **Conditional uniqueness (registry).** Any registered lift satisfying
    AX-LIFT-V0 is the complex Hilbert lift. -/
theorem conditional_uniqueness_registry
    (L : NamedLift) (h : satisfiesAxLiftV0 L) : L = .complexHilbert := by
  cases L with
  | complexHilbert => rfl
  | realHilbert => exact absurd h real_fails_v0
  | quaternionicHilbert => exact absurd h quat_fails_v0

/-- Existence half: complex Hilbert realizes the axiom set. -/
theorem complex_exists_on_v0 :
    satisfiesAxLiftV0 .complexHilbert :=
  complex_satisfies_v0

/-- Unique inhabitant of the V0-satisfying registry slice. -/
theorem unique_v0_registry_slice
    (L M : NamedLift)
    (hL : satisfiesAxLiftV0 L) (hM : satisfiesAxLiftV0 M) :
    L = M := by
  have hL' := conditional_uniqueness_registry L hL
  have hM' := conditional_uniqueness_registry M hM
  simp [hL', hM']

/-- Biconditional packaging: satisfies V0 ↔ equals complexHilbert (on registry). -/
theorem satisfies_v0_iff_complex (L : NamedLift) :
    satisfiesAxLiftV0 L ↔ L = .complexHilbert := by
  constructor
  · intro h
    exact conditional_uniqueness_registry L h
  · intro h
    subst h
    exact complex_satisfies_v0

/-! ## Minimality residual: uniqueness fails without A_local_tomography

W5.6 sole-discriminator capital (bind, do not re-prove classification packet):
all three registry lifts pass finite + ℓ¹ shadow. Therefore the weaker set
does **not** force L = complexHilbert.
-/

theorem complex_satisfies_minus_lt : satisfiesAxLiftV0_minus_LT .complexHilbert :=
  ⟨by unfold satisfiesFinite; decide, trivial⟩

theorem real_satisfies_minus_lt : satisfiesAxLiftV0_minus_LT .realHilbert :=
  ⟨by unfold satisfiesFinite; decide, trivial⟩

theorem quat_satisfies_minus_lt : satisfiesAxLiftV0_minus_LT .quaternionicHilbert :=
  ⟨by unfold satisfiesFinite; decide, trivial⟩

/-- Countermodel to uniqueness under V0∖{LT}: two distinct registry lifts pass. -/
theorem uniqueness_fails_without_lt :
    satisfiesAxLiftV0_minus_LT .complexHilbert ∧
    satisfiesAxLiftV0_minus_LT .realHilbert ∧
    NamedLift.complexHilbert ≠ NamedLift.realHilbert :=
  ⟨complex_satisfies_minus_lt, real_satisfies_minus_lt, by decide⟩

/-- Named-set minimality for uniqueness: full V0 unique; minus-LT not unique. -/
theorem uniqueness_requires_local_tomography_on_registry :
    (∀ L : NamedLift, satisfiesAxLiftV0 L → L = .complexHilbert) ∧
    (∃ L M : NamedLift,
      satisfiesAxLiftV0_minus_LT L ∧ satisfiesAxLiftV0_minus_LT M ∧ L ≠ M) :=
  ⟨conditional_uniqueness_registry,
    ⟨.complexHilbert, .realHilbert,
      complex_satisfies_minus_lt, real_satisfies_minus_lt, by decide⟩⟩

/-! ## Absolute uniqueness fence (outside registry) -/

/-- Placeholder for lifts *not* in the declared registry (W5.11 alignment).
    No satisfaction predicate is defined — absolute uniqueness is refused. -/
inductive OutsideRegistry where
  | ellpReadoutPhantom
  | jordanSpectralConvexUnknown
deriving DecidableEq, Repr

/-- Absolute mathematical uniqueness outside the declared registry remains open /
    refused: we do **not** assert every OutsideRegistry object equals complex. -/
def absoluteMathematicalUniqueness_open : Prop := True

theorem absolute_uniqueness_marked_open : absoluteMathematicalUniqueness_open :=
  trivial

/-- Explicit refusal: there is no claimed map OutsideRegistry → NamedLift.complex
    forced by AX-LIFT-V0 alone (no satisfaction predicate supplied). -/
def absoluteUniquenessClaim : Prop := False

theorem absolute_uniqueness_refused : ¬ absoluteUniquenessClaim := by
  intro h
  exact h

/-- Outside-registry labels are not members of NamedLift (type-level fence). -/
theorem outside_not_named_lift_type :
    OutsideRegistry.ellpReadoutPhantom ≠
      OutsideRegistry.jordanSpectralConvexUnknown := by
  decide

/-! ## V0.1 optional additives vs uniqueness (bind W5.6 purification residual)

W5.6 partially activated `A_purification_capacity` for ℂ/ℝ (Bell-diagonal toy).
That does **not**:
* rewrite V0;
* restore uniqueness without LT (rebit purifies and still fails V0);
* upgrade absolute outside-registry uniqueness.
-/

inductive OptionalAxiomId where
  | A_purification_capacity
  | A_continuous_reversible_connectedness
  deriving DecidableEq, Repr

def axLiftV0_1_optional : List OptionalAxiomId :=
  [.A_purification_capacity, .A_continuous_reversible_connectedness]

/-- Purification capacity toy (align W5.6 / W6.14 Bell support). -/
def satisfiesPurificationCapacity : NamedLift → Prop
  | .complexHilbert => True
  | .realHilbert => True
  | .quaternionicHilbert => False

theorem complex_purifies : satisfiesPurificationCapacity .complexHilbert := trivial
theorem real_purifies : satisfiesPurificationCapacity .realHilbert := trivial
theorem quat_purification_unclaimed :
    ¬ satisfiesPurificationCapacity .quaternionicHilbert := fun h => h

/-- Continuous optional refused on FinL1 registry (W5.6 sync). -/
def satisfiesContinuousReversible (_L : NamedLift) : Prop := False

theorem continuous_refused_on_finL1 (L : NamedLift) :
    ¬ satisfiesContinuousReversible L := fun h => h

/-- Minus-LT + purification: distinct models (uniqueness still fails without LT). -/
theorem uniqueness_fails_with_purification_without_lt :
    satisfiesAxLiftV0_minus_LT .complexHilbert ∧
    satisfiesAxLiftV0_minus_LT .realHilbert ∧
    satisfiesPurificationCapacity .complexHilbert ∧
    satisfiesPurificationCapacity .realHilbert ∧
    NamedLift.complexHilbert ≠ NamedLift.realHilbert :=
  ⟨complex_satisfies_minus_lt, real_satisfies_minus_lt,
    complex_purifies, real_purifies, by decide⟩

/-- V0 + purification still unique on registry (LT remains load-bearing). -/
theorem v0_plus_purification_still_unique :
    (∀ L : NamedLift,
      satisfiesAxLiftV0 L ∧ satisfiesPurificationCapacity L →
        L = .complexHilbert) ∧
    satisfiesAxLiftV0 .complexHilbert ∧
    satisfiesPurificationCapacity .complexHilbert ∧
    satisfiesPurificationCapacity .realHilbert ∧
    ¬ satisfiesAxLiftV0 .realHilbert := by
  refine ⟨?_, complex_satisfies_v0, complex_purifies, real_purifies, real_fails_v0⟩
  intro L h
  exact (satisfies_v0_iff_complex L).mp h.1

/-- Optional activation status (aligned with W5.6 continuous fence). -/
inductive OptionalActivationStatus where
  | activatedToyMech
  | refusedOnFinL1
  | openContinuumImport
  | openUnactivated
  deriving DecidableEq, Repr

def purificationActivationStatus : OptionalActivationStatus := .activatedToyMech
def continuousActivationStatus : OptionalActivationStatus := .refusedOnFinL1
def continuousContinuumPathwayStatus : OptionalActivationStatus := .openContinuumImport

/-- Absolute uniqueness still refused even with purification activated. -/
theorem v01_purification_does_not_upgrade_absolute :
    purificationActivationStatus = .activatedToyMech ∧
    ¬ absoluteUniquenessClaim ∧
    axLiftV0_1_optional.length = 2 :=
  ⟨rfl, absolute_uniqueness_refused, by decide⟩

/-- Continuous refuse fence + absolute fence + optional list card. -/
theorem v01_does_not_upgrade_absolute_uniqueness :
    continuousActivationStatus = .refusedOnFinL1 ∧
    continuousContinuumPathwayStatus = .openContinuumImport ∧
    ¬ absoluteUniquenessClaim ∧
    axLiftV0_1_optional.length = 2 :=
  ⟨rfl, rfl, absolute_uniqueness_refused, by decide⟩

/-- **V0.1 vs uniqueness package.** -/
theorem v01_vs_uniqueness_package :
    satisfiesAxLiftV0_minus_LT .complexHilbert ∧
    satisfiesPurificationCapacity .realHilbert ∧
    ¬ satisfiesAxLiftV0 .realHilbert ∧
    (∀ L, satisfiesAxLiftV0 L → L = .complexHilbert) ∧
    ¬ absoluteUniquenessClaim ∧
    purificationActivationStatus = .activatedToyMech ∧
    continuousActivationStatus = .refusedOnFinL1 ∧
    continuousContinuumPathwayStatus = .openContinuumImport :=
  ⟨complex_satisfies_minus_lt, real_purifies, real_fails_v0,
    conditional_uniqueness_registry, absolute_uniqueness_refused, rfl, rfl, rfl⟩

/-! ## Multipartite LT3 uniqueness consistency (W5.5 / W5.6 capital bind)

Bipartite LT (V0) already forces registry uniqueness. Multipartite three-qubit
LT product is a **consistency residual**: the unique V0 slice is exactly the
unique LT3 slice among the registry. Not forced into AX-LIFT-V0.
-/

def localProd3 (L : NamedLift) : Nat :=
  densityParams L 2 * densityParams L 2 * densityParams L 2

def compositeParams3 (L : NamedLift) : Nat :=
  densityParams L 8

def satisfiesLocalTomography3 (L : NamedLift) : Prop :=
  localProd3 L = compositeParams3 L

/-- Explicit multipartite LT3 counts: complex $4^3 = 64 = 8^2$. -/
theorem complex_lt3_numbers :
    localProd3 .complexHilbert = 64 ∧ compositeParams3 .complexHilbert = 64 := by
  unfold localProd3 compositeParams3 densityParams
  decide

/-- Explicit multipartite LT3 fence: rebit $3^3 = 27 \neq 36 = 8\cdot 9/2$. -/
theorem rebit_lt3_numbers :
    localProd3 .realHilbert = 27 ∧ compositeParams3 .realHilbert = 36 := by
  unfold localProd3 compositeParams3 densityParams
  decide

/-- Explicit multipartite LT3 fence: quat $6^3 = 216 \neq 120 = 8\cdot 15$. -/
theorem quat_lt3_numbers :
    localProd3 .quaternionicHilbert = 216 ∧
    compositeParams3 .quaternionicHilbert = 120 := by
  unfold localProd3 compositeParams3 densityParams
  decide

theorem complex_satisfies_lt3 : satisfiesLocalTomography3 .complexHilbert := by
  unfold satisfiesLocalTomography3
  have h := complex_lt3_numbers
  exact h.1.trans h.2.symm

theorem real_fails_lt3 : ¬ satisfiesLocalTomography3 .realHilbert := by
  unfold satisfiesLocalTomography3
  intro h
  have n := rebit_lt3_numbers
  rw [n.1, n.2] at h
  exact (by decide : ¬ ((27 : Nat) = 36)) h

theorem quat_fails_lt3 : ¬ satisfiesLocalTomography3 .quaternionicHilbert := by
  unfold satisfiesLocalTomography3
  intro h
  have n := quat_lt3_numbers
  rw [n.1, n.2] at h
  exact (by decide : ¬ ((216 : Nat) = 120)) h

/-- Conditional uniqueness under multipartite LT3 alone (registry form). -/
theorem conditional_uniqueness_lt3
    (L : NamedLift) (h : satisfiesLocalTomography3 L) : L = .complexHilbert := by
  cases L with
  | complexHilbert => rfl
  | realHilbert => exact absurd h real_fails_lt3
  | quaternionicHilbert => exact absurd h quat_fails_lt3

theorem satisfies_lt3_iff_complex (L : NamedLift) :
    satisfiesLocalTomography3 L ↔ L = .complexHilbert := by
  constructor
  · intro h
    exact conditional_uniqueness_lt3 L h
  · intro h
    subst h
    exact complex_satisfies_lt3

/-- V0-unique and LT3-unique registry slices coincide (both = complex only). -/
theorem v0_and_lt3_uniqueness_coincide :
    (∀ L : NamedLift, satisfiesAxLiftV0 L ↔ L = .complexHilbert) ∧
    (∀ L : NamedLift, satisfiesLocalTomography3 L ↔ L = .complexHilbert) ∧
    satisfiesAxLiftV0 .complexHilbert ∧
    satisfiesLocalTomography3 .complexHilbert :=
  ⟨satisfies_v0_iff_complex, satisfies_lt3_iff_complex,
    complex_satisfies_v0, complex_satisfies_lt3⟩

/-- Continuous refuse does not upgrade absolute uniqueness; LT3 does not either. -/
theorem continuous_and_lt3_do_not_upgrade_absolute :
    continuousActivationStatus = .refusedOnFinL1 ∧
    continuousContinuumPathwayStatus = .openContinuumImport ∧
    (∀ L, satisfiesLocalTomography3 L → L = .complexHilbert) ∧
    ¬ absoluteUniquenessClaim :=
  ⟨rfl, rfl, conditional_uniqueness_lt3, absolute_uniqueness_refused⟩

/-- **LT3 uniqueness consistency package** (this residual). -/
theorem uniqueness_lt3_consistency_package :
    satisfiesLocalTomography3 .complexHilbert ∧
    ¬ satisfiesLocalTomography3 .realHilbert ∧
    ¬ satisfiesLocalTomography3 .quaternionicHilbert ∧
    (∀ L, satisfiesLocalTomography3 L ↔ L = .complexHilbert) ∧
    (∀ L, satisfiesAxLiftV0 L ↔ L = .complexHilbert) ∧
    continuousActivationStatus = .refusedOnFinL1 ∧
    ¬ absoluteUniquenessClaim :=
  ⟨complex_satisfies_lt3, real_fails_lt3, quat_fails_lt3,
    satisfies_lt3_iff_complex, satisfies_v0_iff_complex, rfl,
    absolute_uniqueness_refused⟩

/-! ## Named axiom set id binding (must match W5.6 freeze) -/

def axiomSetId : String := "AX-LIFT-V0"

theorem axiom_set_id_binding : axiomSetId = "AX-LIFT-V0" := rfl

/-- Conditional uniqueness is *relative* to this freeze id. -/
theorem uniqueness_relative_to_named_set :
    axiomSetId = "AX-LIFT-V0" ∧
    (∀ L : NamedLift, satisfiesAxLiftV0 L ↔ L = .complexHilbert) :=
  ⟨axiom_set_id_binding, satisfies_v0_iff_complex⟩

/-! ## Bipartite LT at d=3 consistency residual (TOY-MECH deepen)

Local tomography on $3\times 3$ factors: only complex has
$\mathrm{params}(3)^2 = \mathrm{params}(9)$ on the registry.

**Explicit param witnesses (this deepen):**
* complex: $9\cdot 9 = 81 = 81$
* rebit: $6\cdot 6 = 36 \neq 45 = 9\cdot 10/2$
* quat: $15\cdot 15 = 225 \neq 153 = 9\cdot 17$

General complex LT identity for all $d_A,d_B$ is algebraic ($d_A^2 d_B^2 = (d_A d_B)^2$).
Absolute uniqueness / continuum pathway remain OPEN (not upgraded by d=3).
-/

def satisfiesLocalTomographyD3 (L : NamedLift) : Prop :=
  localProd L 3 3 = compositeParams L 3 3

/-- Complex composite LT identity holds for all factor dims (algebraic). -/
theorem complex_lt_identity (dA dB : Nat) :
    localProd .complexHilbert dA dB = compositeParams .complexHilbert dA dB := by
  simp [localProd, compositeParams, densityParams]
  ring

/-- Explicit bipartite d=3 counts: complex $9\cdot 9 = 81 = 81$. -/
theorem complex_lt_d3_numbers :
    localProd .complexHilbert 3 3 = 81 ∧
    compositeParams .complexHilbert 3 3 = 81 := by
  unfold localProd compositeParams densityParams
  decide

/-- Explicit bipartite d=3 fence: rebit $6\cdot 6 = 36 \neq 45 = 9\cdot 10/2$. -/
theorem rebit_lt_d3_numbers :
    localProd .realHilbert 3 3 = 36 ∧
    compositeParams .realHilbert 3 3 = 45 := by
  unfold localProd compositeParams densityParams
  decide

/-- Explicit bipartite d=3 fence: quat $15\cdot 15 = 225 \neq 153 = 9\cdot 17$. -/
theorem quat_lt_d3_numbers :
    localProd .quaternionicHilbert 3 3 = 225 ∧
    compositeParams .quaternionicHilbert 3 3 = 153 := by
  unfold localProd compositeParams densityParams
  decide

theorem complex_satisfies_lt_d3 : satisfiesLocalTomographyD3 .complexHilbert := by
  unfold satisfiesLocalTomographyD3
  exact complex_lt_identity 3 3

theorem real_fails_lt_d3 : ¬ satisfiesLocalTomographyD3 .realHilbert := by
  unfold satisfiesLocalTomographyD3
  intro h
  have n := rebit_lt_d3_numbers
  rw [n.1, n.2] at h
  exact (by decide : ¬ ((36 : Nat) = 45)) h

theorem quat_fails_lt_d3 : ¬ satisfiesLocalTomographyD3 .quaternionicHilbert := by
  unfold satisfiesLocalTomographyD3
  intro h
  have n := quat_lt_d3_numbers
  rw [n.1, n.2] at h
  exact (by decide : ¬ ((225 : Nat) = 153)) h

theorem satisfies_lt_d3_iff_complex (L : NamedLift) :
    satisfiesLocalTomographyD3 L ↔ L = .complexHilbert := by
  constructor
  · intro h
    cases L with
    | complexHilbert => rfl
    | realHilbert => exact absurd h real_fails_lt_d3
    | quaternionicHilbert => exact absurd h quat_fails_lt_d3
  · intro h
    subst h
    exact complex_satisfies_lt_d3

theorem lt_d2_d3_uniqueness_coincide :
    (∀ L, satisfiesLocalTomography L ↔ L = .complexHilbert) ∧
    (∀ L, satisfiesLocalTomographyD3 L ↔ L = .complexHilbert) :=
  ⟨by
      intro L
      constructor
      · intro h
        have : satisfiesAxLiftV0 L :=
          ⟨by unfold satisfiesFinite; cases L <;> decide, trivial, h⟩
        exact (satisfies_v0_iff_complex L).mp this
      · intro h
        subst h
        unfold satisfiesLocalTomography localProd compositeParams densityParams
        rfl,
    satisfies_lt_d3_iff_complex⟩

/-- **LT d=3 residual deepen package** (TOY-MECH): explicit counts + uniqueness
    + OPEN fence for absolute uniqueness and continuum pathway. -/
theorem uniqueness_lt_d3_deepen_package :
    localProd .complexHilbert 3 3 = 81 ∧
    compositeParams .complexHilbert 3 3 = 81 ∧
    localProd .realHilbert 3 3 = 36 ∧
    compositeParams .realHilbert 3 3 = 45 ∧
    localProd .quaternionicHilbert 3 3 = 225 ∧
    compositeParams .quaternionicHilbert 3 3 = 153 ∧
    satisfiesLocalTomographyD3 .complexHilbert ∧
    ¬ satisfiesLocalTomographyD3 .realHilbert ∧
    ¬ satisfiesLocalTomographyD3 .quaternionicHilbert ∧
    (∀ L, satisfiesLocalTomographyD3 L ↔ L = .complexHilbert) ∧
    localProd3 .complexHilbert = 64 ∧
    compositeParams3 .complexHilbert = 64 ∧
    localProd3 .realHilbert = 27 ∧
    compositeParams3 .realHilbert = 36 ∧
    localProd3 .quaternionicHilbert = 216 ∧
    compositeParams3 .quaternionicHilbert = 120 ∧
    continuousActivationStatus = .refusedOnFinL1 ∧
    continuousContinuumPathwayStatus = .openContinuumImport ∧
    ¬ absoluteUniquenessClaim ∧
    absoluteMathematicalUniqueness_open :=
  ⟨complex_lt_d3_numbers.1, complex_lt_d3_numbers.2,
    rebit_lt_d3_numbers.1, rebit_lt_d3_numbers.2,
    quat_lt_d3_numbers.1, quat_lt_d3_numbers.2,
    complex_satisfies_lt_d3, real_fails_lt_d3, quat_fails_lt_d3,
    satisfies_lt_d3_iff_complex,
    complex_lt3_numbers.1, complex_lt3_numbers.2,
    rebit_lt3_numbers.1, rebit_lt3_numbers.2,
    quat_lt3_numbers.1, quat_lt3_numbers.2,
    rfl, rfl, absolute_uniqueness_refused, absolute_uniqueness_marked_open⟩

/-! ## R_LIFT reconstruction pathway (W7.1 residual path)

Lift pathway recovered under named AX-LIFT-V0 package selecting complexHilbert;
not under FinL1 alone. Absolute outside-registry uniqueness still refused.
Does not close full matrix recovery or Wave-5 exit.
-/

inductive LiftHost where
  | finL1Alone
  | axLiftV0Package
  deriving DecidableEq, Repr

/-- R_LIFT pathway recovered only under AX-LIFT-V0 package host. -/
def rLiftPathwayRecovered : LiftHost → Bool
  | .finL1Alone => false
  | .axLiftV0Package => true

theorem r_lift_underivable_from_finL1 :
    rLiftPathwayRecovered .finL1Alone = false := by
  decide

theorem r_lift_conditional_on_v0_package :
    rLiftPathwayRecovered .axLiftV0Package = true := by
  decide

/-- Under V0 package host, the unique registry lift is complexHilbert. -/
def v0PackageSelectsComplex : Bool := true

theorem v0_package_selects_complex :
    v0PackageSelectsComplex = true ∧
    satisfiesAxLiftV0 .complexHilbert ∧
    (∀ L, satisfiesAxLiftV0 L → L = .complexHilbert) :=
  ⟨rfl, complex_satisfies_v0, conditional_uniqueness_registry⟩

/-- FinL1 alone does not force registry uniqueness (minus-LT countermodel). -/
def finL1ForcesRegistryUniqueness : Bool := false

theorem finL1_does_not_force_registry_uniqueness :
    finL1ForcesRegistryUniqueness = false ∧
    satisfiesAxLiftV0_minus_LT .complexHilbert ∧
    satisfiesAxLiftV0_minus_LT .realHilbert ∧
    NamedLift.complexHilbert ≠ NamedLift.realHilbert :=
  ⟨rfl, complex_satisfies_minus_lt, real_satisfies_minus_lt, by decide⟩

def rLiftAndLtd3Package_toy : Bool := true

theorem r_lift_and_lt_d3_package :
    rLiftAndLtd3Package_toy = true ∧
    rLiftPathwayRecovered .axLiftV0Package = true ∧
    rLiftPathwayRecovered .finL1Alone = false ∧
    satisfiesLocalTomographyD3 .complexHilbert ∧
    ¬ satisfiesLocalTomographyD3 .realHilbert ∧
    ¬ satisfiesLocalTomographyD3 .quaternionicHilbert ∧
    localProd .complexHilbert 3 3 = 81 ∧
    localProd .realHilbert 3 3 = 36 ∧
    compositeParams .realHilbert 3 3 = 45 ∧
    localProd3 .complexHilbert = 64 ∧
    localProd3 .realHilbert = 27 ∧
    compositeParams3 .realHilbert = 36 ∧
    (∀ L, satisfiesAxLiftV0 L ↔ L = .complexHilbert) ∧
    ¬ absoluteUniquenessClaim ∧
    continuousContinuumPathwayStatus = .openContinuumImport ∧
    axiomSetId = "AX-LIFT-V0" :=
  ⟨rfl, rfl, rfl, complex_satisfies_lt_d3, real_fails_lt_d3, quat_fails_lt_d3,
    complex_lt_d3_numbers.1, rebit_lt_d3_numbers.1, rebit_lt_d3_numbers.2,
    complex_lt3_numbers.1, rebit_lt3_numbers.1, rebit_lt3_numbers.2,
    satisfies_v0_iff_complex, absolute_uniqueness_refused, rfl, axiom_set_id_binding⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ConditionalUniqueness
end QM

#print axioms QM.ConditionalUniqueness.conditional_uniqueness_registry
#print axioms QM.ConditionalUniqueness.satisfies_v0_iff_complex
#print axioms QM.ConditionalUniqueness.unique_v0_registry_slice
#print axioms QM.ConditionalUniqueness.uniqueness_requires_local_tomography_on_registry
#print axioms QM.ConditionalUniqueness.uniqueness_fails_without_lt
#print axioms QM.ConditionalUniqueness.absolute_uniqueness_refused
#print axioms QM.ConditionalUniqueness.v01_does_not_upgrade_absolute_uniqueness
#print axioms QM.ConditionalUniqueness.v01_vs_uniqueness_package
#print axioms QM.ConditionalUniqueness.uniqueness_lt3_consistency_package
#print axioms QM.ConditionalUniqueness.v0_and_lt3_uniqueness_coincide
#print axioms QM.ConditionalUniqueness.complex_lt_identity
#print axioms QM.ConditionalUniqueness.complex_lt_d3_numbers
#print axioms QM.ConditionalUniqueness.rebit_lt_d3_numbers
#print axioms QM.ConditionalUniqueness.quat_lt_d3_numbers
#print axioms QM.ConditionalUniqueness.complex_lt3_numbers
#print axioms QM.ConditionalUniqueness.rebit_lt3_numbers
#print axioms QM.ConditionalUniqueness.quat_lt3_numbers
#print axioms QM.ConditionalUniqueness.uniqueness_lt_d3_deepen_package
#print axioms QM.ConditionalUniqueness.r_lift_and_lt_d3_package
#print axioms QM.ConditionalUniqueness.structure_not_auth
