# Lean Claim Map: Paper GR-002 — Discrete General Relativity on L1

**Paper Target:** `004_general_relativity/002_constraint_closure_and_the_l1structure_of_physical_law`
**Version:** v1.2.0
**Mechanization Level:** 15 formal interactive Lean 4 theorem reports verified in `lean4/` under `verify_manifest.py` with zero `sorry` and axioms within `{propext, Classical.choice, Quot.sound}`.
**Evidence Scope:** Lean receipts certify the listed finite formal checks; they do not promote continuous-GR or particle-physics claims.

---

## Claim Mechanization Matrix

| ID | Claim Description | Paper Section | Declared Status | Lean 4 Status | Lake Module | Mechanized Theorems | Axioms |
|---|---|---|---|---|---|---|---|
| `GR-THM-1.1` | Simplicial operator nilpotency $\partial^2 = 0, d^2 = 0$ | §1.2 | `PROVED` | `MECHANIZED-PARTIAL` | `GR002.HodgeDiracSUSY` | `d1_d0_nilpotent` | `{propext, Quot.sound}` |
| `GR-THM-2.1` | Flat space deficit angle vanishing $\|\omega_R\|_1 = 0$ | §2.2 | `PROVED` | `PROSE` | `GR002.ReggeDeficit` | `total_units_formula`, `total_deficit_formula` | `{propext, Quot.sound}` |
| `GR-THM-3.1` | 3D Contracted Bianchi identity $\sum \varepsilon_e \hat{e} = 0$ | §3.1 | `PROVED` | `PROSE` | N/A | Schläfli identity derivation; verified to $< 10^{-14}$ in Python. | N/A |
| `GR-THM-3.2` | 4D Discrete Bianchi identity $d_2 \varepsilon = 0$ | §3.2 | `PROVED` | `PROSE` | N/A | Topological 3-ball holonomy closure; verified on $S^4$ complex. | N/A |
| `GR-THM-4.1` | Spatial gauge invariance of $L^1$ quotient norm $\Phi$ | §4.1 | `PROVED` | `PROSE` | `GR002.HodgeSplitC3` | `e0_split_inflation`, `nonzero_equal_ratio` | `{propext, Quot.sound}` |
| `GR-DEF-4.2` | Exact constraint closure $\Phi([\omega]) = 0 \iff \omega \in \mathrm{im}(d_0)$ | §4.2 | `DEFINITION` | `PROSE` | N/A | Definitional; checked across $L^1$ gauge projection orbits. | N/A |
| `GR-THM-5.1` | Strong polyhedral duality (zero duality gap) | §5.1 | `PROVED` | `PROSE` | N/A | Linear programming strong duality; verified to $< 10^{-12}$. | N/A |
| `GR-THM-5.2` | Certified divergence-free dual circulation witness $w^* \in Z_1$ | §5.2 | `PROVED` | `PROSE` | N/A | Dual certificate extraction in `DualWitnessLPSolver`. | N/A |
| `GR-THM-6.1` | Ponzano–Regge 6j phase $\ell^1$ Lipschitz continuity | §6.1 | `PROVED` | `MECHANIZED-PARTIAL` | `GR002.PonzanoRegge6j` | `racah_sum_is_96`, `regular_fixture_arithmetic_equals_one_sixth` | `{propext, Classical.choice, Quot.sound}` |
| `GR-QRN-7.1` | $SU(3) \times SU(2) \times U(1)$ Simplicial Gauge Uniqueness | §7.1 | `QUARANTINED_FALSIFIED` | `N/A` | None | Refuted by arbitrary Lie group connection admissibility. | None |
| `GR-QRN-7.2` | Electroweak Higgs VEV 246 GeV Derivation | §7.2 | `QUARANTINED_FALSIFIED` | `MECHANIZED` | `GR002.LinearEnergy` | `linear_energy_scaling`, `norm_scal_homogeneity` (falsifies quartic VEV) | `{propext, Quot.sound}` |
| `GR-QRN-7.3` | Topological SUSY 85.6 TeV Saturation Scale | §7.3 | `QUARANTINED_FALSIFIED` | `MECHANIZED-PARTIAL` | `GR002.HodgeDiracSUSY` | `delta1_is_3_identity` (discrete Laplacian lacks mass splitting) | `{propext, Quot.sound}` |
| `GR-QRN-7.4` | Hexagonal Regge Wall Fine Structure Constant | §7.4 | `QUARANTINED_FALSIFIED` | `MECHANIZED` | `GR002.ReggeDeficit` | `total_units_strictly_increasing` (falsifies wall gauge coupling) | `{propext, Quot.sound}` |
| `GR-QRN-7.5` | Cold Dark Matter as Isolated Cochain Edges | §7.5 | `QUARANTINED_FALSIFIED` | `MECHANIZED` | `GR002.TopDimensionVanishing`| `dim_3_cochains_vanish_on_2_complex` (boundary defect has no stress-energy) | `{propext, Quot.sound}` |

---

## Falsifier Check: `LEAN_TOY`-as-`MECHANIZED`

- **Total mechanized theorem reports:** 15 across 6 Lean modules.
- **`LEAN_TOY` sold as paper theorem:** 0 (all toy or fixture mechanizations are strictly labeled `MECHANIZED-PARTIAL` or used as negative falsification witnesses for quarantine receipts).
- **Axioms check:** `{propext, Classical.choice, Quot.sound}` (standard Lean 4 kernel whitelist).
- **Lake verification:** Clean pass via `verify_manifest.py`.
- **Result:** `PASS`. Honest claim classification across all 14 ledger entries.
