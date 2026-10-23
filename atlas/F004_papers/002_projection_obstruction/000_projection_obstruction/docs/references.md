# Primary-source registry for *Projection Obstruction*

**Date:** 2026-10-11

**Scope:** Bibliographic and support-role registry for
`projection_obstruction.md`. A registry entry identifies a source and the claim
family for which it may be relevant. It does not prove a corpus-specific claim.

## Registry protocol

Each record has five fields:

- **Record:** canonical bibliographic information and a stable DOI, arXiv, or
  standards-body link when verified.
- **Consultation:** how much was checked for this synthesis.
- **Support role:** the narrow comparison or imported standard for which the
  source may be used.
- **Affected sections:** sections whose related-work or import ledger cite
  the source.
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

---

## Primary References

### REF-PO-001 — Lieb & Robinson (1972)
- **Record:** E. H. Lieb and D. W. Robinson, "The Finite Group Velocity of Quantum Spin Systems," *Commun. Math. Phys.* **28** (1972), 251–257.
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Historical and baseline group-velocity bounds for spin lattices.
- **Affected sections:** §1.2, §5.4.
- **Boundary:** Theorem 5.1 short-time defect does not invoke causal-cone truncation.

### REF-PO-002 — Mac Lane (1971)
- **Record:** S. Mac Lane, *Categories for the Working Mathematician*, Springer, 1971.
- **Consultation:** `OFFICIAL RECORD VERIFIED`
- **Support role:** Standard categorical definitions for diagrams, natural transformations, and functors.
- **Affected sections:** §2.1.
- **Boundary:** Abstract category theory does not establish metric convergence or dynamics.

### REF-PO-003 — Nachtergaele & Sims (2006)
- **Record:** B. Nachtergaele and R. Sims, "Lieb–Robinson Bounds and the Exponential Clustering Theorem," *Commun. Math. Phys.* **265** (2006), 119–130.
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Exponential clustering and locality bounds for quantum lattice dynamics.
- **Affected sections:** §1.2, §5.4.
- **Boundary:** Does not supply the exact short-time commutator coefficient.

### REF-PO-004 — Bravyi, Hastings & Verstraete (2006)
- **Record:** S. Bravyi, M. B. Hastings, and F. Verstraete, "Lieb–Robinson Bounds and the Generation of Correlations and Topological Quantum Order," *Phys. Rev. Lett.* **97** (2006), 050401.
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Correlation generation rate bounds and topological entanglement comparison.
- **Affected sections:** §1.2, §5.4.
- **Boundary:** Does not provide exact normal rates or local retraction geometry.

