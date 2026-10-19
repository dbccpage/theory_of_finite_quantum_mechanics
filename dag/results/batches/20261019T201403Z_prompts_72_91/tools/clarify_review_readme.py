from pathlib import Path
B=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics\dag\results\batches\20261019T201403Z_prompts_72_91')
p=B/'tools/finalize.py';t=p.read_text();old='Original failed attempts and setup refusals remain preserved.';new='Original failed attempts and setup refusals remain preserved. One P2 checkpoint lost output recording to disk exhaustion: its Rust exit status is explicitly unknown, and a fresh named retry supplies the accepted result. The actual work-unit hypotheses are added to reviewed ambient slots separately from the historical source assumption list, so an empty source list is not promoted into an assumption-free result.'
if old not in t:raise ValueError('Unexpected README template')
p.write_bytes(t.replace(old,new).encode());(B/'tools/clarify_review_readme.py').write_bytes(Path(__file__).read_bytes())
