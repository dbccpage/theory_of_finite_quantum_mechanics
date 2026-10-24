# Pre-Commit Review: `FSP-EFFICIENT-SAMPLING-OBLIGATIONS` (`TFQ-0409`)

AuthorityEffect: None.

- **Node**: `FSP-EFFICIENT-SAMPLING-OBLIGATIONS` (`TFQ-0409`)
- **Stage**: `FERMION_SIGN`
- **Status**: `OPEN` (preserved)
- **Evidence Grade**: `E1 -> E3` (`L4D`, 0 flags)
- **Lean 4 Module**: `lean4/CampaignFspEfficientSamplingObligations.lean` (10 theorems, 0 `sorry`, 0 custom axioms, 6/6 mutants killed)
- **Independent Check**: `checks/independent/fsp-efficient-sampling-obligations.py` (`checks=327 scaling_costs=85 bqnf_normal_forms=142 variance_mixing=52 scope_fences=48 failures=0`)
- **Statement-Match Review**:
  1. **What it supports**: Input-size vs representation-cost separation ($4^L > L^3$, $\binom{2m}{m}$ configuration blowup, DQMC rank-1 $c N_s^2 < c N_s^3$ stabilization cost), meron zero-sum pair cancellation preserving $Z = w_1 + w_2$ while raising $\langle\sigma\rangle$ to $1$, RREF canonical section non-optimality in $\ell_1$ norm ($\|N(c)\|_1 = 2 > \|c - d_0\|_1 = 1$), and explicit scope fences showing that strictly positive weights $(p, 1-p)$ do not bound observable variance $1/p - 1$ or bimodal barrier mixing lower bounds $W_{\text{well}} / (2b)$.
  2. **What it does not support**: Does not claim a polynomial-time Monte Carlo sampler for general fermionic models; preserves `OPEN` status.
  3. **Scope fences included**: Positive-weight variance blowup, bimodal barrier conductance bottleneck, configuration-graph exponential size, doped/frustrated Hubbard negative determinant witness, and four-tier epistemic separation.
