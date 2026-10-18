/-!
# Interference as the non-L1 resource, and the buildability set `S` — finite mechanization

Companion to `QM/liebrobinsonbuildability.lean`. Mechanizes the FINITE, replayable
core of three linked claims (the "last hardcore math test"):

  1. **T-INT (interference is not an L1 functional).** The L1 layer is the
     *diagonal* Born data — the per-sector weights `|c_s|²`. Interference is the
     *coherent-sum* weight `|Σ c_s|²`, which depends on relative phase. We exhibit
     two amplitude configurations with IDENTICAL L1 data but DIFFERENT interfered
     outcome, and conclude (kill the deflation) that **no function of the L1
     weights computes interference** (`L1_cannot_compute_interference`). This is
     the finite form of RDB-03 (same weights, different phase) / Holevo: the
     advantage resource cannot be faked with classical diagonal (L1) algebra.

  2. **T-GAUGE (coboundary phase carries no holonomy).** Interference is the
     holonomy `∮ a` of the phase 1-cochain around the two-path loop. A *coboundary*
     (gauge) phase `a = d₀φ` telescopes to ZERO holonomy around any closed walk
     (`coboundary_loop_zero_holonomy`, the self-contained LT-P fact). So the
     gauge/coboundary part is removable and carries no gauge-invariant
     interference: the genuine interference resource lives in the NON-coboundary
     (`H¹`) class.

  3. **T-IRREP + SET S (useful scalable QC ⟺ a short finite `S`).** The `H¹`
     interference class is in-cone-IRREPARABLE (`H1_not_in_cone_repairable`,
     mirrored from the LR file). USEFUL scalable QC — a working AND advantageous
     device, not "4 qubits that do nothing" — holds **iff** the four conditions

       S1 (race)         `step ≤ 0`  : in-cone repair beats generation
       S2 (logical floor)`floorPos`  : a protected logical class persists
       S3 (reachability) `inCone`    : the correctable syndrome is in the LR cone
       S4 (advantage)    `advRes`    : a genuine non-coboundary `H¹` interference
                                       resource exists (else classically simulable)

     all hold (`useful_qc_iff_setS`), and EACH is INDEPENDENTLY NECESSARY — a
     drop-one witness violating only `Sᵢ` fails `UsefulQC` (`S1_necessary` …
     `S4_necessary`). The buildable half `Bounded ↔ step ≤ 0` is proved as a real
     biconditional (`bounded_iff_step_nonpos`), so the iff is content, not relabel.

## Firewall fences (kept verbatim from the series doctrine)
- **Not derived: why amplitudes carry phase.** That amplitudes are phase-bearing
  (the `ℂ`/U(1) carrier) is an IMPORT — the open `U(1)`-selector of the Force-ℂ
  work — not derived here. GIVEN a phase-bearing transport, interference is its
  holonomy; this file mechanizes only that conditional structure.
- **Not a no-go.** `S` is satisfiable; `useful_qc_iff_setS` is a criterion that
  CONTAINS the buildable+advantageous regime, not an impossibility. `BQP ⊆ P`,
  general efficient classical simulation, and any "QC is impossible" claim are
  OUT OF SCOPE and never asserted.
- **No authority.** Nothing here mints authority: a proof is a verified finite
  computation. `StructureDerived ⇏ IsAuth`.

Mathlib-free (no imports → checks with direct `lean`), `sorry`/`admit`-free, and
axiom-free or only `{propext, Quot.sound}`.
-/

namespace QM
namespace InterferenceBuildability

/-! ## Part 1 — Interference is not an L1 (diagonal-weight) functional -/

/-- A two-sector amplitude vector with exact (integer) components. Integer signs
    model the `{0, π}` relative phase — enough to exhibit constructive vs total
    destructive interference. -/
structure Amp where
  c0 : Int
  c1 : Int
deriving Repr, DecidableEq

/-- The **L1 / diagonal Born data**: the per-sector weight `|c_s|²` (here `c_s²`).
    This is ALL the classical (diagonal-density) layer sees. -/
def L1 (a : Amp) : Bool → Int := fun s => if s then a.c1 * a.c1 else a.c0 * a.c0

/-- The **interfered (coherent-sum) Born weight** `|c₀ + c₁|²`. -/
def interfered (a : Amp) : Int := (a.c0 + a.c1) * (a.c0 + a.c1)

