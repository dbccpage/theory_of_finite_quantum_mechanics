# Hypothesis Ledger for Relational Algebra & Database Theory

**Domain Key:** `ansi_sql`  
**AuthorityEffect:** `None`  

Statuses below refer to the stated models, not to the frozen Genesis source or a Python/Lean equivalence. See the [publication review](../../publication_review.md) for current executions.

| hypothesis_id | statement | verification_method | invalidation_criterion | status |
| --- | --- | --- | --- | :---: |
| `hyp_ansi_sql_germ_distinctness` | The primitive difference pair $(a, b)$ with $r a b$ and $\neg r a a$ strictly separates $a \neq b$. | Lean 4 proof (`irrefl_distinct`) and Python assertion. | An instance where $a = b$ satisfies $r a b \wedge \neg r a a$. | `VERIFIED` |
| `hyp_ansi_sql_transposition_sign` | Transposition operator $\sigma(a, b) = (b, a)$ satisfies boundary sign inversion $\partial_1(\sigma(e)) = -\partial_1(e)$ in SQL views. | SQLite query over `view_boundary_sign_inversion`. | Any vertex where $\text{net\_sum} \neq 0$. | `VERIFIED` |
| `hyp_ansi_sql_check_constraint_irrefl` | SQL table check constraint `CHECK (src <> dst)` blocks reflexive loops at database engine level. | SQLite `INSERT INTO difference_relations VALUES ('a', 'a', 1)` raising `IntegrityError`. | An instance where a self-loop $(a, a)$ is inserted without error. | `VERIFIED` |
| `hyp_ansi_sql_bareiss_exactness` | Bareiss fraction-free elimination computes exact integer determinants over $\mathbb{Z}$ with zero division remainder. | Python integer assertions on Sylvester quotient division. | Any Bareiss reduction step producing non-zero remainder on division by previous pivot. | `VERIFIED` |
| `hyp_ansi_sql_redheffer_mertens` | The determinant of Redheffer matrix $R_n$ identically equals the Mertens function $M(n)$ for all $n \ge 1$. | Bareiss determinant evaluation vs exact arithmetic Mertens sum. | Any $n$ where $\det(R_n) \neq M(n)$. | `VERIFIED` |
| `hyp_ansi_sql_gin_fermion_sign_pairing` | GIN index inverted posting list pairing between configuration $C$ and involution partner $\Xi(C)$ produces exact weight-preserving sign cancellation. | SQLite query over `view_gin_fermion_cancellation`. | Any involution pair where $\text{net\_weight} \neq 0$. | `VERIFIED` |
| `hyp_ansi_sql_boundary_closure` | Discrete boundary operators over relational chains satisfy $\partial^2 = 0$. | Python combinatorial simulation. | Any non-vanishing boundary sum along closed simplicial cycles. | `VERIFIED` |
| `hyp_ansi_sql_gap_obstruction` | `ThreeValuedNullObstruction` is a legacy scenario label, not a proved impossibility result. | The former fixed-root predicate is now characterized exactly by `every_endomap_fixes_root_iff`. | A verified domain-specific theorem would need explicit assumptions and a faithful model bridge. | `WITHDRAWN_AS_THEOREM` |
