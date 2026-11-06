# Four-source inventory before the distinct-image closure

Inventory date: 2026-10-05. AuthorityEffect: None.
Baseline: `e2cd90471b89c543f2c240293a971f0ef61d98a1`, which was `origin/main` at fetch.
This record was written before the distinct-image and Chapter 23 corrections.
Model-response claims of closure are not evidence. Theorem identifiers keep the meanings in the source line cited here. A later correction uses a new identifier or an explicit correction label and does not silently strengthen the old ID.

Canonical manuscript: `witnessed_difference_programme.md`, abbreviated **MS**.
Evidence columns: **W** written proof, **E** executable checker, **M** mechanized Lean.
Dispositions: proved, corrected, refuted, conditional, open.

## 1. Chapter 23 (`chapter_23_toric_code_observer_completion.md`)

Carrier declared by `WDP-CH23-D01`: periodic lattice \(\Lambda=\mathbb Z_L\times\mathbb Z_L\), \(L\ge 3\); qubits on edges, \(n=2L^2\); Pauli space \(\mathcal P=\mathbb F_2^n\oplus\mathbb F_2^n\); weight \(\mathrm{wt}(e)=|\mathrm{supp}\,e_X|+|\mathrm{supp}\,e_Z|\). Stabilizers \(S\) are \(X\)-stars and \(Z\)-plaquettes. \(Q\) in the source is overloaded between the CSS commutation syndrome and a partial detector map \(Q_D\). Field: \(\mathbb F_2\). MS already contains this text after an imported-draft fence; that copy is not an accepted proof.

