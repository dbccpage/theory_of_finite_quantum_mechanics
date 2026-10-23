# WDP-APPW-JOINT-SPATIAL-RECONSTRUCTION

Goal id: WDP-APPW-JOINT-SPATIAL-RECONSTRUCTION

Selected scope for WDP-APPW-JOINT-SPATIAL-RECONSTRUCTION is recorded in this note.

The plan row is open. Its `depends_on` list is empty and it names no fence. Its statement is that joint spatial reconstruction remains a separate obligation of the Appendix W scope. This note records the finite identities that the written carrier does supply. It does not construct a spatial reconstruction map and it does not close a joint \((L,M)\) limit. No Python, Rust, or Lean kernel was run for this note. The arithmetic below is exact rational comparison of the printed normalizations.

## Selected scope

Fixed Appendix W carrier only: \(L=4\) periodic sites, 16-dimensional CAR Fock space, \(N=2M\), response order \(LN=8M\), and \(q_M(\psi)=\psi^T G_M\psi/(L N^2)\). At the labelled point \(M=1\), \(N=2\), the §5 kernel-cell prescription (cell value \(L G_{ij}\) and one factor \(1/(LN)\) on each sample index) has prefactor \(L\cdot(1/(LN))^2=1/(L N^2)=1/16\). Theorem T1 still sums \(x\) over these four sites and defines no spatial reconstruction map. The grid sample of \(\cos(8\pi\xi)\) at \(\xi=x/4\) is the 4-tuple \((1,1,1,1)\), the same tuple as the constant profile \(1\), while \(\cos(\pi)=-1\). Not a joint \((L,M)\) limit, not variable \(L\), and not a reconstruction of the continuous kernel \(K\).

## Hypotheses

H1. Appendix W copies the accepted Trotter argument. The opening states that the theorem closes a fixed finite spatial carrier's time limit and does not assert a joint infinite-volume/continuum limit or a Gaussian field law. The same two sentences open `docs/meron_field_limit_derivations/trotter_cochain_extinction_derivation.md`. This copy in the monograph, not a link, is the canonical proof.

H2. Section 1 fixes that carrier. There are \(L=4\) sites and the full 16-dimensional CAR Fock space. Indices are periodic. For \(0<\theta\le 1\) and an integer \(M\ge 1\), the step is \(r=\theta/M\) and \(N=2M\). The response \(G_M=4 D_z^2\log Z_M(0)\) is symmetric of order \(LN=8M\). The declared quadratic is \(q_M(\psi)=\psi^T G_M\psi/(L N^2)\). The scalar \((1+r)^{-M}\) cancels from \(G\).

