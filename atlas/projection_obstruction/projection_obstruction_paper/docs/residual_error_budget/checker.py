"""Check the two scalar witnesses; rejection checks survive Python -O."""
from fractions import Fraction
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from residual_error_budget import advance_budget, waiting_window, product_defect_interval


def check(folder: Path) -> dict:
    inputs = yaml.safe_load((folder / "input.yaml").read_text(encoding="utf-8"))
    names = {"error", "rate", "integration_reserve", "jump_reserve", "target", "horizon"}
    if type(inputs) is not dict or set(inputs) != names or any(type(x) is not str for x in inputs.values()):
        raise ValueError("inputs must contain exactly six rational strings")
    bounds = {key: Fraction(value) for key, value in inputs.items()}
    result = {"scope": "exact arithmetic on supplied bounds; no physical enclosure certified", "witnesses": []}
    for name in ("witness_valid.json", "witness_near_miss.json"):
        data = json.loads((folder / name).read_text(encoding="utf-8"))
        if (type(data) is not dict or type(data.get("expected_within_budget")) is not bool
                or type(data.get("duration")) is not str):
            raise ValueError("witness requires a rational duration string and boolean verdict")
        budget = advance_budget(bounds["error"], bounds["rate"], Fraction(data["duration"]),
                                bounds["integration_reserve"], bounds["jump_reserve"])
        accepted = budget <= bounds["target"]
        if accepted != data["expected_within_budget"]:
            raise ValueError("incorrect expected verdict: " + name)
        result["witnesses"].append(dict(file=name, budget=str(budget), accepted=accepted))
    result["waiting_window"] = str(waiting_window(bounds["target"], bounds["error"],
        bounds["integration_reserve"] + bounds["jump_reserve"], bounds["rate"], bounds["horizon"]))
    result["uncertainty_interval"] = [str(x) for x in product_defect_interval(2, Fraction(1, 50), Fraction(1, 150))]
    return result


def main() -> int:
    try:
        print(json.dumps(check(Path(__file__).parent), indent=2))
    except (OSError, ValueError, TypeError, KeyError, ZeroDivisionError, yaml.YAMLError) as error:
        print("FAIL:", error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

