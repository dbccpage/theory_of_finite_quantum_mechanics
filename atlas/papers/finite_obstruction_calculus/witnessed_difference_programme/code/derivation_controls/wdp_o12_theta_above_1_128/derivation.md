# WDP-O12-THETA-ABOVE-1-128

Goal id: WDP-O12-THETA-ABOVE-1-128

Selected scope for WDP-O12-THETA-ABOVE-1-128 is recorded in this note.

The plan row is open. Its `depends_on` list is empty and it names no fence. Its statement is that nothing is proved for \(\theta>1/128\) about the row-sum covariance limit. The monograph, after display (O-15), lists as not proved “anything for \(\theta>1/128\)”, and the row note says no target is given beyond that word. The thermodynamic-limit note supplies no statement for \(\theta>1/128\); its dated note of 2026-10-07 keeps that nonclaim for the ring lemmas TL-4 and TL-5. This note does not fill the absence. It records the printed domain of the TL-5 majorant and the rational obstruction at and above the cut. No Python, Rust, or Lean kernel was run. The arithmetic below compares printed rationals. It is not a value of \(k_{L,\theta}\).

## Selected scope

Even periodic CAR rings \(L\ge 4\), full \(2^L\) space, and only the written TL-5 majorant. The finite object is the printed rate domain

\[
\varepsilon_L(\theta)=\sup_u\lvert k_{L,\theta}(u)-k_\theta(u)\rvert
\le 4 M_1 L(128\theta)^L,
\qquad M_1=\frac{24576}{43},
\]

for \(0\le\theta<1/128\), together with the closed-disk bound \(\lvert D_y\rvert\le 4 M_1\) on \(\lvert\theta\rvert\le 1/128\). The in-scope contrast is display (O-15) and TL-5. Uniformity of that rate is only the smaller interval \(0\le\theta\le 1/192\).

Excluded from this note as a theorem for \(\theta>1/128\): any extension of the lift, a larger Schwarz radius, real-time spectral density, the \(X_{LM}\) comparison, a Lean proof of the analytic estimates, and reuse of the \(\theta\le 1/192\), \(\theta_*\), \(\theta=0\), open-chain, or polymer-label bounds as identification of \(\lim_L k_{L,\theta}\).

This is not \(\lim_L k_{L,\theta}\) for any \(\theta>1/128\).

## Hypotheses

H1. \(L\) is even and at least 4. The carrier is the full \(2^L\)-dimensional periodic CAR ring of TL-0, with the physical Jordan–Wigner sign on the wrapping bond. The row sum is \(k_{L,\theta}(u)=\sum_y C^L_{0y}(u)\). The line row sum, where it is written, is \(k_\theta=\sum_n C^\infty_{0n}\). Nothing below passes that identification through \(\theta=1/128\).

H2. The five premises of TL-1 are used only as named: (i) each bond term is four times a projector; (ii) the normalized trace factorizes on words supported on pairwise disjoint label components; (iii) bond terms and sources commute with local operators off their supports; (iv) the staggered source has vanishing mean; (v) on the physical ring, bond terms and sources are even. The Kotecký–Preiss bound imported on \(\lvert\theta\rvert\le 1/96\) is not reproved. It is the source of \(S_1=3/43\) and \(M_1=2 S_1\cdot 64^2=24576/43\).

H3. The wrapped difference \(D_y=C^L_{0y}-\sum_{n\equiv y\ (L)}C^\infty_{0n}\) vanishes in \(\theta\) below order \(L\). On \(\lvert\theta\rvert\le 1/128\) the thermodynamic-limit note records convergence of the image sum with ratio \(3/4\) and \(\lvert D_y\rvert\le M_1(1+512/175)<4 M_1\).

H4. Schwarz on that disk is the written step. It gives \(\lvert D_y\rvert\le 4 M_1(128\lvert\theta\rvert)^L\), and then \(\varepsilon_L(\theta)\le 4 M_1 L(128\theta)^L\), only for \(0\le\theta<1/128\). The same display’s embedding line is a different norm and stops at \(0\le\theta\le 1/192\).

H5. `constants.lift_error_bound` raises unless \(\lvert\theta\rvert<1/128\). The source of `test_rate_and_embedding_bounds` expects that raise at \(\theta=1/128\). The function was not executed for this note.

H6. No radius \(R\) with \(\theta<R<1/96\) is written as a Schwarz disk for \(D_y\). No exact rational value of \(k_{L,\theta}\), and no exact rational gap \(\lvert k_{L,\theta}-k_\theta\rvert\), is given on a finite CAR carrier for any \(\theta>1/128\).

