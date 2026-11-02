import pathlib
t=pathlib.Path("where_to_contest_multiverse_realism.md").read_text()
q=t[t.index("> Everett removes one rule"):]
q=q[2:q.index("\n")]
print(len(q), "chars")
