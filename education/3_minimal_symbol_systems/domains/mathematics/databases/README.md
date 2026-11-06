# Relational Database Schemas: Discrete Mathematics & Simplicial Homology

**Directory:** `coda_all_universe/1_the_tower/2_mathematics/databases/`  
**Status:** LAB APPARATUS  
**AuthorityEffect:** None  
**Primary Formal Reference:** `sealed-derivation-v1` (`3100c4e`)  

---

## 1. Directory Contents

This directory serves as the designated repository for relational database schemas, DDL scripts, and SQL representations of discrete mathematical structures within Domain 2 (`2_mathematics`):

- **Simplicial Boundary Complexes:** Relational representation of finite abstract simplicial complexes $K$, storing oriented $k$-simplices $\sigma = [v_0, \ldots, v_k]$ and incidence matrices $\partial_k$.
- **Smith Normal Form (SNF) & Torsion:** Relational algebraic tables capturing integer row/column operations $S = U A V$ over $\mathbb{Z}$, invariant factors $d_i \mid d_{i+1}$, and discrete torsion subgroups $\mathbb{Z} / d_i \mathbb{Z}$.
- **Bareiss Fraction-Free Elimination:** SQL CTE specifications mirroring fraction-free Gaussian elimination for computing exact homology ranks $\beta_k = \dim \ker \partial_k - \mathrm{rank}\, \partial_{k+1}$.

---

## 2. Relational Schema Specification Blueprint

```sql
-- Finite Abstract Simplicial Complex Table
CREATE TABLE IF NOT EXISTS simplicial_k_faces (
    complex_id TEXT NOT NULL,
    dim_k INTEGER NOT NULL,
    simplex_id TEXT NOT NULL,
    vertices_json TEXT NOT NULL, -- sorted tuple [v_0, ..., v_k]
    orientation INTEGER NOT NULL CHECK (orientation IN (-1, 1)),
    PRIMARY KEY (complex_id, dim_k, simplex_id)
);

-- Simplicial Boundary Operator Matrix Entries
CREATE TABLE IF NOT EXISTS boundary_operator_matrix (
    complex_id TEXT NOT NULL,
    dim_k INTEGER NOT NULL,
    row_k_minus_1 TEXT NOT NULL,
    col_k TEXT NOT NULL,
    incidence_coeff INTEGER NOT NULL, -- (-1)^i
    PRIMARY KEY (complex_id, dim_k, row_k_minus_1, col_k)
);

-- Smith Normal Form Invariant Subgroup Register
CREATE TABLE IF NOT EXISTS smith_normal_form_factors (
    complex_id TEXT NOT NULL,
    dim_k INTEGER NOT NULL,
    factor_index INTEGER NOT NULL,
    invariant_factor INTEGER NOT NULL CHECK (invariant_factor >= 1),
    is_torsion BOOLEAN NOT NULL, -- invariant_factor > 1
    PRIMARY KEY (complex_id, dim_k, factor_index)
);
```

---

## 3. Claim Hygiene Ledger

1. **What this supports:**  
   Structured relational storage of discrete simplicial structures, boundary operator incidence matrices, and integer homology torsion invariants.
2. **What this does not support:**  
   Continuous differential geometry, non-computable infinite chain complexes, or topological invariants beyond finite simplicial sets.
3. **The narrowest defensible claim:**  
   Finite abstract simplicial complexes and their boundary matrices can be losslessly represented in 1NF relations, with exact homology groups computable via integer matrix transformations.
4. **The next test needed:**  
   Execute cross-domain bisimulation receipts verifying bijection between `lean4/simplicial_complex.lean` and SQLite table queries.
