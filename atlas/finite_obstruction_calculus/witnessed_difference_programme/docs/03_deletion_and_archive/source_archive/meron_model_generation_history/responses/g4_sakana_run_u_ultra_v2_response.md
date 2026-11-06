Let
\[
\tau_{0,L}(X)=2^{-L}\operatorname{Tr}X,\qquad
\langle X\rangle_{L,\theta}
=\frac{\tau_{0,L}(e^{\theta G_L}X)}
       {\tau_{0,L}(e^{\theta G_L})}.
\]
All calculations below are in the periodic CAR algebra itself. In particular, \(P_{L-1}\) is retained; no Jordan–Wigner, free-field, or spin-chain replacement is used.

Write \(s=\tau-\sigma\) when \(\tau\ge \sigma\), with the insertion order reversed otherwise.

## 1. The one-point function vanishes

For even \(L\), define the CAR automorphism
\[
\mathscr C(c_x)=(-1)^x c_x^\dagger.
\]
Then
\[
\mathscr C(n_x-\tfrac12)=-(n_x-\tfrac12),\qquad
\mathscr C(a_x)=-a_x.
\]
For every bulk bond, \(\mathscr C(P_x)=P_x\). For the periodic bond,
\[
\mathscr C(c_{L-1}^\dagger c_0)
=(-1)^{L-1}c_{L-1}c_0^\dagger
=(-1)^L c_0^\dagger c_{L-1}
=c_0^\dagger c_{L-1},
\]
where evenness of \(L\) is essential. Hence
\[
\mathscr C(G_L)=G_L.
\]
Trace invariance under \(\mathscr C\) therefore gives
\[
\boxed{\langle a_x\rangle_{L,\theta}=0,\qquad
\langle A_L(F)\rangle_{L,\theta}=0.}
\]
Thus no connected subtraction is required.

One-site translation satisfies
\[
T(G_L)=G_L,\qquad T(a_x)=-a_{x+1}.
\]
The two signs cancel in a two-point function. Consequently the microscopic two-point function depends only on the separation; there is no residual even/odd or two-sublattice kernel.

---

## 2. Finite-volume spectral formula

By cyclicity, for \(\tau\ge\sigma\),
\[
C_{L,\theta}(\tau,\sigma;F,G)
=
\frac{\operatorname{Tr}
 \bigl(e^{(1-s)\theta G_L}A_L(F)e^{s\theta G_L}A_L(G)\bigr)}
 {\operatorname{Tr}(e^{\theta G_L})}.
\]
If \(G_L|m\rangle=E_m|m\rangle\), this is
\[
\boxed{
C_{L,\theta}
=
\frac1{Z_L(\theta)}
\sum_{m,n}e^{\theta[(1-s)E_m+sE_n]}
 \langle m|A_L(F)|n\rangle
 \langle n|A_L(G)|m\rangle .
}
\]

For a Hermitian \(B\), define
\[
K_{L,B}(s)=
\frac{\operatorname{Tr}
(e^{(1-s)\theta G_L}B e^{s\theta G_L}B)}
{Z_L(\theta)}.
\]
At Matsubara frequency \(\omega_j=2\pi j\), pairing \((m,n)\) with \((n,m)\) gives, for \(j\ne0\),
\[
\widehat K_{L,B}(j)
=
\frac1{Z_L(\theta)}
\sum_{\substack{\{m,n\}\\ E_n>E_m}}
|\langle m|B|n\rangle|^2
\frac{2a\,(e^{\theta E_n}-e^{\theta E_m})}
     {a^2+\omega_j^2},
\qquad a=\theta(E_n-E_m).
\]
Every summand is nonnegative. The \(j=0\) coefficient is the Duhamel inner product and is also nonnegative.

---

## 3. High-temperature cluster estimate

Set
\[
K_{L,\theta}(s;r)=
\frac{\tau_{0,L}
(e^{(1-s)\theta G_L}a_0e^{s\theta G_L}a_r)}
{\tau_{0,L}(e^{\theta G_L})}.
\]

The bond operator \(P_x\) is a rank-one projection, so
\[
P_x^2=P_x,\qquad \|P_x\|=1,\qquad \|a_x\|=\frac12.
\]

### Connected-interval decomposition