H3. Theorem T1 uses real periodic \(C^1\) profiles on these four named sites, with \(|\psi_x|\le B\) and \(|\psi'_x|\le D\), sampled by \(\psi_{(j,x)}=\psi_x(j/N)\). Its target \(Q_\theta\) is the continuous-time covariance on the same four sites, with prefactor \(1/L=1/4\) and integrals in the two time variables only. The proof says that no spatial quadrature is taken: the sum over \(x,y\) is the exact sum over the original four indices.

H4. The same paragraph states the missing joint object and does not define it. A joint \(L,M\) limit needs uniform spatial estimates and an actual spatial reconstruction map, and sampling a spatially oscillating function on a fixed grid cannot supply those hypotheses. No formula for that map, no finite family of volumes, and no exact spatial error identity are given in Appendix W.

H5. Section 5's optional kernel prescription is a different object. It assigns cell values \(L G_{ij}\) and cell measure \(1/(LN)\), because the double integral must equal \(q_M\). A convolution of \(K\) with the uniform grid converges to the average of \(K\) and does not reproduce \(K\). The text says this alternative cannot substitute for T1 without its own kernel-binding evidence. The conditional quadratic error \(\delta B^2+\kappa(2B\eta+\eta^2)\) is stated only after a separate absolute kernel bound \(\kappa\) is declared.

## Derivation

### 1. The obstruction is inside the written scope

Section 7 lists joint spatial reconstruction among the obligations that remain separate, beside general all-\(M\) inertia, uniform infinite-volume estimates, cumulant control, Gaussian limits, and native physical repair bindings. It says this scope does not close the continuum or guarded-history registers.

Section 20.12 (GEN-WDP-57) states the finite-carrier time theorem: response matrices have size \(8M\), the quadratic normalization is \(1/(L(2M)^2)\), and the complete quadratic has an \(A/M\) envelope against the fixed four-site continuous-time covariance. The same section says that neither the four spectra nor this fixed carrier's time limit closes all-\(M\) inertia or the spatial continuum programme.

W.8 states that neither compressed-channel extinction nor T1 is a spatial continuum theorem. Earlier model responses that proposed to close the joint limit remain proposals. The estimates they name and do not finish include a uniform infinite-volume bound and a joint spacetime limit under the source normalization and sign conventions. W.8 also says that independently supported static Gaussian and bounded time-labelled cumulant results remain under their own hypotheses and are not a joint spacetime field limit.

`docs/derivation_evidence.md` records the same cut: the full time-limit theorem fixes the spatial carrier at four sites, and no joint spatial limit is included; spatial continuum foundations still need their own witnesses. `docs/four_source_inventory.md` records T1 as proved on the fixed four-site carrier, with the non-implication "No spatial continuum," and records the §7 boundaries, including joint spacetime reconstruction, as open. The plan row for this goal has an empty `depends_on` list and no fence. The source record therefore admits the obligation and does not supply the map.

This is an obstruction inside the written scope. It is not a claim that no later estimate could exist. The reconstruction map and the uniform spatial estimates are the missing objects, not inputs of a calculation on this carrier.

### 2. The §5 cell prefactor equals \(1/16\) at \(M=1\), and only reproduces \(q_M\)

The only reconstruction-shaped formula in §5 is not that map. Place the value \(L G_{ij}\) on each cell and give each sample index the factor \(1/(LN)\). The double sum of cell value times the two cell measures is

\[
\sum_{i,j}(L G_{ij})\,\psi_i\psi_j\cdot\frac1{LN}\cdot\frac1{LN}
=
L\cdot\frac1{(LN)^2}\,\psi^T G_M\psi
=
\frac1{L N^2}\,\psi^T G_M\psi
=
q_M(\psi).
\]

The prefactor identity is the cancellation \(L\cdot(1/(LN))^2=L/(L^2 N^2)=1/(L N^2)\). Both sides are rational for every integer \(M\ge 1\), with \(N=2M\) and the fixed \(L=4\):

\[
\frac1{L N^2}=\frac1{4\cdot(2M)^2}=\frac1{16M^2},
\qquad
L\cdot\frac1{(LN)^2}=\frac4{(8M)^2}=\frac4{64M^2}=\frac1{16M^2}.
\]

At the labelled point \(M=1\), \(N=2\), and \(LN=8\), each side equals \(1/16\):

\[
L\cdot\Bigl(\frac18\Bigr)^2=\frac4{64}=\frac1{16},
\qquad
\frac1{L N^2}=\frac1{4\cdot 4}=\frac1{16}.
\]

The identity is why the piecewise-constant kernel reproduces the discrete quadratic \(q_M\). The same prefactor equality holds for every integer \(M\ge 1\) and still only reproduces \(q_M\). Matching \(q_M\) is not a left inverse for a continuum spatial profile.

The next sentences of §5 state that convolution of \(K\) with the uniform grid converges to the average of \(K\) and does not reproduce \(K\), and that this alternative cannot substitute for T1 without its own kernel-binding evidence. The conditional error bound \(\delta B^2+\kappa(2B\eta+\eta^2)\) is not instantiated here: no absolute kernel bound \(\kappa\) and no spatial mesh are supplied in that paragraph.

### 3. A fixed-grid sample does not separate one oscillation from a constant

T1's sample map sends a profile to values on the four labels \(x\in\{0,1,2,3\}\), at the points \(\xi=x/4\). Take \(f(\xi)=\cos(2\pi L\xi)=\cos(8\pi\xi)\). Then

\[
f(x/4)=\cos(2\pi x)=\operatorname{Re}(e^{2\pi i x}).
\]

For each integer \(x\), \(e^{2\pi i x}=1\), so \(f(x/4)=1\). The sample is the 4-tuple \((1,1,1,1)\), the same tuple as the constant profile \(1\). At the off-grid point \(\xi=1/8\),

\[
f(1/8)=\cos(\pi)=-1,
\]

and \(e^{i\pi}=-1\), so the value is \(-1\), not \(1\). The four-point sample does not separate this oscillation from the constant. It is therefore not a reconstruction map. These are integer identities. They do not send \(L\) or \(M\) to infinity, and they are not a table printed in the monograph. They are the finite content of the sentence that sampling a spatially oscillating function on a fixed grid cannot supply the joint-limit hypotheses.

### 4. Objects that are not reused as the map

Section 6 gives a one-dimensional weighted identity on a single periodic cycle: with fine edge weight \(k\), the sum of \(k(x_j/k)^2\) over fine edges equals the sum of \(x_j^2\) over coarse edges. That identity is not used as a spacetime sum or as a sum over variable \(L\).

The four inertias at \(\theta=1/10\) and \(M=1,2,3,4\), the staggered eigenvalues, the rank-one bound \(|q_{v,M}|\le(E+E^2)D^2/(16M^2)\) with \(E=e^{4\theta}\), and the constant-profile margin \(1/(4e^{4\theta})\) are fixed-carrier time statements. They are not reused as a spatial reconstruction. The Gate E point \(L=4\), \(M=1\), \(r=1/10\) is one finite Trotter-response point. W.8 says it does not establish an unrestricted finite-\(M\) claim or an asymptotic formula, and that neither that channel nor T1 is a spatial continuum theorem.

Theorem T2 is nonnegativity of \(Q_\theta\) for the declared real sources by a finite thermal spectral expansion. The accepted argument states that it contains no unexplained \(|k|\) Fourier weight. The archived draft under `docs/source_archive/locality_and_smearing/` writes a frequency sum with a factor \(|k|\) and a reciprocal factor \(1/|k|\). That draft is not the canonical Appendix W argument. Its frequency weight is not used.

Theorem T4 is descent of a linear adapter through \(C^1/B\) on a declared periodic \(N\)-cycle. The staggered mode and the constant mode are temporal cochain alternatives. The text says neither is automatically the CAR repair relation. The remark that a two-dimensional complex also has an \(\operatorname{im} d_1^*\) summand does not construct a joint spatial limit.

W.8 keeps the static Gaussian and the bounded time-labelled cumulant results under their own hypotheses. They are not used here as a joint spacetime field limit, and the Appendix W obligation is not renamed onto them.

### 5. Conclusion

On this labelled carrier the checkable result is the normalization identity \(1/16\) at \(M=1\). The same prefactor equality holds for every integer \(M\ge 1\) and still only reproduces \(q_M\). The four-site sample of \(\cos(8\pi\xi)\) collides with the constant profile. Neither identity constructs a spatial reconstruction map, a uniform-in-\(L\) estimate, or a joint \((L,M)\) limit. Joint spatial reconstruction therefore remains a separate obligation of the Appendix W scope. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope.

## Claims this note does not make

- It does not claim a joint \((L,M)\) limit, a uniform infinite-volume bound, a continuum spatial law, or a reconstruction of the continuous kernel \(K\).
- It does not treat the rational \(1/16\), or the identity \(L\cdot(1/(LN))^2=1/(L N^2)\) at every integer \(M\ge 1\), as anything beyond the §5 cell-normalization that reproduces \(q_M\). Matching \(q_M\) is not a left inverse for a continuum spatial profile.
- It does not supply the missing \(\kappa\), the missing spatial mesh, or the conditional error \(\delta B^2+\kappa(2B\eta+\eta^2)\). No such bound is evaluated.
- It does not treat T1, T2, T3, the rank-one extinction bound, the four inertias at \(\theta=1/10\) for \(M=1,2,3,4\), or the Gate E point \(L=4\), \(M=1\), \(r=1/10\), as a spatial reconstruction.
- It does not treat T4, the weighted subdivision identity, or the staggered cochain class as the physical CAR repair relation or as this map.
- It does not treat convolution against the uniform grid as a reconstruction of \(K\). The source says that convolution converges to the average of \(K\).
- It does not use the archived draft's \(|k|\) Fourier weight. The accepted T2 argument states that it contains no unexplained \(|k|\) weight.
- It does not treat the static Gaussian, the bounded time-labelled cumulant bound, or a spatially collapsed row-sum of one time variable as discharging the Appendix W joint-spatial obligation. W.8 keeps those results under their own hypotheses.
- It does not treat \(e^{2\pi i x}=1\) and \(\cos(\pi)=-1\) as a printed monograph table, as a classification of every function space, or as the missing uniform spatial estimate. They are the finite content of the fixed-grid sampling sentence.
- It does not claim a device realization, a Gaussian spacetime field, or an unpinned physical law. The joint spatial reconstruction obligation stays open.
