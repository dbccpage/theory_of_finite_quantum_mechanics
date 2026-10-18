
import json
from pathlib import Path
from omega_engine.crates.majorana.engines.terminalizer import (
    D0_DEMO,
    D1_DEMO,
    RESIDUALS_DEMO,
    terminalize,
    write_ledger,
    demo_payload,
)
from omega_engine.crates.majorana.certificates.ledger import verify_ledger
from omega_engine.crates.majorana.evaluators.dashboard import calculate_dashboard_metrics

def main():
    for name, res in RESIDUALS_DEMO.items():
        result = terminalize(D0_DEMO, D1_DEMO, res)
        print(result["terminal_status"])

    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    ledger_path = artifacts_dir / "certificate_ledger.jsonl"
    write_ledger(ledger_path)

    verification = verify_ledger(ledger_path)
    verified = str(verification["verified"]).lower()
    print(f"ledger verified: {verified}")

    verification_path = artifacts_dir / "ledger_verification.json"
    with verification_path.open("w", encoding="utf-8") as f:
        json.dump(verification, f, indent=2)

    demo_out_path = artifacts_dir / "demo_output.json"
    with demo_out_path.open("w", encoding="utf-8") as f:
        json.dump(demo_payload(), f, indent=2)

    rows = []
    with ledger_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    calculate_dashboard_metrics(rows)
    print("dashboard generated")


if __name__ == "__main__":
    main()




