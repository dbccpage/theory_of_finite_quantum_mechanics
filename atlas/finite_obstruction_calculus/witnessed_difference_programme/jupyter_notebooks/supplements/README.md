# Derivation notebooks

[Trotter cochain extinction](100_trotter_cochain_extinction.ipynb) builds the
exact rational response matrix G^(2)_{4,M} and checks its 4M-1 zero modes
for M = 1, 2, 3. It needs `sympy` and runs from the paper root or this
directory.

[Certified preservers](110_certified_preservers.ipynb) replays Chapter 19A's
exact phase, Hadamard, reachability, postselection, qubit, finite graph and
generator examples. It retains eight executed cells. Rebuild and compare
outputs from the paper root and this directory with
`python scripts/build_preserver_notebook.py` from the paper root, in an
environment containing `nbformat`, `nbclient` and `ipykernel`.

This is a separately generated proof-supplement notebook. It does not change
the historical ten-lesson output-free curriculum, its canonical claim
bindings, or its execution receipt. The
[evidence guide](../../docs/derivation_evidence.md#certified-preservers-and-algebraic-generators)
distinguishes the notebook from native tests and Lean proofs.
