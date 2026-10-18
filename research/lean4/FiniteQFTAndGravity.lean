/- FiniteQFTAndGravity.lean — finite rational maps for Goals 4 through 9
   (QM-226 .. QM-231) of the Finite Quantum Mechanics 10-Goal Roadmap.

   AuthorityEffect: None.

   Scope: core Lean 4 only, no imports. Every theorem is a closed identity over Rat,
   over the Gaussian rationals (pairs of Rat) or over Int, discharged by `grind`,
   `ext`, `decide`, `split` or `omega`. Transcendental constants (pi, ln, square
   roots) do not appear here: their rational interval enclosures live in the Rust
   and Python finite maps (qed_weak_hadronic_finite_maps.rs,
   regge_gravity_ghz_chern_finite_maps.rs and the matching use cases). The CKM
   Cayley transform over Q(i), the Fermi-constant enclosure, the 8 x 8 GHZ
   eigenvector checks and the 4-tick Page-Wootters history constraint are checked
   in Rust and Python only; this file carries the scalar, 2 x 2 and 4 x 4 pieces
   that those checks rest on. Statements are about constructed objects (tensors,
   matrices, channel applications), not about bare numerals.

   Track A (QM-226, QM-227, QM-228): Klein-Nishina ratio, Thomson limit and
   normalization, Bhabha/Moller crossing, chiral projectors in the Weyl basis,
   muon phase-space factor, Adler-Bell-Jackiw colour factor, Gell-Mann-Okubo
   octet and decuplet identities.
   Track B (QM-229, QM-230, QM-231): PPN deflection and perihelion factors, the
   Minkowski trace of a constructed flow tensor e k k (null probe and dust), the
   cyclic clock shift, Pauli single-site identities behind the GHZ sign, the
   Mermin bound over all 64 deterministic assignments, the rational-Gaussian
   Page-Wootters step unitary, three applications of the Pythagorean
   phase-damping channel, and the QWZ Chern-number parity table. -/

namespace FiniteQFTAndGravity

-- =============================================================================
-- QM-226 (Goal 4): Klein-Nishina ratio, Thomson limit, Bhabha/Moller crossing
-- =============================================================================

/-- Klein-Nishina ratio R(x, u) = (1/2) eta^2 (eta + 1/eta - (1 - u^2)) in
    division-free form. eta is the frequency ratio 1 / (1 + x (1 - u)), so 1/eta
    is 1 + x (1 - u) and enters as that polynomial. -/
abbrev knRatio (x u eta : Rat) : Rat :=
  (1 / 2) * eta * eta * (eta + (1 + x * (1 - u)) - (1 - u * u))

/-- With eta (1 + x (1 - u)) = 1 and eta nonzero, the division-free form agrees
    with the textbook expression containing 1/eta. -/
theorem kn_textbook_form (x u eta : Rat) (_heta : eta ≠ 0)
    (h : eta * (1 + x * (1 - u)) = 1) :
    (1 / 2) * eta * eta * (eta + 1 / eta - (1 - u * u)) = knRatio x u eta := by
  grind

/-- The defining relation of eta at u = 1 forces eta = 1 for every x. -/
theorem kn_forward_eta (x eta : Rat) (h : eta * (1 + x * (1 - 1)) = 1) : eta = 1 := by
  grind

/-- Forward scattering (u = 1, eta = 1): R(x, 1) = 1 for every x. -/
theorem kn_forward (x : Rat) : knRatio x 1 1 = 1 := by
  grind

/-- The defining relation of eta at x = 0 forces eta = 1 for every u. -/
theorem kn_thomson_eta (u eta : Rat) (h : eta * (1 + 0 * (1 - u)) = 1) : eta = 1 := by
  grind

/-- Thomson limit (x = 0, eta = 1): R(0, u) = (1 + u^2) / 2. -/
theorem kn_thomson (u : Rat) : knRatio 0 u 1 = (1 + u * u) / 2 := by
  grind

/-- Sample values at x in {1/10, 1, 2} and u in {-1, 0}, eta = 1 / (1 + x (1 - u)). -/
theorem kn_samples :
    knRatio 1 0 (1 / 2) = 3 / 16 ∧
    knRatio 1 (-1) (1 / 3) = 5 / 27 ∧
    knRatio 2 0 (1 / 3) = 7 / 54 ∧
    knRatio 2 (-1) (1 / 5) = 13 / 125 ∧
    knRatio (1 / 10) 0 (10 / 11) = 555 / 1331 ∧
    knRatio (1 / 10) (-1) (5 / 6) = 305 / 432 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> grind

/-- Each eta used in `kn_samples` satisfies its defining relation. -/
theorem kn_sample_etas :
    (1 / 2 : Rat) * (1 + 1 * (1 - 0)) = 1 ∧
    (1 / 3 : Rat) * (1 + 1 * (1 - (-1))) = 1 ∧
    (1 / 3 : Rat) * (1 + 2 * (1 - 0)) = 1 ∧
    (1 / 5 : Rat) * (1 + 2 * (1 - (-1))) = 1 ∧
    (10 / 11 : Rat) * (1 + (1 / 10) * (1 - 0)) = 1 ∧
    (5 / 6 : Rat) * (1 + (1 / 10) * (1 - (-1))) = 1 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> grind

/-- Antiderivative of the normalized Thomson weight (3/8)(1 + u^2):
    F(u) = (3/8)(u + u^3/3). -/
abbrev thomsonAntiderivative (u : Rat) : Rat :=
  (3 / 8) * (u + u * u * u / 3)