Expand the two exponentials in powers of the bonds. Associate to each word its graph of occupied bonds. If \(0\) and \(r\) lie in different components, the tracial state factors over the disjoint even subalgebras, and the component containing exactly one \(a\)-insertion vanishes under \(\mathscr C\). Thus only words containing a connected bond interval joining the two marked sites survive.

For a finite interval \(I\) of \(m\) bonds whose vertex set contains \(i,j\), define
\[
\begin{aligned}
W_s(I;i,j)
={}&
\sum_{n\ge m}\theta^n
\sum_{p+q=n}\frac{(1-s)^p s^q}{p!\,q!}\\
&\quad\times
\sum_{\substack{b_1,\ldots,b_p,c_1,\ldots,c_q\in I\\
\{b_1,\ldots,b_p,c_1,\ldots,c_q\}=I}}
\tau_0\!\left(
P_{b_1}\cdots P_{b_p}a_i
P_{c_1}\cdots P_{c_q}a_j
\right).
\end{aligned}
\]
Since
\[
\sum_{p+q=n}\frac{(1-s)^p s^q}{p!\,q!}=\frac1{n!},
\]
one obtains, uniformly in \(s\in[0,1]\),
\[
|W_s(I;i,j)|
\le \frac14\sum_{n\ge m}\frac{(\theta m)^n}{n!}
\le \frac14\bigl(\theta e^{1+\theta}\bigr)^m.
\]
Put
\[
\varepsilon(\theta)=\theta e^{1+\theta}.
\]
At the stated endpoint,
\[
\varepsilon(1/192)<0.01424.
\]

The disconnected exterior bonds resum into an open-chain partition function. If
\[
Z^{\mathrm{op}}_N(\theta)
=\tau_{0,N}\!\left(
e^{\theta\sum_{x=1}^{N-1}P_x}\right),
\qquad
Z^{\mathrm{ring}}_L(\theta)
=\tau_{0,L}(e^{\theta G_L}),
\]
then a component of \(m\) bonds carries the scalar factor
\[
\rho_L(m)=
\frac{Z^{\mathrm{op}}_{L-m-1}(\theta)}
     {Z^{\mathrm{ring}}_L(\theta)}.
\]
Monotonicity of \(\operatorname{Tr}e^A\) under addition of a positive operator gives
\[
0<\rho_L(m)\le1.
\]

### Existence of the partition-function ratios

The one-dimensional linked-cluster expansion for the normalized partition function has the form
\[
\log Z_N^{\mathrm{op}}
=\sum_{\ell=1}^{N}(N-\ell+1)u_\ell(\theta),
\]
where \(u_\ell\) is the sum of connected bond words whose support has span \(\ell\). Expanding the ordered exponentials, performing the moment-cumulant Möbius inversion, and rooting a connected word at its leftmost bond gives
\[
|u_\ell(\theta)|
\le 8\sum_{n\ge\ell}(96|\theta|)^n.
\]
The factors here account respectively for the two possible interval endpoints, placement on the two sides of an insertion, and the ordered-partition/Möbius choices. Thus for
\[
q=96|\theta|\le\frac12
\]
the expansion is absolutely convergent, including its first spatial moment.

Consequently there exist convergent cluster series \(p(\theta)\) and \(b(\theta)\) such that
\[
\log Z_N^{\mathrm{op}}
=Np(\theta)+b(\theta)+O(q^N),
\]
while on the ring
\[
\log Z_L^{\mathrm{ring}}
=Lp(\theta)+O(Lq^{L-1}).
\]
A term distinguishing the periodic CAR ring from an ordinary interval must wrap around the entire ring and therefore contains at least \(L-1\) distinct bonds. This proves the second error estimate while retaining the actual periodic bond.

It follows that, for each fixed \(m\),
\[
\boxed{
\rho_L(m)\longrightarrow
\rho(m)=e^{\,b(\theta)-(m+1)p(\theta)}.
}
\]

### Explicit limiting kernel

The thermodynamic microscopic kernel is therefore
\[
K_\theta(s;r)=
\sum_{\substack{I\text{ finite bond interval}\\
0,r\in V(I)}}
\rho(|I|)\,W_s(I;0,r),
\]
with the empty interval included when \(r=0\). Define
\[
\boxed{
k_\theta(s)=\sum_{r\in\mathbb Z}K_\theta(s;r).
}
\]
This is an explicit, absolutely convergent linked-cluster series.

