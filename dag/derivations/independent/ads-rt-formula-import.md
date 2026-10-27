# Independent Derivation Note: `ADS-RT-FORMULA-IMPORT` (`TFQ-2204`)

**AuthorityEffect:** None.
**Node:** `ADS-RT-FORMULA-IMPORT` (`TFQ-2204`, stage `ADS_CFT`, status `IMPORTED_ASSUMPTION`)
**Outcome Class:** Narrowed (continuum Ryu-Takayanagi formula remains `IMPORTED_ASSUMPTION`; narrowed to three finite/rational algebraic shadows and non-equivalence scope fences in [AdsRtFormulaImport.lean](../../../lean4/AdsRtFormulaImport.lean) and [ads-rt-formula-import.py](../../../checks/independent/ads-rt-formula-import.py)).

---

## 1. Source Formula & Scope Boundary

Ryu and Takayanagi (2006, `arXiv:hep-th/0603001`, Section 1 eq. (1.5) p. 2) state the leading-order holographic entanglement entropy formula for a spatial boundary region $A$ of a $(d+1)$-dimensional CFT dual to static $\mathrm{AdS}_{d+2}$:
$$S_A = \frac{\mathrm{Area}(\gamma_A)}{4 G_N^{(d+2)}},$$
where $\gamma_A$ is the minimal-area static bulk $d$-surface anchored on $\partial A$. In Section 2 (eqs. (2.1), (2.5)-(2.6) p. 3), for $\mathrm{AdS}_3 / \mathrm{CFT}_2$ with regulated geodesic length $L_{\gamma_A} = 2 R_{\mathrm{AdS}} \ln\!\left(\frac{L}{\pi a}\sin\frac{\pi \ell}{L}\right)$ and the Brown-Henneaux central charge $c = \frac{3 R_{\mathrm{AdS}}}{2 G_N^{(3)}}$, this formula reproduces the 2D CFT single-interval formula $S_A = \frac{c}{3}\ln\!\left(\frac{L}{\pi a}\sin\frac{\pi \ell}{L}\right)$.

In this repository, the continuum Ryu-Takayanagi formula remains an `IMPORTED_ASSUMPTION`: it presupposes both a continuum boundary Hilbert space with well-defined subregion von Neumann entropy and a smooth bulk geometry with minimal surfaces. Neither the repository's finite von Neumann entropy dichotomy ([EntropyDichotomy.lean](../../../lean4/EntropyDichotomy.lean), `FQ-ENTROPY-DICHOTOMY-BAKER`) nor its exact rational Regge action proxy ([action.rs](../../../code/rust/src/general_relativity/exact_regge/action.rs), `TFQ-0100`) provides a minimal-surface area in a continuum bulk geometry.

---

## 2. Three Formalized Algebraic Shadows & Scope Fences

### 2.1 Ryu-Takayanagi / Brown-Henneaux Coupling Elimination & Minimal-Cut Submodularity

