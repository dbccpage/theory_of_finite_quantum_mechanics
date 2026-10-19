"""Prepare one file-based PFP stage packet. No provider or proof checker is run.

Use the existing omega_engine_pfp prepare_finite_qm_turn/provider ports for paid
dispatch and native candidate checking. This helper retains per-target context
and refuses stage skipping; a receipt's reviewer identity remains the host's duty.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import yaml

SLOTS = (
    'slot_m1_layer0_ambient_carrier',
    'slot_m2_layer1_forward_morphisms',
    'slot_m3_layer2_ideals_and_annihilators',
    'slot_m4_tri_language_witness_anchors',
)
MODEL_STAGES = ('P0_MINE_OPERAD','P1_DERIVE','P3_REPAIR','P4_CHALLENGE')
FAILURE_CODES = {'G1_SCHEMA','G2_COCHAIN','G3_WITNESS','G4_COUNTERMODEL','G5_SCOPE'}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path):
    return yaml.safe_load(path.read_bytes())


def public_exact(value):
    if type(value) is dict:
        for key,item in value.items():
            if type(key) is not str or key.startswith('expected_') or key in {'ground_truth','oracle_answer','solution','host_diagnostics','judge_diagnostics'}:
                raise ValueError('private_or_expected_answer_in_public_input')
            public_exact(item)
    elif type(value) is list:
        for item in value:
            public_exact(item)
    elif type(value) not in (str,int,bool,type(None)):
        raise ValueError('exact_public_json_required')


def witness_schema(value):
    if type(value) is dict:
        if set(value) & {'default','example','examples'} or value.get('type') == 'number':
            raise ValueError('answer_instance_or_float_schema')
        for keyword in ('const','enum'):
            if keyword in value:
                choices=value[keyword] if keyword=='enum' else [value[keyword]]
                if any(type(x) is not str and x is not None for x in choices):
                    raise ValueError('fixed_numeric_or_boolean_answer')
        for key,item in value.items():
            if key not in ('const','enum'):
                witness_schema(item)
    elif type(value) is list:
        for item in value:
            witness_schema(item)


def reviewed_work(prompt, collection, reviewed_path, review_path):
    if reviewed_path is None or review_path is None:
        raise ValueError('reviewed_missions_and_host_review_required')
    reviewed=load(reviewed_path)
    review=load(review_path)
    if review.get('task_id') != prompt['node_id'] or review.get('review_status') != 'accepted_for_next_step':
        raise ValueError('host_review_binding')
    if review.get('reviewed_sha256') != digest(reviewed_path.read_bytes()):
        raise ValueError('stale_host_review')
    unit=reviewed['work_unit']
    if unit.get('schema_id') != 'omega.pfp.finite-qm-work-unit.v1' or unit.get('task_id') != prompt['node_id']:
        raise ValueError('work_unit_binding')
    if not unit.get('objective') or not unit.get('checker_id'):
        raise ValueError('target_and_checker_required')
    # An explicitly narrowed lemma must retain its relationship to the original target.
    if reviewed.get('original_target') != collection['target']['source_statement']:
        raise ValueError('original_target_binding')
    public_exact(unit)
    slots=unit.get('operad_slots',{})
    if set(slots) != set(SLOTS) or any(slots[k].get('mining_status') != 'FILLED' for k in SLOTS):
        raise ValueError('reviewed_four_missions_required')
    m1,m2,m3,m4=(slots[k] for k in SLOTS)
    if not m1.get('carrier') or not m1.get('coefficient_ring') or not m1.get('source_pins'):
        raise ValueError('carrier_ring_and_sources_required')
    root=Path(__file__).resolve().parents[2]
    for pin in m1['source_pins']:
        path=Path(pin['path'])
        if not path.is_absolute(): path=root/path
        if not path.is_file() or digest(path.read_bytes())!=pin['sha256']:
            raise ValueError('reviewed_source_pin_changed')
    if not m2.get('operations') or not m2.get('composition_plan'):
        raise ValueError('typed_operations_and_composition_required')
    entries={x['id']:x for x in reviewed.get('catalog',{}).get('entries',[])}
    selected=unit.get('selected_catalog_ids',[])
    if not selected or len(selected)!=len(set(selected)) or not set(selected)<=set(entries):
        raise ValueError('reviewed_operation_catalog_required')
    for op in m2['operations']:
        entry=entries.get(op.get('catalog_id'),{})
        if op.get('catalog_id') not in selected or not op.get('semantic_predicate'):
            raise ValueError('operation_semantics_required')
        if not isinstance(op.get('inputs'),list) or op.get('inputs')!=entry.get('inputs') or not op.get('output') or op.get('output')!=entry.get('output'):
            raise ValueError('operation_signature_mismatch')
    if not m3.get('algebraic_relations') or not m3.get('rejection_predicates') or not m3.get('negative_control_plan'):
        raise ValueError('relations_and_controls_required')
    if not m4.get('certificate_predicates') or not m4.get('anchors') or 'unpaid_imports' not in m4:
        raise ValueError('independent_certificate_contract_required')
    witness_schema(unit['answer_schema'])
    return reviewed


def build_packet(prompt_path: Path, stage_id: str='P0_MINE_OPERAD', *, attempt_id: str,
                 reviewed_path: Path | None=None, review_path: Path | None=None,
                 candidate_path: Path | None=None, host_check_path: Path | None=None):
    if stage_id not in MODEL_STAGES:
        raise ValueError('host_stage_not_a_model_dispatch')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*',attempt_id):
        raise ValueError('invalid_attempt_id')
    prompt=load(prompt_path)
    collection_path=(prompt_path.parent/prompt['operad_record']).resolve()
    collection=load(collection_path)
    if collection['node_id'] != prompt['node_id']:
        raise ValueError('collection_task_mismatch')
    workflow=load((prompt_path.parent/prompt['workflow']).resolve())
    contracts=load((prompt_path.parent/prompt['stage_contracts']).resolve())
    stage=next(s for s in workflow['stages'] if s['id']==stage_id)
    context={'original_target':collection['target'],'operad_collection':collection}
    if stage_id!='P0_MINE_OPERAD':
        reviewed=reviewed_work(prompt,collection,reviewed_path,review_path)
        context={'original_target':collection['target'],'reviewed_work':reviewed}
    if stage_id in ('P3_REPAIR','P4_CHALLENGE'):
        if candidate_path is None or host_check_path is None:
            raise ValueError('prior_candidate_and_host_check_required')
        check=load(host_check_path)
        if check.get('task_id')!=prompt['node_id'] or check.get('candidate_sha256')!=digest(candidate_path.read_bytes()):
            raise ValueError('candidate_host_check_binding')
        required='repairable_candidate_defect' if stage_id=='P3_REPAIR' else 'accepted_candidate_for_challenge'
        if check.get('status')!=required:
            raise ValueError('host_transition_not_authorized')
        # Raw prior responses stay on disk. Repair receives only bounded failure classes.
        if stage_id=='P3_REPAIR':
            failures=check.get('bounded_failure_codes',[])
            if not failures or not set(failures)<=FAILURE_CODES:
                raise ValueError('bounded_failure_classes_required')
            context['bounded_failure_codes']=failures
        else:
            context['accepted_candidate']=load(candidate_path)
    canonical=json.dumps(context,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    return {
        'schema_id':'omega.pfp.finite-qm.stage-packet.v1',
        'task_id':prompt['node_id'],'stage_id':stage_id,'attempt_id':attempt_id,
        'input_sha256':digest(canonical),'authority_effect':'None',
        'system_prompt':prompt['system_prompt'],
        'user_prompt':'Target: '+collection['target']['source_statement']+'\nStage: '+stage_id+'\n'+stage['instruction'],
        'public_context':context,
        'response_contract':{'every_stage':contracts['every_stage'],'stage':contracts['stages'][stage_id]},
        'checkpoint_directory':f"dag/results/{prompt['node_id']}/runs/{{run_id}}/{attempt_id}/",
        'dispatch_status':'prepared_only_no_provider_or_checker_executed',
    }


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prompt',type=Path)
    parser.add_argument('--stage',choices=MODEL_STAGES,default='P0_MINE_OPERAD')
    parser.add_argument('--attempt',required=True)
    parser.add_argument('--reviewed',type=Path)
    parser.add_argument('--host-review',type=Path)
    parser.add_argument('--candidate',type=Path)
    parser.add_argument('--host-check',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    packet=build_packet(args.prompt,args.stage,attempt_id=args.attempt,reviewed_path=args.reviewed,
        review_path=args.host_review,candidate_path=args.candidate,host_check_path=args.host_check)
    rendered=json.dumps(packet,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8',newline='\n') as stream:
            stream.write(rendered)
    else:
        print(rendered,end='')
