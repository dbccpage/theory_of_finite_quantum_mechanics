"""Put the flat ``code/ddc`` modules on the import path, relative to this file."""

import sys
from pathlib import Path

DDC_DIR = Path(__file__).resolve().parent.parent / "ddc"
if str(DDC_DIR) not in sys.path:
    sys.path.insert(0, str(DDC_DIR))
