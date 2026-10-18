from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
HERE=Path(__file__).parent
def write(path,txt): path.write_bytes(txt.encode())
p=ROOT/'code/python/src/qm/bell_joint_extension.py'
text=p.read_text();text+= (HERE/'python_add.py').read_text();write(p,text)
p=ROOT/'code/python/tests/test_bell_joint_extension.py'
text=p.read_text();text=text.replace('if __name__ == "__main__":\n    unittest.main()', (HERE/'python_tests_add.py').read_text()+'\n\nif __name__ == "__main__":\n    unittest.main()');write(p,text)
p=ROOT/'code/rust/src/finite_probability/bell_joint_extension.rs'
text=p.read_text().replace('    WrongCarrier,','    WrongCarrier,\n    #[error("the response map must have exactly 16 rows")]\n    WrongResponseCarrier,\n    #[error("response ({0},{1}) is not a canonical rational")]\n    InvalidResponseRational(usize, usize),\n    #[error("certificate does not match the supplied joint law")]\n    CertificateMismatch,',1)
text+=(HERE/'rust_add.rs').read_text();write(p,text)
write(ROOT/'lean4/BellOperad.lean',(HERE/'BellOperad.lean').read_text())
p=ROOT/'lean4/lakefile.lean';text=p.read_text().replace('    `BellClassicalJointExtension,','    `BellClassicalJointExtension,\n    `BellOperad,');write(p,text)
print('Installed P1 implementations, consumers, tests, and Lean construction.')
