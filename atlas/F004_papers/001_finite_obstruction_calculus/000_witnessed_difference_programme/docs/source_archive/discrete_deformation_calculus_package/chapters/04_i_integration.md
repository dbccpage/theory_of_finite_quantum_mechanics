# Chapter 4 — Letter I: integration {#chapter-4}

**Part of:** [Discrete Deformation Calculus v1.0.3](../discrete_deformation_calculus.md)

No progress counts until it is committed. I appends a receipt to an
append-only, hash-chained tape and changes nothing else.

## 4.1 Definition

The tape at step $t$ is $T_t = [r_0, \dots, r_{t-1}]$. With
$h_0 = \mathrm{SHA256}(\text{genesis root})$, the receipt for letter
$\alpha \in \{E, R, C, I, \Lambda, D, M, T\}$ is chained as

$$h_{t+1} = \mathrm{SHA256}\big(t : h_t : \alpha : \mathrm{json}(r_t)\big).$$

Every letter enters the chain, I included; the first draft's letter set left
I out. The index, the previous head (64 hex digits) and the letter cannot
contain the separator, so the preimage parses uniquely. Payloads are
canonical JSON with exact rationals written as strings, and floats are refused.

## 4.2 Step law

I leaves the state unchanged and carries a receipt (Law 5). The historical comparison model checks
the unchanged state (`InertOpMutatedState`); the receipt clause is paper-only
(residual R-DDC-05).

## 4.3 Receipt

`TapeEntry` records `index`, `prev_hash`, `letter`, the canonical `payload` and
`current_hash`.

## 4.4 Results

**Theorem 4.1** (DDC-I-01). The tape only grows: a tape is a prefix of every
later tape, and the receipts of a replay are a prefix of the receipts of any
extension of it. Lean: `Ddc.I_commit_prefix`, `Ddc.I_receipts_prefix`.

**Proposition 4.2** (DDC-I-02). A broken hash or predecessor link is
located by `first_broken_index`. Replacing a final entry and rehashing it,
rewriting a suffix, or truncating the tape can leave a consistent chain.
`verify_integrity(checkpoint)` compares with an independently retained
genesis hash, head hash and length; under SHA-256 collision resistance it
detects these changes. A checkpoint obtained from the suspect tape supplies
no authentication. A final checkpoint detects a mismatch but does not locate
the original first alteration. Tests:
`test_review_regressions.py::test_tape_checkpoint_detects_rehashed_replacement_and_truncation`.

**Proposition 4.3** (DDC-I-03). Replaying the same steps from the same state
reproduces every state and the same head hash. Tests:
`test_automaton.py::test_replay_is_deterministic`, and the pinned heads in
`test_fsm_and_demos.py`.

**Proposition 4.4** (DDC-I-04). A step that fails its law is not committed:
replay stops before recording it. Lean: `Ddc.I_needs_receipt`; test:
`test_automaton.py::test_run_tape_stops_at_the_first_unlawful_step_and_chains_receipts`.

## 4.5 Falsifiers

- An I step without a receipt is refused (`MissingReceipt`).
- An I step that alters the state is refused by paper and historical comparison model.

## 4.6 Nonclaims

```text
I does not claim semantic authority or that committed steps are optimal.
I provides deterministic commitment; historical integrity needs a trusted checkpoint.
No authorization is conferred.
```
