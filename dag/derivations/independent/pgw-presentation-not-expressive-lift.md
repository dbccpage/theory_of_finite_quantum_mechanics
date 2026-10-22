Status: AI-drafted, awaiting human review.

# Derivation Note: Inscription Non-Injectivity Under Opaque Convention (PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT / TFQ-0422)

**AuthorityEffect:** None.  
**Node ID:** `PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT`  
**TFQ ID:** `TFQ-0422`  
**Stage:** `PREGENESIS`  
**Outcome Class:** `Derived`

---

## 1. Statement and Target

The target statement asserts:
> "Write $P$ for the presented inscriptions and $O$ for the internal observations. Supplying $\langle a \rangle$ after $\langle\rangle$ changes $P$ from $\{\langle\rangle\}$ to $\{\langle a \rangle\}$ and leaves $O_1 = O_0 = \emptyset$, so no new internal distinction is available. With $q : P \to N$ sending an inscription to the distinctions the regime has, $x \neq y$ in $P$ can hold while $q(x) = q(y)$ in $N$, so a new presentation does not imply a new internal class, and in the other direction $q(x) = q(y)$ does not imply $x = y$. Under the opaque convention $\langle a \rangle$ is a new presentation state in the same internal class as $\langle\rangle$; the statement holds under that convention only."

This note provides an exact, constructive mathematical derivation of this statement, establishing the outcome as **Derived**.

---

## 2. Mathematical Formalization

### 2.1. Presentation Space and Syntactic Enlargement
Let $P$ denote the alphabet or space of presented inscriptions. In the minimal pre-genesis setting, consider the canonical inscriptions:
- $x_0 = \langle\rangle$ (the inert root inscription, or empty payload `nil`),
- $x_1 = \langle a \rangle$ (an inscription carrying a token or payload `markA`).

Syntactically, these inscriptions are distinct:
$$x_0 \neq x_1$$
Initially, the presentation set contains only the root inscription:
$$P_0 = \{x_0\} = \{\langle\rangle\}, \quad |P_0| = 1$$
Upon supplying $\langle a \rangle$, the presentation set expands to include both inscriptions:
$$P_1 = \{x_0, x_1\} = \{\langle\rangle, \langle a \rangle\}, \quad |P_1| = 2$$
Because $x_1 \notin P_0$ and $x_1 \in P_1$, we have a strict syntactic enlargement:
$$P_0 \subset P_1$$

### 2.2. Internal Observations in the Unformed Regime
An internal regime $r$ possesses an inventory of admitted distinction predicates or form instances. For any presented inscription $x \in P$, let $O(x)$ denote the set of internal distinctions / form instances satisfied by $x$.

In the unformed / pre-genesis regime prior to the admission of any forms (e.g. $r = \langle 2, [], [], [], [] \rangle$ with data count 2 and empty forms list), no form instances exist. Consequently, the internal distinction sets are identically empty:
$$O_0 = O(x_0) = \emptyset$$
$$O_1 = O(x_1) = \emptyset$$
Therefore:
$$O_1 = O_0 = \emptyset$$
The set of new internal distinctions introduced by presenting $\langle a \rangle$ is given by the set difference:
$$O_1 \setminus O_0 = \emptyset \setminus \emptyset = \emptyset$$
No new internal distinction is available to the regime upon supplying $\langle a \rangle$.

### 2.3. The Distinction Quotient Map $q : P \to N$
Define the distinction map $q : P \to N$ sending each presented inscription $x \in P$ to its distinction profile in the space $N$ of available internal distinctions (or the canonical quotient space of $P$ modulo observational indistinguishability):
$$q(x) := O(x)$$
Evaluating $q$ on $x_0$ and $x_1$:
$$q(x_0) = \emptyset, \quad q(x_1) = \emptyset \implies q(x_0) = q(x_1)$$
Since $x_0 \neq x_1$, the pair $(x_0, x_1)$ is a witness to the simultaneous satisfaction:
$$x_0 \neq x_1 \quad \text{and} \quad q(x_0) = q(x_1)$$

From this explicit witness, two logical non-implications follow immediately:
1. **New presentation does not imply new internal class:**
   $$\neg \Big(\forall x, y \in P, \; x \neq y \implies q(x) \neq q(y)\Big)$$
   (i.e., $q$ is strictly not injective).
2. **Identical internal class does not imply identical presentation:**
   $$\neg \Big(\forall x, y \in P, \; q(x) = q(y) \implies x = y\Big)$$
   (i.e., fibers of $q$ are not singletons).

---

## 3. The Role of Identity Conventions

The derivation statement explicitly conditions the collapse behavior on the choice of identity convention:
> "Under the opaque convention $\langle a \rangle$ is a new presentation state in the same internal class as $\langle\rangle$; the statement holds under that convention only."

We formalize both conventions as equivalence relations on $P$:

### 3.1. Opaque Identity Convention
Under the opaque convention, an internal state is defined solely by what the regime's observation apparatus can distinguish. Two inscriptions are identified if they share identical distinction profiles:
$$x \sim_{\text{opaque}} y \iff O(x) = O(y) \iff q(x) = q(y)$$
Since $O(x_0) = \emptyset = O(x_1)$, we have:
$$x_0 \sim_{\text{opaque}} x_1$$
Thus, in the quotient space $N_{\text{opaque}} = P / \sim_{\text{opaque}}$:
$$[x_0]_{\text{opaque}} = [x_1]_{\text{opaque}}$$
The quotient space has cardinality:
$$|N_{\text{opaque}}| = 1$$
Here, $\langle a \rangle$ is a new presentation inscription ($x_1 \neq x_0$) that collapses into the same internal class as $\langle\rangle$. Distinct presentations collapsing into a single internal class **does hold** under this convention.

