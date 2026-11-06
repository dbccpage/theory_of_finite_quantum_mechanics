"""Explicit finite models used by transport regression fixtures."""
from coda_mur_core import DescentSquareCertificate


def finite_certificate(*args, **kwargs) -> DescentSquareCertificate:
    outputs = {"source_01": "artifact_01", "src_01": "art_01", "s": "art",
               "source": "art", "art_01": "obj_x", "art0": "art0_mapped"}
    kwargs.update(carrier=("source_01",),
        state_map=lambda x: outputs.get(x, x), observation_map=lambda x: 0,
        source_look=lambda x: 0, target_look=lambda x: 0)
    return DescentSquareCertificate(*args, **kwargs)
