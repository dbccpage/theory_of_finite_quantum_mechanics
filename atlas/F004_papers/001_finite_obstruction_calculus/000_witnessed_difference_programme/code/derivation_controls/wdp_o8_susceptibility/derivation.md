# WDP-O8-SUSCEPTIBILITY

Goal id: WDP-O8-SUSCEPTIBILITY

Selected scope for WDP-O8-SUSCEPTIBILITY is recorded in this note.

The plan row is open. Its `depends_on` list is empty and it names no fence. Its statement is that outside the O.8 analytic high-temperature region, the derivative, sector, and temperature-scaling obligations for pointwise susceptibility stay open. This note does not close that statement. It records that the canonical fixture is not an AR-1 parameter. The witness is the positive integer 767. No Python, Rust, or Lean kernel was run. The arithmetic below compares printed rationals and one factorial bound. It is not a value of \(p''(\theta,0)\).

## Selected scope

Labelled carrier: even periodic full-Fock ring \(L=4\), dimension \(16\), checkerboard count \(M=2\), source parameter \(q=3\). This is the canonical fixture outside the O.8 disk \(0\le\theta\le 1/192\). Exact result: the greatest AR-1 parameter \(q=1+r/M\) at \(r=1/192\) and this \(M\) is \(385/384\), and \(3\cdot 384-385=767\), so \(3-385/384=767/384\).

Not selected: all-temperature pointwise susceptibility, a parity-sector ratio, or a law for \(\theta\) growing with \(L\). The one-dimensional SQL ratios \(48/19\) and \(149/57\) are not reused.

## Hypotheses

H1. Manuscript O.8 and Analytic §1 admit only \(0\le\theta\le 1/192\), with \(q=1+r/M\) for \(r+\rho\le 1/192\) and source radius \(R=1/64\). These constants are sufficient, not a maximal temperature. At \(M=2\) the greatest such \(q\) is \(1+(1/192)/2=385/384\). The complex branch of the pressure is the continuation from zero coupling and zero source. The source disk is not extended by this note.

H2. Analytic §1 takes \(h_x=I/4-P_x\) with norm \(3/4\) and \(a_x=(-1)^x(n_x-1/2)\) with norm \(1/2\). Analytic §3 takes bond labels \(K_x=-\theta h_x\) and two source labels \(z a_x/2\) at each site. On the admitted domain every label has norm at most \(b=1/256\), because \((1/192)\cdot(3/4)=1/256\) and \(|z|\cdot\|a_x\|/2\le(1/64)\cdot(1/4)=1/256\). The polymer margin AR-5, the bound \(C_0=1/19\), and the Cauchy bounds AR-8 and AR-9 are derived only after that ceiling. AR-8's factor \(384\) is \(4!/(1/2)^4\). It is the same integer as the denominator below and is not that denominator's reason.

H3. The fixture is the full \(2^L\) occupation basis at \(L=4\), so the dimension is \(16\), with \(M=2\) and \(q=3\). Time/volume §1 sets the dimensionless temperature \(\theta=M\log q\) and inserts no fixed-number projection. Analytic §7 sets \(\theta_{\mathrm{hat}}=2\log 3\) and states that the fixture lies outside the region and that AR-9 supplies no continuum certificate. The logarithm is the one in \(\theta=M\log q\), the same logarithm for which Analytic §4 uses \(e<3\).

H4. Both parity sectors enter the polymer expansion: Analytic §2 keeps them in one CAR trace and substitutes no unrestricted periodic spin trace. Spin transport §1 keeps the odd sector \(p=-1\) as periodic Heisenberg coupling and the even sector \(p=+1\) as a \(\pi\) twist on the closing bond. Analytic §5 infers no increasing-temperature scaling. Presentation §10 still requires the odd-periodic and even-twisted sectors when \(\theta\) may grow with \(L\), and says a \(\theta/L\) boundary bound need not vanish. O.12 lists anything for \(\theta>1/128\) as not proved. Display (O-13) is a finite-volume comparison. The next sentence of O.11 puts source-disk control of \(p_L''\) in the declared analytic region, not outside it.

H5. O.7 and source-field §5 record why a pressure bound does not give a pointwise second derivative. The pair \(p(x)=\log\cosh(x)/2\) and \(p_n(x)=(1-1/n)p(x)+\log\cosh(nx)/(2n^2)\) satisfies \(0\le p_n-p\le(n-1)\log 2/(2n^2)\), while \(p''(0)=1/2\) and \(p_n''(0)=1-1/(2n)\). The source calls this a logical countermodel to differentiating a pressure claim, not a counterexample to this Hamiltonian. SF-3 is the triangularly averaged response. If the resolution shrinks, pointwise identification needs a further bound. SF-1 through SF-3 supply no third-derivative certificate.

