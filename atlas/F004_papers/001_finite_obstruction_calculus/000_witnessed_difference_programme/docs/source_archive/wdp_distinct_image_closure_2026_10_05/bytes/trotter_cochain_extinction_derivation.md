# Trotter response, smooth observations, and cochain descent

Corrected derivation, 2026-10-05. AuthorityEffect: None.
Original submitted bytes are retained under
[`docs/source_archive/locality_and_smearing`](docs/source_archive/locality_and_smearing/).
The theorem closes a fixed finite spatial carrier's time limit. It does not
assert a joint infinite-volume/continuum limit or Gaussian field law.

## 1. The exact supplied finite carrier

Take L=4 sites and the full 16-dimensional CAR Fock space. In the ascending
occupation basis, c_x removes site x with sign (−1) raised to the number of
occupied sites preceding x. Define

\[
 n_x=c_x^*c_x,\quad a_x=(-1)^x(n_x-\tfrac12I),\qquad
 P_x=\tfrac12(n_x+n_{x+1}-2n_xn_{x+1}+c_x^*c_{x+1}+c_{x+1}^*c_x).
\]

Indices are periodic. Each P_x is an orthogonal projection. Disjoint even
bonds commute, as do disjoint odd bonds. Let 0<θ≤1, M≥1, r=θ/M, N=2M,
T₀=(I+rP₀)(I+rP₂), T₁=(I+rP₁)(I+rP₃), and K_j=T_(j mod 2).
The input partition is

\[
 Z_M(z)=(1+r)^{-M}\operatorname{Tr}
 \bigl(K_{N-1}e^{\sum_xz_{N-1,x}a_x/2}\cdots K_0e^{\sum_xz_{0,x}a_x/2}\bigr),
 \qquad G_M=4\,D_z^2\log Z_M(0).
\]

The scalar prefactor cancels from G. Its matrix dimension is LN=8M;
this is a spacetime response matrix, not a one-particle Hilbert-space matrix.
For sampled real profiles ψ_(j,x), the declared physical quadratic is

\[
 q_M(\psi)=\frac{1}{L N^2}\psi^TG_M\psi.
\]

This normalization is used throughout. The original Gate E implementation
is reconstructed exactly at M=1; the new reference extends the same insertion
convention, using full traces rather than guessed spectral formulas.

## 2. Reconstructed finite spectra

Independent congruence witnesses establish these inertias at θ=1/10.
Counts below are (positive, negative, zero).

| M | step r | normalized partition | staggered eigenvalue | inertia |
|---|---|---|---|---|
| 1 | 1/10 | 17661/1100 | −1/706440 | (4,1,3) |
| 2 | 1/20 | 755374987/47040000 | −35281/90644998440 | (8,1,7) |
| 3 | 1/30 | 1395062306051761/86870556000000 | −12188547841/55802492242070440 | (12,1,11) |
| 4 | 1/40 | 2379246859363301568641/148151258316800000000 | −14588472130734881/95169874374532062745640 | (16,1,15) |

For M=1 the full spectrum is 10/21,21/40,420/841 (twice),
0 (three times), and −1/706440. At a symbolic one-period r,

\[
 \lambda_1(r)=\frac{-r^4}{4(r+2)(r^2+4r+8)}.
\]

Thus λ₁(1/192)=−1/87426958080. The denominator is
64+64r+24r²+4r³, giving
λ₁=−r⁴/64+r⁵/64−5r⁶/512+O(r⁷).
At r=1/10 the quadratic factor is 841/100, not 281/100.
The table verifies four finite matrices; it is not an all-M inertia theorem.
The time-limit theorem below does not depend on that unproved extrapolation.

## 3. A sharp finite pairing theorem

Let v_(j,x)=(−1)^j, so ∥v∥²=LN, and put
bar A=(LN)⁻¹Σ_(j,x)(−1)^jψ_(j,x). If
|ψ_(2k,x)−ψ_(2k+1,x)|≤D/N, then

\[
 |\bar A|\le\frac{D}{2N}=\frac{D}{4M}.
\]

