# Primary-source registry for *Witnessed Difference*

**Date:** 2026-10-05

**Scope:** Bibliographic and support-role registry for
`witnessed_difference_programme.md`. A registry entry identifies a source and
the claim family for which it may be relevant. It does not prove a
corpus-specific claim.

## Registry protocol

Each record has five fields.

- **Record:** canonical bibliographic information and a stable DOI, arXiv, or
  standards-body link when verified.
- **Consultation:** how much was checked for this synthesis.
- **Support role:** the narrow comparison or imported standard for which the
  source may be used.
- **Affected chapters:** chapters whose related-work or import ledger should
  cite the source.
- **Boundary:** what the citation does not establish.

Consultation labels are:

- `OFFICIAL RECORD VERIFIED` — an official standards/publisher record and its
  scope or abstract were checked.
- `PRIMARY METADATA VERIFIED` — title, authors, venue, and identifier were
  checked against a primary host, but the abstract or theorem text was not
  substantively audited.
- `PRIMARY METADATA AND ABSTRACT VERIFIED` — title, authors, identifier, and
  abstract-level scope were checked against a primary host or author archive;
  the complete text was not audited for every theorem used.
- `PRIMARY METADATA AND PRIMARY PDF VERIFIED` — bibliographic metadata and the
  primary-hosted paper were checked at scope level, but no claim is made that
  every theorem or proof was audited.
- `CORPUS CITATION; FULL TEXT NOT RECHECKED` — the source is already named in
  the corpus, but this pass did not re-audit the complete source.
- `UNCONSULTED` — known citation target not read in this synthesis.
- `UNRESOLVED` — the corpus gives insufficient or possibly corrupted
  bibliographic data; the entry must not support a released claim until fixed.

No `UNCONSULTED` or `UNRESOLVED` record may be used as evidence for a theorem.
An abstract-level check supports only positioning and source selection unless
the exact theorem and hypotheses are subsequently checked in the primary text.

---

## A. Metrology, scales, and instruments

### REF-MET-001 — International Vocabulary of Metrology (VIM3)

