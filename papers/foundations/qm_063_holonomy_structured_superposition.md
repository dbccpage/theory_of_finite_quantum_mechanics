> **Annex notice (2026-07-31, AuthorityEffect: None).**  
> Packaging annex absorbed: `qm_064_phase_gauge_residual/` (phase 1-cochain gauge residual / holonomy invariance — annex to holonomy-structured superposition).  
> Claim namespaces remain distinct; this is not a theorem upgrade.


# 063 Holonomy Structured Superposition

## GTOC Foundations — Quantum Contact Series (qm_063_holonomy_structured_superposition)

**Date:** 2026-07-29 · **Version:** v1.0  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  
**Status:** RELEASED  
**Authority:** `AuthorityEffect::None`  

## Mechanism inventory

| Slot | Value / Description |
| --- | --- |
| **Primitive Differences** | $\delta c = \text{{defect mass}}$ |
| **Carriers / Structure** | Finite Graph 0-Cochain / Hilbert Space |
| **Cochain complex** | $C^0 \to C^1 \to C^2$ |
| **Coboundary maps** | $\delta^0, \delta^1$ |
| **ZeroRel** | Preserved under $L_1$ quotient |
| **Licensed repairs** | None |
| **Quotient / Q1** | Banach Quotient |
| **Residuals** | $\delta c \neq 0$ boundary defect |
| **Witnesses** | Replayable Python / Rust Certifiers |
| **Observers / profiles** | Operational Observer |
| **Anomalons** | None |
| **CompletionLaw** | Finite Cochain Completion |
| **Terminal / route** | Route to 003 Quantum Foundations |
| **AuthorityEffect** | None |

Quantum Contact 1 - Holonomy-Structured Superposition
=====================================================

U(1) transport on a finite carrier, coherent L2 lifts of L1 weights, and the exact interference obstruction

