# PROD-KERNEL

## Target
Implement the canonical **Proof-Carrying Reasoning Kernel** (`PROD-KERNEL`, unblocking 18 downstream nodes in `goal_dag.jsonl`). Every reasoning output is paired with a deterministically checkable receipt or a typed refusal (`Refused` / `RefusalCode`) via `witnessed_difference.receipts` and `certified_progress.checker`, mapped directly onto `omega_engine_operating_system` and `omega_engine_pfp`.

## Mathematical Formulation

Let $M = (S, O, Q, c, T)$ be a finite relational model. A reasoning step takes an input state $x \in S$, proposes a transition or certificate $\pi$, and produces an outcome in the disjoint union:

$$\mathrm{Outcome}(x, \pi) \in \mathrm{Accepted}(\text{receipt}(\pi)) \sqcup \mathrm{Refused}(\text{code} \in \mathcal{R}, \text{detail}),$$

where:
1. **Receipt Determinism**: `make_receipt(step, inputs, outputs, checks)` computes a canonical SHA-256 digest over the sorted JSON representation of `(step, inputs, outputs, checks)`.
2. **Independent Replay Verification**: `verify_receipt(receipt)` recomputes the canonical payload digest and rejects any mutated payload, step label, or check entry.
3. **Typed Refusal Preservation**: When `check_certificate(model, cert)` detects a violation (e.g., invalid state, cost-bound breach, or non-decreasing rank), the kernel emits a structured `Refused(code, detail)` object rather than an unverified string.

## Verification Summary
- Valid certificates produce canonical SHA-256 receipts that pass `verify_receipt`.
- Tampered receipts fail `verify_receipt`.
- Invalid certificates produce typed `Refused` outcomes with explicit `RefusalCode` values.
