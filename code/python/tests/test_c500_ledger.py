from pathlib import Path
import copy,importlib.util,unittest
p=Path(__file__).resolve().parents[1]/'src/qm/c500_ledger.py';sp=importlib.util.spec_from_file_location('ledger',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def fixture():return {'gap':{'status':'RESOLVED_WITH_SCOPED_EVIDENCE','resolution':'RESOLVED','unresolved_targets':['C500-T301'],'open_or_invalid_bet_clauses':['M2']},'review':{'block':'block_01','launch_preconditions':'NOT_ESTABLISHED','supported_scope':'one finite example','targets':[{'id':'C500-T301','action':'prove original','required_exit_evidence':'proof','plan_target_satisfied':False}],'scores':[{'id':'M1','resolution':'SCOPED_EVIDENCE'},{'id':'M2','resolution':'OPEN'}]}}
class LedgerTests(unittest.TestCase):
    def test_scoped_status_does_not_discharge_original(self):self.assertEqual(m.summarize(fixture())['original_scope_evidence_ceiling'],'NOT_DISCHARGED_BY_EXAMINED_RECORDS')
    def test_positive_source_label_is_still_not_a_proof(self):
        x=fixture();x['review']['targets'][0]['plan_target_satisfied']=True;self.assertEqual(m.summarize(x)['original_scope_evidence_ceiling'],'SOURCE_LABEL_REQUIRES_INDEPENDENT_PROOF')
    def test_original_clause_identity_required(self):
        x=fixture();x['gap']['open_or_invalid_bet_clauses']=[]
        with self.assertRaises(ValueError):m.summarize(x)
    def test_duplicate_target_is_rejected(self):
        x=fixture();x['review']['targets']*=2
        with self.assertRaises(ValueError):m.summarize(x)
    def test_malformed_records_raise_typed_error(self):
        with self.assertRaises(ValueError):m.summarize({})
        with self.assertRaises(ValueError):m.summarize({'review': {}, 'gap': {}})
        bad = fixture(); bad['review']['targets'] = [{'id': 'T1'}] # missing fields
        with self.assertRaises(ValueError):m.summarize(bad)
        bad_score = fixture(); bad_score['review']['scores'] = [{'id': 'S1', 'resolution': 'UNKNOWN'}]
        with self.assertRaises(ValueError):m.summarize(bad_score)
if __name__=='__main__':unittest.main()