H7. EP-10, EP-12, TL-3, the weighted tail, TL-12, the label norm \(1/128\), and `embedding_bound` are different sentences. They are recorded so they are not reused as TL-5 above the cut. They are not hypotheses that extend the lift.

## Derivation

### 1. What the printed rate says

O.12 defines \(k_{L,\theta}(u)=\sum_y C^L_{0y}(u)\) on even \(L\ge 4\). The ring kernel minus its wrapped line images vanishes below order \(L\). Schwarz on \(\lvert\theta\rvert\le 1/128\) is stated for \(0\le\theta<1/128\):

\[
\sup_u\lvert k_{L,\theta}(u)-k_\theta(u)\rvert\le 4 M_1 L(128\theta)^L\to 0.
\]

That is display (O-15), first line, and display (TL-5). The second line of (O-15) bounds \(\lVert E_L-C^\infty\rVert_{\ell^1_\mu}\) for \(0\le\theta\le 1/192\), \(\mu\ge 0\), and \(q=96\lvert\theta\rvert e^\mu<1\). The monograph then says the rate is uniform on \(0\le\theta\le 1/192\). The thermodynamic-limit note makes the comparison that justifies that smaller interval: \(128\theta\le 2/3\) there.

The cut \(1/192\) does not cross \(1/128\). In lowest terms,

\[
\frac{128}{192}=\frac{2}{3}<1,
\qquad
\frac{1}{128}-\frac{1}{192}=\frac{1}{384}>0.
\]

So \(0\le\theta\le 1/192\) lies inside \(0\le\theta<1/128\). It is not a statement for \(\theta>1/128\). The scope sentence of the same note says TL-2 through TL-7 hold on \(0\le\theta\le 1/192\), with TL-5 kept on \(0\le\theta<1/128\).

### 2. Closed-disk arithmetic feeding Schwarz

Two uses of the rational \(1/128\) are distinct.

The polymer label norm is the bound on the gas, not the TL-5 temperature cut. On \(\lvert\theta\rvert\le 1/96\) and \(\lvert z\rvert,\lvert w\rvert\le 1/64\), every label norm is at most \(1/128\), because a bond has norm at most \((3/4)\lvert\theta\rvert\) and a source has norm \(\lvert z\rvert/2\) or \(\lvert w\rvert/2\). The code asserts

\[
\frac{3}{4}\cdot\frac{1}{96}=\frac{1}{128},
\qquad
\frac{1}{64}\cdot\frac{1}{2}=\frac{1}{128}.
\]

That gas produces \(S_1=3/43\) and \(M_1=24576/43\) on the larger disk \(\lvert\theta\rvert\le 1/96\). It does not identify periodic and line row sums.

The image ratio used for \(D_y\) is the decay base of TL-3 at the Schwarz edge. At \(\lvert\theta\rvert=1/128\),

\[
96\cdot\frac{1}{128}=\frac{96}{128}=\frac{3}{4}.
\]

The thermodynamic-limit note says that on \(\lvert\theta\rvert\le 1/128\) the sum over images converges with this ratio \(3/4\), and \(\lvert D_y\rvert\le M_1(1+512/175)<4 M_1\). The code comment and asserts record the same wrap comparison: the sum of \((3/4)^{\lvert n\rvert}\) over \(n\equiv y\pmod L\) is bounded by

\[
\frac{2}{1-(3/4)^4}=\frac{512}{175},
\]

and \(1+512/175<4\). The sum of those rationals is

\[
1+\frac{512}{175}=\frac{687}{175},
\qquad
4-\frac{687}{175}=\frac{13}{175}>0.
\]

Hence \(687/175<4\), and the note’s strict comparison with \(4 M_1\) is the printed one. Schwarz of order \(L\) then multiplies that constant by \((128\lvert\theta\rvert)^L\). Summing the \(L\) sites produces the factor \(L\). These fractions \(512/175\), \(687/175\), and \(13/175\) are threshold arithmetic for that majorant. They are not a row sum.

### 3. The endpoint \(\theta=1/128\)

At \(\theta=1/128\) one has \(128\theta=1\), so every power \((128\theta)^L\) equals \(1\). The formal majorant collapses to

\[
4 M_1 L=\frac{98304}{43}\,L.
\]

The prefactor is \(4\cdot 24576/43=98304/43\). For the smallest even ring in TL-0,

\[
4 M_1\cdot 4=\frac{393216}{43}.
\]

The factor \(L\) sends \(98304\,L/43\) to infinity through even \(L\ge 4\). A majorant that increases with \(L\) does not prove \(\varepsilon_L(\theta)\to 0\).