/-- The normalized Thomson weight integrates to one over u in [-1, 1]:
    F(1) - F(-1) = 1. -/
theorem thomson_normalized :
    thomsonAntiderivative 1 - thomsonAntiderivative (-1) = 1 := by
  grind

/-- The normalized weight is (3/4) times the Thomson ratio R(0, u). -/
theorem thomson_weight_vs_ratio (u : Rat) :
    (3 / 8) * (1 + u * u) = (3 / 4) * knRatio 0 u 1 := by
  grind

/-- Exact finite difference of the antiderivative: F(u + h) - F(u) is h times the
    weight plus the explicit remainder (3/8)(u h^2 + h^3/3). -/
theorem thomson_antiderivative_difference (u h : Rat) :
    thomsonAntiderivative (u + h) - thomsonAntiderivative u
      = h * ((3 / 8) * (1 + u * u)) + (3 / 8) * (u * h * h + h * h * h / 3) := by
  grind

/-- Tree-level Bhabha amplitude (spin-averaged, massless, units of 2 e^4):
    M = 2 ((s^2 + u^2)/t^2 + 2 u^2/(s t) + (t^2 + u^2)/s^2). -/
abbrev bhabha (s t u : Rat) : Rat :=
  2 * ((s * s + u * u) / (t * t) + 2 * u * u / (s * t) + (t * t + u * u) / (s * s))

/-- Tree-level Moller amplitude in the same units:
    M = 2 ((s^2 + u^2)/t^2 + 2 s^2/(t u) + (s^2 + t^2)/u^2). -/
abbrev moller (s t u : Rat) : Rat :=
  2 * ((s * s + u * u) / (t * t) + 2 * s * s / (t * u) + (s * s + t * t) / (u * u))

/-- Crossing: Moller is Bhabha with s and u exchanged (t fixed). -/
theorem moller_eq_bhabha_su (s t u : Rat) (_ht : t ≠ 0) (_hu : u ≠ 0) :
    moller s t u = bhabha u t s := by
  grind

/-- Moller is symmetric under t <-> u (identical final-state electrons). -/
theorem moller_tu_symmetric (s t u : Rat) (_ht : t ≠ 0) (_hu : u ≠ 0) :
    moller s t u = moller s u t := by
  grind

/-- Crossing at the sample point (s, t, u) = (5, -2, -3): both sides are 361/9. -/
theorem crossing_sample :
    moller 5 (-2) (-3) = 361 / 9 ∧ bhabha (-3) (-2) 5 = 361 / 9 := by
  refine ⟨?_, ?_⟩ <;> grind

/-- The s <-> t exchange is not the crossing: at (5, -2, -3) Bhabha is 361/25 while
    Moller at (-2, 5, -3) is 1444/225, and the two differ. -/
theorem crossing_st_witness :
    bhabha 5 (-2) (-3) = 361 / 25 ∧
    moller (-2) 5 (-3) = 1444 / 225 ∧
    bhabha 5 (-2) (-3) ≠ moller (-2) 5 (-3) := by
  refine ⟨?_, ?_, ?_⟩ <;> grind

-- =============================================================================
-- QM-227 (Goal 5): chiral projectors in the Weyl basis, muon phase space
-- =============================================================================

/-- 4 x 4 rational matrix, row-major entries a_ij. -/
@[ext] structure Mat4Rat where
  a00 : Rat
  a01 : Rat
  a02 : Rat
  a03 : Rat
  a10 : Rat
  a11 : Rat
  a12 : Rat
  a13 : Rat
  a20 : Rat
  a21 : Rat
  a22 : Rat
  a23 : Rat
  a30 : Rat
  a31 : Rat
  a32 : Rat
  a33 : Rat
  deriving DecidableEq, Repr

namespace Mat4Rat

abbrev zero : Mat4Rat :=
  ⟨0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0⟩

abbrev id : Mat4Rat :=
  ⟨1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 1, 0,  0, 0, 0, 1⟩

abbrev add (A B : Mat4Rat) : Mat4Rat where
    a00 := A.a00 + B.a00
    a01 := A.a01 + B.a01
    a02 := A.a02 + B.a02
    a03 := A.a03 + B.a03
    a10 := A.a10 + B.a10
    a11 := A.a11 + B.a11
    a12 := A.a12 + B.a12
    a13 := A.a13 + B.a13
    a20 := A.a20 + B.a20
    a21 := A.a21 + B.a21
    a22 := A.a22 + B.a22
    a23 := A.a23 + B.a23
    a30 := A.a30 + B.a30
    a31 := A.a31 + B.a31
    a32 := A.a32 + B.a32
    a33 := A.a33 + B.a33

abbrev sub (A B : Mat4Rat) : Mat4Rat where
    a00 := A.a00 - B.a00
    a01 := A.a01 - B.a01
    a02 := A.a02 - B.a02
    a03 := A.a03 - B.a03
    a10 := A.a10 - B.a10
    a11 := A.a11 - B.a11
    a12 := A.a12 - B.a12
    a13 := A.a13 - B.a13
    a20 := A.a20 - B.a20
    a21 := A.a21 - B.a21
    a22 := A.a22 - B.a22
    a23 := A.a23 - B.a23
    a30 := A.a30 - B.a30
    a31 := A.a31 - B.a31
    a32 := A.a32 - B.a32
    a33 := A.a33 - B.a33

