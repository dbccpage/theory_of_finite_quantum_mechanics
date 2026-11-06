# From signed transport to an admitted Hamiltonian

Date: 2026-09-22. AuthorityEffect: None.

## Source custody and the first available constructions

The frozen source is [19L57G1 `sealed-derivation-v1`](https://github.com/dbccpage/19L57G1/tree/sealed-derivation-v1), peeled commit `3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a`. Its mechanical receipt does not certify physical identification or discharge its residual register. The later research below was inspected at commit `30805c5c6598310a4b6cef76e800a9015c9ef56a`; it is post-seal exploratory material and is not part of that receipt. No sealed source was copied or rebuilt for this investigation.

| Logical step | Pinned source | What is supplied and what follows |
|---|---|---|
| Alternating boundary coefficients | [LadderGeneral.lean, lines 38–44 and 299–306](https://github.com/dbccpage/19L57G1/blob/sealed-derivation-v1/lean4/Derivation/LadderGeneral.lean#L38) | Integer coefficients, signs and iteration are declared inputs. Signed deletion is then defined. |
| Double-boundary cancellation | [BoundaryCancellation.lean, lines 25–39 and 377–378](https://github.com/dbccpage/19L57G1/blob/sealed-derivation-v1/lean4/Derivation/BoundaryCancellation.lean#L25) | An unsigned countermodel separates filler admission from alternating signs. `d2_zero_unrestricted` establishes the coefficient identity, not CAR or thermal dynamics. |
| Observer obstruction | [PresentationNaturality.lean, lines 28–68](https://github.com/dbccpage/19L57G1/blob/sealed-derivation-v1/lean4/Derivation/PresentationNaturality.lean#L28) | Observer families and sections are declared; no physical interpretation follows from their names. |
| Native signed hopping | [HopFixture.lean, lines 4–54, 110–168](https://github.com/dbccpage/19L57G1/blob/30805c5c6598310a4b6cef76e800a9015c9ef56a/research/natural_sections/lean/NaturalSections/HopFixture.lean#L4) | Ordered two-occupant configurations, moves and crossings support odd exchange loops on a square and a three-leaf star. No physical system is identified. First entered at `ceb513a8143bb58c397ce303b279421afb26fc81`, 2026-08-30. |
| CAR coefficient comparison | [ExchangeCoefficients.lean, lines 43–64, 84–121 and 135–151](https://github.com/dbccpage/19L57G1/blob/30805c5c6598310a4b6cef76e800a9015c9ef56a/research/exchange_coefficients/lean/ExchangeCoefficients.lean#L43) | Ordered removal/insertion coefficients agree with the two-occupant transport fixture, including its admitted negative hopping convention. First entered at `ac95c8063d03b44907e443b353dd0698b328c383`, 2026-09-09. |

The [exchange-coefficient README, lines 5–29 and 73–75](https://github.com/dbccpage/19L57G1/blob/30805c5c6598310a4b6cef76e800a9015c9ef56a/research/exchange_coefficients/README.md#L5) expressly prices the operator comparison and excludes a dynamics derivation and a general many-occupant correspondence. The [admission-sign shadow, lines 17–30 and 66–79](https://github.com/dbccpage/19L57G1/blob/30805c5c6598310a4b6cef76e800a9015c9ef56a/research/admission_sign_shadow/README.md#L17) retains both trivial and sign characters. Character laws alone do not select the latter.

There are consequently two answers to “where can a Hamiltonian first arise?”

1. After choosing a finite chain complex, complexifying it, and supplying inner products, the Hodge operator
   \[
   H_k=B_k^\dagger B_k+B_{k+1}B_{k+1}^\dagger
   \]
   is a possible positive self-adjoint operator: its quadratic form is
   \(\|B_kv\|^2+\|B_{k+1}^\dagger v\|^2\). Here \(B_k:C_k\to C_{k-1}\). This construction uses the sealed chain ingredients but adds inner products, a chosen complex, energy units and physical interpretation. It selects neither Hubbard dynamics nor a thermal ensemble.
2. Once the post-seal hopping fixture is available, its transport coefficients can be coupled directly to magnitudes and diagonal energies. This yields the more useful many-body bridge below. It is a conditional construction in this paper, not a newly discovered Hamiltonian theorem already proved in the sealed derivation.

The rectangular scale-bonding maps in [ScaleDynamics.lean, lines 19–68](https://github.com/dbccpage/19L57G1/blob/30805c5c6598310a4b6cef76e800a9015c9ef56a/research/sign_tower/lean/ScaleDynamics.lean#L19) change dimension. They cannot themselves be same-space semigroup elements. That observation does not rule out separately constructed Hamiltonians or dilations. [FINDINGS.md, lines 53–67](https://github.com/dbccpage/19L57G1/blob/30805c5c6598310a4b6cef76e800a9015c9ef56a/research/sign_tower/FINDINGS.md#L53) also separates positive cylinder weights from the admission permutation character.

## Conditional signed-transport theorem

Supply a finite configuration set \(X\), a loop-free undirected graph \(G\) on it, symmetric magnitudes \(a_{xy}>0\), edge parities \(\epsilon_{xy}\in\mathbb F_2\), diagonal energies \(V_x\in\mathbb R\), and an orthonormal basis of \(\mathbb C^X\). Define
\[
H_{xx}=V_x,\qquad H_{xy}=-a_{xy}(-1)^{\epsilon_{xy}}
\quad(\{x,y\}\in E(G)),
\]
with zero on other off-diagonal entries. Then \(H=H^\dagger\).

Choose \(E_*\ge\max_xV_x\), and set \(K=E_*I-H\). Its diagonal is nonnegative. For \(\beta\ge0\),
\[
Z=e^{-\beta E_*}\sum_{m=0}^{\infty}\frac{\beta^m}{m!}
\sum_{x_m=x_0}\prod_{j=0}^{m-1}K_{x_{j+1},x_j}.
\]
**Proof.** Factor out the scalar exponential and expand the finite matrix exponential in its absolutely convergent power series. Insert the configuration basis in each trace of \(K^m\). The \(m=0\) contribution is \(|X|\). Every supported hopping walk has sign \((-1)^{\sum_j\epsilon_{x_jx_{j+1}}}\); nonzero diagonal factors add no sign. An odd exchange loop therefore gives a strictly negative individual term for \(\beta>0\), although the full thermal trace is positive. This identifies the required bridge from an exchange character to statistical cancellation.

**Diagonal-gauge criterion.** There exists \(D_{xx}=(-1)^{g_x}\) with all off-diagonal entries of \(DHD\) nonpositive if and only if every cycle of \(G\) has even parity.

**Proof.** The gauge sends \(\epsilon_{xy}\) to \(\epsilon_{xy}+g_x+g_y\). Vertex terms occur twice around each cycle and sum to zero in \(\mathbb F_2\), proving necessity. Conversely choose a rooted spanning forest and define \(g_x\) by the parity of its root-to-vertex path. Every forest edge then has parity zero. Each other edge closes a fundamental cycle, whose even parity forces that edge's transformed parity to zero too. This also supplies a witness and a deterministic normal form once the vertex/edge ordering is fixed. The algorithm takes \(O(|X|+|E|)\) on an explicit graph; \(|X|\) may be exponential in physical sites.

For a number-conserving CAR Hamiltonian, configurations are occupation vectors and the hop sign is the parity of occupied modes strictly between source and destination in the chosen ordering. The post-seal theorem verifies one two-occupant bridge to this rule. Extending to more particles requires the independently admitted Fock construction; it is not supplied by that two-occupant theorem.

## A tree can already carry exchange frustration

Label a star's center 0 and leaves 1, 2, 3. Its two-particle occupation graph contains
\[
\{1,2\}\to\{0,2\}\to\{2,3\}\to\{0,3\}
\to\{1,3\}\to\{0,1\}\to\{1,2\}.
\]
Following the two particle identities around this six-hop loop exchanges them. The hops \(0\to3\), \(3\to0\), and \(0\to2\) have odd between-mode occupancy in the order \(0<1<2<3\); the other three have even parity. Their product is negative. The physical site graph has no cycle; its configuration graph does. Site-graph bipartiteness or acyclicity alone therefore does not establish a sign-free occupation representation for arbitrary particle sectors.

## Residuals that remain

CAR, Hermiticity, locality and number conservation still admit \(H=0\), \(H=\lambda N\), hopping models and interacting Hubbard models. They select a family, not one Hamiltonian. Number conservation also permits higher-body number-conserving terms; a two-body Hamiltonian requires a separate truncation assumption.

The gauge theorem concerns diagonal real sign changes of a specified matrix. It neither obstructs meron regrouping nor determinant representations. A negative loop says nothing by itself about a sampling mixing time, a thermodynamic limit, or an NP-hard family. The frozen [paper's residual register, lines 586–634](https://github.com/dbccpage/19L57G1/blob/sealed-derivation-v1/paper/paper.md#L586) remains distinct from these new model constructions.
