# Pre-Commit Review: `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` (`TFQ-1149`)

AuthorityEffect: None.

- **Node**: `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` (`TFQ-1149` / `MAJ-OPEN-LOCALITY-VIABILITY`)
- **Stage**: `MAJORANA`
- **Status**: `OPEN` (preserved)
- **Evidence Grade**: `E1 -> E3` (`L4D`, 0 flags)
- **Lean 4 Module**: `lean4/CampaignMajOpenLiebRobinsonLocality.lean` (10 theorems, 0 `sorry`, 0 custom axioms, 6/6 mutants killed)
- **Independent Check**: `checks/independent/maj-open-lieb-robinson-locality.py` (`PASS: checks=11633 cone=2100 viability=6424 tail=405 scope_fences=2704 failures=0`)
- **Statement-Match Review**:
  1. **What it supports**: Discrete Lieb-Robinson causal radius and 1D support diameter growth $W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t) = w_0 + 2 v_{\mathrm{LR}} t$, the syndrome recovery viability threshold $2 W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t) < d$ vs logical-collision split $d \le 2 W_{\mathrm{LR}}(w_0, v_{\mathrm{LR}}, t)$, discrete commutator tail suppression $c_0 g^t < c_0 \mu^{\mathrm{dist}}$ for $t < \mathrm{dist}$, and classical syndrome-routing delay bounds.
  2. **What it does not support**: Does not derive continuous-time Banach-algebra Lieb-Robinson bounds for microscopic superconducting Hamiltonians and does not establish a general verdict on physical quantum computing viability (`OPEN` status preserved).
  3. **Scope fences included**: `torus_tetron_viability_window_witness` and `lieb_robinson_locality_open_scope_fence`.
