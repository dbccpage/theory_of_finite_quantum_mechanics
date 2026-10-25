Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` (`TFQ-1149`)

- **DAG Node**: `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` (`TFQ-1149` / `MAJ-OPEN-LOCALITY-VIABILITY`)
- **Stage**: `MAJORANA`
- **Status**: `OPEN` (preserved; formalizes discrete Lieb-Robinson light-cone support growth, syndrome-recovery viability horizon inequalities, logical-cycle collision splits, discrete commutator tail suppression, classical routing delay bounds, and explicit open-scope fences)
- **Evidence Grade**: `E3` (`L4D`, `lean4/CampaignMajOpenLiebRobinsonLocality.lean`, 10 theorems, 0 `sorry`, 6/6 mutations killed)

---

## 1. Mathematical Structure & Mechanized Theorems

Under a discrete local schedule with Lieb-Robinson propagation speed $v_{\mathrm{LR}} \in \mathbb{N}$ and initial contiguous fault support weight $w_0 \in \mathbb{N}$, the two-sided 1D support diameter after $t$ steps is
$$
W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t) = w_0 + 2\,v_{\mathrm{LR}}\,t.
$$
Combining this support expansion with the Theorem 4.4 / Corollary 4.5 syndrome recovery criterion on a code of distance $d = \min\{\mathrm{wt}(z) : z \in \ker Q \setminus B\}$ yields an exact discrete viability horizon:

1. **One-Sided Causal Radius Additivity (`lieb_robinson_causal_radius_additive`)**:
   For $R_{\mathrm{LR}}(r_0, v_{\mathrm{LR}}, t) = r_0 + v_{\mathrm{LR}} t$, sequential intervals $t_1, t_2$ compose additively: $R_{\mathrm{LR}}(R_{\mathrm{LR}}(r_0, v_{\mathrm{LR}}, t_1), v_{\mathrm{LR}}, t_2) = R_{\mathrm{LR}}(r_0, v_{\mathrm{LR}}, t_1 + t_2)$ and $r_0 \le R_{\mathrm{LR}}(r_0, v_{\mathrm{LR}}, t_1)$.
2. **Two-Sided 1D Support Diameter Growth (`lieb_robinson_1d_support_diameter_growth`)**:
   $W_{\mathrm{LR}}(W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t_1), v_{\mathrm{LR}}, t_2) = W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t_1 + t_2)$, and for $v_{\mathrm{LR}} > 0$, $W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t_1) < W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t_1 + 1)$.
3. **Propagated Error-Pair Difference Weight Bound (`lieb_robinson_pair_difference_weight_bound`)**:
   For any two propagated error vectors with weights $w_1, w_2 \le W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t)$ and difference weight $w_{\mathrm{diff}} \le w_1 + w_2$, $w_{\mathrm{diff}} \le 2 W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t) = 2 w_0 + 4 v_{\mathrm{LR}} t$.
4. **Syndrome Recovery Viability Within the Lieb-Robinson Horizon (`syndrome_recovery_viability_within_lr_horizon`)**:
   Whenever $2 W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t) < d$, every propagated error pair satisfies $w_{\mathrm{diff}} < d$, ruling out non-stabilizer logical cycle collisions ($z \in \ker Q \setminus B$).
5. **Monotonicity of the Critical Repair Horizon (`critical_repair_horizon_monotonicity`)**:
   If recovery is viable at extraction latency $t_{\mathrm{hi}}$, then for every earlier latency $t_{\mathrm{lo}} < t_{\mathrm{hi}}$ ($v_{\mathrm{LR}} > 0$), $2 W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t_{\mathrm{lo}}) < 2 W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t_{\mathrm{hi}}) < d$ with distance margin $4 v_{\mathrm{LR}} (t_{\mathrm{hi}} - t_{\mathrm{lo}})$.
6. **Horizon Overflow Logical Collision (`lieb_robinson_horizon_exceeded_logical_collision`)**:
   Conversely, when $d \le 2 W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t)$, any logical cycle of weight $d$ partitions into two weights $w_1 = \lfloor d / 2 \rfloor$ and $w_2 = d - \lfloor d / 2 \rfloor$ with $w_1 + w_2 = d$ and $w_1, w_2 \le W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t)$, creating an indistinguishable syndrome collision inside the propagated error ball.
7. **Discrete Lieb-Robinson Commutator Tail Suppression (`discrete_commutator_tail_decay_recurrence`)**:
   For $c_0 > 0$, $1 < g \le \mu$, and spatial separation $t < \mathrm{dist}$ outside the causal cone, the discrete tail numerator $c_0 g^t$ is strictly bounded by the spatial decay factor $c_0 \mu^{\mathrm{dist}}$.
8. **Classical Syndrome-Routing Delay Constraint (`syndrome_measurement_communication_delay_bound`)**:
   If routing syndromes across an array of linear size $L$ at classical speed $v_{\mathrm{cl}} > 0$ requires time $t_{\mathrm{comm}}$ with $L \le v_{\mathrm{cl}} t_{\mathrm{comm}}$, then viability $2 W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t_{\mathrm{comm}}) < d$ requires $2 w_0 v_{\mathrm{cl}} + 4 v_{\mathrm{LR}} L < d v_{\mathrm{cl}}$.
9. **Tetron Torus Viability Window Witness (`torus_tetron_viability_window_witness`)**:
   For $w_0 = 1, v_{\mathrm{LR}} = 1$, a single step $t = 1$ gives $2 W_{\mathrm{LR}}(1, 1, 1) = 6$, which overflows the $L = 4$ torus ($d = 4 < 6$) while remaining viable on the $L = 7$ torus ($6 < 7 = d$) before overflowing at $t = 2$ ($2 W_{\mathrm{LR}}(1, 1, 2) = 10 > 7$).
10. **Open-Scope Fence (`lieb_robinson_locality_open_scope_fence`)**:
    Packages the viability/collision dichotomy while keeping `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` in status `OPEN`.

---

## 2. Claim Hygiene Summary

1. **What it supports**: Exact discrete light-cone support growth, the $2(w_0 + 2 v_{\mathrm{LR}} t) < d$ viability threshold vs logical-collision split, discrete commutator tail suppression for $t < \mathrm{dist}$, and classical syndrome-routing delay constraints.
2. **What it does not support**: Does not derive continuous-time Banach-algebra Lieb-Robinson bounds for microscopic superconducting Hamiltonians and does not establish a general verdict on physical quantum computing viability (`OPEN` status preserved).
3. **Narrowest defensible claim**: In the declared discrete 1D/2D support-expansion model, weight-bounded syndrome recovery holds up to propagation latency $t$ if and only if $2(w_0 + 2 v_{\mathrm{LR}} t) < d$.
4. **Next test needed**: Formalize the two-direction weight-bounded recovery equivalence $\mathcal{E}_t$ recoverable $\leftrightarrow 2t < d$ for `MAJ-DISTANCE-WEIGHT-CORRECTION` (`TFQ-1148`).
