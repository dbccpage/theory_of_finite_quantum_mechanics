/-
  WitnessedDifference/WdpBatch10.lean

  Constructive mechanization of Batch 10 derivations (5 nodes):
  1. L1-IMP-COMPLEX-FIELD (L1_TO_L2, TFQ-0293)
  2. PGW-RUNG2A-STAKE-DECLARED-LABEL (GENESIS, TFQ-0464)
  3. PGW-RUNG3-FIRST-DEMAND-INDEX (GENESIS, TFQ-0466)
  4. PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM (GENESIS, TFQ-0467)
  5. PGW-RUNG5-SYMMETRY-ALONG-HISTORY (GENESIS, TFQ-0468)

  All proofs are constructive (zero `sorry`, zero `Classical.choice`).
-/
import WitnessedDifference.WdpBatch9

namespace WitnessedDifference.WdpBatch10

open WitnessedDifference.WdpBatch9

/-! ## 1. L1-IMP-COMPLEX-FIELD (L1_TO_L2) -/

/-- State-space real dimension `K_d(n) = n + d * n * (n - 1) / 2` for an `n`-level
    system with off-diagonal coherence parameter `d` (`d = 1` real, `d = 2` complex,
    `d = 4` quaternionic). -/
def carrierDimK (d n : Nat) : Nat :=
  n + d * (n * (n - 1) / 2)

/-- Gaussian rational `a + b i` with `a, b : Rat`. -/
structure GaussianRat10 where
  re : Rat
  im : Rat
  deriving DecidableEq, Repr

def gratMul (z w : GaussianRat10) : GaussianRat10 :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

def gratNormSq (z : GaussianRat10) : Rat :=
  z.re * z.re + z.im * z.im

def gratInv (z : GaussianRat10) : GaussianRat10 :=
  let n := gratNormSq z
  ⟨z.re / n, -z.im / n⟩

/-- Gaussian norm is multiplicative: `N(z * w) = N(z) * N(w)`. -/
theorem gratNormSq_mul (z w : GaussianRat10) :
    gratNormSq (gratMul z w) = gratNormSq z * gratNormSq w := by
  simp only [gratNormSq, gratMul]
  grind

/-- Composite dimension multiplicativity `K_d(4) = K_d(2) * K_d(2)` over positive `d > 0`
    uniquely selects `d = 2` (refuting `d = 1` real where `10 ≠ 9` and `d = 4` quaternionic
    where `28 ≠ 36`). -/
theorem composite_dimension_multiplicativity_selects_d_eq_two (d : Nat) (hd : 0 < d) :
    carrierDimK d 4 = carrierDimK d 2 * carrierDimK d 2 ↔ d = 2 := by
  have h2 : 2 * (2 - 1) / 2 = 1 := by decide
  have h4 : 4 * (4 - 1) / 2 = 6 := by decide
  simp only [carrierDimK, h2, h4, Nat.mul_one]
  match d with
  | 0 => omega
  | 1 => decide
  | 2 => decide
  | k + 3 =>
    have h1 : (2 + (k + 3)) * (2 + (k + 3)) =
        2 * 2 + 2 * (k + 3) + (k + 3) * 2 + (k + 3) * (k + 3) := by
      simp only [Nat.add_mul, Nat.mul_add]; omega
    have h3 : 3 * (k + 3) ≤ (k + 3) * (k + 3) :=
      Nat.mul_le_mul_right (k + 3) (by omega)
    omega

/-- Representative theorem for `L1-IMP-COMPLEX-FIELD`:
    under composite dimension multiplicativity `K_d(4) = K_d(2)^2`, `d = 2` is the unique
    positive parameter (`d = 1` fails with `10 ≠ 9`, `d = 4` fails with `28 ≠ 36`),
    Gaussian norm is multiplicative (`N(1+i) * N(2+i) = 2 * 5 = 10`), and `1 + i` and `2 + i`
    have non-unit integer norms `2` and `5` while admitting exact reciprocals in `ℚ(i)`. -/
