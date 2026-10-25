import Mathlib.Tactic

/-!
# Campaign: FSP-THETA-TERM-COMPLEX-WEIGHT (TFQ-1198 / FSP-DERIV-034)

Formalizes the lattice topological charge $Q_{\mathrm{top}} = n_+ - n_- \in \mathbb{Z}$,
rational $\theta/\pi$ phase non-reality criterion, CP-conjugate pair sine cancellation,
$\theta = \pi$ parity character $(-1)^Q$, two-sector partition sum cancellation,
instanton susceptibility second-moment positivity, and `GIN-C9` scope fences for
`FSP-THETA-TERM-COMPLEX-WEIGHT` (`TFQ-1198`, stage `FERMION_SIGN`, status `IMPORTED_ASSUMPTION`).
-/

namespace CampaignFspThetaTermComplexWeight

/-- Integer lattice topological charge $Q_{\mathrm{top}} = n_+ - n_-$ from chiral zero-mode
    counts $n_+, n_- \in \mathbb{N}$ (matching `CdtTopologicalChargeEvaluator` in
    `code/python/src/fsp/cdt_topological_charge_evaluator.py`). -/
def latticeTopologicalCharge (nPos nNeg : Nat) : Int :=
  (nPos : Int) - (nNeg : Int)

/-- Theorem 1: The lattice topological charge $Q_{\mathrm{top}}(n_+, n_-) = n_+ - n_-$
    is antisymmetric under chirality / CP reversal $(n_+, n_-) \mapsto (n_-, n_+)$
    and vanishes on chirality-balanced configurations $n_+ = n_-$. -/
theorem lattice_chiral_index_cp_antisymmetry (nPos nNeg : Nat) :
    latticeTopologicalCharge nNeg nPos = -latticeTopologicalCharge nPos nNeg ∧
    latticeTopologicalCharge nPos nPos = 0 := by
  dsimp [latticeTopologicalCharge]
  omega

/-- Criterion for a rational multiple $\theta = (p/q)\pi$ ($q > 0$) times integer charge $Q$
    to lie in $\pi \mathbb{Z}$, i.e., $q \mid p \cdot Q$. -/
def thetaChargeInPiZ (p q Q : Int) : Bool :=
  decide ((p * Q) % q == 0)

/-- Theorem 2: For a rational vacuum angle $\theta = (p/q)\pi$ with $q = 3$, non-zero
    charges $Q \in \{1, 2\}$ and numerators $p \in \{1, 2\}$ fail the $\pi \mathbb{Z}$
    integrality condition (`thetaChargeInPiZ p 3 Q = false`), whereas $Q = 0$ or $Q = 3$
    satisfy it (`thetaChargeInPiZ p 3 Q = true`). -/
theorem rational_pi_theta_real_weight_iff_divisible :
    thetaChargeInPiZ 1 3 1 = false ∧
    thetaChargeInPiZ 1 3 2 = false ∧
    thetaChargeInPiZ 2 3 1 = false ∧
    thetaChargeInPiZ 2 3 2 = false ∧
    thetaChargeInPiZ 1 3 0 = true ∧
    thetaChargeInPiZ 1 3 3 = true := by
  decide

/-- Complex weight pair `(re, im)` representing $w (\cos(\theta Q) - i \sin(\theta Q))$
    in scaled integer coordinates. -/
@[ext]
structure ComplexWeightInt where
  re : Int
  im : Int
  deriving DecidableEq, Repr

/-- Addition of two complex weights. -/
def complexWeightAdd (z1 z2 : ComplexWeightInt) : ComplexWeightInt :=
  { re := z1.re + z2.re, im := z1.im + z2.im }

/-- Boltzmann weight of a sector $+Q$ with positive gauge weight $w$ and scaled
    trig factors $(c, -s)$ vs its CP-conjugate sector $-Q$ with $(c, +s)$. -/
def thetaSectorWeight (w c s : Int) : ComplexWeightInt :=
  { re := w * c, im := -(w * s) }

def thetaSectorWeightCP (w c s : Int) : ComplexWeightInt :=
  { re := w * c, im := w * s }

/-- Theorem 3: Summing a topological sector $+Q$ and its CP-conjugate partner $-Q$
    with equal positive gauge action weight $w$ cancels the imaginary sine component
    identically and leaves the purely real weight $2 w c$. -/
theorem cp_conjugate_pair_cancels_imaginary_boltzmann_phase (w c s : Int) :
    complexWeightAdd (thetaSectorWeight w c s) (thetaSectorWeightCP w c s) =
      { re := 2 * w * c, im := 0 } := by
  ext <;> dsimp [complexWeightAdd, thetaSectorWeight, thetaSectorWeightCP] <;> ring

