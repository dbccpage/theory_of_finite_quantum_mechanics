"""Read-only replay of exact separator evidence and stage/source custody.

All acceptance guards are explicit, including under python -O. Native receipts
are retained executions, not fresh compiler runs or authority tokens.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode=True
RUN=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def safe(root,relative):
    p=(root/relative).resolve();require(p.is_relative_to(root.resolve()) and p!=root.resolve(),'custody:path_escape');return p
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def verify_inventory(run,manifest):
    rows=manifest['artifacts'];require(type(rows) is list and bool(rows),'custody:empty_manifest')
    names=[r['path'] for r in rows];require(len(names)==len(set(names)),'custody:duplicate_path')
    for row in rows:require(sha(safe(run,row['path']))==row['sha256'],'custody:artifact:'+row['path'])
    actual={p.relative_to(run).as_posix() for p in run.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json'}
    require(actual==set(names),'custody:inventory_changed')
    return len(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--working-sources',action='store_true');args=parser.parse_args()
    root=next(p for p in RUN.parents if (p/'dag/pfp/prepare_stage.py').is_file())
    manifest=read(RUN/'manifest.json');count=verify_inventory(RUN,manifest)
    if args.working_sources:
        for pin in manifest['working_sources']:require(sha(safe(root,pin['path']))==pin['sha256'],'custody:working_source:'+pin['path'])
    for stage in ('p0','p1','p3','p4'):
        packet=read(RUN/stage/'request.json')
        canonical=json.dumps(packet['public_context'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
        require(hashlib.sha256(canonical).hexdigest()==packet['input_sha256'],'binding:context:'+stage)
    missions=RUN/'p0/reviewed_missions.json';review=read(RUN/'p0/host_review.json')
    require(sha(missions)==review['reviewed_sha256'],'binding:mission_review')
    for pin in read(missions)['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['source_pins']:
        require(sha(safe(root,pin['path']))==pin['sha256'],'custody:mission_source')
    require(sha(safe(root,review['checker_pin']['path']))==review['checker_pin']['sha256'],'custody:checker_pin')
    checker=module('independent_separator_checker',RUN/'check_candidate.py')
    first=checker.check(RUN/'p1/request.json',RUN/'p1/candidate.json');accepted=checker.check(RUN/'p3/request.json',RUN/'p3/candidate.json')
    require(first['counts']==accepted['counts'],'binding:math_problem_changed_in_repair')
    rejected=read(RUN/'p2/host_check.json');passed=read(RUN/'p2_after_repair/host_check.json')
    require(rejected['candidate_sha256']==sha(RUN/'p1/candidate.json') and rejected['status']=='repairable_candidate_defect','binding:rejected_attempt')
    require(passed['candidate_sha256']==sha(RUN/'p3/candidate.json') and passed['status']=='accepted_candidate_for_challenge','binding:accepted_attempt')
    p3=read(RUN/'p3/request.json')
    require(p3['public_context'].get('bounded_failure_codes')==['G5_SCOPE'] and 'accepted_candidate' not in p3['public_context'],'binding:bounded_repair')
    for folder,kind,expected,success in [('p2','python',1,True),('p2','rust',1,True),('p2','rust_replay',1,True),
     ('p2','certificate',1,True),('p2','lean',5,False),('p2_after_repair','certificate',1,True),
     ('p2_after_repair','lean_recheck',2,True),('p5','protocol',1,True)]:
        receipt=read(RUN/folder/(kind+'_receipt.json'));require(type(receipt) is list and len(receipt)==expected,'native:missing_invocations:'+kind)
        require(all(type(r['exit_code']) is int for r in receipt),'native:invalid_exit_type')
        require(all(r['exit_code']==0 for r in receipt) if success else all(r['exit_code']==0 for r in receipt[:-1]) and receipt[-1]['exit_code']!=0,'native:unexpected_status:'+kind)
        for r in receipt:
            require(bool(r['argv']),'native:missing_command')
            require(safe(RUN,r['stdout']).is_file() and safe(RUN,r['stderr']).is_file(),'native:missing_logs')
    lean=(RUN/'p2_after_repair/logs/lean_recheck_1.stdout.log').read_text()
    require('sorryAx' not in lean,'native:unproved_accepted_anchor')
    for axioms in re.findall(r'depends on axioms:\s*\[(.*?)\]',lean,re.S):
        require({a.strip() for a in axioms.split(',')} <= {'propext','Classical.choice','Quot.sound'},'native:unapproved_axiom')
    for name in ['separator_iff_chsh','split_triple_exists','chsh_has_two_triples','full_family_joint_necessity']:
        require("'QuantumMechanics.BellSeparatorExtension."+name+"'" in lean,'native:missing_named_report')
    require('version 4.33.1' in (RUN/'p2_after_repair/logs/lean_recheck_0.stdout.log').read_text(),'native:Lean_version')
    candidate=read(RUN/'p3/candidate.json');lines=(RUN/'p2/logs/rust_replay_0.stdout.log').read_text().splitlines()
    require(len(lines)==len(candidate['cases']),'native:replay_count')
    for line,answer in zip(lines,candidate['cases']):
        row=line.split('\t');flat=answer['lower']+answer['upper']+answer['facets']
        flat+=([answer['separator']]+answer['triples'][0]+answer['triples'][1]+answer['weights']) if answer['status']=='extended' else [str(answer['violating_mask'])]
        require(row[:2]==[answer['id'],answer['status']] and list(map(Q,row[2:]))==list(map(Q,flat)),'native:cross_language_difference')
    p4=read(RUN/'p4/host_check.json');require(sha(RUN/'p4/candidate.json')==p4['candidate_sha256'],'binding:challenge')
    public=read(missions)['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']['cases'];public_by_id={p['id']:p for p in public}
    for mutant in p4['predicate_results']['mutants']:
        try:
            if mutant['id']=='duplicate_raw_key':checker.check(RUN/'p3/request.json',safe(RUN,mutant['candidate']))
            else:
                case=checker.load(safe(RUN,mutant['candidate']));checker.check_case(public_by_id[case['id']],case)
        except ValueError as error:require(str(error)==mutant['reason'],'challenge:wrong_failure_class')
        else:raise ValueError('challenge:mutant_accepted')
    control=read(RUN/'p4/two_sided_chsh_control.json')
    require(checker.check_case(control['case'],control['answer'])=='blocked','challenge:obstruction')
    require(abs(Q(control['standard_CHSH_value']))<=2 and Q(control['violated_facet_value'])>2,'challenge:two_sided_control')
    p5=read(RUN/'p5/candidate.json');require(p5['input_sha256']==sha(RUN/'p4/host_check.json') and p5['stop']=='user_review_requested','binding:final_stop')
    py=(RUN/'p2/logs/python_0.stderr.log').read_text();rust=(RUN/'p2/logs/rust_0.stdout.log').read_text();protocol=(RUN/'p5/logs/protocol_0.stderr.log').read_text()
    require(re.search(r'\bOK\s*$',py) and re.search(r'\bOK\s*$',protocol),'native:test_summary')
    rmatch=re.search(r'test result: ok\. (\d+) passed; 0 failed',rust);require(rmatch is not None,'native:Rust_summary')
    print(json.dumps({'artifacts_checked':count,'counts':accepted['counts'],'cross_language_cases':len(lines),
     'Python_tests':int(re.search(r'Ran (\d+) tests',py).group(1)),'Rust_tests':int(rmatch.group(1)),
     'PFP_protocol_tests':int(re.search(r'Ran (\d+) tests',protocol).group(1)),
     'repaired_kernel_anchors':4,'challenge_mutants_rejected':len(p4['predicate_results']['mutants']),
     'working_sources_checked':args.working_sources,'scope':'Integer separator reduction and exact finite Q witnesses; full formal rational Fine converse remains open.'},indent=2))


if __name__=='__main__':main()
