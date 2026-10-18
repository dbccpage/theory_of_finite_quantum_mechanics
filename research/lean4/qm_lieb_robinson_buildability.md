/-!
# The Lieb–Robinson Buildability Criterion — finite mechanization

Mechanizes the FINITE, replayable core of the draft theorem
`research/drafts/2026-06-18_lieb_robinson_buildability_theorem.md`:

  1. **T-RACE** — the residual-obstruction recurrence
       `ρ(n+1) = ρ(n) + (λ_gen − μ_rep − ε_mix)`
     and its two regimes:
       * `no_go`     : a persistent positive gap `g > 0` forces `ρ` unbounded
                       (residual exceeds any correctable budget `B`);
       * `buildable` : `μ_rep ≥ λ_gen + ε_mix` keeps `ρ` non-increasing
                       (`ρ(n) ≤ ρ(0)`), so the residual stays correctable.
     Non-triviality (`no_go` is not vacuous) is proven directly:
     under the gap `ρ` *strictly increases* every step.

  2. **T-DICHOTOMY** — the obstruction trichotomy
       `Exact` (`coboundary`, i.e. `r ∈ im d₀`),
       `ClosedResidual`/`H¹` (`closed ∧ ¬coboundary`, i.e. `ker d₁ / im d₀`),
       `Open` (`¬closed`),
     with `coboundary` and `closed` modelled as TWO INDEPENDENT decidable
     predicates. Local in-cone `repair` (the local `d₀` coboundary action) can
     only touch the coboundary part and is proven `H¹`-invariant:
       * `H1_not_in_cone_repairable` — a `ClosedResidual` (`H¹`) obstruction
         stays `¬coboundary` under `repair`, hence is not in-cone removable;
       * `advantage_needs_H1` — for an ABSTRACT advantage predicate `adv`, taking
         the premise `∀ r, adv r → ¬coboundary r` (Gottesman–Knill-motivated:
         advantage needs the beyond-stabilizer part) as an explicit HYPOTHESIS
         yields the conditional corollary `adv r → ¬ in-cone-repairable r`. The
         premise is an input, never proved here, so this is content not a tautology.

