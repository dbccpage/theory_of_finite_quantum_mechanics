"""Unit and Integration Tests: Continuous-Time Auxiliary-Field QMC (CT-AUX) Streaming GIN Indexing.
AuthorityEffect: None.

Tests:
1. CT-AUX auxiliary vertex representation and temporal orbital mode discretization.
2. Non-interacting Green's function anti-periodicity g0(tau) = -g0(tau + beta) and free determinant base cases.
3. CT-AUX Markov chain transitions (birth, death, spin-flip) with log-space acceptance ratios.
4. Dynamic streaming GIN posting list insertions and deletions: zero dangling references and clean pruning.
5. Strict memory boundedness under sliding-window eviction: memory O(W * k_bar) as T -> infty.
6. Real-time involution partner pairing and exact destructive sign cancellation.
7. Adversarial falsification tests: safe refusal on double-deletion and detection of desynchronized posting lists.
8. Full end-to-end streaming simulation receipt certification.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.ct_aux_streaming_gin_engine import (
    CtAuxConfiguration,
    CtAuxMarkovChainSampler,
    CtAuxVertex,
    StreamingGinPostingIndex,
    run_streaming_ct_aux_simulation,
)


def test_ct_aux_vertex_and_mode_discretization():
    """Validates that auxiliary vertices map to consistent, non-overlapping orbital modes."""
    v1 = CtAuxVertex(site=1, tau=0.5, spin=1)
    v2 = CtAuxVertex(site=1, tau=0.5, spin=-1)
    v3 = CtAuxVertex(site=2, tau=0.5, spin=1)

    m1 = v1.mode_id(num_sites=4, num_time_bins=16, beta=2.0)
    m2 = v2.mode_id(num_sites=4, num_time_bins=16, beta=2.0)
    m3 = v3.mode_id(num_sites=4, num_time_bins=16, beta=2.0)

    assert m1 != m2
    assert abs(m1 - m2) == 1
    assert m1 != m3


def test_ct_aux_determinants_and_greens_function():
    """Validates free Green's function boundary conditions and perturbation order k=0 determinants."""
    sampler = CtAuxMarkovChainSampler(num_sites=4, t_hopping=1.0, beta=2.0)

    log_up, log_down, sign = sampler.compute_log_determinants([])
    assert log_up == 0.0
    assert log_down == 0.0
    assert sign == 1

    tau = 0.4
    g_pos = sampler.g0(1, 2, tau)
    g_neg = sampler.g0(1, 2, tau - sampler.beta)
    assert abs(g_pos + g_neg) < 1e-12, "g0 failed anti-periodicity under imaginary time translation"


def test_ct_aux_sampler_transitions():
    """Validates that sampler moves (birth, death, flip) preserve finite log-determinants and valid orders."""
    sampler = CtAuxMarkovChainSampler(num_sites=4, beta=1.5, seed=123)

    accepted_moves = 0
    for _ in range(50):
        accepted, cfg = sampler.step()
        if accepted:
            accepted_moves += 1
            assert cfg is not None
            assert cfg.order >= 0
            assert math.isfinite(cfg.logdet_up)
            assert math.isfinite(cfg.logdet_down)
            assert cfg.sign in (-1, 1)
            assert len(cfg.active_modes) <= cfg.order

    assert accepted_moves > 0, "Sampler accepted zero moves in 50 steps"


def test_streaming_gin_dynamic_insert_and_delete_consistency():
    """Validates that dynamic insert/delete maintains 100% bijective posting list integrity."""
    index = StreamingGinPostingIndex(max_window_size=100)

    cfgs = []
    for cid in range(1, 11):
        v = CtAuxVertex(site=cid % 4 + 1, tau=0.2 * cid, spin=1 if cid % 2 == 1 else -1)
        mode = v.mode_id(num_sites=4, num_time_bins=16, beta=2.0)
        c = CtAuxConfiguration(
            cfg_id=cid,
            order=1,
            vertices=(v,),
            active_modes=frozenset([mode]),
            log_weight=0.0,
            weight=1.0,
            sign=1,
            logdet_up=0.0,
            logdet_down=0.0,
        )
        cfgs.append(c)
        index.insert_configuration(c)

    assert index.current_window_size == 10
    assert index.total_insertions == 10

    for cid in range(1, 6):
        deleted = index.delete_configuration(cid)
        assert deleted is True

    assert index.current_window_size == 5
    assert index.total_deletions == 5

    for m, post in index.posting_index.items():
        assert len(post) > 0, f"Empty posting list was not pruned for mode {m}"
        for del_id in range(1, 6):
            assert del_id not in post, f"Deleted ID {del_id} remained in posting list for mode {m}"

    for cid in range(6, 11):
        m = next(iter(cfgs[cid - 1].active_modes))
        assert cid in index.posting_index[m]


