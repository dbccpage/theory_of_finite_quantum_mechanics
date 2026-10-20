"""Independent PyYAML parsing and exact pair inventory. AuthorityEffect: None."""
import hashlib
import json
from pathlib import Path
import sys
import yaml

root = Path(__file__).resolve().parents[4]
folder = Path(__file__).parent
manifest = json.loads((folder / "sidecars.json").read_text(encoding="utf8"))
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

pairs = {}
for entry in manifest["sidecars"]:
    path = root / entry["path"]
    assert digest(path) == entry["sha256"]
    text = path.read_text(encoding="utf8")
    parsed = yaml.safe_load(text)
    assert parsed == json.loads(text.split("\n", 1)[1])
    source = parsed["artifact"]["path"]
    assert digest(root / source) == parsed["artifact"]["sha256"]
    role = "contract" if path.name.endswith(".contract.yaml") else "scoring"
    assert role not in pairs.setdefault(source, {})
    pairs[source][role] = parsed
groups = ("holonomy", "homology", "homotopy_type_theory", "lie_theory", "linear_algebra", "local_green_global_red_lggr")
subjects = {path.relative_to(root).as_posix() for group in groups
            for path in (root / "code/rust/src" / group).rglob("*")
            if path.is_file() and (path.suffix == ".rs" or path.name == "Cargo.toml")}
assert set(pairs) == subjects
for pair in pairs.values():
    assert set(pair) == {"contract", "scoring"}
    assert pair["contract"]["artifact"] == pair["scoring"]["artifact"]
    assert pair["contract"]["profile"] == pair["scoring"]["profile"]
receipt = {"AuthorityEffect": "None", "scope": "YAML/JSON parse agreement, complete pair inventory and source custody only; no engineering promotion.",
    "python": sys.version, "pyyaml": yaml.__version__, "command": ["py", "-3.9", str(Path(__file__).relative_to(root))],
    "script_sha256": digest(Path(__file__)), "sidecar_manifest_sha256": digest(folder / "sidecars.json"),
    "parsed_sidecars": len(manifest["sidecars"]), "complete_pairs": len(pairs), "exit_code": 0}
(folder / "yaml_validation.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf8")
print(json.dumps({"parsed_sidecars": receipt["parsed_sidecars"], "complete_pairs": len(pairs)}))
