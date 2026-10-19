from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
HERE=Path(__file__).parent
def write(path,text):path.write_bytes(text.encode())
for filename,dest in [('bell_separator_extension.py','code/python/src/qm/bell_separator_extension.py'),
 ('test_bell_separator_extension.py','code/python/tests/test_bell_separator_extension.py'),
 ('BellSeparatorExtension.lean','lean4/BellSeparatorExtension.lean'),
 ('bell_separator_replay.rs','code/rust/src/finite_probability/examples/bell_separator_replay.rs')]:
    write(ROOT/dest,(HERE/filename).read_text())
write(ROOT/'code/rust/src/finite_probability/bell_separator_extension.rs',(HERE/'bell_separator_extension.rs').read_text()+(HERE/'rust_tests.rs').read_text())
p=ROOT/'code/rust/src/finite_probability/lib.rs';s=p.read_text();assert 'pub mod bell_separator_extension;' not in s
write(p,s.replace('pub mod bell_joint_extension;','pub mod bell_joint_extension;\npub mod bell_separator_extension;'))
p=ROOT/'lean4/lakefile.lean';s=p.read_text();assert '`BellSeparatorExtension,' not in s
write(p,s.replace('    `BellOperad,','    `BellOperad,\n    `BellSeparatorExtension,'))
print('Installed new separator modules, native tests, Rust replay, and Lean target.')