1. **Exact Coupling Elimination in $\mathrm{AdS}_3 / \mathrm{CFT}_2$**:
   Define over $\mathbb{Q}$:
   $$\mathrm{rtLeadingEntropy}(\mathrm{area}, G_N) = \frac{\mathrm{area}}{4 G_N}, \qquad \mathrm{brownHenneauxCentralCharge}(R_{\mathrm{AdS}}, G_N^{(3)}) = \frac{3 R_{\mathrm{AdS}}}{2 G_N^{(3)}},$$
   $$\mathrm{ads3GeodesicLength}(R_{\mathrm{AdS}}, \Lambda_{\log}) = 2 R_{\mathrm{AdS}} \Lambda_{\log}, \qquad \mathrm{calabreseCardyCoefficient}(c) = \frac{c}{3}.$$
   Then for all $R_{\mathrm{AdS}}, G_N^{(3)}, \Lambda_{\log} \in \mathbb{Q}$:
   $$\mathrm{rtLeadingEntropy}(\mathrm{ads3GeodesicLength}(R_{\mathrm{AdS}}, \Lambda_{\log}), G_N^{(3)}) = \mathrm{calabreseCardyCoefficient}(\mathrm{brownHenneauxCentralCharge}(R_{\mathrm{AdS}}, G_N^{(3)})) \cdot \Lambda_{\log}$$
   ([`rt_ads3_reproduces_calabrese_cardy`](../../../lean4/AdsRtFormulaImport.lean#L97-L101)), and for $R_{\mathrm{AdS}} \neq 0, G_N^{(3)} \neq 0$, the ratio to $c$ eliminates both bulk couplings:
   $$\frac{\mathrm{rtLeadingEntropy}(\mathrm{ads3GeodesicLength}(R_{\mathrm{AdS}}, \Lambda_{\log}), G_N^{(3)})}{\mathrm{brownHenneauxCentralCharge}(R_{\mathrm{AdS}}, G_N^{(3)})} = \frac{\Lambda_{\log}}{3}$$
   ([`rt_over_brown_henneaux_eliminates_couplings`](../../../lean4/AdsRtFormulaImport.lean#L105-L111)).
2. **Cut-Pasting Strong Subadditivity (`arXiv:hep-th/0603001` eq. (3.2) p. 4) & HaPPY Complement Symmetry**:
   Additivity of $\mathrm{rtLeadingEntropy}$ ([`rtLeadingEntropy_linear_in_area`](../../../lean4/AdsRtFormulaImport.lean#L114-L118)) and surface-reconnection submodularity $\mathrm{area}_{\cup} + \mathrm{area}_{\cap} \le \mathrm{area}_{AB} + \mathrm{area}_{BC}$ with minimality $\mathrm{min}_{ABC} \le \mathrm{area}_{\cup}$, $\mathrm{min}_B \le \mathrm{area}_{\cap}$ at $G_N > 0$ yield
   $$\mathrm{rtLeadingEntropy}(\mathrm{min}_{ABC}, G_N) + \mathrm{rtLeadingEntropy}(\mathrm{min}_B, G_N) \le \mathrm{rtLeadingEntropy}(\mathrm{area}_{AB}, G_N) + \mathrm{rtLeadingEntropy}(\mathrm{area}_{BC}, G_N)$$
   ([`cut_pasting_strong_subadditivity_from_submodularity`](../../../lean4/AdsRtFormulaImport.lean#L125-L139)).
   On the 20-qubit 6-pentagon HaPPY `{5,4}` patch ([FrontierHappyMincut.lean](../../../lean4/FrontierHappyMincut.lean)), both `mincut` and `boundaryEntropy` satisfy exact complement symmetry $(s, \ell) \mapsto ((s + \ell) \bmod 20, 20 - \ell)$ across all `380` proper nonempty contiguous boundary intervals ([`happy_mincut_and_entropy_complement_symmetry_all_380`](../../../lean4/AdsRtFormulaImport.lean#L146-L151)).

### 2.2 Von Neumann Entropy Dichotomy Fence (`FQ-ENTROPY-DICHOTOMY-BAKER`)

Importing [`C750B01`](../../../lean4/EntropyDichotomy.lean#L11-L248):
- Every rational RT ratio $(\mathrm{rtLeadingEntropy}(\mathrm{area}, G_N) : \mathbb{R})$ is algebraic over $\mathbb{Q}$ ([`rtLeadingEntropy_realCast_isAlgebraic`](../../../lean4/AdsRtFormulaImport.lean#L159-L161)).
- Under `BakerCitedInput`, for every mixed algebraic spectrum $s : \mathrm{AlgebraicSpectrum}\, d$ ($\neg \mathrm{Pure}(s)$), the natural-log von Neumann entropy $\mathrm{entropy}(s) = -\sum_i p_i \ln p_i$ is transcendental over $\mathbb{Q}$, and therefore cannot equal any rational RT ratio:
  $$\mathrm{entropy}(s) \neq (\mathrm{rtLeadingEntropy}(\mathrm{area}, G_N) : \mathbb{R})$$
  ([`no_rational_rt_area_for_mixed_algebraic_spectrum`](../../../lean4/AdsRtFormulaImport.lean#L166-L174)).
- Under `BakerCitedInput` and $G_N > 0$, equality holds if and only if the state is pure and the area vanishes:
  $$\mathrm{entropy}(s) = (\mathrm{rtLeadingEntropy}(\mathrm{area}, G_N) : \mathbb{R}) \iff \mathrm{Pure}(s) \wedge \mathrm{area} = 0$$
  ([`rational_rt_match_iff_pure_and_zero_area`](../../../lean4/AdsRtFormulaImport.lean#L179-L198)).
- For a $k$-bit maximally mixed stabilizer marginal with natural-log entropy $k \ln 2$, the integer bond count $k$ is recovered only after dividing by the conversion factor $\ln 2 \neq 0$ ([`stabilizer_bits_to_nats_transcendental_conversion`](../../../lean4/AdsRtFormulaImport.lean#L203-L206)).

### 2.3 Exact Rational Regge Proxy (`TFQ-0100`) vs. Minimal-Surface Area & HaPPY Bond-Cut Fence

In [action.rs](../../../code/rust/src/general_relativity/exact_regge/action.rs) and [sphere.rs](../../../code/rust/src/general_relativity/exact_regge/sphere.rs) (`TFQ-0100`), the rational Regge proxy sums Cayley-Menger squared triangle areas $A_h^2$ times rational holonomy defects $\kappa_h$:
$$\mathrm{cayleyMengerTriangleAreaSq}(s_{01}, s_{02}, s_{12}) = \frac{2(s_{01}s_{02} + s_{01}s_{12} + s_{02}s_{12}) - (s_{01}^2 + s_{02}^2 + s_{12}^2)}{16},$$
$$\mathrm{rationalReggeAction}(A_{\mathrm{sq}}, \kappa) = \sum_i A_{\mathrm{sq}}(i)\,\kappa(i).$$
Three structural fences separate this proxy from both the continuum RT area term and discrete HaPPY bond counts:
1. **Irrational Linear Area on the `orthogonal_pentatope` Chart (`TFQ-0100`)**:
   On `orthogonal_pentatope` (vertices $0$ and $e_1, e_2, e_3, e_4 \in \mathbb{Q}^4$), the 6 right-triangle hinges have squared edge lengths $(1, 1, 2)$ and $A_h^2 = 1/4$, while the 4 equilateral-triangle hinges have squared edge lengths $(2, 2, 2)$ and $A_h^2 = 3/4$, summing to $9/2$ ([`orthogonal_pentatope_hinge_areas_sq`](../../../lean4/AdsRtFormulaImport.lean#L226-L231)). However, by 3-adic divisibility on reduced fractions ([`nat_dvd_three_of_sq_mul_four_eq_three_mul_sq`](../../../lean4/AdsRtFormulaImport.lean#L234-L264)), no rational linear area $A \in \mathbb{Q}$ satisfies $A^2 = 3/4$:
   $$\forall A \in \mathbb{Q},\quad A^2 \neq \mathrm{cayleyMengerTriangleAreaSq}(2, 2, 2)$$
   ([`no_rational_linear_area_for_equilateral_pentatope_hinge`](../../../lean4/AdsRtFormulaImport.lean#L269-L286)).
2. **Flat-Background Vanishing vs. Strictly Positive HaPPY Cuts**:
   When $\kappa = 0$ (`flat_einstein_hilbert`), $\mathrm{rationalReggeAction}(A_{\mathrm{sq}}, 0) = 0$ identically ([`reggeProxy_zero_on_flat_chart`](../../../lean4/AdsRtFormulaImport.lean#L290-L293)), whereas on the 20-qubit 6-pentagon HaPPY patch every one of the `380` proper nonempty contiguous boundary intervals satisfies $1 \le \mathrm{boundaryEntropy}(A)$ and $1 \le \mathrm{mincut}(A)$ ([`happy_all_380_intervals_pos_entropy_and_mincut`](../../../lean4/AdsRtFormulaImport.lean#L300-L304)).
3. **Scaling-Degree Mismatch ($\lambda^4$ vs. $\lambda^2$ vs. $\lambda^0$)**:
   Under uniform length rescaling $L \mapsto \lambda L$ ($s_{ij} \mapsto \lambda^2 s_{ij}$), $\mathrm{cayleyMengerTriangleAreaSq}$ scales as $\lambda^4$ ([`cayleyMengerTriangleAreaSq_homogeneous_deg4_in_length`](../../../lean4/AdsRtFormulaImport.lean#L309-L314)), whereas a 2-surface area scales as $\lambda^2$ and a topological bond count scales as $\lambda^0$; no constant $\alpha \in \mathbb{Q}$ can equate $\alpha(\lambda^4 A_0)$ with $\lambda^2 A_0$ or $A_0$ across $\lambda = 1$ and $\lambda = 2$ for $A_0 \neq 0$ ([`no_scale_invariant_regge_to_rt_dictionary`](../../../lean4/AdsRtFormulaImport.lean#L320-L336)).
