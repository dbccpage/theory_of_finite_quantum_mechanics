# Paper Claim Ledger: S(n) Tower Architecture

**Document:** `papers/000_sn/paper.md`  
**AuthorityEffect:** None.

| Claim ID | Section | Type | Formal Statement | Evidence / Check | Scope Boundary |
|---|---|---|---|---|---|
| `SN-C01` | Sec 1 | Proved Law | Mathematical realizations have zero authority to extend Genesis. | Two Boxed Laws | Metatheoretic invariant. |
| `SN-C02` | Sec 3.0 | Proved Theorem | S(0) ground state has proved inertia (`genesis_underivable`, `supply_no_op`). | Lean 4 proof kernel | Holds over void carrier $V_0 = \emptyset$. |
| `SN-C03` | Sec 3.1 | Proved Theorem | Renaming the lone mark does not alter presentation structure. | Permutation invariance | Subsingleton carrier. |
| `SN-C04` | Sec 3.2 | Proved Theorem | Admitting two marks without distinguishing forms leaves them observationally collapsed. | $S_2$ basis permutation | Requires explicit form to separate. |
| `SN-C05` | Sec 3.3 | Proved Theorem | Cost-2 floor theorem: minimum separation cost is strictly 2 items (1 form + 1 instance). | `cost1_insufficient_general` | Minima tied under $\mu_1$, unique under $\mu_2$. |
| `SN-C06` | Sec 3.4 | Proved Theorem | Automorphism orbit closure terminates at fixpoint with zero unresolved obstructions ($s_4 = 0$). | `terminal_all_separated` | Progress theorem holds. |
| `SN-C07` | Sec 3.5 | Proved Invariant | Endogenous demand halts at closure fixpoint (`OB-1`), requiring external continuation policy. | `engine.build_tree` | Token ingestion boundary. |
| `SN-C08` | Sec 3.6 | Proved Contract | Adjacent presentation stages relate via section lift $u_N$ and retraction down-map $r_N$. | `r_N(u_N(x)) = x` | Section/retraction, not involution. |
