---
documentation_contract: symbol-game-documentation/v1
title: "Lesson 750.01: The Three Prime Algorithms Triad Architecture and Primitives"
kind: pedagogical-lesson
track: 750_three_prime_algos_foundations
status: active
maturity: production
claim_status: verified
authority_effect: "None"
source_paths:
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/mod.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_0.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_1.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_algorithm_2.rs
  - omega_engine/crates_rs/omega_wdp/src/prime_algos/prime_scope.rs
---

# Lesson 750.01: The Three Prime Algorithms Triad Architecture and Primitives

**AuthorityEffect:** None. Complete mathematical and algorithmic specification of the Prime Triad Architecture; no authorization is conferred.  
**Track:** `750_three_prime_algos_foundations`  
**Topic:** Prime Triad stages {-1, 000, 001, 002}, 12-step obstruction fill, scale descent loss ledgers, and licensed structural lift.

---

## 1. Pedagogical Objective

Master the four sequential protocol stages of **The Three Prime Algorithms** (Prime -1, Prime 000, Prime 001, Prime 002), understanding how carrier honesty, exact coboundary repair, scale descent, and licensed structural lift operate in lockstep without ungrounded coordinate creation or universal authority claims.

---

## 2. The Four Protocol Stages of the Prime Triad

In `omega_wdp::prime_algos`, the Prime Triad is structured into four sequential protocol stages:

| Stage | Name | Role & Invariant | Governing Module |
| :---: | :--- | :--- | :--- |
| **Prime -1** | **Carrier Honest Initialization** | Sizing carrier capacity $C$, coordinates $K$, and verifying non-empty basis honesty without shadow coordinates. | `prime_scope.rs` |
| **Prime 000** | **Obstruction Fill (12 Steps)** | Exact local coboundary repair; systematically eliminates boundary obstructions on local star neighborhoods. | `prime_algorithm_0.rs` |
| **Prime 001** | **Scale Descent & Loss Ledger** | Coarse-graining state to lower dimension while recording every dropped coordinate in an immutable loss ledger. | `prime_algorithm_1.rs` |
| **Prime 002** | **Dialectical Gauge Break & Lift** | Evaluates harmonic residual and licenses carrier dimension lift only under an authenticated context contract. | `prime_algorithm_2.rs` |

---

## 3. Coordinate Conservation and Loss Ledger Discipline

During scale descent (Prime 001), high-frequency coordinates are coarse-grained out of the active carrier. To prevent epistemic loss:
$$\dim(C_{\mathrm{in}}) = \dim(C_{\mathrm{coarse}}) + |\mathcal{L}_{\mathrm{loss}}|$$

Every dropped degree of freedom is appended to an append-only loss ledger $\mathcal{L}_{\mathrm{loss}}$ with its coordinate index, exact rational valuation, and descent context hash.

---

## 4. Check for Understanding

1. Why must Prime -1 verify carrier honesty before any computation begins?
2. How does the 12-step obstruction fill (Prime 000) resolve local boundary defects without expanding the carrier?
3. What prevents Prime 002 from arbitrarily expanding carrier dimension when faced with an apparent obstruction?

---

## 5. Laboratory Workbench

- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_750_01_prime_triad_architecture.ipynb)
