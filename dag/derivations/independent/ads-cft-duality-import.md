Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `ADS-CFT-DUALITY-IMPORT` (`TFQ-2202`, `ADS-01`)

AuthorityEffect: None.

## Target & Outcome Class

- **Campaign Node**: `ADS-CFT-DUALITY-IMPORT` (`TFQ-2202`, source ID `ADS-01`, stage `ADS_CFT`)
- **Outcome Class**: **Narrowed** (node status remains `IMPORTED_ASSUMPTION`)
- **Primary Literature**:
  - J. M. Maldacena, *The Large-$N$ Limit of Superconformal Field Theories and Supergravity*, Adv. Theor. Math. Phys. **2**, 231–252 (1998) [arXiv:hep-th/9711200]
  - S. S. Gubser, I. R. Klebanov, and A. M. Polyakov, *Gauge Theory Correlators from Non-Critical String Theory*, Phys. Lett. B **428**, 105–114 (1998) [arXiv:hep-th/9802109]
  - E. Witten, *Anti-de Sitter Space and Holography*, Adv. Theor. Math. Phys. **2**, 253–291 (1998) [arXiv:hep-th/9802150]
  - P. Breitenlohner and D. Z. Freedman, *Stability in Gauged Extended Supergravity*, Annals Phys. **144**, 249–281 (1982)
  - G. 't Hooft, *A Planar Diagram Theory for Strong Interactions*, Nucl. Phys. B **72**, 461–473 (1974)
- **Verification Artifacts**:
  - Lean 4 module: `lean4/AdsCftDualityImport.lean`
  - Standalone zero-import Python checker: `checks/independent/ads-cft-duality-import.py`
  - Receipts: `dag/research/campaign_ads-cft-duality-import_lean_replay.json`, `dag/research/campaign_ads-cft-duality-import_lean_mutation.json`, `dag/research/campaign_ads-cft-duality-import_independent.json`

---

## 1. GKPW Scalar Mass-Dimension Quadratic & Breitenlohner-Freedman Stability Bound

In the Gubser-Klebanov-Polyakov-Witten (GKPW) dictionary between a free scalar field of dimensionless mass-squared $m_{\mathrm{sq}} = (m R_{\mathrm{AdS}})^2$ on $\mathrm{AdS}_{d+1}$ and a scalar primary operator of conformal dimension $\Delta$ in a $d$-dimensional boundary CFT, the asymptotic radial wave equation near the conformal boundary imposes the quadratic relation:
$$
\operatorname{gkpwMassSq}(d, \Delta) := \Delta(\Delta - d) = m_{\mathrm{sq}}.
$$

Over $\mathbb{Q}$, `lean4/AdsCftDualityImport.lean` establishes:
1. **Shadow Involution and Vieta Relations**:
   Defining $\operatorname{shadowDimension}(d, \Delta) := d - \Delta$,
   - `shadowDimension_involutive`: $\operatorname{shadowDimension}(d, \operatorname{shadowDimension}(d, \Delta)) = \Delta$.
   - `shadowDimension_sum`: $\Delta + \operatorname{shadowDimension}(d, \Delta) = d$.
   - `gkpwMassSq_shadow_eq`: $\operatorname{gkpwMassSq}(d, \operatorname{shadowDimension}(d, \Delta)) = \operatorname{gkpwMassSq}(d, \Delta)$.
   - `gkpw_vieta_product`: $\Delta \cdot \operatorname{shadowDimension}(d, \Delta) = -\operatorname{gkpwMassSq}(d, \Delta)$.
2. **Completed Square and Rational Root Recovery**:
   Defining the discriminant $\operatorname{gkpwDiscriminant}(d, m_{\mathrm{sq}}) := d^2 + 4 m_{\mathrm{sq}}$ and roots $\Delta_{\pm}(d, s) := (d \pm s)/2$:
   - `gkpw_completed_square`: $(2\Delta - d)^2 = d^2 + 4 \Delta(\Delta - d)$.
   - `gkpw_roots_from_square_discriminant`: Whenever $s^2 = d^2 + 4 m_{\mathrm{sq}}$, both $\Delta_+(d, s)$ and $\Delta_-(d, s)$ satisfy $\operatorname{gkpwMassSq}(d, \Delta_\pm) = m_{\mathrm{sq}}$, $\Delta_+ + \Delta_- = d$, and $\Delta_+ - \Delta_- = s$.
