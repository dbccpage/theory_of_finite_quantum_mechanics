from __future__ import annotations

import json
import sys
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
_WDP_CODE = (
    _REPO_ROOT
    / "omega_engine_atlas"
    / "coda_atlas"
    / "F004_papers"
    / "001_finite_obstruction_calculus"
    / "000_witnessed_difference_programme"
    / "code"
)
if str(_WDP_CODE) not in sys.path:
    sys.path.insert(0, str(_WDP_CODE))

from witnessed_difference.calibration_composition import (
    AffineCalibrationStage,
    BoundedReading,
)
from witnessed_difference.measurement import (
    Calibration,
    CalibrationLink,
    IndicationValueMap,
    MeasurandSpecification,
    MetrologicalTraceability,
    NumericScale,
    Provenance,
    ReportedValue,
    measure,
)
from witnessed_difference.measurement_replay import (
    replay_composed_measurement,
    verify_measurement_replay,
)
from witnessed_difference.observation import (
    EvaluatorResult,
    EvaluatorStanding,
    EvaluatorStatus,
    Interaction,
    ObservationReceipt,
    classify_observation,
)
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from witnessed_difference.witness import Registration, make_witness


def witness() -> dict[str, object]:
    mark = {"indication": 2}
    registration = Registration("sensor", mark, 0)
    w_res = make_witness(registration, dict(mark), "E")
    assert isinstance(w_res, Accepted)
    obs = classify_observation(
        ObservationReceipt(
            Interaction(("sensor", "sample"), "sensor"),
            registration,
            w_res.value,
            EvaluatorResult("E", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING),
        )
    )
    assert isinstance(obs, Accepted)

    spec = MeasurandSpecification("declared quantity", "sample", ("finite trial",))
    reported = ReportedValue("display", -13)
    scale = NumericScale("scale", "declared-unit", Fraction(-100), Fraction(100), Fraction(1))
    cal = Calibration("cal", "scale", "E", Fraction(1))
    prov = Provenance(("registered", "reaccess matched"))
    trace = MetrologicalTraceability(
        (CalibrationLink("cal", "reference", "declared fixture", Fraction(1, 10)),),
        "reference",
        "declared_reference",
        "additive_upper_bound",
    )
    vmap = IndicationValueMap("composed", "sensor", "display", "indication", -6, -1)

    bad_neg_unc = measure(obs.value, spec, reported, scale, cal, Fraction(-1, 10), prov, trace, vmap)
    valid_meas = measure(obs.value, spec, reported, scale, cal, Fraction(7, 5), prov, trace, vmap)
    assert isinstance(valid_meas, Accepted)
    measurement = valid_meas.value

    stages = (
        AffineCalibrationStage("amplify", 2, 1, Fraction(1, 10), Fraction(1, 20)),
        AffineCalibrationStage("invert", -3, 2, residual_error=Fraction(1, 50)),
    )
    radius = Fraction(1, 10)
    replay = replay_composed_measurement(measurement, stages, radius, dict(mark))
    assert isinstance(replay, Accepted)
    verified = verify_measurement_replay(replay.value, measurement, stages, radius, mark)

    altered_meas = replace(measurement, corrected_value=Fraction(0))
    res_altered = replay_composed_measurement(altered_meas, stages, radius, mark)

    return {
        "goal_id": "REV-SMRM-P2-NUMERAL",
        "negative_uncertainty_refused": isinstance(bad_neg_unc, Refused)
        and bad_neg_unc.code is RefusalCode.INVALID_UNCERTAINTY,
        "valid_measurement_accepted": isinstance(valid_meas, Accepted),
        "enclosure_matches_expected": replay.value.corrected_enclosure
        == BoundedReading(-12, Fraction(3, 2)),
        "replay_verified": isinstance(verified, Accepted) and verified.value is True,
        "altered_record_refused": isinstance(res_altered, Refused)
        and res_altered.code is RefusalCode.CERTIFICATE_MISMATCH,
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
