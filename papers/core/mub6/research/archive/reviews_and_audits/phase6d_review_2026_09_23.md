# Phase 6D review: finite fixture and degree-8 diagnostics

**AuthorityEffect:** None.

**Firewall:** `stated region only; mints no authority`

## What is established in this PR

| Component | Checked result | Boundary |
| --- | --- | --- |
| P5 Python and Rust | A rational grid has area one. An assigned three-edge fixture with each weight `12133/15000` has cycle sum `12133/5000`; the exact discrete optimization and coboundary identity agree on supplied cycles. | The weights are assigned from the target sum. The routing rule uses a box coordinate only; it does not prove chart overlap, a transition law, a curvature-to-cochain map, or a MUB obstruction. |
| P5 Lean | Finite directed-pair weight identities, an integer vertex-potential shift identity, and a constant assignment of collar inputs to one chart-label triple. The declared face now requires three distinct labels. | The weight table is not alternating, so it is not a simplicial 1-cochain. The constant assignment ignores the collar data. The conditional `NoCompleteMUB6` clause uses the earlier `h_class`, `h_had`, and `h_bridge` premises independently of the new finite identities. |
| Q4 Python and Rust | Experimental 22x22 and 36x36 rational coefficient matrices and positive witness pivots. The fixture traces are `-9071/10800` and `-5046587/129600`. | Projector-moment identities and a positivity-preserving representation are missing. The negative traces do not refute a MUB candidate or establish a level-4 Lasserre relaxation. The certification APIs refuse these obligations. |
| C5 | The PR author recorded prior build and receipt checks. | Those checks need replay after the review repairs. Digest agreement alone does not discharge a mathematical claim. |

The P5 diagnostic receipt uses schema `mub.target_b2_nerve_chaining_diagnostic.v2`. It records `mathematical_certification: false`, `collar_overlap_verified: false`, and `curvature_to_cochain_verified: false`. Its auditor replays the canonical finite fixture and compares the complete serialized receipt; changing a numerical field or an authority flag fails audit. The Python and Rust solvers reject non-integral scaled weights rather than truncating them. Rust also rejects out-of-range weights, and both implementations reject repeated chart labels in a triangular input.

## Replay and remaining work

The review ran all 24 P5 and 14 Q4 Python test functions locally against the branch files through a small `pytest.raises` compatibility shim, plus Python syntax compilation. The checkout available to the reviewer has no `pytest`, `cargo`, or `lake` executable; this is not a full CI run. Run `python -m pytest tests/mub_verify -n 8 --basetemp=scratch/pytest_tmp`, `cargo test -p omega_mub`, and `lake build` from their documented roots before treating the multi-runtime regression as checked.

The scientific P5 obligation remains: construct a genuine alternating transition 1-cochain from chart and collar overlap data, prove the routing and curvature comparison on the stated parameter region, and connect that witness to the finite cycle computation. A positive cycle sum assigned directly in a fixture cannot supply that bridge.

