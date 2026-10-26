# Selected sensor pair: trial premises and the repair

**Status.** Selected finite derivation for the broader-work column of
`CH19-O01`. Appendix J already gives the exact compatible-polytope distance
and the conditional finite-sample bound. This note justifies those trial
premises only inside one declared measurement protocol, and it names the
fields of two §13.5 sensors that enter the repair. It does not replace
`WDP-CH19-O01`, and it does not change the nonclaims of Chapters 13 and 19.

**Witness.** `ch19-o01-sensor-repair`,
`problem_sha256` `25e96d22962a5fe701e605af0cf638ff7f70541cede14acad5ad89fa30ac5895`,
receipt
[`evidence/ch19_o01_sensor_repair_receipt.json`](../../evidence/ch19_o01_sensor_repair_receipt.json).
The checker is
[`code/witnessed_difference/ch19_o01_sensor_repair.py`](../../code/witnessed_difference/ch19_o01_sensor_repair.py).
The primal/dual replay is exact rational arithmetic. It does not call the
native functional evaluator.

## 1. What is being selected

The open remainder asks for a justification of the declared within-context
iid categorical trial model, and for a connection from selected physical
measurements to the compatible-polytope repair. The selection made here is
**sensor pair P**:

- two copies, `v` and `w`, of the four-level sensor in §13.5;
- one declared partition of raw codes into outcomes;
- one declared within-context product protocol.

The run table does not force this selection (§9.9). A different partition, or
a different preparation of the same sensor type, is a different repair problem.

## 2. The measurements that the repair sees

Raw codes are \(Z=\{0,1,2,3\}\). The §13.5 calibration, version S13.5, is the
rational interval table

\[
0\mapsto[0,2/5],\quad
1\mapsto[2/5,9/10],\quad
2\mapsto[9/10,3/2],\quad
3\mapsto[3/2,2].
\]

The outcome partition \(P\) is declared on codes, not derived from the
endpoints:

\[
\pi(0)=\pi(1)=0,\qquad \pi(2)=\pi(3)=1.
\]

