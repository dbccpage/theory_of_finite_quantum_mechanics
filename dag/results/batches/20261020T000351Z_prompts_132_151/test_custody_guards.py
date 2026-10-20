"""Adversarial custody and exact primitive-type regressions for all twenty runs."""
import copy,json,tempfile,unittest
from pathlib import Path
import verify_batch as v
class Guards(unittest.TestCase):
    def setUp(self):
        self.rows=v.load(v.BATCH/'selection.json')['nodes']
    def mutate(self,fn,request=False,raw=None):
        with tempfile.TemporaryDirectory() as d:
            for i,row in enumerate(self.rows):
                run=v.ROOT/row['run'];checker=v.module('guards'+str(i),run/'check_candidate.py');p=run/v.load(run/'accepted.json')['attempt'];candidate=v.load(p/'candidate.json');r=v.load(p/'request.json');cpath=Path(d)/'candidate.json';rpath=Path(d)/'request.json'
                fn(r if request else candidate);cpath.write_text(json.dumps(candidate) if raw is None else raw(candidate),encoding='utf8');rpath.write_text(json.dumps(r),encoding='utf8')
                # Original request must remain byte-identical except in an explicit request mutation.
                if not request:rpath.write_bytes((p/'request.json').read_bytes())
                with self.assertRaises(ValueError,msg=row['node_id']):checker.check(rpath,cpath)
    def test_missing_pin(self):self.mutate(lambda c:c['source_pins'].pop())
    def test_duplicate_pin(self):self.mutate(lambda c:c['source_pins'].append(c['source_pins'][0]))
    def test_wrong_source_hash(self):self.mutate(lambda c:c['source_pins'][0].__setitem__('sha256','0'*64))
    def test_unsealed_request(self):self.mutate(lambda r:r.__setitem__('extra_reviewed_flag',True),request=True)
    def test_public_input_alias(self):self.mutate(lambda c:c['data']['records'][0]['input'].__setitem__(0,True))
    def test_output_boolean(self):self.mutate(lambda c:c['data']['records'][0]['output'].__setitem__(0,True))
    def test_float(self):self.mutate(lambda c:None,raw=lambda c:json.dumps(c).replace('"records":','"ignored_float":1.0,"records":',1))
    def test_duplicate_json_key(self):self.mutate(lambda c:None,raw=lambda c:'{"data":null,'+json.dumps(c)[1:])
    def test_wrong_stage(self):self.mutate(lambda c:c.__setitem__('stage_id','P5_RECORD'))
    def test_noncanonical(self):self.mutate(lambda c:c['data']['records'][0]['output'].__setitem__(0,'2/2'))
    def test_valid_controls(self):
        for i,row in enumerate(self.rows):
            run=v.ROOT/row['run'];c=v.module('valid'+str(i),run/'check_candidate.py');self.assertGreater(c.check(run/v.load(run/'accepted.json')['attempt']/'request.json',run/v.load(run/'accepted.json')['attempt']/'candidate.json')['records_checked'],0)
    def mutate_successor(self,change):
        value=copy.deepcopy(v.load(v.BATCH/'custody/pg_sn_header_successor/receipt.json'));change(value)
        with self.assertRaises(ValueError):v.audit_source_successor(value)
    def test_source_successor_valid(self):v.audit_source_successor()
    def test_source_successor_wrong_old_hash(self):self.mutate_successor(lambda d:d.__setitem__('historical_sha256','0'*64))
    def test_source_successor_wrong_current_hash(self):self.mutate_successor(lambda d:d.__setitem__('current_sha256','0'*64))
    def test_source_successor_boolean_header(self):self.mutate_successor(lambda d:d.__setitem__('historical_header_lines',True))
    def test_source_successor_boolean_binding(self):self.mutate_successor(lambda d:d.__setitem__('binding_index',True))
    def test_source_successor_boolean_line(self):self.mutate_successor(lambda d:d.__setitem__('current_declaration_line',True))
    def test_source_successor_wrong_node(self):self.mutate_successor(lambda d:d.__setitem__('node_id','OTHER'))
    def test_source_successor_wrong_collection(self):self.mutate_successor(lambda d:d.__setitem__('collection_path','dag/operads/other.yaml'))
    def test_source_successor_promoted_role(self):self.mutate_successor(lambda d:d['successor_entry'].__setitem__('role','proved_adjunction'))
if __name__=='__main__':unittest.main()