3. **Breitenlohner-Freedman (BF) Stability Bound**:
   Defining $\operatorname{bfBound}(d) := -d^2/4$:
   - `bf_bound_iff_discriminant_nonneg`: $-d^2/4 \le m_{\mathrm{sq}} \iff 0 \le d^2 + 4 m_{\mathrm{sq}}$.
   - `bf_saturation_double_root`: At $m_{\mathrm{sq}} = -d^2/4$, the discriminant vanishes and the roots coalesce at $\Delta_+ = \Delta_- = d/2$ with $\operatorname{gkpwMassSq}(d, d/2) = -d^2/4$.
   - `gkpwMassSq_ge_bfBound`: For every $\Delta \in \mathbb{Q}$, $\operatorname{bfBound}(d) \le \operatorname{gkpwMassSq}(d, \Delta)$ via $\Delta(\Delta - d) - (-d^2/4) = (\Delta - d/2)^2 \ge 0$.
   - `no_rational_root_below_bf_bound`: For every $m_{\mathrm{sq}} < \operatorname{bfBound}(d)$ and every $\Delta \in \mathbb{Q}$, $\operatorname{gkpwMassSq}(d, \Delta) \ne m_{\mathrm{sq}}$.
4. **Recorded $\mathrm{AdS}_5/\mathrm{CFT}_4$ ($d=4$) and $\mathrm{AdS}_3/\mathrm{CFT}_2$ ($d=2$) Points** (`recorded_ads5_and_ads3_gkpw_points`):
   - $(d=4, m_{\mathrm{sq}}=0)$: $D=16$, $\Delta_+=4$ (marginal operator), $\Delta_-=0$.
   - $(d=4, m_{\mathrm{sq}}=-4)$: BF saturation $D=0$, double root $\Delta_\pm = 2$.
   - $(d=4, m_{\mathrm{sq}}=-3)$: conformally coupled scalar on $\mathrm{AdS}_5$, $D=4$, $\Delta_+=3$, $\Delta_-=1$.
   - $(d=4, m_{\mathrm{sq}}=5)$: $D=36$, $\Delta_+=5$, $\Delta_-=-1$.
   - $(d=2, m_{\mathrm{sq}}=-1)$: $\mathrm{AdS}_3/\mathrm{CFT}_2$ BF saturation $D=0$, double root $\Delta_\pm = 1$.
   - $(d=4, m_{\mathrm{sq}}=1)$: $D = 20$ with $4^2 < 20 < 5^2$, demonstrating that even integer $(d, m_{\mathrm{sq}})$ above the BF bound can yield non-square discriminants whose roots $\Delta_\pm = 2 \pm \sqrt{5}$ require quadratic field extensions beyond $\mathbb{Q}$.

---

## 2. 't Hooft Large-$N$ Ribbon-Graph Genus Scaling & $U(N)/SU(N)$ Dimension Split

In 't Hooft's double-line representation for $U(N)$ gauge theory with coupling $g_{\mathrm{YM}}^2$ and 't Hooft coupling $\lambda := g_{\mathrm{YM}}^2 N$, a connected vacuum ribbon graph with $V$ vertices, $E$ propagators ($V \le E$), and $F$ closed index loops has Euler characteristic $\chi(V, E, F) = V - E + F = 2 - 2g$ and unnormalized double-line weight:
$$
\operatorname{ribbonDoubleLineWeight}(g_{\mathrm{YM}}^2, N, V, E, F) := (g_{\mathrm{YM}}^2)^{E - V} N^F.
$$

`lean4/AdsCftDualityImport.lean` establishes:
- `thooft_factorization`:
  $$
  (g_{\mathrm{YM}}^2)^{E - V} N^F \cdot N^{E - V} = (g_{\mathrm{YM}}^2 N)^{E - V} N^F = \lambda^{E - V} N^F.
  $$
- `thooft_planar_vs_torus_suppression`: For the 2-vertex, 3-propagator vacuum ribbon graphs ($E - V = 1$), the planar dipole ($V=2, E=3, F=3$) has $\chi = 2 = 2 - 2(0)$ ($g=0$) and weight $\lambda N^2$, whereas the non-planar genus-1 torus contraction ($V=2, E=3, F=1$) has $\chi = 0 = 2 - 2(1)$ ($g=1$) and weight $\lambda$, so multiplying the torus weight by $N^2$ equals the planar weight.
- `recorded_thooft_and_gauge_counts`: The Lie algebra dimension split $N^2 = (N^2 - 1) + 1$ separating $\mathfrak{u}(N) \cong \mathfrak{su}(N) \oplus \mathfrak{u}(1)$ (with $\dim \mathfrak{su}(3) = 8$ and $\dim \mathfrak{su}(4) = 15$), together with concrete evaluation at $N = 3, g_{\mathrm{YM}}^2 = 1/3, \lambda = 1$ giving planar weight $9$ and torus weight $1$.

---

## 3. Finite Isometric Bulk-to-Boundary Dictionary & Non-Surjectivity Fence

