# Description

A Lexically Filtered Meron-Cluster Benchmark: Exact Ground Truth, Mechanized Cancellation Lemmas, and a Pilot That Exposes Answer Leakage

Jeremy H. Carroll. Version 0.4.0, 2026-09-28.

This deposit contains a small, exactly solvable instance of the meron-cluster
mechanism for the fermion sign problem, machine-checked lemmas for it, and the
record of a pilot language-model run that cannot support a discovery claim. The
instance is a four-site periodic chain with 256 breakup graphs and 1,296
configurations, 192 of them negative. An exact oracle, written with SQLite and
rational arithmetic, finds that the 57 graphs containing a meron cluster cancel
exactly and that the other 199 give the signed sum Z = 912; an independent
transfer-matrix trace also gives 912. Lean 4 proofs cover the per-orbit
cancellation lemmas. A substring filter and five prompt builders present the
instance as a graph problem without twelve domain words. In the retained pilot,
five language models were accessed through OpenRouter with one run per model and
prompt type, and no unassisted prompt produced a passing answer (0 of 9). Every
pass came after the prompt contained the answer: the scorer's feedback states
that Z must equal 912 and gives the split into 57 cancelling and 199 surviving
subgraphs, and one prompt type also dictates the sign formula and the
cancellation step. Even the unassisted prompts state the configuration count and
the average sign, which fix Z. The paper describes the changes a valid rerun
needs; that rerun requires authorized live API calls and has not been made.
Extensions include finite 2D staggered Gross-Neveu (Z = 150) and 3D meron
string loop (Z = 310) cluster solvers with exact pairwise zero-sum
cancellation over rational arithmetic, alongside an OpenRouter multi-turn model
ladder benchmark operating over a 38-glyph wire format. The text is licensed
under CC BY 4.0 and the code under PolyForm Noncommercial 1.0.0.

