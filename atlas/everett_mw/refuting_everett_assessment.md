# Can Everett be refuted? What a decisive result would have to look like

Working note, 2026-11-02, revision 3 (after independent refereeing: [referee_report_2026-11-02.md](referee_report_2026-11-02.md)). Builds on [`everett_from_weights_math_only.md`](everett_from_weights_math_only.md), cited as EW.

## 0. What turns on what

Write a theory as dynamics plus a predictive map Pred: (Ψ, U, {F_k}) ↦ p_k = Tr(ρ U†F_k U) (EW(5.1)), plus an **observer-selection rule** saying which outcome a given observer should expect. Everett = universal unitary dynamics + Born map + a branch-relative selection rule + the predicate W ("the emergent, decohered structures are worlds").

> **Lemma 0 (conditional).** Two theories that share dynamics, observables, preparations, the Born map and the observer-selection rule, and differ only by a predicate W that enters none of these, are empirically indistinguishable. EW(5.2) is the instance.

This is a tautology about a fixed Pred, and that is its use: it says where a refutation must aim. Everett is refuted empirically only if one of its *shared* components fails: (i) unitarity, (ii) the Born map, or (iii) its selection rule. It can be refuted mathematically only by showing a *precise* formulation is inconsistent, ill-defined, or incompatible with another accepted structure (Lorentz covariance, AQFT subsystem structure, a theory of records). An interpretation defined to add no predictive content and free to revise its own formulation cannot be refuted by anything; a precise formulation can.

Finiteness plays no role in any of this.

## 1. Route A: empirical

| Component | What would refute it | State of play |
|---|---|---|
| (i) unitarity, closed systems | A closed-system collapse generator (CSL with (λ, r_C), regularized Diósi–Penrose) confirmed against all environmental noise | Matter-wave interference to ~25 kDa (Fein et al., Nat. Phys. 2019); DP regularization constrained to R_0 ≳ 0.54 Å (Donadi et al., Nat. Phys. 2021); CSL squeezed, not closed |
| (i) unitarity, gravity | Fundamentally classical gravity coupled to quantum matter (Oppenheim, PRX 2023; decoherence–diffusion trade-off, Nat. Commun. 2023) | Testable; would refute *universal-unitary* Everett. A non-unitary branching theory could still call itself many-worlds |
| (ii) Born map | Statistically robust Born-rule deviations | Would refute Everett+Born without touching unitarity (non-equilibrium Bohm shows the logical space) |
| (iii) selection rule | A uniqueness theorem for observer-selection kernels p(o \| Ψ, observer data) that excludes Everett's | Open; Sebens–Carroll, Greaves–Myrvold, Saunders, Kent, Vaidman give incompatible rules. Mathematical, and **could change Pred** |

Corrections from the review: a Kraus dephasing channel (EW(5.3)) has a unitary dilation and is **not** evidence of fundamental non-unitarity. Absence of gravitationally induced entanglement would not refute unitarity (weak coupling, ordinary decoherence, calibration); its presence supports Everett no more than Bohm. Frauchiger–Renner (universal validity, consistency, single outcomes) and Local Friendliness (absoluteness, locality, free choice) are different theorems; neither singles out Everett, and nonlocal Bohmian mechanics survives both.

The Nobel pattern (Aspect–Clauser–Zeilinger 2022) is: theory turns a dispute into an inequality or scaling law, then an experiment. Route A is that pattern; the discovery itself is outside a theorist's control.

## 2. Route B: precise formulations

