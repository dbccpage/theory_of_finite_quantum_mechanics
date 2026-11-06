# Appendices — Discrete Deformation Calculus v1.0.3 {#appendices}

**Part of:** [Discrete Deformation Calculus v1.0.3](../discrete_deformation_calculus.md)

The appendices hold candidate adapters, observer notes and worked
trajectories. Nothing here is part of the core calculus unless its ledger row
says so.

## A. Candidate adapter: ZX diagrams to cochains

> **Fence.** A candidate adapter from planar ZX diagrams to finite cochains. It
> is not core DDC and asserts no quantum or physical result (DDC-OPEN-03).

A finite ZX diagram gives a graph carrier: spiders with a type $Z$ or $X$ and a
phase $\theta_v$ are vertices, oriented wires with a phase discrepancy
$\omega_e$ are edges, and closed plaquettes are faces. The candidate
coboundary is colour-relative:

$$(d_0 \theta)_{u \to v} = \theta_v - \theta_u - H_{u,v}, \qquad
H_{u,v} = \begin{cases} 0 & \text{same type,} \\ \pi/2 & \text{different type,} \end{cases}$$

with $d_1$ summing signed discrepancies around each plaquette. Two obligations
are open. First, $d_0$ with a non-zero $H$ is affine, not linear, so
$d_1 \circ d_0 = 0$ must be proved or refused for the declared $H$. Second,
phases are real, so an exact treatment needs a finite shadow over $\mathbb{Q}$
or a declared oracle. Spider fusion $Z(\alpha) \circ Z(\beta) \Rightarrow
Z(\alpha + \beta)$ would read as E when a local $\theta$ with
$\theta_v - \theta_u = \omega_e$ exists, giving the candidate tape
`C·R·E·I·T`.

## B. Observer gauges and dual witnesses

> **Fence.** An observer-gauge note. It is not core DDC, and it leaves
> $\mathbb{Q}$ where it takes a square root (DDC-OPEN-04).

For a two-component defect $\omega = (1, 1)$ on one edge of a hollow six-cycle,
a coordinate-separable observer reads $\lVert (1,1) \rVert_1 = 2$, and a
rotation-invariant observer reads $\lVert (1,1) \rVert_2 = \sqrt{2}$. The ratio
$\sqrt{2}$ is specific to this defect and these gauges; for (1,0) the
ratio is 1. A feasible dual flow must have zero divergence. For the separable
gauge, the vector (1,1) circulates on every consistently oriented cycle edge;
only its pairing with the one-edge defect is concentrated on that edge. The
rotation-invariant gauge similarly uses the constant unit flow
$(1,1)/\sqrt{2}$ on every edge. A one-edge dual vector would violate flow
conservation. Formalizing the finite dual
certificate, with its Fenchel–Rockafellar hypotheses named, is open.

## C. Worked trajectories

**C.1 Trajectory recording** (OE010-06). A trajectory maps concrete tool and
human actions into cochain classes, and cochains back into readable evidence,
with $d_{k} \circ d_{k-1} = 0$ on the window. This is a positioning statement.
The recorder cited by the first draft is not part of this deposit, and no
claim here depends on it.

**C.2 Projection-context congruence** (OE010-07). Following the coalgebraic
partition refinement of Birkmann et al. (arXiv:2204.06248), signatures
$\mathrm{sig}_\pi = F\pi \circ c$ split states until a representation $p$ and
every context continuation agree. When $p(x) = p(y)$ but some context $c$
separates them, the pair and its separating word witness a *returning
projection*. This is positioning. A related implementation exists elsewhere in
the repository, outside this deposit, and is not relied on here.

**C.3 Newton–Leibniz as a tape** (OE010-08). Integrate $f(x) = x$ on
$[0, 10]$ with ten left-endpoint steps, exactly over $\mathbb{Q}$. The carrier
is a path with vertices $0, \dots, 10$. The measured increments are $k$ (left
sum $45$). The exact increments are $d_0 F$ for $F(k) = k^2/2$, namely
$k + \tfrac{1}{2}$. The defect is $\tfrac{1}{2}$ on every edge, total $5$. A
path has no cycles, so every defect on it is exact. The tape `C·R·E·I·T`
declares the grid, registers the defect, repairs it to $d_0 F$, commits and
seals. The integral is the telescoping sum $F(10) - F(0) = 50$: on a path, the
discrete fundamental theorem of calculus says that summing a coboundary
returns the difference of the potential at the endpoints. `demos.newton_leibniz`
computes these numbers and the tape's receipt head;
`test_fsm_and_demos.py::test_newton_leibniz_is_exact` pins both. No hash is
copied into this text.

## D. Spectral sequences, skills and operads

> **Fence.** These are programme definitions, not theorems. No code in this
> deposit implements them, and the first draft's references to such code were
> dead.

- **Self-maintenance mode** (OE010-11). A tape that re-examines its own
  detector through `C·R·Λ·I·T` would relate to the $E_\infty$ page of a
  filtration spectral sequence. Open.
- **Skill objects** (OE010-12). A *skill* is proposed to be a residual class
  that survives every licensed attachment in a growth filtration, bound to a
  receipt. Definition proposal; open.
- **Meta-skills** (OE010-13). A meta-skill is proposed to be a class that
  persists across a family of carriers. Open.
- **Spectral sequence on a minimal complex** (OE010-14). Attaching a 2-cell
  $\sigma$ with nonzero pairing $\omega(\partial\sigma) \ne 0$ changes the
  question: $\omega$ is no longer closed, so the class leaves $H^1$ as an open
  face defect ($\Gamma_2 > 0$), and it is not repaired. Demo 3's falsifier
  shows this directly, and Theorem 5.5 shows that no lift makes a survivor
  exact under its commuting-restriction hypotheses. Support containment alone
  is insufficient: two triangle circulations +1 and −1 cancel on a face
  traversing both cycles (`test_review_regressions.py::test_attaching_a_face_must_pair_nontrivially_with_the_residual`). A correct page-by-page account over a declared filtration is open.
- **Coloured operads of skills** (OE010-15). Composition
  $\gamma \in \mathcal{T}(c_1, \dots, c_n; d)$ with loss-ledger accumulation
  $L_{\gamma \circ (\delta_i)} = L_\gamma \cup \bigcup_i \gamma^{(i)}_*(L_{\delta_i})$
  is a design sketch. The associativity and unit laws of such an operad are
  open, and composition mints no authority.
