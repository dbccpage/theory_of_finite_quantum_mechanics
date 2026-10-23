I'm considering whether every frame function on rays over Q(i) in dimension 3 must be quadratic, starting by pinning down exactly what counts as a ray—a line K·v for nonzero v in K^3—and whether there's any normalization condition on the inner product.

I'm recalling that in the analogous rational case over Q, a Gleason-type parity argument restricts to primitive integer triples whose squared norm is a perfect square, but here with Q(i) and unrestricted lines, that constraint doesn't directly apply, so I need to think about whether a similar parity or divisibility obstruction still forces quadraticity, perhaps by considering Gaussian integer vectors and their norms directly.

Godsil and Zaks' parity-coloring gives Meyer's result for rational points on $S^2$, but I'm unsure whether the same obstruction extends to all directions in $\mathbb{Q}^3$. The hint about non-real frames nudges me toward adapting the parity argument to Gaussian integers, using norms and congruences modulo powers of $(1+i)$ as a potential obstruction for frame functions over $K^3$ rays with non-square norms.

Over $\mathbb{Q}(i)$, since any positive rational is expressible as a sum of four squares, the norm $\langle v,v\rangle$ can take any positive rational value, meaning rays of every norm exist — so I can't assume normalization to a fixed norm when analyzing these vectors.

Reconsidering the problem's definition: a ray is any line $K\cdot v$, and the frame function needs additivity over all orthogonal frames of such lines. The value $f(Kv) = \langle v,\rho v\rangle/\langle v,v\rangle$ is rational since $\rho$ is Hermitian, making the numerator real hence rational. This brings me back to the key question of whether every frame function must be quadratic, which would be at odds with what I expected from the $\mathbb{Q}^3$ case.

I'm now considering that the $\mathbb{Q}^3$ example only involved rays with square norm (the rational unit sphere), whereas allowing all rational lines changes the problem — I should check whether the orthogonality structure of primitive integer vectors in $\mathbb{Z}^3$ admits a nonquadratic frame function, possibly drawing on known rational analogues of Gleason-type or Kochen-Specker theorems.

Godsil-Zaks showed rational points on $S^2$ have chromatic number 3 for the orthogonality graph, which makes me recall that Peres's 33-vector Kochen-Specker construction uses specific rational direction vectors like $(1,1,0)$ and similar triples.

I'm trying to recall whether rational directions in $\mathbb{Q}^3$ admit a KS-type coloring, and testing a parity approach: reducing primitive integer vectors mod 2 gives one of 7 nonzero elements of $\mathbb{F}_2^3$, and I'm checking whether orthogonality is preserved under this reduction.

I notice that some orthogonal triples collapse under mod-2 reduction, like $(1,1,0),(1,-1,0),(0,0,1)$ both mapping the first two vectors to the same class, so a consistent coloring would force a parity constraint on the counts within each triple — and I'm comparing this against the standard basis triple to see if the constraints are compatible.

Working through several explicit triples and their reductions, I find that symmetry forces $c(110)=c(101)=c(011)=t$ and $c(111)=c(001)=c(010)=c(100)=1-2t$, and plugging into the sum constraint gives $t=1/3$, so $c(111)=1/3$.

Mod 2 reasoning isn't pinning things down uniquely, so maybe I should consider mod 4 structure instead. I'm also wondering if this connects to a known theorem — something like Gleason's theorem adapted to rational or Gaussian-integer vectors, which could suggest an approach for the broader problem about primitive vectors.

I want to check whether the parity trick extends to Gaussian integer vectors $(a,b,c)$ where not all are divisible by $1+i$, using the quotient ring $\mathbb{Z}[i]/(1+i)\cong\mathbb{F}_2$ and working out how norms reduce mod that ideal.

Actually I realize I should re-examine what the problem actually specifies about the rays — whether it's all lines or restricted to a norm-square condition, since that distinction matters a lot for whether the earlier mod-8 argument carries over.

So the real question becomes whether a frame function on all rational lines in $\mathbb{Q}^3$ (or over $\mathbb{Q}(i)$) can fail to be quadratic, thinking of this as orthogonality constraints on the rational projective plane where frame function values on orthogonal triples must sum to 1.

I'm comparing this to Gleason-type theorems for rational vector spaces, checking whether the quadratic family (5-dimensional, coming from trace-1 symmetric forms) exhausts all solutions or whether there's extra freedom from the orthogonal complement structure within each rational plane.

Gleason's original proof relies on continuity, which breaks down entirely over $\mathbb{Q}$, and I recall Meyer's parity function giving a counterexample on the rational sphere—so I need to figure out whether similar pathologies can occur across all of $\mathbb{Q}P^2$ rather than just a single plane.

I'm exploring whether norms of an orthogonal integer frame $(u,v,w)$ satisfy a cross-product identity forcing $N(u)N(v)N(w)$ to be a square times $N(w)^2$, which could be the key to building (or ruling out) a non-quadratic frame function using Hilbert symbol-type obstructions.

I realize that $\chi(N(u))\chi(N(v))\chi(N(w)) = 1$, so an even number of the three values $g(v) = \chi(N(v)) \in \{\pm 1\}$ are negative on a frame, giving $g(u)+g(v)+g(w) \in \{3,-1\}$ -- not constant, so this doesn't directly give me a sum-to-1 function. I need to combine these values somehow to force the sum to always equal 1.

Testing any additive function $h$ on $\mathbb{Q}^*/(\mathbb{Q}^*)^2$ satisfying $h(x)+h(y)+h(z)=1$ whenever $xyz=1$, I plug in $x=y=z=1$ to get $h(1)=1/3$, then $x=y=t, z=1$ to get $h(t)=1/3$ for all $t$ -- so $h$ must be constant, which isn't useful by itself but might combine with a mod-2 reduction approach.

I'm now considering whether a Kochen–Specker approach could apply: if $\mathbb{Q}P^2$ admits a finite KS-colorable set of rational vectors, that would rule out a 0/1 frame function, though frame functions valued more generally in $\mathbb{Q}$ could still avoid being quadratic. I'm trying to recall whether any known KS sets, like Peres' 33 rays built from cube vectors involving $\sqrt{2}$, have purely rational analogues.

I'm trying to recall whether rational direction sets in $\mathbb{Q}^3$ admit a consistent 0/1 coloring avoiding the Kochen-Specker obstruction — I remember Godsil–Zaks showing rational points on the sphere have chromatic number 3 for the orthogonality graph, meaning no KS contradiction arises there. I'm now trying to construct from scratch using integer vectors like $\{0,\pm1\}$ entries plus something like $(1,1,2)$.

Classic KS proofs like the 117-vector construction rely on specific angles such as $\arcsin(1/3)$ built from a particular graph diagram, and these typically require continuous rotations that don't naturally preserve rationality — so I'm questioning whether that construction can be emulated purely with rational direction vectors.

Instead, I'm turning to thinking about primitive vectors in $\mathbb{Z}^3$ modulo 2, which reduce to the 7 nonzero elements of $\mathbb{F}_2^3$: three unit classes, three edge classes, and the all-ones class — this mod-2 structure might give a cleaner combinatorial handle on the problem than trying to force the classic angular construction into rational coordinates.

a 111-type vector requires the other two frame members to be among 110, 101, 011, and these pairwise fail orthogonality mod 2 unless they're the same edge class. So the possible frame types reduce to $\{e_1,e_2,e_3\}$ and $\{e_i, \text{edge}_i, \text{edge}_i\}$ where edge$_i$ has a 0 in position $i$, plus whatever happens with 111-type combinations.

Checking remaining combinations confirms no other mixed types work out, leaving exactly three frame types up to symmetry: Type I is $(e_1,e_2,e_3)$, Type II is $(e_i, \epsilon_i, \epsilon_i)$, and Type III is $(111, \epsilon_i, \epsilon_i)$. Now I want to connect this to Meyer's function on the rational sphere, looking at rays of square norm.

Since unit-type vectors all give Type I frames, the $e_3$-type function handles the sphere case directly, but for $\mathbb{Q}P^2$ I still need to deal with Types II and III. I'm trying to refine the edge classes with a finer invariant — for example, writing $v=(a,b,c)$ with $a,b$ odd and $c$ even in the Type II case — so that the two matching edge-class vectors within a frame can be told apart.