**B1. Exact branches.** A no-go for exact, permanently stable, covariant branch maps would refute only exact-branch Everett, which no one defends (Wallace's branches are emergent and approximate). The statement still needs definitions of "branch", "stable", "generic"; exact permanence fails trivially in finite closed systems by recurrence. Dowker–Kent (1996) gave set-selection problems for consistent histories, not this theorem. Cotler–Penington–Ranard (2019) fix a local factorization from the spectrum only under a local-Hamiltonian ansatz and genericity. Related: quantum-Darwinism uniqueness and Lorentz-covariant branching in type-III AQFT; no accepted no-go exists for either.

**B2. Probability: classified in its core form (this revision).** *Status: argument sketch from the referee exchange (referee report §3). Only the item-5 witness is machine-checked (`check_conjugate_measure.py`); items 1–4 are not yet written out in full or formalized.* In the measure-theoretic core of Deutsch–Wallace over a conjugation-closed field K ⊆ ℂ (certainty/nullity, positivity, finite additivity / branching indifference, K-unitary covariance, measurement neutrality with K-ancillas, multiplicative composition; **no continuity axiom**):

1. **Equivalence is derived.** Equal Hilbert weight ⇒ equal value, by Witt extension of Gram-preserving isometries plus covariance.
2. **Rational weights are forced to Born** by exact equal-cell fine-graining (the rational lemma; cf. EW(4.6) and `RationalSector.rational_finegraining_exists`).
3. **K = ℚ or ℚ(i): Born is forced without continuity.** Every weight is rational.
4. **K real closed (e.g. real algebraic numbers) or its complexification: Born is forced without continuity**, by a rational order squeeze (unique ordering).
5. **K with a second real embedding: Born is not forced.** Over ℚ(√2), μ_ψ(P) = σ(⟨ψ,Pψ⟩) with σ: √2 ↦ −√2 satisfies every axiom and is non-Born. Witness a = (−3−8√2)/17, c = (12−2√2)/17, a² + c² = 1, a² ≈ 0.709 but σ(a²) ≈ 0.239. Realizable weights are exactly the totally positive ones (sums of squares), so σ never goes negative. Checked exactly: `check_conjugate_measure.py`.

**What this means.** The exotic ℚ³ frame function is not a counterexample: it never takes the value 1, so it fails pure-state certainty, and 0/1 colourings fail the rational lemma. If items 3–4 hold as sketched, the suspicion that "Born enters through continuity" is **false** over ℚ, ℚ(i) and real-closed fields. The physically contestable premise is **branching indifference / measurement neutrality**. Item 5 is the genuine residue: Born uniqueness needs one extra datum, *which real embedding (order) of the scalar field is physical*. The conjugate measure is Born in the conjugate embedding, so it is a Galois relabelling rather than new physics. It bears on every symmetry-based derivation of Born (Gleason included), not on Everett specifically.

Honest verdict on B2: **it does not refute Everett. Its core supports Everett's probability derivation**, given branching indifference. What remains to attack is branching indifference itself, which is a normative premise about rational agents, not a mathematical one.

**B3. Further mathematical targets with some bite.** Continuum branching and unbounded utilities (whether Wallace's preferences extend without St. Petersburg pathologies); personal identity and confirmation (no branch-relative confirmation rule meeting stated constraints). Each could invalidate a *derivation*; none falsifies Born statistics unless an alternative measure is supplied.

## 3. Route C: redundancy

EW(5.2) already shows W is idle in Pred. Redundancy is Occam, not refutation. Corrections: Holevo bounds accessible information but does not explain speedup; Howard et al. (2014) make contextuality necessary for magic-state advantage in specified models, not a full account of quantum computation; the proposed "branches are gauge" quotient is unsupported, because branch-mixing maps change record observables and are physical, not gauge.

## 4. Audit of the DeepSeek "six-layer / transcendental / Lean" argument (2026-11-02)

**Lean names: all 24 cited declarations exist, 0 `sorry`**, in `lean4/Imported/GenesisDerivation/Derivation/{PrimDiff,PrimitiveCore,Apartness,Pigeonhole,Basic}.lean` (imported Genesis layer). One misattribution: `supply_no_op` is in `Inertia.lean`, not `Basic.lean`. One misreading: `orientation_data_invisible_to_collapse` has a first conjunct DeepSeek omits: no endpoint-fixing map carries `D2` to `D2rev`. Orientation is real data that collapse cannot see; it is not absent.

**What the theorems actually say, and whether they touch Everett:**

| Theorem | Actual content | Bears on Everett's branches? |
|---|---|---|
| `f_ops_irrelevant` | `F {S with Ops := O'} ↔ F S` by `Iff.rfl`: `F` is *defined* without `Ops` | No. A definitional fact about a predicate that by design has no dynamics. Branch stability is a dynamical claim (record overlaps $G_{ij}(t)\to0$, EW(3.4)); `F` cannot express it, so it cannot refute it |
| `prot_/ret_not_from_witness` | A model exists with the `prot`/`ret` store empty | No. Everett agrees: records are not implied by a difference; they are *produced* by the coupling $U_M$ (EW(4.1)). The Lean layer has no unitary dynamics, so it cannot ask whether $U_M$ produces them |
| `merger_erases`, `irred_antitone` | A constant map in the admitted family destroys irreducibility | **Cuts the other way.** Unitaries are bijections; a unitary family contains no merger. "No mergers" *is* unitarity, Everett's one empirical commitment. So this reduces to Lemma 0 / Route A: find a physical merger (collapse) and Everett falls |
| `symmetric_no_equivariant_classifier` | $f:\mathrm{Bool}\to\mathrm{Bool}$, $f\circ\neg=f\Rightarrow f$ constant | No. Everett's observer is not a swap-equivariant classifier on the global state; each relative state carries its own record $|O_i\rangle$ (EW(4.3)). The symmetry is broken by the records, inside the theory |
| `Pigeonhole.*`, `R2L_wf`, `R2F_wf`, `separable_not_collapsed` | finite counting; well-formedness of two declared regimes | No bearing on branches |
| "`Setting` has no observation field" | a docstring about a signature | Not a theorem. Leaving a field out of a structure proves nothing about the world; it scopes the file |

**The transcendental argument is an equivocation.** Step 5 says "MW denies that any observer exists outside the container". Everett denies *external* observers, not observers. Its observers are subsystems specified in the theory's own terms: a tensor factor plus records (EW(4.3)). Step 6 ("the container can only be specified from outside") therefore does not follow. The argument also proves too much. Any universal theory (closed-universe GR, Bohm, GRW applied to the whole cosmos) is "stated from inside" in the same sense. If valid, it eliminates universal physics, not Everett. DeepSeek's own §3 concedes the symmetry, which is the tell.

**What survives (and is already Route B1).** The precise kernel is the **factorization problem**: Everett needs a declared tensor split (system / apparatus / observer) and a branch criterion, and $(\Psi,H)$ alone do not obviously supply either (Schwindt 2012; partial answer Cotler–Penington–Ranard 2019: the spectrum generically fixes a *local* factorization if one exists). That is a sharp mathematical target. The six-layer vocabulary adds no content beyond it.

**DeepSeek's final verdict ("reclassification: MW is an undischarged presentation claim […]") equals EW(5.2) in other words**, and applies to every interpretation equally, as DeepSeek admits. It is consistent with this note. It is not a refutation, and DeepSeek does not claim one.

## 5. Verdict

| Route | Can it eliminate Everett? | With the repository's mathematics? |
|---|---|---|
| A. Non-unitarity or Born violation found | Universal-unitary Everett, yes | No; needs experiment. The repository can supply a closed-system collapse model and exclusion bounds |
| A(iii). Selection-kernel uniqueness theorem | Possibly, and it changes Pred | Yes in principle; open, hard |
| B1. Exact-branch no-go | Only exact-branch Everett | Yes, once the statement is made precise |
| B2. Deutsch–Wallace core | **No: core forces Born over ℚ, ℚ(i), real-closed fields (sketch)** | Yes. Field-dependent classification is Lean-suitable |
| C. Redundancy | No | Already done (EW(5.2)) |

**Bottom line.** No small team will eliminate every reasonable Everett formulation in 12 months. The realistic outputs are (1) a Lean classification theorem for the Deutsch–Wallace core by field (forced over ℚ, ℚ(i), real-closed; conjugate counterexample over ℚ(√2)), and (2) a parameterized closed-system collapse analysis against published data. The sharpest *open* target that could change predictions is A(iii): a uniqueness theorem for observer-selection rules. Everett's real exposure is empirical (unitarity, gravity) and normative (branching indifference). It is not formal.
