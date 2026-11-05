# Claim Ledger for Minimal Symbol System - N (MSS-N) Foundational Monograph Package

AuthorityEffect: None. GenesisEffect: None.

This ledger records every mathematical derivation, empirical grammar finding, and architectural claim in `paper.md`, accompanied by its verification evidence and boundary.

| Claim ID | Section | Category | Description | Exact Verification Evidence |
| :--- | :--- | :--- | :--- | :--- |
| `CLAIM-MSSN-001` | §0 | Pre-Genesis | Distinguishes four mathematical states: absent input (typed `None`), empty word $\varepsilon$, literal boundary packet $\langle\rangle$, and declared ground carrier. | Typed option formalization; absence of $\varepsilon$ production in `word` EBNF rule. |
| `CLAIM-MSSN-002` | §1 | Data Separation | Distinguishes 8 dimensions of declared data and decouples encoded graph relations $E$, rewrite relations $\to_{\text{rewrite}}$, and observation maps $q$. | Structural separation in §1.1-§1.2; schema contracts in `nf.mssn.yaml`. |
| `CLAIM-MSSN-003` | §3 | Monoid Algebra | Free monoids on distinct numbers of generators are non-isomorphic: $\{0,1\}^* \not\cong \{0,\dots,9\}^*$. | Formal proof via indecomposable elements (generators) in §3.3. |
| `CLAIM-MSSN-004` | §3 | Category Theory | Discrete categories $\mathbf{C}_2$ and $\mathbf{C}_{26}$ are neither isomorphic nor equivalent. | Proof via object class cardinality and absence of non-identity arrows in §3.4. |
| `CLAIM-MSSN-005` | §4 | Retraction | For terminal alphabets $A \subseteq B$, language inclusion lift and restriction satisfy $r(\ell(L)) = L$ on $\mathcal{P}(A^*)$. | Set-theoretic derivation in §4.1; language intersection on string sets. |
| `CLAIM-MSSN-006` | §4 | Erasure | Total projection homomorphism $h: B^* \to A^*$ induces information loss by erasing symbols in $B \setminus A$. | Algebraic definition in §4.1; counter-example $h(a_1 b a_2) = a_1 a_2$. |
| `CLAIM-MSSN-007` | §5 | Graph Homology | Finite graph with $c$ connected components has $H_0 \cong \mathbb{Z}^c$ and $\tilde{H}_0 \cong \mathbb{Z}^{c-1}$. | Standard simplicial graph homology boundary matrix rank in §5.1. |
| `CLAIM-MSSN-008` | §5 | Obstruction Theorem | An extension killing a non-zero homology class cannot have a chain-map retraction fixing the original complex. | Formal proposition proof and 2-point, 1-edge counterexample in §5.2. |
| `CLAIM-MSSN-009` | §5 | Cycle Filling | Inscription `a>b>c>a` defines a 1-cycle $z$ with $\partial_1 z = 0$ in the 1-skeleton; filling requires an explicitly added 2-cell $f$. | Direct calculation $\partial_1 z = (b-a)+(c-b)+(a-c) = 0$ in §5.3. |
| `CLAIM-MSSN-010` | §6 | Grammar Profiles | Creator examples `a>b>c>a` and `a0>b2>c1>a0` are evaluated across four distinct profile readings with differing acceptance. | Verified by `check_mssn.py` and fixtures in `mssn_conformance_cases.json`. |
| `CLAIM-MSSN-011` | §6 | Implementation | The engine registers 28 total profiles (6 retained + 22 new starts) and exercises 3 production parsers at runtime. | Runtime check in `check_grammars.py --runtime` and inventory in §6.4. |
| `CLAIM-MSSN-012` | §7 | Codec Collisions | Non-injective code $a \mapsto 0, b \mapsto 00$ produces exact collisions $aa, b \mapsto 00$ and $ab, ba \mapsto 000$. | Algebraic calculation in §7.1. |
| `CLAIM-MSSN-013` | §7 | Edge Inversion | Reversing traversal order and inverting directions ($a>b \to b<a$) preserves directed edge representation. | Direct derivation in §7.2. |
| `CLAIM-MSSN-014` | §8.1 | Ontology | Index Non-Identity Invariant: Atlas specification row index does not equal Genesis derivation index (MSS-2 != S(2)). | Formalization in §8.1; crosswalk table in `levels/README.md`. |
| `CLAIM-MSSN-015` | §8.2 | Ascent | Ascent Triad: A declared successor specification does not constitute a candidate lift or licensed lift. | Procedural definition in §8.2. |
| `CLAIM-MSSN-016` | §8.3 | Accounting | Dual Accounting Invariant: Atlas specification coverage C(N) does not compute licensed machine-checked depth D(k). | Formal separation in §8.3; verified by `verify_normal_forms.py`. |
| `CLAIM-MSSN-017` | §8.4 | Runtime | Proposer-Host Oracle evaluates streams into four mutually exclusive terminal states: Saturation, Blocked Extension, Budget Stop (UNKNOWN), and Licensed Lift. | State-machine classification in §8.4 and `nf.mssn.bqnf.yaml`. |
| `CLAIM-MSSN-018` | §8.6 | Codec | Historical rational representation encodes -3/2 via binary payloads as op<<10010><1><11><10>> rather than decimal floating point. | Verified against `historical_packet.ebnf` and golden corpus replay. |