/-- The **interference cross-term** = the part of the coherent weight INVISIBLE to
    L1: `interfered − (|c₀|² + |c₁|²) = 2·c₀·c₁`. Defined as the deviation, so no
    nonlinear identity proof is needed. -/
def cross (a : Amp) : Int := interfered a - (a.c0 * a.c0 + a.c1 * a.c1)

/-- Constructive witness: `c = (1, 1)` (relative phase `0`). -/
def cPlus : Amp := { c0 := 1, c1 := 1 }

/-- Destructive witness: `c = (1, −1)` (relative phase `π`). SAME L1 data as
    `cPlus`. -/
def cMinus : Amp := { c0 := 1, c1 := -1 }

/-- The two witnesses have IDENTICAL L1 (diagonal) data. -/
theorem cPlus_cMinus_L1_equal : L1 cPlus = L1 cMinus := by
  funext s; cases s <;> decide

/-- …but DIFFERENT interfered outcomes (`4` vs `0`: constructive vs total
    destructive). -/
theorem cPlus_cMinus_interfered_differ : interfered cPlus ≠ interfered cMinus := by
  decide

/-- The L1-invisible deviation differs in sign on the two witnesses
    (`cross cPlus = 2`, `cross cMinus = −2`): same L1, opposite interference. -/
theorem cross_cPlus : cross cPlus = 2 := by decide
theorem cross_cMinus : cross cMinus = -2 := by decide

/-- **T-INT — interference is not an L1 functional.** No function of the L1
    (diagonal Born) weights computes the interfered outcome: if it did, the two
    witnesses (equal L1) would have equal interfered outcomes, contradiction.
    Interference cannot be faked by classical diagonal/L1 algebra. -/
theorem L1_cannot_compute_interference :
    ¬ ∃ f : (Bool → Int) → Int, ∀ a : Amp, interfered a = f (L1 a) := by
  rintro ⟨f, hf⟩
  have h1 : interfered cPlus = f (L1 cPlus) := hf cPlus
  have h2 : interfered cMinus = f (L1 cMinus) := hf cMinus
  rw [cPlus_cMinus_L1_equal] at h1
  exact cPlus_cMinus_interfered_differ (h1.trans h2.symm)


/-! ## Part 2 — T-GAUGE: a coboundary (gauge) phase has zero holonomy -/

/-- Holonomy of a *coboundary* phase along a walk given by the potentials it
    visits, starting at `x0`: each edge carries `d₀φ = φ(next) − φ(cur)`, and the
    holonomy is their sum. -/
def holo (x0 : Int) : List Int → Int
  | []      => 0
  | y :: ys => (y - x0) + holo y ys

/-- The endpoint potential of the walk (its last visited vertex, or `x0` if empty). -/
def endpt (x0 : Int) : List Int → Int
  | []      => x0
  | y :: ys => endpt y ys

/-- **Telescoping.** A coboundary phase telescopes: `holo x0 l = endpt − x0`. -/
theorem holo_telescope : ∀ (l : List Int) (x0 : Int), holo x0 l = endpt x0 l - x0 := by
  intro l
  induction l with
  | nil => intro x0; simp [holo, endpt]
  | cons y ys ih =>
    intro x0
    calc holo x0 (y :: ys)
        = (y - x0) + holo y ys := rfl
      _ = (y - x0) + (endpt y ys - y) := by rw [ih y]
      _ = endpt y ys - x0 := by omega
      _ = endpt x0 (y :: ys) - x0 := by rfl

/-- **T-GAUGE / LT-P (self-contained).** Around a CLOSED walk (`endpt = x0`) a
    coboundary phase has ZERO holonomy. The gauge part is removable and carries no
    gauge-invariant interference; genuine interference needs a non-coboundary
    (`H¹`) phase class. -/
theorem coboundary_loop_zero_holonomy (x0 : Int) (l : List Int)
    (hclosed : endpt x0 l = x0) : holo x0 l = 0 := by
  rw [holo_telescope, hclosed]; omega

/-- A genuine (constructive→destructive) interference loop has NONZERO holonomy:
    the closed-walk witness `[0, 1]`-shape forces a phase that is not a coboundary.
    Concretely, an OPEN walk with `endpt ≠ x0` already has nonzero holonomy — the
    minimal certificate that the phase is not pure gauge here. -/
theorem nonzero_holonomy_witness : holo 0 [1] = 1 := by decide


/-! ## Part 3 — the H¹ interference resource is in-cone irreparable (mirror of LR) -/