### 3.2. Exact-Inscription Convention
Under the exact-inscription convention, state identity is syntactic identity on the presented tokens themselves:
$$x \sim_{\text{exact}} y \iff x = y$$
Under this convention:
$$x_0 \not\sim_{\text{exact}} x_1 \quad (\text{since } \langle\rangle \neq \langle a \rangle)$$
The quotient space $N_{\text{exact}} = P / \sim_{\text{exact}} \cong P$ retains cardinality:
$$|N_{\text{exact}}| = |P| = 2$$
The canonical projection $q_{\text{exact}}$ is the identity map, which is strictly injective:
$$q_{\text{exact}}(x) = q_{\text{exact}}(y) \implies x = y$$
Consequently, under the exact-inscription convention, two distinct presentations can **never** share an internal class:
$$\neg \Big(\exists x, y \in P, \; x \neq y \land x \sim_{\text{exact}} y\Big)$$

### 3.3. Convention Characterization Theorem
Define the property $\mathrm{HasCollapse}(c)$ that distinct presentations exist which share an internal class under convention $c \in \{\text{opaqueConv}, \text{exactInscription}\}$:
$$\mathrm{HasCollapse}(c) \iff \exists x, y \in P, \; x \neq y \land x \sim_c y$$
We have proven:
1. $\mathrm{HasCollapse}(\text{opaqueConv})$ is True (witnessed by $(x_0, x_1)$).
2. $\mathrm{HasCollapse}(\text{exactInscription})$ is False (since $x \sim_{\text{exact}} y \implies x = y$).
Therefore, the equivalence:
$$\mathrm{HasCollapse}(c) \iff c = \text{opaqueConv}$$
holds unconditionally. The collapse statement holds under the opaque convention **only**.

---

## 4. Connection to Genesis Regime Replay

In `lean4/GenesisComputation.lean` and `lean4/CampaignPgwPresentationLift.lean`, a regime with 2 data marks and no forms ($r = \langle 2, [], [], [], [] \rangle$) is defined.
A unary separation between data $i$ and $j$ requires the existence of a form index $f < \mathrm{length}(r.\mathrm{forms}) = 0$. Since no natural number is strictly less than 0, no separating form exists:
$$\forall i, j, \; \neg \mathrm{UnarySep}(r, i, j)$$
Thus, both $\mathrm{UnarySep}(r, 0, 1)$ and $\mathrm{UnarySep}(r, 1, 0)$ are false, which proves:
$$\mathrm{Collapsed}(r, 0, 1)$$
This constructively confirms the unformed mark collapse theorem (`two_marks_without_forms_collapsed`), verifying that until unary forms are admitted, distinct marks are indistinguishable to the internal regime.

---

## What is proved

1. **Syntactic Growth**: Presentation sets $P_0 = \{\langle\rangle\}$ and $P_1 = \{\langle\rangle, \langle a \rangle\}$ satisfy $|P_0| = 1$, $|P_1| = 2$, and $P_0 \subset P_1$.
2. **Distinction Absence**: Internal observation profiles in an unformed regime satisfy $O_0 = \emptyset$, $O_1 = \emptyset$, $O_1 = O_0$, and $O_1 \setminus O_0 = \emptyset$.
3. **Non-Injectivity of $q$**: The distinction map $q : P \to N$ satisfies $x_0 \neq x_1$ and $q(x_0) = q(x_1)$.
4. **Logical Non-Implications**:
   - $\neg (\forall x y : P, x \neq y \implies q(x) \neq q(y))$ (a new presentation does not imply a new internal class).
   - $\neg (\forall x y : P, q(x) = q(y) \implies x = y)$ (equal internal distinction does not imply identical presentation).
5. **Opaque Collapse**: Under `opaqueConv`, $[x_0] = [x_1]$ in $N_{\text{opaque}}$, and $|N_{\text{opaque}}| = 1$.
6. **Exact Non-Collapse**: Under `exactInscription`, $x \sim y \implies x = y$, so $[x_0] \neq [x_1]$ and $|N_{\text{exact}}| = 2$.
7. **Convention Characterization**: Distinct presentations share an internal class if and only if the identity convention is `opaqueConv`.
8. **Genesis Unformed Regime**: Two marks in an unformed regime ($0$ forms) are constructively proven collapsed.
9. **Full Lean 4 Formalization**: All above theorems are proved in `lean4/CampaignPgwPresentationLift.lean` and verified under Lean 4.35.0 with zero `sorry`, zero `admit`, zero custom `axiom`, and axioms in $\{propext, Classical.choice, Quot.sound\}$.
10. **Independent SymPy Verification**: All cardinalities, non-implications, and quotient structures are verified in `checks/independent/pgw-presentation-not-expressive-lift.py` with zero repository imports.

---

## What is assumed

1. **Declared Identity Convention**: The distinction between opaque and exact-inscription identity is a declared foundational assumption of Pre-Genesis, not derived from prior primitives (consistent with `PGW-IDENTITY-CONVENTION-UNDECIDABLE`).
2. **Unformed Starting Point**: The initial pre-genesis regime has admitted no discriminating forms ($r.\mathrm{forms} = []$), so observation profiles are initially empty.

---

## What is open

1. **Dynamic Inscription Learning**: Modeling the operational process by which a regime transitions from an unformed state to admitting forms that lift the collapse of specific presentation inscriptions.
2. **Higher-Arity Context Distinctions**: The present result covers unary distinctions and empty profiles; extending the exact quotient classification to arbitrary $k$-ary relational forms in the full Genesis event calculus.