Using the cross product relation $u \times v = \lambda w$, I derive that $N(u)N(v) = \lambda^2 N(w)$ must hold, and working through the factor of 2 in $N(v)$ and $N(w)$ leads to $N(u) m \equiv \lambda^2 n$ with $m,n$ odd, forcing $m \equiv n \pmod 4$ since $\lambda$ turns out odd.

But checking mod 8 doesn't give a clean enough invariant either — depending on $N(u) \bmod 8$, I get $n \equiv m$ or $n \equiv 5m \pmod 8$, which still doesn't cleanly distinguish the two edge vectors. I think I need a different invariant altogether, perhaps looking at the coordinates $a,b \bmod 4$ directly rather than through the norm relation.

So I'm considering, for a type II vector $v=(a,b,c)$ with $a,b$ odd and $c$ even, the invariant $[a\equiv b\pmod 4]$ up to simultaneous sign flip, splitting into $\{(1,1),(3,3)\}$ versus $\{(1,3),(3,1)\}$. Testing this against orthogonality: for a frame with $u\equiv e_3$ and $v,w\equiv 110\pmod 2$, the dot product condition $v\cdot w=0$ forces $aa'+bb'\equiv 0\pmod 4$ since $cc'\equiv0\pmod4$, and I'm working through what this implies when $a\equiv b\pmod4$.

With $c, c'$ even, $cc' \equiv 0 \pmod 4$ holds fine, confirming the pattern for type III frames too — exactly one of $v, w$ has $a \equiv b \pmod 4$, by the same argument with $(1,1,1)$ and $(1,1,0)$ coordinates. This suggests a definition: for primitive $v=(a,b,c)$, classify based on whether $a \equiv b \pmod 4$.

I'm now trying to extend this to vectors congruent to $(1,0,1)$ or $(0,1,1) \pmod 2$. For the type II frame built from $e_1$ and $\epsilon_1$, $f(e_1)=0$, so I need the two $\epsilon_1$-type vectors to sum to 1 — suggesting using $b \equiv c \pmod 4$ as the relevant condition there.

But testing against type II frames with $e_3$ reveals an inconsistency: since $f(e_3)=1$, I need the other two vectors to sum to 0, yet the symmetric construction forces exactly one of them to equal 1, giving a sum of 1 instead. I'm now considering fixing this by forcing $f(v)=0$ whenever $v \equiv (1,1,0) \pmod 2$ regardless of the mod-4 condition, and checking whether that resolves the type II case with $e_3$.

Setting $f(e_1)=f(e_2)=0$ forces constraints that cascade: type II with $e_1$ requires $\epsilon_1$-type pairs to sum to 1, type III with $\epsilon_1$ then forces $f(111)=0$, which through $\epsilon_3$ constraints eventually forces $f(e_3)=0$ too, contradicting type I. I'm trying to see if defining separate functions $g_i$ for each $\epsilon_i$-type could avoid this forced contradiction.

Supposing $f$ only depends on mod-2 class, with $\alpha_i = f(e_i)$ and $\beta = f(111)$, the type I condition gives $\sum\alpha_i=1$, and orthogonal pairs within each frame type must sum to $1-\alpha_i$ or $1-\beta$ depending on frame type. I'm now checking whether every orthogonal pair of a given $\epsilon_i$-type actually appears together in some frame, which would pin down these sums consistently.

I want to see if whether $v\times w$ reduces to an $e_i$-type or $111$-type can be determined from invariants of $v,w$ individually, so I'm computing the cross product components mod 2 and mod 4, writing $c=2\gamma, c'=2\gamma'$ to track the parity structure more carefully.

Working through the mod-4 arithmetic using $a$ odd with $a^2\equiv1\pmod8$, I find $ab'-ba'\equiv2\pmod4$, meaning $(ab'-ba')/2$ is odd. That tells me the third coordinate of $(v\times w)/2$ is odd, so this vector has the parity pattern matching type $e_3$.

Now I check the first two components' parities mod 2, finding both share the same parity determined by $\gamma+\gamma'\pmod2$. This means the resulting vector is $e_3$-type when $c\equiv c'\pmod4$, and type $111$ otherwise.

This suggests defining an invariant $\delta(v)=c/2\bmod2$ for $\epsilon_3$-type vectors $v=(a,b,c)$, well-defined up to sign. In a type II frame $(e_3,v,w)$, $\delta(v)=\delta(w)$, while in type III $(111,v,w)$, $\delta(v)\ne\delta(w)$. I'm also considering a second invariant $\sigma(v)\in\{0,1\}$, equal to 1 iff $a\equiv b\pmod4$.

I'm now trying to combine both invariants into a single function $f(v)=\phi(\sigma(v),\delta(v))$ and derive constraints from type II and III frame equations, setting up relations like $\alpha_3+\phi(0,d)+\phi(1,d)=1$ for type II and a similar equation with swapped $d$ for type III, aiming to solve for $\phi$ consistently across all cases.

Subtracting the two equations forces $q=s$ and $p=r$, so $\phi$ actually only depends on $\sigma$, not $\delta$, giving $\alpha_3=\beta$ and by symmetry all $\alpha_i=1/3$. This ansatz pins the unit types to the constant $1/3$ but still leaves freedom for $\epsilon_3$-types to split as $p$ or $q$ with $p+q=2/3$.

I should double-check I haven't missed any other frame types beyond I, II, and III up to permutation, and I'm re-verifying the type II case by checking that $e_3\cdot\epsilon_3=0$ and $\epsilon_3\cdot\epsilon_3=0$ hold as required.

So the three frame types do seem to be: $\{e_1,e_2,e_3\}$, $\{e_i,\epsilon_i,\epsilon_i\}$, and $\{\tau,\epsilon_i,\epsilon_i\}$ where $\tau=111$, and I'm now setting up the full orthogonality relations mod 2 among all seven classes $e_1,e_2,e_3,\epsilon_1,\epsilon_2,\epsilon_3,\tau$ to confirm no other combinations work.

I also check whether three $\epsilon$-type vectors could be mutually orthogonal, but computing the cross-product parity shows two orthogonal $\epsilon$-type vectors force the third to be an $e$-type or $\tau$-type, so a triangle of three $\epsilon$'s can't occur.

So I define a candidate frame function assigning $1/3$ to $e_i$/$\tau$-type vectors, and $2/3$ or $0$ to $\epsilon_i$-type vectors depending on whether their two odd coordinates agree mod 4. Testing it on the frame $(1,1,0),(1,-1,0),(0,0,1)$ to verify the values come out consistently.

I check several more test frames, computing $f$ on each vector and confirming the sums equal 1 each time, which supports the consistency of the function.

Checking consistency confirms this. I'm testing whether $f$ could be quadratic of the form $v^T\rho v/v^Tv$, solving for $\rho_{12}=-1/3$ from the basis values and verifying it matches other computed values.

By symmetry $\rho_{13}=\rho_{23}=-1/3$ as well, but then plugging into $f(1,1,1)$ gives $-1/3$, contradicting the expected value of $1/3$ -- so $f$ is not quadratic after all. This suggests a genuine non-quadratic frame function exists on the rational lines of $\mathbb{Q}^3$, so I want to verify the underlying lemma: for vectors with specific odd/even coordinate patterns that are orthogonal, checking the parity condition $aa'+bb' \equiv 0 \pmod 4$.

I work through both cases of the mod-4 residues and confirm the claim holds in each -- establishing that exactly one of the two congruences must hold. Now I need to check that the frame function is actually well-defined when passing between a vector and its negative.

Since both the mod-4 condition and mod-2 class are invariant under negation, the function descends properly to $\mathbb{Q}P^2$. I should also verify the construction works consistently across all type II/III cases and symmetric coordinate choices, then revisit the specific frame case where $u \equiv e_3$ to make sure the identification is consistent there too.

Let me verify no frame type is missing by checking mod-2 orthogonality: pairs like $e_i \cdot e_i$, $\tau\cdot\tau$, $e_i\cdot\tau$, and mixed $e_i,\epsilon_j$ all fail mod 2, so the only compatible orthogonal triples come from mutually orthogonal classes built from $\{e_1,e_2,e_3\}$ with repetition allowed only among the $\epsilon_i$.