| ID | Location | Statement and quantifiers | MS | W / E / M | Dependencies and contradictions | Destination | Disposition |
|---|---|---|---|---|---|---|---|
| D01 | §23.1 | Packet \((\Lambda,S,D,T,P,E,q,B)\). All fields finite and declared. \(S\subseteq B=\ker q\). | copy under fence | W definition; E geometry in `toric_code_observer_completion.py`; M none | Weight convention later conflicts with the \(2L-1\) slogan in P07. | Corrected §23 / Appendix W | proved as a definition |
| D02 | §23.1 | Cumulative \(Q_{D,k}\) and, with no readout error, \(Q(e)=(Ae_X,A_ve_Z)\). | copy | W; E incidence matrices; M none | The following kernel proof uses ambient dimension \(2L^2\), not \(\dim\mathcal P=4L^2\). | Corrected syndrome definition | proved as a definition; the displayed single-round formula is the CSS commutation map |
| P01 | §23.2 | Claims \(\operatorname{rank} A=\operatorname{rank} A_v=L^2-1\), \(\ker Q=\mathrm{Cyc}\oplus\mathrm{Cut}\), \(S=\mathrm{Plaq}\oplus\mathrm{Star}\), \(\operatorname{rank} Q=2L^2-2\), \([\ker Q:S]=4\). The proof's last line computes \(2L^2-(2L^2-2)=2\). The prose then says both "two-dimensional" and \(\mathbb F_2^2\oplus\mathbb F_2^2\). | copy, explicitly not discharged | W contradictory; E ranks of \(A,A_v\) only; M none | Identifier P01 is not kept as "kernel \(=S\)" and is not kept as quotient dimension 2. Hygiene §23.12 says the full syndrome has kernel \(S\). | `WDP-CH23-P01C` | corrected |
| P02 | §23.2 | \(\min\{\mathrm{wt}(e):e\in\ker Q\setminus S\}=L\), with a weight-\(L\) vector in each sector. Proof is a sketch. | copy | W sketch; E weights of four named vectors equal \(L\) for \(L=3\); M none | Sketch mixes face boundaries with the graph cycle space. The winding invariants below repair the bound under D01's weight. | `WDP-CH23-P02C` | corrected |
| N01 | §23.2 | Textbook import note. | copy | none | Not a theorem. | retained note | open as attribution only |
| P03 | §23.3 | For homomorphisms \(Q,q\) and finite \(E\subseteq\mathcal P\), \(q|_E\) is a function of \(Q|_E\) iff \((E-E)\cap\ker Q\subseteq B=\ker q\). | copy | W complete for this equivalence; E `evaluate_observer_completion`; M fiber pattern only in `LocalObservationCompletion.lean`, not this carrier | The written \(\Rightarrow\) direction says \(e_1-e_2\in\ker Q\subseteq B\), which assumes the inclusion under proof. The converse construction is the sound half. | `WDP-CH23-P03C` | corrected |
| P04 | §23.3 | Recovery \(\rho\) with \(e+\rho(Qe)\in B\) for all \(e\in E\) iff the same inclusion. | copy | W; E recovery table; M none | Depends on a repaired P03. | `WDP-CH23-P04C` | corrected |
| P05 | §23.3 | A failed inclusion returns an admitted pair with equal syndrome and different \(q\). | copy | W; E dual witness; M none | The pair must be searched in \(E\), not manufactured from \(\dim(S^\perp/S)\). | `WDP-CH23-P05C` | proved after the search is required |
| P06 | §23.4 | For \(E_t=\{wt\le t\}\) and \(B=S\), the inclusion holds iff \(2t<L\), using P02 and \(E_t-E_t=E_{2t}\). | copy | W conditional on P02; E not a full ball check; M none | True for the full syndrome once distance \(L\) is proved. It does not by itself force every schedule to buy \(2L^2-2\) detectors. | `WDP-CH23-P06C` | conditional on the distance proof; the purchase reading is refuted |
| P07 | §23.4 | Distances of enlarged \(B_W\). Claims \(d_{\langle\bar X\bar Z\rangle}=2L-1\). | copy | W; E none for the diagonal; M none | Under D01's additive weight a two-sector class has distance \(2L\), not \(2L-1\). However, the separation distance governing fault tolerance is \(d_B = \min\{\mathrm{wt}(z) : z \in \ker Q \setminus B\} = L\), retaining \(2t < L\). | `WDP-CH23-P07C` | corrected |
| P08 | §23.4 | Says the diagonal question tolerates \(t\le L-1\), halves the lattice, and is factorially cheaper. | copy | W slogan; E none; M none | The claim \(t\le L-1\) fails because forbidden differences in \(\ker Q \setminus B\) have weight \(L\), giving a collision at \(L=3, t=2\); \(2t < L\) is retained. The halving and factorial sentences have no proof. | `WDP-CH23-P08C` | corrected; slogan and tolerance threshold refuted |
| D03 | §23.5 | Partial cumulative syndrome and dark rounds. | copy | W definition | Repeated rounds are not the same row without a state-evolution model. | retained with that limit | proved as a definition |
| P09 | §23.5 | Terminal-error convention: \((E-E)\cap\ker Q_D\subseteq B\). Spacetime convention is a different map. | copy | W; E partial schedules; M none | Sound for the convention it names. | retained | proved |
| D04, P10 | §23.5 | Omitted-stabilizer codimension and homological expansion. | copy | W; E none beyond rank; M none | A dropped independent check enlarges the kernel. It creates an admitted low-weight collision only when that new vector lies in \(E-E\). | `WDP-CH23-P10C` | corrected |
| N02 | §23.5 | Dark windows are fatal only when they create an unresolved admitted pair. | copy | W note | Consistent with P09. | retained | proved as a fence |
| D05 | §23.6 | Rational detector prices, nonnegative in the source and positive in the new obligation. | copy | W definition | The new procedure uses strictly positive rational costs. | corrected procedure | proved as a definition |
| P11 | §23.6 | For \(2t<L\) and \(B=S\), sufficiency iff full rank \(2L^2-2\), because "the full stabilizer syndrome has kernel \(S\)". | copy | W; E tests lock a full-rank spine, not \(t=0\); M none | The kernel is \(S^\perp\), not \(S\). Full rank \(2L^2-2\) is sufficient for \(1\le t\), \(2t<L\), \(B=S\), by the distance inclusion. It is not necessary: at \(L=3\) the face rows \(\{0,1,3,5,7,8\}\) have rank \(6\) and kill no weight-one column, and at \(L=4\) twenty-nine independent syndrome rows separate \(\mathcal E_1\). The claim is also false at \(t=0\). | `WDP-CH23-P11C` | corrected |
| D06, P12 | §23.6 | Linear matroid and greedy minimum-weight basis, only "provided that sufficiency is equivalent to full detector rank". | copy | W under that hypothesis; E no greedy proof; M none | The full-rank hypothesis fails for \(\mathcal E_t\) when \(1\le t\), \(2t<L\), and \(B=S\), by the same \(L=4\) suite. General \(E\) is a hitting-set problem. | `WDP-CH23-P12C` | hypothesis withdrawn for this regime; unrestricted use refuted |
| D07, P13 | §23.6 | Uniform cost minimum \(\|D\|=2L^2-2\), and every detector in a basis is essential. The proof says the quotient is two-dimensional. | copy | W; E asserts the count for a full question; M none | False at \(t=0\). For \(1\le t\) and \(2t<L\), rank \(2L^2-2\) is sufficient and need not be the minimum independent count; the strict saving exhibited here has $L=4,t=1$. The two-dimensional sentence contradicts the claimed index 4. | `WDP-CH23-P13C` | corrected |
| D08, D09, P14 | §23.7 | Primal recovery dictionary or dual admitted pair. | copy | W; E dichotomy tests; M none | Valid when the pair is taken from \(E\). | retained | proved |
| N03 | §23.7 | Zero duality gap only for the finite declared family. | copy | W note | Not a general pricing theorem. | retained | conditional |
| D10, D11, P15, N04 | §23.8 | Time envelope and a causal-cone lower bound under a declared cone. | copy | W conditional; E none; M none | A cone hypothesis is not a physical light-cone theorem. | retained as conditional | conditional |
| D12, D13, P16 | §23.9 | Noisy records and spacetime consistency. Probabilistic separation is not deterministic factorization. | copy | W; E none; M none | Classical bits do not imply physical non-disturbance. | retained with that fence | conditional |
| D14, N05 | §23.9 | \(R\ge L\) only inside the declared temporal chain model. | copy | W fence already present | Repeated rounds are not interchangeable rows. | retained | conditional |
| D15, P17 | §23.10 | Adaptive policies. Claims worst-case adaptivity cannot beat the nonadaptive threshold and that every transcript needs \(2L^2-2\) checks. | copy | W incorrect proof: the adversary is allowed to pick any kernel vector, not an element of \(E-E\); E none; M none | False for \(t=0\) and for a finite passive shelf whose branches use different instruments. | `WDP-CH23-P17C` | refuted as a universal claim; corrected scope supplied |
| P18 | §23.10 | Uniform adaptive cost at least \(2L^2-2\). | copy | W depends on P17; E none; M none | Same counterexamples. | `WDP-CH23-P18C` | refuted as a universal claim |
| N06 | §23.10 | Fence: not Bayesian, not probabilistic, not known-support. | copy | W note | The fence does not repair P17. | retained | open relative to those excluded tasks |
| D16, P19, P20 | §23.11 | Finite enumeration procedure and a complexity bound. | copy | W termination argument; E partial; M none | Termination is real. The kernel test must use \(E-E\), not global rank alone. | retained and implemented | proved for finite instances |
| §23.12 | hygiene | Says the full syndrome has kernel \(S\) and that adaptivity does not lower the check count. | copy | contradicts P01's index-4 sentence and the \(t=0\) case | Replaced by the corrected hygiene in Appendix W. | corrected | refuted |