abbrev smul (c : Rat) (A : Mat4Rat) : Mat4Rat where
    a00 := c * A.a00
    a01 := c * A.a01
    a02 := c * A.a02
    a03 := c * A.a03
    a10 := c * A.a10
    a11 := c * A.a11
    a12 := c * A.a12
    a13 := c * A.a13
    a20 := c * A.a20
    a21 := c * A.a21
    a22 := c * A.a22
    a23 := c * A.a23
    a30 := c * A.a30
    a31 := c * A.a31
    a32 := c * A.a32
    a33 := c * A.a33

abbrev mul (A B : Mat4Rat) : Mat4Rat where
    a00 := A.a00 * B.a00 + A.a01 * B.a10 + A.a02 * B.a20 + A.a03 * B.a30
    a01 := A.a00 * B.a01 + A.a01 * B.a11 + A.a02 * B.a21 + A.a03 * B.a31
    a02 := A.a00 * B.a02 + A.a01 * B.a12 + A.a02 * B.a22 + A.a03 * B.a32
    a03 := A.a00 * B.a03 + A.a01 * B.a13 + A.a02 * B.a23 + A.a03 * B.a33
    a10 := A.a10 * B.a00 + A.a11 * B.a10 + A.a12 * B.a20 + A.a13 * B.a30
    a11 := A.a10 * B.a01 + A.a11 * B.a11 + A.a12 * B.a21 + A.a13 * B.a31
    a12 := A.a10 * B.a02 + A.a11 * B.a12 + A.a12 * B.a22 + A.a13 * B.a32
    a13 := A.a10 * B.a03 + A.a11 * B.a13 + A.a12 * B.a23 + A.a13 * B.a33
    a20 := A.a20 * B.a00 + A.a21 * B.a10 + A.a22 * B.a20 + A.a23 * B.a30
    a21 := A.a20 * B.a01 + A.a21 * B.a11 + A.a22 * B.a21 + A.a23 * B.a31
    a22 := A.a20 * B.a02 + A.a21 * B.a12 + A.a22 * B.a22 + A.a23 * B.a32
    a23 := A.a20 * B.a03 + A.a21 * B.a13 + A.a22 * B.a23 + A.a23 * B.a33
    a30 := A.a30 * B.a00 + A.a31 * B.a10 + A.a32 * B.a20 + A.a33 * B.a30
    a31 := A.a30 * B.a01 + A.a31 * B.a11 + A.a32 * B.a21 + A.a33 * B.a31
    a32 := A.a30 * B.a02 + A.a31 * B.a12 + A.a32 * B.a22 + A.a33 * B.a32
    a33 := A.a30 * B.a03 + A.a31 * B.a13 + A.a32 * B.a23 + A.a33 * B.a33

abbrev tr (A : Mat4Rat) : Rat := A.a00 + A.a11 + A.a22 + A.a33

end Mat4Rat

/-- Rational 4-vector. -/
@[ext] structure Vec4Rat where
  v0 : Rat
  v1 : Rat
  v2 : Rat
  v3 : Rat
  deriving DecidableEq, Repr

abbrev Vec4Rat.zero : Vec4Rat := ⟨0, 0, 0, 0⟩

/-- Matrix-vector action. -/
abbrev Mat4Rat.mulVec (A : Mat4Rat) (v : Vec4Rat) : Vec4Rat where
    v0 := A.a00 * v.v0 + A.a01 * v.v1 + A.a02 * v.v2 + A.a03 * v.v3
    v1 := A.a10 * v.v0 + A.a11 * v.v1 + A.a12 * v.v2 + A.a13 * v.v3
    v2 := A.a20 * v.v0 + A.a21 * v.v1 + A.a22 * v.v2 + A.a23 * v.v3
    v3 := A.a30 * v.v0 + A.a31 * v.v1 + A.a32 * v.v2 + A.a33 * v.v3

/-- gamma5 in the Weyl (chiral) basis: diag(-1, -1, 1, 1). -/
abbrev gamma5 : Mat4Rat :=
  ⟨-1, 0, 0, 0,  0, -1, 0, 0,  0, 0, 1, 0,  0, 0, 0, 1⟩

/-- Left chiral projector P_L = (I - gamma5) / 2. -/
abbrev projL : Mat4Rat := Mat4Rat.smul (1 / 2) (Mat4Rat.sub Mat4Rat.id gamma5)

/-- Right chiral projector P_R = (I + gamma5) / 2. -/
abbrev projR : Mat4Rat := Mat4Rat.smul (1 / 2) (Mat4Rat.add Mat4Rat.id gamma5)

theorem gamma5_squared : Mat4Rat.mul gamma5 gamma5 = Mat4Rat.id := by
  ext <;> grind

theorem gamma5_traceless : Mat4Rat.tr gamma5 = 0 := by
  grind

/-- Idempotent, mutually orthogonal, complete, each of trace 2. -/
theorem chiral_projectors :
    Mat4Rat.mul projL projL = projL ∧
    Mat4Rat.mul projR projR = projR ∧
    Mat4Rat.mul projL projR = Mat4Rat.zero ∧
    Mat4Rat.mul projR projL = Mat4Rat.zero ∧
    Mat4Rat.add projL projR = Mat4Rat.id ∧
    Mat4Rat.tr projL = 2 ∧
    Mat4Rat.tr projR = 2 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind
  · grind
  · grind

/-- Explicit forms: P_L = diag(1, 1, 0, 0), P_R = diag(0, 0, 1, 1). -/
theorem chiral_projectors_explicit :
    projL = ⟨1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0⟩ ∧
    projR = ⟨0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 1, 0,  0, 0, 0, 1⟩ := by
  refine ⟨?_, ?_⟩ <;> ext <;> grind