I realize $\{\epsilon_i,\epsilon_i,\epsilon_i\}$ is automatically excluded, since three pairwise orthogonal vectors would need pairwise distinct $\sigma$ values among only two options—impossible for three. So the key lemma handles this without further computation, letting me define the frame function based on parity of odd coordinates.

For two odd coordinates $x,y$, I'm finding $f(v)=0$ when $xy\equiv1\pmod4$ and $f(v)=2/3$ when $xy\equiv-1\pmod4$, which unifies nicely into the form $f(v)=(1-\chi(v))/3$ or similar expression depending on whether $x\equiv y$ or $x\equiv-y$ mod 4.

For one or three odd coordinates, $f=1/3$ uniformly, so I'm trying to find a single invariant $\epsilon(v)\in\{-1,0,1\}$ that captures all cases at once, looking at the norm $N(v)=a^2+b^2+c^2$ and how it behaves mod 4 along with the product $xy \bmod 4$.

I notice $(1,1,0)$ and $(1,-1,0)$ share the same norm 2 but give different $f$ values, so the frame function clearly isn't a function of the norm alone — it isn't rational in that sense. This raises the question of whether the rational result carries over to the Gaussian rational case over $K=\mathbb{Q}(i)$, where I need to think about $K$-lines in $K^3$ and their primitive Gaussian-integer representatives.

I'm considering whether a non-quadratic frame function could exist on these $K$-rays, since real rational frames embed into $K$-frames but there are far more $K$-frames overall, including rays with no real vector at all — so I want to try adapting the mod-2/mod-4 congruence approach to $\mathbb{Z}[i]$ using the prime $\pi=1+i$.

Working through the quotient rings $\mathbb{Z}[i]/(\pi^k)$ for small $k$ and counting units, trying to see how the orthogonality condition for frames constrains things mod these primes.

Since $c,c'$ are both divisible by $\pi$, their product $\bar c c'$ is only forced to vanish mod 2, not mod 4 as in the integer case. That leaves $\bar a a' + \bar b b' \equiv 0 \pmod 2$ where $a,b,a',b'$ are units mod $\pi$ — essentially residues in $\{1,i\}$ in $\mathbb{Z}[i]/(2)$ — and I'm trying to see what constraint this places on them.

So actually this gives "same" congruence class rather than "exactly one," which seems backwards from what I wanted. Let me test concrete examples with complex vectors to check orthogonality, like $(1,1,0)$ against $(1,-1,0)$ and the complex analog with $i$, to see what's actually happening.

I realize orthogonality holds for many more pairs like $(1,-1,2)$ or $(1,-1,2i)$, so I need a sharper invariant for the Gaussian integer case — perhaps working mod $\pi^3$ or $\pi^4=4$. I'm setting up primitive vectors $v \in \mathbb{Z}[i]^3$, reducing mod $\pi$ to get $\bar v \in \mathbb{F}_2^3 \setminus 0$, and noting Hermitian orthogonality reduces to the ordinary $\mathbb{F}_2$ dot product since conjugation is trivial mod $\pi$.

This gives the same 7 classes and frame-type analysis as before, but now I need to separately check the case where all three coordinates are odd. Focusing on Type II, I'm examining when $u \equiv e_3$ and the other two vectors have two odd coordinates and one divisible by $\pi$, using that divisibility by $\pi$ corresponds to the sum of real and imaginary parts being even.

Computing the inner product condition, the even-coordinate terms simplify to twice a product of the quotients, leaving a relation between the odd-coordinate products. I'm then looking for quantities invariant under scaling by the unit group $\{\pm1,\pm i\}$, finding that products like $\bar a b$ remain fixed under such scaling.

I'm manipulating the relation by multiplying through by $b\bar b'$, trying to express a connection between $\bar a b \cdot a'\bar b'$ and the quantities $|b|^2|b'|^2$ plus a correction term involving $\bar\gamma\gamma'$, aiming to isolate the product that links the two class invariants.

I work out that $|b|^2 \equiv 1 \pmod 4$ for odd Gaussian integers, since one of the two coordinates is even and the other odd. This lets me reduce $s\bar s' \equiv -1 - 2\bar\gamma\gamma' b\bar b' \pmod 4$, and taking mod 2 gives $s\bar s' \equiv 1 \pmod 2$, narrowing down what $s$ must be relative to $s'$.

The term $2\bar\gamma\gamma' b\bar b' \bmod 4$ depends only on whether $\pi \mid \gamma\gamma'$, that is on whether $c$ or $c'$ is divisible by 2. So the invariant likely needs to combine $s \bmod 4$ with a flag $\delta(v) = [2 \mid c]$ tracking divisibility of $c$ by 2.

When at least one of $c, c'$ is even, $s\bar s' \equiv -1 \pmod 4$; when both $\gamma, \gamma'$ are odd, the product $\bar\gamma\gamma' b \bar b'$ is odd and I need to pin down whether it's $1$ or $i$ mod something to resolve this case.

I'm finding that this gives $s\bar s' \equiv 1$ or $-1+2i \pmod 4$ depending on $\bar\gamma\gamma' b\bar b' \bmod 2$, which depends on four separate residues of $\gamma, \gamma', b, b'$ mod 2 — so I likely need a finer invariant than just $\delta$, perhaps something tracking $\gamma$ and $b$ together mod 2.

This derives case B giving $s\bar s' \equiv -1 - 2t(v)t(v') \pmod 4$, then shifts to analyzing the structure of $(\mathbb{Z}[i]/4)^*$, a group of order 8, checking which elements like $i$, $-1$, and $1+2i$ it contains and whether it decomposes as $\mathbb{Z}/4 \times \mathbb{Z}/2$.

I verify all 8 elements generated by $i$ and $1+2i$ account for the full group, confirming $(\mathbb{Z}[i]/4)^* \cong \mathbb{Z}/4 \times \mathbb{Z}/2$, and begin working out what the quantity $s$ corresponds to in this structure.

Trying to mirror the real case argument, I attempt to derive the analogous invariant relation $aa' \equiv -bb' \pmod 4$ for the complex setting but get tangled in the algebra and need to redo the multiplication step more carefully.

Working through the possible values mod 4, I see $s\bar s'$ lands in $\{-1, 1, -(1+2i)\}$, which isn't a single fixed element, so the simple $\sigma$ map doesn't cleanly work here without more structure. I should step back and consider a different invariant, perhaps one tied to the norm instead.

Let me try a non-quadratic function $f$ on $K$-rays that's additive on frames, where I assign a sign $\epsilon(v)\in\{-1,0,1\}$: zero on vectors with an odd number of odd coordinates, and $\pm1$ on two-odd-coordinate vectors, with the constraint that orthogonal pairs sharing odd positions have opposite signs.

This is really asking whether the orthogonality graph on primitive vectors congruent to $(1,1,0) \bmod \pi$ is 2-colorable—equivalently, bipartite with no odd cycles. In the real case I recall the sign $\epsilon(v) = -(ab \bmod 4)$ worked, so now I'm checking whether an analogous construction exists in the complex setting.

I'm trying to find a triangle: three pairwise orthogonal vectors in $E_3$ over $\mathbb{Z}[i]$. I'm testing specific vectors like $(1,1,0)$ and $(1,-1,2)$ to see if their orthogonal complement also lies in $E_3$, checking whether such triangles actually exist, which would determine bipartiteness.

I realize the natural candidate for the third vector is the conjugate cross product $u = \bar v \times \bar w$, since this automatically satisfies orthogonality to both $v$ and $w$. I'm now checking whether this constructed vector, once normalized, can actually land in $E_3$ by expanding its components in terms of the coordinates of $v$ and $w$.

Working mod 2, I'm checking whether $ab'+ba'$ is forced by $aa'\equiv bb'$, multiplying through by $a$ to relate the cross term to $a^2+b^2$ times $b'$.

Since $a^2,b^2\equiv 1\pmod 2$, this sum is $2b'\equiv 0$, confirming $u_3\equiv 0\pmod 2$, so $\pi^2\mid u_3$ while $u_1$ has valuation at least 1. This means if $u_1,u_2$ both have valuation exactly 1 and $u_3$ has valuation at least 2, then dividing through by $\pi$ places $u$ in $E_3$.

