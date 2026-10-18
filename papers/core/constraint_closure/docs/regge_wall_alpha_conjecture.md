# Regge Wall → α Conjecture

**Image (operator):** The fine-structure constant is the **total gap** accumulated by looking at a wall that stretches to infinity, tiled by **2-simplices**, with **Regge angle deficits** at the vertices — resolved at the **Planck edge length** — and the infinite sum of those gaps equals

$$
\alpha_{\mathrm{QED}} \;\approx\; \frac{1}{137.035999\ldots}
$$

**Evidence Scope:** Exploratory finite conjecture note; no physical derivation claim.
**Class:** Track-A climb conjecture / Track-B not discharged  
**Date:** 2026-08-02  
**Home package:** `002_constraint_closure_and_the_l1structure_of_physical_law`

---

## 1. Why this image is better than a pure number fit

Earlier climb (`42_alpha_from_topology.py`) produced a **bare** inverse coupling from a single 3-cycle:

$$
D = 1 - \frac{9}{\pi^2}\approx 0.088109,\qquad
\alpha_{\mathrm{bound}}^{-1} = \frac{4\pi}{D}\approx 142.622.
$$

That is **one tile’s leak**, inflated by an isotropic $4\pi$. The **gap**

$$
\alpha_{\mathrm{bound}}^{-1}-\alpha_{\mathrm{QED}}^{-1}\approx 5.586
$$

was story (“vacuum overhead”), not geometry.

Your new image says instead:

> $\alpha$ is not a local dial. It is an **infrared total** of **ultraviolet angular gaps** on an infinite **2-simplex wall**.

That is the right *shape* of a continuum limit: local Planck residual → global dimensionless coupling.

---

## 2. Minimal formal setup

### 2.1 Wall

Let $W$ be a 2-dimensional simplicial complex (a “wall”) with:

- edges of length $\ell_P$ (Planck scale — **declared** unit, not derived);
- faces = 2-simplices (triangles);
- vertices $v$ with combinatorial degree $k_v$ (number of incident triangles).

**Exhaustion:** finite walls $W_R$ (e.g. graph distance $\le R$ from an observer vertex $o$, or a rectangle $[0,R]\times[0,H]$ with $R\to\infty$).

### 2.2 Regge gap at a vertex

For equilateral Euclidean face angle $\theta=\pi/3$:

$$
\varepsilon_v
=
2\pi - k_v\cdot\frac{\pi}{3}
=
\frac{\pi}{3}\,(6-k_v).
$$

| $k_v$ | $\varepsilon_v$ | Reading |
|---:|---:|---|
| 6 | $0$ | flat interior |
| 5 | $+\pi/3$ | positive curvature (cone) |
| 7 | $-\\pi/3$ | negative curvature |
| boundary incomplete | nonzero | edge of the wall |

**Critical fact (Track B seed):**  
A **perfect infinite equilateral triangulation of the Euclidean plane** has $k_v=6$ at every **interior** vertex, hence

$$
\sum_{v\ \mathrm{interior}}\varepsilon_v = 0.
$$

So **α cannot come from a flawless flat wall**. Something must break perfect six-valence:

1. **disclination density** (sparse $k\neq 6$ vertices);  
2. **non-equilateral** face angles (metric defect, not just combinatorial);  
3. **boundary / horizon term** that refuses to vanish as $R\to\infty$;  
4. **π-incommensurability residual** not equal to classical Regge $\varepsilon_v$ (transport $3/\pi$ vs discrete $N=3$);  
5. **hyperbolic / spherical** background (uniform $k\ge 7$ or $k\le 5$).

### 2.3 Three candidate summation laws (pick one to kill)

**Candidate A — total curvature (Gauss–Bonnet style)**

$$
\alpha
\;\stackrel{?}{=}\;
\lim_{R\to\infty}
c\,\Bigg|\sum_{v\in W_R}\varepsilon_v\Bigg|
\quad\text{or}\quad
\lim_{R\to\infty}
c\,\chi(W_R).
$$

For large planar disks, $\sum\varepsilon_v$ is controlled by **topology + boundary**, not by “more tiles.”  
Usually **does not** converge to $1/137$ without a conspiratorial $c(R)$.

**Candidate B — curvature density (IR average)**