### REF-PO-005 — Carroll (2026, Zenodo 20564214)
- **Record:** J. H. Carroll, "M-Compatible Gauge Classification for Banach Presheaf Coboundaries: The $\ell^1$ Maximal-Symmetry Endpoint," Zenodo, 2026. [DOI 10.5281/zenodo.20564214](https://doi.org/10.5281/zenodo.20564214).
- **Consultation:** `OFFICIAL RECORD VERIFIED`
- **Support role:** Stage-2 functional-analytic classification of $\ell^1$ coboundary norm.
- **Affected sections:** §1.3, §4.1.
- **Boundary:** Does not prove lattice dynamics or finite Hamiltonian defect bounds.

### REF-PO-014 — Hall (2013)
- **Record:** M. J. W. Hall, "Correlation Distance and Bounds for Mutual Information," *Entropy* **15** (2013), 3698–3713. [DOI 10.3390/e15093698](https://doi.org/10.3390/e15093698).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Correlation distance definitions and trace-norm bounds on mutual information.
- **Affected sections:** §1.2, §5.11.
- **Boundary:** Product retraction distance is not generally the minimum trace distance over all products.

### REF-PO-015 — Haegeman et al. (2016)
- **Record:** J. Haegeman, C. Lubich, I. Oseledets, B. Vandereycken, and F. Verstraete, "Unifying time evolution and optimization with matrix product states," *Phys. Rev. B* **94** (2016), 165116. [DOI 10.1103/PhysRevB.94.165116](https://doi.org/10.1103/PhysRevB.94.165116).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** TDVP manifold projection and geometric time evolution.
- **Affected sections:** §1.2.
- **Boundary:** Does not establish finite obstruction cochain diagnostics.

### REF-PO-016 — Yang (2018)
- **Record:** I.-S. Yang, "The Entanglement Timescale," *Phys. Rev. D* **97** (2018), 066008. [DOI 10.1103/PhysRevD.97.066008](https://doi.org/10.1103/PhysRevD.97.066008).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Entanglement growth timescale comparisons.
- **Affected sections:** §1.2, §5.3.1.
- **Boundary:** Does not govern unentangled normal projection defect.

### REF-PO-017 — Cresswell (2018)
- **Record:** J. C. Cresswell, "Universal entanglement timescale for Rényi entropies," *Phys. Rev. A* **97** (2018), 022317. [DOI 10.1103/PhysRevA.97.022317](https://doi.org/10.1103/PhysRevA.97.022317).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Rényi entropy growth rates and universal short-time behavior.
- **Affected sections:** §1.2, §5.3.1.
- **Boundary:** Limited to entropy observables; does not cover local edge-tally obstruction.

### REF-PO-018 — Aaronson et al. (2013)
- **Record:** B. Aaronson, R. Lo Franco, G. Compagno, and G. Adesso, "Hierarchy and dynamics of trace distance correlations," *New J. Phys.* **15** (2013), 093022. [DOI 10.1088/1367-2630/15/9/093022](https://doi.org/10.1088/1367-2630/15/9/093022).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Trace distance correlation hierarchy and geometric distance from product states.
- **Affected sections:** §1.2, §5.11.
- **Boundary:** Does not supply dual witness certificates or local repair quotients.

### REF-PO-022 — OpenAI (2026, Metric Markov Cotype Two)
- **Record:** OpenAI, "Metric Markov Cotype Two of $\ell^1$," preprint, October 5, 2026.
- **Consultation:** `PRIMARY METADATA AND PRIMARY PDF VERIFIED`
- **Support role:** External extension premise $(E_K)$ in Proposition D.1.
- **Affected sections:** Appendix D.
- **Boundary:** Proof of $(E_K)$ is external; Proposition D.1 conditions on it explicitly.

### REF-PO-024 — Brunton et al. (2016)
- **Record:** S. L. Brunton, B. W. Brunton, J. L. Proctor, and J. N. Kutz, "Koopman Invariant Subspaces and Finite Linear Representations of Nonlinear Dynamical Systems for Control," *PLOS ONE* **11**(2) (2016), e0150171. [DOI 10.1371/journal.pone.0150171](https://doi.org/10.1371/journal.pone.0150171).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Finite Koopman invariant subspaces and linear lifting.
- **Affected sections:** §5.16.
- **Boundary:** Does not establish finite polynomial onset bounds for quantum lattices.

### REF-PO-025 — Hein, Eisert & Briegel (2004)
- **Record:** M. Hein, J. Eisert, and H. J. Briegel, "Multiparty entanglement in graph states," *Phys. Rev. A* **69** (2004), 062311. [DOI 10.1103/PhysRevA.69.062311](https://doi.org/10.1103/PhysRevA.69.062311).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Graph state definitions, local Clifford equivalence, and stabilizer correlations.
- **Affected sections:** §7.8.
- **Boundary:** Graph state entanglement does not resolve cycle repair differentials.

### REF-PO-026 — Chiribella, D'Ariano & Perinotti (2011)
- **Record:** G. Chiribella, G. M. D'Ariano, and P. Perinotti, "Informational derivation of quantum theory," *Phys. Rev. A* **84** (2011), 012311. [DOI 10.1103/PhysRevA.84.012311](https://doi.org/10.1103/PhysRevA.84.012311).
- **Consultation:** `PRIMARY METADATA AND ABSTRACT VERIFIED`
- **Support role:** Operational purification axiom and operational quantum foundations.
- **Affected sections:** Appendix E.
- **Boundary:** Purification selector is evaluated as a conditional axiom, not derived from obstruction data.

### REF-PO-027 — Murphy (1990)
- **Record:** G. J. Murphy, *$C^*$-Algebras and Operator Theory*, Academic Press, 1990.
- **Consultation:** `OFFICIAL RECORD VERIFIED`
- **Support role:** Standard finite-dimensional $C^*$-algebra structure theorems.
- **Affected sections:** Appendix E.2.
- **Boundary:** Classical reference; does not assert Jordan-Lie operational reconstruction.

### REF-PO-028 — Choi (1975)
- **Record:** M.-D. Choi, "Completely positive linear maps on complex matrices," *Linear Algebra and its Applications* **10** (1975), 285–290. [DOI 10.1016/0024-3795(75)90075-0](https://doi.org/10.1016/0024-3795(75)90075-0).
- **Consultation:** `OFFICIAL RECORD VERIFIED`
- **Support role:** Characterization of completely positive maps on matrix algebras.
- **Affected sections:** Appendix E.3, E.5.
- **Boundary:** Does not establish Jordan-algebraic operational classifications.
