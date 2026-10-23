# References and their role {#references-and-their-role}

External literature supplies definitions and context; none of these references
authenticates a DDC runtime or supplies a licence. Local companion links are
pinned to repository commit e4a1214bb3e47570b0f74ecc9117c98f27a26b5e.

1. J. H. Carroll. *Local Green, Global Red I: Evaluated Path Kernels for
   Composed Agent Reliability*, v1.2.3 (2026).
   [Pinned companion source](https://github.com/dbccpage/the_symbol_game/blob/e4a1214bb3e47570b0f74ecc9117c98f27a26b5e/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/012_local_green_global_red_foundational_series/lggr_i_evaluated_path_kernels/lggr_i_evaluated_path_kernels.md).
   Context for the local/global distinction; no DDC proof depends on it.
2. J. H. Carroll. *Finite Obstruction Calculus: Exact Quotient Diagnostics,
   Dual Witnesses, Two-Stage Coherence, and Transport*, v3.2.0.
   [Pinned companion source](https://github.com/dbccpage/the_symbol_game/blob/e4a1214bb3e47570b0f74ecc9117c98f27a26b5e/omega_engine_atlas/coda_atlas/F005_coda/foc/coda_foc.md).
   Context for §3; the DDC graph formulas and arguments are supplied locally.
3. J. H. Carroll. *Six jobs, not one machine: obstruction, standing,
   transport, comparison, shadow, leftover*, v3.2.0 (2026).
   [Pinned companion source](https://github.com/dbccpage/the_symbol_game/blob/e4a1214bb3e47570b0f74ecc9117c98f27a26b5e/omega_engine_atlas/coda_atlas/F005_coda/coda_gtla/coda_gtla_monograph.md).
   Background to the authorization distinction. DDC's refusal terminal is an
   explicit local policy, not an application of an unstated external theorem.
4. F. Birkmann, H.-P. Deifel and S. Milius. *Distributed Coalgebraic Partition
   Refinement*. TACAS 2022, LNCS 13244, 159–177.
   [DOI 10.1007/978-3-030-99527-0_9](https://doi.org/10.1007/978-3-030-99527-0_9),
   [arXiv:2204.06248](https://arxiv.org/abs/2204.06248).
   Positioning for Appendix C.2; no implementation is imported.
5. J. Meseguer. *Conditional rewriting logic as a unified model of concurrency*.
   Theoretical Computer Science 96(1), 73–155 (1992).
   [DOI 10.1016/0304-3975(92)90182-F](https://doi.org/10.1016/0304-3975(92)90182-F).
   Prior-art context for §16; separation from rewriting logic remains open.
   [Maude project overview](https://maude.cs.illinois.edu/overview) and
   [documentation](https://maude.cs.illinois.edu/documentation).
   The framework can represent other operational specifications; DDC's
   chosen guards and receipt fields do not establish an expressivity separation.
6. D. Deutsch and C. Marletto. *Constructor theory of information*.
   Proceedings of the Royal Society A 471, 20140540 (2015).
   [DOI 10.1098/rspa.2014.0540](https://doi.org/10.1098/rspa.2014.0540),
   [arXiv:1405.5563](https://arxiv.org/abs/1405.5563).
   Possible/impossible transformations are a comparison in §16, not a physics claim.
7. J. J. M. M. Rutten. *Universal coalgebra: a theory of systems*.
   Theoretical Computer Science 249(1), 3–80 (2000).
   [CWI publication record](https://ir.cwi.nl/pub/48),
   [DOI 10.1016/S0304-3975(00)00056-6](https://doi.org/10.1016/S0304-3975(00)00056-6).
   Coalgebraic context for signatures and transition systems in Appendix C.2.
8. B. Coecke and A. Kissinger. *Picturing Quantum Processes: A First Course
   in Quantum Theory and Diagrammatic Reasoning*. Cambridge University Press
   (2017), ISBN 978-1-107-10422-8.
   [Publisher record](https://www.cambridge.org/core/books/picturing-quantum-processes/1119568B3101F3A685BE832FEEC53E52).
   Diagrammatic context only; Appendix A's proposed adapter remains unproved.
9. L.-H. Lim. *Hodge Laplacians on Graphs*. SIAM Review 62(3), 685–715 (2020).
   [DOI 10.1137/18M1223101](https://doi.org/10.1137/18M1223101),
   [arXiv:1507.05379](https://arxiv.org/abs/1507.05379).
   Linear-algebra background for the decomposition stated and proved in §3.
10. The Lean project. [Lean 4 reference manual](https://lean-lang.org/doc/reference/latest/).
    The executable toolchain is pinned to v4.34.0 in lean4/lean-toolchain;
    the axiom report records the actual compiler version and commit.