**Proof.** Pair the N terms into M adjacent differences. The total absolute
sum is at most LM D/N; divide by LN and use N=2M. A linear sampled
profile ψ_j=j/N attains equality, so the finite pair bound is sharp. A
C¹ profile with sup|∂_τψ|≤D supplies this premise by the mean-value theorem.
Time-independent profiles have bar A=0 exactly. ∎

For the rank-one compressed channel P_vG_MP_v, set
λ_v=vᵀG_Mv/(LN). Its contribution is exactly

\[
 q_{v,M}=\frac{\lambda_v}{N}\bar A^2,\qquad
 |q_{v,M}|\le\frac{|\lambda_v|D^2}{4N^3}
             =\frac{|\lambda_v|D^2}{32M^3}.
\]

No eigenvector hypothesis is needed for this compression identity. When v
is the sole negative eigenvector, as in the four checked instances, it is
the entire negative spectral contribution. Outside those instances this
identification needs its own proof.

**All-M extinction of this channel.** Set E=e^(4θ). Products of the K_j
have norm at most E. Tr((T₁T₀)^M)≥16 because T₀,T₁≥I and T₁T₀ is
similar to T₀^(1/2)T₁T₀^(1/2)≥I. First and second normalized insertion
moments have magnitudes at most E/2 and E/4. Hence each response entry
has magnitude at most (E+E²)/4, and
|λ_v|≤2M(E+E²). Consequently

\[
 |q_{v,M}|\le\frac{(E+E^2)D^2}{16M^2}\longrightarrow0.
\]

This proves extinction for the declared smooth observed channel without
postulating bounded eigenvalues or extrapolating the finite inertia table.
It does not by itself prove positivity of the full q_M.

## 4. The fixed-L time-continuum theorem

Let H=Σ_xP_x, and let ψ_x(τ) be real, periodic C¹ functions with
|ψ_x|≤B and |ψ'_x|≤D. Set A(τ)=Σ_xψ_x(τ)a_x, Z=Tr e^(θH),
and ρ=e^(θH)/Z. Define the continuous time-ordered covariance kernel

\[
 K_{xy}(s)=Z^{-1}\operatorname{Tr}(e^{(1-s)\theta H}a_y e^{s\theta H}a_x)
              -\operatorname{Tr}(\rho a_x)\operatorname{Tr}(\rho a_y),\quad0\le s\le1.
\]

For τ_i≤τ_j use s=τ_j−τ_i; reverse order transposes x,y. This produces
a continuous periodic symmetric kernel on pairs: at the endpoints the
trace is cyclic, and at coinciding times the a_x commute. Define

\[
 Q_\theta(\psi)=\frac1L\sum_{x,y}\int_0^1\!\int_0^1
 \psi_x(\tau)K_{xy}(\sigma-\tau)\psi_y(\sigma)\,d\tau d\sigma.
\]

**Theorem T1 (full consistency, explicit envelope).** For the supplied
L=4 carrier and samples ψ_(j,x)=ψ_x(j/N),

\[
 |q_M-Q_\theta|\le\frac{A_\theta(B,D)}{M},\qquad
 A_\theta=L\{30(\theta+\theta^2)e^{16\theta}B^2
                   +2\theta e^{4\theta}B^2+\tfrac12e^{16\theta}BD\}.
\]

**Proof, with conservative constants.** Write H₀=P₀+P₂,H₁=P₁+P₃.
Their norms are at most two and ∥H∥≤4. Taylor's integral remainder gives
∥T_i−e^(rH_i)∥≤r²e^(2r). Duhamel's double integral gives
∥e^(rH₁)e^(rH₀)−e^(rH)∥≤(r²/2)∥[H₁,H₀]∥e^(4r)
≤4r²e^(4r). Thus a complete period has error at most 6r²e^(4r).
The same bound holds in the other layer order. Telescoping k≤M periods
gives 6Mr²e^(4θ). For an unmatched half-period, the identity expansion
and ∥H_i∥,∥H/2∥≤2 give
∥T_i−e^(rH/2)∥≤2r+r²+(e^(2r)−1)≤6re^(2r), since r≤1.
Multiplying the remaining segment and adding the complete-period error
therefore bounds **every** ordered segment by
ε_M=6(θ+θ²)e^(8θ)/M against its ideal e^(θ length H/N).
This covers both starting parities and cyclic arcs.