/-- P_L (P_R v) = 0 for every rational 4-vector v. -/
theorem projL_projR_vec (v : Vec4Rat) :
    Mat4Rat.mulVec projL (Mat4Rat.mulVec projR v) = Vec4Rat.zero := by
  ext <;> grind

/-- Muon-decay phase-space factor f0(x) = 1 - 8 x + 8 x^3 - x^4, x = (m_e/m_mu)^2. -/
abbrev muonF0 (x : Rat) : Rat := 1 - 8 * x + 8 * x * x * x - x * x * x * x

theorem muonF0_endpoints : muonF0 0 = 1 ∧ muonF0 1 = 0 := by
  refine ⟨?_, ?_⟩ <;> grind

/-- f0 factors through (1 - x): f0(x) = (1 - x)(1 - 7 x - 7 x^2 + x^3). -/
theorem muonF0_factor (x : Rat) :
    muonF0 x = (1 - x) * (1 - 7 * x - 7 * x * x + x * x * x) := by
  grind

/-- One-loop sign: the bracket 25/4 - pi^2 is negative for any rational lower
    bound p of pi with p > 5/2 (the enclosures in the Rust and Python maps give
    p > 3). -/
theorem muon_qed_correction_negative (p : Rat) (hp : 5 / 2 < p) :
    25 / 4 - p * p < 0 := by
  have h1 : 0 ≤ p - 5 / 2 := by grind
  have h3 : 0 ≤ (p - 5 / 2) * (p - 5 / 2) := Rat.mul_nonneg h1 h1
  grind

-- =============================================================================
-- QM-228 (Goal 6): ABJ colour factor and Gell-Mann-Okubo identities
-- =============================================================================

/-- Anomaly factor S(N_c) = N_c (Q_u^2 - Q_d^2) with Q_u = 2/3 and Q_d = -1/3. -/
abbrev abjFactor (nc : Rat) : Rat := nc * ((2 / 3) * (2 / 3) - (-1 / 3) * (-1 / 3))

theorem abj_factor_closed (nc : Rat) : abjFactor nc = nc / 3 := by
  grind

theorem abj_factor_values : abjFactor 3 = 1 ∧ abjFactor 1 = 1 / 3 := by
  refine ⟨?_, ?_⟩ <;> grind

/-- The pi0 -> gamma gamma rate scales as S^2, so N_c = 3 against N_c = 1 is a
    factor 9. -/
theorem abj_rate_ratio :
    abjFactor 3 * abjFactor 3 = 9 * (abjFactor 1 * abjFactor 1) := by
  grind

/-- Gell-Mann-Okubo mass operator M = M0 + M1 Y + M2 (I (I + 1) - Y^2 / 4). -/
abbrev gmoMass (m0 m1 m2 i y : Rat) : Rat :=
  m0 + m1 * y + m2 * (i * (i + 1) - y * y / 4)

/-- Octet relation 2 (M_N + M_Xi) = 3 M_Lambda + M_Sigma with
    (I, Y) = (1/2, 1), (1/2, -1), (0, 0), (1, 0). -/
theorem gmo_octet (m0 m1 m2 : Rat) :
    2 * (gmoMass m0 m1 m2 (1 / 2) 1 + gmoMass m0 m1 m2 (1 / 2) (-1))
      = 3 * gmoMass m0 m1 m2 0 0 + gmoMass m0 m1 m2 1 0 := by
  grind

/-- Decuplet equal spacing: Delta (3/2, 1), Sigma* (1, 0), Xi* (1/2, -1),
    Omega (0, -2). -/
theorem gmo_decuplet_equal_spacing (m0 m1 m2 : Rat) :
    gmoMass m0 m1 m2 1 0 - gmoMass m0 m1 m2 (3 / 2) 1
        = gmoMass m0 m1 m2 (1 / 2) (-1) - gmoMass m0 m1 m2 1 0 ∧
    gmoMass m0 m1 m2 (1 / 2) (-1) - gmoMass m0 m1 m2 1 0
        = gmoMass m0 m1 m2 0 (-2) - gmoMass m0 m1 m2 (1 / 2) (-1) := by
  refine ⟨?_, ?_⟩ <;> grind

/-- The common decuplet spacing is -(M1 + 3 M2 / 2). -/
theorem gmo_decuplet_spacing_value (m0 m1 m2 : Rat) :
    gmoMass m0 m1 m2 1 0 - gmoMass m0 m1 m2 (3 / 2) 1 = -(m1 + 3 * m2 / 2) := by
  grind

/-- Omega prediction from the spacing: M_Omega = 2 M_Xi* - M_Sigma*. -/
theorem gmo_omega_from_spacing (m0 m1 m2 : Rat) :
    gmoMass m0 m1 m2 0 (-2)
      = 2 * gmoMass m0 m1 m2 (1 / 2) (-1) - gmoMass m0 m1 m2 1 0 := by
  grind

-- =============================================================================
-- QM-229 (Goal 7): PPN deflection and perihelion factors, clock shift
-- =============================================================================

/-- Light-deflection PPN factor (1 + gamma) / 2. -/
abbrev deflectionFactor (gamma : Rat) : Rat := (1 + gamma) / 2

/-- Perihelion PPN factor (2 + 2 gamma - beta) / 3. -/
abbrev perihelionFactor (gamma beta : Rat) : Rat := (2 + 2 * gamma - beta) / 3

theorem deflection_factor_values :
    deflectionFactor 1 = 1 ∧
    deflectionFactor 0 = 1 / 2 ∧
    deflectionFactor 1 = 2 * deflectionFactor 0 := by
  refine ⟨?_, ?_, ?_⟩ <;> grind

