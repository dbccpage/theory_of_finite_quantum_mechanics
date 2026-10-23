# WDP-O12-XLM-COMPARISON

Goal id: WDP-O12-XLM-COMPARISON

Selected scope for WDP-O12-XLM-COMPARISON is recorded in this note.

The plan row is open. Its `depends_on` list is empty and it names no fence. Its statement is that the comparison of the Euclidean row-sum limit with the time-labelled discrete transfer (\(X_{LM}\)) is not proved. Its note says that identifying O.11's phrase "comparison with the time-labelled discrete transfer" with O.12's "\(X_{LM}\) comparison" is by wording. That join is not a formula. This note does not fill the absence. It differentiates the closed product TD-2a on one pinned carrier and compares that rational with two printed numbers, both \(1/4\). No Python, Rust, or Lean kernel was run.

## Selected scope

Labelled carrier: periodic full-Fock ring \(L=4\) (dimension 16), \(M=1\), \(r=0\) so \(q=1\), half-steps \(j\in\{0,1\}\), sites \(x\in\{0,1,2,3\}\). Discrete object: \(X_{4,1}\) from TD-2a. For each time pair \((j,k)\), \(R(j,k)\) is the sum over \(y\) of \((2M)^2\) times the mixed partial of \(\log X\) in \(z_{j,0}\) and \(z_{k,y}\), at zero source. Euclidean side: the finite row-sum \(k_{4,0}(u)=1/4\) and the \(\theta=0\) limit value \(k_0=1/4\). Exact result: \(R(j,k)=1/4\) and \(R(j,k)-k_0=0\).

Excluded: every \(r>0\), every \(\theta>0\), \(M\to\infty\), \(L\to\infty\), the unrescaled Hessian, and any sum over a time index.

## Hypotheses

H1. \(L=4\) is even and the carrier is the full 16-dimensional Fock space. \(M=1\) and \(r=0\), so \(q=1\). TD-1 then has identity layers, and TD-2a reduces without a continuum step to

\[
X=\prod_{x=0}^{3}2\cosh\bigl((z_{0,x}+z_{1,x})/4\bigr).
\]

Hence \(X(0)=16\). The scalar \(q^{-LM/4}\) equals \(1\) and does not depend on the labels.

H2. TD-1 inserts \(\exp(z_{j,x}a_x/(2M))\). The factor \((2M)^2\) is the rescaling this note uses so that a second derivative of \(\log X\) has the scale of a correlator of \(a\). Here that factor is \(4\). It is the normalization of this one carrier. It is not a comparison normalization printed for general \(M\).

H3. The sentence after EP-8 says that at \(\theta=0\) the normalized trace gives \(C_{xy}(u)=\delta_{xy}/4\), so \(k_{L,0}=1/4\) for every even \(L\ge 4\) and every \(u\). O.12's \(\theta=0\) bullet says \(k_0=1/4\). Those two values already agree at finite \(L\). The polymer criterion and display (O-15) are not used.

H4. First derivatives vanish: \(\tanh(0)=0\), and TD records that odd responses vanish by particle-hole symmetry.

## Derivation

### 1. The closed product

Set \(s_x=(z_{0,x}+z_{1,x})/4\). Then

\[
\log X=\sum_{x=0}^{3}\bigl(\log 2+\log\cosh s_x\bigr).
\]

Each label \(z_{j,x}\) enters only \(s_x\), and \(\partial s_x/\partial z_{j,x}=1/4\).

### 2. The Hessian at zero

Differentiating once gives \(\partial\log X/\partial z_{j,a}=\tanh(s_a)/4\). At zero source this is \(0\). Differentiating again gives

\[
\frac{\partial^2\log X}{\partial z_{j,a}\,\partial z_{k,b}}
=\delta_{ab}\,\mathrm{sech}^2(s_a)/16.
\]

At zero, \(\mathrm{sech}(0)=1\), so the mixed partial is \(\delta_{ab}/16\). Both half-step indices carry the same coefficient in \(s_x\), so the four pairs \((j,k)\in\{0,1\}^2\) give the same rational.

The constant-source check in TD-2a is a different derivative. A common label \(z\) produces \([2\cosh(z/2)]^4\). The second derivative of \(\log(2\cosh(z/2))\) at zero is \(1/4\) per site, and \(4\cdot(1/16)=1/4\), so that check matches the sum of the four unrescaled same-site entries. It is not one pair \((j,k)\).

### 3. The rescaled spatial row

Multiplying by \((2M)^2=4\) sends \(\delta_{xy}/16\) to \(\delta_{xy}/4\). The spatial row at site \(0\), for any one pair \((j,k)\), is

\[
R(j,k)=\sum_{y=0}^{3}\delta_{0y}/4=1/4.
\]

Each difference from \(k_{4,0}\) and from \(k_0\) is the rational \(0\). The two Euclidean numbers do not depend on \(u\). The four discrete pairs do not depend on \((j,k)\). The agreement is an equality of these rationals on this carrier. It is not an identification of the function \(k_\theta(u)\) with a limit of the transfer.

