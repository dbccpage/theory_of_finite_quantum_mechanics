from pathlib import Path
import shutil

STAGING=Path(__file__).resolve().parent
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-RATIONAL-VIOLATION-14-5/runs/20261019T015232Z_staged'
for name,relative in [('pfp_exact.py','code/python/src/qm/pfp_exact.py'),('rational_bell.py','code/python/src/qm/rational_bell.py'),('test_rational_bell.py','code/python/tests/test_rational_bell.py'),('pfp_exact.rs','code/rust/src/finite_probability/pfp_exact.rs'),('rational_bell.rs','code/rust/src/finite_probability/rational_bell.rs'),('rational_bell_replay.rs','code/rust/src/finite_probability/examples/rational_bell_replay.rs'),('PromptBellRational.lean','lean4/PromptBellRational.lean'),('exact_json.py','dag/pfp/exact_json.py')]:
    target=ROOT/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(STAGING/name,target)
shutil.copyfile(STAGING/'check_rational_bell.py',RUN/'check_candidate.py')
p=ROOT/'code/rust/src/finite_probability/lib.rs';s=p.read_text();s=s.replace('pub mod bell_separator_extension;','pub mod bell_separator_extension;\npub mod pfp_exact;\npub mod rational_bell;');p.write_bytes(s.encode())
p=ROOT/'lean4/lakefile.lean';s=p.read_text();s=s.replace('    `BellSeparatorExtension,','    `BellSeparatorExtension,\n    `PromptBellRational,');p.write_bytes(s.encode())