/-- Newtonian deflection 2 G M / (c^2 b). -/
abbrev newtonDeflection (gm c b : Rat) : Rat := 2 * gm / (c * c * b)

/-- GR deflection 4 G M / (c^2 b). -/
abbrev grDeflection (gm c b : Rat) : Rat := 4 * gm / (c * c * b)

/-- delta_GR = 2 delta_Newton, and the PPN factor at gamma = 0 gives the
    Newtonian value from the GR one. -/
theorem gr_deflection_twice_newton (gm c b : Rat) (_hc : c ≠ 0) (_hb : b ≠ 0) :
    grDeflection gm c b = 2 * newtonDeflection gm c b ∧
    newtonDeflection gm c b = deflectionFactor 0 * grDeflection gm c b := by
  refine ⟨?_, ?_⟩ <;> grind

/-- Stress tensor e k^mu k^nu of a pressureless flow with four-vector k. -/
abbrev flowTensor (e : Rat) (k : Vec4Rat) : Mat4Rat :=
  ⟨e * k.v0 * k.v0, e * k.v0 * k.v1, e * k.v0 * k.v2, e * k.v0 * k.v3,
   e * k.v1 * k.v0, e * k.v1 * k.v1, e * k.v1 * k.v2, e * k.v1 * k.v3,
   e * k.v2 * k.v0, e * k.v2 * k.v1, e * k.v2 * k.v2, e * k.v2 * k.v3,
   e * k.v3 * k.v0, e * k.v3 * k.v1, e * k.v3 * k.v2, e * k.v3 * k.v3⟩

/-- Minkowski trace eta_{mu nu} T^{mu nu} with signature (+, -, -, -). -/
abbrev minkowskiTrace (t : Mat4Rat) : Rat := t.a00 - t.a11 - t.a22 - t.a33

/-- Minkowski norm eta(k, k) with signature (+, -, -, -). -/
abbrev minkowskiNorm (k : Vec4Rat) : Rat :=
  k.v0 * k.v0 - k.v1 * k.v1 - k.v2 * k.v2 - k.v3 * k.v3

/-- The Minkowski trace of e k k is e eta(k, k), for every e and k. -/
theorem flow_tensor_trace (e : Rat) (k : Vec4Rat) :
    minkowskiTrace (flowTensor e k) = e * minkowskiNorm k := by
  grind

/-- Null probe k = (1, 1, 0, 0): T^00 = T^11 = E, and the trace vanishes for every
    energy E. -/
theorem null_probe_traceless (e : Rat) :
    (flowTensor e ⟨1, 1, 0, 0⟩).a00 = e ∧
    (flowTensor e ⟨1, 1, 0, 0⟩).a11 = e ∧
    minkowskiTrace (flowTensor e ⟨1, 1, 0, 0⟩) = 0 := by
  refine ⟨?_, ?_, ?_⟩ <;> grind

/-- Dust at rest, u = (1, 0, 0, 0): the trace is rho, so dust with rho ≠ 0 is not
    traceless. -/
theorem dust_trace (rho : Rat) :
    minkowskiTrace (flowTensor rho ⟨1, 0, 0, 0⟩) = rho := by
  grind

theorem perihelion_factor_gr : perihelionFactor 1 1 = 1 := by
  grind

/-- Mercury precession per orbit in arcseconds: 6 pi G M / (a (1 - e^2) c^2)
    radians times 648000 / pi arcseconds per radian, so pi cancels:
    ((2 + 2 gamma - beta)/3) * 6 * 648000 G M / (a (1 - e^2) c^2) at
    gamma = beta = 1. -/
abbrev mercuryPerOrbitArcsec (gm a e c : Rat) : Rat :=
  perihelionFactor 1 1 * (6 * 648000) * gm / (a * (1 - e * e) * c * c)

theorem mercury_per_orbit_arcsec (gm a e c : Rat) :
    mercuryPerOrbitArcsec gm a e c = 3888000 * gm / (a * (1 - e * e) * c * c) := by
  grind

/-- Cyclic lowering shift on four clock ticks, S |t> = |t - 1 mod 4>. -/
abbrev clockShift : Mat4Rat :=
  ⟨0, 1, 0, 0,  0, 0, 1, 0,  0, 0, 0, 1,  1, 0, 0, 0⟩

theorem clock_shift_action :
    Mat4Rat.mulVec clockShift ⟨0, 1, 0, 0⟩ = ⟨1, 0, 0, 0⟩ ∧
    Mat4Rat.mulVec clockShift ⟨1, 0, 0, 0⟩ = ⟨0, 0, 0, 1⟩ := by
  refine ⟨?_, ?_⟩ <;> ext <;> grind

theorem clock_shift_order_four :
    Mat4Rat.mul clockShift (Mat4Rat.mul clockShift (Mat4Rat.mul clockShift clockShift))
      = Mat4Rat.id := by
  ext <;> grind

theorem clock_shift_not_id : clockShift ≠ Mat4Rat.id := by
  grind

-- =============================================================================
-- QM-230 (Goal 8): Pauli identities behind the GHZ sign, Mermin bound,
--                  Page-Wootters step unitary, Pythagorean phase damping
-- =============================================================================

/-- Gaussian rational re + im i. -/
@[ext] structure GRat where
  re : Rat
  im : Rat
  deriving DecidableEq, Repr

namespace GRat

abbrev zero : GRat := ⟨0, 0⟩
abbrev one : GRat := ⟨1, 0⟩
abbrev i : GRat := ⟨0, 1⟩
abbrev add (x y : GRat) : GRat := ⟨x.re + y.re, x.im + y.im⟩
abbrev neg (x : GRat) : GRat := ⟨-x.re, -x.im⟩
abbrev mul (x y : GRat) : GRat :=
  ⟨x.re * y.re - x.im * y.im, x.re * y.im + x.im * y.re⟩
