# PLAN-WDP-EDITORIAL

Goal id: PLAN-WDP-EDITORIAL

AuthorityEffect: None.

## Selected scope

Finite controls and manuscript/archive checks for the E1–E12 editorial, type, summary, anchor, and rendered-link reconciliations in `witnessed_difference_programme`:

1. **E1 (Nonsurjective report map and singleton target exception):** On $X=\{0,1\}$, $P=\{0,1\}$ with $q(x)=0$ ($\operatorname{im}(q)=\{0\}\subsetneq P$), no section $s:P\to X$ with $q\circ s=\operatorname{id}_P$ exists; for $|A|=2$ there are $2$ distinct factors $\bar d:P\to A$ extending $d(x)=0$, whereas for a singleton answer target $|A|=1$ there is still a unique factor on all of $P$.
2. **E2 (Mixed-sign weight counterexample):** For $Dx=(x,x)$ and $Au=(u,u)$, the mixed-sign weights $w=(-1,2)$ give $-|x+u|+2|x+u|=|x+u|\ge 0$ with finite minimum $0$ at $u=-x$, whereas $w=(-2,1)$ gives $-|x+u|$, which is unbounded below.
3. **E3 (CHSH bit-to-sign conversion):** Over all $16$ bit tuples $(a_0,a_1,b_0,b_1)\in\{0,1\}^4$, the sign conversion $A_x=(-1)^{a_x}, B_y=(-1)^{b_y}\in\{-1,+1\}$ satisfies $A_0(B_0+B_1)+A_1(B_0-B_1)\in\{-2,+2\}$, whereas the raw bit expression $a_0(b_0+b_1)+a_1(b_0-b_1)$ takes values $\{0,1,2\}$.
4. **E4 (Vector-target linear adapter descent $A:C^1\to W$):** On $\mathbb{Q}^4$ with repair subspace $B=\operatorname{span}\{(1,-1,1,-1)\}$ and a two-dimensional target $W$ whose projector $\Pi_W$ does not annihilate $B$, raw $\Pi_W(v)\ne 0$ while the pre-projected adapter $\Pi_W(I-P_B):C^1\to W$ annihilates $B$ and descends to $C^1/B$.
5. **E5–E10 (Census, Appendix A scope, Chapter 11 anchor, non-simplex polytope, duplicate phrase, and Pauli quotient wording):** Verified directly against `witnessed_difference_programme.md` and `lean4/`.
6. **E11 (Outcome-pair switching probability $j\ne o$):** For a repeatable two-outcome projective instrument on $I/2$, the cross-outcome switching sum ($j\ne o$) is $0$, whereas including $j=o$ yields $1$.
7. **E12 (Archive manifest links):** Relative links to `docs/source_archive/appendix_s_review/source_manifest.json` and `docs/source_archive/locality_and_smearing/source_manifest.json` resolve to regular files with explicit `.json` extensions rather than bare directories that `hyperref` rewrites to `.pdf`.

## Claims this note does not make

- It does not claim that editorial, type, or navigation repairs establish new continuum, infinite-dimensional, or quantum-reconstruction theorems.
- It does not replace independent Lean or Rust proof obligations outside the checked finite carriers.