An alternate interval table with the same code cut,
\(0\mapsto[0,1/4]\), \(1\mapsto[1/4,9/10]\), \(2\mapsto[9/10,5/4]\),
\(3\mapsto[5/4,2]\), is a different calibration record and the same function
\(\pi\). A redeclared cut \(P'\), with \(\pi'(0)=0\) and \(\pi'(1)=\pi'(2)=\pi'(3)=1\),
is a different function. The repair consumes \(\pi\) and the admitted bins.
It does not consume the volt numerals.

A trial is admitted only when its range test and checksum pass. One refused
raw code `3` on `v`, and one refused pair `(1,1)` on `(v,w)`, are absent from
the run table. Each would change the bin list if it were counted: code `3`
lands in outcome `1`, and `(1,1)` lands in section `(0,0)`.

The cover has measurements \(\{v,w\}\), outcomes \(\{0,1\}\), and contexts
\(C_0=(v)\), \(C_1=(v,w)\). Sections are listed in product order. The admitted
raw trials are twelve single codes

\[
0,0,0,0,0,0,0,0,0,1,1,1
\]

and twelve pairs

\[
\begin{align*}
&(0,0),\ (0,1),\ (1,0),\\
&(0,2),\ (1,2),\ (1,3),\\
&(2,0),\ (2,1),\ (3,0),\ (3,1),\ (2,0),\ (3,0).
\end{align*}
\]

Under \(P\) the frequencies are

\[
f_0=(1,0),\qquad f_1=\bigl(\tfrac14,\tfrac14,\tfrac12,0\bigr).
\]

The overlap is \(\{v\}\). The marginal of \(f_1\) on \(v\) is \((1/2,1/2)\),
so the \(\ell^1\) overlap defect is \(1\).

## 3. The premises, and the sensor fact that supports them

Three declarations are kept separate.

1. **(I) Within-context iid draws.** For each context \(i\), the admitted
   trials are independent draws from one fixed rational law \(q_i\) on the
   raw codes of that context.
2. **(P) Declared binning.** The recorded outcome of a trial is \(\pi\)
   applied coordinatewise.
3. **(C) One preparation.** The laws \(q_i\) are the marginals of a single
   joint law \(Q\) on the raw codes of \(\{v,w\}\).

**(Proposition 1.)** Under (I) and (P), the binned trials in context \(i\) are
iid categorical on the sections of \(C_i\), with

\[
p_i(s)=\sum_{z:\pi(z)=s} q_i(z).
\]

*Proof.* A function of one trial sends an iid sequence to an iid sequence.
The law of the image is the pushforward of \(q_i\). \(\square\)

**(Proposition 2.)** If (C) holds, the binned family \((p_i)\) lies in the
compatible polytope: equal overlap marginals, nonnegative, and normalized.

*Proof.* Let \(\overline Q\) be the pushforward of \(Q\) by \(\pi\) on every
coordinate. Each \(p_i\) is the marginal of \(\overline Q\) on \(C_i\).
Marginals of one joint assignment agree on overlaps. \(\square\)

The four-level sensor does not provide \(Q\). The same code alphabet can be
driven by different preparations.

**Countermodel to reading (C) off the sensor type.** Take \(q_0=\delta_0\) and
\(q_1=\delta_{(3,0)}\). Binning by \(P\) gives

\[
p_0=(1,0),\qquad p_1=(0,0,1,0).
\]

The overlap marginals are \((1,0)\) and \((0,1)\). The exact repair radius of
this pair is \(1\), not \(0\). Hypothesis (C) is additional.

**A preparation that does satisfy (C).** Let every raw code be uniform and
independent, probability \(1/4\). Proposition 1 gives

\[
p_0=\bigl(\tfrac12,\tfrac12\bigr),\qquad
p_1=\bigl(\tfrac14,\tfrac14,\tfrac14,\tfrac14\bigr).
\]

The overlap marginals agree, and the repair radius is \(0\).

## 4. The sampling bound, once (I) is declared

Let \(f\) be the empirical frequency of \(n\) iid categorical trials with law
\(p\) on \(m\) sections. Coordinate \(s\) has

\[
\operatorname{Var}(f_s)=\frac{p_s(1-p_s)}{n},
\]

because \(n f_s\) is binomial. Summing over sections,

\[
\mathbb E\|f-p\|_2^2
=\sum_s\operatorname{Var}(f_s)
=\frac{1-\sum_s p_s^2}{n}.
\]

The cross covariances of a multinomial do not appear: the squared Euclidean
norm expands into a sum of squares. Cauchy–Schwarz on the probability vector
gives \(\sum p_s^2\ge 1/m\), hence

\[
\mathbb E\|f-p\|_2^2\le\frac{m-1}{m n}.
\]

Cauchy–Schwarz on the error vector gives \(\|v\|_1^2\le m\|v\|_2^2\), so

\[
\mathbb E\|f-p\|_1^2\le\frac{m-1}{n}.
\]

For a declared rational \(r>0\), Markov's inequality yields

\[
\mathbb P\bigl(\|f-p\|_1>r\bigr)
\le\min\Bigl(1,\frac{m-1}{n r^2}\Bigr).
\]

If \(r\ge 2\) the event is empty, since any two probability vectors have
\(\ell^1\) distance at most \(2\). No independence between contexts is used.
The union bound is the sum of the context bounds, capped at \(1\).

On the event \(\|f_i-p_i\|_1\le r_i\) for every \(i\), marginalization
contracts \(\ell^1\), so each overlap defect is at most \(r_i+r_j\). If (C)
also holds, the population family is a feasible repair, and the minimax
radius satisfies \(\rho(f)\le\max_i r_i\).

The identity is checked by enumerating all four binary strings of length
\(n=2\) with \(p=(1/2,1/2)\). Each string has weight \(1/4\). The average of
\(\|f-p\|_2^2\) is \(1/4\), matching \((1-\sum p_s^2)/n\). The average of
\(\|f-p\|_1^2\) is \(1/2\), matching \((m-1)/n\).

For the twelve admitted trials, the declared radii \(r_0=1/2\) and \(r_1=1\)
give context bounds \(1/3\) and \(1/4\). The pair tolerance is \(3/2\), and
the union bound is \(7/12\). These radii are part of the protocol. They are
not estimated from the twelve rows.

## 5. The distance on this cover

**(Proposition 3.)** For the admitted frequencies of §2,
\(\rho(f)=1/2\). One minimizer is

\[
p_0=\bigl(\tfrac34,\tfrac14\bigr),\qquad
p_1=\bigl(\tfrac12,\tfrac14,\tfrac14,0\bigr).
\]

*Proof.* A compatible pair is a weight \(a\in[0,1]\) with \(p_0=(a,1-a)\) and
a distribution \(p_1\) whose marginal on \(v\) is \((a,1-a)\). Then

\[
\|p_0-f_0\|_1=2(1-a),
\]

because \(a\in[0,1]\) and \(f_0=(1,0)\). The marginal of \(f_1\) on \(v\) is
\((1/2,1/2)\), and marginalization contracts \(\ell^1\), so

\[
\|p_1-f_1\|_1\ge |2a-1|.
\]

If \(a<1/2\), then \(2(1-a)>1\). If \(a\ge 1/2\), the lower bound is
\(\max\bigl(2(1-a),2a-1\bigr)\), which equals \(1/2\) at \(a=3/4\) and is
larger elsewhere. The displayed \(p_1\) has marginal \((3/4,1/4)\) and
\(\ell^1\) distance \(1/2\) from \(f_1\), so the bound is achieved. \(\square\)

The standard-form LP of Appendix J returns the same value. Its primal unpacks
to this same pair, the repaired family is compatible, and an independent
replay checks \(x\ge 0\), \(Ax=b\), \(A^\top y\le c\), and \(c\cdot x=b\cdot y\).
The certificate is the receipt. Changing the table changes the programme that
the replay checks.

Under \(P'\) the single-sensor frequency becomes \((3/4,1/4)\). The source
vector changes, so the repair programme changes. Two calibrations that induce
the same \(\pi\) do not.

## 6. The recorded table does not justify (I)

Let the twelve binned joint trials be read once, as the whole experiment, and
let \(f_1\) be their normalized count. Against that same \(f_1\) the squared
error is \(0\). The iid formula at \(p=f_1\) is

\[
\frac{1-\sum_s f_1(s)^2}{12}
=\frac{1-\bigl(\tfrac1{16}+\tfrac1{16}+\tfrac14\bigr)}{12}
=\frac{5}{96}.
\]

The two numbers differ. The frequency table is the input of both calculations
and does not choose between them. Section 9.9 already records the same fence;
the fraction \(5/96\) is the witness on this multiset.

Therefore (I) and (C) stay declarations. What the sensor contributes is the
admitted code, the declared partition, and, when a joint preparation is
supplied, Propositions 1 and 2. What the repair contributes is \(\rho(f)\) for
the resulting frequency table, together with the Appendix J tolerance on the
declared radii and the actual counts.

## 7. What stays outside

This note does not certify the external volt standard, the checksum, or
metrological traceability (§13.4). It does not derive a Hilbert state, a Born
readout, or tensor composition. Radius zero means compatible context
marginals, not a nonnegative global hidden-variable model; the four-context
PR remark in Appendix J is unchanged. `CH19-O02`, `CH19-O03`, and `CH19-O04`
are not addressed. The canonical ledger row `WDP-CH19-O01` remains the
conditional result already registered.