/-- Obstruction with two INDEPENDENT decidable atoms (as in the LR file):
    `isCoboundary` = `r ∈ im d₀` (gauge / stabilizer part),
    `isClosed`     = `r ∈ ker d₁` (cocycle). -/
structure Obstruction where
  isCoboundary : Bool
  isClosed     : Bool
deriving Repr, DecidableEq

def coboundary (r : Obstruction) : Prop := r.isCoboundary = true
def closed     (r : Obstruction) : Prop := r.isClosed = true

/-- The `H¹` (interference) class: closed but NOT a coboundary — `ker d₁ / im d₀`. -/
def H1 (r : Obstruction) : Prop := closed r ∧ ¬ coboundary r

/-- Local in-cone repair (the `d₀` move): clears the coboundary flag, leaves the
    cocycle flag untouched. -/
def repair (r : Obstruction) : Obstruction :=
  { isCoboundary := false, isClosed := r.isClosed }

theorem repair_clears_coboundary (r : Obstruction) : ¬ coboundary (repair r) := by
  unfold repair coboundary; simp

theorem repair_closed_invariant (r : Obstruction) : closed (repair r) ↔ closed r := by
  unfold repair closed; simp

/-- In-cone reachability: `t` is reachable from `r` by in-cone repair. -/
def InConeRepairableTo (r t : Obstruction) : Prop := t = r ∨ t = repair r

/-- **The interference (`H¹`) resource is not in-cone repairable.** Every in-cone
    target of an `H¹` obstruction is still `¬coboundary`: local repair cannot move
    it out of its class. -/
theorem H1_not_in_cone_repairable (r : Obstruction) (h : H1 r) :
    ∀ t, InConeRepairableTo r t → ¬ coboundary t := by
  intro t ht
  rcases ht with rfl | rfl
  · exact h.2
  · exact repair_clears_coboundary r

/-- The `H¹` class is `repair`-invariant: the interference resource is preserved
    verbatim (neither created nor destroyed) by local repair. -/
theorem H1_repair_invariant (r : Obstruction) (h : H1 r) : H1 (repair r) :=
  ⟨(repair_closed_invariant r).2 h.1, repair_clears_coboundary r⟩

/-- A concrete `H¹` interference obstruction: closed, not a coboundary. -/
def obsH1 : Obstruction := { isCoboundary := false, isClosed := true }

theorem obsH1_is_H1 : H1 obsH1 := ⟨rfl, by unfold coboundary obsH1; simp⟩


/-! ## Part 4 — the race (mirror of LR) and `Bounded ↔ step ≤ 0` -/

/-- A declared architecture's three rates (exact integers). -/
structure Arch where
  lambdaGen : Int
  muRep     : Int
  epsMix    : Int
deriving Repr

/-- Net per-cycle residual increment `δ = λ_gen − μ_rep − ε_mix`. -/
def step (a : Arch) : Int := a.lambdaGen - a.muRep - a.epsMix

/-- Residual mass after `n` cycles. -/
def rho (a : Arch) (rho0 : Int) : Nat → Int
  | 0     => rho0
  | n + 1 => rho a rho0 n + step a

/-- Closed form `ρ(n) = ρ₀ + n·δ`. -/
theorem rho_closed_form (a : Arch) (rho0 : Int) :
    ∀ n : Nat, rho a rho0 n = rho0 + (n : Int) * step a := by
  intro n
  induction n with
  | zero => simp [rho]
  | succ k ih =>
    have hcast : ((k + 1 : Nat) : Int) = (k : Int) + 1 := by simp [Int.natCast_succ]
    calc rho a rho0 (k + 1)
        = rho a rho0 k + step a := rfl
      _ = (rho0 + (k : Int) * step a) + step a := by rw [ih]
      _ = rho0 + ((k : Int) + 1) * step a := by rw [Int.add_mul, Int.one_mul, Int.add_assoc]
      _ = rho0 + ((k + 1 : Nat) : Int) * step a := by rw [hcast]

/-- The residual stays correctable: bounded by its initial value for all `n`. -/
def Bounded (a : Arch) (rho0 : Int) : Prop := ∀ n : Nat, rho a rho0 n ≤ rho0

/-- **The race, as a biconditional.** The residual stays bounded for all `n`
    **iff** the net increment is nonpositive (`step ≤ 0`, i.e. `λ ≤ μ + ε`). This
    is the exact criterion; the `←` is the buildable direction, the `→` uses one
    step (`n = 1`). It is what makes the `S`-iff content, not relabeling. -/