## 2. Locality (`unified_lieb_robinson_observer_completion_derivation.md`)

Field and carrier are stated per theorem. MS §10.7 and §20.11 summarize these theorems and point at this file. A link is not integration. Older bytes in `docs/source_archive/locality_and_smearing/` are the submitted draft, not this corrected text.

| ID | Location | Carrier, assumptions, quantifiers | MS | W / E / M | Dependencies | Destination | Disposition |
|---|---|---|---|---|---|---|---|
| L1 | §1 | Finite \(E\subseteq V=\mathbb F_2^n\), subspace \(B\le\ker Q\), \(Q:V\to\mathbb F_2^m\). Decoder on \(Q(E)\) succeeds for every admitted error iff equal syndromes imply \(e+f\in B\). | summary plus link | W complete; E `locality_smearing`; M `decoder_iff` and one binary decoder | Does not prove Knill–Laflamme. | Appendix T of MS | proved |
| L2 | §1 | Extra rows annihilate \(B\). Minimum hitting suite on the finite forbidden set. If \(E\) is a subspace containing \(B\), the minimum is \(\dim(\ker(Q|_E)/B)\). | summary plus link | W; E one \(n=3\) example; M concrete decoder only | Dimension formula is not claimed for arbitrary \(E\). | Appendix T | proved in the stated regimes |
| L3 | §2 | Equal joint marginals on \(R\), \(\|O-O_R\|_\infty\le\beta\), then the readout difference is at most \(2\beta\). Lieb–Robinson input is an imported hypothesis, not a derived Hamiltonian bound. | summary | W; E Bell sharpness check; M rational consequence `local_readout_bound` | An upper bound is not an error floor. Equal single-site marginals are not the hypothesis. | Appendix T | proved as a finite readout bound; analytic LR hypothesis conditional |
| L4 | §3 | \(\delta\le 2\alpha+\kappa\eta\). If \(\eta\le 2\beta\) and \(\delta>2\alpha\), stable decoding needs the conditioning price. | summary | W; E refusal controls; M `conditioning_bound`, `common_report_error` | Not a device error floor. | Appendix T | proved |
| Bell, gauge, star exchange, upper envelope | §4 | Finite counterexamples: single-site marginals lose \(X\otimes X\); gauge gradients preserve a cycle; six CAR signs multiply to \(-1\); an upper bound does not force a positive error. | summary | W; E replay; M sign and triangle identities | CAR locality is a configuration-graph declaration. | Appendix T | proved as counterexamples |
| §5–6 scope | end | No MUB6 resolution, no Majorana device, no physical error floor. | partial | W fences | — | Appendix T | proved as nonclaims |

