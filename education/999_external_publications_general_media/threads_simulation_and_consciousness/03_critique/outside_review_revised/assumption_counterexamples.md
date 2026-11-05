# Counterexamples and limits of the review

These examples delimit the conclusions of the [main review](holographic_brain_review.md). They are included in the [verification script](verification/review_checks.py) where a finite calculation is possible.

## 1. Correlation is not necessarily entanglement

The separable state
$$
\rho=\tfrac12|00\rangle\langle00|+\tfrac12|11\rangle\langle11|
$$
has maximally mixed marginals and
$$
\|\rho-\rho_a\otimes\rho_b\|_1=1.
$$
Call this quantity a **correlation defect**. It detects departure from a product state, including classical correlations. It is not an entanglement measure on arbitrary mixed states.

## 2. First moments do not determine a product state

The product state $|1\rangle\otimes|0\rangle$ has zero annihilation-operator expectations. A coherent-state reconstruction from those first moments returns the vacuum. The two density matrices have trace-norm distance 2, while the product of the exact marginals is the original state.

Thus marginal-product reconstruction and coherent-state reconstruction are different maps. Neglecting terms involving propagators in an evolution equation does not prove that either map was used.

## 3. Local terms can matter to a finite-time bound

For the two-mode Hamiltonian
$$
H=\omega a^\dagger a+\Omega b^\dagger b
+\kappa(a+a^\dagger)b^\dagger b,
$$
the local oscillator terms can generate revivals. A first-order correlation rate does not justify linear growth over a time of order $1/\kappa$. In the finite-system projection theorem, the full incident norm includes the local terms. Its short certified interval must not be extended using the interaction norm alone.

The small two-qubit example in the verification script checks the stated lower bound with its actual full incident norm. It does not certify a bosonic cutoff or the paper's field model.

## 4. A discarded phase and a changed gauge are different operations

Let $q(R,\beta,\mathbf A)=R^2$. On a periodic line, take $R=1$, $\mathbf A=0$, and compare $\beta_1=0$ with $\beta_2=\epsilon\cos x$. Both have the same density, but A69 gives
$$
\dot n_1=0,\qquad \dot n_2=\frac{\epsilon}{m}\cos x.
$$
Density alone therefore does not determine its own subsequent evolution on this state class.

By contrast, changing $\beta\to\beta+\alpha$ and
$\mathbf A\to\mathbf A+\nabla\alpha/e$ together preserves
$\mathbf B=\mathbf A-\nabla\beta/e$. These two descriptions are gauge equivalent. A test of missing physical information must not count them as different physical states. The Madelung description also requires care at zeros of $R$ and around nontrivial phase winding.

## 5. A blind spot is relative to a channel

For a deterministic report $q:X\to P$,
$$
q(x)=q(y)\ \Longrightarrow\ E(q(x))=E(q(y))
$$
for any evaluator $E$ that uses only that report. Another channel can separate $x$ and $y$. The implication is about access to evidence, not identity of worlds.

If $X,P$ are finite and $|X|>|P|$, a collision is unavoidable. Finiteness alone is insufficient: the identity map on a two-element set is injective.

## 6. Equal marginals are not equal experimental predictions

Under hypothesis $H_1$, two fair bits are independent. Under $H_2$, the second copies the first. Each individual bit has the same distribution under both hypotheses, but
$$
P(00\mid H_1)=\tfrac14,\qquad P(00\mid H_2)=\tfrac12.
$$
The joint record has Bayes factor 2 in favor of $H_2$.

For an observed record $D$ with positive likelihood, equal **joint** likelihoods give
$$
\frac{P(H_1\mid D)}{P(H_2\mid D)}
=\frac{P(H_1)}{P(H_2)}.
$$
This preserves prior odds between the two hypotheses. An independent-trial product formula is valid only when the respective independence assumptions hold. Correcting an objection to a model also does not by itself demonstrate that model's distinctive predictions.

## 7. No drawing, no evolution and no record are separate choices

A simulated object may be saved while its update loop is paused, or may evolve while nothing is drawn. These are independent implementation choices. An analogy with a game therefore supplies no unique physical prediction about an unobserved region.

A physical proposal must specify what differs, when it differs, and how a later measurement depends on that difference. Absence of a proposed test is not a proof that no test could exist.

## 8. Uniform screening reconstructs no image

If $o=0$ and $n$ is uniform, $T(n)r$ only rescales the reference field. The nonzero screening parameter does not imply a nonzero reconstructed object image. A valid image test needs spatial modulation and a defined readout.

## 9. Distortion and erasure require a decoder

A distorted analog pattern may still decode perfectly. An apparently unchanged pattern can fail if readout noise crosses the decision threshold. Retention should therefore be assessed by a declared decoding rule or reconstruction tolerance, not by visual adjectives.

## 10. A retained copy changes an erasure problem

On classical bits, the reversible map
$$
(x,y)\mapsto(x,y\oplus x)
$$
copies $x$ into a blank $y=0$, and clears a duplicate $y=x$ while retaining $x$. This does not erase all information about $x$. It shows why a universal energy charge for every operation called “recording” or “clearing” is too broad.
