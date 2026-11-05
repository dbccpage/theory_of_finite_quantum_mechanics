"""Compatibility entry point for the shared manifest/archive contract.

Without --check this refreshes both manifests and the deterministic archive.
With --check it verifies the exhaustive payload and complete archive.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rebuild_release import main

if __name__ == "__main__":
    raise SystemExit(main())