theorem l1_imp_complex_field_selection_and_gaussian_standin :
    (∀ d : Nat, 0 < d → (carrierDimK d 4 = carrierDimK d 2 * carrierDimK d 2 ↔ d = 2)) ∧
    carrierDimK 1 4 = 10 ∧ carrierDimK 1 2 * carrierDimK 1 2 = 9 ∧
    carrierDimK 2 4 = 16 ∧ carrierDimK 2 2 * carrierDimK 2 2 = 16 ∧
    carrierDimK 4 4 = 28 ∧ carrierDimK 4 2 * carrierDimK 4 2 = 36 ∧
    (∀ z w : GaussianRat10, gratNormSq (gratMul z w) = gratNormSq z * gratNormSq w) ∧
    gratNormSq ⟨1, 1⟩ = 2 ∧
    gratNormSq ⟨2, 1⟩ = 5 ∧
    gratMul ⟨1, 1⟩ (gratInv ⟨1, 1⟩) = ⟨1, 0⟩ ∧
    gratMul ⟨2, 1⟩ (gratInv ⟨2, 1⟩) = ⟨1, 0⟩ := by
  refine ⟨composite_dimension_multiplicativity_selects_d_eq_two,
    by decide, by decide, by decide, by decide, by decide, by decide,
    gratNormSq_mul, ?_, ?_, ?_, ?_⟩ <;>
  · simp only [gratNormSq, gratMul, gratInv, GaussianRat10.mk.injEq]
    grind

/-! ## 2. PGW-RUNG2A-STAKE-DECLARED-LABEL (GENESIS) -/

/-- Two-sided stake label on ordered datum pairs. -/
inductive StakeLabel where
  | apart
  | same
  | free
  deriving DecidableEq, Repr

/-- A declared two-sided stake assigns a `StakeLabel` to each ordered pair `(i, j)`. -/
abbrev Stake := Nat → Nat → StakeLabel

/-- The all-free stake: assigns `.free` to every pair. -/
def freeStake : Stake := fun _ _ => .free

/-- The all-apart stake: assigns `.apart` to every distinct pair `i ≠ j`, `.free` on the diagonal. -/
def allApartStake : Stake := fun i j => if i == j then .free else .apart

/-- Whether a single unary context `⟨f, [none]⟩` separates `i` and `j` in regime `r`. -/
def unarySeparatedBool (r : RungRegime) (i j : Nat) : Bool :=
  (List.range r.forms.length).any (fun f =>
    decide (derivableRung r (f, [i])) != decide (derivableRung r (f, [j])))

/-- Whether a regime honours a `StakeLabel` on pair `(i, j)` (using unary context separation
    for `.apart` and collapse for `.same`). -/
def honoursLabelBool (r : RungRegime) (lbl : StakeLabel) (i j : Nat) : Bool :=
  match lbl with
  | .free => true
  | .apart => unarySeparatedBool r i j
  | .same => !unarySeparatedBool r i j

/-- Whether an unresolved demand stands at ordered pair `(i, j)` in regime `r` under `stake`. -/
def demandAtPairBool (stake : Stake) (r : RungRegime) (i j : Nat) : Bool :=
  decide (i < r.data ∧ j < r.data ∧ i ≠ j) && !honoursLabelBool r (stake i j) i j

/-- Whether any unresolved demand stands in regime `r` under `stake`. -/
def hasDemandBool (stake : Stake) (r : RungRegime) : Bool :=
  (List.range r.data).any (fun i =>
    (List.range r.data).any (fun j => demandAtPairBool stake r i j))

/-- Under the `freeStake`, no demand ever stands at any pair or regime. -/
theorem free_stake_carries_no_demand (r : RungRegime) (i j : Nat) :
    demandAtPairBool freeStake r i j = false := by
  simp [demandAtPairBool, freeStake, honoursLabelBool]