abbrev conj (x : GRat) : GRat := ⟨x.re, -x.im⟩

end GRat

theorem grat_i_squared : GRat.mul GRat.i GRat.i = GRat.neg GRat.one := by
  ext <;> grind

/-- 2 x 2 matrix over the Gaussian rationals. -/
@[ext] structure GMat2 where
  a00 : GRat
  a01 : GRat
  a10 : GRat
  a11 : GRat
  deriving DecidableEq, Repr

namespace GMat2

abbrev id : GMat2 := ⟨GRat.one, GRat.zero, GRat.zero, GRat.one⟩

abbrev neg (A : GMat2) : GMat2 :=
  ⟨GRat.neg A.a00, GRat.neg A.a01, GRat.neg A.a10, GRat.neg A.a11⟩

abbrev add (A B : GMat2) : GMat2 :=
  ⟨GRat.add A.a00 B.a00, GRat.add A.a01 B.a01, GRat.add A.a10 B.a10, GRat.add A.a11 B.a11⟩

abbrev mul (A B : GMat2) : GMat2 :=
  ⟨GRat.add (GRat.mul A.a00 B.a00) (GRat.mul A.a01 B.a10),
   GRat.add (GRat.mul A.a00 B.a01) (GRat.mul A.a01 B.a11),
   GRat.add (GRat.mul A.a10 B.a00) (GRat.mul A.a11 B.a10),
   GRat.add (GRat.mul A.a10 B.a01) (GRat.mul A.a11 B.a11)⟩

/-- Conjugate transpose. -/
abbrev dagger (A : GMat2) : GMat2 :=
  ⟨GRat.conj A.a00, GRat.conj A.a10, GRat.conj A.a01, GRat.conj A.a11⟩

end GMat2

abbrev pauliX : GMat2 := ⟨GRat.zero, GRat.one, GRat.one, GRat.zero⟩
abbrev pauliY : GMat2 := ⟨GRat.zero, GRat.neg GRat.i, GRat.i, GRat.zero⟩
abbrev pauliZ : GMat2 := ⟨GRat.one, GRat.zero, GRat.zero, GRat.neg GRat.one⟩

theorem pauli_squares :
    GMat2.mul pauliX pauliX = GMat2.id ∧
    GMat2.mul pauliY pauliY = GMat2.id ∧
    GMat2.mul pauliZ pauliZ = GMat2.id := by
  refine ⟨?_, ?_, ?_⟩ <;> ext <;> grind

/-- Single-site products behind A1 A2 A3 = -B for A1 = X Y Y, A2 = Y X Y,
    A3 = Y Y X, B = X X X (site by site): X Y Y = X, Y X Y = -X, Y Y X = X,
    so the three-fold Kronecker product carries exactly one minus sign. -/
theorem pauli_ghz_sites :
    GMat2.mul pauliX (GMat2.mul pauliY pauliY) = pauliX ∧
    GMat2.mul pauliY (GMat2.mul pauliX pauliY) = GMat2.neg pauliX ∧
    GMat2.mul pauliY (GMat2.mul pauliY pauliX) = pauliX := by
  refine ⟨?_, ?_, ?_⟩ <;> ext <;> grind

/-- X and Y anticommute: X Y = -Y X. -/
theorem pauli_xy_anticommute :
    GMat2.mul pauliX pauliY = GMat2.neg (GMat2.mul pauliY pauliX) := by
  ext <;> grind

/-- Mermin combination x1 x2 x3 - x1 y2 y3 - y1 x2 y3 - y1 y2 x3 over Int. -/
abbrev merminCombo (x1 x2 x3 y1 y2 y3 : Int) : Int :=
  x1 * x2 * x3 - x1 * y2 * y3 - y1 * x2 * y3 - y1 * y2 * x3

/-- Every deterministic +-1 assignment gives a Mermin value in [-2, 2]
    (all 64 cases by case split). -/
theorem mermin_deterministic_bound (x1 x2 x3 y1 y2 y3 : Int)
    (h1 : x1 = 1 ∨ x1 = -1) (h2 : x2 = 1 ∨ x2 = -1) (h3 : x3 = 1 ∨ x3 = -1)
    (h4 : y1 = 1 ∨ y1 = -1) (h5 : y2 = 1 ∨ y2 = -1) (h6 : y3 = 1 ∨ y3 = -1) :
    -2 ≤ merminCombo x1 x2 x3 y1 y2 y3 ∧ merminCombo x1 x2 x3 y1 y2 y3 ≤ 2 := by
  rcases h1 with rfl | rfl <;> rcases h2 with rfl | rfl <;> rcases h3 with rfl | rfl <;>
    rcases h4 with rfl | rfl <;> rcases h5 with rfl | rfl <;> rcases h6 with rfl | rfl <;>
    decide

/-- The deterministic bound is attained at both ends. -/
theorem mermin_bound_attained :
    merminCombo 1 1 1 1 1 1 = -2 ∧ merminCombo (-1) 1 1 (-1) 1 1 = 2 := by
  decide

/-- Rational-Gaussian unitary W = (1/5) [[3, 4 i], [4 i, 3]]. -/
abbrev pwFrame : GMat2 :=
  ⟨⟨3 / 5, 0⟩, ⟨0, 4 / 5⟩, ⟨0, 4 / 5⟩, ⟨3 / 5, 0⟩⟩

