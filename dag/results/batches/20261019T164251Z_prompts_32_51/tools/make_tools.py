from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');OLD=ROOT/'dag/results/batches/20261019T160201Z_prompts_22_31';B=ROOT/'dag/results/batches/20261019T164251Z_prompts_32_51'
def put(p,t):
    if p.exists():raise ValueError('Refuse overwrite '+str(p))
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(t.encode())
t=(OLD/'verify_batch.py').read_text().replace('[21:31]','[31:51]').replace('ordered next-ten','ordered next-twenty').replace('20261019_structure_audit','20261019_dynamics_audit');put(B/'verify_batch.py',t)
put(B/'test_custody_guards.py',(OLD/'test_custody_guards.py').read_text().replace('all ten runs','all twenty runs'))
t=(OLD/'tools/repair.py').read_text()
t=t.replace("names=list(dict.fromkeys(names+['lean4/E003_projection_fiber_primitive_difference.lean','lean4/E005_fiber_quotient_equivalence.lean']))", "names=list(dict.fromkeys(names))")
a=t.index("finding='Fresh P2");b=t.index("\ndelta['failed_compositions']",a)
t=t[:a]+"finding='Actual compiler diagnostics in the preceding retained P2 checkpoint require a proof repair. Keep the exact original numerical certificate and mathematical statement; do not promote the failed checkpoint.'"+t[b:]
t=t.replace("lean_dependencies=['E003_projection_fiber_primitive_difference','E005_fiber_quotient_equivalence','H000FinitePresentedCarrier']","lean_dependencies=[]")
put(B/'tools/repair.py',t)
t=(OLD/'tools/review.py').read_text();a=t.index('findings={');b=t.index('\nfor node in ',a)
t=t[:a]+"sys.path.insert(0,str(BATCH/'tools'));from specs import S\nfindings={x['kind']:[x['review']] for x in S}"+t[b:]
t=t.replace('20261019_structure_audit','20261019_dynamics_audit').replace("kind=='time'","kind=='stone'")
put(B/'tools/review.py',t)
t=(OLD/'tools/integrate.py').read_text().replace("tests.add('code/python/tests/test_phase_scope.py');tests.add('code/python/tests/test_structure_exact.py')", "tests.add('code/python/tests/test_phase_scope.py');tests.add('code/python/tests/test_structure_exact.py');tests.add('code/python/tests/test_dynamics_exact.py')")
t=t.replace("s.native.LIB/'PromptStructure.olean'),'PromptStructure.lean'", "s.native.LIB/'PromptDynamics.olean'),'PromptDynamics.lean'").replace('Ten shared Python tests are unique, not counted ten times.','Twenty shared Python tests are unique, not counted twenty times.')
put(B/'tools/integrate.py',t)
t=(OLD/'tools/git_prepare.py').read_text().replace('codex/pfp-prompts-22-through-31','codex/pfp-prompts-32-through-51');put(B/'tools/git_prepare.py',t)
t=(OLD/'tools/finalize.py').read_text().replace('20261019_structure_audit','20261019_dynamics_audit').replace('all_ten_staged_steps_reviewed','all_twenty_staged_steps_reviewed').replace('The next ten scoped','The next twenty scoped')
a=t.index("text='# PFP prompts");b=t.index("\n(BATCH/'README.md')",a)
t=t[:a]+'''text='# PFP prompts 32 through 51\\n\\nTwenty previously unrun prompts were executed locally through P0/P1/P2/P4/P5, with P3 only for actual failed native gates. Each run and review retains operad deltas, exact source snapshots, full native cross-language outputs and literal named kernel reports. This is one local Codex researcher, not an independent-author panel or external-provider transcript.\\n\\n| Prompt | Supported step | Remaining obligation |\\n|---|---|---|\\n'+'\\n'.join(table)+'\\n\\nThe review distinguishes exact retained finite computations from universal proofs and physical or continuum imports. Specific repairs/fences include: actual three-split path overcount instead of a two-term arithmetic proxy; compatibility without a claimed convergence certificate; Euler drift despite zero instantaneous squared-mass rate; class completeness versus Kraus completeness; all-rational polynomial-root exclusion instead of four-candidate testing; rejection of the fake 9/4 embedding with residual 1/16; and a genuine Bell partial-transpose negative witness in place of CP/Stinespring declaration flags. Source labels and original prompts remain unchanged historical annotations. Formal coordinate/matrix transports and full refined-carrier operad identity, substitution, symmetry and coherence remain open where stated.\\n\\nMeasured counts: '+json.dumps(counts,sort_keys=True)+'.\\n\\nFresh integration: '+json.dumps(integration,sort_keys=True)+'. Counts are unique tests and anchors, not sums of repeated gates. Retained failed checkpoints are included in the measured count and never promoted to passing. Pinned cached Mathlib is an import; no fresh full Mathlib build, full transitive dependency custody, whole-repository/hosted CI or completed physical reconstruction is claimed.\\n\\nRead-only exact/custody replay (checks saved compiler receipts and recomputes exact predicates):\\n\\n    py -3.9 -X utf8 verify_batch.py\\n    py -3.9 -X utf8 -O verify_batch.py\\n    py -3.9 -X utf8 test_custody_guards.py -v\\n\\nDedicated per-prompt README and scope_review.json files state the supported step and remaining obligations. Construction, review, native receipts and Git staging tools are retained here. Source digests bind bytes, not independent authorship. External provider calls: zero; chat cost unmeasured. GitHub merge state is verified separately. AuthorityEffect: None.\\n'
'''+t[b:]
put(B/'tools/finalize.py',t)
put(B/'tools/make_tools.py',Path(__file__).read_text())
print('Installed review, repair, replay, integration and sealing tools.')