### 4. Rationals that are not the comparison

The unrescaled spatial row-sum of the same Hessian is \(1/16\), not \(1/4\). Summing the rescaled row-sum over the two values of \(k\) gives \(1/2\). That is a sum over a time index and is not the Euclidean row-sum. Neither \(1/16\) nor \(1/2\) is used as the comparison.

### 5. What this identity does not close

O.11 says the finite-volume Euclidean argument does not compare the kernel with the time-labelled discrete transfer. The covariance boundary is later and narrower: the volume-limit questions named in that O.11 paragraph are resolved on the thermodynamic supplement's region, and the transfer's pair derivatives still need an \(M\)-uniform spatial bound and a quantitative comparison with EP-2. Those later results do not establish the discrete-transfer comparison.

O.12 lists the \(X_{LM}\) comparison as not proved. The scope sentence of the thermodynamic-limit note says no comparison with \(X_{LM}\) is supplied. Neither sentence writes a map, a schedule, a norm, or a finite \((L,M)\) at which \(k_\theta\), \(k_{L,\theta}\), or \(C^L\) is compared with a derivative of \(\log X_{L,M}\). Display (O-15) compares the ring row sum with the line row sum. It does not mention \(X_{L,M}\).

The symbol \(X_{L,M}\) is defined in O.10 and by TD-1, on even \(L\ge 4\), integer \(M\ge 1\), and \(0\le r\le 1/192\). TD-3 gives \(|\log X_{L,M}(z)-L\log 2|\le L/19\) for \(|z_{j,x}|\le 1/64\). TD-6 bounds smeared cumulants and says they are not a probability expectation. TD-3 through TD-9 do not give covariance convergence. The boundary of the time-labelled note says comparison with these discrete signed histories remains open, and it does not bound individual non-equal-time site pairs at the natural \((2M)^2\) rescaling.

AR-9 bounds only \(|f_{L,M}''(0)-p''(\theta,0)|\) for the repeated-source curve AR-1. By EP-7a that zero mode is the integral of \(k_{L,\theta}\), not the function \(k_\theta(u)\), and AR-1 repeats one source on every half-step. It is not this independent-label Hessian.

The identity above uses identity layers and \(\theta=0\) evolution. No opened file states an exact rational for the same row-sum at any \(r>0\). The Euclidean series `ZERO_MODE` \(=[1/4,1/8,1/48,-1/96]\) in `checks.py` is a theta-series of the Euclidean zero mode, not a value of \(X_{LM}\). The thermodynamic-limit checks do not name \(X_{LM}\).

A finite model on this carrier does not establish the volume-limit comparison, a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not claim that the comparison of the Euclidean row-sum limit with the time-labelled discrete transfer is proved, refuted, or reduced to a rational gap. O.12 and the thermodynamic-limit scope sentence name that comparison and print no map. The rational \(0\) is the difference of two numbers defined in the selected scope. It is not that missing map.
- It does not identify O.11's phrase "comparison with the time-labelled discrete transfer" with O.12's "\(X_{LM}\) comparison" as one formula. The goal note says that identification is by wording. O.11 does not write the symbol \(X_{LM}\).
- It does not keep O.11's earlier volume-limit list open. The covariance boundary says uniqueness, spatial summability, and the uniform positive lower bound on nonzero modes were later resolved on the supplement's region. The discrete-transfer comparison was not.
- It does not treat display (O-15), the polymer criterion, or the rate \(4 M_1 L(128\theta)^L\) as a comparison with \(X_{L,M}\).
- It does not treat the logarithm bound \(L/19\), the free cosh product as a probability expectation, or the printed value \(k_0=1/4\) by itself as the comparison. The cosh product is the input differentiated here. The bound \(L/19\) is TD-3.
- It does not use the unrescaled row-sum \(1/16\), or the time-index sum \(1/2\), as \(R(j,k)\) or as \(k_0\).
- It does not treat the constant-source second derivative \(1/4\) per site as one independent pair \((j,k)\). That derivative sums the four unrescaled same-site entries.
- It does not treat AR-9, AR-1, or EP-7a as this Hessian. AR-9 is a repeated-source zero mode. EP-7a identifies that mode with \(\widehat k_{L,\theta}(0)\), not with the function \(k_\theta(u)\).
- It does not treat `ZERO_MODE` \(=[1/4,1/8,1/48,-1/96]\) as a value of \(X_{LM}\).
- It does not state an exact rational for the same row-sum at any \(r>0\), any \(\theta>0\), or any \(M\neq 1\). No opened file gives one. The superseded point \(r=1/10\) lies outside \(0\le r\le 1/192\) and is not this carrier.
- It does not claim an \(M\)-uniform spatial bound on the pair derivatives, a fixed comparison normalization for general \(M\), a quantitative match with EP-2 on a joint \((L,M)\) schedule, a distribution topology, or positivity of a finite signed-history measure.
- It does not claim a continuum limit, a physical law, or a closed theorem outside the selected scope.