## 3. Trotter (`trotter_cochain_extinction_derivation.md`)

Carrier: \(L=4\) CAR sites, 16-dimensional Fock space, \(\theta\in(0,1]\), \(M\ge 1\), \(r=\theta/M\), \(N=2M\), response matrix size \(8M\), quadratic normalization \(1/(LN^2)\). MS §20.12 summarizes and links. The old archive draft is not this proof.

| ID | Location | Assumptions and quantifiers | MS | W / E / M | Dependencies and non-implications | Destination | Disposition |
|---|---|---|---|---|---|---|---|
| Finite spectra | §2 | Inertias at \(\theta=1/10\), \(M=1,2,3,4\) only. \(M=1\) eigenvalue \(-1/706440\). | summary | W table; E congruence replay; M integer matrix for \(M=1\) in `CARResponseWitness.lean` | Four inertias are not an all-\(M\) formula. \(r=1/10\) is outside \(r\le 1/192\). | Appendix U | proved for those four \(M\) |
| Pairing | §3 | If adjacent samples differ by at most \(D/N\), then \(\|\bar A\|\le D/(4M)\), sharp for \(\psi_j=j/N\). | summary | W; E alternating average; M pairing inequality | — | Appendix U | proved |
| Compressed all-\(M\) | §3 | For the rank-one channel along \(v_{j,x}=(-1)^j\), \(\|q_{v,M}\|\to 0\) using \(\|K_j\|\le e^{4\theta}\). | summary | W; E envelope arithmetic; M not the operator exponential | This is one compressed channel, not full \(q_M\) positivity and not all-\(M\) inertia. | Appendix U | proved for that channel |
| T1 | §4 | Fixed \(L=4\), \(C^1\) periodic profiles, explicit \(A_\theta(B,D)/M\) envelope against the continuous kernel \(Q_\theta\). | summary plus link | W complete; E rational majorant for the constant profile; M not the Duhamel estimate | No spatial continuum. | Appendix U | proved; analytic steps written-only |
| T2 | §5 | \(Q_\theta(\psi)\ge 0\) for real symmetric \(H\) and real \(C^1\) sources, by the finite thermal spectral expansion. | summary | W; E not a general spectral check; M none for the Fourier argument | Positivity is not Gaussianity. | Appendix U | proved; written-only |
| T3 | §5 | A supplied margin \(m>0\) gives \(q_M>0\) for every \(M\ge\lfloor A/m\rfloor+1\). Constant profile \(m\ge 1/(4e^{4\theta})\). | summary | W; E strict threshold; M margin arithmetic | The margin is profile-specific. | Appendix U | proved; analytic comparison written-only |
| T4 | §6 | Adapter factors through \(C^1/B\) iff it kills \(B\). Low-pass alone need not. Subdivision isometry uses the weighted \(L^2\) convention. | summary | W; E cochain tests; M quotient identities | Factorization is not a physical repair. | Appendix U | proved |
| §7 boundaries | end | All-\(M\) inertia, infinite volume, joint spacetime reconstruction, cumulants, Gaussian limits, and native repair bindings stay open. | summary | W | — | Appendix U | open |