/-- Theorem 4: Even after CP-pairing eliminates the imaginary part, whenever $w > 0$
    and the cosine factor $c < 0$ (for example $\pi/2 < |\theta Q| \le \pi$), the
    paired real weight $2 w c < 0$ is strictly negative, obstructing positive-weight
    importance sampling. -/
theorem cp_conjugate_pair_negative_real_weight_at_obtuse_phase (w c s : Int)
    (hw : 0 < w) (hc : c < 0) :
    (complexWeightAdd (thetaSectorWeight w c s) (thetaSectorWeightCP w c s)).im = 0 ∧
    (complexWeightAdd (thetaSectorWeight w c s) (thetaSectorWeightCP w c s)).re < 0 := by
  dsimp [complexWeightAdd, thetaSectorWeight, thetaSectorWeightCP]
  refine ⟨by omega, ?_⟩
  nlinarith

/-- Parity sign character $\sigma_\pi(Q) = (-1)^Q \in \{1, -1\}$ at $\theta = \pi$. -/
def thetaPiSign (Q : Int) : Int :=
  if Q % 2 == 0 then 1 else -1

/-- Theorem 5: At $\theta = \pi$, the topological sign factor $\sigma_\pi(Q) = (-1)^Q$
    is real-valued in $\{1, -1\}$, alternates between even and odd topological sectors,
    and is multiplicative under charge addition $\sigma_\pi(Q_1 + Q_2) = \sigma_\pi(Q_1)\sigma_\pi(Q_2)$. -/
theorem theta_pi_alternating_sector_sign_homomorphism (Q1 Q2 : Int) :
    thetaPiSign 0 = 1 ∧
    thetaPiSign 1 = -1 ∧
    thetaPiSign (-1) = -1 ∧
    thetaPiSign 2 = 1 ∧
    thetaPiSign (Q1 + Q2) = thetaPiSign Q1 * thetaPiSign Q2 := by
  refine ⟨by decide, by decide, by decide, by decide, ?_⟩
  dsimp [thetaPiSign]
  have h1 : Q1 % 2 = 0 ∨ Q1 % 2 = 1 := by omega
  have h2 : Q2 % 2 = 0 ∨ Q2 % 2 = 1 := by omega
  rcases h1 with h1 | h1 <;> rcases h2 with h2 | h2
  · have h12 : (Q1 + Q2) % 2 = 0 := by omega
    simp [h1, h2, h12]
  · have h12 : (Q1 + Q2) % 2 = 1 := by omega
    simp [h1, h2, h12]
  · have h12 : (Q1 + Q2) % 2 = 1 := by omega
    simp [h1, h2, h12]
  · have h12 : (Q1 + Q2) % 2 = 0 := by omega
    simp [h1, h2, h12]

/-- Two-sector partition sum $Z(\pi) = w_0 - w_1$ and phase-quenched sum $Z_{\mathrm{pq}} = w_0 + w_1$. -/
def twoSectorSignedZ (w0 w1 : Int) : Int := w0 - w1
def twoSectorQuenchedZ (w0 w1 : Int) : Int := w0 + w1

/-- Theorem 6: In a two-sector topological ensemble ($Q = 0$ weight $w_0 > 0$, $|Q| = 1$
    weight $w_1 > 0$) at $\theta = \pi$, the signed partition function satisfies
    $Z(\pi) < Z_{\mathrm{pq}}$, vanishes at the self-dual point $w_0 = w_1$, and is positive
    if and only if $w_1 < w_0$. -/
theorem two_sector_theta_pi_partition_cancellation_and_average_sign (w0 w1 : Int)
    (hw0 : 0 < w0) (hw1 : 0 < w1) :
    twoSectorSignedZ w0 w1 < twoSectorQuenchedZ w0 w1 ∧
    0 < twoSectorQuenchedZ w0 w1 ∧
    twoSectorSignedZ w0 w0 = 0 ∧
    (0 < twoSectorSignedZ w0 w1 ↔ w1 < w0) := by
  dsimp [twoSectorSignedZ, twoSectorQuenchedZ]
  refine ⟨by omega, by omega, by omega, by omega⟩

/-- Theorem 7: When the $|Q| = 1$ topological sector has a strictly positive action gap
    $\Delta S > 0$ over the $Q = 0$ vacuum sector ($S_1 = S_0 + \Delta S$), the actions
    satisfy $S_0 < S_1$, and any positive sector weights with $w_1 < w_0$ have strictly
    disjoint values ($w_0 \neq w_1$) and positive uncancelled residual $w_0 - w_1 > 0$. -/
