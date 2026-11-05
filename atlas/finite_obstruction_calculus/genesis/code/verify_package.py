"""Execute the standalone Python/Rust replay and the mechanized Lean encoder."""
import json

from reproduce import reproduce

if __name__ == "__main__":
    print(json.dumps(reproduce(lean_wire=True), indent=2))