/-- Eigenvalue matrix diag(1, i), an order-four phase. -/
abbrev pwPhase : GMat2 := ⟨GRat.one, GRat.zero, GRat.zero, GRat.i⟩

/-- Page-Wootters step unitary U = W diag(1, i) W^dagger
    = (1/25) [[9 + 16 i, -12 - 12 i], [12 + 12 i, 16 + 9 i]]. -/
abbrev stepUnitary : GMat2 :=
  ⟨⟨9 / 25, 16 / 25⟩, ⟨-12 / 25, -12 / 25⟩, ⟨12 / 25, 12 / 25⟩, ⟨16 / 25, 9 / 25⟩⟩

theorem pw_frame_unitary : GMat2.mul pwFrame (GMat2.dagger pwFrame) = GMat2.id := by
  ext <;> grind

theorem step_unitary_factorization :
    GMat2.mul (GMat2.mul pwFrame pwPhase) (GMat2.dagger pwFrame) = stepUnitary := by
  ext <;> grind

theorem step_unitary_unitary :
    GMat2.mul stepUnitary (GMat2.dagger stepUnitary) = GMat2.id := by
  ext <;> grind

/-- U^4 = I, as the four-tick cyclic history requires. -/
theorem step_unitary_order_four :
    GMat2.mul stepUnitary (GMat2.mul stepUnitary (GMat2.mul stepUnitary stepUnitary))
      = GMat2.id := by
  ext <;> grind

/-- Phase damping with 1 - lambda = p^2/q^2 and lambda = r^2/q^2 on a Pythagorean
    triple: K0 = diag(1, p/q), K1 = diag(0, r/q), and trace preservation is
    (p/q)^2 + (r/q)^2 = 1. -/
theorem phase_damping_trace_preserving (p r q : Rat) (_hq : q ≠ 0)
    (h : p * p + r * r = q * q) :
    (p / q) * (p / q) + (r / q) * (r / q) = 1 := by
  grind

theorem phase_damping_triples :
    (3 / 5 : Rat) * (3 / 5) + (4 / 5) * (4 / 5) = 1 ∧
    (5 / 13 : Rat) * (5 / 13) + (12 / 13) * (12 / 13) = 1 ∧
    (8 / 17 : Rat) * (8 / 17) + (15 / 17) * (15 / 17) = 1 := by
  refine ⟨?_, ?_, ?_⟩ <;> grind

/-- Kraus operators of the (3, 4, 5) channel as Gaussian-rational matrices. -/
abbrev kraus0 : GMat2 := ⟨GRat.one, GRat.zero, GRat.zero, ⟨3 / 5, 0⟩⟩
abbrev kraus1 : GMat2 := ⟨GRat.zero, GRat.zero, GRat.zero, ⟨4 / 5, 0⟩⟩

/-- K0^dagger K0 + K1^dagger K1 = I. -/
theorem kraus_completeness :
    GMat2.add (GMat2.mul (GMat2.dagger kraus0) kraus0)
              (GMat2.mul (GMat2.dagger kraus1) kraus1) = GMat2.id := by
  ext <;> grind

/-- Maximally coherent input rho = (1/2) [[1, 1], [1, 1]]. -/
abbrev rhoPlus : GMat2 := ⟨⟨1 / 2, 0⟩, ⟨1 / 2, 0⟩, ⟨1 / 2, 0⟩, ⟨1 / 2, 0⟩⟩

/-- One channel step keeps the populations and scales the coherence 1/2 -> 3/10. -/
theorem phase_damping_channel_step :
    GMat2.add (GMat2.mul (GMat2.mul kraus0 rhoPlus) (GMat2.dagger kraus0))
              (GMat2.mul (GMat2.mul kraus1 rhoPlus) (GMat2.dagger kraus1))
      = ⟨⟨1 / 2, 0⟩, ⟨3 / 10, 0⟩, ⟨3 / 10, 0⟩, ⟨1 / 2, 0⟩⟩ := by
  ext <;> grind

/-- One application of the (3, 4, 5) phase-damping channel,
    rho -> K0 rho K0^dagger + K1 rho K1^dagger. -/
abbrev dampStep (rho : GMat2) : GMat2 :=
  GMat2.add (GMat2.mul (GMat2.mul kraus0 rho) (GMat2.dagger kraus0))
            (GMat2.mul (GMat2.mul kraus1 rho) (GMat2.dagger kraus1))

abbrev rhoOne : GMat2 := ⟨⟨1 / 2, 0⟩, ⟨3 / 10, 0⟩, ⟨3 / 10, 0⟩, ⟨1 / 2, 0⟩⟩
abbrev rhoTwo : GMat2 := ⟨⟨1 / 2, 0⟩, ⟨9 / 50, 0⟩, ⟨9 / 50, 0⟩, ⟨1 / 2, 0⟩⟩
abbrev rhoThree : GMat2 := ⟨⟨1 / 2, 0⟩, ⟨27 / 250, 0⟩, ⟨27 / 250, 0⟩, ⟨1 / 2, 0⟩⟩

theorem phase_damping_step_one : dampStep rhoPlus = rhoOne := by
  ext <;> grind

theorem phase_damping_step_two : dampStep rhoOne = rhoTwo := by
  ext <;> grind

theorem phase_damping_step_three : dampStep rhoTwo = rhoThree := by
  ext <;> grind

/-- Three applications of the channel to rho_plus keep the populations at 1/2 and
    scale the off-diagonal entry 1/2 by (3/5)^3. -/
