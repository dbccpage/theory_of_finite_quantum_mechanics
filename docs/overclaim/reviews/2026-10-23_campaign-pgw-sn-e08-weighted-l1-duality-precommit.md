# Pre-commit review: `PGW-SN-E08-WEIGHTED-L1-DUALITY` (`TFQ-0522`)

AuthorityEffect: None. AI-assisted review; no human attestation.

## Scope and method

Target node: `PGW-SN-E08-WEIGHTED-L1-DUALITY` (`TFQ-0522`, stage `MSSN_SN`, slice `pregenesis_to_wdp`).
Reviewed artifacts:
- `lean4/CampaignSnE08WeightedL1Duality.lean`
- `checks/independent/pgw-sn-e08-weighted-l1-duality.py`
- `dag/derivations/independent/pgw-sn-e08-weighted-l1-duality.md`
- `dag/fragments/pregenesis_to_wdp.json` (`TFQ-0522`)

## Statement-versus-theorem table

| Node clause (`TFQ-0522` summary & obligation) | Lean declaration(s) | Scope / Match |
|---|---|---|
| Finite rational cochain spaces, $d_0 : C^0 \to C^1$, and nonnegative weights $\omega_e$; minimum over $g$ of $\sum_e \omega_e \lvert c_e - (d_0 g)_e \rvert$ equals maximum of $c^T y$ subject to $d_0^T y = 0$ and $\lvert y_e \rvert \le \omega_e$ | `CampaignSnE08WeightedL1Duality.weighted_l1_strong_duality`, `CampaignSnE08WeightedL1Duality.e08_rational` | Full match over any linearly ordered field $K$ and specialized to $K = \mathbb{Q}$ (`e08_rational`) for arbitrary `[Fintype V] [Fintype E]` and `∀ e, 0 ≤ w e` |
| Finite linear-programming duality for the stated feasible bounded problem (previously cited as an unproved assumption over $\mathbb{Q}$) | `CampaignSnE08WeightedL1Duality.farkas`, `CampaignSnE08WeightedL1Duality.farkas_fintype`, `CampaignSnE08WeightedL1Duality.lp_weak_duality`, `CampaignSnE08WeightedL1Duality.lp_strong_duality` | Full match: proved from scratch by induction on the variable dimension via Fourier–Motzkin elimination over $K$ without external LP or Hahn–Banach imports |
| Matching primal and dual feasible values certify optimality | `CampaignSnE08WeightedL1Duality.weak_duality`, `CampaignSnE08WeightedL1Duality.certificate_optimal` | Full match: `cost D w h x = dualObj h y` with `DualFeasible D w y` implies global primal and dual optimality |
| An $\ell^1$ minimizer need not be unique and is not in general the $\ell^2$ harmonic residual | `CampaignSnE08WeightedL1Duality.cyc_optimum`, `CampaignSnE08WeightedL1Duality.cyc_residuals_differ`, `CampaignSnE08WeightedL1Duality.cyc_harmonic` | Full match: oriented 3-cycle witnesses with optimal cost $1$, distinct $\ell^1$ residuals $(1,0,0)$ and $(0,0,1)$, and $\ell^2$ harmonic residual $(1/3,1/3,1/3) \in \ker(d_0^T)$ |
| Categorical adjunction defined by unit, counit, and triangle identities; `AdjunctionCochain` implements $(x \mapsto (x,0), (x,y) \mapsto x)$ and is not the matrix pair $(d_0, d_0^T)$ | `CampaignSnE08WeightedL1Duality.AdjunctionTriangleData`, `CampaignSnE08WeightedL1Duality.adjunctionCochain_section_retraction`, `CampaignSnE08WeightedL1Duality.adjunctionCochain_not_cycD_transpose` | Full match on the declared algebraic separation; `record_status` remains `SOURCE_RECORD` with fence noting that `AdjunctionCochain` in `sn_realizations.py` is a product section/projection |

## Result

- **Outcome**: Discharged imported LP strong-duality assumption (`imports: []`), promoting DAG node `PGW-SN-E08-WEIGHTED-L1-DUALITY` from `CONDITIONAL` to `PROVED_LEAN` while keeping `record_status: "SOURCE_RECORD"` and preserving the `AdjunctionCochain` implementation fence.
- **Axiom check**: Only `propext`, `Classical.choice`, `Quot.sound`.
- **Mutation test**: 6 of 6 one-ingredient mutations killed by `lake env lean`.
- **Independent check**: `checks/independent/pgw-sn-e08-weighted-l1-duality.py` passes 970 exact rational checks across 60 random instances (18 distinct check names) and 2 negative controls (`halved_changed=30`, `free_changed=60`).