## 4. G3/G4 (`meron_field_limit_derivations/`)

These files are a model-response archive plus one exact Gate E checker. Appendix O of MS already keeps separate analytic hypotheses. This closure does not enlarge the Meron programme. "CLOSED" and "ESTABLISHED" labels in model responses are proposals.

| ID | Location | Carrier and region actually used | MS | W / E / M | Contradiction | Destination | Disposition |
|---|---|---|---|---|---|---|---|
| Gate E | `gate_e_exact_refutation.md`, `code/gate_e_exact_counterexample.py`, receipt JSON | One point \(L=4\), \(M=1\), \(r=1/10\). \(\lambda_{\min}=-1/706440\), \(v^\top Gv=-1/88305\), vector \((-1,-1,-1,-1,+1,+1,+1,+1)\), not PSD. | Appendix O mentions the point; the proof is not the receipt | W for this point; E the checker and frozen receipt; M none of the 16-dimensional trace | \(r=1/10\not\le 1/192\). The receipt does not state \(\lambda_{\min}\sim -r^4/9\) and does not state all finite \(M\). | Appendix U / O boundary | proved at one point; universal readings refuted |
| Theorem A | `meron_spacetime_field_theorems.md` §4 | Continuous-time Gaussian field on \(\mathbb T^2\). | Appendix O has related written limits under its own hypotheses | W is a model synthesis; E none for the field limit; M none | A Gaussian limit is not the Gate E matrix and not a probability characteristic function merely by writing a signed generating function. | open boundary in MS | open |
| Theorem B | same §8 | Discrete-to-continuum partition convergence. | not this closure | model text | Fixed-carrier time limits in T1 are not this joint limit. | open | open |
| Gate D | dossier and §6 | Complex polydisk \(\|z\|\le 1/64\), Kotecký–Preiss numerical criterion. | not re-proved here | model text claims closure | The numerical criterion is not rechecked in this closure. | source proposal | open |
| Gate F / Lemma A | dossier §3 | Spacetime Ursell bound. | not re-proved here | model text | Scorecard status is not a proof. | source proposal | open |
| Gate G | dossier §3 | Mode extinction. | explicitly not in the Gate E receipt | model text | Do not rename the missing estimate. | open | open |
| Static Gaussian and bounded time-labelled cumulants | Appendix O and the dossier's citations of those arguments | Only under the hypotheses those sections already state | already in MS as written results | W in Appendix O; E not a new field limit; M none | Euclidean covariance positivity is not a physical quantum reconstruction theorem. | left in Appendix O | conditional |
| Provider responses | `responses/*.md`, Fugu receipt JSON | Historical model output | not proofs | custody only | Must stay labeled as model responses. | retained in place | open |

Active code dependency: `docs/meron_field_limit_derivations/code/gate_e_exact_counterexample.py` is hashed by `locality_smearing` replay.

## 5. Outstanding target 1, before this derivation

`docs/five_outstanding_derivations.md` §1 asks for distinct images \(R=\operatorname{im} D_s\) and \(B=\operatorname{im} D_r\) over finite rational spaces, without \(R=B\). MS §10.6 and `code/observer_completion/` prove the equal-image counts \((r,k-r,k)\) only. That equal-image theorem keeps its meaning. The distinct-image statement is a new identifier, `WDP-DIM-1`, not a silent rewrite of §10.6.

Targets 2–5 in that note stay open, as do guarded-history coherence, unrestricted source refinement, physical reconstruction, and joint continuum foundations.

## 6. Dispositions after the closure