theorem phase_damping_three_applications :
    dampStep (dampStep (dampStep rhoPlus)) = rhoThree := by
  rw [phase_damping_step_one, phase_damping_step_two, phase_damping_step_three]

/-- The coherence 2 Re rho_01 after three applications is (3/5)^3 = 27/125, read
    off the channel output, not assumed. -/
theorem phase_damping_coherence_three_steps :
    2 * (dampStep (dampStep (dampStep rhoPlus))).a01.re = (3 / 5) * (3 / 5) * (3 / 5) := by
  rw [phase_damping_three_applications]
  grind

-- =============================================================================
-- QM-231 (Goal 9): QWZ Chern-number parity table
-- =============================================================================

/-- Integer sign function. -/
def sgn (x : Int) : Int := if 0 < x then 1 else if x < 0 then -1 else 0

/-- Twice the QWZ Chern number: the signed sum over the four Dirac points
    (-1)^{n_x + n_y} sgn(m + cos k_x + cos k_y) equals
    sgn(m + 2) - 2 sgn(m) + sgn(m - 2). -/
def twoChern (m : Int) : Int := sgn (m + 2) - 2 * sgn m + sgn (m - 2)

theorem sgn_values : sgn 5 = 1 ∧ sgn 0 = 0 ∧ sgn (-7) = -1 := by
  decide

theorem sgn_cases (x : Int) : sgn x = 1 ∨ sgn x = -1 ∨ sgn x = 0 := by
  unfold sgn
  split
  · exact Or.inl rfl
  · split
    · exact Or.inr (Or.inl rfl)
    · exact Or.inr (Or.inr rfl)

theorem sgn_nonzero (x : Int) (hx : x ≠ 0) : sgn x = 1 ∨ sgn x = -1 := by
  unfold sgn
  split
  · exact Or.inl rfl
  · split
    · exact Or.inr rfl
    · exfalso
      omega

/-- C1(-1) = +1, C1(+1) = -1, C1(+-3) = 0 (as twice the Chern number). -/
theorem chern_table :
    twoChern (-1) = 2 ∧ twoChern 1 = -2 ∧ twoChern 3 = 0 ∧ twoChern (-3) = 0 := by
  decide

/-- At the gap closings m = +-2 the signed sum is odd, so no integer Chern number
    is assigned there. -/
theorem chern_gap_closings_odd : twoChern 2 = -1 ∧ twoChern (-2) = 1 := by
  decide

/-- Away from m = +-2 the signed sum is even, so C1(m) is an integer. -/
theorem chern_parity (m : Int) (h2 : m ≠ 2) (h2' : m ≠ -2) : twoChern m % 2 = 0 := by
  have ha : sgn (m + 2) = 1 ∨ sgn (m + 2) = -1 := sgn_nonzero (m + 2) (by omega)
  have hc : sgn (m - 2) = 1 ∨ sgn (m - 2) = -1 := sgn_nonzero (m - 2) (by omega)
  have hb : sgn m = 1 ∨ sgn m = -1 ∨ sgn m = 0 := sgn_cases m
  unfold twoChern
  rcases ha with ha | ha <;> rcases hc with hc | hc <;> rcases hb with hb | hb | hb <;>
    omega

-- =============================================================================
-- Axiom census
-- =============================================================================

#print axioms kn_textbook_form
#print axioms kn_forward_eta
#print axioms kn_forward
#print axioms kn_thomson_eta
#print axioms kn_thomson
#print axioms kn_samples
#print axioms kn_sample_etas
#print axioms thomson_normalized
#print axioms thomson_weight_vs_ratio
#print axioms thomson_antiderivative_difference
#print axioms moller_eq_bhabha_su
#print axioms moller_tu_symmetric
#print axioms crossing_sample
#print axioms crossing_st_witness
#print axioms gamma5_squared
#print axioms gamma5_traceless
#print axioms chiral_projectors
#print axioms chiral_projectors_explicit
#print axioms projL_projR_vec
#print axioms muonF0_endpoints
#print axioms muonF0_factor
#print axioms muon_qed_correction_negative
#print axioms abj_factor_closed
#print axioms abj_factor_values
#print axioms abj_rate_ratio
#print axioms gmo_octet
#print axioms gmo_decuplet_equal_spacing
#print axioms gmo_decuplet_spacing_value
#print axioms gmo_omega_from_spacing
#print axioms deflection_factor_values
#print axioms gr_deflection_twice_newton
#print axioms null_probe_traceless
#print axioms dust_trace
#print axioms flow_tensor_trace
#print axioms perihelion_factor_gr
#print axioms mercury_per_orbit_arcsec
#print axioms clock_shift_action
#print axioms clock_shift_order_four
#print axioms clock_shift_not_id
#print axioms grat_i_squared
#print axioms pauli_squares
#print axioms pauli_ghz_sites
#print axioms pauli_xy_anticommute
#print axioms mermin_deterministic_bound
#print axioms mermin_bound_attained
#print axioms pw_frame_unitary
#print axioms step_unitary_factorization
#print axioms step_unitary_unitary
#print axioms step_unitary_order_four
#print axioms phase_damping_trace_preserving
#print axioms phase_damping_triples
#print axioms kraus_completeness
#print axioms phase_damping_channel_step
#print axioms phase_damping_step_one
#print axioms phase_damping_step_two
#print axioms phase_damping_step_three
#print axioms phase_damping_three_applications
#print axioms phase_damping_coherence_three_steps
#print axioms sgn_values
#print axioms sgn_cases
#print axioms sgn_nonzero
#print axioms chern_table
#print axioms chern_gap_closings_odd
#print axioms chern_parity

end FiniteQFTAndGravity