The code does not return this formal value. `lift_error_bound` is defined only for \(\lvert\theta\rvert<1/128\) and raises otherwise. Its docstring states the formula \(4 M_1 L(128\lvert\theta\rvert)^L\) under that strict inequality. The test source calls `lift_error_bound(10, Fraction(1, 128))` inside `pytest.raises(ValueError)`. Refusal at the endpoint is the domain statement. It is not an evaluation of \(\lvert k_{L,1/128}-k_{1/128}\rvert\), and it is not a proof that the limit fails.

### 4. Every temperature strictly above \(1/128\)

Fix a real \(\theta>1/128\). That point lies outside the disk on which Schwarz was applied, so the hypothesis of the written estimate is false. The same formal expression is not an upper bound on \(\lvert k_{L,\theta}-k_\theta\rvert\).

The rational witness named in the sources is \(\theta=1/96\). It lies above the cut:

\[
\frac{1}{96}-\frac{1}{128}=\frac{1}{384}>0,
\qquad
128\cdot\frac{1}{96}=\frac{128}{96}=\frac{4}{3}>1.
\]

Thus \((128\theta)^L=(4/3)^L\) grows with \(L\). Growth of an expression whose prefactor \(4 M_1\) was taken on the disk of radius \(1/128\) is not a bound, and it is not a counterexample. A majorant that does not apply does not prove that \(\lim_L k_{L,\theta}\) fails to exist, fails to be unique, or fails to equal the line row sum.

No file replaces the disk. TL-2 bounds \(\lvert C\rvert\) by \(M_1\) on the larger polydisk \(\lvert\theta\rvert\le 1/96\), but the image-sum comparison that produces \(512/175\) and the constant \(4 M_1\) is written at ratio \(3/4\), that is, at radius \(1/128\). A Schwarz radius \(R\) with \(\theta<R<1/96\) is not written. This note does not choose one.

No sentence assigns an exact rational \(k_{L,\theta}\) or an exact limit gap on a finite CAR carrier for any \(\theta>1/128\). The checks named in O.12 — series on \(L=4,6,8\), the lift through the computed order, the \(B_0\) certificate, and the rational window floors — stay inside the proved window. The word “anything” does not name a quantity. There is no missing calculation inside the selected scope.

### 5. Sentences that meet some \(\theta>1/128\) and are not this limit

TL-3 writes the open-chain limit \(C^\infty\) for \(\lvert\theta\rvert<1/96\). The weighted tail is finite when \(q=96\lvert\theta\rvert e^\mu<1\). That is summability of the line kernel. It is not the identification of the periodic row sum with \(k_\theta\) on \((1/128,1/96)\).

EP-12 gives, for each fixed even \(L\ge 4\), every \(\theta>0\), and every \(m\neq 0\),

\[
0<\widehat k_{L,\theta}(m)\le\frac{\theta}{2\pi^2 m^2}.
\]

The upper bound uses \(0\le D_{L,\theta}\le 2L\) and \(\omega_m^2\ge 4\pi^2 m^2\). The inequality is finite-volume. EP-10’s subsequential limits of the periodic row sum are stated on the admitted interval \(0\le\theta\le 1/192\), and the boundary paragraph says they do not by themselves give uniqueness. Both stop at or below \(1/128\) for the periodic limit. Positivity of one finite-volume mode at one \(\theta>1/128\) is not \(\lim_L k_{L,\theta}\).

TL-12 gives the open-chain lower bound \(\omega^2\widehat{k^I}(m)\ge\theta^2/9\) for every even open chain and every \(0<\theta\le 1/96\). Since \(1/96>1/128\), that finite-volume interval contains temperatures above the Schwarz cut. The same section passes the bound to the limit modes only for \(0<\theta\le 1/192\), with

\[
\widehat k_\theta(m)\ge\frac{\theta^2}{36\pi^2 m^2},
\]

and it lists as not proved the limit for \(\theta>1/192\) and open chains for \(\theta>1/96\). In `positivity.py` the constants are different objects: `WINDOW = 1/192` and `LIMIT_RADIUS = 1/96`. The open-chain bound is not the periodic row-sum limit.

The values inside the proved window stay there. At \(\theta=0\), \(k_0=1/4\). TL-9 gives \(\widehat k_\theta(m)\ge\theta^2/(16\pi^2 m^2)\) for \(0<\theta\le\theta_*=2537/100281465600\). The window bound above stops at \(1/192\). None of these is a theorem for \(\theta>1/128\).

