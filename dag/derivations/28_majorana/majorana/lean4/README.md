# Lean 4 Formalization: The Majorana Problem (PO-026)

**Package:** `po026`  
**Toolchain:** `leanprover/lean4:v4.35.0`  
**Authority:** `AuthorityEffect: None`  

## Module Structure

- `MajoranaCore`: Formal mechanization of binary field $\mathbb{F}_2$ operations, vector weights, linear maps, finite cochain complexes, boundary nilpotency implications, trichotomy exclusivity (`exact_not_open`), $\ell^1 / \ell^2$ binary weight coincidence (`f2_weight_l1_l2_coincide`), and 1D Kitaev sweet-spot boundary Majorana zero mode decoupling (`mzm_boundary_decoupling`).
- `MajoranaGinCore`: Formal mechanization of Generalized Inverted Index (GIN) cochains for the Fermion Sign Problem and Majorana Zero Mode boundaries, including involution sign cancellation (`involution_pair_cancels_sign`), boundary mode decoupling ($\gamma_1$ and $\gamma_{2L}$ disjoint from bulk pairing bonds), and BQNF terminal routing (`evaluate_gin_fermion_recovery`).

## Building the Package

```bash
lake build
```

Requires Lean 4.35.0. Builds in under 2 seconds with zero external network dependencies, zero unproved `sorry` placeholders, and zero synthetic axioms.
