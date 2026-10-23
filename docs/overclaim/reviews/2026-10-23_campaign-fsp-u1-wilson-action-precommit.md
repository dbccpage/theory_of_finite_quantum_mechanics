# Pre-commit statement-vs-theorem review: FSP-U1-WILSON-ACTION

AuthorityEffect: None.

Reviewer: AI agent (campaign author). This is a self-review before the maintainer review; it does not replace it.

## Node statement (after narrowing)

> With link phases U_ij = exp(i A_ij) on ordered vertex pairs and oriented closed-path products U_p over a finite plaquette family, the Wilson action S = beta_g sum_p (1 - Re U_p) is invariant under local U(1) gauge transformations and is nonnegative for beta_g >= 0.

The prior statement did not say `beta_g >= 0`. Without it the nonnegativity claim is false (one self-link plaquette, phase `-1`, `beta_g = -1`, `S = -2`). The prior statement did not fix a link model; the narrowed statement uses ordered vertex pairs.

## Statement-vs-theorem table

| Claim in the node statement | Lean declaration (`lean4/CampaignFspU1WilsonAction.lean`) | Verdict |
|---|---|---|
| Link phases `U_ij = exp(i A_ij)` | `linkOfAngle` (definition, `Circle.exp`) | FULL (definition) |
| Oriented plaquette products `U_p` | `holonomy`, `ClosedPath`, `loopHolonomy` (definitions) | FULL (definition) |
| `S = beta_g Σ_p (1 - Re U_p)` | `wilsonAction` (definition); `wilsonAction_linkOfAngle` gives `β Σ_p (1 - cos Σ_p A)` | FULL |
| Invariant under local `U(1)` gauge transformations | `fsp_u1_wilson_action` (first two conjuncts), `wilsonAction_gauge_invariant`, `linkOfAngle_gaugeAngle` | FULL, for every `g : V → Circle` and every angle shift |
| Nonnegative | `fsp_u1_wilson_action` (third conjunct), `wilsonAction_nonneg` | FULL under `β ≥ 0` (the narrowing) |
| `β ≥ 0` cannot be dropped | `wilsonAction_negative_beta_witness`, `wilsonAction_nonneg_needs_beta` | FULL |
| Lattice reading | `plaquette`, `hypercubicWilson_gauge_invariant`, `hypercubicWilson_nonneg` on `(ZMod L)^d` | FULL for the vertex-pair model; for `L ≤ 2` parallel links are identified |
| Fermion-sign consequence | none | NOT CLAIMED (the source supplies none) |

Axioms: the twelve `#print axioms` lines report only `propext`, `Classical.choice`, `Quot.sound` (`dag/research/campaign_fsp-u1-wilson-action_lean_replay.json`). No `sorry`, `admit`, `axiom`, `native_decide` or `unsafe` in the module.

## Claim hygiene

1. **Supports.** For any vertex type, any finite family of closed oriented paths and any real coupling, the `U(1)` Wilson action is gauge invariant, and it is nonnegative when the coupling is nonnegative; for positive coupling it vanishes exactly on fields flat on the supplied plaquette family.
2. **Does not support.** Any fermion-sign statement; a non-abelian Wilson action; reflection positivity, a transfer matrix or a continuum limit; the multigraph lattice with distinct parallel links at `L ≤ 2`.
3. **Narrowest defensible claim.** `CampaignFspU1WilsonAction.fsp_u1_wilson_action` as stated, with `β ≥ 0` explicit.
4. **Next test.** A maintainer reads the table against the Lean statement of `fsp_u1_wilson_action`; downstream, `FSP-WILSON-DIRAC-GAMMA5` still needs `γ5 D_W γ5 = D_W†` stated for a link field of this type.
