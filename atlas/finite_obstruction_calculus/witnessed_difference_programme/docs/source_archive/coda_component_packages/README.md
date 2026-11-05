# CODA source estate and the integrated WDP mathematics

The shared mathematics of these component papers is now organized in
[WDP Appendix P](../../../witnessed_difference_programme.md)
and its [mathematical decomposition](../../coda_mathematical_decomposition.md).
That is the integrated reading route: six reusable constructions connect
the component results, with explicit assumptions and implementation limits.

| Retained component source | WDP construction |
| --- | --- |
| [Stack](coda/coda.md) | Witnessed cut, explicit admissions and layer interfaces. |
| [FOC](foc/coda_foc.md) | Repair quotient, dual certificates and closure modulo a second repair space. |
| [MUR](mur/coda_mur.md) | Quotient transport, square pasting, collisions and loss. |
| [CS](cs/coda_cs.md) | Realized-image factorization and refinement. |
| [CS_Q](cs_q/coda_cs_q_bridge.md) | Approximate decoder bounds and their separation premises. |
| [Q](q/coda_q.md) | Uniform completion and common-target enclosures. |
| [A](a/coda_a.md) | Residual projection and a chosen quotient splitting. |
| [OR](or/coda_or.md) | Compatible overlap gluing and support conditions. |
| [FDA](fda/coda_fda.md) | Terminal paths, guards and conditional standing soundness. |
| [GTLA](coda_gtla/coda_gtla_monograph.md.txt) | Comparison spans, trace erasure, prices and terminal variants. |

The component manuscripts, proof files, computational companions and release
artifacts remain retained sources. Their publication records and older
verification receipts keep their original scopes. This consolidation does
not declare a new deposit or a fresh build of every component proof estate.

The [finite Python application](../../../code/coda_application/README.md) and native
`omega_coda` implement selected finite contracts. Native `omega_q` is a
compatibility re-export of `omega_coda::q`; `omega_wdp` retains source-specific
adapters and observation assembly. The WDP decomposition records their
differences, including the Rust pipeline's refusal of unverified grants.
No source directory is removed and no Rust crate decomposition is performed.

The [current source errata](../../source_errata_20261008.md) qualify claims retained in these historical manuscripts.