For each trace there are 16 dimensions and ∥a_x∥=1/2. Both discrete and
ideal normalizing traces are at least 16; their difference is at most
16ε_M. The quotient identity u/d−u'/d'=(u−u')/d+u'(d'−d)/(dd')
then bounds first-moment errors by ε_M(1+E), where E=e^(4θ).
For the two-arc second moment the product telescopes into two errors,
giving ε_M(2E+E²). Products of first moments differ by at most
E ε_M(1+E). Thus each covariance-entry error is at most
5ε_ME²=30(θ+θ²)e^(16θ)/M.
Multiplying by (LN²)⁻¹Σ|ψ_iψ_j| yields the first term of A_θ/M.

For temporal quadrature, |K_xy|≤(E+E²)/4≤e^(16θ)/2.
Differentiating a time segment introduces θ[H,a_x]; trace duality gives
|K'_xy|≤2θE. This bound also controls the kernel across its continuous
coinciding-time seam. The integrand has Lipschitz bound
2θEB²+(e^(16θ)/2)BD in each time coordinate. Each grid cell has total
coordinate error at most 2/N. Summing all x,y and dividing by L yields
L(2θEB²+(e^(16θ)/2)BD)/M. Add the two bounds. ∎

No spatial quadrature is taken in T1: the x indices are the original four
sites. A joint L,M limit needs uniform spatial estimates and an actual
spatial reconstruction map. Sampling a spatially oscillating function on
a fixed grid cannot supply those hypotheses.

## 5. Positivity, strict margins and exact rational schedules

**Theorem T2.** Q_θ(ψ)≥0. Strict positivity requires a nonzero channel
in the spectral formula; a nonzero profile alone need not suffice.

**Proof.** The supplied H and a_x are real symmetric. Choose a real
orthogonal eigenbasis for H, writing its eigenvalues h_a
and thermal weights w_a=e^(θh_a)/Z. Expand A(τ) in temporal Fourier modes.
For each unequal-energy ordered pair a,b and frequency ω_p=2πp, the
real covariance coefficient is

\[
 \frac{(w_a-w_b)\,\theta(h_a-h_b)}
 {\theta^2(h_a-h_b)^2+\omega_p^2}\ge0.
\]

Its contribution is this coefficient times |Â_ab(p)|²/L. The unsymmetrized
coefficient is (w_a−w_b)/(θ(h_a−h_b)+iω_p). Since A(τ) is real symmetric
in this eigenbasis, Â_ab(p)=Â_ba(p); the a,b and b,a coefficients are
complex conjugates at the same frequency, so their imaginary parts cancel.
This real-source hypothesis is part of this theorem; the argument is not
asserted for arbitrary time-dependent complex matrix sources.
At equal energies only p=0 remains. Their combined term is the thermal
variance of the energy-block-diagonal part of the temporal average of A,
which is nonnegative by the weighted square inequality. Subtracting the
mean occurs in this variance term, not separately at every frequency.
These terms exhaust the finite spectral trace and its Fourier expansion.
C¹ profiles justify the summation by square summability. ∎

This is the usual finite thermal spectral argument, derived here from the
declared H. It contains neither an unexplained |k| Fourier weight nor a
replacement of time-dependent Fourier coefficients with only their p=0
averages. Positivity of a covariance also does not establish Gaussianity.

**Corollary T3 (eventual finite positivity).** If an independently justified
margin Q_θ(ψ)≥m>0 is supplied, q_M>0 for every

\[
 M\ge M_0=\max(1,\lfloor A_\theta/m\rfloor+1).
\]

The inequality is strict. A ceiling alone fails when A_θ/m is an integer.
The result uses a uniform error envelope for all later M, not a single
positive sample or an assumption of monotonicity.

There is a concrete source-derived positive-margin example: ψ_x(τ)=1.
Then A=Σa_x has trace zero, Tr A²=16, and thermal mean zero. The last
statement follows from the unitary cyclic site translation, which preserves
H and sends A to −A. In the constant-frequency Kubo trace each spectral
weight before division by Z is ∫e^((1-s)θh_a+sθh_b)ds≥1, since H≥0.
Therefore Q_θ≥Tr A²/(LZ)≥1/(4e^(4θ)).

For exact rational schedules replace e^(kθ) by
E_k=(1−kθ/32)^(-32), k∈{4,8,16}, 0≤θ≤1. The inequality
−log(1−u)≥u proves E_k≥e^(kθ). The reference computes a rational A
and m=1/(4E₄), then checks M₀m>A independently. The margin is bound
to the constant source profile; it is not silently assigned to other fields.

An optional general kernel reconstruction has cell values L G_ij, with each
cell measure 1/(LN), because its double integral must equal q_M. If its
L¹ kernel error is δ and profile interpolation error η, then a separate
declared absolute kernel bound κ yields a quadratic error at most
δB²+κ(2Bη+η²). A convolution of K with the uniform grid converges to
the **average** of K; it does not reproduce K. This alternative cannot
substitute for T1 without its own kernel-binding evidence.

## 6. Exact cochain descent and its limits

On a declared periodic N-cycle let (Df)_j=f_(j+1)−f_j. Then
im D={x:Σx_j=0}; a primitive is constructed by cumulative sums.
The Euclidean quotient norm on C¹/im D is
√N times |mean(x)|. Constants are harmonic, not exact cochains.
The staggered vector is exact: D(−v/2)=v.

**Theorem T4 (adapter descent).** A linear adapter A:C¹→R factors
through C¹/B if and only if A(B)=0. An orthogonal low-pass projector Π_W
alone need not satisfy this. The valid contractive adapter is
Π_W(I−P_B), with P_B the orthogonal projector onto the **declared** B.
It can discard further quotient information; descent is not faithfulness.

**Proof.** Descent implies A(x+b)=A(x), hence Ab=0. Conversely this
identity makes the class formula [x]↦Ax well-defined. Orthogonal projections
are contractions, so their composition is contractive. ∎

For the full cycle B=im D, the adapter keeps only the constant mode if
0∈W, and is zero otherwise. A nonzero low-frequency exact mode is a
counterexample to the claim that low-pass filtering alone kills B. To retain
low-frequency fluctuations while rejecting only the staggered mode, one
must instead declare the smaller B=span(v), and must justify that repair
space for the represented task. Neither choice is automatically the CAR
physics' repair relation. In a two-dimensional cochain complex, the general
Hodge decomposition also includes im d₁*, the coexact component; only on
cocycles does quotienting im d₀ leave precisely the harmonic component.

For integrated edge cochains, subdivision by k maps each edge x_j to k
copies of x_j/k. Potentials interpolate linearly, so D'F₀=F₁D.
Summing the k fragments is a left inverse, and periods are preserved.
If fine edge weight is k, Σ_fine k(x_j/k)²=Σ_coarse x_j², giving the
declared weighted L² isometry and quotient-norm preservation. Unweighted
L² is not invariant. This convention is separate from WDP's L¹ price norm.

## 7. Evidence and remaining scope

The written T1–T3 prove the fixed four-site time limit and its positive-margin
case. The general rank-one smearing theorem does not require an all-M
negative-eigenspace classification. Python retains four original-operator
matrices and independent congruence certificates, pairing witnesses,
cycle primitives, weighted subdivisions and mutation controls. Lean proves
the finite pairing inequality, normalization, square/energy bounds,
strict-margin consequences, and quotient-adapter/cycle identities.
The analytic exponential, spectral and C¹ arguments are written proofs;
they are not advertised as Lean formalization of the physical CAR evolution.
Python is also not formally verified by the Lean mathematical model.

General all-M inertia, uniform infinite-volume estimates, joint spatial
reconstruction, cumulant control, Gaussian limits and native physical repair
bindings remain separate obligations. This scope does not close the paper's
full continuum or guarded-history registers.
