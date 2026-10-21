"""Smoke test for decomposed pipeline/certified_pipeline.py."""
import pytest
from omega_engine.crates.pipeline.certified_pipeline import (
    FingerprintedBag,
    Pipeline,
    Step,
    Tag,
    TransitionCert,
)


def test_certified_pipeline_smoke():
    bag = FingerprintedBag("input", {"key": "val"})
    assert len(bag.fingerprint()) == 64

    def dummy_transform(b: FingerprintedBag) -> FingerprintedBag:
        return FingerprintedBag("output", {"key": "val_modified"})

    step = Step("dummy_step", dummy_transform)
    out_bag, cert = step.run(bag)
    assert cert.is_valid()
    assert cert.step_name == "dummy_step"

    pipeline = Pipeline("test_pipe", [step])
    res_bag, certs = pipeline.run(bag)
    assert len(certs) == 1
    assert certs[0].is_valid()


def test_old_coda_import_deleted():
    with pytest.raises(ImportError):
        import omega_engine.crates.coda.certified_pipeline


