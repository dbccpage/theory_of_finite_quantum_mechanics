"""Correct generic repair metadata in the review overlay, retaining raw stages."""
from pathlib import Path
B=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics\dag\results\batches\20261019T201403Z_prompts_72_91')
p=B/'tools/review.py';t=p.read_text();needle='    work_hypotheses=list('
insert='''    if kind=='majorana':
        for failed in delta['failed_compositions']:
            if 'Actual Majorana P2' in failed.get('reason',''):
                failed['historical_proposal_annotation']=failed['proposal']
                failed['proposal']='Accept AB-BA in an AB+BA anticommutator slot'
                failed['failure_predicate']='G3_WITNESS'
        delta['review_metadata_corrections']={'generic_P3_wrapper_annotation':'The historical wrapper called the submission uncompiled and used a G5_SCOPE repair tag. Actual P2 Lean compilation passed; the failing predicate was G3_WITNESS from the Rust sign/output mismatch. Raw P3 bytes are retained, and this review overlay states the corrected classification.'}
'''
if needle not in t:raise ValueError('Unexpected review state')
t=t.replace(needle,insert+needle);p.write_bytes(t.encode());(B/'tools/correct_repair_annotations.py').write_bytes(Path(__file__).read_bytes())