H6. The domain gate was read and not executed. In `meron_analytic_response.py`, `AnalyticResponsePlan` raises when the rational parameter's upper end is strictly above \(1/192\). The endpoint \(1/192\) is admitted. In `meron_source_field.rs`, `AnalyticResponsePlan::new` returns `TemperatureDomain` when \(r+\rho>1/192\). The Rust test source expects that error at \((L,M,r,\rho)=(4,2,4,0)\), and the Python test source expects the same refusal on the point interval \(I(4)\) at \(M=2\). Either comparison is \(q=1+4/2=3\). The gate does not take a complex source \(z\), and it does not return a second derivative.

## Derivation

### 1. The cleared gap in the AR-1 parameter

H1 gives \(q=1+r/M\) with \(r+\rho\le 1/192\). At this checkerboard count the greatest admitted \(q\) has \(\rho=0\) and \(r=1/192\):

\[
q=1+\frac{1/192}{2}=1+\frac{1}{384}=\frac{385}{384}.
\]

The fixture has \(q=3\). Clearing the positive difference gives

\[
3-\frac{385}{384}=\frac{3\cdot 384-385}{384}=\frac{1152-385}{384}=\frac{767}{384}.
\]

The integer \(767\) is that cleared gap. It shows that this \(q\) is not an AR-1 parameter at \(M=2\). The denominator \(384\) is \(2\cdot 192\), from dividing the temperature ceiling by \(M\). It is not AR-8. On the half-radius \(|x|\le R/2\), Cauchy's formula contributes \((R/2)^{-4}=16/R^4\), and \(4!/(1/2)^4=24\cdot 16=384\), so AR-8 states the fourth-derivative majorant \(384 C_0/R^4\). That factor is not a temperature gap.

The same integer appears if the comparison is made in the Euler parameter. The relation \(q=1+r/M\) at \(q=3\) and \(M=2\) forces \(r=M(q-1)=4\). Then

\[
4-\frac{1}{192}=\frac{768-1}{192}=\frac{767}{192}>0,
\]

so the hypothesis \(r+\rho\le 1/192\) fails at \(\rho=0\). Dividing by this \(M\) returns the \(q\)-gap: \((767/192)/2=767/384\). Both displays are outside-membership of one parameter. Neither is \(p''(\theta,0)\).

### 2. The bond-norm ceiling fails by more than \(383/256\)

Independently of the rational truncation in the next section, the factorial comparison used by the polymer argument puts the fixture temperature above \(2\).

For every integer \(n\ge 1\), \(n!\ge 2^{n-1}\). The case \(n=1\) is \(1=2^0\). If the bound holds at some \(n\ge 1\), then \((n+1)!=(n+1)\,n!\ge(n+1)2^{n-1}\), and \(n+1\ge 2\), so the right side is at least \(2^n\). At \(n=3\) the inequality is strict: \(3!=6>4=2^{2}\). Therefore \(1/n!\le 2^{1-n}\) for every \(n\ge 1\), and \(1/3!<2^{1-3}\).

The exponential series and the geometric series then give

\[
e=\sum_{n\ge 0}\frac{1}{n!}
<1+\sum_{n\ge 1}2^{1-n}.
\]

The geometric sum is \(\sum_{n\ge 1}2^{1-n}=\sum_{j\ge 0}(1/2)^j=2\), so \(e<1+2=3\). Hence \(\log 3>1\), and H3 gives

\[
\theta_{\mathrm{hat}}=2\log 3>2>\frac{1}{192}.
\]

H2 gives \(\|h_x\|=3/4\), so the bond-label norm on this fixture satisfies

\[
\theta_{\mathrm{hat}}\,\|h_x\|>2\cdot\frac{3}{4}=\frac{3}{2}.
\]

The admitted ceiling is \(b=1/256\). The excess of this lower bound over that ceiling is

\[
\frac{3}{2}-\frac{1}{256}=\frac{384-1}{256}=\frac{383}{256}.
\]

The fixture bond norm is therefore strictly greater than \(b\), by more than \(383/256\). The activity estimate AR-2, with \(b=1/256\), is not a hypothesis of this fixture. The same holds for the ordered-product activities AR-3, whose exponents are bounded by \(b/M\) only after \(h\le r/M\) on the admitted interval.