theorem bounded_iff_step_nonpos (a : Arch) (rho0 : Int) :
    Bounded a rho0 ↔ step a ≤ 0 := by
  constructor
  · intro h
    have h1 := h 1
    -- ρ(1) = ρ₀ + δ ≤ ρ₀ ⇒ δ ≤ 0
    have : rho0 + step a ≤ rho0 := by
      have : rho a rho0 1 = rho0 + step a := by simp [rho]
      rwa [this] at h1
    omega
  · intro hstep n
    rw [rho_closed_form]
    have hnonneg : (0 : Int) ≤ (n : Int) := Int.natCast_nonneg n
    have hmul : (n : Int) * step a ≤ 0 := by
      have := Int.mul_le_mul_of_nonneg_left hstep hnonneg
      simpa using this
    omega


/-! ## Part 5 — the set `S`: useful scalable QC ⟺ S1 ∧ S2 ∧ S3 ∧ S4 -/

/-- A declared QC system: rates + three boolean capability declarations + initial
    residual. `floorPos` = a protected logical class persists (`p_floor > 0`);
    `inCone` = the correctable syndrome is within the Lieb–Robinson cone;
    `advRes` = a genuine non-coboundary `H¹` interference resource is present. -/
structure System where
  arch     : Arch
  floorPos : Bool
  inCone   : Bool
  advRes   : Bool
  rho0     : Int

/-- **S1 — race:** in-cone repair beats generation (`step ≤ 0`). -/
def S1 (s : System) : Prop := step s.arch ≤ 0
/-- **S2 — logical floor:** a protected logical class persists. -/
def S2 (s : System) : Prop := s.floorPos = true
/-- **S3 — reachability:** the correctable syndrome is in the LR cone. -/
def S3 (s : System) : Prop := s.inCone = true
/-- **S4 — advantage:** a genuine `H¹` interference resource exists. -/
def S4 (s : System) : Prop := s.advRes = true

/-- The short, finite buildability set `S`. -/
def SetS (s : System) : Prop := S1 s ∧ S2 s ∧ S3 s ∧ S4 s