`embedding_bound` raises unless \(\lvert\theta\rvert\le 1/192\). That gate is the smaller cut. Because \(1/192<1/128\), acceptance on that interval is not a statement above \(1/128\).

The dated note keeps the monograph line “anything for \(\theta>1/128\)” only as it applies to the ring lemmas TL-4 and TL-5. It does not convert TL-12 into a periodic volume limit, and it does not withdraw the nonclaim for those two lemmas.

### 6. What stays obstructed

The obstruction is the domain of the written estimate. For \(0\le\theta<1/128\) the sources state \(\varepsilon_L(\theta)\to 0\). At \(\theta=1/128\) the formal factor \(98304\,L/43\) does not tend to \(0\), and the code refuses the point. For every \(\theta>1/128\) the Schwarz hypothesis is false, so \(4 M_1 L(128\theta)^L\) is not a proved bound on \(\lvert k_{L,\theta}-k_\theta\rvert\). The sources do not replace it.

No periodic identification \(\lim_L k_{L,\theta}=k_\theta\) is proved here for any \(\theta>1/128\). The goal row remains the open non-supply those sentences record. A finite model on this carrier does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not claim that \(\lim_L k_{L,\theta}\) exists, is unique, or equals the line row sum \(k_\theta\) for any \(\theta>1/128\). O.12 and TL-5 state the row-sum limit on \(0\le\theta<1/128\). They do not state it above that cut.
- It does not claim that the limit fails. A majorant that does not apply is not a counterexample. Refusal by `lift_error_bound` at \(\lvert\theta\rvert\ge 1/128\) is a domain gate, not a value of the gap.
- It does not treat \(4 M_1 L(128\theta)^L\) at \(\theta=1/96\), where \(128\theta=4/3\), as a bound on \(\lvert k_L-k_\theta\rvert\). The prefactor \(4 M_1\) was taken on the disk of radius \(1/128\).
- It does not treat the endpoint expression \(98304\,L/43\), or the \(L=4\) value \(393216/43\), as \(\varepsilon_L(1/128)\) or as \(\lvert k_{L,1/128}-k_{1/128}\rvert\). The expression is the formal majorant when the power equals \(1\). The code does not return it.
- It does not reuse \(1/384\), \(4/3\), \(2/3\), \(512/175\), \(687/175\), \(13/175\), or \(98304/43\) as a row sum. They are threshold arithmetic for the printed cut and the printed majorant.
- It does not treat TL-2 or TL-3, existence of \(C^\infty\) on \(\lvert\theta\rvert<1/96\), or the tail bound when \(96\lvert\theta\rvert e^\mu<1\), as identification of the periodic row-sum limit on \((1/128,1/96)\).
- It does not treat TL-12, the open-chain bound \(\theta^2/9\) for \(0<\theta\le 1/96\), as that periodic limit. The window section passes positivity to the limit modes only for \(0<\theta\le 1/192\). `WINDOW` and `LIMIT_RADIUS` are different constants.
- It does not treat EP-12’s finite-volume bound \(\theta/(2\pi^2 m^2)\), valid for every fixed even \(L\ge 4\) and every \(\theta>0\), as a thermodynamic limit. It does not treat EP-10’s subsequential limits, which stop at \(0\le\theta\le 1/192\), as a statement for \(\theta>1/128\).
- It does not treat the embedding on \(\lvert\theta\rvert\le 1/192\), or uniformity of the TL-5 rate on that interval, as a statement for \(\theta>1/128\). Since \(128/192=2/3<1\), that interval lies inside the open Schwarz range.
- It does not treat the polymer label norm \(1/128\), coming from \(\lvert\theta\rvert\le 1/96\) and \(\lvert z\rvert,\lvert w\rvert\le 1/64\), as the TL-5 temperature cut. The identity \((3/4)/96=1/128\) is the bond-label edge of that gas.
- It does not reuse \(k_0=1/4\), the bound \(\theta^2/(16\pi^2 m^2)\) on \(0<\theta\le\theta_*\), or \(\theta^2/(36\pi^2 m^2)\) on \(0<\theta\le 1/192\) as a theorem for \(\theta>1/128\).
- It does not choose a Schwarz radius \(R\) with \(\theta<R<1/96\). No such radius is written for \(D_y\).
- It does not claim a real-time or spectral-density statement, the \(X_{LM}\) comparison, a Lean proof of the analytic estimates, probability status for finite signed SQL histories, a continuum limit, or a physical law.
- It does not assert that no later estimate above \(1/128\) could exist. It asserts that the printed TL-5 majorant is not that estimate, and that the goal remains the open non-supply the two source sentences record.
- A finite model on this carrier does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.