Without that ceiling, the margin AR-5, the bound \(C_0=1/19\), and AR-9 do not control the intensive second derivative. AR-9 bounds \(|f_{L,M}''(0)-p''(\theta,0)|\) by \(4B/\epsilon^2+64 C_0\epsilon^2/R^4\) only for \(0<\epsilon\le R/2\) inside the disk, with \(f_{L,M}''(0)=\langle Q^2\rangle/((2M)^2 L)\). The schedule \(L=4k^4\), \(M=L^2\), \(\epsilon=R/(4k)\) keeps one fixed admitted temperature. Analytic §7 says the fixture receives no such certificate. That is the missing derivative control on this carrier. It is not a value of the derivative, and it is not a proof that the derivative limit fails at every temperature.

### 3. A rational separation that does not use \(e<3\)

The series for the same logarithm at \(x=1/2\),

\[
\log 3=\log\frac{1+1/2}{1-1/2}
=2\sum_{k\ge 0}\frac{(1/2)^{2k+1}}{2k+1},
\]

has positive terms. Truncation after three terms is a lower bound:

\[
\log 3>2\left(\frac12+\frac1{24}+\frac1{160}\right).
\]

The sum in parentheses is \(240/480+20/480+3/480=263/480\), so \(\log 3>263/240\) and \(\theta_{\mathrm{hat}}>263/120\). Then

\[
\frac{263}{120}-\frac{1}{192}=\frac{2104}{960}-\frac{5}{960}=\frac{2099}{960}>0.
\]

Thus the fixture temperature lies strictly above the closed upper end \(1/192\). The positive rational \(2099/960\) is this separation. It is not \(p''(\theta_{\mathrm{hat}},0)\), and it does not replace the integer \(767\). The integer shows that \(q=3\) is not an AR-1 parameter. The truncation shows that the temperature named by Analytic §7 lies above the rectangle on which AR-9 was stated.

### 4. The domain gate is not a derivative

H6 is the same outside-membership as a typed refusal. The Python comparison is strict on the upper end, so \(r=1/192\) with radius \(0\) is admitted and any strictly larger upper end is refused. The Rust comparison refuses \(r+\rho>1/192\), and the test source names \((4,2,4,0)\). Refusal at that point is the domain statement. It attaches no AR-9 enclosure, no sector numerator, and no temperature-scaling bound. A gate that does not return \(p''\) does not evaluate \(p''\).

### 5. The sector obligation stays open

Inside the admitted expansion, H4 keeps both fermion parity sectors in the full trace. The spin identity writes the full partition as the sum of the two matching sector traces. Two unrestricted spin traces double the carrier. One unrestricted periodic spin trace is a different operator.

The bulk comparison of Spin transport §2 bounds the log-density difference with the unrestricted periodic spin chain by \(\theta/L\). The same paragraph says this does not erase the finite sectors. Presentation §10 retains the odd-periodic and even-twisted sectors rather than discarding them by a fixed-temperature bulk-density argument.

ARCH-R2-52 withdraws a sector-ratio phase pin: at \(\theta=0\), \(z=0\), the two sectors have equal dimension, so their ratio is one; a modulus bound need not exclude argument \(\pi\); and the rescaling of \(r/M\le 1/192\) into \(r/M\le 1/(192M)\) was then used at \(r=1/10\), outside the region. That withdrawal is not a sector susceptibility on the \(q=3\), \(M=2\) fixture. The sources read here assign no sector numerators and no sector-resolved susceptibility on this carrier. The integer \(767\) does not supply them. The full-trace polymer argument is unavailable once the norm ceiling of §2 fails, and Presentation §10 still requires both sectors.

### 6. The temperature-scaling obligation stays open

Analytic §5 says no increasing-temperature scaling is inferred. One temperature \(\theta_{\mathrm{hat}}>2\) is not a scaling law for \(\theta\) growing with \(L\).

The printed one-bond comparison is at most \(\theta/L\). Presentation §10 says that this bound need not vanish when \(\theta\) grows with \(L\). The schedule \(\theta(L)=L/192\), on even \(L\ge 4\), lies outside the disk at every such length: \(L/192\ge 4/192=1/48\) and

\[
\frac{1}{48}-\frac{1}{192}=\frac{1}{64}>0,
\]

while \(\theta(L)/L=1/192\) does not tend to \(0\). That is a statement about the printed bound. It is not a susceptibility.

The volume error \(3\theta/(2L)\) is the value of \(B\) that AR-9 uses for \(p_L\) inside the declared domain. Source-field §6 says constants valid at a fixed \(\theta\) need not remain uniform when \(\theta\) grows with \(L\). The factor \(\epsilon^{-2}\) in AR-9 is the amplification of a pressure error that has already been taken inside the disk. Neither display is a derivative theorem on a growing-temperature regime. O.12 does not give the susceptibility limit for \(\theta>1/128\). Since \(\theta_{\mathrm{hat}}>2>1/128\), that non-supply covers the fixture temperature and does not evaluate it. Display (O-13) does not move the source-disk control of \(p_L''\) outside the analytic region.