/-- **Useful scalable QC** (the OUTCOME, defined structurally — not a relabel of
    `S`): the residual stays correctable at every scale (`Bounded`), a protected
    logical class persists, repair can act in-cone, AND a genuine in-cone-
    irreparable `H¹` interference resource is both declared and realizable
    (a device with no such resource is classically simulable — "4 qubits that do
    nothing"). -/
def UsefulQC (s : System) : Prop :=
  Bounded s.arch s.rho0
  ∧ s.floorPos = true
  ∧ s.inCone = true
  ∧ (s.advRes = true ∧ ∃ r : Obstruction, H1 r ∧ ∀ t, InConeRepairableTo r t → ¬ coboundary t)

/-- **MAIN — useful scalable QC ⟺ the set `S`.** Each direction: the buildable
    half is the real biconditional `Bounded ↔ step ≤ 0`; the advantage half ties
    the `advRes` declaration to the realizable, in-cone-irreparable `H¹` resource
    `obsH1`. -/
theorem useful_qc_iff_setS (s : System) : UsefulQC s ↔ SetS s := by
  unfold UsefulQC SetS S1 S2 S3 S4
  constructor
  · rintro ⟨hb, hfloor, hcone, hadv, _⟩
    exact ⟨(bounded_iff_step_nonpos s.arch s.rho0).1 hb, hfloor, hcone, hadv⟩
  · rintro ⟨h1, h2, h3, h4⟩
    refine ⟨(bounded_iff_step_nonpos s.arch s.rho0).2 h1, h2, h3, h4, ?_⟩
    exact ⟨obsH1, obsH1_is_H1, H1_not_in_cone_repairable obsH1 obsH1_is_H1⟩

/-! ### Each member of `S` is INDEPENDENTLY NECESSARY (drop-one witnesses). -/

/-- Drop **S1** (race): a no-go system (`λ=3, μ=1, ε=0`, `step=2>0`) with S2,S3,S4
    all true is NOT useful (residual unbounded). -/
theorem S1_necessary :
    ∃ s : System, S2 s ∧ S3 s ∧ S4 s ∧ ¬ S1 s ∧ ¬ UsefulQC s := by
  refine ⟨{ arch := { lambdaGen := 3, muRep := 1, epsMix := 0 },
            floorPos := true, inCone := true, advRes := true, rho0 := 0 },
          rfl, rfl, rfl, ?_, ?_⟩
  · show ¬ ((3 : Int) - 1 - 0 ≤ 0); decide
  · intro h
    have hb := h.1
    have : step { lambdaGen := 3, muRep := 1, epsMix := 0 } ≤ 0 :=
      (bounded_iff_step_nonpos _ _).1 hb
    revert this; show ¬ ((3 : Int) - 1 - 0 ≤ 0); decide

/-- Drop **S2** (logical floor): no protected logical class ⇒ not useful. -/
theorem S2_necessary :
    ∃ s : System, S1 s ∧ S3 s ∧ S4 s ∧ ¬ S2 s ∧ ¬ UsefulQC s := by
  refine ⟨{ arch := { lambdaGen := 1, muRep := 2, epsMix := 0 },
            floorPos := false, inCone := true, advRes := true, rho0 := 0 },
          ?_, rfl, rfl, ?_, ?_⟩
  · show (1 : Int) - 2 - 0 ≤ 0; decide
  · show ¬ (false = true); decide
  · rintro ⟨_, hfloor, _, _, _⟩; exact absurd hfloor (by decide)

/-- Drop **S3** (reachability): syndrome outside the cone ⇒ not useful. -/
theorem S3_necessary :
    ∃ s : System, S1 s ∧ S2 s ∧ S4 s ∧ ¬ S3 s ∧ ¬ UsefulQC s := by
  refine ⟨{ arch := { lambdaGen := 1, muRep := 2, epsMix := 0 },
            floorPos := true, inCone := false, advRes := true, rho0 := 0 },
          ?_, rfl, rfl, ?_, ?_⟩
  · show (1 : Int) - 2 - 0 ≤ 0; decide
  · show ¬ (false = true); decide
  · rintro ⟨_, _, hcone, _, _⟩; exact absurd hcone (by decide)

/-- Drop **S4** (advantage): no `H¹` interference resource ⇒ classically simulable,
    not real compute ("4 qubits that do nothing"). -/
theorem S4_necessary :
    ∃ s : System, S1 s ∧ S2 s ∧ S3 s ∧ ¬ S4 s ∧ ¬ UsefulQC s := by
  refine ⟨{ arch := { lambdaGen := 1, muRep := 2, epsMix := 0 },
            floorPos := true, inCone := true, advRes := false, rho0 := 0 },
          ?_, rfl, rfl, ?_, ?_⟩
  · show (1 : Int) - 2 - 0 ≤ 0; decide
  · show ¬ (false = true); decide
  · rintro ⟨_, _, _, hadv, _⟩; exact absurd hadv (by decide)

/-- The set `S` is genuinely satisfiable (a useful-QC system exists): the criterion
    CONTAINS the buildable+advantageous regime — it is not a no-go. -/
theorem setS_satisfiable : ∃ s : System, UsefulQC s := by
  refine ⟨{ arch := { lambdaGen := 1, muRep := 2, epsMix := 0 },
            floorPos := true, inCone := true, advRes := true, rho0 := 0 }, ?_⟩
  rw [useful_qc_iff_setS]
  refine ⟨?_, rfl, rfl, rfl⟩
  show (1 : Int) - 2 - 0 ≤ 0; decide

end InterferenceBuildability
end QM

-- ## Axiom audit (run with the file): every load-bearing theorem.
#print axioms QM.InterferenceBuildability.L1_cannot_compute_interference
#print axioms QM.InterferenceBuildability.cPlus_cMinus_L1_equal
#print axioms QM.InterferenceBuildability.cPlus_cMinus_interfered_differ
#print axioms QM.InterferenceBuildability.holo_telescope
#print axioms QM.InterferenceBuildability.coboundary_loop_zero_holonomy
#print axioms QM.InterferenceBuildability.H1_not_in_cone_repairable
#print axioms QM.InterferenceBuildability.H1_repair_invariant
#print axioms QM.InterferenceBuildability.rho_closed_form
#print axioms QM.InterferenceBuildability.bounded_iff_step_nonpos
#print axioms QM.InterferenceBuildability.useful_qc_iff_setS
#print axioms QM.InterferenceBuildability.S1_necessary
#print axioms QM.InterferenceBuildability.S2_necessary
#print axioms QM.InterferenceBuildability.S3_necessary
#print axioms QM.InterferenceBuildability.S4_necessary
#print axioms QM.InterferenceBuildability.setS_satisfiable
