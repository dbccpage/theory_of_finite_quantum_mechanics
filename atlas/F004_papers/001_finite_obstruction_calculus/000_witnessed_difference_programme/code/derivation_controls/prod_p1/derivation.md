# PROD-P1

## Target
Bind the **P1 Abstention and Impossibility Governor** (`PROD-P1`) to `omega_engine_pfp` via `EvaluateAbstentionGovernorUseCase` and `WdpAbstentionGovernorAdapter`. Every bounded-budget query is evaluated over its finite arena (compressed via coarsest congruence quotient when enabled) and assigned an exact 4-label termination partition (`TERMINATED`, `OUT_OF_FUEL`, `IMPOSSIBLE`, `INVALID_REQUEST`) backed by an independently checked progress certificate and `PROD-KERNEL` SHA-256 receipt.

## Mathematical Formulation

Let $M = (S, O, Q, c, T)$ be a finite relational arena with initial state $s_0 \in S$, target set $G \subseteq S$, and fuel budget $B \in \mathbb{Q}_{\ge 0}$.
1. **Congruence Quotient Compression (`REV-SMRM-P1-QUOTIENT`)**: Refines the target/non-target seed partition to the coarsest congruence $\sim_q$ and compresses $M \mapsto M / {\sim_q}$, preserving the optimal winning value $V^*(s_0)$.
2. **Exact 4-Label Partition (`PROD-P1-NEXT-1`, `PROD-P1-KILL`)**:
   - `IMPOSSIBLE` when $V^*(s_0) = \infty$ (target unreachable under any finite budget),
   - `OUT_OF_FUEL` when $B < V^*(s_0) < \infty$,
   - `TERMINATED` when $B \ge V^*(s_0)$,
   - `INVALID_REQUEST` when the arena or certificate fails structural verification.

## Verification Summary
- `EvaluateAbstentionGovernorUseCase` in `omega_engine_pfp` compresses the symmetric 4-state arena to 3 quotient classes and emits `OUT_OF_FUEL` at budget `"2"`, `TERMINATED` at budget `"3"`, and `IMPOSSIBLE` on an unreachable arena, each with a verified `PROD-KERNEL` receipt.