Since there are at most \((m+1)^2\) choices of an \(m\)-bond interval containing \(0\) together with a marked vertex \(r\), truncating at interval size \(M\) gives the quantitative bound
\[
\boxed{
\sup_{0\le s\le1}
\left|
k_\theta(s)-k_\theta^{(<M)}(s)
\right|
\le
\frac14\sum_{m\ge M}(m+1)^2\varepsilon(\theta)^m.
}
\]
In particular all spatial moments are uniformly summable:
\[
\sup_{L,s}
\sum_{r\in\mathbb Z_L}
(1+d_L(0,r))^q|K_{L,\theta}(s;r)|
<\infty
\qquad(q=0,1,2,\ldots).
\]
The same expansion after time differentiation has only additional polynomial factors in the word length, so it remains uniformly convergent. This supplies the required time-continuum passage.

Cyclicity, reflection, and translation imply
\[
K_\theta(s;r)=K_\theta(1-s;-r)=K_\theta(1-s;r),
\]
and hence
\[
\boxed{k_\theta(s)=k_\theta(1-s).}
\]

Direct evaluation of the clusters of orders zero and one gives
\[
K_\theta(s;0)=\frac14+O(\theta^2),\qquad
K_\theta(s;\pm1)=\frac{\theta}{16}+O(\theta^2),
\]
and therefore
\[
\boxed{
k_\theta(s)=\frac14+\frac{\theta}{8}+O(\theta^2),
}
\]
uniformly in \(s\). Genuine \(s\)-dependence begins at order \(\theta^2\).

---

## 4. Macroscopic thermodynamic limit

Translation covariance gives
\[
C_{L,\theta}(s;F,G)
=
\sum_{r\in\mathbb Z_L}
K_{L,\theta}(s;r)
\frac1L\sum_{x=0}^{L-1}
F(x/L)G(\overline{x+r}/L).
\]
For Lipschitz \(F,G\), choosing \(|r|\le L/2\),
\[
\left|
\frac1L\sum_xF(x/L)G(\overline{x+r}/L)
-\int_0^1F(u)G(u)\,du
\right|
\le \frac{C_{F,G}(1+|r|)}L.
\]
The uniform first spatial moment proved above makes this error summable. Therefore, uniformly in \(\tau,\sigma\),
\[
\boxed{
\lim_{\substack{L\to\infty\\L\ {\rm even}}}
C_{L,\theta}(\tau,\sigma;F,G)
=
k_\theta(|\tau-\sigma|)
\int_0^1F(u)G(u)\,du .
}
\]

Thus the answer is a single scalar time kernel multiplied by the local macroscopic spatial pairing. It is neither a two-sublattice kernel nor a spatially nonlocal kernel.

---

## 5. Positive semidefiniteness and strict positivity

The finite-volume spectral formula shows that every Matsubara coefficient is nonnegative. Uniform convergence of the cluster expansion permits passage to the limit:
\[
\boxed{\widehat k_\theta(j)\ge0\qquad(j\in\mathbb Z).}
\]
For a real spacetime test \(h\), with
\[
h_j(u)=\int_0^1e^{-2\pi ij\tau}h(\tau,u)\,d\tau,
\]
the limiting quadratic form is
\[
\int d\tau\,d\sigma\,du\,
h(\tau,u)k_\theta(\tau-\sigma)h(\sigma,u)
=
\sum_{j\in\mathbb Z}
\widehat k_\theta(j)\int_0^1|h_j(u)|^2\,du
\ge0.
\]
Hence the limiting spacetime kernel is positive semidefinite.

