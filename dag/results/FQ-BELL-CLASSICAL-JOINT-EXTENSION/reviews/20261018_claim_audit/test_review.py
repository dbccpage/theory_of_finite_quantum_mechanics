import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'dag/pfp/prepare_stage.py').is_file())
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T225117Z_operad_expectation'
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
strict=module('strict',HERE/'check_certificate.py')
verify=module('verify',HERE/'verify_review.py')


class ReviewChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.directory=Path(self.temp.name)
        self.request=json.loads((RUN/'p1/request.json').read_bytes())
        self.candidate=json.loads((RUN/'p1/candidate.json').read_bytes())
    def check(self):
        rp=self.directory/'request.json';cp=self.directory/'candidate.json'
        rp.write_bytes(json.dumps(self.request).encode());cp.write_bytes(json.dumps(self.candidate).encode())
        return strict.check(rp,cp)
    def test_original_numeric_witness_is_valid(self):
        result=self.check()
        self.assertEqual(result['checked_samples'],len(self.candidate['samples']))
        self.assertIn('separate host checks',result['scope_gate'])
    def test_duplicate_raw_keys_are_refused(self):
        path=self.directory/'duplicate.json'
        text=(RUN/'p1/candidate.json').read_text().replace('"chsh": "2"','"chsh": "999", "chsh": "2"',1)
        path.write_bytes(text.encode())
        with self.assertRaisesRegex(ValueError,'G1_SCHEMA:duplicate_key:chsh'):
            strict.check(RUN/'p1/request.json',path)
    def test_changed_context_with_matching_candidate_label_is_refused(self):
        self.request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']['required_anchors']=['missing.lean::made_up']
        self.candidate['anchors']=['missing.lean::made_up']
        with self.assertRaisesRegex(ValueError,'G1_SCHEMA:public_context_digest'):self.check()
    def test_all_nine_component_mutations_are_refused(self):
        from fractions import Fraction as Q
        original=copy.deepcopy(self.candidate)
        for field in ('chsh','positive_score_mass','negative_score_mass','lower_slack','upper_slack'):
            self.candidate=copy.deepcopy(original)
            self.candidate['samples'][0][field]=str(Q(self.candidate['samples'][0][field])+1)
            with self.assertRaisesRegex(ValueError,'G3_WITNESS:false_certificate'):self.check()
        for j in range(4):
            self.candidate=copy.deepcopy(original);self.candidate['samples'][0]['correlators'][j]='0'
            with self.assertRaisesRegex(ValueError,'G3_WITNESS:false_certificate'):self.check()
    def test_nonexact_and_malformed_values_are_refused(self):
        original=copy.deepcopy(self.candidate)
        for value in (True,1.0,'2.0','1/0','NaN'):
            self.candidate=copy.deepcopy(original);self.candidate['samples'][0]['chsh']=value
            with self.assertRaisesRegex(ValueError,'G1_SCHEMA:'):self.check()
    def test_negative_normalized_law_is_refused_even_after_rebinding(self):
        law=['3/2','-1/2']+['0']*14
        public=self.request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']
        public['cases'][0]['weights']=law;self.candidate['samples'][0]['weights']=law
        self.request['input_sha256']=strict.context_digest(self.request['public_context']);self.candidate['input_sha256']=self.request['input_sha256']
        with self.assertRaisesRegex(ValueError,'G3_WITNESS:law'):self.check()
    def test_scope_or_anchor_mismatch_is_refused(self):
        self.candidate['anchors']=['missing.lean::made_up']
        with self.assertRaisesRegex(ValueError,'G5_SCOPE:'):self.check()
    def test_empty_native_receipt_does_not_pass(self):
        with self.assertRaisesRegex(ValueError,'native:missing_invocations:lean'):
            verify.validate_receipts('lean',[],self.directory)
    def test_artifact_corruption_is_refused_with_python_optimization(self):
        p=self.directory/'data.txt';p.write_bytes(b'original')
        manifest={'artifacts':[{'path':'data.txt','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}
        verify.verify_inventory(self.directory,manifest)
        p.write_bytes(b'corrupted')
        manifest_path=self.directory/'manifest.json';manifest_path.write_text(json.dumps(manifest))
        source='import importlib.util,json,pathlib; s=importlib.util.spec_from_file_location("verify",'+repr(str(HERE/'verify_review.py'))+'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.verify_inventory(pathlib.Path('+repr(str(self.directory))+'),json.loads(pathlib.Path('+repr(str(manifest_path))+').read_text()))'
        result=subprocess.run([sys.executable,'-O','-c',source],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.assertNotEqual(result.returncode,0)
        self.assertIn(b'custody:digest:data.txt',result.stderr)


if __name__=='__main__':unittest.main()