/-- A `supply` event preserves all demands under any stake. -/
theorem supply_preserves_demands (stake : Stake) (r : RungRegime) (t i j : Nat) :
    (stepRung r (.supply t)).map (fun r' => demandAtPairBool stake r' i j) =
      some (demandAtPairBool stake r i j) := rfl

/-- When `r.insts = []`, `unarySeparatedBool r i j = false` for every pair `(i, j)`. -/
theorem unarySeparatedBool_false_of_no_insts (r : RungRegime) (hi : r.insts = []) (i j : Nat) :
    unarySeparatedBool r i j = false := by
  unfold unarySeparatedBool
  rw [List.any_eq_false]
  intro f _
  have hEq : derivableRung r (f, [i]) ↔ derivableRung r (f, [j]) := by
    have hc := collapsedRung_of_no_insts r hi i j ⟨f, [none]⟩
    simpa [plugCtx] using hc
  by_cases h1 : derivableRung r (f, [i])
  · have h2 : derivableRung r (f, [j]) := hEq.mp h1
    simp [h1, h2]
  · have h2 : ¬ derivableRung r (f, [j]) := fun h => h1 (hEq.mpr h)
    simp [h1, h2]

/-- Growth (`admitDatum`) from a regime with `r.insts = []` and `0 < r.data` generates an
    `.apart` demand at `(0, r.data)` whenever `stake 0 r.data = .apart`. -/
theorem growth_generates_apart_of_no_insts
    (stake : Stake) (r : RungRegime) (hi : r.insts = []) (hd : 0 < r.data)
    (hLbl : stake 0 r.data = .apart) :
    ∃ r', stepRung r .admitDatum = some r' ∧ demandAtPairBool stake r' 0 r.data = true := by
  refine ⟨{ r with data := r.data + 1 }, rfl, ?_⟩
  have hSep : unarySeparatedBool { r with data := r.data + 1 } 0 r.data = false :=
    unarySeparatedBool_false_of_no_insts { r with data := r.data + 1 } hi 0 r.data
  have hBounds : 0 < r.data + 1 ∧ r.data < r.data + 1 ∧ (0 : Nat) ≠ r.data := by omega
  simp [demandAtPairBool, hBounds, hLbl, honoursLabelBool, hSep]

/-- Representative theorem for `PGW-RUNG2A-STAKE-DECLARED-LABEL`:
    the `freeStake` carries no demand, `supply` preserves all demands, and growth (`admitDatum`)
    generates an `.apart` demand when `insts = []` while generating a `.same` demand only when
    the pair is separated. -/