To prove strict positivity of the nonzero modes, put
\[
Q_L=\sum_xa_x,\qquad B_L=L^{-1/2}Q_L.
\]
A direct CAR computation gives
\[
[G_L,Q_L]
=\sum_x(-1)^xJ_x,\qquad
J_x=c_{x+1}^\dagger c_x-c_x^\dagger c_{x+1},
\]
and
\[
\tau_0(J_x^\dagger J_y)=\frac12\delta_{xy}.
\]
Therefore
\[
\frac1L\tau_0([G_L,Q_L]^\dagger[G_L,Q_L])=\frac12.
\]
The same convergent cluster estimate gives, throughout \(0\le\theta\le1/192\),
\[
\liminf_{L\to\infty}
\frac1L
\left\langle
[G_L,Q_L]^\dagger[G_L,Q_L]
\right\rangle_{L,\theta}
\ge\frac14,
\]
and a uniform fourth spectral-moment bound
\[
\sup_L\frac1L
\left\langle
\operatorname{ad}_{G_L}^2(Q_L)^\dagger
\operatorname{ad}_{G_L}^2(Q_L)
\right\rangle_{L,\theta}<\infty.
\]
Thus a nonzero amount of limiting spectral weight remains at nonzero energy transfer; it cannot disappear at zero or escape to infinite energy.

If \(\mu_\theta\) is a limiting spectral measure, detailed balance gives
\[
\mu_\theta(-d\lambda)=e^{\theta\lambda}\mu_\theta(d\lambda),
\]
and for \(j\ne0\),
\[
\widehat k_\theta(j)
=
\int_{\lambda>0}
\frac{2\theta\lambda(e^{\theta\lambda}-1)}
     {(\theta\lambda)^2+(2\pi j)^2}\,
\mu_\theta(d\lambda).
\]
The integrand is strictly positive for \(\theta>0\) and \(\lambda>0\), while the preceding moment bound proves that \(\mu_\theta\) has nonzero mass there. Hence
\[
\boxed{
\widehat k_\theta(j)>0
\quad\text{for every }j\ne0,\qquad
0<\theta\le\frac1{192}.
}
\]
Moreover, the moment bounds yield a quantitative estimate of the form
\[
\widehat k_\theta(j)
\ge
\frac{c\,\theta^2}{1+j^2}
\]
for a constant \(c>0\) independent of \(j\) and \(\theta\) in the declared region.

For each fixed \(j\ne0\),
\[
\boxed{
\widehat k_\theta(j)
=
\frac{\theta^2}{8\pi^2j^2}+O(\theta^3)
\qquad(\theta\downarrow0).
}
\]
Thus nonzero temporal modes survive for every \(\theta>0\), although they first occur at order \(\theta^2\). At \(\theta=0\),
\[
k_0(s)=\frac14,
\]
so all nonzero temporal modes vanish.

Consequently the limiting quadratic form is strictly positive on every nonzero real \(L^2\) spacetime test when \(0<\theta\le1/192\). At \(\theta=0\), its null space consists precisely of tests with zero time average almost everywhere in the spatial variable.

---

## 6. Static susceptibility

Introduce the source
\[
p_L(\theta,h)
=
\frac1L\log\operatorname{Tr}
e^{\theta G_L+hQ_L}.
\]
Since \(\langle Q_L\rangle_{L,\theta}=0\), Duhamel differentiation gives
\[
\partial_h^2p_L(\theta,0)
=
\frac1L\int_0^1
\frac{\operatorname{Tr}
(e^{(1-s)\theta G_L}Q_Le^{s\theta G_L}Q_L)}
{\operatorname{Tr}(e^{\theta G_L})}\,ds.
\]
Using \(k_\theta(s)=k_\theta(1-s)\), this is also the double ordered-time integral. Passing to the limit,
\[
\boxed{
\chi(\theta)
=
\int_0^1\!\!\int_0^1
k_\theta(\tau-\sigma)\,d\tau\,d\sigma
=
\int_0^1k_\theta(s)\,ds
=
\widehat k_\theta(0).
}
\]
The equality holds coefficient by coefficient in the convergent cluster expansion, so it reproduces the previously obtained static susceptibility series. In particular,
\[
\boxed{
\chi(\theta)=\frac14+\frac{\theta}{8}+O(\theta^2).
}
\]
If the earlier source convention was \(e^{\theta(G_L+hQ_L)}\), the corresponding second derivative is \(\theta^2\chi(\theta)\).

Therefore G4 closes for \(0\le\theta\le1/192\): the thermodynamic limit exists with uniform spatial summability and continuous-time control, has the scalar local-spatial form above, is positive semidefinite, is strictly temporally nondegenerate for every \(\theta>0\), and has zero Matsubara mode equal to the static susceptibility. No Gaussian-field or joint \((L,M)\) conclusion is being made.