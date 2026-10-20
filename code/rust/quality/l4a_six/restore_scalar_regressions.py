"""Restore original scalar contract tests with explicit fallible-API adaptations.

AuthorityEffect: None. Preserve the interrupted survivor campaign separately.
"""
from datetime import datetime, timezone
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import re
import shutil
from native_scalar_probe import item
from replay import ROOT, RUST, digest, write


def main():
    old = ROOT / "evidence/quality/l4a_six/20261020T104119Z-scalar-activation/before/src/linear_algebra/scalars.rs"
    target = RUST / "src/linear_algebra/scalars.rs"
    current = target.read_bytes()
    assert b"mod retained_contract_challenges" not in current
    original = item(old.read_bytes().decode("utf8"), "mod tests {")
    adapted = original.replace("mod tests {", "mod retained_contract_challenges {", 1)
    adapted = adapted.replace(".conjugate()", ".try_conj().unwrap()")
    # Change only method calls and retain every original assertion and fixture.
    for match in reversed(list(re.finditer(r"\.(add|sub|mul)\(", adapted))):
        opening = match.end() - 1
        depth = 1
        end = opening + 1
        while depth:
            depth += (adapted[end] == "(") - (adapted[end] == ")")
            end += 1
        adapted = adapted[:end] + ".unwrap()" + adapted[end:]
        adapted = adapted[:match.start()] + ".try_" + adapted[match.start() + 1:]
    for expression in ("zero.try_inv()", "z.try_inv()", "z.try_div(w)"):
        adapted = adapted.replace("assert_eq!(" + expression + ", None);",
            "assert_eq!(" + expression + ", Err(ScalarError::DivisionByZero));")
    adapted = adapted.replace("// zero inversion is None", "// zero inversion is a typed refusal")
    assert original.count("#[test]") == adapted.count("#[test]") == 9
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-scalar-regression-restoration"
    out = ROOT / "evidence/quality/l4a_six" / stamp
    out.mkdir()
    _copy_record_file(__file__, out / "restore.py")
    (out / "before.rs").write_bytes(current)
    (out / "original_tests.rs").write_bytes(original.encode("utf8"))
    (out / "adapted_tests.rs").write_bytes(adapted.encode("utf8"))
    target.write_bytes(current + b"\n\n#[cfg(test)]\n" + adapted.encode("utf8") + b"\n")
    (out / "after.rs").write_bytes(target.read_bytes())
    write(out / "restoration.json", {"AuthorityEffect": "None", "source": "code/rust/src/linear_algebra/scalars.rs",
        "before_sha256": digest(out / "before.rs"), "after_sha256": digest(target),
        "original_source": {"path": str(old.relative_to(ROOT)), "sha256": digest(old)},
        "tests_restored": re.findall(r"#\[test\]\s+fn (\w+)", adapted),
        "adaptations": ["Rename module to avoid collision with new scalar protocol tests.",
            "Replace old add/sub/mul and conjugate calls by checked try_* plus explicit unwrap on admitted fixtures.",
            "Change three zero inverse/division expectations from None to typed DivisionByZero.",
            "Keep every original fixture and assertion, including literal hash frames and both Gaussian component roles."],
        "survivor_campaign": "evidence/quality/l4a_six/20261020T104923Z-mutations/INTERRUPTION.json",
        "scope": "Test restoration only. Production code is unchanged; current integrated metrics/baselines/challenges must be refreshed."})
    print(out, flush=True)


if __name__ == "__main__":
    main()
