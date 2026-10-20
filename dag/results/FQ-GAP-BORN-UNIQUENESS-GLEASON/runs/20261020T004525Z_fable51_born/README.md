# Born-rule uniqueness: Fable 5.1 review checkpoint

AuthorityEffect: None. **Stopped for review: the 120000-token total generation ceiling was reached. No general Born-rule or effect-valuation uniqueness theorem is accepted.**

The cap was interpreted as a total across this run, including thinking and answer text. Two `claude-fable-5-1` calls used `xhigh`. P0 returned a detailed mining proposal: 78058 output tokens, including46062 thinking tokens. P1 used its remaining41942 output tokens entirely in thinking, ended with `max_tokens`, and returned **zero visible answer bytes**. It supplied no proof certificate or operad delta. No retry was sent. P2 records absence of a candidate; P3/P4 were not entered. P5 records the budget stop.

Total measured API usage:56166 input tokens and120000 output tokens, including88004 thinking tokens. Published standard-rate estimate: **USD6.56166**. Invoice cost is unobserved. The adapter initially classified the non-end-turn response as unknown; the retained terminal `message_delta`/`message_stop` provided authoritative usage for an offline accounting reconciliation. That reconciliation accepts no mathematics.

The original SSE stream and timestamped received-line log are saved for both calls. `response.json` is reconstructed from those events. `response.txt` contains only the visible answer; the P1 file is intentionally empty. The service did not expose the counted private thinking text. The raw response, error, original reservation and accounting reconciliation are preserved separately.

P0 collected12 proposed generators,13 relations,5 composition proposals,5 failed compositions and6 counterexample proposals. These are proposals, not established operads. The host separately checked four control operations, three relations and two typed compositions on the explicit rational symmetric-matrix carrier. Its matrix algebra/readout is supplied, not derived physics. Full refined-carrier operad coherence remains open.

Independent validation: Python Fraction and standalone Rust agree on all four complete numeric records; eight Rust tests and52 field/type mutations pass. The repaired concrete matrix module compiles with eight named axiom reports containing only propext, Classical.choice and Quot.sound. A concrete positive effect valuation witnesses consistency of the admitted hypotheses. The original failed matrix compiler run and its recovery sorryAx reports remain rejected. These checks do not provide any of the eight general Fable target proofs. Twelve stage-protocol tests also passed. Final custody/audit receipts are under `final_checks`.

Review corrected a Fable source-audit mistake: `Enum` in HWKernel.lean has a nodup field, so duplicate entries cannot inflate that enumeration. Label cardinality still does not establish Hilbert dimension. The historical/current paper-hash difference was reconciled by the exact existing filename/line-ending migration, retaining both byte versions. Every P0 claim has an explicit disposition in `p0_mine/claim_review.json`; extension, trace-representation and real-continuum claims are not promoted.

The first missing lemma is rational homogeneity of an effect-additive valuation: prove p(qA)=q p(A) for rational0<=q<=1 without assuming linearity, while proving intermediate arguments remain effects. `contract.lean`, `target_types.txt` and `host_type_wrappers.txt` freeze the larger eight-lemma interface. A future attempt should start directly at P1, not repeat mining. Full projective Gleason uniqueness and operational justification of effect additivity remain separate obligations.

Key files: `p0_mine/response.txt`, `p0_mine/operad_delta.json`, `p0_mine/claim_review.json`, `p1_derive/raw.sse`, `accounting_reconciliation/receipt.json`, `p5_record/checkpoint.json`, `host_control_operad_delta.json`, and `verify_run.py`.

The earlier canonical operad collections and all prior staged evidence remain unchanged. No commit, push, PR or merge was performed.