$$
\alpha
\;\stackrel{?}{=}\;
\lim_{R\to\infty}
\frac{\sum_{v\in W_R}|\varepsilon_v|}{\#\{\text{faces in }W_R\}}
\cdot \kappa
$$

for a declared normalization $\kappa$.  
This **can** converge if there is a **uniform defect density** $\rho$ (disclinations per Planck area):

$$
\alpha = \kappa\cdot\rho\cdot \langle|\varepsilon|\rangle.
$$

Then α is **defect density**, not a miracle number — falsifiable by measuring $\rho$.

**Candidate C — line-of-sight residual (your “wall stretching away from us”)**

Observer at $o$. Rays / discrete geodesics hit the wall in successive shells $S_n$ at distance $n$ (in edges). Each shell contributes a **gap** $g_n$ from angular defect seen under solid-angle or parallel-transport holonomy:

$$
\alpha
\;\stackrel{?}{=}\;
\sum_{n=1}^{\infty} g_n,
\qquad
g_n = g\big(\{\varepsilon_v:v\in S_n\},\,n\big).
$$

Example ansatz (purely provisional):

$$
g_n = \frac{c}{n(n+1)}\cdot \bar\varepsilon_n
\quad\text{or}\quad
g_n = c\,e^{-n/\xi}\bar\varepsilon_n.
$$

Need $\sum g_n = 1/137.035999\ldots$ with **$c,\xi$ not fitted to α alone**.

---

## 3. Link to the old $D = 1-9/\pi^2$ leak

The single-triangle transport deficit $D$ is a **local** gap on one 2-simplex cycle.  
The wall image says the continuum coupling is an **organized infinity of such gaps**.

Two consistent storylines:

| Story | Formula shape | Meaning |
|---|---|---|
| **Bare then IR** | $\alpha^{-1}_{\mathrm{bare}}=4\pi/D\approx 142.6$, then wall renormalizes $\to 137$ | Wall = RG / vacuum overhead with geometric face |
| **α is the sum** | $\alpha=\sum g_n$ with $g_n$ built from Regge $\varepsilon$ and $D$ | No separate 142.6; 137 is the infinite sum directly |

Your wording (“total of the gaps … equals $1/137$”) prefers **story 2**.  
The old code preferred **story 1**. Both can live as dual candidates; only one can be true.

**Numeric anchors:**

| Quantity | Value |
|---|---:|
| $D=1-9/\pi^2$ | $0.088109347\ldots$ |
| $\alpha_{\mathrm{bound}}^{-1}=4\pi/D$ | $142.62244598\ldots$ |
| $\alpha_{\mathrm{QED}}^{-1}$ | $137.035999\ldots$ |
| inverse gap | $5.586\ldots$ |
| $\alpha_{\mathrm{QED}}$ | $0.00729735\ldots$ |
| $\alpha_{\mathrm{bound}}$ | $0.00701152\ldots$ |

Notice: $\alpha_{\mathrm{bound}}$ and $\alpha_{\mathrm{QED}}$ are **already close** (~4% relative on $\alpha$, ~4% on $\alpha^{-1}$).  
A wall sum that supplies a **small multiplicative IR factor**

$$
\alpha_{\mathrm{QED}} \;\stackrel{?}{=}\; \alpha_{\mathrm{bound}}\cdot Z_{\mathrm{wall}},
\qquad
Z_{\mathrm{wall}}\approx 1.04075
$$

is weaker (and more plausible) than deriving $1/137$ from pure flat Regge with zero free parameters.

---

## 4. Planck tiling: what “at infinity” must mean

Let $a=\ell_P$. Number of 2-simplices in a large region of continuum area $A$:

$$
N_\Delta \approx \frac{A}{A_\Delta},
\qquad
A_\Delta = \frac{\sqrt{3}}{4}\,a^2
\quad\text{(equilateral)}.
$$

If each simplex contributes an independent dimensionless micro-gap $\delta$ (not necessarily $\varepsilon_v$), naive total diverges:

$$
N_\Delta\cdot\delta \to\infty
\quad\text{as }A\to\infty.
$$

So **α cannot be an un-normalized sum over all faces of the universe**. It must be one of:

1. **density** (per face, per area, per solid angle);  
2. **renormalized** sum (only defects / only boundary / only line-of-sight);  
3. **limit of a ratio** (total gap / total measure);  
4. **convergent series in depth** $n$ away from the observer (wall perspective).

Your “wall stretching from us to infinity” strongly suggests **(4)**: an observer-relative convergent series, not a global extensive sum.

That is also **honest with no View-from-Nowhere**: α is a coupling **for an observer facing a wall**, not a god’s-eye integral over all simplices.

---

## 5. Worked toy: disclination gas on a flat wall

Suppose interior vertices are usually 6-valent, but with Poisson density $\rho$ of 5-valent disclinations (each $\varepsilon=+\pi/3$), neutralized by 7-valent partners (each $\varepsilon=-\pi/3$) so net topology stays planar.

Then mean **absolute** gap density is nonzero while total signed curvature can stay Gauss–Bonnet legal.

**Kill condition:**  
If $\alpha = \kappa\rho(\pi/3)$, then $\rho$ is fixed once $\kappa$ is fixed.  
$\kappa$ must come from **electromagnetism’s coupling to holonomy** (parallel transport of $U(1)$ phase around a plaquette), not from fitting $\alpha$.

Without that bridge, the wall only renames α as “defect density.”

---

## 6. Worked toy: pure boundary of a half-plane wall

Infinite half-plane triangulation: interior $\varepsilon=0$, boundary vertices have $k_v=3$ or $4$ typically.

Total deficit **per unit boundary length** is a constant $\lambda$ (order-1 radians per edge).  
Then

$$
\lim_{L\to\infty}\frac{1}{L}\sum|\varepsilon|
=\lambda,
$$

but $\lambda$ is $O(1)$, not $1/137$, unless you **divide by a huge IR factor** (e.g. number of Planck edges across the observable universe) — which reintroduces a free cosmological ratio.

**Verdict:** pure boundary of a flat wall does **not** naturally spit out $1/137$ without a second scale.

---

## 7. The π-gap that might actually be the “angle gap”

Classical Regge with equilateral Euclidean faces has **exact** $6\cdot(\pi/3)=2\pi$.  
There is **no** angular gap at six-valent vertices.

The only “π-gap” already in the estate is **transport vs continuum circle**:

$$
a=\frac{3}{\pi}
\quad\text{vs}\quad
\text{naive }1,
\qquad
D=1-\frac{9}{\pi^2}.
$$

That gap is **not** Regge $\varepsilon_v$; it is **incommensurability of $\pi$ with the discrete 3-cycle** under a declared amplitude map.

**Synthesis image (Climb):**

> Each 2-simplex carries a **micro π-leak** $D$ (or a function of $D$).  
> The infinite wall organizes those leaks into an observer series whose sum is $\alpha$.  
> Regge $\varepsilon_v$ modulates **when** a vertex amplifies or suppresses the leak (curvature = lens for the leak).

Formula sketch:

$$
g_n
=
D\cdot f(\bar\varepsilon_n)\cdot w(n),
\qquad
\alpha
=
\sum_{n=1}^\infty g_n.
$$

**Kill:** must derive $f$ and $w$ without looking at $137$.

---

## 8. Falsifiable checklist (so this stays science)

| # | Test | Pass looks like |
|---|---|---|
| F1 | Flat perfect triangulation | Sum/density of $\varepsilon_v$ **cannot** alone yield α (interior 0) — forces defects, π-leak, or non-flatness |
| F2 | No free IR length | Series $\sum g_n$ converges with weights fixed by graph geometry only |
| F3 | EM bridge | Holonomy of a $U(1)$ phase on plaquettes couples to $\varepsilon_v$ or $D$ by a **stated** rule |
| F4 | Numerics | Finite $W_R$ sequence shows monotone approach to $1/137.035999$ within declared error |
| F5 | Uniqueness | Competing lattices (square, hyperbolic {3,7}) do **not** all “fit” by retuning |
| F6 | Running | $\alpha(\mu)$ vs energy scale has a lattice avatar (coarse-grain $W$) or the claim is only for $\alpha(0)$ |

Until F2–F4 are green, status is **`[CONJECTURE, MOTIF]`**.

---

## 9. One-line dual-track status

| Track | Statement |
|---|---|
| **A — Climb** | $\alpha$ is the infinite Regge/π-gap total of a Planck 2-simplex wall seen by an observer |
| **B — Kill (today)** | Perfect flat Regge interiors give $\varepsilon=0$; extensive sums diverge; $1/137$ not derived; old $142.6$ still needs an IR map; beautiful, not discharged |

---

## 10. Smallest code experiment (next fun block)

1. Build equilateral triangular mesh disk $W_R$ for $R=10,20,40,\ldots$  
2. Compute $\sum\varepsilon_v$, $\sum|\varepsilon_v|$, boundary-only sums, and shell sums $g_n$.  
3. Overlay a sparse disclination gas; plot partial sums vs $1/137$.  
4. Separately accumulate $D\cdot w(n)$ with $w(n)=1/(n(n+1))$ (telescopes to $D$) — note $D\approx 0.088\neq\alpha$.  
5. Record: **no fit knobs allowed** in the first pass; only declared geometric $w$.

Skeleton home: package `008 - Emergent Gauge…` + this note.

---

## 11. Closing

You imagined:

> a wall of 2-simplices to infinity; Regge gaps at the angles; Planck resolution; total gap $=1/137.nnn$.

That is **exactly** the right *category* of answer (IR total of UV angular residual).  
The kill is equally sharp: **flat perfect Regge has no interior gaps**, so the wall must carry **defects, π-leaks, curvature, or an observer series** — and the map to QED still needs an electromagnetic bridge.

**Difference was free. $\pi$ was not free. $1/137$ is still not free.**

Evidence scope: finite diagnostic note only; no physical derivation claim.