The pre-change rows above are unchanged. This section records where each accepted statement went. Written, executable, and mechanized evidence stay separate.

| Statement | Written | Executable | Mechanized | Disposition |
|---|---|---|---|---|
| WDP-DIM-1, distinct images, joint count \(m_{\mathrm{both}}=\dim K-\dim(K\cap B)+\dim T\) | Appendix T | `code/observer_completion/distinct_image.py`, replayed by `distinct_replay` | `DistinctImageCompletion.lean` proves the three example counts, the raw and quotient kernel criteria on those matrices, the annihilator obstruction, and the admissible preimage identity. It does not postulate the general theorem. | proved |
| Equal-image §10.6 counts \((r,k-r,k)\) | unchanged | unchanged `observer_completion.py` | unchanged | proved; not redefined |
| WDP-CH23-P01C, kernel \(S^\perp\neq S\), quotient dimension 4 | Appendix U | `commutation_kernel_report` | `ToricSyndromeCorrespondence.lean` at \(L=3\), plus the Nat identity for \(L\ge 1\) | corrected; old P01 text retained |
| Fiber criterion P03C and recovery witness | Appendix U | `admitted_collision`, `recovery_witness` | fiber pattern already in `LocalObservationCompletion.lean`; the toric matrices are the new encoding | corrected |
| Distance \(L\), diagonal distance \(2L\), threshold \(2t < L\); P08 slogans | Appendix U | weight of the exhibited logical at \(L=3\); collision counterexample at \(L=3, t=2\) | weight 3 and the flux dots at \(L=3\) only | P07C corrected (\(d_B = L \implies 2t < L\)); P08 slogans and \(t \le L-1\) refuted |
| Full rank \(2L^2-2\) is sufficient for \(1\le t\), \(2t<L\), \(B=S\); necessity is refuted by the \(L=3\) face rows \(\{0,1,3,5,7,8\}\) and the \(L=4\) rank-\(29\) suite; empty purchase at \(t=0\) | Appendix U | `suite_separates` and `admitted_collision` on the shipped syndrome | not the general-\(L\) purchase theorem | P06C, P11C, P13C corrected; the necessity sentence previously placed under those identifiers is withdrawn |
| Matroid greedy | Appendix U | exhaustive checker; no greedy shortcut in the new code | none | P12C withdraws the full-rank hypothesis for this \(\mathcal E_t\) regime |
| Adaptivity buys nothing | Appendix U | `passive_adaptive_gap` costs 6 and 4 | none | P17C and P18C refuted as universal claims; the all-zero full-rank branch is withdrawn |
| Cone radius and noisy spacetime complex | Appendix U | none beyond the fiber checker | none | P15C refuted as a failure certificate; P16C conditional on a supplied complex |
| L1–L4 | Appendix V, the complete copied proof | existing locality replay | `LocalObservationCompletion.lean` for the finite and rational consequences. Analytic L3/L4 hypotheses stay written-only. | proved on the stated carriers |
| T1–T4, pairing, margin, cochain descent | Appendix W, the complete copied proof | existing Trotter replay | `TrotterObservableFiltering.lean` and `CARResponseWitness.lean` for the finite consequences and the M=1 integer witness. Analytic estimates stay written-only. | proved on the fixed four-site carrier |
| Gate E at \(L=4\), \(M=1\), \(r=1/10\) | Appendix W.8 | historical receipt, not rewritten | none | proved as one point outside \(r\le 1/192\); not an all-\(M\) theorem |
| Theorem A, Theorem B, Gates D, F, G as model-response closures | Appendix W.8 names the missing estimates | Gate E checker remains the active code | none | open |

The destination letters in §§1–3 were assigned before the manuscript letters were fixed. They are not a second set of theorems. The landed letters are Appendix T for `WDP-DIM-1`, Appendix U for the Chapter 23 corrections `WDP-CH23-P01C` through `WDP-CH23-P18C`, Appendix V for the complete L1–L4 text, and Appendix W for the complete Trotter text and the Gate E boundary. Old identifiers keep the statements in the rows above.

Live derivation files and the G3/G4 tree stay in place. Replay still hashes them. Current bytes are copied under `docs/source_archive/wdp_distinct_image_closure_2026_10_05/`.