Working out $v(u_1)=1$, I find it's equivalent to $\gamma'\not\equiv\gamma\pmod\pi$, since mod $\pi$ both $b,b'\equiv 1$ in $\mathbb{F}_2$, so $b\gamma'-\gamma b'\equiv \gamma'-\gamma$.

By symmetry $v(u_2)=1$ gives the same condition, so when $\gamma\not\equiv\gamma'\pmod\pi$ it looks like $u/\pi$ lands in $E_3$ -- but that contradicts what happened in the real case, where $u_3/2$ was odd instead. I need to recheck the real case computation for $u_3 = ab'-ba'$ to see where the discrepancy comes from.

Testing a concrete example with $v=(1,1,0)$, $w=(1,-1,2)$: computing $\gamma$ and $\gamma'$ shows they're not congruent mod $\pi$, yet the resulting $u$ turns out to be type $\tau$ rather than $E_3$, meaning $u_3$ has valuation 0 rather than 1 as I'd expect. So I'm recomputing $u_1$ directly from the cross product to find the error.

Computing $\bar\pi(\overline{1-i})$ confirms $u_1 = 2$. I realize I made an error here: $\gamma' = 1-i$ is actually divisible by $\pi$ since $1-i = -i(1+i)$, so $\gamma \equiv \gamma' \pmod \pi$ after all, which explains why the valuation isn't 1 as I'd expected.

Let me try a cleaner example where $\gamma \not\equiv \gamma' \pmod\pi$: take $v = (1,1,0)$ with $\gamma=0$, and look for $w = (a',b',\pi)$ with $\gamma'=1$ satisfying the orthogonality condition $a'+b'=0$. Setting $w = (1,-1,1+i)$ works, giving $\langle v,w\rangle = 0$ as required, and now I need to check if $w$ is primitive.

Computing the cross product $\bar v \times \bar w$ to find $u$, I'm getting components that factor nicely by $1-i$...

Checking: $u'=(1,-1,-1-i)$ pairs orthogonally with both $v$ and $w$, confirming all three vectors are mutually orthogonal and lie in $E_3$ — so a triangle does exist in $E_3$.

This is concerning because it shows an all-$\epsilon_3$ type frame exists over $\mathbb{Z}[i]$, which breaks the naive bipartite coloring approach. With the $f=\frac13(1-\epsilon)$ ansatz, I'd need $\epsilon(v)+\epsilon(w)+\epsilon(u')=0$ for $\epsilon\in\{\pm1\}$, which is impossible for three equal values. So the simple sign-based ansatz fails and I need a richer approach.

The problem genuinely gets harder over $\mathbb{Q}(i)$, and the hint about non-real frames being allowed makes me wonder if the parity argument breaks down entirely — possibly pointing toward option (B), that no such function exists and every frame function is quadratic. But proving that would essentially require a Gleason-type theorem over $\mathbb{Q}(i)^3$, which is an extremely heavy lift to formalize given that Gleason's original proof leans on real analysis.

I'm trying to work out whether an algebraic version of Gleason's theorem could hold here, examining whether every $K$-line has a representative vector normalized so $\langle v,v\rangle=1$, since that norm expression reduces to a sum of squared absolute values and is always a positive rational.

This requires the rational value to be a norm from $K^*$, meaning its prime factorization has even exponents at primes congruent to 3 mod 4. Checking an example like $(1,1,1)$ gives norm 3, which fails this condition, so the "unit sphere" structure differs from the usual case—though this shouldn't matter for frame functions defined directly on lines rather than normalized vectors, which leads me to wonder about non-quadratic frame functions.

I'm now considering the general structure on $K$-rays in $K^3$: viewing $P = \mathbb{P}(K^3)$ with its orthogonality graph, a frame function satisfies $\sum f = 1$ on each frame, and the space of such functions is affine over the "null functions" that sum to zero on every frame. Quadratic null functions arise from traceless Hermitian operators, giving an 8-dimensional space over the rationals.

I'm wondering whether exotic (non-quadratic) null functions could be built via local invariants, group actions of $U_3(K)$ on rays, or by gluing constructions from the 2-dimensional case where such exotic functions are known to exist.

Reconsidering the problem over $\mathbb{Z}[i]$, I note that triangles obstructing non-quadratic functions over $\mathbb{Q}$ don't vanish the same way here, so I'm examining the orthogonality graph on $E_3$ more carefully, looking for a null function vanishing elsewhere but exhibiting non-quadratic behavior on that class, trying to work through how each frame type constrains the function.

I also need every orthogonal triple within $E_3$ to sum to zero, and I want to rule out $g$ being quadratic — checking whether a quadratic function like $\langle v,\rho v\rangle/\langle v,v\rangle$ could vanish on this set, since the relevant vectors form a Zariski-dense family and would force any such quadratic form to vanish identically.

This translates to needing a nullity condition on $g$ itself: every orthogonal pair or orthogonal triple within $E_3$ must sum to zero, so I need to understand how orthogonality behaves restricted to this substructure, including whether pairs always extend uniquely to frames inside or outside $E_3$. I'm also considering shifting the support to a different residue class, like vectors congruent to $(1,1,1)$ under some equivalence.

I check whether that candidate support actually satisfies the frame conditions, but type III frames and unit-class frames both force $g$ to vanish trivially, so those don't work — meaning the support genuinely has to involve $E$. Now I'm digging into the structure of $E_3$ itself, looking at vectors with two odd Gaussian-integer coordinates and one even one, and trying to find invariants under unit scaling since the components aren't normalizable the way I'd like.

I recall that in the real analogue, $g$ was built from $\chi_4(ab)$, the quadratic character mod 4 applied to the product of two coordinates, which factors as $\chi_4(a)\chi_4(b)$ and stays invariant under $v \to -v$. This suggests I should look for an analogous character-product construction in the Gaussian integer setting.

Now I want to analyze the orthogonality condition $\bar a a' + \bar b b' + \bar c c' = 0$ directly, treating $(a,b)$ and $(a',b')$ as pairs in $\mathbb{Z}[i]^2$ satisfying $\bar a a' + \bar b b' = -\bar c c'$.

I'm examining the quantity $r = \bar a b$ as a unit-invariant odd Gaussian integer, and relating $r\bar r'$ to $\bar a a'$ and $b\bar b'$, then trying to track this mod 4 by analogy with the simpler real-number case where $cc'$ vanishes mod the relevant modulus.

In the complex case I notice $\bar c c'$ only vanishes mod 2, not mod 4, so the parallel breaks down. This makes me consider instead working modulo $\pi^3$ where $\pi = 1+i$, computing the structure of $\mathbb{Z}[i]/\pi^3$, which has 8 elements with 4 units, and checking whether these unit classes are actually distinct.

I verify by checking differences: $1-i$, $1-(-1)$, $1-(-i)$ all have valuation 1 or 2 but never 3, confirming the four units $\{1,i,-1,-i\}$ remain distinct mod $\pi^3$ and form a cyclic group of order 4 generated by $i$. So every odd Gaussian integer reduces to one of these four units modulo $\pi^3$.

This is a unit-invariant in $\mathbb{Z}/4$. I'm checking the condition $r\bar r' = (\bar a a')(b\bar b')$ mod $\pi^3$, reducing to whether $\pi$ divides $\gamma\gamma'$, and verifying the congruences $2 \equiv -2$ and related residues mod $\pi^3$.