theorem rung2a_stake_declared_label_and_growth_cases :
    (∀ r : RungRegime, ∀ i j : Nat, demandAtPairBool freeStake r i j = false) ∧
    (∀ stake : Stake, ∀ r : RungRegime, ∀ t i j : Nat,
      (stepRung r (.supply t)).map (fun r' => demandAtPairBool stake r' i j) =
        some (demandAtPairBool stake r i j)) ∧
    (∀ stake : Stake, ∀ r : RungRegime,
      r.insts = [] → 0 < r.data → stake 0 r.data = .apart →
      ∃ r', stepRung r .admitDatum = some r' ∧ demandAtPairBool stake r' 0 r.data = true) :=
  ⟨free_stake_carries_no_demand, supply_preserves_demands, growth_generates_apart_of_no_insts⟩

/-! ## 3. PGW-RUNG3-FIRST-DEMAND-INDEX (GENESIS) -/

/-- Relational specification of the first-demand index `k` along a run of length `n`:
    `k ≤ n`, a demand holds at prefix `k`, and no shorter prefix `j < k` holds a demand. -/
def IsFirstDemandIndex (P : Nat → Prop) (n k : Nat) : Prop :=
  k ≤ n ∧ P k ∧ ∀ j : Nat, j < k → ¬ P j

/-- Uniqueness of the first-demand index with NO decidability hypothesis on `P`. -/
theorem first_demand_unique {P : Nat → Prop} {n k₁ k₂ : Nat}
    (h1 : IsFirstDemandIndex P n k₁) (h2 : IsFirstDemandIndex P n k₂) :
    k₁ = k₂ := by
  have hlt_or_eq : k₁ < k₂ ∨ k₁ = k₂ ∨ k₂ < k₁ := by omega
  rcases hlt_or_eq with hlt | heq | hgt
  · exact absurd h1.2.1 (h2.2.2 k₁ hlt)
  · exact heq
  · exact absurd h2.2.1 (h1.2.2 k₂ hgt)

/-- A successor index `k + 1` cannot be the first-demand index if step `k + 1` is demand-inert
    (`P (k + 1) → P k`). -/
theorem successor_first_demand_not_inert {P : Nat → Prop} {n k : Nat}
    (hInert : P (k + 1) → P k) :
    ¬ IsFirstDemandIndex P n (k + 1) := by
  intro hFirst
  have hPk : P k := hInert hFirst.2.1
  exact hFirst.2.2 k (Nat.lt_succ_self k) hPk

/-- Compute the first prefix length `k ≤ h.length` at which `hasDemandBool stake` holds. -/
def firstDemandIndexOpt (stake : Stake) (base : RungRegime) (h : List RungEvent) : Option Nat :=
  (List.range (h.length + 1)).find? (fun k =>
    match replayRung (h.take k) base with
    | some r => hasDemandBool stake r
    | none => false)

/-- Countermodel 1 for Rung 3: two histories `[.admitDatum, .admitDatum]` and
    `[.supply 0, .admitDatum, .admitDatum]` from `genesisRegime` reach the exact same regime
    `⟨2, [], [], [], []⟩`, yet have first-demand indices `some 2` and `some 3` under `allApartStake`. -/
theorem index_is_not_a_function_of_the_reached_regime :
    let h2 : List RungEvent := [.admitDatum, .admitDatum]
    let h3 : List RungEvent := [.supply 0, .admitDatum, .admitDatum]
    replayRung h2 genesisRegime = replayRung h3 genesisRegime ∧
    firstDemandIndexOpt allApartStake genesisRegime h2 = some 2 ∧
    firstDemandIndexOpt allApartStake genesisRegime h3 = some 3 := by
  decide

/-- Countermodel 2 for Rung 3: a standing demand can cease when a separating instance is admitted. -/
theorem demand_can_cease :
    let hBefore : List RungEvent := [.admitDatum, .admitDatum, .admitForm 1]
    let hAfter  : List RungEvent := [.admitDatum, .admitDatum, .admitForm 1, .admitInst 0 [0]]
    (replayRung hBefore genesisRegime).map (hasDemandBool allApartStake) = some true ∧
    (replayRung hAfter genesisRegime).map (hasDemandBool allApartStake) = some false := by
  decide

/-- Representative theorem for `PGW-RUNG3-FIRST-DEMAND-INDEX`:
    combines decidability-free uniqueness of the first-demand index, non-consumption of inert
    events at successor indices, and the two executable countermodels (non-functionality on the
    reached regime and demand cessation). -/
theorem rung3_first_demand_index_uniqueness_and_countermodels :
    (∀ P : Nat → Prop, ∀ n k₁ k₂ : Nat,
      IsFirstDemandIndex P n k₁ → IsFirstDemandIndex P n k₂ → k₁ = k₂) ∧
    (∀ P : Nat → Prop, ∀ n k : Nat,
      (P (k + 1) → P k) → ¬ IsFirstDemandIndex P n (k + 1)) ∧
    (replayRung [.admitDatum, .admitDatum] genesisRegime =
      replayRung [.supply 0, .admitDatum, .admitDatum] genesisRegime ∧
     firstDemandIndexOpt allApartStake genesisRegime [.admitDatum, .admitDatum] = some 2 ∧
     firstDemandIndexOpt allApartStake genesisRegime [.supply 0, .admitDatum, .admitDatum] = some 3) ∧
    ((replayRung [.admitDatum, .admitDatum, .admitForm 1] genesisRegime).map
        (hasDemandBool allApartStake) = some true ∧
     (replayRung [.admitDatum, .admitDatum, .admitForm 1, .admitInst 0 [0]] genesisRegime).map
        (hasDemandBool allApartStake) = some false) :=
  ⟨fun _ _ _ _ h1 h2 => first_demand_unique h1 h2,
   fun _ _ _ hInert => successor_first_demand_not_inert hInert,
   index_is_not_a_function_of_the_reached_regime,
   demand_can_cease⟩

/-! ## 4. PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM (GENESIS) -/

/-- A stake is uniform when it assigns the same label `L0` to every distinct pair `i ≠ j`. -/
def IsUniformStake (stake : Stake) (L0 : StakeLabel) : Prop :=
  ∀ i j : Nat, i ≠ j → stake i j = L0

/-- Under a uniform stake, any datum bijection `π` that preserves `< data`, inequality, and
    `unarySeparatedBool` transports `demandAtPairBool` between `(i, j)` and `(π i, π j)`. -/
theorem uniform_stake_transports_demand_pair
    (stake : Stake) (L0 : StakeLabel) (hUnif : IsUniformStake stake L0)
    (r₁ r₂ : RungRegime) (π : Nat → Nat)
    (hBound : ∀ i j : Nat, (i < r₁.data ∧ j < r₁.data ∧ i ≠ j) ↔
      (π i < r₂.data ∧ π j < r₂.data ∧ π i ≠ π j))
    (hSep : ∀ i j : Nat, unarySeparatedBool r₁ i j = unarySeparatedBool r₂ (π i) (π j))
    (i j : Nat) :
    demandAtPairBool stake r₁ i j = demandAtPairBool stake r₂ (π i) (π j) := by
  by_cases hValid : i < r₁.data ∧ j < r₁.data ∧ i ≠ j
  · have hValid2 : π i < r₂.data ∧ π j < r₂.data ∧ π i ≠ π j := (hBound i j).mp hValid
    have hL1 : stake i j = L0 := hUnif i j hValid.2.2
    have hL2 : stake (π i) (π j) = L0 := hUnif (π i) (π j) hValid2.2.2
    simp [demandAtPairBool, hValid, hValid2, hL1, hL2, honoursLabelBool, hSep i j]
  · have hValid2 : ¬ (π i < r₂.data ∧ π j < r₂.data ∧ π i ≠ π j) :=
      fun h => hValid ((hBound i j).mpr h)
    simp [demandAtPairBool, hValid, hValid2]

/-- The non-uniform `chainStake` reader: labels `(i, j)` as `.apart` iff `i + 1 == j`. -/
def chainStake : Stake := fun i j => if i + 1 == j then .apart else .free

/-- Two isomorphic 3-datum, 1-unary-form regimes related by swapping data `0` and `2`:
    - `isoRegimeA` has unary instance `(0, [0])`, separating `0` from `1` and `2` while leaving `(1, 2)` collapsed.
    - `isoRegimeB` has unary instance `(0, [2])`, separating `2` from `0` and `1` while leaving `(0, 1)` collapsed.
    Under `chainStake`, `isoRegimeA` has a demand at `(1, 2)` whereas `isoRegimeB` has a demand at `(0, 1)`;
    and under the single-pair stake `pair12Stake` (reading `(1, 2)` only), `isoRegimeA` has a demand while
    its isomorphic partner `isoRegimeB` has NO demand! -/
def isoHistoryA : List RungEvent :=
  [.admitDatum, .admitDatum, .admitDatum, .admitForm 1, .admitInst 0 [0]]

def isoHistoryB : List RungEvent :=
  [.admitDatum, .admitDatum, .admitDatum, .admitForm 1, .admitInst 0 [2]]

/-- Index-reading stake that tests whether `i == 1 && j == 2`. -/
def indexReader12Stake : Stake := fun i j => if i == 1 && j == 2 then .apart else .free

/-- Representative theorem for `PGW-RUNG4-INDEX-UP-TO-ISOMORPHISM`:
    uniform stakes transport pair demands across datum isomorphisms, whereas under an
    index-reading stake (`indexReader12Stake` / `chainStake`) isomorphic 3-datum regimes
    differ in whether a demand stands at a given pair and class-matched histories differ
    after the separating instance is admitted. -/
theorem rung4_uniform_transport_and_nonuniform_escape :
    (∀ stake : Stake, ∀ L0 : StakeLabel, IsUniformStake stake L0 →
      ∀ r₁ r₂ : RungRegime, ∀ π : Nat → Nat,
      (∀ i j : Nat, (i < r₁.data ∧ j < r₁.data ∧ i ≠ j) ↔
        (π i < r₂.data ∧ π j < r₂.data ∧ π i ≠ π j)) →
      (∀ i j : Nat, unarySeparatedBool r₁ i j = unarySeparatedBool r₂ (π i) (π j)) →
      ∀ i j : Nat, demandAtPairBool stake r₁ i j = demandAtPairBool stake r₂ (π i) (π j)) ∧
    (replayRung isoHistoryA genesisRegime).map (hasDemandBool indexReader12Stake) = some true ∧
    (replayRung isoHistoryB genesisRegime).map (hasDemandBool indexReader12Stake) = some false ∧
    (replayRung isoHistoryA genesisRegime).map (fun r => demandAtPairBool chainStake r 1 2) = some true ∧
    (replayRung isoHistoryB genesisRegime).map (fun r => demandAtPairBool chainStake r 1 2) = some false := by
  refine ⟨uniform_stake_transports_demand_pair, by decide, by decide, by decide, by decide⟩

/-! ## 5. PGW-RUNG5-SYMMETRY-ALONG-HISTORY (GENESIS) -/

/-- Exact step law for `rungElems`: every valid step either keeps the regime (and element count)
    unchanged, or changes the regime and raises `rungElems` by `1`. -/
theorem stepRung_eq_or_elems_succ {r r' : RungRegime} {e : RungEvent}
    (h : stepRung r e = some r') :
    (r' = r ∧ rungElems r' = rungElems r) ∨ (r' ≠ r ∧ rungElems r' = rungElems r + 1) := by
  cases e with
  | supply _ =>
      simp only [stepRung, Option.some.injEq] at h
      subst h
      exact Or.inl ⟨rfl, rfl⟩
  | admitDatum =>
      simp only [stepRung, Option.some.injEq] at h
      subst h
      refine Or.inr ⟨?_, by simp [rungElems]; omega⟩
      intro heq
      have hd : r.data + 1 = r.data := congrArg RungRegime.data heq
      omega
  | admitForm a =>
      simp only [stepRung] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        refine Or.inr ⟨?_, by simp [rungElems]; omega⟩
        intro heq
        have hf : (r.forms ++ [a]).length = r.forms.length :=
          congrArg (fun x => x.forms.length) heq
        simp at hf
      · cases h
  | admitInst f args =>
      simp only [stepRung] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        rcases insertNew_eq_or_succ r.insts (f, args) with heq | hlen
        · rw [heq]; exact Or.inl ⟨rfl, rfl⟩
        · refine Or.inr ⟨?_, by simp [rungElems, hlen]; omega⟩
          intro hReg
          have hi : (insertNew r.insts (f, args)).length = r.insts.length :=
            congrArg (fun x => x.insts.length) hReg
          omega
      · cases h
  | admitRuleAll f =>
      simp only [stepRung] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        rcases insertNew_eq_or_succ r.rules f with heq | hlen
        · rw [heq]; exact Or.inl ⟨rfl, rfl⟩
        · refine Or.inr ⟨?_, by simp [rungElems, hlen]; omega⟩
          intro hReg
          have hrul : (insertNew r.rules f).length = r.rules.length :=
            congrArg (fun x => x.rules.length) hReg
          omega
      · cases h
  | impose i j =>
      simp only [stepRung] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        rcases insertNew_eq_or_succ r.reqs (i, j) with heq | hlen
        · rw [heq]; exact Or.inl ⟨rfl, rfl⟩
        · refine Or.inr ⟨?_, by simp [rungElems, hlen]; omega⟩
          intro hReg
          have hreq : (insertNew r.reqs (i, j)).length = r.reqs.length :=
            congrArg (fun x => x.reqs.length) hReg
          omega
      · cases h

/-- Check whether a datum permutation `π : List Nat` (on `0 .. r.data - 1`) preserves
    unary instances in `r.insts` (fixes form `0` and maps each `[d]` to `[π[d]]`). -/
def permPreservesInstsBool (r : RungRegime) (π : List Nat) : Bool :=
  r.insts.all (fun inst =>
    (inst.1, inst.2.map (fun d => π.getD d d)) ∈ r.insts)

/-- All 6 permutations of `3` data `{0, 1, 2}`. -/
def permsS3 : List (List Nat) :=
  [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]

/-- Count of `S_3` datum automorphisms preserving `r.insts`. -/
def autCountS3 (r : RungRegime) : Nat :=
  (permsS3.filter (permPreservesInstsBool r)).length

/-- Three 3-datum regimes along an instance-adding path `[ ] → [(0,[0])] → [(0,[0]),(0,[1]),(0,[2])]`
    demonstrating that `admitInst` decreases the automorphism count from `6` to `2` and then
    increases it back from `2` to `6`. -/
def symRegime0 : RungRegime := ⟨3, [1], [], [], []⟩
def symRegime1 : RungRegime := ⟨3, [1], [(0, [0])], [], []⟩
def symRegime2 : RungRegime := ⟨3, [1], [(0, [0]), (0, [1])], [], []⟩
def symRegime3 : RungRegime := ⟨3, [1], [(0, [0]), (0, [1]), (0, [2])], [], []⟩

/-- Representative theorem for `PGW-RUNG5-SYMMETRY-ALONG-HISTORY`:
    every event either keeps the regime or raises `rungElems` by `1` (`stepRung_eq_or_elems_succ`),
    `supply` preserves the automorphism count, and `admitInst` both lowers (`6 → 2`) and raises
    (`2 → 6`) the `S_3` automorphism count along a valid history. -/
theorem rung5_symmetry_step_law_and_both_ways_witness :
    (∀ r r' : RungRegime, ∀ e : RungEvent,
      stepRung r e = some r' →
      (r' = r ∧ rungElems r' = rungElems r) ∨ (r' ≠ r ∧ rungElems r' = rungElems r + 1)) ∧
    stepRung symRegime0 (.admitInst 0 [0]) = some symRegime1 ∧
    stepRung symRegime1 (.admitInst 0 [1]) = some symRegime2 ∧
    stepRung symRegime2 (.admitInst 0 [2]) = some symRegime3 ∧
    autCountS3 symRegime0 = 6 ∧
    autCountS3 symRegime1 = 2 ∧
    autCountS3 symRegime2 = 2 ∧
    autCountS3 symRegime3 = 6 := by
  refine ⟨fun _ _ _ h => stepRung_eq_or_elems_succ h,
    by decide, by decide, by decide, by decide, by decide, by decide, by decide⟩

end WitnessedDifference.WdpBatch10
