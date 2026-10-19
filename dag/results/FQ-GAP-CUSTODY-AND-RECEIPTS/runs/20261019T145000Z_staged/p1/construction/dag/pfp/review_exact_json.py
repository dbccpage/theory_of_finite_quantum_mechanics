"""Successor custody predicates for an explicitly sealed staged run.

The original domain checker still decides mathematical certificates. This
successor requires the complete construction-source set and the actual reviewed
request bytes; no status label or pin set is a theorem proof.
"""
from pathlib import Path
import hashlib
from exact_json import bound,load,require
def type_shape(value):
    if type(value) is dict:return {k:type_shape(v) for k,v in value.items()}
    if type(value) is list:return [type_shape(v) for v in value]
    require(type(value) in (str,int,bool,type(None)),'G1_SCHEMA:unsupported_review_shape')
    return {str:'str',int:'int',bool:'bool',type(None):'null'}[type(value)]
def require_type_shape(value,shape):
    if type(shape) is str:
        require(shape in ('str','int','bool','null') and type(value)=={'str':str,'int':int,'bool':bool,'null':type(None)}[shape],'G1_SCHEMA:reviewed_primitive_type');return
    if type(shape) is dict:
        require(type(value) is dict and set(value)==set(shape),'G1_SCHEMA:reviewed_object_shape')
        for k in shape:require_type_shape(value[k],shape[k])
        return
    require(type(shape) is list and type(value) is list and len(value)==len(shape),'G1_SCHEMA:reviewed_list_shape')
    for v,s in zip(value,shape):require_type_shape(v,s)
def audit_bound(request_path,candidate_path,task,config_path):
    config=load(config_path);request,candidate,public=bound(request_path,candidate_path,task)
    require(config['task_id']==task,'G1_SCHEMA:audit_task')
    attempt=request['attempt_id'];require(attempt in config['attempts'],'G5_SCOPE:unreviewed_attempt')
    expected=config['attempts'][attempt]
    require(hashlib.sha256(Path(request_path).read_bytes()).hexdigest()==expected['request_sha256'],'G5_SCOPE:unreviewed_request_bytes')
    require(type(candidate['source_pins']) is list and len(candidate['source_pins'])==len(expected['source_pins']),'G5_SCOPE:construction_source_coverage')
    require({p['path']:p['sha256'] for p in candidate['source_pins']}==expected['source_pins'],'G5_SCOPE:construction_source_identity')
    require_type_shape(candidate['data'],config['data_type_shape'])
    return request,candidate,public