I need $i^m + i^n \pmod{\pi^3}$: this vanishes exactly when $n-m \equiv 2 \pmod 4$, and equals $2 \pmod{\pi^3}$ exactly when $n = m$; if $n-m$ is odd the valuation is only 1, matching neither case. So depending on whether $\pi \mid \gamma\gamma'$, I get a congruence relating $k(a')-k(a)$ and $k(b')-k(b)$ mod 4.

This gives $\kappa(w) = \kappa(v) + 2$ when $\pi$ divides $\gamma\gamma'$, and $\kappa(w) = \kappa(v)$ when $\pi$ divides neither. This is promising — it suggests I should define $\kappa(v) \in \mathbb{Z}/4$ and $\delta(v)$ as an indicator tied to divisibility by $\pi$, essentially tracking parity of some coefficient.

I verify the rule against the triangle: for $w=(1,-1,1+i)$ and $u'=(1,-1,-1-i)$, both have $\kappa=2$ with $c=\pi$ giving $\delta=0$, and since $\delta(v)=1$, the rule correctly predicts $\kappa(w)=\kappa(v)+2$; and since $w,u'$ both have $\delta=0$, their $\kappa$ values match as expected.

Now I'm turning to when the third vector of an orthogonal pair in $E_3$ stays in $E_3$, working through the cross product formula $u=\bar v\times\bar w$ and tracking the valuation $v_\pi(u_1)$ via $b\gamma'-\gamma b'\equiv \gamma'-\gamma \pmod \pi$ since $b,b'$ are odd.

I find $v_\pi(u_1)=1$ exactly when $\gamma\not\equiv\gamma'\pmod\pi$, i.e. when $\delta(v)\ne\delta(w)$, and the same holds for $u_2$ by symmetry. So in that case, $u_1,u_2$ each have $\pi$-valuation 1 while $u_3$ has valuation at least 2, meaning $\gcd(u)$ has $\pi$-valuation exactly 1 and after dividing out, the resulting vector has odd first two coordinates with an even third one.

This matches the structure of $E_3$ — confirming the "if $\delta(v)\ne\delta(w)$" direction. For the converse, I still need to work out what happens when $\delta(v)=\delta(w)$, where both $v_\pi(u_1)$ and $v_\pi(u_2)$ are at least 2 along with $v_\pi(u_3)$; I'll need to pin down the exact valuations in that case to settle whether membership in $E_3$ really forces $\delta(v)\ne\delta(w)$.

Checking the case where two of the three have $\delta = 1$ leads to a contradiction, since the implied $\kappa(w)$ values conflict by 2 mod 4 — so that configuration is impossible. Testing all three with $\delta = 1$ gives a similar consistency check to verify.

So type IV frames can have at most one vector with $\delta = 1$, meaning the $\delta$-pattern is either $(0,0,0)$ or $(1,0,0)$ up to ordering. I'm now defining a function $g$ on $E_3$ via $\phi(\kappa(v), \delta(v))$ and checking two conditions: orthogonality constraints when the third vector isn't in $E_3$, and the sum condition for type IV triangles. I need to pin down exactly when the third vector fails to be in $E_3$ — it looks like differing $\delta$ values between $v$ and $w$ force the third vector into $E_3$.

So condition (α) only applies when $\delta(v) = \delta(w)$, with $\kappa(w)$ shifting by 2 if $\delta=1$ or staying equal if $\delta=0$. Checking a concrete example like $(1,1,0)$ and $(1,-1,0)$ confirms such pairs exist, giving me the relation $\phi(\kappa,1) + \phi(\kappa+2,1) = 0$ for all $\kappa$.

Now I want to check the $\delta=0$ case similarly — testing $v=(1,1,\pi)$ against a candidate $w$ and solving the orthogonality condition, I find $w = -v$ satisfies it.

Trying another candidate $w=(1,-3,1+i)$ instead, I verify the inner product vanishes, then compute the cross product $u = \bar v \times \bar w$ to get the third vector in the orthogonal triple.

I simplify $u$ to $(1-i, 0, -1)$ and check its coordinates mod $\pi$: with $0$ and $1-i$ even and $-1$ odd, this reduces to $e_3$, confirming it's not in $E_3$, so $\phi(\kappa,0)=0$ for this choice. Now I want to check other values of $\kappa$, starting with $v = (1, i, \pi)$ giving $\kappa=1$, and I set up a similar orthogonal vector $w$ to test.

Simplifying confirms this is again an $e_3$-type vector, giving $\phi(1,0)=0$, so I conjecture $\phi(\kappa,0)=0$ for all $\kappa$, meaning $g$ vanishes on all $\delta=0$ vectors. Checking the type IV triangle case $(0,0,0)$ trivially works, and $(1,0,0)$ requires $\phi(\kappa(v),1)=0$ — I need to check whether such triangles actually exist.

I find an explicit example with $\kappa=0,\delta=1$, and by applying a unitary symmetry (multiplying by powers of $i$) I can shift $\kappa$ to any value, showing triangles exist for all $\kappa$ and hence $\phi(\kappa,1)=0$ identically. That means $g\equiv 0$ under this ansatz entirely, so depending only on $(\kappa,\delta)$ isn't enough — I need a richer invariant.

So I reconsider whether answer (B) could actually hold, wondering whether Gleason's theorem extends to $\mathbb{Q}(i)^3$: the unitary group over $\mathbb{Q}(i)$ is larger, and I'm checking whether every 2-dimensional Hermitian subspace orthogonal to a line looks essentially the same.

I'm working out that these binary Hermitian forms over $\mathbb{Q}(i)$ are classified by their determinant class and local invariants, and I'm computing that determinant in an orthogonal basis of the orthogonal complement.

So $N(u')N(v)N(w)$ lands trivially in $N(K^*)$, meaning the product of the three norm classes vanishes for any $K$-frame. That makes the norm-class function $\nu$ into rays a trivial invariant on frames by itself — as I found before, this alone forces constant functions, so I need to check whether richer invariants could still produce nontrivial null functions on the relevant projective space.

Looking at 2-dimensional subspaces, I'm examining the binary Hermitian form on $\ell^\perp$ over $\mathbb{Q}(i)$: choosing an orthogonal basis gives a diagonal form with coefficients equal to the norms of the basis vectors, and I'm working out the condition for two vectors in this space to be orthogonal to each other.

This gives an explicit involution on $\mathbb{P}(\ell^\perp) \cong \mathbb{P}^1(K)$ pairing each point with its orthogonal complement, having no fixed points, and the frame function must satisfy a complementary-sum condition on these pairs partitioning the projective line.

I'm now wondering if there's a more direct construction of an exotic frame function on $K^3$: perhaps I could define an invariant on primitive vectors in $\mathbb{Z}[i]^3$ that's "local" at some prime $\pi$, respecting frame consistency, but since type IV frames exist I suspect this requires a more intricate invariant.

So I'm shifting to the $\pi$-adic completion picture, considering $\mathbb{Z}_2[i]$ and asking whether a locally constant function on $\mathbb{P}^2(\mathbb{Q}_2(i))$ can vanish on every orthogonal frame of the Hermitian form over this local extension. Since the Hermitian form becomes isotropic in dimension at least 3 over this local field, this seems like a promising angle to explore.

I should instead revisit the real/integer construction structurally to see why it worked: the function was built from $\chi_4(ab)$ on odd integer pairs, which factors multiplicatively as $\chi_4(a)\chi_4(b)$, with $\chi_4(a)$ tied to the Jacobi symbol $(-1/a)$ — perhaps this connects to Hilbert symbols or spinor norms rather than something purely quadratic.

This splits as $(-1,a)_2(-1,b)_2$, so I'm wondering if there's a conceptual reason via Hilbert symbols on the frame $(u,v,w)$ with norm product a square. For $v \in E_3$, the norm $a^2+b^2+c^2$ reduces mod 8 to either 2 or 6 since $a^2+b^2 \equiv 2 \pmod 8$, and I'm checking what $(-1, N(v))_2$ evaluates to in each case.

It seems $(-1,N(v))_2$ actually encodes $\delta(v)$ rather than $\kappa$, since it simplifies to a sign depending on whether $c \equiv 0$ or $2 \pmod 4$. So the real invariant $\chi_4(ab)$ must be coming from somewhere else -- I'm trying factoring $a^2+b^2$ as $(a+ib)(a-ib)$ in the Gaussian integers to see if that reveals the connection.

Continuing, I find that $\chi_4(ab)$ reduces to whether $(a+ib)/\pi$ is congruent to $1$ or $i$ mod $2$, equivalently whether $a+ib \equiv \pi$ or $i\pi \pmod{\pi^3}$ — a neat reformulation but possibly not useful. I'm now considering pivoting toward the approach the problem itself hints at.

Given the setter's explicit mention of norms and congruences mod powers of $(1+i)$, plus the warning about non-real frames and checking which rays actually exist, I suspect the expected obstruction mirrors the parity argument but needs careful restriction to the right set of rays. The instructions push toward settling the question definitively and proving it in Lean, or otherwise isolating the largest honest finite case if neither direction fully works. This pushes me to dig deeper into whether exotic null functions can actually exist on $\mathbb{P}(\mathbb{Q}(i)^3)$.

I try examining this through the orthogonality relation tied to $U_3(\mathbb{Z}[i])$ and reductions modulo powers of $\pi$, but primitivity issues with the third vector mean frames don't reduce cleanly mod $\pi^k$. So instead I go back to the real-case construction and try adapting it directly, defining a function on primitive vectors using the quartic character applied to pairwise products of coordinates, split across the different frame types.

I'm checking whether summing $\chi_4(ab)+\chi_4(bc)+\chi_4(ca)$ (treating even arguments as contributing 0) gives something uniform: for the $E_3$-type frame it isolates just $\chi_4(ab)$, for unit-type frames all products are even so it vanishes, and for the $\tau$-type with all coordinates odd I'm working out that $(abc)^2\equiv 1\pmod 4$, so I'm counting how many of the three terms come out to $-1$.

That count must be even — 0 or 2 — giving a sum of either 3 or $-1$, never 0, so this invariant isn't uniform across frame types either. I'm now trying a projective reformulation: viewing the odd pair $(a,b)$ as a point of $\mathbb{P}^1(\mathbb{Q})$ reducing mod 2 to $(1:1)$, where $\chi_4(ab)$ just records which of the two lifts, $(1:1)$ or $(1:-1)=(1:3)$, it reduces to mod 4.

So $g$ on $E_3$ essentially picks out which of these two mod-4 points $(a:b)$ lands on, and the orthogonality condition $aa'+bb'\equiv 0 \pmod 4$ corresponds to the mod-4 orthogonal involution on $\mathbb{P}^1(\mathbb{Z}/4)$ that swaps those two points. I want to see if this same structure carries over to the complex setting.

Mod $\pi^3$ this reduces to $\bar c c' \bmod \pi^3$ and the deltas, but the triangle relations collapsed everything, so I'd need higher precision—mod $\pi^4$, $\pi^5$—to extract more structure. I'm also wondering if there's existing literature on a "Gleason-type theorem" for $\mathbb{Q}(i)$ that I could draw on.

I recall Hrushovski and Pitowsky's paper on generalizations of Kochen-Specker and the effectiveness of Gleason's theorem, which discusses frame functions and whether Gleason's theorem holds effectively over rational-type spaces—they seem to show some finite combinatorial obstruction related to Kochen-Specker, though I'm trying to recall the precise statement about $\mathbb{Q}^n$.

I should verify the congruence claim mod 4 with a few explicit vector examples, checking cases like $(1,1,0)$ vs $(1,-1,0)$ and $(1,1,2)$ vs $(3,1,-2)$ to see whether the parity condition on coordinates holds consistently.

Computing $g(v) = \chi_4(3) = -1$, $g(w) = \chi_4(-3) = 1$, confirming the sum is zero. The third vector from the cross product gives a $\tau$-type with $g=0$, completing another valid frame. I'm now revisiting whether $f = (1-\chi_4(ab))/3$ on $E$ matches the earlier formula $f = \frac13 + \frac13 g$.

I need to check whether the real $\mathbb{Q}^3$ analysis actually carries over to $\mathbb{Q}(i)^3$ -- specifically whether the exotic function on real projective space extends to the full complex projective plane, since real rays alone give the same orthogonality condition, but mixed frames with both real and non-real rays could impose additional constraints I haven't accounted for.

I'm examining the perpendicular plane to $(1,1,0)$, working out the involution structure in the basis given by $(1,-1,0)$ and $e_3$, trying to pin down how the perp map acts on rays $(1:z)$ within that plane.

I'm checking each parity case for $(p,q)$ systematically, verifying that the $g$-values for a primitive triple and its paired triple under the involution always sum to $-1$, confirming the identity holds across all the odd/even combinations.

Now I'm turning to the harder question of non-real $z$: here there's apparent freedom in each plane, but since a non-real ray belongs to multiple planes simultaneously, extending consistently is a genuinely global constraint. I want to search for a potential obstruction by testing whether a cycle of such constraints forces a contradiction, starting with a specific non-real ray to probe.

This gives $g(w) + g(u') = -1$, pairing each ray with its complementary partner in the orthogonal plane. I wonder if conjugation symmetry forces more structure, but rather than chase this specific example, it seems better to step back and think structurally about null functions in general—for each ray, consider the plane orthogonal to it and what constraints that imposes.

I was tempted to restrict attention to functions supported on $E_1 \cup E_2 \cup E_3$, but that's just a special property of the real exotic example—a general exotic $g$ need not vanish outside that set, so I shouldn't assume that restriction.

Instead I'm considering the lattice $\mathbb{Z}[i]^3$ with its Hermitian form, noting that its automorphism group is the finite monomial group of order 384. I'm wondering whether building exotic functions from 2-dimensional exotic examples could be a cleverer path forward.

Over $\mathbb{R}$, Gleason's theorem holds via continuity, but over $\mathbb{Q}$ exotic functions exist, as I constructed one on all of $\mathbb{Q}P^2$. I suspect similarly that exotic functions should exist over $\mathbb{Q}(i)$, since it would be strange for Gleason's theorem to hold there but fail over $\mathbb{Q}^3$, even though the orthogonality structure is denser.

I want to find a conceptual version of the real construction using primitive vectors in $\mathbb{Z}^3$, where for primitive $v$, the orthogonal complement $v^\perp \cap \mathbb{Z}^3$ forms a rank-2 lattice whose discriminant relates to $N(v)$.

I'm trying to express $g(v)$ directly in terms of the components of $v$, like $\chi_4(ab)$ for $v=(a,b,c)$ with $a,b$ odd and $c$ even, but this abstract approach isn't quite clicking, so I think I should return to the more direct local analysis while letting $g$ depend on additional data.

I'm examining the obstruction coming from the type IV triangle and related vector configurations, trying to see whether finer invariants — like tracking $a,b \bmod \pi^k$ and the extra parameter in $v=(a,b,\pi\gamma)$ — can resolve the forced vanishing $g(\delta=0)=0$ under the simple $(\kappa,\delta)$ ansatz, though I worry the constraint system will blow up in complexity.

Rather than refining the invariant further, I wonder if switching primes entirely would help: instead of the ramified prime $1+i$, I could try an inert prime like 3 (giving residue field $\mathbb{F}_9$) or a split prime like $2+i$ over 5, where conjugation swaps the two factors — this might give a cleaner structural picture via the map sending a vector to the cross product with its conjugate.

When it's inert, orthogonality collapses to the Hermitian form over $\mathbb{F}_{p^2}$ using Frobenius conjugation. When it splits, the two conjugate primes separate the pairing into a bilinear relation between reductions mod $\mathfrak p$ and mod $\bar{\mathfrak p}$, effectively pairing points in $\mathbb{P}^2$ of the residue field against each other.

For the ramified prime $1+i$ the residue field is $\mathbb{F}_2$ and conjugation becomes trivial mod $\pi$, so I'm shifting attention to the real quadratic form case. Since the exotic structure at $p=2$ was special, I'm checking whether for odd $p$ the standard form $x^2+y^2+z^2=0$ always has nontrivial solutions mod $p$, which would give isotropic points in $\mathbb{P}^2(\mathbb{F}_p)$ regardless of whether $-1$ is a square.

Ternary forms are isotropic over finite fields, so self-orthogonal vectors exist mod $p$ which degenerates the notion of a "frame" there, but for $p=2$ the form reduces to the sum of coordinates and isotropic vectors become exactly the even-weight ones like $(1,1,0)$ — the $E$-classes the real construction was built on, lifting to mod 4. Now I'm turning to $\mathbb{Z}[i]$ with the inert prime 3, considering the Hermitian form over $\mathbb{F}_9$.

I'm checking that the Hermitian curve in three variables has many isotropic points — 28 for $q=3$ — so there's a richer, more complicated structure than the simple $p=2$ case. For the split prime $p=5$ I'm trying to set up a pairing between residues modulo the two conjugate primes, and more broadly I'm weighing whether it's feasible to prove that every null function is quadratic by examining restrictions to the reals over $\mathbb{Q}(i)^3$.

A full argument would need to control values on non-real rays as well, so I'm exploring whether the real exotic solution $g$ extends consistently to all $K$-rays — if it doesn't extend, that hints toward the quadratic-only statement being true, while if it does extend, the existence result would hold instead. I'm now trying to find constraints linking real rays through a chosen non-real ray and its associated frame.

So non-real $w$ is paired with a unique $w'$ sharing the same real ray $r(w)$, satisfying $g(w)+g(w') = -g(r(w))$, since $w^\perp$ contains only one real ray and $w'$ is the remaining frame vector distinct from $r(w)$.

Now I need $g$ on non-real rays to satisfy two constraints: pairwise sums $g(w)+g(w')=-g(r)$ for shared real ray $r$, and triple sums $g(u)+g(v)+g(w)=0$ for any orthogonal frame of three rays. Frames with two real rays force the third real too, so these are the only constraints to check, and I'm now considering frames made entirely of non-real rays where $w$ relates to $u,v$ via conjugation.

I'm working out the perpendicular complement explicitly using an orthogonal basis $p, q$ of the real plane, writing $w = sp+tq$ and computing its partner $w'$ in terms of conjugates and norms, with non-reality of $w$ corresponding to $s/t \notin \mathbb{Q}$.

Non-real rays correspond to points $(s:t)$ in $\mathbb{P}^1(K)$ outside $\mathbb{P}^1(\mathbb{Q})$, with the involution sending $z=s/t$ to $-\beta/(\alpha\bar z)$. I'm now trying to understand how a frame of three non-real rays relates to the three real rays obtained by taking $r(u) = \mathrm{Re}\,u \times \mathrm{Im}\,u$ for each.

I reason that if two of these associated real rays coincided, the third ray would have to be real too, contradicting non-realness, so for a genuine non-real frame these three real rays must be pairwise distinct, though not necessarily orthogonal to each other. I want to find an obstruction -- some combination of the orthogonality constraints where the non-real unknowns cancel out, leaving a relation purely among the real $g$-values that isn't automatically satisfied.

Testing a specific construction: take a non-real frame and its complex-conjugate partner frame, both satisfying the sum-zero constraint, and combine with the pairwise relations linking each vector to its orthogonal real ray. Adding everything up, the non-real terms cancel and I get that $g$ evaluated on the three associated real rays must sum to zero -- a genuine new constraint beyond the real-frame conditions.

This gives $g(1,i,0)+g(1,-i,0) = -g(e_3) = 0$. Now I'm checking frames containing $u=(1,i,0)$ with a non-real partner other than $u'$, parametrizing $v$ in $u^\perp$ and testing which choices of $(s,t)$ make $v$ non-real, i.e. not a rational multiple of a real vector.

Since $i\in\mathbb{Q}$ would be impossible, every $v=(is,s,t)$ with $s\ne0$ is non-real, so normalizing $s=1$ gives $v=(i,1,t)$ for $t\in K^*$, and I'm computing $w=\bar u\times\bar v$ to continue building the frame.

Computing $r(u) = e_3$ and then working out $r(v)$ for $v = (i,1,t)$ by splitting into real and imaginary parts and taking their cross product, getting $(t_2, t_1, -1)$, and verifying the inner product condition $\langle v, r(v)\rangle$ holds.

Now I'm computing $r(w)$ for the paired point $w = (i, 1, s)$ with $s = -2/\bar t$, simplifying to get $r(w) \sim (2t_2, 2t_1, |t|^2)$, and setting up to find the third partner point in the configuration.

Next I'm trying to verify my construction by picking a concrete value of $t$ and checking whether the resulting triple $\{u', v', w'\}$ actually forms an orthogonal frame, starting with $u' = (i,1,0)$ and checking if $v'$ is perpendicular to it.

Computing $\langle u', v'\rangle$ I find it reduces to $\bar t(it_1 + t_2)$, which vanishes only when $t_1 = t_2 = 0$ — so this family never produces a valid frame. This pushes me toward a more structural approach: viewing non-real rays $w$ as pairs $(r, z)$ consisting of a real ray $r$ together with a coordinate $z$ in $\mathbb{P}^1(K)$ outside $\mathbb{P}^1(\mathbb{Q})$.

Rather than chasing a direct construction of a $\pi$-adic exotic function over $\mathbb{Z}[i]$ by hand, which seems too unwieldy, I want to work with reductions mod $\pi^k$. I'm setting up $R_k = \mathbb{Z}[i]/\pi^k$ and considering the set of primitive vectors over $R_k^3$ modulo units, aiming to understand this finite structure layer by layer.

I'm being careful here: since the function $g$ is defined on rays, meaning primitive vectors modulo $\{\pm 1, \pm i\}$, a function depending only on $v \bmod \pi^k$ should be invariant just under $\{\pm1,\pm i\}$, not necessarily all units of $R_k$—imposing full unit-invariance might be too strong a simplification, so I need to keep track of this subtlety as I examine how the frame condition for triples interacts with this periodicity.

Checking the actual frame condition, I see that for a frame $(u,v,w)$ of primitive vectors, knowing $v,w \bmod \pi^k$ only determines $u \bmod \pi^{k-j}$ where $j$ is the valuation of the gcd appearing in $u = \bar v \times \bar w/d$ — since $j$ can be arbitrarily large, this creates a real obstruction to defining $g$ consistently from reductions mod $\pi^k$ alone.

In the real case with $v,w \in E_3$ classes mod 2, that gcd valuation $j$ actually stayed bounded (equal to 1 or 0 depending on which basis classes $v,w$ reduced to), so I'm checking whether the orthogonality structure similarly forces $j$ bounded in this setting given the classes mod $\pi^k$.

In the complex orthogonal case, the cross product coordinates are divisible by $\pi$, and by $\pi^2$ when $\delta(v) = \delta(w)$, but the valuation can jump higher unexpectedly -- like the example giving $j=4$. This means the third vector's residue class isn't determined by $v, w$ at low precision unless the class has $g\ne 0$; when $g=0$ (the $e_3$-type case) this doesn't matter, but it's a real obstruction otherwise.

Maybe I should try the norm class invariant $\nu(v) = N(v) \bmod N(K^*)$ instead, since frames satisfy $\nu(u)\nu(v)\nu(w)=1$. Checking this on the $E_3$-triangle: norms come out to 2, 4, 4, and I'm checking whether 2 lies in the norm group by testing against $|1+i|^2$ type expressions.

Actually the key distinguishing feature seems to be real versus non-real rays rather than the norm class, since $(1,1,0)$ is real while $(1,-1,\pi)$ isn't, and I know $g(1,1,0)=1$ with $g(1,-1,\pi)+g(1,-1,-\pi)=-1$. So I'm trying a new definition: for a non-real ray $w$, tie $g(w)$ to the value at its canonical real counterpart $r(w)$, setting $g(w) = -\frac12 g(r(w))$ given that $w$ lies in $r(w)^\perp$.

This automatically satisfies the pairing constraint, since $g(w)+g(w') = -g(r(w))$ holds by construction. The real question becomes whether the triple-sum constraint $g(r_u)+g(r_v)+g(r_w)=0$ holds for a non-real orthogonal frame $\{u,v,w\}$, where $r_u, r_v, r_w$ are the corresponding real rays — so I'm testing this against my earlier parametrized family of frames to check if it actually holds.

Computing $r_w = (0,2,1)$ gives $g=0$, but the sum $-1+0 \ne 0$, so this simple ansatz fails. I need to reconsider: maybe $g$ should take the form $g(w) = -\frac12 g(r(w)) + h(w)$ with $h(w)+h(w')=0$, and I should step back to think about whether exotic null functions even exist on $\mathbb{P}(K^3)$ at all.

Let me try restricting to real rays: if $g$ is null on $K$-rays, its restriction to real rays must be null on $\mathbb{Q}P^2$ with extra constraints. For a non-real ray $u$ with real partner $r$, I'm examining which frames contain $u$ alongside $r$ and its complex conjugate $u'$ to pin down what these constraints actually look like.

Proving Gleason over $\mathbb{Q}(i)^3$ outright seems very hard, so a partial result -- the largest piece I can honestly establish -- may be the realistic target here. I still want to get a heuristic sense of which way the truth points before committing to that approach.

Looking at the standard proof structure (Cooke–Keane–Moran) for $\mathbb{R}^3$, it relies on continuity arguments for frame functions on the sphere that don't obviously transfer to $\mathbb{Q}(i)$, since there's no natural topology there and the problem doesn't even require nonnegativity -- our exotic example already takes rational values like $0, 1/3, 2/3$, which suggests the usual continuity machinery won't directly apply.

Since in dimension 2 exotic frame functions trivially exist and I've now constructed one over $\mathbb{Q}$ in dimension 3, I suspect something exotic also exists over $\mathbb{Q}(i)$, though its richer orthogonality structure makes this less obvious. A dimension-counting heuristic doesn't help here since both the unknowns (ray values) and constraints (frames) are infinite, so I need to think more carefully about actually constructing an exotic function over $\mathbb{Z}[i]$.

I'm trying a $\mathbb{Z}/2$-cocycle style construction using a character on the product of coordinates, and analyzing how orthogonal vectors in this lattice project onto $\mathbb{P}^1(\mathbb{Q})$ modulo small integers, looking at how points cluster under the orthogonality congruence.

I'm extending this to the complex case, comparing how many points lie over a given base point in $\mathbb{P}^1$ for different moduli $R_3$ and $R_4 = \mathbb{Z}[i]/4$, and working out the analogous orthogonality relation involving complex conjugates.

Trying a sharper ansatz: letting $g$ depend on $u = a^{-1}b \bmod 4$ where $a$ is invertible since it's odd, and checking that this ratio is invariant under simultaneous unit scaling of $a$ and $b$.

Now I'm dividing the orthogonality relation through by $\bar a a'$ to express it purely in terms of these ratios $u, u'$ and the corresponding relation for $\gamma$, trying to see if a consistent dependence on $u \bmod 4$ emerges.

I'm working out a cleaner set of invariants for $v$: $u(v)=a^{-1}b \bmod 4$ taking 8 possible values, a binary $\delta(v)$, and when $\delta=0$ an auxiliary $\theta(v)\in\{1,i\}$ given by $\gamma a^{-1}\bmod 2$. Now I'm trying to pin down the orthogonality relation these invariants must satisfy in $E_3$, splitting into cases depending on whether $\delta(v)$ or $\delta(w)$ equals 1.

I'm parametrizing $u = i^m(1+2i)^n$ using the group structure $R_4^* = \langle i\rangle \times \langle 1+2i\rangle$, then computing $\bar u u' = i^{m'-m}(1+2i)^{n+n'}$ and checking the condition when $\delta(v)=1$ or $\delta(w)=1$.

From matching conditions across cases, I identify that $m$ corresponds to $\kappa$ from the earlier mod $\pi^3$ analysis, while $n$ and $\theta$ carry new information. Now I need to work out when the third vector lands in $E_3$ based on its invariants.

I initially thought $\delta(v)\ne\delta(w)$ was both necessary and sufficient, but I need to double check the "only if" direction—if $\delta(v)=\delta(w)=0$, could the third vector still have $\delta=0$ and lie in $E_3$? That would require checking whether a $(0,0,0)$ triangle of pairwise orthogonal vectors actually exists.

Tracing through the refined rules, if two of the three vectors share $\theta$ then their $m,n$ match, and the third either matches too or shifts by $(+2,+1)$ depending on whether its $\theta$ differs—so I need to see if a consistent triangle can actually form this way.

I'm now trying a concrete example with $v=(1,1,\pi)$ and seeking a matching $w$ with odd $\gamma'$ satisfying the sum constraint, then computing the cross-product vector $u = \bar v \times \bar w$ component by component to check consistency.

Substituting gives $u_1 = \bar\pi\overline{(3+a')}$ and $u_2 = \bar\pi\overline{(a'-1)}$. I'm checking the valuation conditions for membership in $E_3$ with $\delta=0$, requiring $v_\pi(u_1) = v_\pi(u_2) = j$ and $v_\pi(u_3) = j+1$, which translates into valuation conditions on $3+a'$, $a'-1$, and $1+a'$ given that $a'$ is odd.

Checking whether $v_\pi(a'+1) = v_\pi(a'-1)$ is achievable: working through the cases for $v_\pi(a'-1) = 1$, $2$, or $\geq 3$, I find the two valuations never match — they're always off by at least one. So this particular configuration with $\gamma'=1$ doesn't work out.

Let me try $\gamma'$ odd instead, expressing $b'$ in terms of $a'$ and $\gamma'$ via $a'+b'=-2\gamma'$, and computing the residues $u_1$, $u_2$, $u_3$ in terms of $a'$ and $\gamma'$ to see if a valid triangle emerges.

Working out valuations: since $a'+3\gamma' = (a'-\gamma')+4\gamma'$ and $a'+\gamma' = (a'-\gamma')+2\gamma'$ with $\gamma'$ odd, I'm checking whether assuming $v(a'-\gamma')=1$ forces $v(a'+\gamma')\ge 2$ and $v(a'+3\gamma')=1$, matching the same pattern as before.

But when $\delta(v) = \delta(w) = 1$, the third vector can't be type IV with two $\delta=1$ entries, so it's excluded from $E_3$. Let me redo the case analysis systematically for $v \perp w$ in $E_3$: case (a) both $\delta=1$ excludes third from $E_3$ with relation $m'=m+2, n'=n$; case (b) $\delta(v)=1,\delta(w)=0$ gives third in $E_3$ with $\delta=0$, type IV $(1,0,0)$, and I'm working out the relation for $m'$.

Now for cases (c) and (d) where both $\delta(v)=\delta(w)=0$ — splitting by whether $\theta=\theta'$ or not — I need to determine whether the third vector lands in $E_3$ with $\delta=1$, or falls outside $E_3$ entirely as an $e_3$ or $\tau$-type vector, since it must be orthogonal mod $\pi$ to the $\epsilon_3$-class vectors.

Looking at a triangle with pattern $(1,0,0)$: if $u$ has $\delta=1$ and $v,w$ have $\delta=0$, then both $(u,v)$ and $(u,w)$ fall under case (b), forcing $m_v=m_w$ and $n_v=n_w$. That means $(v,w)$ must fall under case (c) with $\theta_v=\theta_w$ — so in case (d) the third vector can never lie in $E_3$, while in case (c) it may or may not. Now I need to pin down the $m,n$ values of the third vector in case (b) itself.

I'm setting up an ansatz where $g(v)=\phi(m,n)$ when $\delta=1$ and $g(v)=\psi(m,n,\theta)$ when $\delta=0$, then working through the resulting functional constraints from cases (a) and (b).

Combining these shows $\psi(m,n,\theta)=\phi(m,n)/2$, independent of $\theta$, and then case (c), where the third vertex falls outside $E_3$, forces $\psi(m,n,\theta)=0$ entirely.

Tracking how these monomial matrices act on the invariants: shifting coordinates by $i^k$ changes $m$ and $\theta$ but seems to leave $n$ fixed, since swapping coordinates inverts $u$ while preserving $n$. That suggests $n$ is invariant under this unitary group, though I should check whether unitaries over a larger ring could change that.

This unitary maps $(1,1,0)$ to something equivalent to $e_1$, so it doesn't preserve $E_3$ -- but that's fine since I just need explicit examples showing (c)-pairs with third coordinate outside $E_3$ for each $(m,n,\theta)$. Checking the $n=1$ case now, trying $a=1$, $b=1+2i$ to construct such a $v$.

If every $(m,n,\theta)$ admits such a pair, then $\phi(m,n)=0$ follows and $g$ vanishes identically. So I need to pin down exactly when the third coordinate of a (c)-pair lands in $E_3$ versus not, examining the structure of pairs $v=(a,b,\pi\gamma)$ and $w=(a',\ldots)$ more closely.

I'm working out the condition more carefully: the third element lands in $E_3$ precisely when $v(u_1)=v(u_2) < v(u_3)$, and otherwise it must instead be orthogonal mod $\pi$ to the earlier elements, placing it in a different type.

