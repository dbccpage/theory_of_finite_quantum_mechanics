Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `FSP-EFFICIENT-SAMPLING-OBLIGATIONS` (`TFQ-0409`)

AuthorityEffect: None.

## 1. Scope and Narrowed Target

Node `FSP-EFFICIENT-SAMPLING-OBLIGATIONS` (`TFQ-0409`, stage `FERMION_SIGN`, status `OPEN`) records the methodological and complexity boundary governing the `FERMION_SIGN` branch:

$$\text{Canonical sign representatives, finite cancellation, and nonnegative determinant weights do not by themselves establish an efficient sampler or a general fermion sign-problem solution.}$$

While keeping the node status at `OPEN`, this note and its local witnesses ([`lean4/CampaignFspEfficientSamplingObligations.lean`](../../../lean4/CampaignFspEfficientSamplingObligations.lean) and [`checks/independent/fsp-efficient-sampling-obligations.py`](../../../checks/independent/fsp-efficient-sampling-obligations.py)) formalize the quantitative input-size, representation-cost, estimator-variance, and Markov-chain mixing obligations that separate finite algebraic identities from polynomial-time Monte Carlo sampling.

## 2. Input-Size, Normal-Form, and Per-Step Cost Accounting

1. **Exhaustive SQL enumeration vs. polynomial linear algebra (`sql_exhaustive_orbit_size_exponential_vs_polynomial`, `exponential_configuration_graph_sign_switching_cost_fence`)**:
   Full spinful Fock space dimension $4^L$ strictly exceeds $L^3$ for $L \ge 3$ ($4^6 = 4096 > 6^3 = 216$), and the half-filled configuration vertex count $\binom{2m}{m}$ grows rapidly ($\binom{2}{1} = 2 < \binom{4}{2} = 6 < \binom{6}{3} = 20 < \binom{8}{4} = 70$). Thus an algorithm running in time polynomial in the configuration-graph size $|V_{\text{conf}}|$ or SQL orbit table size is exponential in the physical lattice size $L$.
2. **RREF canonical section is not an $\ell_1$ minimizer (`rref_canonical_section_not_l1_minimizer_witness`)**:
   In `BQNFSignEvaluator.normalize_cochain`, setting RREF pivot coordinates to zero selects a unique coset representative modulo $\operatorname{im}(d_0)$, but does not minimize the $\ell_1$ norm: for $d_0 = (1, 1, 1)^T$ and $c = (0, 1, 1)^T$, the RREF pivot-zero representative is $N(c) = (0, 1, 1)^T$ with $\|N(c)\|_1 = 2$, whereas $c - d_0 = (-1, 0, 0)^T$ has $\|c - d_0\|_1 = 1 < 2$. Moreover, `solve_quotient_distance` enumerates up to $\binom{\dim C^1}{\operatorname{rank} d_0}$ candidate bases and refuses when the candidate budget is exceeded.
3. **DQMC update vs. stabilization cost (`determinant_weight_evaluation_and_update_cost_accounting`)**:
   In Determinant Quantum Monte Carlo on $N_s \ge 2$ spatial sites, a rank-1 Sherman-Morrison update costs $c N_s^2$ operations while a full QR/SVD stabilization sweep costs $c N_s^3 > c N_s^2$.

## 3. Variance, Mixing, and Four-Tier Epistemic Scope Fences

1. **Meron orbit cancellation vs. survivor sampling (`meron_orbit_cancellation_preserves_partition_and_observable`)**:
   Cancelling a zero-sum meron pair $(+w_m, -w_m)$ ($w_m > 0$) preserves $Z = w_1 + w_2$ while reducing $Z_{\text{abs}}$ from $w_1 + w_2 + 2 w_m$ to $w_1 + w_2$, raising the average sign from $\frac{w_1 + w_2}{w_1 + w_2 + 2 w_m} < 1$ to $1$.
2. **Nonnegative weights do not bound observable variance (`nonnegative_weights_do_not_bound_observable_variance_fence`)**:
   Even in a strictly positive probability distribution $(p, 1 - p)$ ($0 < p < 1$, zero sign problem), an observable taking value $1/p$ with probability $p$ and $0$ with probability $1 - p$ has unit mean $\mu = 1$ and variance $\operatorname{Var}(O) = 1/p - 1$, which grows without bound as $p \to 0^+$.
3. **Nonnegative weights do not imply rapid mixing (`bimodal_energy_barrier_conductance_bottleneck_fence`)**:
   Even when all weights are positive, two wells of weight $W_{\text{well}} > 0$ separated by a saddle barrier of weight $0 < b_1 < b_2$ have inverse-conductance mixing lower bound $\frac{W_{\text{well}}}{2 b}$, which grows strictly as the barrier weight decreases ($\frac{W_{\text{well}}}{2 b_2} < \frac{W_{\text{well}}}{2 b_1}$).
4. **Four-tier epistemic separation (`four_tier_fsp_epistemic_separation_obligations`)**:
   Distinguishes (1) exact finite identity, (2) protected sign-free weight representation ($W(c) \ge 0$), (3) polynomial-time sampler with bounded variance and mixing, and (4) unrestricted FSP solution, keeping `FSP-EFFICIENT-SAMPLING-OBLIGATIONS` `OPEN`.