- **Record:** Joint Committee for Guides in Metrology, *International
  Vocabulary of Metrology—Basic and General Concepts and Associated Terms*,
  3rd ed., JCGM 200:2012. [DOI 10.59161/JCGM200-2012](https://doi.org/10.59161/JCGM200-2012).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; official BIPM record and
  vocabulary scope checked.
- **Support role:** normative vocabulary for measurand, measurement,
  indication, result, calibration, measuring instrument/system, metrological
  traceability, and uncertainty.
- **Affected chapters:** 12–13, 15, Appendix E.
- **Boundary:** VIM definitions do not prove that the monograph’s observer
  architecture is complete or that any specific measurement packet is valid.

### REF-MET-002 — Guide to the Expression of Uncertainty in Measurement

- **Record:** Joint Committee for Guides in Metrology, *Evaluation of
  Measurement Data—Guide to the Expression of Uncertainty in Measurement*,
  JCGM 100:2008, [DOI 10.59161/JCGM100-2008E](https://doi.org/10.59161/JCGM100-2008E),
  with Amendment 1:2026,
  [DOI 10.59161/PPDI3267](https://doi.org/10.59161/PPDI3267).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; scope and current BIPM listing
  checked. The amendment record was identified but its substantive changes were
  not audited here.
- **Support role:** primary standard for stating and propagating measurement
  uncertainty for well-defined measurands.
- **Affected chapters:** 7, 13, 15.
- **Boundary:** it does not select the finite interval or probabilistic
  uncertainty semantics used in a particular worked example.

### REF-MET-003 — GUM introduction

- **Record:** Joint Committee for Guides in Metrology, *Guide to the Expression
  of Uncertainty in Measurement—Part 1: Introduction*, JCGM GUM-1:2023.
  [DOI 10.59161/JCGMGUM-1-2023](https://doi.org/10.59161/JCGMGUM-1-2023).
- **Consultation:** `OFFICIAL RECORD VERIFIED` at bibliographic level.
- **Support role:** contemporary entry point for uncertainty concepts and the
  GUM document family.
- **Affected chapters:** 13 and reference guidance.
- **Boundary:** use the exact applicable GUM document, not this introductory
  record alone, for a quantitative uncertainty theorem.

### REF-MET-004 — SI Brochure

- **Record:** Bureau International des Poids et Mesures, *The International
  System of Units (SI)*, 9th ed. (2019), updated 2026.
  [DOI 10.59161/AUEZ1291](https://doi.org/10.59161/AUEZ1291).
- **Consultation:** `OFFICIAL RECORD VERIFIED`.
- **Support role:** units, SI definitions, and reference-system context.
- **Affected chapters:** 7, 13.
- **Boundary:** an SI unit definition does not calibrate an instrument or
  establish a traceability chain by itself.

### REF-MET-005 — Scales of measurement

- **Record:** S. S. Stevens, “On the Theory of Scales of Measurement,”
  *Science* 103 (2684), 677–680 (1946).
  [DOI 10.1126/science.103.2684.677](https://doi.org/10.1126/science.103.2684.677).
- **Consultation:** `PRIMARY METADATA VERIFIED`; full historical argument not
  re-audited.
- **Support role:** historical classification of nominal, ordinal, interval,
  and ratio scales.
- **Affected chapters:** 13.
- **Boundary:** Stevens’s operational classification is not a substitute for
  current metrological vocabulary, calibration, traceability, or uncertainty.

### REF-MET-006 — Davies–Lewis instruments

- **Record:** E. B. Davies and J. T. Lewis, “An Operational Approach to Quantum
  Probability,” *Communications in Mathematical Physics* 17, 239–260 (1970).
  [DOI 10.1007/BF01647093](https://doi.org/10.1007/BF01647093).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** primary source for the quantum instrument concept and
  repeated-measurement operational framework.
- **Affected chapters:** 13, 19.
- **Boundary:** the Hilbert/operator framework is an optional quantum import; it
  does not define general measurement at the root level.

### REF-MET-007 — Ozawa measuring processes

- **Record:** M. Ozawa, “Quantum Measuring Processes of Continuous
  Observables,” *Journal of Mathematical Physics* 25, 79–87 (1984).
  [DOI 10.1063/1.526000](https://doi.org/10.1063/1.526000).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** relation between measuring processes, completely positive
  instruments, state change, and repeatability limitations.
- **Affected chapters:** 13, 19.
- **Boundary:** does not show that the finite observation ladder derives a
  quantum instrument.

---

## B. Finite cochains, topology, optimization, and proof receipts

### REF-MATH-001 — Discrete Hodge theory

- **Record:** J. Dodziuk, “Finite-Difference Approach to the Hodge Theory of
  Harmonic Forms,” *American Journal of Mathematics* 98 (1), 79–104 (1976).
  [DOI 10.2307/2373615](https://doi.org/10.2307/2373615).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** established discrete cochain/Hodge context for finite graph
  and cell-complex operators.
- **Affected chapters:** 4–5.
- **Boundary:** does not select the monograph’s coefficient norm, observer, or
  quantum interpretation.

### REF-MATH-002 — Algebraic topology

- **Record:** A. Hatcher, *Algebraic Topology*, Cambridge University Press
  (2002). [Author-hosted text](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** standard definitions of chain complexes, cohomology, and
  related topology.
- **Affected chapters:** 4, 5, 11, 16.
- **Boundary:** standard cohomology does not apply when the proposed
  differentials fail square-zero.

### REF-MATH-003 — Homology

- **Record:** S. Mac Lane, *Homology*, Springer (1963).
  [DOI 10.1007/978-3-642-62029-4](https://doi.org/10.1007/978-3-642-62029-4).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; complete book not re-audited.
- **Support role:** standard homological algebra and complex terminology.
- **Affected chapters:** 4, 16.
- **Boundary:** citing a standard text does not discharge the corpus-specific
  differential identities.

### REF-MATH-004 — Categories and universal properties

- **Record:** S. Mac Lane, *Categories for the Working Mathematician*, 2nd ed.,
  Springer (1998). [DOI 10.1007/978-1-4757-4721-8](https://doi.org/10.1007/978-1-4757-4721-8).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; complete book not re-audited.
- **Support role:** categories, naturality, limits, and universal-property
  vocabulary.
- **Affected chapters:** 10–11, 16, 20.
- **Boundary:** it does not establish that the proposed observer category or a
  root observer exists.

### REF-MATH-005 — Convex analysis

- **Record:** R. T. Rockafellar, *Convex Analysis*, Princeton University Press
  (1970). [Publisher record](https://press.princeton.edu/books/paperback/9780691015866/convex-analysis).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** finite-dimensional convex duality and separation context.
- **Affected chapters:** 4–5.
- **Boundary:** a general duality citation does not replace checking constraint
  qualifications for the weighted quotient problem.

### REF-MATH-006 — Functional equations

- **Record:** J. Aczél, *Lectures on Functional Equations and Their
  Applications*, Mathematics in Science and Engineering 19, Academic Press
  (1966), 510 pp. [Google Books record](https://books.google.com/books?id=1Va4QgAACAAJ).
- **Consultation:** `PRIMARY METADATA VERIFIED`; full book and theorem text
  were not audited.
- **Support role:** candidate source for additivity and representation results
  used by observer-gauge source papers.
- **Affected chapters:** 4, 8, 10.
- **Boundary:** metadata verification alone is not theorem evidence; every
  imported representation result still needs an exact statement and matched
  hypotheses.

### REF-MATH-007 — Proof-carrying code

- **Record:** G. C. Necula, “Proof-Carrying Code,” *POPL ’97*, 106–119 (1997).
  [DOI 10.1145/263699.263712](https://doi.org/10.1145/263699.263712).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** comparison for portable machine-checkable evidence and
  verifier boundaries.
- **Affected chapters:** 10, 12, 21.
- **Boundary:** a proof-carrying-code architecture does not validate this
  repository’s receipts or confer authority.

### REF-MATH-008 — Permutation groups

- **Record:** P. J. Cameron, *Permutation Groups*, Cambridge University Press
  (1999).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** group actions, orbits, stabilizers, and symmetry context.
- **Affected chapters:** 3, 8.
- **Boundary:** the finite fixed-point arguments in the monograph are proved
  directly; the citation is context, not their evidence.

### REF-MATH-009 — Graph spectra

- **Record:** Y. Colin de Verdière, *Spectres de graphes*, Société Mathématique
  de France, Cours Spécialisés 4 (1998), 122 pp., ISBN 978-2-85629-068-2.
  [Official SMF record](https://smf.emath.fr/node/43207).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; full book not audited.
- **Support role:** graph spectral context for connection-Laplacian sources.
- **Affected chapters:** 5.
- **Boundary:** no detailed spectral theorem is imported without a page- or
  theorem-level check.

### REF-MATH-010 — Finite pivoting rule for the simplex method

- **Record:** R. G. Bland, “New finite pivoting rules for the simplex method,”
  *Mathematics of Operations Research* 2(2), 103–107 (1977).
  [DOI 10.1287/moor.2.2.103](https://doi.org/10.1287/moor.2.2.103).
- **Consultation:** `PRIMARY METADATA VERIFIED` (Crossref record checked
  2026-09-28); the paper was not re-audited.
- **Support role:** termination of the exact simplex method used by the
  executable package to find repair/circulation pairs (§4.10).
- **Affected chapters:** 4.
- **Boundary:** soundness of every reported $\Phi_1$ value rests on the
  independent certificate check of `CH04-P07`, not on this citation.

### REF-MATH-011 — Group cohomology

- **Record:** K. S. Brown, *Cohomology of Groups*, Graduate Texts in
  Mathematics 87, Springer (1982).
  [DOI 10.1007/978-1-4684-9327-6](https://doi.org/10.1007/978-1-4684-9327-6).
- **Consultation:** `PRIMARY METADATA VERIFIED` (Crossref record checked
  2026-09-28); the book was not re-audited.
- **Support role:** the standard correspondence between projective
  representations, phase 2-cocycles, and $H^2(G;U(1))$ used in §5.13.
- **Affected chapters:** 5.
- **Boundary:** the Klein-four and clock-and-shift computations in §5.13 are
  checked directly; the citation supplies vocabulary, not the examples.

---

### REF-MATH-012 — Abstract polymer convergence

- **Record:** Roberto Fernández and Aldo Procacci, *Cluster expansion for
  abstract polymer models. New bounds from an old approach*,
  [arXiv:math-ph/0605041v2](https://arxiv.org/pdf/math-ph/0605041v2),
  16 October 2006.
- **Consultation:** `PRIMARY METADATA AND PRIMARY PDF VERIFIED`; section 2,
  equations (2.10), (2.14) and (2.15), checked on 2026-10-03.
- **Support role:** the Kotecky–Preiss condition for hard-core abstract
  polymers and its absolute pinned-log expansion bound, including
  self-incompatibility. The Meron supplements derive their own CAR
  factorization, activities, support graph and convergence margin.
- **Affected chapters:** Appendix O.8–O.9 and their analytic/spatial supplements.
- **Boundary:** the abstract criterion does not identify a physical model,
  prove a Meron activity estimate, or establish quantum field dynamics.

## C. Automata, information flow, and weighted histories

### REF-AUT-001 — Myhill’s finite-automata report

- **Record:** J. Myhill, “Finite Automata and the Representation of Events,”
  in *Fundamental Concepts in the Theory of Systems*, Wright Air Development
  Center Technical Report 57-624, pp. 112–137 (1957).
- **Consultation:** `PRIMARY METADATA VERIFIED`; no stable primary scan was
  located, so theorem text was not audited.
- **Support role:** historical source for the distinguishability/minimal-state
  tradition.
- **Affected chapters:** 3.
- **Boundary:** this record is historical positioning only. The verified
  Nerode record below is the operative primary anchor for minimization, and
  neither source derives order-free retention.

### REF-AUT-002 — Nerode equivalence

- **Record:** A. Nerode, “Linear Automaton Transformations,” *Proceedings of the
  American Mathematical Society* 9 (4), 541–544 (1958).
  [DOI 10.1090/S0002-9939-1958-0135681-9](https://doi.org/10.1090/S0002-9939-1958-0135681-9).
- **Consultation:** `PRIMARY METADATA VERIFIED`; theorem text not re-audited.
- **Support role:** primary historical anchor for automaton quotient/minimization
  by future distinguishability.
- **Affected chapters:** 3.
- **Boundary:** the word-based theorem presupposes ordered input and does not
  derive order-free retention.

### REF-AUT-003 — Weighted automata

- **Record:** M. P. Schützenberger, “On the Definition of a Family of Automata,”
  *Information and Control* 4, 245–270 (1961).
  [DOI 10.1016/S0019-9958(61)80020-X](https://doi.org/10.1016/S0019-9958(61)80020-X).
- **Consultation:** `PRIMARY METADATA AND PRIMARY PDF VERIFIED` at scope level.
- **Support role:** foundational weighted/linear automata and recognizable-
  series context for finite semiring history sums.
- **Affected chapters:** 17.
- **Boundary:** does not prove the corpus’s proposed all-length star theorem over
  an arbitrary semiring.

### REF-AUT-004 — Information flow

- **Record:** J. Barwise and J. Seligman, *Information Flow: The Logic of
  Distributed Systems*, Cambridge University Press (1997).
  [DOI 10.1017/CBO9780511895968](https://doi.org/10.1017/CBO9780511895968).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; complete book not
  audited.
- **Support role:** classifications, channels, and information-flow comparison
  for presentation and retention.
- **Affected chapters:** 3, 10–11.
- **Boundary:** channel theory takes substantial classification structure as
  input and does not derive the programme’s root observer.

### REF-AUT-005 — Bisimulation sources

- **Record:** D. Park, “Concurrency and Automata on Infinite Sequences,” in
  *Theoretical Computer Science*, LNCS 104, 167–183 (1981),
  [DOI 10.1007/BFb0017309](https://doi.org/10.1007/BFb0017309); R. Milner,
  *Communication and Concurrency*, Prentice Hall (1989), ISBN 0-13-115007-3.
- **Consultation:** `PRIMARY METADATA VERIFIED`; full chapter and book were not
  audited.
- **Support role:** identity-through-transition and behavioral-equivalence
  comparison.
- **Affected chapters:** 3, 10.
- **Boundary:** these records support comparison only; no bisimulation theorem
  is imported without matching transition-system hypotheses.

### REF-AUT-006 — Formal power series texts

- **Record:** J. Berstel and C. Reutenauer, *Noncommutative Rational Series with
  Applications*, Cambridge University Press (2011), ISBN 978-0-521-19022-0,
  [DOI 10.1017/CBO9780511760860](https://doi.org/10.1017/CBO9780511760860).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; full book not audited.
- **Support role:** standard matrix representations and recognizable series.
- **Affected chapters:** 17.
- **Boundary:** the record does not make an arbitrary semiring admit an
  infinite sum or a Kleene-star interpretation; those conditions remain
  explicit in Chapter 17.

### REF-AUT-007 — Feynman path formulation

- **Record:** R. P. Feynman, “Space-Time Approach to Non-Relativistic Quantum
  Mechanics,” *Reviews of Modern Physics* 20, 367–387 (1948).
  [DOI 10.1103/RevModPhys.20.367](https://doi.org/10.1103/RevModPhys.20.367).
- **Consultation:** `PRIMARY METADATA VERIFIED`; full derivation not re-audited.
- **Support role:** primary contrast for the continuum/complex-amplitude path
  formulation.
- **Affected chapters:** 17, 19.
- **Boundary:** finite semiring path aggregation is not identified with
  Feynman’s formulation.

---

## D. Time, order, and causal-set comparisons

### REF-TIME-001 — Causal sets

- **Record:** L. Bombelli, J. Lee, D. Meyer, and R. D. Sorkin, “Space-Time as a
  Causal Set,” *Physical Review Letters* 59, 521–524 (1987).
  [DOI 10.1103/PhysRevLett.59.521](https://doi.org/10.1103/PhysRevLett.59.521).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** original locally finite partial-order proposal for causal
  spacetime.
- **Affected chapters:** 6–7.
- **Boundary:** causal order, local finiteness, and continuum approximation are
  inputs/results of that programme, not consequences of witnessed difference.

### REF-TIME-002 — Causal-set review

- **Record:** J. Henson, “The Causal Set Approach to Quantum Gravity” (2006).
  [arXiv:gr-qc/0601121](https://arxiv.org/abs/gr-qc/0601121).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** review of causal-set motivation, Lorentz issues, history
  spaces, results, and open problems.
- **Affected chapters:** 6–7.
- **Boundary:** a review citation does not supply a duration gauge or clock
  adequacy theorem for this monograph.

### REF-TIME-003 — Causal-set directions

- **Record:** S. Surya, “Directions in Causal Set Quantum Gravity” (2011).
  [arXiv:1103.6272](https://arxiv.org/abs/1103.6272).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** broader causal-set research context.
- **Affected chapters:** 6–7.
- **Boundary:** no corpus-specific claim is supported without checking the exact
  passage used.

### REF-TIME-004 — Causal-set axioms

- **Record:** B. F. Dribus, “On the Axioms of Causal Set Theory” (2013).
  [arXiv:1311.2148](https://arxiv.org/abs/1311.2148).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** comparison between local causal relations and generated
  order.
- **Affected chapters:** 6.
- **Boundary:** does not validate the monograph’s succession construction.

### REF-TIME-005 — Energetic causal sets

- **Record:** M. Cortês and L. Smolin, “Energetic Causal Sets” (2013/2014).
  [arXiv:1308.2206](https://arxiv.org/abs/1308.2206).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** downstream model adding energy-momentum, conservation, and
  amplitudes to causal links.
- **Affected chapters:** 6–7, 19.
- **Boundary:** these added physical structures are not root-level results.

### REF-TIME-006 — Relational/deparametrized time

- **Record:** C. Rovelli, “Forget Time” (2009).
  [arXiv:0903.3832](https://arxiv.org/abs/0903.3832).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** comparison for removing a preferred external time parameter
  while retaining relational dynamical structure.
- **Affected chapters:** 6–7.
- **Boundary:** does not construct the monograph’s succession relation or select
  its duration gauge.

### REF-TIME-007 — Timeless configuration comparison

- **Record:** J. B. Barbour, “The Emergence of Time and Its Arrow from
  Timelessness,” in J. J. Halliwell, J. Pérez-Mercader, and W. H. Zurek (eds.),
  *Physical Origins of Time Asymmetry*, Cambridge University Press, 405–414
  (1994). [Author publication record](https://platonia.com/papers.html).
- **Consultation:** `PRIMARY METADATA VERIFIED`; chapter text not audited.
- **Support role:** comparison for complete configurations, best matching, and
  emergent temporal description.
- **Affected chapters:** 6–7.
- **Boundary:** comparison only; it does not prove the WDP succession or
  duration constructions.

### REF-TIME-008 — Lynds on time representation

- **Record:** P. Lynds, “Time and Classical and Quantum Mechanics: Indeterminacy
  vs. Discontinuity” (2003). [arXiv:physics/0310055](https://arxiv.org/abs/physics/0310055).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** interpretive warning against reifying coordinate instants as
  static physical atoms.
- **Affected chapters:** 6–7.
- **Boundary:** the monograph does not import universal-indeterminacy, Zeno, or
  chronon conclusions.

### REF-TIME-009 — Russell, Wiener, and Walker instant constructions

- **Record:** B. Russell, *Our Knowledge of the External World*, Open Court
  (1914), [public-domain text](https://www.gutenberg.org/ebooks/37090); N.
  Wiener, “A Contribution to the Theory of Relative Position,” *Proceedings of
  the Cambridge Philosophical Society* 17, 441–449 (1914); A. G. Walker,
  “Foundations of Relativity: Parts I and II,” *Proceedings of the Royal Society
  of Edinburgh A* 62 (3), 319–335 (1948),
  [DOI 10.1017/S0080454100006725](https://doi.org/10.1017/S0080454100006725).
- **Consultation:** `PRIMARY METADATA VERIFIED`; Russell’s public text and the
  official Walker abstract/record were checked, but no full comparative audit
  of the three constructions was performed.
- **Support role:** history of reconstructing instants from already temporal
  event relations.
- **Affected chapters:** 6.
- **Boundary:** the records support a narrow historical comparison only; no
  equivalence among their constructions or with WDP succession is claimed.

---

## E. Probability and representation

### REF-PROB-001 — Kolmogorov probability

- **Record:** A. N. Kolmogorov, *Grundbegriffe der
  Wahrscheinlichkeitsrechnung* (1933).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`; stable edition
  and translation record to be selected.
- **Support role:** countably additive probability on a sigma-algebra.
- **Affected chapters:** 8–9.
- **Boundary:** the monograph constructs only finite normalized valuations until
  such measure structure is imported.

### REF-PROB-002 — Gleason’s theorem

- **Record:** A. M. Gleason, “Measures on the Closed Subspaces of a Hilbert
  Space,” *Journal of Mathematics and Mechanics* 6, 885–893 (1957).
  [DOI 10.1512/iumj.1957.6.56050](https://doi.org/10.1512/iumj.1957.6.56050).
- **Consultation:** `PRIMARY METADATA VERIFIED`; theorem hypotheses not
  re-audited in full for this pass.
- **Support role:** primary source for a Hilbert-space measure representation
  theorem relevant to Born-rule uniqueness under substantial assumptions.
- **Affected chapters:** 9, 18–19.
- **Boundary:** positivity and normalization in the finite root do not satisfy
  or derive Gleason’s hypotheses.

### REF-PROB-003 — Hume’s principle and neo-logicism

- **Record:** Frege’s *Grundlagen der Arithmetik* (1884) and Wright’s 1983
  neo-logicist treatment: G. Frege, *Die Grundlagen der Arithmetik*, W.
  Koebner (1884); C. Wright, *Frege’s Conception of Numbers as Objects*,
  Aberdeen University Press (1983), ISBN 0-08-025726-7.
- **Consultation:** `PRIMARY METADATA VERIFIED`; exact page-level philosophical
  argument was not audited.
- **Support role:** comparison for number via one-to-one correspondence.
- **Affected chapters:** 8.
- **Boundary:** the monograph uses per-exhibition matching and does not infer a
  Fregean number object.

### REF-PROB-004 — Frequentist sources

- **Record:** J. Venn, *The Logic of Chance*, Macmillan (1866); R. von Mises,
  *Wahrscheinlichkeit, Statistik und Wahrheit*, Springer (1928).
- **Consultation:** `PRIMARY METADATA VERIFIED`; complete editions were not
  audited.
- **Support role:** limiting-frequency comparison.
- **Affected chapters:** 9.
- **Boundary:** finite exhibited proportions are not limiting frequencies.

### REF-PROB-005 — Exchangeability

- **Record:** B. de Finetti, “La prévision: ses lois logiques, ses sources
  subjectives,” *Annales de l’Institut Henri Poincaré* 7 (1), 1–68 (1937).
  [Official Numdam record and scan](https://www.numdam.org/item/AIHP_1937__7_1_1_0/).
- **Consultation:** `PRIMARY METADATA AND PRIMARY PDF VERIFIED` at scope level;
  the representation theorem was not rederived or matched line by line.
- **Support role:** comparison for exchangeable sequences and representation.
- **Affected chapters:** 9.
- **Boundary:** no exchangeability or infinite representation theorem is
  derived from finite witness symmetry.

### REF-PROB-006 — Indifference and maximum entropy

- **Record:** P.-S. Laplace, *Théorie analytique des probabilités* (1812), as a
  historical indifference source; E. T. Jaynes, “Information Theory and
  Statistical Mechanics,” *Physical Review* 106, 620–630 (1957),
  [DOI 10.1103/PhysRev.106.620](https://doi.org/10.1103/PhysRev.106.620).
- **Consultation:** `PRIMARY METADATA VERIFIED`; neither full historical text
  nor Jaynes’s derivation was audited for theorem import.
- **Support role:** comparison for prior selection under symmetry or constraints.
- **Affected chapters:** 8–9.
- **Boundary:** the finite orbit theorem does not choose weights across distinct
  orbits and does not derive maximum entropy.

---

## F. Contextuality, quantum foundations, and reconstruction

### REF-QM-001 — Sheaf-theoretic contextuality

- **Record:** S. Abramsky and A. Brandenburger, “The Sheaf-Theoretic Structure
  of Non-Locality and Contextuality,” *New Journal of Physics* 13, 113036
  (2011). [arXiv:1102.0264](https://arxiv.org/abs/1102.0264);
  [DOI 10.1088/1367-2630/13/11/113036](https://doi.org/10.1088/1367-2630/13/11/113036).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** measurement covers, empirical models, global sections, and
  contextuality/nonlocality obstruction hierarchy.
- **Affected chapters:** 2, 4, 11, 18–19.
- **Boundary:** a graph non-coboundary or parity contradiction is not
  automatically an empirical contextuality model.

### REF-QM-002 — Cohomological contextuality witnesses

- **Record:** S. Abramsky, S. Mansfield, and R. S. Barbosa, “The Cohomology of
  Non-Locality and Contextuality” (2011/2012).
  [arXiv:1111.3620](https://arxiv.org/abs/1111.3620).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** cohomological obstructions as sufficient witnesses in the
  declared empirical-model setting.
- **Affected chapters:** 4, 18.
- **Boundary:** the source itself distinguishes sufficiency from necessity; the
  corpus must also supply a valid cochain complex and empirical adapter.

### REF-QM-003 — Hardy reconstruction

- **Record:** L. Hardy, “Quantum Theory From Five Reasonable Axioms” (2001).
  [arXiv:quant-ph/0101012](https://arxiv.org/abs/quant-ph/0101012).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** reconstruction benchmark in which continuity separates the
  intended quantum branch from a classical alternative under the paper’s
  complete axiom package.
- **Affected chapters:** 9, 18–19.
- **Boundary:** citing the reconstruction does not show that the witnessed-
  difference calculus satisfies its axioms.

### REF-QM-004 — Informational reconstruction

- **Record:** G. Chiribella, G. M. D’Ariano, and P. Perinotti,
  “Informational Derivation of Quantum Theory,” *Physical Review A* 84, 012311
  (2011). [arXiv:1011.6451](https://arxiv.org/abs/1011.6451);
  [DOI 10.1103/PhysRevA.84.012311](https://doi.org/10.1103/PhysRevA.84.012311).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** operational principles and purification-based quantum
  reconstruction benchmark.
- **Affected chapters:** 18–19.
- **Boundary:** the monograph currently does not derive or verify purification
  and the other required principles.

### REF-QM-005 — Generalized probabilistic theories

- **Record:** J. Barrett, “Information Processing in Generalized Probabilistic
  Theories,” *Physical Review A* 75, 032304 (2007).
  [DOI 10.1103/PhysRevA.75.032304](https://doi.org/10.1103/PhysRevA.75.032304).
- **Consultation:** `PRIMARY METADATA VERIFIED`; full framework not re-audited.
- **Support role:** GPT comparison class for classical, quantum, and broader
  operational models.
- **Affected chapters:** 18–19.
- **Boundary:** GPT vocabulary is imported structure, not generated by the root
  calculus.

### REF-QM-006 — Masanes–Müller reconstruction

- **Record:** L. Masanes and M. P. Müller, “A Derivation of Quantum Theory from
  Physical Requirements,” *New Journal of Physics* 13, 063001 (2011).
  [arXiv:1004.1483](https://arxiv.org/abs/1004.1483);
  [DOI 10.1088/1367-2630/13/6/063001](https://doi.org/10.1088/1367-2630/13/6/063001).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** reconstruction comparison involving operational/physical
  requirements.
- **Affected chapters:** 9, 18–19.
- **Boundary:** exact hypotheses must be checked before any theorem-level
  comparison.

### REF-QM-007 — Bell/CHSH

- **Record:** J. S. Bell, “On the Einstein Podolsky Rosen Paradox,” *Physics*
  1, 195–200 (1964).
  [DOI 10.1103/PhysicsPhysiqueFizika.1.195](https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195).
- **Consultation:** `PRIMARY METADATA VERIFIED`.
- **Support role:** primary nonlocality/Bell-inequality context.
- **Affected chapters:** 18–19.
- **Boundary:** a repository CHSH fixture does not inherit every conclusion of
  Bell’s paper.

### REF-QM-008 — Kochen–Specker

- **Record:** S. Kochen and E. P. Specker, “The Problem of Hidden Variables in
  Quantum Mechanics,” *Journal of Mathematics and Mechanics* 17, 59–87
  (official record 1968; commonly cited 1967).
  [DOI 10.1512/iumj.1968.17.17004](https://doi.org/10.1512/iumj.1968.17.17004).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; theorem proof and hypotheses
  were not re-audited.
- **Support role:** contextual value-assignment no-go background.
- **Affected chapters:** 18–19.
- **Boundary:** contextuality background only; a detailed use still requires
  matching the paper’s dimension and valuation hypotheses.

### REF-QM-009 — PR-box boundary

- **Record:** S. Popescu and D. Rohrlich, “Quantum Nonlocality as an Axiom,”
  *Foundations of Physics* 24, 379–385 (1994).
  [DOI 10.1007/BF02058098](https://doi.org/10.1007/BF02058098).
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** nonsignalling post-quantum comparison showing that
  nonlocality alone does not characterize quantum correlations.
- **Affected chapters:** 18–19.
- **Boundary:** the monograph’s PR-box fixture must state its own table and
  checks; the citation does not verify repository code.

### REF-QM-010 — Tsirelson bound

- **Record:** B. S. Cirel’son, “Quantum Generalizations of Bell’s Inequality,”
  *Letters in Mathematical Physics* 4, 93–100 (1980).
  [DOI 10.1007/BF00417500](https://doi.org/10.1007/BF00417500).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`; full proof not
  re-audited.
- **Support role:** primary source for the quantum correlation bound.
- **Affected chapters:** 18–19.
- **Boundary:** the monograph now derives the squared bound conditionally on the declared Hilbert-space, positivity, tensor-product and Born-pairing assumptions; it does not derive those assumptions or classify all theories attaining the bound.

### REF-QM-011 — Generalized contextuality

- **Record:** R. W. Spekkens, “Contextuality for Preparations,
  Transformations, and Unsharp Measurements,” *Physical Review A* 71, 052108
  (2005). [DOI 10.1103/PhysRevA.71.052108](https://doi.org/10.1103/PhysRevA.71.052108).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** broader operational contextuality comparison.
- **Affected chapters:** 18–19.
- **Boundary:** the source’s operational equivalences must not be conflated with
  arbitrary observer-profile equivalence.

### REF-QM-012 — Relational quantum mechanics

- **Record:** C. Rovelli, “Relational Quantum Mechanics” (1996).
  [arXiv:quant-ph/9609002](https://arxiv.org/abs/quant-ph/9609002).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** interpretive comparison for observer-relative states while
  retaining quantum formalism.
- **Affected chapters:** 10–11, 18, 20.
- **Boundary:** RQM posits physical systems in a quantum framework; it does not
  derive the programme’s observer packet from Primitive Difference.

### REF-QM-013 — QBism

- **Record:** C. A. Fuchs, N. D. Mermin, and R. Schack, “An Introduction to
  QBism with an Application to the Locality of Quantum Mechanics” (2013/2014).
  [arXiv:1311.5253](https://arxiv.org/abs/1311.5253).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** agent-relative probability/state comparison.
- **Affected chapters:** 9–10, 18.
- **Boundary:** the monograph neither derives QBist agency nor treats its own
  finite valuation as QBist probability.

### REF-QM-014 — Eighteen-vector Kochen-Specker proof

- **Record:** A. Cabello, J. M. Estebaranz, and G. García-Alcaine, “Bell-Kochen-Specker theorem: A proof with 18 vectors,” *Physics Letters A* 212, 183–188 (1996); [arXiv:quant-ph/9706009](https://arxiv.org/abs/quant-ph/9706009).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** minimal 18-ray contextuality configuration in dimension 4.
- **Affected chapters:** 18.
- **Boundary:** contextuality obstruction over ray systems; not derived from primitive difference alone.

### REF-QM-015 — Mermin-Peres magic square

- **Record:** N. D. Mermin, “Simple unified form for the major no-hidden-variables theorems,” *Physical Review Letters* 65, 3373–3376 (1990); A. Peres, “Incompatible results of quantum measurements,” *Physics Letters A* 151, 107–108 (1990).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** state-independent operator-algebraic contextuality and parity obstruction.
- **Affected chapters:** 18.
- **Boundary:** presupposes tensor product $M_2(\mathbb{C}) \otimes M_2(\mathbb{C})$ and Pauli algebra.

### REF-QM-016 — Stinespring dilation and finite Kraus rank

- **Record:** W. F. Stinespring, “Positive functions on C*-algebras,” *Proceedings of the American Mathematical Society* 6, 211–216 (1955); see also finite-dimensional environment bounds (e.g. arXiv:2301.05488v3).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** dilation of quantum channels to unitary operations on enlarged state spaces.
- **Affected chapters:** 18.
- **Boundary:** for finite-dimensional systems, Kraus rank $r \le d_A d_B$ bounds environment dimension without infinite-dimensional continuous reservoirs; a stochastic channel need not be a reversible map on the original carrier; a dilation adds a separately declared environment.

### REF-QM-017 — Gleason theorem on frame functions

- **Record:** A. M. Gleason, “Measures on the Closed Subspaces of a Hilbert Space,” *Journal of Mathematics and Mechanics* 6, 885–893 (1957).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** derivation of Born probability measures on projection lattices of dimension $\ge 3$.
- **Affected chapters:** 18.
- **Boundary:** frame regularity/continuity is derived in dimension $\ge 3$, not an independent axiom; discrete subsets admit non-Bornian rational evaluations.

### REF-QM-018 — Sorkin higher-order interference

- **Record:** R. D. Sorkin, “Quantum mechanics as quantum measure theory,” *Modern Physics Letters A* 9, 3119–3127 (1994); [arXiv:gr-qc/9401003](https://arxiv.org/abs/gr-qc/9401003).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** hierarchy of multi-slit interference and vanishing third-order interference $I_3 = 0$.
- **Affected chapters:** 18–19.
- **Boundary:** tests bilinear Born rule against higher-order interference without requiring Hilbert space.

### REF-QM-019 — Stone theorem on unitary groups

- **Record:** M. H. Stone, “On one-parameter unitary groups in Hilbert Space,” *Annals of Mathematics* 33, 643–648 (1932).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** spectral correspondence between strongly continuous 1-parameter unitary groups and self-adjoint Hamiltonians.
- **Affected chapters:** 18.
- **Boundary:** relies on continuous parameter $t \in \mathbb{R}$ and Hilbert space completion; distinct from discrete algebraic steps in $\mathrm{SO}(n, \mathbb{Q})$.

### REF-QM-020 — Contraction of trace distance under channels

- **Record:** M. B. Ruskai, “Beyond strong subadditivity? Improved bounds on the
  contraction of generalized relative entropy,” *Reviews in Mathematical
  Physics* 6(5a), 1147–1161 (1994).
  [DOI 10.1142/S0129055X94000407](https://doi.org/10.1142/S0129055X94000407).
- **Consultation:** `PRIMARY METADATA VERIFIED` (Crossref record checked
  2026-09-28); the paper was not re-audited. The absorbed primitive-axiomatics
  source cited this paper with the identifier `10.1142/S0129055X9400041X`,
  which Crossref does not resolve, and with a different subtitle; both are
  corrected here.
- **Support role:** contractivity of trace distance under completely positive
  trace-preserving maps, used in `CH05-C01`.
- **Affected chapters:** 5.
- **Boundary:** an imported finite-dimensional inequality; it does not make a
  channel an observer or derive measurement.

### REF-QM-021 — Trace-norm duality

- **Record:** J. Watrous, *The Theory of Quantum Information*, Cambridge
  University Press (2018).
  [DOI 10.1017/9781316848142](https://doi.org/10.1017/9781316848142).
- **Consultation:** `PRIMARY METADATA VERIFIED` (Crossref record checked
  2026-09-28); the book was not re-audited.
- **Support role:** duality between the trace norm and the operator norm on
  finite-dimensional matrix spaces, used in `CH05-C01`.
- **Affected chapters:** 5.
- **Boundary:** the subspace-distance form in §5.14 follows from this duality by
  standard convex-analysis arguments that are cited, not re-proved.

---

## G. Redundancy, observers, self-reference, and consciousness comparisons

### REF-OBS-001 — Environment as witness

- **Record:** H. Ollivier, D. Poulin, and W. H. Zurek, “Objective Properties
  from Subjective Quantum States: Environment as a Witness,” *Physical Review
  Letters* 93, 220401 (2004).
  [arXiv:quant-ph/0307229](https://arxiv.org/abs/quant-ph/0307229);
  [DOI 10.1103/PhysRevLett.93.220401](https://doi.org/10.1103/PhysRevLett.93.220401).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** quantum-Darwinist redundancy and operational objectivity via
  environment fragments.
- **Affected chapters:** 11.
- **Boundary:** requires an open quantum host, decoherence, environment, and
  preferred observables; none is derived in the observer trunk.

### REF-OBS-002 — Environment as a witness, expanded treatment

- **Record:** H. Ollivier, D. Poulin, and W. H. Zurek, “Environment as a
  Witness: Selective Proliferation of Information and Emergence of Objectivity
  in a Quantum Universe,” *Physical Review A* 72, 042113 (2005).
  [arXiv:quant-ph/0408125](https://arxiv.org/abs/quant-ph/0408125);
  [DOI 10.1103/PhysRevA.72.042113](https://doi.org/10.1103/PhysRevA.72.042113).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** redundant environmental records as a comparison for
  multi-observer stability.
- **Affected chapters:** 11.
- **Boundary:** positioning only; no quantum-Darwinist mechanism is claimed.

### REF-OBS-003 — Autopoiesis

- **Record:** F. G. Varela, H. R. Maturana, and R. Uribe, “Autopoiesis: The
  Organization of Living Systems, Its Characterization and a Model,”
  *BioSystems* 5 (4), 187–196 (1974).
  [DOI 10.1016/0303-2647(74)90031-8](https://doi.org/10.1016/0303-2647(74)90031-8).
- **Consultation:** `PRIMARY METADATA VERIFIED`; full paper not re-audited.
- **Support role:** historical systems/organizational comparison for observer
  and self-maintenance discourse.
- **Affected chapters:** 10, 14.
- **Boundary:** autopoietic organization is not proved by finite obstruction
  closure or self-report.

### REF-OBS-004 — Integrated information theory 3.0

- **Record:** M. Oizumi, L. Albantakis, and G. Tononi, “From the Phenomenology
  to the Mechanisms of Consciousness: Integrated Information Theory 3.0,”
  *PLOS Computational Biology* 10 (5), e1003588 (2014).
  [DOI 10.1371/journal.pcbi.1003588](https://doi.org/10.1371/journal.pcbi.1003588).
- **Consultation:** `PRIMARY METADATA VERIFIED`; complete theory not audited.
- **Support role:** comparison for an integration-based consciousness theory.
- **Affected chapters:** 14.
- **Boundary:** the monograph’s residual symbol, integration, or observer tuple
  is not IIT’s $\Phi$ and yields no consciousness claim.

### REF-OBS-005 — Higher-order thought

- **Record:** D. M. Rosenthal, *Consciousness and Mind*, Oxford University
  Press (2005),
  [DOI 10.1093/oso/9780198236979.001.0001](https://doi.org/10.1093/oso/9780198236979.001.0001).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; full book not audited.
- **Support role:** philosophical comparison for higher-order representation.
- **Affected chapters:** 14.
- **Boundary:** comparison only; no bridge from functional self-report to
  phenomenology is supplied.

### REF-OBS-006 — Self-representational consciousness

- **Record:** U. Kriegel, *Subjective Consciousness: A Self-Representational
  Theory*, Oxford University Press (2009),
  [DOI 10.1093/acprof:oso/9780199570355.001.0001](https://doi.org/10.1093/acprof:oso/9780199570355.001.0001).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; full book not audited.
- **Support role:** philosophical comparison for self-representation.
- **Affected chapters:** 14.
- **Boundary:** philosophical comparison only; it is not evidence that a WDP
  self-report has phenomenal character.

### REF-OBS-007 — Global workspace

- **Record:** B. J. Baars, “Global Workspace Theory of Consciousness: Toward a
  Cognitive Neuroscience of Human Experience,” *Progress in Brain Research*
  150, 45–53 (2005),
  [DOI 10.1016/S0079-6123(05)50004-9](https://doi.org/10.1016/S0079-6123(05)50004-9);
  S. Dehaene and J.-P. Changeux, “Experimental and Theoretical Approaches to
  Conscious Processing,” *Neuron* 70, 200–227 (2011),
  [DOI 10.1016/j.neuron.2011.03.018](https://doi.org/10.1016/j.neuron.2011.03.018).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`; full articles
  were not audited.
- **Support role:** functional/global-availability comparison.
- **Affected chapters:** 14.
- **Boundary:** global availability is not equated with the finite
  self-witnessing definition or phenomenology.

### REF-OBS-008 — Meta-problem of consciousness

- **Record:** D. Chalmers, “The Meta-Problem of Consciousness” (2018), as named
  in the source corpus; *Journal of Consciousness Studies* 25 (9–10), 6–61
  (2018). [ANU repository record](http://hdl.handle.net/1885/310975).
- **Consultation:** `PRIMARY METADATA VERIFIED`; full article not audited.
- **Support role:** comparison for explaining reports and judgments about
  consciousness without claiming resolution of experience.
- **Affected chapters:** 14.
- **Boundary:** positioning only; the monograph does not solve either the
  meta-problem or the problem of phenomenal experience.

### REF-OBS-009 — Frauchiger–Renner

- **Record:** D. Frauchiger and R. Renner, “Quantum Theory Cannot Consistently
  Describe the Use of Itself,” *Nature Communications* 9, 3711 (2018).
  [arXiv:1604.07422](https://arxiv.org/abs/1604.07422);
  [DOI 10.1038/s41467-018-05739-8](https://doi.org/10.1038/s41467-018-05739-8).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`; protocol and proof
  were not audited for import.
- **Support role:** future adversarial fixture for context handling in a fully
  specified quantum observer model.
- **Affected chapters:** 14, 19.
- **Boundary:** it is only an adversarial quantum-protocol comparison and must
  not support awareness or general self-reference conclusions.

---

## H. Curved and homotopy-coherent continuation targets

The following records identify rigorous continuation literatures. They are
research targets, not claims that the required hypotheses or structures have
already been constructed in WDP.

### REF-HOM-001 — Double complexes and spectral sequences

- **Record:** C. A. Weibel, *An Introduction to Homological Algebra*, Cambridge
  University Press (1994),
  [DOI 10.1017/CBO9781139644136](https://doi.org/10.1017/CBO9781139644136).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; no theorem/page-level import was
  audited.
- **Support role:** standard double-complex identities and filtration spectral
  sequences.
- **Affected chapters:** 16.
- **Boundary:** no spectral-sequence claim is available until the corpus establishes
  the differential identities and supplies the required filtration data.

### REF-HOM-002 — Curved differential graded structures

- **Record:** L. Positselski, *Two Kinds of Derived Categories, Koszul Duality,
  and Comodule-Contramodule Correspondence*, Memoirs of the American
  Mathematical Society 212 (996) (2011),
  [DOI 10.1090/S0065-9266-2010-00631-8](https://doi.org/10.1090/S0065-9266-2010-00631-8);
  [arXiv:0905.2621](https://arxiv.org/abs/0905.2621).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`; the curved-DG
  definitions and results were not imported theorem by theorem.
- **Support role:** possible formal host when a curvature element replaces
  square-zero.
- **Affected chapters:** 16.
- **Boundary:** the label “curved” is not sufficient; exact axioms and source
  must be fixed.

### REF-HOM-003 — $A_\infty$ structures

- **Record:** B. Keller, “Introduction to $A_\infty$ Algebras and Modules,”
  *Homology, Homotopy and Applications* 3 (1), 1–35 (2001),
  [DOI 10.4310/HHA.2001.v3.n1.a1](https://doi.org/10.4310/HHA.2001.v3.n1.a1);
  [arXiv:math/9910179](https://arxiv.org/abs/math/9910179).
- **Consultation:** `PRIMARY METADATA AND PRIMARY PDF VERIFIED` at scope level;
  no higher-operation theorem is imported.
- **Support role:** higher operations and curved/$m_0$ continuation route.
- **Affected chapters:** 16.
- **Boundary:** no higher operation is generated just by observing a mixed
  defect.

### REF-HOM-004 — Homotopy-coherent diagrams

- **Record:** R. M. Vogt, “Homotopy Limits and Colimits,” *Mathematische
  Zeitschrift* 134, 11–52 (1973),
  [DOI 10.1007/BF01219090](https://doi.org/10.1007/BF01219090); J.-M. Cordier
  and T. Porter, “Homotopy Coherent Category Theory,” *Transactions of the
  American Mathematical Society* 349 (1), 1–54 (1997),
  [DOI 10.1090/S0002-9947-97-01752-2](https://doi.org/10.1090/S0002-9947-97-01752-2).
- **Consultation:** `PRIMARY METADATA VERIFIED`; full proofs not audited.
- **Support role:** replacing strict commutation by specified coherent higher
  cells.
- **Affected chapters:** 11, 16.
- **Boundary:** higher cells and coherence laws remain new data and obligations.

### REF-HOM-005 — Mori–Zwanzig projection

- **Record:** R. Zwanzig, “Memory Effects in Irreversible Thermodynamics,”
  *Physical Review* 124, 983–992 (1961),
  [DOI 10.1103/PhysRev.124.983](https://doi.org/10.1103/PhysRev.124.983); H.
  Mori, “Transport, Collective Motion, and Brownian Motion,” *Progress of
  Theoretical Physics* 33, 423–455 (1965),
  [DOI 10.1143/PTP.33.423](https://doi.org/10.1143/PTP.33.423); A. J. Chorin,
  O. H. Hald, and R. Kupferman, “Optimal Prediction with Memory,” *Physica D*
  166, 239–257 (2002),
  [DOI 10.1016/S0167-2789(02)00446-3](https://doi.org/10.1016/S0167-2789(02)00446-3).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`; derivations were
  not audited for theorem import.
- **Support role:** comparison for projection-induced memory in reduced
  dynamics.
- **Affected chapters:** 16–17.
- **Boundary:** the finite descent counterexample does not supply a
  Mori–Zwanzig kernel identity.

### REF-HOM-006 — Lieb–Robinson bounds

- **Record:** E. H. Lieb and D. W. Robinson, “The Finite Group Velocity of
  Quantum Spin Systems,” *Communications in Mathematical Physics* 28, 251–257
  (1972), [DOI 10.1007/BF01645779](https://doi.org/10.1007/BF01645779).
- **Consultation:** `OFFICIAL RECORD VERIFIED`; proof and modern extensions were
  not audited.
- **Support role:** possible truncation-control import for local Hamiltonian
  systems.
- **Affected chapters:** 16, optional quantum branch.
- **Boundary:** inapplicable until a lattice, local Hamiltonian, norm, and
  dynamics are declared.

### REF-HOM-007 — Homological perturbation lemma

- **Record:** V. K. A. M. Gugenheim, “On the chain-complex of a fibration,”
  *Illinois Journal of Mathematics* 16(3) (1972),
  [DOI 10.1215/ijm/1256065766](https://doi.org/10.1215/ijm/1256065766); D. W.
  Barnes and L. A. Lambe, “A fixed point approach to homological perturbation
  theory,” *Proceedings of the American Mathematical Society* 112(3), 881–892
  (1991), [DOI 10.1090/S0002-9939-1991-1057939-0](https://doi.org/10.1090/S0002-9939-1991-1057939-0),
  with its correction, *Proc. AMS* 129(3), 941 (2001; online 2000),
  [DOI 10.1090/S0002-9939-00-06018-4](https://doi.org/10.1090/S0002-9939-00-06018-4).
- **Consultation:** `PRIMARY METADATA VERIFIED` (Crossref records checked
  2026-09-29); the papers were not re-audited.
- **Support role:** the perturbation lemma for contractions imported as
  `CH16-C01`.
- **Affected chapters:** 16.
- **Boundary:** sign conventions differ between sources; the monograph states
  its own convention and the executable package re-validates every perturbed
  contraction it produces.

---

### REF-PRES-001 — Algebraic projective orthogonality preservers

- **Record:** Leiba Rodman and Peter Šemrl, “Orthogonality preserving bijective
  maps on finite dimensional projective spaces over division rings,”
  *Linear and Multilinear Algebra* 56(6), 647–664 (2008),
  [DOI 10.1080/03081080701395772](https://www.tandfonline.com/doi/abs/10.1080/03081080701395772).
- **Consultation:** publisher metadata and abstract verified 2026-10-05;
  full text not audited.
- **Support role:** positioning of the algebraic preserver problem.
- **Affected chapters:** 19A.2; preserver supplement §3.
- **Boundary:** no theorem is imported from the abstract. The supplement
  supplies its own coordinate proof for the positive Gaussian-rational
  carrier, global bijection and dimension hypotheses.

### REF-NORM-001 — Gaussian integers and two squares

- **Record:** Keith Conrad, [*The Gaussian Integers*](https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf),
  Theorems 9.6 and 9.10, pp. 32–34.
- **Consultation:** primary PDF statements and proofs checked 2026-10-05.
- **Support role:** prime two-square representation and the integer
  two-squares criterion. The supplement extends the criterion to positive
  rational norms by using a reduced numerator and denominator.
- **Affected chapters:** 19A.3; preserver supplement §§4–5.
- **Boundary:** standard number theory, not a new WDP result. The Lean
  arithmetic corollary explicitly assumes the rational two-squares
  equivalence; concrete factorization and norm witnesses are replayed
  separately in Rust and Python.

---

## I. Internal-source and publication records

Internal Carroll papers, repository encyclopedia entries, pull requests, Lean
modules, notebooks, and Zenodo records are not external primary literature.
They belong in a provenance/evidence manifest with exact revision, artifact
hash, statement, and replay command. They should not be mixed into this
bibliographic registry as though they independently validate the programme.

The source corpus currently names three Zenodo URLs in an observer-control
source and describes the quantum-carrier paper as a Zenodo release. Those
publication claims were not independently resolved into a complete current
record/DOI/custody table during this editorial pass. Until that table exists,
cite the local source revision for provenance and mark external publication
status `UNVERIFIED`.

---

## J. Audit state and future deepening

The original 80-entry audit identified concrete bibliographic records without
`UNRESOLVED` or `UNCONSULTED` states in that cohort. Later additions have their
own consultation status; section L retains five unconsulted supplied leads.
This is a metadata and scope distinction, not a claim that every source was
read end to end.
The consultation field of each entry remains the controlling statement.

Further work is deliberately separated from this release:

1. Before importing any additional external theorem, read its primary text,
   record an exact section/page/theorem anchor, and match every hypothesis.
2. Validate links periodically and archive stable versions only where licensing
   and repository policy permit.
3. Extend a machine-readable bibliography from this reconciled human registry;
   never infer or manufacture identifiers.
4. Deepen historical comparisons only when the monograph needs them; a
   publisher-record check alone does not support interpretive or priority
   claims.
5. Keep primary sources, reviews, internal papers, and nonclaim boundaries
   visibly distinct in every future citation.

---

## K. Causal models and relational observables (added 2026-10-06)

These seven records support the positioning added in §15.12 and Appendix O.6.
They were added after the 80-entry audit in section J. Their metadata was
checked against publisher, arXiv or catalogue records on 2026-10-06; no
theorem is imported from them.

### REF-CAUSE-001 — Structural causal models

- **Record:** J. Pearl, *Causality: Models, Reasoning, and Inference*, 2nd ed.,
  Cambridge University Press, 2009. ISBN 9780521895606.
- **Consultation:** `PRIMARY METADATA VERIFIED`; catalogue records checked.
- **Support role:** standard source for interventional and counterfactual
  queries in structural causal models.
- **Affected chapters:** 15.12.
- **Boundary:** supplies the query language, not an evaluation or authority
  packet for any application.

### REF-CAUSE-002 — Pearl's hierarchy

- **Record:** E. Bareinboim, J. D. Correa, D. Ibeling and T. Icard, "On Pearl's
  hierarchy and the foundations of causal inference," in *Probabilistic and
  Causal Inference: The Works of Judea Pearl*, ACM Books, 2022, pp. 507–556.
- **Consultation:** `PRIMARY METADATA VERIFIED`; author-hosted and book records
  checked.
- **Support role:** separation of associational, interventional and
  counterfactual query layers.
- **Affected chapters:** 15.12.
- **Boundary:** its layer results are not used as WDP theorems.

### REF-REL-001 — Einstein's general covariance

- **Record:** A. Einstein, "Die Grundlage der allgemeinen
  Relativitätstheorie," *Annalen der Physik* 49(7), 1916, 769–822.
- **Consultation:** `CORPUS CITATION; FULL TEXT NOT RECHECKED`.
- **Support role:** historical source of the point-coincidence argument.
- **Affected chapters:** Appendix O.6.
- **Boundary:** no physical theorem is derived in WDP from this citation.

### REF-REL-002 — Kretschmann's objection

- **Record:** E. Kretschmann, "Über den physikalischen Sinn der
  Relativitätspostulate, A. Einsteins neue und seine ursprüngliche
  Relativitätstheorie," *Annalen der Physik* 53, 1917, 575–614.
- **Consultation:** `PRIMARY METADATA VERIFIED`.
- **Support role:** the objection that general covariance alone has no
  physical content.
- **Affected chapters:** Appendix O.6.
- **Boundary:** historical positioning only.

### REF-REL-003 — Komar's intrinsic coordinates

- **Record:** A. Komar, "Construction of a complete set of independent
  observables in the general theory of relativity," *Physical Review* 111,
  1958, 1182. [DOI 10.1103/PhysRev.111.1182](https://doi.org/10.1103/PhysRev.111.1182).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** four invariant scalars used to label events.
- **Affected chapters:** Appendix O.6.
- **Boundary:** WDP uses only the finite-relation reading of event labels.

### REF-REL-004 — Relational observables

- **Record:** C. Rovelli, "What is observable in classical and quantum
  gravity?" *Classical and Quantum Gravity* 8(2), 1991, 297–316.
  [DOI 10.1088/0264-9381/8/2/011](https://doi.org/10.1088/0264-9381/8/2/011).
- **Consultation:** `PRIMARY METADATA VERIFIED`.
- **Support role:** relational (complete and partial) observables.
- **Affected chapters:** Appendix O.6.
- **Boundary:** no quantum-gravity claim is made.

### REF-REL-005 — Dressing-field method

- **Record:** J. T. François and L. Ravera, "Mechanics as a general-relativistic
  gauge field theory, and relational quantization," arXiv:2510.19845
  [physics.gen-ph], 2025. [arXiv](https://arxiv.org/abs/2510.19845).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`.
- **Support role:** the dressing-field construction of invariant variables.
- **Affected chapters:** Appendix P.4.
- **Boundary:** WDP checks only a finite group-action identity, not the field
  theory or its quantization.

---

## L. Supplied SciSpace leads (2026-10-08)

These are bibliographic leads from the supplied review synthesis, not verified
primary records. Both tested source hosts were denied by the environment
proxy; no primary abstract, full text or PDF was acquired. See the
[comparison questions](observation_scope_and_literature.md#6-primary-source-comparison-queue)
and [access inventory](../manifests/literature_access.json). No theorem is
imported from these unconsulted records.

### REF-SCI-001 — Semantic identity compression

- **Supplied record:** Simas, *Semantic Identity Compression: Zero-Error Laws, Rate-Distortion, and Neurosymbolic Necessity*. [Primary record URL](https://arxiv.org/abs/2601.14252).
- **Consultation:** `UNCONSULTED`; title, authors and version not independently
  verified. No primary-source theorem or comparison claim is supported.
- **Planned role:** see the explicit comparison queue in the observation-scope
  supplement; primary definitions and hypotheses must be read first.

### REF-SCI-002 — Inductive diagrams for causal reasoning

- **Supplied record:** Castello, Redmond and Kuper, *Inductive diagrams for causal reasoning*. [Primary record URL](https://arxiv.org/abs/2307.10484).
- **Consultation:** `UNCONSULTED`; title, authors and version not independently
  verified. No primary-source theorem or comparison claim is supported.
- **Planned role:** see the explicit comparison queue in the observation-scope
  supplement; primary definitions and hypotheses must be read first.

### REF-SCI-003 — Higher-order interaction trees

- **Supplied record:** Ayyam and Sammler, *HITrees: Higher-Order Interaction Trees*. [Primary record URL](https://arxiv.org/abs/2510.14558).
- **Consultation:** `UNCONSULTED`; title, authors and version not independently
  verified. No primary-source theorem or comparison claim is supported.
- **Planned role:** see the explicit comparison queue in the observation-scope
  supplement; primary definitions and hypotheses must be read first.

### REF-SCI-004 — Nonlocal perimeter limit

- **Supplied record:** Bungert and Stinson, *Gamma-convergence of a nonlocal perimeter arising in adversarial machine learning*. [Primary record URL](https://link.springer.com/article/10.1007/s00526-024-02721-9).
- **Consultation:** `UNCONSULTED`; title, authors and version not independently
  verified. No primary-source theorem or comparison claim is supported.
- **Planned role:** see the explicit comparison queue in the observation-scope
  supplement; primary definitions and hypotheses must be read first.

### REF-SCI-005 — LLM reasoning failures

- **Supplied record:** Song et al., *Large Language Model Reasoning Failures*. [Primary record URL](https://arxiv.org/abs/2602.06176).
- **Consultation:** `UNCONSULTED`; title, authors and version not independently
  verified. No primary-source theorem or comparison claim is supported.
- **Planned role:** see the explicit comparison queue in the observation-scope
  supplement; primary definitions and hypotheses must be read first.

## M. Guarded-schedule topology

### REF-MATH-013 — Permutohedral complexes and diagonal arrangements

- **Record:** Taras Panov and Vsevolod Tril, “Permutohedral complex and complements of diagonal subspace arrangements” (2025). [arXiv:2504.04183v1](https://arxiv.org/abs/2504.04183v1).
- **Consultation:** Construction 4.5, Theorem 4.6 and the arrangement convention in §2 were checked in the primary source, as recorded in `guarded_schedule_topology.md`; this entry carries that existing consultation record.
- **Support role:** prior identification of the task permutohedral complex with the arrangement complement.
- **Affected chapters:** Appendix P.22.
- **Boundary:** does not supply WDP's identification of its native event complex; that argument is in the deposited supplement.
