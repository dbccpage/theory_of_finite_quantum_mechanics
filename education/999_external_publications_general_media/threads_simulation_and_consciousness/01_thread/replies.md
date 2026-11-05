# Threads replies to wisdomandlogos

Revised 2026-11-05, second plain-prose pass. Jeremy asked for 3 to 5 terse replies in plain, clear reasoning, with no poetry and no in-house terms. This set is built on the plain set merged in #526. Each post is at most 500 characters; `code/self_audit_checks.py` (S5) counts them. What changed from #526, and why, is in [self_audit.md](../04_self_audit/self_audit.md) section H.

The five posts form one sequence and follow the order of her post: the human-versus-device line, the word "render", the paper she linked, the paper's math, and the standard any account has to meet. Post 5 carries the link to the full reconstruction of the paper.

Post 1, the observer

> You say the human-versus-device question misses the point. It is the point, because it is the one the experiment answers. Interference disappears whenever any device records which slit, whether or not a person ever reads the record. The effect follows the record, not a mind. If consciousness does the work, what changes when a person reads the record versus when nobody does? Who decides what counts as looking?

---

Post 2, the word "render"

> "Does not render" can mean three things: it is not shown, it does not change, or it is not stored. The first is true of anything unseen and predicts nothing. If it does not change, a clock left in an empty room would still show the time you left. It does not. If it is rebuilt perfectly whenever we look, no measurement can tell, and again the claim predicts nothing. Which one do you mean?

---

Post 3, what the paper says

> I read the paper you linked, appendices included. It proposes that coherent light from water in the brain stores memory as holograms, supported by a model and one simulation, not a measurement. "Render" never appears. It calls vision "perhaps the most important link between the outside world of the observable phenomena and the inner life of our mind", and how a quantum mind could perceive it "yet another mystery altogether". It does not make your claim.

---

Post 4, the paper's math

> Two of its derivations fail on its own terms. In Appendix A, the two conditions it imposes, fed into its own equation (A7), freeze the charge density, yet the light pulse it derives needs that density to oscillate. In a rerun of its simulation, Gauss's law is violated by more than the charge changes it reports. The 2.5 PB treats 2 mm of cortex as one uniform optical medium, and no energy barrier is given that would hold a memory for a year.

---

Post 5, the bar

> So here is the bar, the same one every account has to clear, mine included. Name one measurement that comes out differently if unobserved regions are not "rendered", and say what does the observing: a detector, a record, or an experience. Until then your account and ordinary physics predict the same data, and the data cannot choose. The paper, taken apart line by line: [link]

---

Before posting, replace `[link]` in post 5 with the reconstruction's public address. Post 5 is 378 characters with the placeholder, so the address may be up to 128 characters. The learning boards (`05_boards/learning_boards.html`) can be linked from the reconstruction.

Fact notes:
- "render" occurs 0 times in the paper.
- The vision sentence is from §6 (Concluding Remarks): "Vision is perhaps the most important link between the outside world of the observable phenomena and the inner life of our mind."
- "But how a quantum mind could perceive the macro-world is yet another mystery altogether" is from §5 (Discussion).
- The paper shows one simulated configuration (N = 4, Figures 4 to 6). It reports no measurement of its own.
- Double slit: interference is lost when which-path information is recorded in any physical system, whether or not a person reads it. This is textbook quantum mechanics, confirmed in many which-path experiments.
- Appendix A: $A^0 = 0$ with $\nabla\cdot\mathbf A = 0$, put into (A7), forces $\partial_t\lvert\varphi\rvert^2 = 0$. The pulse of (A38) needs the oscillating coherence. Checks S2a and `critique_checks.py` check 1.
- Appendix C: in our rerun of the paper's simulation, the Gauss-law residual is 1.1 to 2.3 times the charge change (`04_self_audit/retest_log.md`). The rerun matches the paper's density dips to within about 10%; nobody has compared it with the authors' code.
- 2.5 PB: the paper's inputs (a 2 mm cortex as one uniform optical medium, $n_r = 1.3$, 500 nm). A surface hologram over the same area holds about 0.5 TB (`03_critique/assumptions_mutation_audit.md` row Y1).
- Retention: one barrier needs $k_BT\ln(1\,\text{yr}/\tau_0)$, 1.2 eV for $\tau_0 = 1$ ps or 0.46 eV for 1 s. The paper gives no barrier (S3e, S3e2).
