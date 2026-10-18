"""Smoke test for decomposed residuals/network_residual.py."""
import pytest
from omega_engine.crates.residuals.network_residual import (
    Network,
    build_incidence,
    residual_after_gauge_fix,
    GaugeFixResult,
)


def test_network_residual_smoke():
    net = Network(nodes=[0, 1], edges=[(0, 1)])
    assert net.nodes == (0, 1)
    res = residual_after_gauge_fix(net, {(0, 1): 1.0})
    assert isinstance(res, GaugeFixResult)
    assert res.is_pure_gauge


def test_old_coda_network_import_deleted():
    with pytest.raises(ImportError):
        import omega_engine.crates.coda.network_residual


