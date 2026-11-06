# Response to the adversarial reviews

The reviewer is a fresh, independent subagent, `strips_adversary`, given the draft and artifact paths without this conversation. It was instructed to seek mathematical errors, hidden assumptions and misleading pictures, and not to edit files. All three responses are retained verbatim. No objection has been deleted or rewritten. v1 and v2 remain available with hashes; v3 is the current classical teaching draft.

## Disposition

| Original finding | Revision |
|---|---|
| V1-1: incorrect rate ratio | Both state panels now use (2.1,1.2); rate lengths are 1.2 and 2.1 on one scale. |
| V1-2: changed state/invisible rotation | Three exact samples share the same starting state, scale and origin; joined endpoint arrows show turning. |
| V1-3: undeclared glyph roles | Companion explicitly maps black/green to q/p, signs and state endpoint. |
| V1-4: ambiguous translation histories | Two explicit orders now start at the same state and end at the same state; intermediate values are given. |
| V1-5: finite-kick interpretation | Captions say same instant; the arrow between the two rate panels is removed. |
| V1-6: unannounced change | First-strip caption explicitly says turn one; the turn preserves length. |
| V1-7: inaccessible proof vocabulary | Plain-language expansion/cancellation mechanism, definitions of derivative and technical terms; page is explicitly a proof sketch. This is not a novice-comprehension test. |
| V1-8: variational endpoint conditions | Independent variations and fixed-q endpoint condition are specified; symmetry translations map endpoint data. |
| V1-9: geometric-phase overstatement | Uses cyclic position/angular phase; distinguishes transport holonomy and quantum amplitude. |
| V1-10: oversized arrowheads/ghost count | Arrowheads capped at 35% of segment length; three intermediate directions stated and drawn directionally. |
| V2-A: operation colors changed meaning | Grey consistently encodes shift; orange encodes slide in both orders. |
| V2-B: rate covered green | Orange rate is offset sideways with its magnitude unchanged. |
| V2-C: undefined assumptions | Added short glosses and proof-sketch label. |

V3 also uses the same unshifted free-particle state (2,0.65) in its final conservation strip, sampled at times 0,1,2. The reviewer checked this consistency and all targeted v3 fixes.

## What remains unresolved

- No novice has tested whether the picture sequence is understood without narration. Reviewer acceptance of the algebra does not establish that.
- The picture sheet introduces a chosen state-plane pairing and dynamics. It does not derive those structures from the supplied alpha paper.
- The alpha paper's earlier comparison/reference-change/detector sequence is mapped in `04_alpha_key_ideas_and_review.md`, not silently inserted as a proven foundation for v3.
- The quantum papers supplied during this task require additional source-specific work before extending this page to Born, Everett or Bell.
- The paper review is bounded prose/algebra inspection. No Lean build, proof-term audit or cited external physical claim has been verified.

## Preserved evidence

- `01_draft_for_review.md`: original storyboard and mathematical contract.
- `02_adversary_v1_verbatim.md`: full original ten-finding critique.
- `03_adversary_v2_verbatim.md`: recheck, three remaining issues and narrow alpha-source verification.
- `05_adversary_v3_verbatim.md`: final focused check, with its limits intact.
- `render_sheets_v1.py`, `render_sheets_v2.py`, `render_sheets_v3.py`: versioned reproducible renderers.
- `v1_manifest.json`, `v2_manifest.json`: preserved artifact hashes.
- `numerical_consistency.json`: numerical checks of the two specified classical flows; explicitly not proof of physical laws.
