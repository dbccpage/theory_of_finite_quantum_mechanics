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
    def mutate_source_successor(self,change):
        receipt=copy.deepcopy(v.load(v.BATCH/'custody/finite_qm_source_successor/receipt.json'));change(receipt)
        with self.assertRaises(ValueError):v.audit_source_successor(receipt)
    def test_source_successor_valid(self):v.audit_source_successor()
    def test_source_successor_before_hash(self):self.mutate_source_successor(lambda r:r.__setitem__('historical_sha256','0'*64))
    def test_source_successor_after_hash(self):self.mutate_source_successor(lambda r:r.__setitem__('current_sha256','0'*64))
    def test_source_successor_missing_insertion(self):self.mutate_source_successor(lambda r:r['insertions'].pop())
    def test_source_successor_boolean_range(self):self.mutate_source_successor(lambda r:r['insertions'][0].__setitem__('start_line',True))
    def test_source_successor_missing_binding(self):self.mutate_source_successor(lambda r:r['collections'][0]['binding_indices'].pop())
    def test_source_successor_boolean_index(self):self.mutate_source_successor(lambda r:r['collections'][0]['binding_indices'].__setitem__(0,False))
    def test_source_successor_wrong_node(self):self.mutate_source_successor(lambda r:r['collections'][0].__setitem__('node_id','UNRELATED'))
    def test_valid_controls(self):
        for i,row in enumerate(self.rows):
            run=v.ROOT/row['run'];c=v.module('valid'+str(i),run/'check_candidate.py');self.assertGreater(c.check(run/v.load(run/'accepted.json')['attempt']/'request.json',run/v.load(run/'accepted.json')['attempt']/'candidate.json')['records_checked'],0)
if __name__=='__main__':unittest.main()