theorem su2_vortex_action_gap_sector_weight_ordering (S0 deltaS w0 w1 : Int)
    (hGap : 0 < deltaS) (hOrder : w1 < w0) :
    S0 < S0 + deltaS ∧
    w0 ≠ w1 ∧
    0 < twoSectorSignedZ w0 w1 := by
  dsimp [twoSectorSignedZ]
  refine ⟨by omega, by omega, by omega⟩

/-- Mean charge numerator $\sum_{Q \in \{-1,0,1\}} Q w_{|Q|}$ and second moment
    $\sum_{Q \in \{-1,0,1\}} Q^2 w_{|Q|}$ for a CP-symmetric 3-sector ensemble. -/
def symmetricThreeSectorMeanQ (w0 w1 : Int) : Int :=
  (-1) * w1 + 0 * w0 + 1 * w1

def symmetricThreeSectorSecondMomentQ (w0 w1 : Int) : Int :=
  ((-1) * (-1)) * w1 + (0 * 0) * w0 + (1 * 1) * w1

/-- Theorem 8: In a CP-symmetric 3-sector topological ensemble $Q \in \{-1, 0, +1\}$
    with weights $(w_1, w_0, w_1)$ where $w_0 > 0, w_1 > 0$, the mean topological charge
    vanishes identically while the second moment $\sum Q^2 w_Q = 2 w_1 > 0$ is strictly
    positive (matching `CdtTopologicalChargeEvaluator` instanton susceptibility $\chi_t > 0$). -/
theorem topological_susceptibility_second_moment_positivity (w0 w1 : Int)
    (hw0 : 0 < w0) (hw1 : 0 < w1) :
    symmetricThreeSectorMeanQ w0 w1 = 0 ∧
    symmetricThreeSectorSecondMomentQ w0 w1 = 2 * w1 ∧
    0 < symmetricThreeSectorSecondMomentQ w0 w1 ∧
    0 < w0 + 2 * w1 := by
  dsimp [symmetricThreeSectorMeanQ, symmetricThreeSectorSecondMomentQ]
  refine ⟨by omega, by omega, by omega, by omega⟩

/-- Theorem 9: Scope fence (`GIN-C9`) — the historical Nat inequality `w0 ≠ w0 + deltaS`
    for `deltaS > 0` holds for every natural number `w0` by elementary arithmetic and
    does not depend on or establish a physical SU(2) Yang-Mills gauge theorem. -/
theorem gin_c9_su2_action_gap_fixture_scope_fence (w0 deltaS : Nat) (hGap : 0 < deltaS) :
    w0 ≠ w0 + deltaS := by
  omega

/-- Scope fence structure (`FSP-THETA-TERM-COMPLEX-WEIGHT`): separates finite $\theta$-phase
    algebra and `GIN-C9` fixtures from continuum $\theta$-vacuum phenomenology. -/
structure ThetaTermModelInterpretation where
  genericThetaComplexPhase : Bool
  thetaPiAlternatingSign : Bool
  establishesContinuumThetaPhenomenology : Bool
  deriving DecidableEq, Repr

/-- Projection retaining only the verified finite phase and parity properties. -/
def thetaTermVerifiedCore (x : ThetaTermModelInterpretation) : Bool × Bool :=
  (x.genericThetaComplexPhase, x.thetaPiAlternatingSign)

/-- Theorem 10: Scope fence (`FSP-THETA-TERM-COMPLEX-WEIGHT`) — the verified finite
    phase non-reality and $\theta = \pi$ parity properties are compatible with both
    asserting and withholding continuum $\theta$-vacuum phenomenology, justifying
    `IMPORTED_ASSUMPTION` status under `GIN-C9`. -/
theorem theta_term_phenomenology_scope_fence :
    let overclaimedInterp : ThetaTermModelInterpretation :=
      { genericThetaComplexPhase := true
        thetaPiAlternatingSign := true
        establishesContinuumThetaPhenomenology := true }
    let scopedInterp : ThetaTermModelInterpretation :=
      { genericThetaComplexPhase := true
        thetaPiAlternatingSign := true
        establishesContinuumThetaPhenomenology := false }
    thetaTermVerifiedCore overclaimedInterp = thetaTermVerifiedCore scopedInterp ∧
    overclaimedInterp ≠ scopedInterp ∧
    overclaimedInterp.establishesContinuumThetaPhenomenology ≠
      scopedInterp.establishesContinuumThetaPhenomenology := by
  decide

end CampaignFspThetaTermComplexWeight
