"""Strict exact-certificate IO and PFP task/stage/input custody.

Only the domain checker can accept mathematical predicates. This helper grants
no proof, completion, provider, policy or publication status.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def require(condition,message):
    if not condition:raise ValueError(message)


def _object(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'G1_SCHEMA:duplicate_key');result[key]=value
    return result


def _nonexact(value):
    raise ValueError('G1_SCHEMA:nonexact_json')


def load(path):
    return json.loads(Path(path).read_bytes(),object_pairs_hook=_object,parse_float=_nonexact,parse_constant=_nonexact)


def rational(value):
    require(type(value) is str,'G1_SCHEMA:rational_string')
    try:result=Fraction(value)
    except (ValueError,ZeroDivisionError) as error:raise ValueError('G1_SCHEMA:rational') from error
    require(str(result)==value,'G1_SCHEMA:canonical_rational')
    return result


def vector(value,size):
    require(type(value) is list and len(value)==size,'G1_SCHEMA:vector_shape')
    return [rational(x) for x in value]


def bound(request_path,candidate_path,task):
    request,candidate=load(request_path),load(candidate_path)
    require(type(request) is dict and request.get('schema_id')=='omega.pfp.finite-qm.stage-packet.v1','G1_SCHEMA:packet')
    require(request.get('task_id')==task and request.get('stage_id') in ('P1_DERIVE','P3_REPAIR'),'G1_SCHEMA:task_stage')
    require(type(request.get('attempt_id')) is str and bool(request['attempt_id']),'G1_SCHEMA:attempt')
    context=request['public_context'];work=context['reviewed_work']['work_unit']
    require(work['task_id']==task and context['reviewed_work']['original_target']==context['original_target']['source_statement'],'G1_SCHEMA:reviewed_target')
    digest=hashlib.sha256(json.dumps(context,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    require(digest==request['input_sha256'],'G1_SCHEMA:context_digest')
    require(type(candidate) is dict and set(candidate)=={'schema_id','task_id','stage_id','attempt_id','input_sha256','source_pins','data'},'G1_SCHEMA:certificate_fields')
    require(candidate['schema_id']=='finite-qm.domain-certificate.v1','G1_SCHEMA:certificate_schema')
    for key in ('task_id','stage_id','attempt_id','input_sha256'):
        require(candidate[key]==request[key],'G1_SCHEMA:binding')
    root=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file())
    pins=candidate['source_pins']
    require(type(pins) is list and bool(pins),'G1_SCHEMA:source_pins')
    names=[]
    for pin in pins:
        require(type(pin) is dict and set(pin)=={'path','sha256'},'G1_SCHEMA:source_pin')
        p=(root/pin['path']).resolve();require(p.is_relative_to(root) and p!=root,'G1_SCHEMA:path_escape')
        require(hashlib.sha256(p.read_bytes()).hexdigest()==pin['sha256'],'G5_SCOPE:construction_bytes')
        names.append(pin['path'])
    require(len(names)==len(set(names)),'G1_SCHEMA:duplicate_source_pin')
    return request,candidate,work['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']
