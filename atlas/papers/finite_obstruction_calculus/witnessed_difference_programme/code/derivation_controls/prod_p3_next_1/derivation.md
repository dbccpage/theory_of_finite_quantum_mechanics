# PROD-P3-NEXT-1

Goal id: PROD-P3-NEXT-1

Selected scope for PROD-P3-NEXT-1 is recorded in this note.

## Selected scope

`WdpGuardTransferChecker` adapter (`omega_engine_applications/wdp_products/p3_guard_transfer/adapter.py`) implementing the `GuardTransferChecker` protocol (`omega_engine_applications/wdp_products/p3_guard_transfer/contracts.py`) over `antibody_transfer.checker.transfer` and `antibody_transfer.checker.cost`, with parity and negative-control tests (`omega_engine_applications/tests/test_p3_p5_adapters.py`).

## Hypotheses

H1. A rejection rule $R \subseteq X_{\mathrm{src}}$ is source-sound when $R \cap G_{\mathrm{src}} = \emptyset$ and transfer-safe under adapter $\alpha : \operatorname{dom}(\alpha) \subseteq X_{\mathrm{tgt}} \to X_{\mathrm{src}}$ when $\alpha^{-1}(R) \cap G_{\mathrm{tgt}} = \emptyset$ (WDP Appendix Q.3, `WDP-CHS-P05`, `WDP-CHS-P19`).

H2. Source soundness alone does not imply transfer safety: if a valid target element $y \in G_{\mathrm{tgt}}$ maps under $\alpha$ into $R \subseteq X_{\mathrm{src}} \setminus G_{\mathrm{src}}$, the rule rejects a valid target element (`target_counterexamples` nonempty) and must be refused (`transfer_unsafe`).

H3. On a declared target workload with $N$ candidate occurrences, $h$ early rejections, setup cost $C_0 \ge 0$, guard cost $g \ge 0$, and full evaluation cost $v \ge 0$, the exact saving is $\operatorname{saving} = h v - N g - C_0$, with strict benefit if and only if $h v > N g + C_0$ (WDP Appendix Q.4).

## Derivation

1. **Sound transfer verification (`WdpGuardTransferChecker.transfer`)**:
   - Evaluates the transfer problem via `antibody_transfer.checker.transfer(target)`.
   - Verifies that `rule.source_instance_digest == digest(target["source"])`.
   - Locates `rule.rule_id` in `checked["rules"]`; refuses with `source_unsound` when `source_counterexamples` is nonempty and with `transfer_unsafe` when `target_counterexamples` is nonempty.
   - Emits a transferred `GuardRule` bound to `digest(target["target"])` only when `admitted is True`.

2. **Exact break-even pricing (`WdpGuardTransferChecker.price`)**:
   - Evaluates `antibody_transfer.checker.cost` on the declared `BreakEven` parameters $(N, h, v, g, C_0)$ and verifies exact agreement with `BreakEven.saving()`.
   - For the Appendix Q.4 parameters $(N = 10000, v = 1, g = 1/1000, C_0 = 2)$, $h = 12$ gives $\operatorname{saving} = 0$ (no strict benefit) and $h = 13$ gives $\operatorname{saving} = 1 > 0$ (strict benefit).

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not treat conditional Q.4 arithmetic on declared counts as an empirical hit-rate benchmark.
- It does not infer target transfer safety from source soundness without checking the target valid set under the adapter.