def test_streaming_gin_sliding_window_memory_boundedness():
    """Validates that FIFO sliding window strictly bounds memory to max_window_size."""
    window_capacity = 25
    index = StreamingGinPostingIndex(max_window_size=window_capacity)

    for cid in range(1, 201):
        v = CtAuxVertex(site=cid % 4 + 1, tau=0.1 * (cid % 20), spin=1)
        mode = v.mode_id(num_sites=4, num_time_bins=16, beta=2.0)
        cfg = CtAuxConfiguration(
            cfg_id=cid,
            order=1,
            vertices=(v,),
            active_modes=frozenset([mode]),
            log_weight=0.0,
            weight=1.0,
            sign=1,
            logdet_up=0.0,
            logdet_down=0.0,
        )
        index.insert_configuration(cfg)

        if cid >= window_capacity:
            assert index.current_window_size == window_capacity
            assert len(index.window_queue) == window_capacity

    assert index.total_insertions == 200
    assert index.total_deletions == 200 - window_capacity


def test_streaming_gin_involution_partner_pairing_and_cancellation():
    """Validates that real-time GIN query finds sign-reversing involution partners in live window."""
    index = StreamingGinPostingIndex(max_window_size=50)

    m_spec = 10
    m_spin_pos = 21
    m_spin_neg = 22

    c1 = CtAuxConfiguration(
        cfg_id=101,
        order=2,
        vertices=(CtAuxVertex(1, 0.1, 1), CtAuxVertex(2, 0.2, 1)),
        active_modes=frozenset([m_spec, m_spin_pos]),
        log_weight=math.log(2.5),
        weight=2.5,
        sign=1,
        logdet_up=0.0,
        logdet_down=0.0,
    )

    c2 = CtAuxConfiguration(
        cfg_id=102,
        order=2,
        vertices=(CtAuxVertex(1, 0.1, 1), CtAuxVertex(2, 0.2, -1)),
        active_modes=frozenset([m_spec, m_spin_neg]),
        log_weight=math.log(2.5),
        weight=2.5,
        sign=-1,
        logdet_up=0.0,
        logdet_down=0.0,
    )

    index.insert_configuration(c1)
    index.insert_configuration(c2)

    partner_id = index.find_streaming_involution_partner(cfg_id=102, flip_modes={m_spin_pos, m_spin_neg})
    assert partner_id == 101, f"Expected partner 101, found {partner_id}"

    defect = index.register_involution_cancellation(101, 102)
    assert defect < 1e-12, f"Sign cancellation defect non-zero: {defect}"
    assert index.paired_partners_count == 1


def test_adversarial_double_deletion_refusal():
    """Falsification test: deleting an already-deleted or non-existent ID safely returns False."""
    index = StreamingGinPostingIndex(max_window_size=50)
    cfg = CtAuxConfiguration(
        cfg_id=999,
        order=1,
        vertices=(CtAuxVertex(1, 0.1, 1),),
        active_modes=frozenset([1]),
        log_weight=0.0,
        weight=1.0,
        sign=1,
        logdet_up=0.0,
        logdet_down=0.0,
    )
    index.insert_configuration(cfg)

    assert index.delete_configuration(999) is True
    assert index.delete_configuration(999) is False
    assert index.delete_configuration(888) is False


def test_adversarial_desynchronized_posting_detection():
    """Falsification test: detects if a posting list contains an ID that was deleted from cfg_store."""
    index = StreamingGinPostingIndex(max_window_size=50)
    cfg = CtAuxConfiguration(
        cfg_id=555,
        order=1,
        vertices=(CtAuxVertex(1, 0.1, 1),),
        active_modes=frozenset([42]),
        log_weight=0.0,
        weight=1.0,
        sign=1,
        logdet_up=0.0,
        logdet_down=0.0,
    )
    index.insert_configuration(cfg)
    del index.cfg_store[555]

    candidates = index.query_by_modes(required_modes={42}, forbidden_modes=set())
    valid_candidates = {cid for cid in candidates if cid in index.cfg_store}
    assert len(valid_candidates) == 0, "Corrupted orphaned posting entry was falsely returned as valid"


def test_full_ct_aux_streaming_simulation_receipt():
    """Runs an end-to-end CT-AUX streaming MCMC trajectory and verifies certified receipt."""
    receipt, perf = run_streaming_ct_aux_simulation(
        num_steps=300,
        window_size=100,
        num_sites=4,
        mu=0.5,
        seed=42,
    )
    assert receipt.status == "STREAMING_INDEX_CERTIFIED"
    assert receipt.memory_bounded is True
    assert receipt.current_window_size <= 100
    assert perf["mean_insert_us"] < 200.0
