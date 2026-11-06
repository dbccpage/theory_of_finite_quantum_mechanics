/-
  WitnessedDifference/WdpBatch12.lean

  Constructive mechanization of Batch 12 derivations (5 nodes):
  1. PGW-C1-ENGINE-CLASS-144 (GENESIS, TFQ-0474)
  2. PG-WDP-GENESIS-BRIDGE-OBLIGATIONS (WDP, TFQ-0343)
  3. TFQ-0385 (GENESIS, TFQ-0385)
  4. PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR (WDP, TFQ-0567)
  5. PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION (WDP, TFQ-0569)

  All proofs are constructive (zero `sorry`, zero `Classical.choice`).
-/
import WitnessedDifference.WdpBatch11

namespace WitnessedDifference.WdpBatch12

open WitnessedDifference.WdpBatch9
open WitnessedDifference.WdpBatch10
open WitnessedDifference.WdpBatch11

/-! ## 1. PGW-C1-ENGINE-CLASS-144 (GENESIS) -/

/-- Continuation mode in `Challenge 3` (`0 = HALT`, `1 = growth`, `2 = switch`, `3 = growth + switch`). -/
inductive EngineCont where
  | halt
  | growth
  | switch
  | growthSwitch
  deriving DecidableEq, Repr

def allEngineConts : List EngineCont :=
  [.halt, .growth, .switch, .growthSwitch]