**Series role:** supplementary quantum-contact paper; not a new GTOC degree
**Claim ledger:** [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (IDs `063:QCS-C1` through `063:QCS-C11`)
**Version:** v1.0
**Terminal:** `OpenObstruction` at the unimported L1 boundary; exact conditional results after the stated U(1)/L2 import
**Authority effect:** `None`
**Depends on:** [`qm_072_bit_shadow_and_qubit.md`](qm_072_bit_shadow_and_qubit.md), [`qm_073_correlation_separability_finite_bell.md`](qm_073_correlation_separability_finite_bell.md), [`qm_020_born_normalization_and_conditional_hilbert_lift.md`](qm_020_born_normalization_and_conditional_hilbert_lift.md), and [`qm_061_interference_as_the_non_l1_resource.md`](qm_061_interference_as_the_non_l1_resource.md)
**Mechanization:** not started; targets are stated in Section 9

Abstract

Finite nonnegative L1 weights determine normalized proportions but forget phase. A coherent L2 lift adds square-root amplitudes, a complex involution, and a quadratic readout. This paper makes one further import explicit: a U(1) connection on a finite path carrier. With that structure in place, phase is no longer an arbitrary label. It is transport, and relative phase is loop holonomy.

For two source-to-sink paths `p` and `q` with weights `w_p,w_q` and transports `H_p,H_q in U(1)`, the coherent intensity is

$$
I(p,q)=w_p+w_q+2\sqrt{w_pw_q}\,\operatorname{Re}(H_p\overline{H_q}).
$$

The cross-term is therefore exactly controlled by the relative loop holonomy `H_p overline{H_q}`. This closes a finite, conditional bridge that earlier work left interpretive. It does not derive superposition from L1, derive U(1), derive Hilbert space, or derive quantum mechanics. It proves what follows after those structures are licensed.

On a finite 2-complex, vertex phases form `C^0`, edge phases form `C^1`, and face curvature is `d^1 a in C^2`. The identity `d^1 d^0=0` makes face curvature gauge invariant. Curvature and global holonomy must not be conflated: a flat connection can retain nontrivial holonomy on a non-simply-connected carrier. Conversely, every U(1) connection on a tree is gauge-trivial. More than one dimension matters through faces, curvature, and higher consistency; ordinary path interference itself remains a one-cycle phenomenon.


0. Scope, terminal, and nonclaim fence


The numbered `paper_N` namespace is reserved for the eleven degree papers `delta0` through `delta10`. This paper is a contact construction over resources that Paper 7 explicitly prices as Q1 and Q2. It introduces no degree and changes no lower-degree availability claim.

There are two distinct verdicts:

1. **At the L1-only boundary:** superposition, phase transport, and quadratic interference remain `OpenObstruction`. Supplying them from outside the earned carrier routes through `OracleNeeded` under GTOC-8.
2. **Inside the declared finite U(1)/L2 carrier:** the algebraic identities in Sections 3-6 are proved conditionally. Their authority effect remains `None`.

Retained-carrier prerequisite: every finite path, edge phase, face, and weight below is a declared retained object. A lower-degree flicker that fails the Paper 0 retention gate does not become a zero-amplitude path or a hidden phase; it is outside this imported carrier.

This paper does not claim:

* that L1 weights force complex amplitudes;
* that U(1) transport is derived from the retained admitted-cut basement;
* that a finite complex vector space is a physical Hilbert space;
* that the Born rule is ontologically unique;
* that a graph or 2-complex is physical spacetime;
* that interference alone derives quantum mechanics;
* that any conditional theorem mints epistemic or institutional authority.

### Import Ledger 0

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| finite weights and normalization | `delta2` | Paper 2 | derived conditionally under its standing conventions |
| bit-shadow and Q1-Q4 price | `delta7` | Paper 7 | derived price boundary, not a qubit |
| U(1), complex conjugation, square root | not earned in the degree ladder | this paper | **IMPORTED - Q1/R1 plus finite scalar support** |
| coherent quadratic readout | not earned in the degree ladder | this paper | **IMPORTED - Q2** |
| authority | never inferred from structure | charter / GTLA firewall | `None` |

**Connective audit.** Section order is exposition order, not a derived temporal order.
**Genesis-Bias audit.** The graph and connection are declared finite carriers, not antecedent physical arenas.


1. The primitive difference for superposition


Let `P` be a finite family of distinguishable alternatives connecting one declared source `s` to one declared sink `t`. An L1 packet supplies only nonnegative weights

$$
w:P\longrightarrow \mathbb{R}_{\ge 0},
\qquad
W=\sum_{p\in P}w_p>0.
$$

Its normalized shadow is

$$
\pi_p=\frac{w_p}{W}.
$$

The L1 packet is phase-blind. Two candidates can have the same path set and the same weights while producing different coherent intensities after a merge. That pair is the primitive difference studied here:

$$
(P,w,H)\not\sim (P,w,H')
\quad\text{although}\quad
(P,w)=(P,w).
$$

The missing datum is not another nonnegative weight. It is the relative transport between alternatives.

### Definition 1.1 - Zero relation

Two finite transport packets are locally zero-related when they have:

1. the same declared graph and oriented path family;
2. the same L1 weights;
3. connections related by a vertex gauge transformation;
4. the same coherent readout rule.

The relation deliberately does not identify connections with different gauge-invariant loop holonomy. That difference survives all allowed local phase repairs.

### Proposition 1.2 - The L1 shadow forgets the candidate difference

The projection

$$
\mathcal{S}_1:(P,w,H)\longmapsto (P,w)
$$

is non-injective whenever the carrier admits two connections with distinct relative path holonomy.

**Proof.** Keep `P` and `w` fixed and vary only the connection. The projected packets are equal by construction. Section 3 gives an explicit pair for which the coherent intensities differ. Therefore the coherent distinction does not factor through `mathcal{S}_1`. $\square$

### Import Ledger 1

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| finite path family | carrier declaration | this paper | **DECLARED** |
| nonnegative weights | `delta2` | Paper 2 | available as finite proportions |
| connection and gauge | not earned | Section 2 | **IMPORTED** |
| coherent distinguishability | not earned | Section 3 | **IMPORTED readout** |

**Connective audit.** “Connecting” means graph incidence, not temporal travel.
**Genesis-Bias audit.** `s` and `t` are typed endpoints in a declared combinatorial carrier, not locations in prior space.


2. Declared finite carrier and coherent lift


### Definition 2.1 - Oriented graph carrier

Let `X=(V,E)` be a finite connected graph. Each unoriented edge has two orientations `e` and `bar e`, with

$$
s(\bar e)=t(e),\qquad t(\bar e)=s(e).
$$

A path `p=e_1\cdots e_n` is an incidence-compatible finite edge word. Its reverse is `bar p=bar e_n\cdots bar e_1`.

### Definition 2.2 - Finite U(1) connection

A U(1) connection is a map

$$
U:E^{\mathrm{or}}\longrightarrow U(1),
\qquad U_{\bar e}=U_e^{-1}=\overline{U_e}.
$$

Its path transport is the ordered product

$$
H_U(p)=U_{e_n}\cdots U_{e_1}.
$$

Because U(1) is abelian, the order convention does not affect the scalar product, but fixing it makes the definition reusable for nonabelian extensions.

### Definition 2.3 - Coherent L2 lift

For each path `p` with L1 weight `w_p`, define

$$
A_p=\sqrt{w_p}\,H_U(p)\in\mathbb{C}.
$$

The coherent sink amplitude and intensity are

$$
A_t=\sum_{p\in P(s,t)}A_p,
\qquad
I_t=|A_t|^2.
$$

This is a finite algebraic L2 lift. No norm completion, continuum, wave equation, or physical interpretation follows merely from writing it.

### Definition 2.4 - Vertex gauge repair

For `g:V -> U(1)`, define

$$
U^g_e=g(t(e))\,U_e\,g(s(e))^{-1}.
$$

Then

$$
H_{U^g}(p)=g(t)H_U(p)g(s)^{-1}
$$

for every path from `s` to `t`.

### Import Ledger 2

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| finite graph and paths | not constructed at a new degree here | carrier declaration | **DECLARED** |
| U(1) group | unavailable at `delta7` | Q1 door | **IMPORTED** |
| complex involution and square root | unavailable at `delta7` | Paper 010 interface | **IMPORTED** |
| coherent sum and modulus square | unavailable at `delta7` | Q2 door | **IMPORTED** |
| physical amplitude semantics | nowhere established | - | **REFUSED in this paper** |

**Connective audit.** An edge word is finite combinatorial incidence; no physical time parameter is used.
**Genesis-Bias audit.** The carrier is an explicit input packet. It is not claimed to precede or generate the exhibited differences.


3. Exact interference as relative holonomy


### Theorem 3.1 - Two-path holonomy-interference identity

Let `p,q:s -> t` be two declared paths with weights `w_p,w_q >= 0`. Put

$$
h_{pq}=H_U(p)\overline{H_U(q)}\in U(1).
$$

Then

$$
\boxed{
|\sqrt{w_p}H_U(p)+\sqrt{w_q}H_U(q)|^2
=w_p+w_q+2\sqrt{w_pw_q}\operatorname{Re}(h_{pq})
}.
$$

**Proof.** Expand against the complex involution:

$$
\begin{aligned}
I(p,q)
&=(\sqrt{w_p}H_p+\sqrt{w_q}H_q)
  (\sqrt{w_p}\overline{H_p}+\sqrt{w_q}\overline{H_q})\\
&=w_p|H_p|^2+w_q|H_q|^2
 +\sqrt{w_pw_q}(H_p\overline{H_q}+H_q\overline{H_p}).
\end{aligned}
$$

Since `H_p,H_q in U(1)`, both moduli are one, and the last parenthesis is `2 Re(h_pq)`. $\square$

The closed word `p bar q` has holonomy `h_pq` under the chosen convention. Thus the cross-term is an exact function of loop holonomy, not merely an analogy.

### Corollary 3.2 - Gauge invariance

The relative holonomy `h_pq` and intensity `I(p,q)` are invariant under every vertex gauge repair.

**Proof.** Both endpoint factors cancel:

$$
H_{U^g}(p)\overline{H_{U^g}(q)}
=g(t)H_p g(s)^{-1}\,
 \overline{g(t)H_q g(s)^{-1}}
=H_p\overline{H_q}.
$$

Equivalently, the full sink amplitude receives one common unit-modulus endpoint factor, so its modulus square is unchanged. $\square$

### Corollary 3.3 - L1 nonfactorization

Assume `w_p w_q>0` and that the relative cycle `p bar q` admits connections realizing both `h_pq=+1` and `h_pq=-1`. No function of the L1 weights alone can reproduce the two-path coherent intensity over that connection family.

**Proof.** Use the two connections supplied by the carrier hypothesis. Their L1 shadows are identical, while

$$
I_+=(\sqrt{w_p}+\sqrt{w_q})^2,
\qquad
I_-=(\sqrt{w_p}-\sqrt{w_q})^2.
$$

The difference is `4 sqrt(w_p w_q)>0`. Hence the readout cannot factor through the L1 projection. $\square$

### Definition 3.4 - Interference residual

For a finite path family, define

$$
\Delta_{\mathrm{int}}
=I_t-\sum_p w_p
=2\sum_{p< q}\sqrt{w_pw_q}\,\operatorname{Re}(H_p\overline{H_q}).
$$

The scalar diagnostic

$$
\mathrm{InterferenceReadoutResidual}=|\Delta_{\mathrm{int}}|
$$

detects net deviation from incoherent L1 addition. It is readout-specific and can vanish by cancellation even when individual relative holonomies are nontrivial. Therefore the complete finite obstruction packet also retains

$$
\mathrm{HolonomySignature}=\{h_{pq}:p,q\in P(s,t)\},
$$

modulo redundant path choices.

### Import Ledger 3

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| algebraic expansion | declared complex scalar package | Section 2 | **IMPORTED, then proved conditionally** |
| relative loop holonomy | declared U(1) connection | Section 2 | **IMPORTED carrier datum** |
| L1 nonfactorization | finite comparison | Corollary 3.3 | proved conditionally |
| physical interference experiment | not supplied | - | **NOT CLAIMED** |

**Connective audit.** “Path” and “loop” are combinatorial words; no chronology is inferred.
**Genesis-Bias audit.** The U(1) fiber is a priced addition over the carrier, not a hidden substrate beneath L1.


4. Cochains, curvature, and the two-dimensional contact


Let `X` now be a finite oriented 2-complex. Use additive phases in `R/2 pi Z`:

$$
C^0(X;\mathbb{R}/2\pi\mathbb{Z})
\xrightarrow{d^0}
C^1(X;\mathbb{R}/2\pi\mathbb{Z})
\xrightarrow{d^1}
C^2(X;\mathbb{R}/2\pi\mathbb{Z}).
$$

An edge connection is `a in C^1`, with `U_e=exp(i a_e)`. A vertex phase `alpha in C^0` repairs it by

$$
a\longmapsto a+d^0\alpha.
$$

For an oriented face `f`, define its curvature

$$
\kappa_f=(d^1a)_f.
$$

### Theorem 4.1 - Face curvature is gauge invariant

Under every vertex repair `a -> a+d^0 alpha`, one has

$$
d^1(a+d^0\alpha)=d^1a.
$$

**Proof.** Linearity gives `d^1a+d^1d^0 alpha`, and the cellular coboundary identity gives `d^1d^0=0`. $\square$

### Corollary 4.2 - Plaquette interference reads curvature

Suppose two paths `p,q:s -> t` form the oriented boundary of one face `f`. Then

$$
h_{pq}=\exp(i\kappa_f),
$$

and Theorem 3.1 becomes

$$
I(p,q)=w_p+w_q+2\sqrt{w_pw_q}\cos(\kappa_f).
$$

This is the precise two-dimensional contact: a 2-cell supplies a local curvature witness for the relative phase between its two boundary routes.

### Proposition 4.3 - Curvature is not all holonomy

The condition `d^1a=0` does not imply that `a` is gauge-trivial on every carrier. Flat connections are classified, subject to the declared finite cellular hypotheses, by their global classes in

$$
H^1(X;\mathbb{R}/2\pi\mathbb{Z})
\cong \operatorname{Hom}(H_1(X),U(1)).
$$

Thus the holonomy verdict is structurally a sum type:

```text
HolonomyVerdict =
    Curved { face_curvature }
  | FlatNontrivial { holonomy_class }
  | GaugeTrivial
```

The `Curved` variant carries the `FaceCurvatureProfile` ($d^1a$). The `FlatNontrivial` variant exists only when $d^1a=0$ and carries the `FlatHolonomyClass` ($[a]_{\mathrm{flat}}$).

The first is local curvature on faces. The second is residual loop holonomy not bounded by a chosen face family. The displayed classification is standard finite cellular cohomology, imported as mathematics here rather than reconstructed from `delta0`.

### Corollary 4.4 - Simply connected flat case

If the finite 2-complex is connected and simply connected, then every flat U(1) connection is gauge-trivial.

This follows from `H_1(X)=0` and Proposition 4.3. It is conditional on the standard cellular classification and the declared topological hypotheses.

### Import Ledger 4

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| finite oriented 2-complex | not earned as physical geometry | this section | **DECLARED carrier** |
| cellular cochains and `d^1d^0=0` | finite mathematical package | standard / Paper 0 analogue | **IMPORTED packaging; identity proved in package** |
| cohomology classification | not derived in series | standard mathematics | **IMPORTED, STANDARD** |
| physical gauge field or spacetime | nowhere supplied | - | **REFUSED as an inference** |

**Connective audit.** Boundary orientation is algebraic incidence, not time order.
**Genesis-Bias audit.** The 2-complex is an input carrier. Calling `kappa` curvature does not identify it with physical geometry.


5. Tree triviality and the dimensional limit of the proposal


### Theorem 5.1 - Every U(1) connection on a finite tree is gauge-trivial

Let `T` be a finite connected tree with connection `U`. There exists `g:V(T)->U(1)` such that `U^g_e=1` on every oriented edge.

**Proof.** Choose a root `r` and set `g(r)=1`. Every other vertex has a unique parent edge `e:u -> v`. Define recursively

$$
g(v)=g(u)U_e^{-1}.
$$

Then

$$
U^g_e=g(v)U_e g(u)^{-1}=1.
$$

The unique-path property makes the definition consistent. $\square$

### Corollary 5.2 - No holonomy explanation on a pure branch tree

A branch tree without recombination has no gauge-invariant U(1) loop holonomy. Edge phases can be removed by a local gauge choice. Holonomy can become observable only after adding at least one cycle, a recombination, or a face-bounded alternative-route structure.

This result constrains both papers in this contact pair. Holonomy can govern interference between alternatives that rejoin. It cannot by itself explain why a tree branches, how many branches are real, or which branch basis is physically preferred.

### Proposition 5.3 - What “more than one dimension” buys

For an ordinary U(1) 1-connection:

* path transport lives on 1-chains;
* gauge-invariant comparison lives on closed 1-cycles;
* local curvature lives on 2-cells;
* dimensions above two can impose further cellular consistency, but they do not change the two-path identity;
* surface or volume holonomy requires an imported higher-form or higher-gauge connection.

Therefore a two-dimensional carrier is the first place local curvature can witness path-relative phase. A higher-dimensional holonomy theory is a separate proposal, not a consequence of the present construction.

### OBSTRUCTION - Higher holonomy

The following cannot be derived from the present carrier: surface-valued superposition phases or `k`-form quantum amplitudes. What would have to be admitted: a higher gauge group, higher connection, parallel transport on `k`-cells, and a compatible readout. What is lost if it is admitted: the claim that ordinary L1 weights plus a U(1) edge connection already explain higher-dimensional holonomy.

### Import Ledger 5

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| tree and unique path | finite graph theory | Theorem 5.1 hypotheses | **DECLARED / STANDARD** |
| branch interpretation | not mathematical consequence | contact with Everett paper | **INTERPRETIVE** |
| higher gauge structure | unavailable | obstruction block | **NOT ADMITTED** |

**Connective audit.** Recursive construction is proof induction over a finite rooted tree, not physical succession.
**Genesis-Bias audit.** Dimension is carrier dimension, not an assertion that physical reality occupies the carrier.


6. Worked finite witnesses


### 6.1 Two alternatives

Take `w_p=u`, `w_q=v`, and `h_pq=e^{i theta}`. Then

$$
I_\theta=u+v+2\sqrt{uv}\cos\theta.
$$

At `theta=0`, the alternatives reinforce. At `theta=pi`, they cancel maximally. For `u=v`, the two values are `4u` and `0`, although the L1 packet is identical.

This is the smallest exact witness that phase-sensitive behavior is not an L1 functional.

### 6.2 Square plaquette

Let a square have vertices `s,x,t,y` and two boundary paths

$$
p=(s\to x\to t),
\qquad
q=(s\to y\to t).
$$

If the oriented edge phases sum to `kappa` around the square, then

$$
h_{pq}=e^{i\kappa},
\qquad
I=u+v+2\sqrt{uv}\cos\kappa.
$$

Vertex phase changes alter individual edge labels but leave `kappa` and the intensity fixed.

### 6.3 Flat cycle without local curvature

Let `X` be a cycle graph with no filled face. Assign edge transports whose product around the cycle is `e^{i theta}`. There is no `C^2` face on which to record nonzero local curvature, yet the global loop holonomy is nontrivial when `theta != 0 mod 2pi`. Filling the cycle with a face does not simply "move" the datum. It is a carrier change that requires transporting the edge connection, performing a new closure test, and computing a changed quotient.

The example is the reason `Gamma_face` and `Gamma_global` must remain separate.

### 6.4 Tree control

Delete one edge from the cycle. The carrier becomes a tree. Theorem 5.1 removes every remaining edge phase by gauge repair, and no gauge-invariant loop witness survives.

### Import Ledger 6

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| trigonometric notation | scalar presentation | examples | **IMPORTED presentation** |
| square/cycle/tree carriers | finite graph declarations | examples | **DECLARED** |
| experimental realization | not supplied | - | **NOT CLAIMED** |

**Connective audit.** “Delete” is a comparison between declared finite carriers, not a physical process.
**Genesis-Bias audit.** The examples are mathematical witnesses, not models asserted to underlie nature.


7. GTOC packet and terminalization


The contact construction can be represented by the following bounded obstruction packet.

| Field | Content |
|---|---|
| carrier | finite graph or finite oriented 2-complex, source, sink, path family |
| `C^0` | vertex phases |
| `C^1` | edge connection phases |
| `C^2` | face curvature values |
| `d^0` | vertex-gauge action on edge phases |
| `d^1` | oriented face boundary sum |
| primitive difference | same L1 weights, different gauge-invariant relative holonomy |
| ZeroRel | same weights plus vertex-gauge-equivalent connection |
| `InterferenceReadoutResidual` | net interference mass `|I-sum w|`, with pairwise residuals retained |
| `HolonomyVerdict` | `Curved` (face curvature) or `FlatNontrivial` (global loop-holonomy class) |
| allowed repair | vertex gauge transformation; carrier-preserving path simplification |
| forbidden repair | changing weights, filling cycles, or importing a phase fiber without recording it |
| evidence ceiling | exact finite algebra in the declared carrier |
| authority effect | `None` |

### Terminal map

| Situation | Honest terminal |
|---|---|
| L1 packet asks for coherent superposition without Q1/Q2 import | `OracleNeeded` |
| declared finite U(1)/L2 packet satisfies the identities | conditional finite result; `AuthorityEffect::None` |
| claimed open residue is erased by changing the carrier or readout | typed refusal |
| higher-form holonomy is requested without a licensed higher connection | `OracleNeeded` |
| physical QM or ontology is inferred from the finite result | typed refusal |

No DDA trace may encode “import U(1)” as an internal repair. Imports are not DDA operations. Within a packet that already declares the U(1) carrier, gauge changes are admissible `E`-type equivalences; changing the topology or readout is a carrier change and must be separately licensed.

### Import Ledger 7

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| packet fields and terminals | GTOC/GTLA protocol | math spine / conductor design | **IMPORTED governance contract** |
| DDA operation labels | DDA contract | Rust contract surface | **IMPORTED governance contract** |
| authority effect | GTLA firewall | standing rule | `None` |

**Connective audit.** Terminalization is a typed workflow judgment, not a claim about physical finality.
**Genesis-Bias audit.** The governance packet describes admitted inputs and transformations explicitly; no hidden oracle is internalized.


8. Claim ledger


| ID | Claim | Status | Dependency / fence |
|---|---|---|---|
| QCS-C1 | Finite L1 weights normalize to proportions when total weight is positive. | `[PROVEN, CONDITIONAL]` | Paper 010 / Paper 2 hypotheses |
| QCS-C2 | The two-path coherent intensity equals the L1 sum plus the real part of relative loop holonomy. | `[PROVEN, CONDITIONAL]` | imported complex/U(1) carrier and coherent readout |
| QCS-C3 | Relative path holonomy and coherent intensity are invariant under vertex gauge repair. | `[PROVEN, CONDITIONAL]` | Definition 2.4 |
| QCS-C4 | Coherent intensity does not factor through L1 weights alone when relative holonomy can vary. | `[PROVEN, CONDITIONAL]` | positive two-path weights, realizable distinct holonomies, and Q1/Q2 carrier |
| QCS-C5 | Every U(1) connection on a finite tree is gauge-trivial. | `[PROVEN, CONDITIONAL]` | finite connected tree |
| QCS-C6 | Face curvature is gauge invariant because `d^1d^0=0`. | `[PROVEN, CONDITIONAL]` | imported finite cellular package |
| QCS-C7 | Flat U(1) connections can retain global holonomy on non-simply-connected carriers. | `[STANDARD]` | finite cellular cohomology classification |
| QCS-C8 | Two dimensions are the first carrier dimension supporting local curvature for an ordinary 1-connection. | `[PROVEN, CONDITIONAL]` | declared cellular grading; not physical dimension |
| QCS-C9 | Higher-form holonomy follows from the present L1/U(1) construction. | `[REFUSED FROM CURRENT PREMISES]` | refused without higher-gauge import |
| QCS-C10 | The construction derives physical superposition or quantum mechanics. | `[SCOPE FENCE]` | explicitly not established; stronger reading blocked |

No row is `[PROVEN]` without a condition because the contact carrier itself is imported. No row has authority effect.

### Import Ledger 8

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| claim statuses | ODP vocabulary | series charter | **IMPORTED governance vocabulary** |
| source-local IDs | this paper | ledger | bookkeeping only |

**Connective audit.** Claim order is editorial.
**Genesis-Bias audit.** Conditional status prevents imported structure from being redescribed as a prior physical foundation.


9. Mechanization and falsification program


### QC-SUP-PL1 - finite U(1) path algebra

Formalize a finite graph connection, path transport, vertex gauge action, the two-path identity, gauge invariance, and L1 nonfactorization. A successful build must expose all scalar assumptions and print the axiom set of the main theorem.

### QC-SUP-PL2 - tree gauge triviality

Formalize the rooted-tree gauge construction and prove that every U(1) edge connection is gauge-equivalent to the unit connection.

### QC-SUP-PL3 - finite 2-complex curvature

Formalize `C^0 -> C^1 -> C^2`, prove `d^1d^0=0`, and bind plaquette relative holonomy to exponentiated face curvature. Keep the global `H^1` classification in a separate theorem so local curvature cannot silently stand for all holonomy.

### QC-SUP-PL4 - executable witness

Add a Rust finite certificate carrying graph incidence, rational/algebraic weights, finite phase labels, connection data, path products, and recomputed intensities. The verifier must reject:

* inconsistent reverse-edge transport;
* path endpoint mismatch;
* claimed gauge equivalence with unequal loop holonomy;
* a terminalized open residue;
* an unrecorded phase or higher-gauge import.

### Falsifiers

This paper is refuted or narrowed if any of the following is exhibited:

1. two paths satisfying the declared hypotheses for which Theorem 3.1 fails;
2. a vertex gauge repair that changes a relative loop holonomy or intensity;
3. a finite tree connection that cannot be gauged to the unit connection;
4. a finite 2-complex for which the stated coboundary package has `d^1d^0 != 0`;
5. an L1-only functional that reproduces all phase-sensitive coherent intensities without encoding equivalent phase data.

### Import Ledger 9

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| Lean and Rust verification | software workflow | future targets | **NOT YET EXECUTED** |
| finite phase certificate | future implementation | QC-SUP-PL4 | **OPEN** |
| axiom audit | proof hygiene | future Lean target | **OPEN** |

**Connective audit.** “Future” is project scheduling language, not a derived time claim.
**Genesis-Bias audit.** Mechanization is evidence about formal statements, not an external truth oracle or authority mint.


10. Conclusion


L1 weights provide a phase-blind shadow. A coherent finite L2 lift adds square-root amplitudes and a quadratic readout. A U(1) connection makes the added phase relational: alternatives accumulate transport, and their cross-term reads the holonomy of the loop formed by one path against the reverse of another.

That statement is exact and useful, but its scope is narrow. It explains how holonomy controls interference after the Q1/Q2 doors are opened. It does not explain why those doors must open, why nature realizes the carrier, why a complex Hilbert description is unique, or what ontology should be attached to its alternatives.

The dimensional result is equally sharp. A tree has no gauge-invariant loop phase. A cycle can retain global flat holonomy. A 2-cell can localize the same obstruction as curvature. Higher holonomy requires higher structure. The next paper applies these constraints to relative-state branching and shows where Everettian formalism is illuminated by the L1/L2 split and where holonomy cannot carry the interpretive load.

### Import Ledger 10

| Term used | Degree first available | Where derived | Or: imported flag |
|---|---|---|---|
| explanatory conclusion | synthesis | Sections 1-9 | conditional only |
| physical realization | not established | - | **OPEN** |
| ontology and authority | not established | - | **REFUSED as inference** |

**Connective audit.** “Next paper” is document order only.
**Genesis-Bias audit.** The conclusion retains the carrier/import boundary and makes no substrate claim.

### 9.5 Mathematical Generalization: Matrix-Valued SU(2) Tensor Lifts (`Stage 1.5`)

Beyond scalar $U(1)$ phase transport on 1-cycles, corpus-wide mining over bipartite carriers (Paper 7 / Paper 8) suggests extending loop holonomies to non-Abelian $SU(2)$ matrix connections on tensor product carriers $C^1 \otimes C^1$. For a bipartite path pair $(p_1 \otimes p_2, q_1 \otimes q_2)$, the matrix-valued relative holonomy $H_{\text{rel}} = (H_{p_1} \otimes H_{p_2})(\overline{H_{q_1}} \otimes \overline{H_{q_2}})$ governs non-factorizable bipartite interference. We state this extension as a formal obligation `PL-QM063-11` (`QCS-C11`, `[CONJECTURE]`): matrix-valued holonomy trace $\operatorname{Tr}(H_{\text{rel}})$ lower-bounds separability defects on tensor carriers.


References

1. [`qm_072_bit_shadow_and_qubit.md`](qm_072_bit_shadow_and_qubit.md) (The Bit-Shadow and the Qubit).
2. [`qm_073_correlation_separability_finite_bell.md`](qm_073_correlation_separability_finite_bell.md) (Correlation, Separability, and Finite Bell Bounds).
3. [`qm_020_born_normalization_and_conditional_hilbert_lift.md`](qm_020_born_normalization_and_conditional_hilbert_lift.md) (Born Normalization and Conditional Hilbert Lift).
4. [`qm_061_interference_as_the_non_l1_resource.md`](qm_061_interference_as_the_non_l1_resource.md) (Interference as the Non-L1 Resource).
5. M. V. Berry, [“Quantal phase factors accompanying adiabatic changes”](https://doi.org/10.1098/rspa.1984.0023), *Proceedings of the Royal Society A* 392 (1984), 45-57.
6. B. Simon, [“Holonomy, the quantum adiabatic theorem, and Berry's phase”](https://doi.org/10.1103/PhysRevLett.51.2167), *Physical Review Letters* 51 (1983), 2167-2170.

References 5-6 are positioning sources, not proof premises. Their bibliographic metadata was verified against the DOI records on 2026-07-17.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QCS-C1` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C1`) |
| `QCS-C2` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C2`) |
| `QCS-C3` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C3`) |
| `QCS-C4` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C4`) |
| `QCS-C5` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C5`) |
| `QCS-C6` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C6`) |
| `QCS-C7` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C7`) |
| `QCS-C8` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C8`) |
| `QCS-C9` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C9`) |
| `QCS-C10` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C10`) |
| `QCS-C11` | [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (ID `063:QCS-C11`) |

<!-- claim-id-body-index:end -->