When a finite bulk code space $\mathbb{Q}^b$ is embedded into a boundary state space $\mathbb{Q}^B$ via an isometry $V : \mathrm{Matrix}\,B\,b\,\mathbb{Q}$ satisfying $V^T V = I_b$:
- Bulk operator pushforward: $\iota_V(O_{\mathrm{bulk}}) := V O_{\mathrm{bulk}} V^T \in \mathrm{Matrix}\,B\,B\,\mathbb{Q}$.
- Boundary operator pullback: $\pi_V(O_{\mathrm{bdry}}) := V^T O_{\mathrm{bdry}} V \in \mathrm{Matrix}\,b\,b\,\mathbb{Q}$.
- Quadratic state expectation: $\operatorname{quadExpectation}(O, \psi) := \langle \psi, O \psi \rangle$.

`lean4/AdsCftDualityImport.lean` establishes:
1. `pullback_pushforward_id`: $\pi_V(\iota_V(O_{\mathrm{bulk}})) = O_{\mathrm{bulk}}$ whenever $V^T V = I_b$.
2. `pushforward_mul_of_isometry`: $\iota_V(A) \iota_V(C) = \iota_V(AC)$ whenever $V^T V = I_b$.
3. `correlator_dictionary_pullback`: For every matrix $V$, boundary observable $O_{\mathrm{bdry}}$, and bulk vector $\psi$,
   $$
   \langle V\psi, O_{\mathrm{bdry}}(V\psi) \rangle = \langle \psi, \pi_V(O_{\mathrm{bdry}})\psi \rangle.
   $$
4. `correlator_dictionary_match`: When $V^T V = I_b$, $\langle V\psi, \iota_V(O_{\mathrm{bulk}})(V\psi) \rangle = \langle \psi, O_{\mathrm{bulk}}\psi \rangle$.
5. **Non-Equivalence Fence** (`codeIsometry12_is_isometry`, `codeIsometry12_projector_ne_one`, `boundary_annihilator_obstruction`):
   For the explicit $1 \to 2$ isometric code embedding $V = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$ and orthogonal-complement operator $O_\perp = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}$:
   - $V^T V = I_1$,
   - $V V^T = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \ne I_2$,
   - $O_\perp \ne 0$ but $\pi_V(O_\perp) = 0$, and
   - $\iota_V : \mathrm{Matrix}\,(\mathrm{Fin}\,1)\,(\mathrm{Fin}\,1)\,\mathbb{Q} \to \mathrm{Matrix}\,(\mathrm{Fin}\,2)\,(\mathrm{Fin}\,2)\,\mathbb{Q}$ is not surjective ($O_\perp$ has no bulk preimage).

---

## What is proved

- **GKPW Scalar Mass-Dimension Algebra & BF Bound over $\mathbb{Q}$**: `shadowDimension_involutive`, `shadowDimension_sum`, `gkpwMassSq_shadow_eq`, `gkpw_vieta_product`, `gkpw_completed_square`, `gkpw_roots_from_square_discriminant`, `bf_bound_iff_discriminant_nonneg`, `bf_saturation_double_root`, `gkpwMassSq_ge_bfBound`, `no_rational_root_below_bf_bound`, and `recorded_ads5_and_ads3_gkpw_points` in `lean4/AdsCftDualityImport.lean`.
- **'t Hooft Ribbon-Graph Genus Scaling & $U(N)/SU(N)$ Split**: `thooft_factorization`, `thooft_planar_vs_torus_suppression`, and `recorded_thooft_and_gauge_counts` in `lean4/AdsCftDualityImport.lean`.
- **Finite Isometric Bulk-to-Boundary Dictionary & Non-Surjectivity Fence**: `pullback_pushforward_id`, `pushforward_mul_of_isometry`, `correlator_dictionary_pullback`, `correlator_dictionary_match`, `codeIsometry12_is_isometry`, `codeIsometry12_projector_ne_one`, and `boundary_annihilator_obstruction` in `lean4/AdsCftDualityImport.lean`.
- **Independent Verification & Mutation Killing**: 963 exact rational and matrix checks with 0 failures in `checks/independent/ads-cft-duality-import.py`, and 6 of 6 semantic Lean mutations killed in `dag/research/campaign_ads-cft-duality-import_lean_mutation.json`.

## What is assumed

- The continuum AdS/CFT duality dictionary—identifying the partition function $Z_{\mathrm{grav}}[\phi_0] = \langle \exp(\int \phi_0 \mathcal{O}) \rangle_{\mathrm{CFT}}$, the full Hilbert space isomorphism between type IIB string theory on $\mathrm{AdS}_5 \times S^5$ and $4\mathrm{D}$ $\mathcal{N}=4$ $SU(N)$ super-Yang-Mills theory, and the analytic continuation of bulk boundary-value problems—remains an imported continuum hypothesis (`status: "IMPORTED_ASSUMPTION"`).

## What is open

- Deriving an exact continuum or asymptotic large-$N$ bulk gravitational dynamics and full partition-function equality $Z_{\mathrm{grav}}[\phi_0] = Z_{\mathrm{CFT}}[\phi_0]$ from finite substrate rules without importing continuum quantum field theory or asymptotically anti-de Sitter supergravity.