/-- An engine declaration in continuation attempt one (`Challenge 3`):
    - `rule : StakeMenuRule` (one of the 9 stake rules `E1..E9`, read in the state's mode)
    - `measure : Bool` (`false` = `mu1`, `true` = `mu2`)
    - `validity : Bool` (`false` = `V1`, `true` = `V2`)
    - `cont : EngineCont` (`halt`, `growth`, `switch`, `growthSwitch`)
    Total combinations: `9 * 2 * 2 * 4 = 144` (`108` without `.halt`). -/
structure EngineDecl where
  rule : StakeMenuRule
  measure : Bool
  validity : Bool
  cont : EngineCont
  deriving DecidableEq, Repr

/-- Number of observables referenced by each of the 9 stake rules `E1..E9`. -/
def ruleObsCount : StakeMenuRule → Nat
  | .E1 | .E2 | .E3 | .E4 | .E5 | .E7 => 1
  | .E6 | .E8 | .E9 => 2

/-- Number of validity clauses (`1` for `V1`, `2` for `V2`). -/
def validityClauseCount (v : Bool) : Nat :=
  if v then 2 else 1

/-- Number of continuation capabilities when growth counts as 1 capability. -/
def contCapCount1 : EngineCont → Nat
  | .halt => 0
  | .growth => 1
  | .switch => 1
  | .growthSwitch => 2

/-- Number of continuation capabilities when growth counts as 2 capabilities. -/
def contCapCount2 : EngineCont → Nat
  | .halt => 0
  | .growth => 2
  | .switch => 1
  | .growthSwitch => 3

/-- Total capability count under reading 1 (3 skeleton + rule observables + 1 measure + validity + continuation). -/
def engineCapCount1 (e : EngineDecl) : Nat :=
  3 + ruleObsCount e.rule + 1 + validityClauseCount e.validity + contCapCount1 e.cont

/-- Total capability count under reading 2 (growth counted as 2 capabilities). -/
def engineCapCount2 (e : EngineDecl) : Nat :=
  3 + ruleObsCount e.rule + 1 + validityClauseCount e.validity + contCapCount2 e.cont

/-- Every engine declaration has capability count between 6 and 10 under reading 1,
    and between 7 and 10 whenever its continuation is non-HALT (`e.cont ≠ .halt`). -/
theorem engineCapCount1_bounds (e : EngineDecl) :
    (6 ≤ engineCapCount1 e ∧ engineCapCount1 e ≤ 10) ∧
    (e.cont ≠ .halt → 7 ≤ engineCapCount1 e) := by
  rcases e with ⟨r, m, v, c⟩
  cases r <;> cases m <;> cases v <;> cases c <;> decide

/-- Complete enumeration of all 144 engine declarations. -/
def allEngines : List EngineDecl :=
  allStakeMenuRules.flatMap (fun r =>
    [false, true].flatMap (fun m =>
      [false, true].flatMap (fun v =>
        allEngineConts.map (fun c =>
          ⟨r, m, v, c⟩))))

/-- Seed-literal subclass: the 108 engines whose continuation is not `HALT`. -/
def seedLiteralEngines : List EngineDecl :=
  allEngines.filter (fun e => e.cont != .halt)

/-- Continuation inclusion order. -/
def contSubsetBool : EngineCont → EngineCont → Bool
  | .halt, _ => true
  | .growth, .growth | .growth, .growthSwitch => true
  | .switch, .switch | .switch, .growthSwitch => true
  | .growthSwitch, .growthSwitch => true
  | _, _ => false

/-- Capability inclusion order between two engine declarations:
    `e₁` is included in `e₂` only when they use the same stake rule and measure,
    `e₁`'s validity clauses are a subset of `e₂`'s (`e₁.validity → e₂.validity`),
    and `e₁`'s continuation is a subset of `e₂`'s. -/
def engineDeclSubsetBool (e₁ e₂ : EngineDecl) : Bool :=
  (e₁.rule == e₂.rule) &&
  (e₁.measure == e₂.measure) &&
  (!e₁.validity || e₂.validity) &&
  contSubsetBool e₁.cont e₂.cont

/-- No engine declaration is included in its opposite-measure partner, so no member is initial
    in any class containing both measures (`no_initial`). -/
theorem engine_not_subset_opposite_measure (e : EngineDecl) :
    engineDeclSubsetBool e { e with measure := !e.measure } = false := by
  cases h : e.measure <;> simp [engineDeclSubsetBool, h]

/-- Minimal engine with `E4` (demands at `baseR2L`), minimal engine with `E1` (demand-free at `baseR2L`),
    and minimal non-HALT engine (`seedLiteralMinEngine`, capability count 7). -/
def minEngineE4 : EngineDecl := ⟨.E4, false, false, .halt⟩
def minEngineE1 : EngineDecl := ⟨.E1, false, false, .halt⟩
def seedLiteralMinEngine : EngineDecl := ⟨.E1, false, false, .growth⟩

set_option maxRecDepth 200000 in
/-- Representative theorem for `PGW-C1-ENGINE-CLASS-144`:
    1. `allEngines` has 144 members, and `seedLiteralEngines` has 108 members.
    2. Under reading 1, every member `e : EngineDecl` has `6 ≤ engineCapCount1 e ≤ 10`
       (and `7 ≤ engineCapCount1 e` when `e.cont ≠ .halt`), so no member is a single declaration.
    3. Count-minimal members `minEngineE4` and `minEngineE1` both attain capability count 6 in
       `allEngines`, while `seedLiteralMinEngine` attains capability count 7 in `seedLiteralEngines`.
    4. No member is initial under declaration inclusion (`engine_not_subset_opposite_measure`).
    5. At `baseR2L` (reading L's genesis), `allApartStake` (representing `E4`'s root demand)
       has a standing demand whereas `freeStake` (representing `E1`'s root state) is demand-free
       (`minima_differ_at_genL`). -/
theorem c1_engine_class_144_and_no_initial :
    allEngines.length = 144 ∧
    seedLiteralEngines.length = 108 ∧
    (∀ e : EngineDecl,
      (6 ≤ engineCapCount1 e ∧ engineCapCount1 e ≤ 10) ∧
      (e.cont ≠ .halt → 7 ≤ engineCapCount1 e)) ∧
    engineCapCount1 minEngineE4 = 6 ∧
    engineCapCount1 minEngineE1 = 6 ∧
    engineCapCount1 seedLiteralMinEngine = 7 ∧
    seedLiteralMinEngine.cont ≠ .halt ∧
    (∀ e : EngineDecl, engineDeclSubsetBool e { e with measure := !e.measure } = false) ∧
    hasDemandBool allApartStake baseR2L = true ∧
    hasDemandBool freeStake baseR2L = false := by
  refine ⟨by decide, by decide, engineCapCount1_bounds, by decide, by decide,
    by decide, by decide, engine_not_subset_opposite_measure, by decide, by decide⟩

/-! ## 2. PG-WDP-GENESIS-BRIDGE-OBLIGATIONS (WDP) -/

/-- A finite directed window on `Fin m`. -/
structure BridgeWindow (m : Nat) where
  adj : Fin m → Fin m → Bool

/-- Symmetrised adjacency (`pairDefect` candidate map). -/
def bridgePairDefect {m : Nat} (w : BridgeWindow m) (u v : Fin m) : Bool :=
  w.adj u v || w.adj v u

/-- Presence of a directed step `u → v`. -/
def BridgeDirectedStep {m : Nat} (w : BridgeWindow m) (u v : Fin m) : Prop :=
  w.adj u v = true

/-- A Bool-valued map `φ` is a directed-step certificate when it matches `BridgeDirectedStep` on all windows. -/
def IsBridgeDirectedStepCert {m : Nat} (φ : BridgeWindow m → Fin m → Fin m → Bool) : Prop :=
  ∀ w u v, BridgeDirectedStep w u v ↔ φ w u v = true

/-- `bridgePairDefect` is false iff both directed adjacencies are false. -/
theorem bridgePairDefect_false_iff {m : Nat} (w : BridgeWindow m) (u v : Fin m) :
    bridgePairDefect w u v = false ↔ w.adj u v = false ∧ w.adj v u = false := by
  unfold bridgePairDefect
  cases w.adj u v <;> cases w.adj v u <;> decide

/-- Identity adjacency map is a directed-step certificate for every finite window size `m`. -/
def bridgeIdAdj {m : Nat} (w : BridgeWindow m) (u v : Fin m) : Bool :=
  w.adj u v

theorem bridgeIdAdj_is_cert {m : Nat} :
    IsBridgeDirectedStepCert (m := m) bridgeIdAdj := by
  intro w u v
  exact Iff.rfl

/-- Opposite single-edge windows on 2 vertices. -/
def bridgeEdge01 : BridgeWindow 2 := ⟨fun u v => u.val == 0 && v.val == 1⟩
def bridgeEdge10 : BridgeWindow 2 := ⟨fun u v => u.val == 1 && v.val == 0⟩

/-- Symmetrised adjacency is not a directed-step certificate on 2 vertices. -/
theorem bridgePairDefect_not_directed_step_cert :
    ¬ IsBridgeDirectedStepCert (m := 2) bridgePairDefect := by
  intro h
  have h10 : bridgePairDefect bridgeEdge10 0 1 = true := by decide
  have hstep : BridgeDirectedStep bridgeEdge10 0 1 := (h bridgeEdge10 0 1).mpr h10
  have hfalse : bridgeEdge10.adj 0 1 = false := by decide
  unfold BridgeDirectedStep at hstep
  rw [hfalse] at hstep
  cases hstep

/-- Two-event causal diamond price structure (`GEN-WDP-42`):
    costs `cA_root, cB_after_A` along order `A → B` vs `cB_root, cA_after_B` along order `B → A`. -/
structure CausalDiamondPrice where
  cA_root : Int
  cB_after_A : Int
  cB_root : Int
  cA_after_B : Int
  deriving DecidableEq, Repr

/-- Price curl around the two-event diamond. -/
def diamondPriceCurl (d : CausalDiamondPrice) : Int :=
  (d.cA_root + d.cB_after_A) - (d.cB_root + d.cA_after_B)

/-- Schedule totals agree iff the diamond price curl vanishes (`GEN-WDP-42`). -/
theorem diamond_price_curl_zero_iff (d : CausalDiamondPrice) :
    diamondPriceCurl d = 0 ↔ d.cA_root + d.cB_after_A = d.cB_root + d.cA_after_B := by
  unfold diamondPriceCurl
  constructor <;> intro h <;> omega

/-- Representative theorem for `PG-WDP-GENESIS-BRIDGE-OBLIGATIONS` (scoped finite slice):
    combines the symmetrised-adjacency characterization (`bridgePairDefect_false_iff`),
    its non-reflection on 2 vertices (`bridgePairDefect_not_directed_step_cert`),
    existence of the identity directed-step certificate (`bridgeIdAdj_is_cert`),
    the `GEN-WDP-46` observer completion dimension identity (`dimH + (dimK - dimH) = dimK`),
    and the `GEN-WDP-42` causal-diamond price-curl criterion (`diamond_price_curl_zero_iff`). -/
theorem pg_wdp_genesis_bridge_scoped_finite_slice :
    (∀ (m : Nat) (w : BridgeWindow m) (u v : Fin m),
      bridgePairDefect w u v = false ↔ w.adj u v = false ∧ w.adj v u = false) ∧
    (∀ m : Nat, IsBridgeDirectedStepCert (m := m) bridgeIdAdj) ∧
    (¬ IsBridgeDirectedStepCert (m := 2) bridgePairDefect) ∧
    (∀ dimH dimK : Nat, dimH ≤ dimK → dimH + (dimK - dimH) = dimK) ∧
    (∀ d : CausalDiamondPrice,
      diamondPriceCurl d = 0 ↔ d.cA_root + d.cB_after_A = d.cB_root + d.cA_after_B) := by
  refine ⟨fun _ w u v => bridgePairDefect_false_iff w u v,
    fun _ => bridgeIdAdj_is_cert,
    bridgePairDefect_not_directed_step_cert,
    fun _ _ hle => by omega,
    diamond_price_curl_zero_iff⟩

/-! ## 3. TFQ-0385 (GENESIS) -/

/-- The regime reached after admitting two data, one unary form, and one unary instance on datum 0. -/
def regimeBeforeUniformRule : RungRegime :=
  ⟨2, [1], [(0, [0])], [], []⟩

/-- The regime reached after subsequently admitting the uniform rule `.admitRuleAll 0`. -/
def regimeAfterUniformRule : RungRegime :=
  ⟨2, [1], [(0, [0])], [0], []⟩

/-- Representative theorem for `TFQ-0385` (`WDP-P000-017`):
    1. Replaying `twoNessFromEmpty4` from `genesisRegime` reaches `regimeBeforeUniformRule`,
       where datum `0` and datum `1` are separated (`unarySeparatedBool = true`, `holdsTwoBool = true`)
       and `rungElems = 4`.
    2. Admitting `.admitRuleAll 0` from `regimeBeforeUniformRule` reaches `regimeAfterUniformRule`,
       where the prior separation between datum `0` and datum `1` is erased (`unarySeparatedBool = false`,
       `holdsTwoBool = false`), while `rungElems` increases from `4` to `5`.
    3. By the no-return element-count monotonicity (`replayRung_elems_le`), no continuation history
       `hCont` from `regimeAfterUniformRule` can ever return to `regimeBeforeUniformRule`. -/
theorem tfq_0385_uniform_rule_erases_separation_and_no_return :
    replayRung twoNessFromEmpty4 genesisRegime = some regimeBeforeUniformRule ∧
    unarySeparatedBool regimeBeforeUniformRule 0 1 = true ∧
    holdsTwoBool regimeBeforeUniformRule = true ∧
    rungElems regimeBeforeUniformRule = 4 ∧
    stepRung regimeBeforeUniformRule (.admitRuleAll 0) = some regimeAfterUniformRule ∧
    unarySeparatedBool regimeAfterUniformRule 0 1 = false ∧
    holdsTwoBool regimeAfterUniformRule = false ∧
    rungElems regimeAfterUniformRule = 5 ∧
    (∀ hCont : List RungEvent,
      replayRung hCont regimeAfterUniformRule ≠ some regimeBeforeUniformRule) := by
  refine ⟨by decide, by decide, by decide, by decide, by decide,
    by decide, by decide, by decide, ?_⟩
  intro hCont hrep
  have hle : rungElems regimeAfterUniformRule ≤ rungElems regimeBeforeUniformRule :=
    replayRung_elems_le hCont hrep
  have h5 : rungElems regimeAfterUniformRule = 5 := by decide
  have h4 : rungElems regimeBeforeUniformRule = 4 := by decide
  omega

/-! ## 4. PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR (WDP) -/

/-- A finite source transition, cost, and future-question system. -/
structure FiniteBridgeSystem (S : Type) where
  step : S → S → Prop
  cost : S → Nat
  question : S → Prop

/-- A map `f : S → T` between finite bridge systems preserves and reflects transitions,
    costs, and future questions (`GEN-WDP-O02` scoped finite criterion). -/
def PreservesAndReflectsBridge {S T : Type}
    (sysS : FiniteBridgeSystem S) (sysT : FiniteBridgeSystem T) (f : S → T) : Prop :=
  (∀ s₁ s₂ : S, sysS.step s₁ s₂ ↔ sysT.step (f s₁) (f s₂)) ∧
  (∀ s : S, sysT.cost (f s) = sysS.cost s) ∧
  (∀ s : S, sysS.question s ↔ sysT.question (f s))

/-- Preservation and reflection maps compose cleanly across bridge stages. -/
theorem o02_preservation_reflection_comp {S T U : Type}
    (sysS : FiniteBridgeSystem S) (sysT : FiniteBridgeSystem T) (sysU : FiniteBridgeSystem U)
    {f : S → T} {g : T → U}
    (hf : PreservesAndReflectsBridge sysS sysT f)
    (hg : PreservesAndReflectsBridge sysT sysU g) :
    PreservesAndReflectsBridge sysS sysU (fun s => g (f s)) := by
  rcases hf with ⟨hstepF, hcostF, hqF⟩
  rcases hg with ⟨hstepG, hcostG, hqG⟩
  refine ⟨fun s₁ s₂ => (hstepF s₁ s₂).trans (hstepG (f s₁) (f s₂)),
    fun s => (hcostG (f s)).trans (hcostF s),
    fun s => (hqF s).trans (hqG (f s))⟩

/-- Any preservation-and-reflection map is automatically fiber-constant on costs and questions,
    so any candidate map `f` that identifies two states `s₁, s₂` with different costs or different
    future-question answers cannot satisfy `PreservesAndReflectsBridge`. -/
theorem o02_collision_refutes_preservation_reflection {S T : Type}
    (sysS : FiniteBridgeSystem S) (sysT : FiniteBridgeSystem T) (f : S → T)
    (hPR : PreservesAndReflectsBridge sysS sysT f)
    {s₁ s₂ : S} (hcoll : f s₁ = f s₂) :
    sysS.cost s₁ = sysS.cost s₂ ∧ (sysS.question s₁ ↔ sysS.question s₂) := by
  rcases hPR with ⟨_, hcost, hq⟩
  have hc : sysS.cost s₁ = sysS.cost s₂ := by
    rw [← hcost s₁, ← hcost s₂, hcoll]
  have hqq : sysS.question s₁ ↔ sysS.question s₂ := by
    rw [hq s₁, hq s₂, hcoll]
  exact ⟨hc, hqq⟩

/-- Representative theorem for `PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR`:
    combines composition of preservation/reflection bridge maps (`o02_preservation_reflection_comp`),
    the fiber-collision refutation criterion (`o02_collision_refutes_preservation_reflection`),
    and the 2-vertex orientation-swap countermodel (`bridgePairDefect_not_directed_step_cert`). -/
theorem wdp_bridge_o02_scoped_preservation_reflection_characterization :
    (∀ (S T U : Type) (sysS : FiniteBridgeSystem S) (sysT : FiniteBridgeSystem T)
       (sysU : FiniteBridgeSystem U) (f : S → T) (g : T → U),
      PreservesAndReflectsBridge sysS sysT f →
      PreservesAndReflectsBridge sysT sysU g →
      PreservesAndReflectsBridge sysS sysU (fun s => g (f s))) ∧
    (∀ (S T : Type) (sysS : FiniteBridgeSystem S) (sysT : FiniteBridgeSystem T) (f : S → T),
      PreservesAndReflectsBridge sysS sysT f →
      ∀ s₁ s₂ : S, f s₁ = f s₂ →
        sysS.cost s₁ = sysS.cost s₂ ∧ (sysS.question s₁ ↔ sysS.question s₂)) ∧
    (¬ IsBridgeDirectedStepCert (m := 2) bridgePairDefect) :=
  ⟨fun _ _ _ sysS sysT sysU _ _ hf hg => o02_preservation_reflection_comp sysS sysT sysU hf hg,
   fun _ _ sysS sysT f hPR _ _ hcoll => o02_collision_refutes_preservation_reflection sysS sysT f hPR hcoll,
   bridgePairDefect_not_directed_step_cert⟩

/-! ## 5. PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION (WDP) -/

/-- Exact Gaussian integer `a + b i` for constructive 2x2 state/effect factor readout. -/
structure GInt12 where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def gintAdd (z w : GInt12) : GInt12 :=
  ⟨z.re + w.re, z.im + w.im⟩

def gintConj (z : GInt12) : GInt12 :=
  ⟨z.re, -z.im⟩

def gintMul (z w : GInt12) : GInt12 :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

def gintNormSq (z : GInt12) : Int :=
  z.re * z.re + z.im * z.im

theorem int_sq_nonneg (x : Int) : 0 ≤ x * x := by
  cases x with
  | ofNat n =>
    exact Int.ofNat_le.mpr (Nat.zero_le (n * n))
  | negSucc n =>
    exact Int.ofNat_le.mpr (Nat.zero_le ((n + 1) * (n + 1)))

theorem gintNormSq_nonneg (z : GInt12) : 0 ≤ gintNormSq z := by
  unfold gintNormSq
  have h1 := int_sq_nonneg z.re
  have h2 := int_sq_nonneg z.im
  omega

/-- Exact 2x2 matrix over `GInt12`. -/
structure GMat2 where
  a00 : GInt12
  a01 : GInt12
  a10 : GInt12
  a11 : GInt12
  deriving DecidableEq, Repr

def gmatZero : GMat2 := ⟨⟨0, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩⟩
def gmatId : GMat2 := ⟨⟨1, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩, ⟨1, 0⟩⟩

def gmatAdd (A B : GMat2) : GMat2 :=
  ⟨gintAdd A.a00 B.a00, gintAdd A.a01 B.a01, gintAdd A.a10 B.a10, gintAdd A.a11 B.a11⟩

def gmatDagger (A : GMat2) : GMat2 :=
  ⟨gintConj A.a00, gintConj A.a10, gintConj A.a01, gintConj A.a11⟩

def gmatMul (A B : GMat2) : GMat2 :=
  ⟨gintAdd (gintMul A.a00 B.a00) (gintMul A.a01 B.a10),
   gintAdd (gintMul A.a00 B.a01) (gintMul A.a01 B.a11),
   gintAdd (gintMul A.a10 B.a00) (gintMul A.a11 B.a10),
   gintAdd (gintMul A.a10 B.a01) (gintMul A.a11 B.a11)⟩

def gmatGram (A : GMat2) : GMat2 :=
  gmatMul (gmatDagger A) A

def gmatTrace (A : GMat2) : GInt12 :=
  gintAdd A.a00 A.a11

def gmatFrobSq (A : GMat2) : Int :=
  gintNormSq A.a00 + gintNormSq A.a01 + gintNormSq A.a10 + gintNormSq A.a11

/-- Frobenius norm squared of any `GMat2` is nonnegative. -/
theorem gmatFrobSq_nonneg (A : GMat2) : 0 ≤ gmatFrobSq A := by
  unfold gmatFrobSq
  have h00 := gintNormSq_nonneg A.a00
  have h01 := gintNormSq_nonneg A.a01
  have h10 := gintNormSq_nonneg A.a10
  have h11 := gintNormSq_nonneg A.a11
  omega

theorem gintMul_conj_left_re (z : GInt12) :
    (gintMul (gintConj z) z).re = gintNormSq z := by
  rcases z with ⟨r, i⟩
  simp only [gintMul, gintConj, gintNormSq, Int.neg_mul]
  omega

/-- Exact Born Gram-trace numerator identity: `Re(Tr((C B†)† (C B†))) = ‖C B†‖²_F`. -/
theorem gmat_born_numerator_identity (B C : GMat2) :
    (gmatTrace (gmatGram (gmatMul C (gmatDagger B)))).re =
      gmatFrobSq (gmatMul C (gmatDagger B)) := by
  rcases gmatMul C (gmatDagger B) with ⟨a00, a01, a10, a11⟩
  simp only [gmatTrace, gmatGram, gmatMul, gmatDagger, gintAdd, gmatFrobSq,
    gintMul_conj_left_re]
  omega

/-- Computational basis state `|0⟩⟨0|` factor, superposition `|+⟩` factor, and `Z`-basis effect factors. -/
def gmatBasis0 : GMat2 := ⟨⟨1, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩⟩
def gmatPlus : GMat2 := ⟨⟨1, 0⟩, ⟨1, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩⟩
def gmatAccept0 : GMat2 := ⟨⟨1, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩⟩
def gmatReject0 : GMat2 := ⟨⟨0, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩, ⟨1, 0⟩⟩
def gmatAcceptPlus : GMat2 := ⟨⟨1, 0⟩, ⟨1, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩⟩

/-- Classical diagonal-projection readout numerator: ignores off-diagonal coherence `a01, a10`
    before computing the Born numerator. -/
def diagProjection (A : GMat2) : GMat2 :=
  ⟨A.a00, ⟨0, 0⟩, ⟨0, 0⟩, A.a11⟩

def classicalDiagNumerator (B C : GMat2) : Int :=
  gmatFrobSq (gmatMul C (gmatDagger (diagProjection B)))

/-- Representative theorem for `PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION`:
    1. Every `GMat2` has nonnegative Frobenius norm squared (`gmatFrobSq_nonneg`), and the Born
       Gram-trace numerator factors as `Re(Tr((C B†)†(C B†))) = ‖C B†‖²_F` (`gmat_born_numerator_identity`).
    2. For the complete binary effect `(gmatAccept0, gmatReject0)`, the Born numerators partition
       `gmatFrobSq B` on both `gmatBasis0` (`1 + 0 = 1`) and `gmatPlus` (`1 + 1 = 2`).
    3. The classical diagonal-projection readout `classicalDiagNumerator` agrees with the Born
       numerator on `gmatBasis0` and `(gmatAccept0, gmatReject0)`, yet differs from the Born
       numerator on the coherent superposition `gmatPlus` paired with `gmatAcceptPlus` (`1 ≠ 4`),
       exhibiting an operational countermodel unless off-diagonal coherence is enforced. -/
theorem wdp_bridge_o04_scoped_operational_readout_and_countermodel :
    (∀ A : GMat2, 0 ≤ gmatFrobSq A) ∧
    (∀ B C : GMat2,
      (gmatTrace (gmatGram (gmatMul C (gmatDagger B)))).re =
        gmatFrobSq (gmatMul C (gmatDagger B))) ∧
    gmatAdd (gmatGram gmatAccept0) (gmatGram gmatReject0) = gmatId ∧
    gmatFrobSq (gmatMul gmatAccept0 (gmatDagger gmatBasis0)) = 1 ∧
    gmatFrobSq (gmatMul gmatReject0 (gmatDagger gmatBasis0)) = 0 ∧
    gmatFrobSq (gmatMul gmatAccept0 (gmatDagger gmatPlus)) = 1 ∧
    gmatFrobSq (gmatMul gmatReject0 (gmatDagger gmatPlus)) = 1 ∧
    classicalDiagNumerator gmatBasis0 gmatAccept0 =
      gmatFrobSq (gmatMul gmatAccept0 (gmatDagger gmatBasis0)) ∧
    classicalDiagNumerator gmatPlus gmatAcceptPlus = 1 ∧
    gmatFrobSq (gmatMul gmatAcceptPlus (gmatDagger gmatPlus)) = 4 := by
  refine ⟨gmatFrobSq_nonneg, gmat_born_numerator_identity,
    by decide, by decide, by decide, by decide, by decide,
    by decide, by decide, by decide⟩

end WitnessedDifference.WdpBatch12