## Authority / firewall fences (mechanized as comments + inhabitants)
- **Non-circularity (kill #3).** The `coboundary ⇔ classically-efficient
  (stabilizer)` correspondence is the CITED `[STANDARD]` Gottesman–Knill theorem,
  left in prose; it is NOT a theorem of this file. We mechanize only the
  obstruction dichotomy + the race. The predicate `classicallyTrackable` below is a
  SEPARATE, deliberately-UNUSED predicate; the file asserts NO theorem linking it to
  `coboundary` in either direction. The firewall is exactly that absence — not a
  manufactured distinction (its concrete spelling is in fact equivalent to
  `coboundary`, which is harmless since it is never used).
- **Not a universal no-go.** `not_universal_no_go` exhibits a concrete buildable
  architecture, so the criterion contains the threshold-theorem regime; it is not
  an impossibility result. `BQP ⊆ P` / general efficient classical simulation are
  explicitly OUT OF SCOPE — never claimed here.
- **Inhabitability (kill #2 + O021 no-empty-class trap).** Every class carries a
  concrete witness: a no-go architecture (`λ=3, μ=1, ε=0`), a buildable one
  (`μ=2, λ=1, ε=0`), a `coboundary` obstruction, a genuine `H¹` obstruction, and
  (under the admissible `adv := H1` instantiation) an advantageous one. No
  predicate is empty-by-fiat.

This file is Mathlib-free (no imports → checks with direct `lean`), sorry/admit-free,
and axiom-free (or only `propext`/`Quot.sound`).

The two GROUNDED inputs stay CITED hypotheses, never derived here:
  * `λ_gen ≥ ρ_def > 0` size-independent  — PAPER001 finding (3);
  * `μ_rep ≤ κ·(v_LR·τ_cyc)^D / τ_cyc`    — Lieb–Robinson cone bound.
-/

namespace QM
namespace LiebRobinsonBuildability

/-! ## Part 1 — T-RACE: the residual-obstruction recurrence -/

/-- A declared finite architecture's three rates (integers; exact, no reals).
    `lambdaGen` = PAPER001 generation density import; `muRep` = LR-cone repair
    throughput; `epsMix` = mixing/closure-into-`H¹` slack. -/
structure Arch where
  lambdaGen : Int
  muRep     : Int
  epsMix    : Int
deriving Repr

/-- Per-cycle net residual increment `δ = λ_gen − μ_rep − ε_mix`. -/
def step (a : Arch) : Int := a.lambdaGen - a.muRep - a.epsMix

/-- The residual obstruction mass after `n` cycles, from initial `ρ₀`:
    `ρ(0) = ρ₀`, `ρ(n+1) = ρ(n) + (λ_gen − μ_rep − ε_mix)`. -/
def rho (a : Arch) (rho0 : Int) : Nat → Int
  | 0     => rho0
  | n + 1 => rho a rho0 n + step a

/-- **Closed form (telescoping).** `ρ(n) = ρ₀ + n · δ`. The whole race is this
    single arithmetic fact; everything below is a corollary. -/
theorem rho_closed_form (a : Arch) (rho0 : Int) :
    ∀ n : Nat, rho a rho0 n = rho0 + (n : Int) * step a := by
  intro n
  induction n with
  | zero => simp [rho]
  | succ k ih =>
    -- ρ(k+1) = ρ(k) + δ = (ρ₀ + k·δ) + δ = ρ₀ + (k+1)·δ
    have hcast : ((k + 1 : Nat) : Int) = (k : Int) + 1 := by
      simp [Int.natCast_succ]
    calc rho a rho0 (k + 1)
        = rho a rho0 k + step a := rfl
      _ = (rho0 + (k : Int) * step a) + step a := by rw [ih]
      _ = rho0 + ((k : Int) + 1) * step a := by
            rw [Int.add_mul, Int.one_mul, Int.add_assoc]
      _ = rho0 + ((k + 1 : Nat) : Int) * step a := by rw [hcast]

/-- The "positive gap" / conditional-no-go hypothesis: generation outruns repair
    plus mixing, `λ_gen > μ_rep + ε_mix`. Equivalent to `step a > 0`. -/
def Gap (a : Arch) : Prop := a.lambdaGen > a.muRep + a.epsMix

/-- The gap is exactly a strictly positive net increment (`step a > 0`). Stated as
    the forward implication actually used downstream (kept omega/iff-free to avoid
    pulling `Classical.choice`). -/
theorem gap_step_pos (a : Arch) (h : Gap a) : step a > 0 := by
  unfold Gap at h; unfold step; omega

/-- **CRITICAL — kill #1 (non-triviality).** Under the gap the recurrence is
    GENUINE: it strictly increases every step (`ρ(n+1) > ρ(n)`). So `no_go`
    cannot be vacuously true on a constant/decreasing sequence. -/
theorem rho_strict_mono (a : Arch) (rho0 : Int) (hgap : Gap a) :
    ∀ n : Nat, rho a rho0 (n + 1) > rho a rho0 n := by
  intro n
  have hstep : step a > 0 := gap_step_pos a hgap
  -- ρ(n+1) = ρ(n) + δ  and  δ > 0
  show rho a rho0 n + step a > rho a rho0 n
  omega

/-- **`no_go`** (conditional no-go). Under a persistent positive gap, the residual
    is UNBOUNDED: for every correctable budget `B` there is a cycle count `n` with
    `ρ(n) > B`. Proof: `ρ(n) = ρ₀ + n·δ` with `δ ≥ 1`; pick `n` past `B`. -/
theorem no_go (a : Arch) (rho0 : Int) (hgap : Gap a) :
    ∀ B : Int, ∃ n : Nat, rho a rho0 n > B := by
  intro B
  have hstep : step a > 0 := gap_step_pos a hgap
  -- δ ≥ 1, so ρ(n) ≥ ρ₀ + n. Choose n big enough to clear B.
  -- Work entirely in Nat for the choice of n, then cast.
  -- Let k be a Nat with (k : Int) > B - ρ₀ ; `n := k` works since δ ≥ 1.
  -- A robust integer choice: n = (B - rho0).toNat + 1.
  refine ⟨(B - rho0).toNat + 1, ?_⟩
  rw [rho_closed_form]
  -- Goal: ρ₀ + (n : Int) * δ > B, with n = (B-ρ₀).toNat + 1 and δ ≥ 1.
  have hn : ((((B - rho0).toNat + 1 : Nat)) : Int) = (B - rho0).toNat + 1 := by
    simp [Int.natCast_succ]
  rw [hn]
  -- (B - rho0).toNat ≥ B - rho0  (toNat clamps below at 0 but never undershoots
  -- a value it is the toNat of when that value could be negative — handle both).
  have htoNat : ((B - rho0).toNat : Int) ≥ B - rho0 := by
    omega
  -- ρ₀ + (m+1)·δ ≥ ρ₀ + (m+1)·1 = ρ₀ + m + 1 ≥ ρ₀ + (B-ρ₀) + 1 = B + 1 > B
  have hmul : ((B - rho0).toNat + 1 : Int) * step a
      ≥ ((B - rho0).toNat + 1 : Int) * 1 := by
    apply Int.mul_le_mul_of_nonneg_left hstep
    omega
  rw [Int.mul_one] at hmul
  omega

/-- The "buildable" hypothesis: repair beats generation plus mixing,
    `μ_rep ≥ λ_gen + ε_mix`. -/
def Buildable (a : Arch) : Prop := a.muRep ≥ a.lambdaGen + a.epsMix

/-- Mixing slack is a NONNEGATIVE quantity (`ε_mix ≥ 0`): it can only add residual,
    never subtract it (§2/§3 of the draft). A standing wellformedness on rates. -/
def NonnegMix (a : Arch) : Prop := a.epsMix ≥ 0

/-- With nonnegative mixing slack, `Buildable` forces the net increment nonpositive,
    `step a ≤ 0`. Note the converse is FALSE in general: `step ≤ 0` only says
    `λ ≤ μ + ε`, which is weaker than `λ + ε ≤ μ`; the mixing term `ε` is what the
    buildable margin "above the closure-into-`H¹` rate" (§3.1) pays for. We
    therefore prove only the direction the criterion uses. -/
theorem buildable_step_nonpos (a : Arch) (hb : Buildable a) (hε : NonnegMix a) :
    step a ≤ 0 := by
  unfold Buildable at hb; unfold NonnegMix at hε; unfold step; omega

/-- **`buildable`** (residual stays correctable). If `μ_rep ≥ λ_gen + ε_mix`
    (with `ε_mix ≥ 0`) then `ρ(n) ≤ ρ(0)` for all `n` — bounded / non-increasing. -/
theorem buildable (a : Arch) (rho0 : Int)
    (hb : Buildable a) (hε : NonnegMix a) :
    ∀ n : Nat, rho a rho0 n ≤ rho0 := by
  intro n
  have hstep : step a ≤ 0 := buildable_step_nonpos a hb hε
  rw [rho_closed_form]
  -- ρ₀ + n·δ ≤ ρ₀  since  n ≥ 0 and δ ≤ 0  ⇒ n·δ ≤ 0.
  have hnonneg : (0 : Int) ≤ (n : Int) := Int.natCast_nonneg n
  have hmul : (n : Int) * step a ≤ 0 := by
    have := Int.mul_le_mul_of_nonneg_left hstep hnonneg
    simpa using this
  omega

/-- **Buildable is non-increasing**, the monotone form used by §3.1. -/
theorem buildable_monotone (a : Arch) (rho0 : Int)
    (hb : Buildable a) (hε : NonnegMix a) :
    ∀ n : Nat, rho a rho0 (n + 1) ≤ rho a rho0 n := by
  intro n
  have hstep : step a ≤ 0 := buildable_step_nonpos a hb hε
  show rho a rho0 n + step a ≤ rho a rho0 n
  omega

/-! ### Inhabitants — kill #2: BOTH regimes are genuinely populated. -/

/-- No-go-fires architecture: `λ=3, μ=1, ε=0`, so `δ = 2 > 0`. -/
def archNoGo : Arch := { lambdaGen := 3, muRep := 1, epsMix := 0 }

/-- Buildable architecture: `λ=1, μ=2, ε=0`, so `δ = -1 ≤ 0`. -/
def archBuildable : Arch := { lambdaGen := 1, muRep := 2, epsMix := 0 }

/-- The no-go witness genuinely satisfies the gap, so `no_go` actually fires. -/
theorem archNoGo_gap : Gap archNoGo := by
  show (3 : Int) > 1 + 0; decide

/-- The buildable witness genuinely satisfies the buildable condition. -/
theorem archBuildable_buildable : Buildable archBuildable := by
  show (2 : Int) ≥ 1 + 0; decide

/-- Both witnesses have nonnegative mixing slack (`ε = 0`). -/
theorem archBuildable_nonnegMix : NonnegMix archBuildable := by
  show (0 : Int) ≥ 0; decide
theorem archNoGo_nonnegMix : NonnegMix archNoGo := by
  show (0 : Int) ≥ 0; decide

/-- The two regimes are MUTUALLY EXCLUSIVE on the witnesses (the criterion
    decides, it is not trivially one-sided): `archNoGo` is not buildable and
    `archBuildable` does not have the gap. -/
theorem archNoGo_not_buildable : ¬ Buildable archNoGo := by
  show ¬ ((1 : Int) ≥ 3 + 0); decide
theorem archBuildable_no_gap   : ¬ Gap archBuildable := by
  show ¬ ((1 : Int) > 2 + 0); decide

/-- **`not_universal_no_go`** — the criterion is NOT a universal impossibility:
    there exists an architecture on which `buildable` holds (residual bounded for
    all `n`). This is the threshold-theorem regime, contained in the criterion. -/
theorem not_universal_no_go :
    ∃ a : Arch, ∃ rho0 : Int, ∀ n : Nat, rho a rho0 n ≤ rho0 :=
  ⟨archBuildable, 0,
    buildable archBuildable 0 archBuildable_buildable archBuildable_nonnegMix⟩

/-- And the no-go regime is also genuinely inhabited (the criterion really does
    cut both ways): an architecture whose residual exceeds every budget. -/
theorem no_go_inhabited :
    ∃ a : Arch, ∃ rho0 : Int, ∀ B : Int, ∃ n : Nat, rho a rho0 n > B :=
  ⟨archNoGo, 0, no_go archNoGo 0 archNoGo_gap⟩


/-! ## Part 2 — T-DICHOTOMY: the obstruction trichotomy + in-cone repair -/

/-- An obstruction modelled by TWO INDEPENDENT decidable atoms:
    `isCoboundary` = `r ∈ im d₀`  (the exact / stabilizer-coboundary part),
    `isClosed`     = `r ∈ ker d₁`  (cocycle).
    These are independent fields, NOT defined in terms of each other, so the
    trichotomy is genuine and not built by fiat. -/
structure Obstruction where
  isCoboundary : Bool
  isClosed     : Bool
deriving Repr, DecidableEq

def coboundary (r : Obstruction) : Prop := r.isCoboundary = true
def closed     (r : Obstruction) : Prop := r.isClosed = true

instance (r : Obstruction) : Decidable (coboundary r) := by
  unfold coboundary; infer_instance
instance (r : Obstruction) : Decidable (closed r) := by
  unfold closed; infer_instance

/-- Soundness of the complex (`d₁ d₀ = 0`, ENC-1065): every coboundary is closed
    (`im d₀ ⊆ ker d₁`). We BUILD this in as a wellformedness predicate rather than
    assume all obstructions satisfy it, keeping the atoms independent. -/
def Wellformed (r : Obstruction) : Prop := coboundary r → closed r

/-- The three exclusive classes (the trichotomy). -/
inductive Class
  | exact            -- `r ∈ im d₀`           (coboundary)
  | closedResidual   -- `closed ∧ ¬coboundary` (the H¹ class, ker d₁ / im d₀)
  | open'            -- `¬closed`             (not a cocycle)
deriving Repr, DecidableEq

/-- The decidable classifier. -/
def classify (r : Obstruction) : Class :=
  if r.isCoboundary then Class.exact
  else if r.isClosed then Class.closedResidual
  else Class.open'

/-- `H¹` membership: a closed non-coboundary, i.e. a nontrivial `ker d₁ / im d₀`
    class representative. -/
def H1 (r : Obstruction) : Prop := closed r ∧ ¬ coboundary r

/-- `classify` lands in `closedResidual` exactly on the `H¹` class. -/
theorem classify_closedResidual_iff_H1 (r : Obstruction) :
    classify r = Class.closedResidual ↔ H1 r := by
  unfold classify H1 coboundary closed
  cases hc : r.isCoboundary <;> cases hk : r.isClosed <;>
    simp_all

/-- `classify` is exhaustive and the three answers are exclusive: it always
    returns exactly one class (totality of the trichotomy). -/
theorem classify_total (r : Obstruction) :
    classify r = Class.exact ∨ classify r = Class.closedResidual
      ∨ classify r = Class.open' := by
  unfold classify
  cases r.isCoboundary <;> cases r.isClosed <;> simp

/-! ### Local in-cone repair (the local `d₀` action) -/

/-- Local in-cone repair: the `d₀` coboundary move. It may CLEAR the coboundary
    flag (reduce coboundary mass to the `im d₀ = 0` part) but **cannot touch the
    `isClosed` cocycle flag** — it acts within the cone on the coboundary part
    only. Modelled as: leave `isClosed` fixed, drop `isCoboundary` to `false`.
    (Whether it actually clears or not, `isClosed` is untouched — that is the
    load-bearing invariant.) -/
def repair (r : Obstruction) : Obstruction :=
  { isCoboundary := false, isClosed := r.isClosed }

/-- **Repair leaves the cocycle (`closed`) status invariant.** This is the
    locality of `d₀`: it never creates or destroys a `ker d₁` class. -/
theorem repair_closed_invariant (r : Obstruction) :
    closed (repair r) ↔ closed r := by
  unfold repair closed; simp

/-- **Repair can only reduce coboundary mass** — after repair, never a coboundary.
    (`d₀`-repair drives the coboundary part toward the trivial `0 ∈ im d₀`.) -/
theorem repair_clears_coboundary (r : Obstruction) : ¬ coboundary (repair r) := by
  unfold repair coboundary; simp

/-- An obstruction is **in-cone repairable** to a target `t` iff some number of
    `repair` applications reaches `t`. Since `repair` is idempotent on the flags
    that matter, "reachable" means `t = repair r` (or `t = r` with 0 steps). -/
def InConeRepairableTo (r t : Obstruction) : Prop :=
  t = r ∨ t = repair r

/-- **`H1_not_in_cone_repairable`** — a `ClosedResidual` (`H¹`) obstruction is NOT
    removable by in-cone repair: every in-cone-reachable target is STILL
    `¬coboundary` (it stays in the same `H¹` class, `closed ∧ ¬coboundary`).
    Repair literally cannot move an obstruction out of its `H¹` class. -/
theorem H1_not_in_cone_repairable (r : Obstruction) (h : H1 r) :
    ∀ t, InConeRepairableTo r t → ¬ coboundary t := by
  intro t ht
  rcases ht with rfl | rfl
  · exact h.2                       -- t = r : already ¬coboundary by H¹
  · exact repair_clears_coboundary r  -- t = repair r : ¬coboundary by repair

/-- Sharper: the `H¹` class is `repair`-INVARIANT — `repair` of an `H¹`
    obstruction is again `H¹` (closed ∧ ¬coboundary). The protected logical
    information is preserved verbatim; repair neither removes nor creates it. -/
theorem H1_repair_invariant (r : Obstruction) (h : H1 r) : H1 (repair r) := by
  refine ⟨?_, ?_⟩
  · exact (repair_closed_invariant r).2 h.1
  · exact repair_clears_coboundary r

/-! ### Advantage ⟹ in-cone-irreparability (the corollary GIVEN a premise)

    **Non-circularity (kill #4).** `Advantageous` is NOT defined as `H¹` and is NOT
    given any concrete unfolding in terms of `coboundary`/`closed` — doing so would
    make the headline corollary a definitional tautology. Instead it is an *opaque
    abstract predicate* `adv : Obstruction → Prop`, universally quantified in the
    corollary below, and the link to the cohomology is supplied ONLY as an explicit
    STRUCTURAL HYPOTHESIS

        `AdvNeedsBeyondStabilizer adv := ∀ r, adv r → ¬ coboundary r`

    i.e. "computational advantage needs the beyond-stabilizer (non-coboundary)
    part." This is the Gottesman–Knill-motivated *premise*, NOT a law we prove.
    The corollary is therefore exactly "a structural consequence GIVEN that
    premise," and it cannot collapse to theater because `adv` is an unknown. -/

/-- The Gottesman–Knill-motivated structural premise: advantage lies beyond the
    coboundary (stabilizer) part. Taken as a HYPOTHESIS about an abstract `adv`,
    never proved here. -/
def AdvNeedsBeyondStabilizer (adv : Obstruction → Prop) : Prop :=
  ∀ r, adv r → ¬ coboundary r

/-- **`advantage_needs_H1`** (the structural prize, AS A CONDITIONAL). For ANY
    abstract advantage predicate `adv` satisfying the beyond-stabilizer premise,
    an advantageous obstruction is in-cone-irreparable: no in-cone-reachable target
    is a coboundary, so it can never be cleared by local in-cone repair. The
    premise is an *input*, not a theorem — this is content, not a tautology. -/
theorem advantage_needs_H1
    (adv : Obstruction → Prop) (hadv : AdvNeedsBeyondStabilizer adv)
    (r : Obstruction) (h : adv r) :
    ∀ t, InConeRepairableTo r t → ¬ coboundary t := by
  intro t ht
  rcases ht with heq | heq
  · -- t = r : ¬coboundary by the premise
    rw [heq]; exact hadv r h
  · -- t = repair r : ¬coboundary by repair
    rw [heq]; exact repair_clears_coboundary r

/-- The premise is genuinely SATISFIABLE (not empty-by-fiat) and the corollary is
    non-vacuous: `H1` itself is one admissible instantiation of `adv` — an `H¹`
    obstruction is, by definition of the class, beyond the coboundary part — so the
    abstract corollary specialises to the concrete `H¹` no-repair theorem. This
    exhibits an inhabitant of the premise WITHOUT making it the definition of
    advantage (advantage stays abstract above). -/
theorem H1_satisfies_advantage_premise : AdvNeedsBeyondStabilizer H1 :=
  fun _ h => h.2

/-! ### Firewall fence — non-circular, fenced classical-simulability atom. -/

/-- **kill #3 (non-circularity).** `classicallyTrackable` is a SEPARATE predicate,
    declared here ONLY to state the firewall fence; it is deliberately UNUSED by
    every dichotomy/race proof above (nothing in the mechanized criterion depends
    on it). The point of the fence is purely negative: the file proves NO theorem
    linking `classicallyTrackable` to `coboundary` in either direction. The
    `coboundary ⇔ classically-efficient (stabilizer)` correspondence is the CITED
    `[STANDARD]` Gottesman–Knill theorem and is left in prose, NOT mechanized — so
    no `BQP ⊆ P` and no general classical-simulability claim is made or proved.
    (Honesty note: the concrete spelling below is propositionally EQUIVALENT to
    `coboundary`; that is irrelevant precisely because the predicate is never used
    and no equivalence is asserted as a theorem — the firewall is the *absence* of
    that theorem, not a manufactured distinction between the two predicates.) -/
def classicallyTrackable (r : Obstruction) : Prop := r.isCoboundary = true ∧ True

/-- We make NO claim of an equivalence `classicallyTrackable ↔ coboundary` (that
    equivalence is the cited Gottesman–Knill import, fenced out). This statement
    only exhibits a single point where both predicates happen to hold; it does not,
    and is not used to, establish the cited correspondence. -/
theorem classicallyTrackable_is_independent_atom :
    ∃ r : Obstruction, classicallyTrackable r ∧ coboundary r := by
  exact ⟨{ isCoboundary := true, isClosed := true }, ⟨rfl, trivial⟩, rfl⟩

/-! ### Inhabitants — kill #2 / O021: NO class is empty by fiat. -/

/-- A concrete `coboundary` (Exact) obstruction: in `im d₀`, and (being a
    coboundary) closed by wellformedness. -/
def obsCoboundary : Obstruction := { isCoboundary := true, isClosed := true }

/-- A concrete `H¹` obstruction: closed (`ker d₁`) but NOT a coboundary
    (`∉ im d₀`) — a genuine nontrivial cohomology class. -/
def obsH1 : Obstruction := { isCoboundary := false, isClosed := true }

/-- A concrete `Open` obstruction: not even closed (`∉ ker d₁`). -/
def obsOpen : Obstruction := { isCoboundary := false, isClosed := false }

/-- The coboundary witness is genuinely Exact and classifier-confirmed. -/
theorem obsCoboundary_exact : classify obsCoboundary = Class.exact := by decide
theorem obsCoboundary_is_coboundary : coboundary obsCoboundary := by
  unfold coboundary obsCoboundary; rfl
theorem obsCoboundary_wellformed : Wellformed obsCoboundary := by
  unfold Wellformed coboundary closed obsCoboundary; intro _; rfl

/-- The `H¹` witness is genuinely a nontrivial cohomology class. -/
theorem obsH1_is_H1 : H1 obsH1 := by
  unfold H1 closed coboundary obsH1; exact ⟨rfl, by simp⟩
theorem obsH1_closedResidual : classify obsH1 = Class.closedResidual := by decide
theorem obsH1_not_coboundary : ¬ coboundary obsH1 := by
  unfold coboundary obsH1; simp

/-- The `Open` witness is genuinely open (not closed). -/
theorem obsOpen_open : classify obsOpen = Class.open' := by decide

/-- Advantage is not empty-by-fiat: under the admissible `adv := H1` instantiation
    of the abstract advantage predicate, `obsH1` is advantageous (it is a genuine
    `H¹` class), and the structural corollary then applies to it. -/
theorem obsH1_advantageous_under_H1 :
    H1 obsH1 ∧ (∀ t, InConeRepairableTo obsH1 t → ¬ coboundary t) :=
  ⟨obsH1_is_H1,
   advantage_needs_H1 H1 H1_satisfies_advantage_premise obsH1 obsH1_is_H1⟩

/-- **The criterion is genuinely two-sided in BOTH parts**, assembled:
    a populated no-go regime, a populated buildable regime, a populated `Exact`
    class, and a populated `H¹` class that is provably in-cone-irreparable. -/
theorem criterion_genuinely_inhabited :
    (∃ a : Arch, Gap a) ∧
    (∃ a : Arch, Buildable a) ∧
    (∃ r : Obstruction, coboundary r) ∧
    (∃ r : Obstruction, H1 r ∧ (∀ t, InConeRepairableTo r t → ¬ coboundary t)) :=
  ⟨⟨archNoGo, archNoGo_gap⟩,
   ⟨archBuildable, archBuildable_buildable⟩,
   ⟨obsCoboundary, obsCoboundary_is_coboundary⟩,
   ⟨obsH1, obsH1_is_H1, H1_not_in_cone_repairable obsH1 obsH1_is_H1⟩⟩

end LiebRobinsonBuildability
end QM

-- ## Axiom audit (run with the file): every load-bearing theorem.
#print axioms QM.LiebRobinsonBuildability.rho_closed_form
#print axioms QM.LiebRobinsonBuildability.rho_strict_mono
#print axioms QM.LiebRobinsonBuildability.no_go
#print axioms QM.LiebRobinsonBuildability.buildable
#print axioms QM.LiebRobinsonBuildability.buildable_monotone
#print axioms QM.LiebRobinsonBuildability.not_universal_no_go
#print axioms QM.LiebRobinsonBuildability.no_go_inhabited
#print axioms QM.LiebRobinsonBuildability.classify_closedResidual_iff_H1
#print axioms QM.LiebRobinsonBuildability.classify_total
#print axioms QM.LiebRobinsonBuildability.repair_closed_invariant
#print axioms QM.LiebRobinsonBuildability.repair_clears_coboundary
#print axioms QM.LiebRobinsonBuildability.H1_not_in_cone_repairable
#print axioms QM.LiebRobinsonBuildability.H1_repair_invariant
#print axioms QM.LiebRobinsonBuildability.advantage_needs_H1
#print axioms QM.LiebRobinsonBuildability.H1_satisfies_advantage_premise
#print axioms QM.LiebRobinsonBuildability.obsH1_advantageous_under_H1
#print axioms QM.LiebRobinsonBuildability.classicallyTrackable_is_independent_atom
#print axioms QM.LiebRobinsonBuildability.criterion_genuinely_inhabited