### 7. The printed SQL ratios stay one-dimensional

Spin transport §3 records, on this same fixture, the full-trace integers \(Z=912\) and \(Q^2\) numerator \(36864\). The time-average square printed there is

\[
\frac{36864}{4^2\cdot 912}=\frac{48}{19}.
\]

The equal-time numerator \(2384\) gives \(2384/912=149/57\), and \(|48/19-149/57|=5/57\). The intensive ratio named by AR-10 would divide by a further factor \(L=4\):

\[
\frac{36864}{(2\cdot 2)^2\cdot 4\cdot 912}=\frac{12}{19}.
\]

These are fixed-volume readouts of one carrier. They are not a spatial sum, not a parity-sector split, and not an all-temperature derivative bound. The in-disk value at \(r=0\), whose intensive readout the analytic test source identifies with \(1/4\), is the high-temperature centre \(k_0=1/4\). The order-\(\theta\) site tuple at \(\theta=0\) is that same centre. Neither is this outside-region carrier, and neither is reused here.

### 8. What the integer does not close

The obstruction on this carrier is the failed AR-1 hypothesis and the failed label ceiling. The integer \(767\) shows that \(q=3\) is not an AR-1 parameter at \(M=2\), and §2 shows that the bond norm lies above \(b=1/256\). Without that ceiling, AR-9 does not control the intensive second derivative.

The same integer does not close the other two obligations named by the goal. No file read here gives a uniform bound on \(p''(\theta,0)\) for \(\theta>1/192\), a proved parity-sector ratio on that range, or a scaling relation for \(\theta\) growing with \(L\). Those three obligations stay open. This finite gap is not an impossibility theorem for every temperature.

A finite model does not establish a continuum limit, a physical law, or a closed theorem outside this carrier and the integer \(767\). The goal statement remains the open obligation named by O.7 and O.8.

## Claims this note does not make

- It does not claim an all-temperature pointwise susceptibility, or derivative control of \(p''(\theta,0)\) for \(\theta>1/192\) or \(|z|>1/64\). O.8 and AR-9 state that control on \(0\le\theta\le 1/192\) and \(|z|\le 1/64\). Analytic §7 and Presentation §12 say the \(q=3\), \(M=2\) fixture receives no analytic certificate.
- It does not treat \(767\), \(767/384\), \(767/192\), \(383/256\), or \(2099/960\) as a susceptibility, a row sum, or a value of \(p''(\theta,0)\). They are threshold arithmetic for outside-membership of this fixture.
- It does not treat AR-8's factor \(384=4!/(1/2)^4\) as the denominator of \(767/384\). The denominator is \(2\cdot 192\).
- It does not treat the domain refusal `TemperatureDomain`, or the Python raise on an upper end strictly above \(1/192\), as a derivative. The endpoint \(1/192\) remains admitted. The gate was not executed for this note.
- It does not read \(Z=912\), the numerator \(36864\), the ratios \(48/19\), \(149/57\), or \(12/19\), or the gap \(5/57\), as the thermodynamic susceptibility. They are one-dimensional fixed-volume readouts and are not reused.
- It does not treat \(\chi(0)=1/4\), or the \(\theta=0\) site jet, as this outside-region carrier.
- It does not claim a parity-sector ratio, a sector-phase pin, or the deletion of either parity sector. Presentation §10 retains the odd-periodic and even-twisted sectors. ARCH-R2-52 withdraws a ratio pin that was already outside the region.
- It does not claim a scaling law for \(\theta\) growing with \(L\). The comparison \(\theta(L)=L/192\), the bound \(\theta/L\), and the coefficient \(3\theta/(2L)\) are statements about printed bounds, not a susceptibility on that regime.
- It does not treat O.12's non-supply for \(\theta>1/128\), or display (O-13), as an identification of \(\lim p_L''\) outside the O.8 disk. O.9's static profile, critical mesh, coupling renormalization, and an interacting spacetime field are the neighbouring obligations, not this carrier.
- It does not treat the convex pair \(p\) and \(p_n\) as a counterexample to this Hamiltonian. Source-field §5 calls it a logical countermodel to differentiating a pressure claim.
- It does not claim that the outside limit fails. A majorant that does not apply is not a counterexample. The finite gap is not an impossibility theorem for every temperature.
- It does not claim a sign-problem algorithm, new Lean coverage, probability status for finite signed SQL histories, a continuum limit, or a physical law.
- A finite model on this carrier does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.
