# Lemma 7.1: conditional Hilbert completion and Galerkin dynamics

Status: WRITTEN CONDITIONAL PACKAGE WITH NAMED IMPORTS; not kernel checked. AuthorityEffect: None. No continuum-Hilbert gap closed. Function coordinates are primary; mass-density coordinates are explicitly translated.

## Declared data

Fix a conjugation-compatible embedding of the algebraic coefficient field in C and its standard absolute-value metric. Choose positive pre-Hilbert forms at the finite stages. Admit one of:

G. A countable increasing family of finite cell sets with stable positive weights, mapped by zero extension; or
R. A countable nested family of finite partitions of a fixed total space, with surjective parent maps, positive weights of fixed finite total, additive under refinement, mapped by constant function pullback.

For dynamics, additionally specify a densely defined closed nonnegative form q on the completed Hilbert space H, its associated self-adjoint A, and nested finite-dimensional V_n subset Dom(q) whose union is a FORM core. Define A_n by restricting q to V_n. These are hypotheses to prove in the concrete program, not consequences of the place or additive weights alone.

## 1. Finite spectral algebra and scalar completion

After choosing an ordering of the cyclotomic fixed field, its real closure identifies with R_alg at that ordering; adjoining i gives Qbar with conjugation. Hermitian algebraic matrices have real algebraic spectra and algebraic unitary eigenbases. This follows by splitting over R_alg(i), positivity of the norm and orthogonal-complement induction. Nonsingular inverses and PSD algebraic square roots stay algebraic. Metric completion at the chosen embedding yields C.

Exact real-time exponentiation is a SEPARATE analytic operation. It need not remain algebraic even in dimension one: exp(-i) is transcendental. This part does not place arbitrary finite-stage unitary evolution inside Qbar. A place identifies an embedding modulo conjugation; it is not merely a two-way orientation.

## 2. Hilbert norm and the two completions

A normed direct limit has a Hilbert completion in the same norm iff its norm obeys the parallelogram identity. This is a universal identity, not a finite-sampling decision theorem. Weighted l1 fails on two independent cells. Declare instead the diagonal form <x,y>=sum w_c conj(x_c)y_c, including the disjoint-cell orthogonality it encodes.

In G, completion of finite-support functions is weighted l2 on the cell union. In R, pullbacks are isometric precisely because parent weights sum over children. The countable union Boolean algebra has a compact metrizable Stone space S; its compatible finite clopen charge extends uniquely to a finite Borel measure mu. Locally constant functions are dense, and the completion is L2(S,mu). Both spaces are separable. This is not a spatial-manifold construction.

If a_c=w_c f_c denotes cell MASS, its norm is sum |a_c|^2/w_c and its refinement map is a_child=(w_child/w_parent)a_parent. Do not copy mass coordinates unchanged.

## 3. State and probability convergence

Let P_n be the orthogonal projections onto nested finite-stage spaces with dense union. Then P_n x -> x strongly. For x,y in the common L2 or weighted l2 carrier,

|| |x|^2-|y|^2 ||_L1 <= ||x-y||_2 ||x+y||_2.

For normalized x,y, the corresponding probability measures have TV <= ||x-y||_2, using TV=one-half L1. Coarse-graining preserves this bound. Unnormalized projections give subprobabilities; normalize P_n x when nonzero, or retain a missing-mass outcome. For a unit x the normalized projections converge as well.

Proof: dense nested ranges give projection convergence. Pointwise factorization through the real part of conj(x-y)(x+y), followed by Cauchy-Schwarz, gives the density estimate.

## 4. An admissible closed dynamical realization

Compatible uniformly bounded finite differentials extend uniquely by continuity. Without uniform bounds, first prove a dense differential delta is closable; its closure D gives the closed form ||Dx||^2 on Dom(D) and self-adjoint A=D*D. Alternatively construct a densely defined semibounded symmetric operator and choose its Friedrichs extension. Boundary/core choices must be declared. Neither positivity of a formal expression nor compatibility of finite matrices alone establishes these domains or closability.

The form q in the declared data can be this differential form once its hypotheses have been proved. If stage forms differ from its restrictions, a separate convergence theorem is needed.

## 5. Resolvent and unitary convergence

Let j_n:V_n->H be inclusion and A_n the form/Galerkin operator. Then

j_n(A_n+1)^(-1)P_n f -> (A+1)^(-1)f

for each f in H. Indeed q+<.,.> defines the form Hilbert norm. The Galerkin solution is its orthogonal projection of the full variational solution; form-core density gives convergence in that norm.

Set Atilde_n=A_n direct-sum 0 on V_n^perp. The complement contribution (I-P_n) to (Atilde_n+1)^(-1) tends strongly to zero, giving ordinary same-space strong resolvent convergence. The standard self-adjoint unitary-group convergence theorem then gives

sup_(|t|<=T) || exp(-it A_n)P_n f - exp(-it A)f || -> 0

for each f and each finite T. Real time and the spectral exponential are declared analytic inputs. No operator-norm convergence or effective error rate is asserted. A_n is an operator compression only if V_n subset Dom(A); form-core membership by itself does not supply this.

The named imports are standard scalar closure, Hilbert completion, measure extension, closed-form representation and self-adjoint group convergence theorems. The actual program still owes the specified stage, norm, differential and core hypotheses.
