"""Finite honeycomb computations retained after withdrawal of physical certificates."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))
from kitaev_honeycomb_evaluator import KitaevHoneycombModel

def test_finite_lattice_and_skew_matrix():
    model = KitaevHoneycombModel(lx=3, ly=3)
    assert len(model.sites) == 18
    assert len(model.links) == 27
    a = model.compute_majorana_hamiltonian()
    assert np.array_equal(a.T, -a)

def test_link_flip_agrees_with_full_plaquette_recomputation():
    model = KitaevHoneycombModel(lx=3, ly=3)
    index = model.gin_index
    for link in model.links:
        index.flip_link(link)
        incremental = {key: p.flux_wp for key,p in model.plaquettes.items()}
        index.recompute_all_fluxes()
        assert incremental == {key: p.flux_wp for key,p in model.plaquettes.items()}
    assert all(p.flux_wp in (-1, 1) for p in model.plaquettes.values())
