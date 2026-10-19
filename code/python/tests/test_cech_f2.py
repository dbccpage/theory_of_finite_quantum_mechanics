import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/'src/qm/cech_f2.py';s=importlib.util.spec_from_file_location('cech',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
CONTEXTS=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8]]
def case(targets):return {'id':'test','measurements':9,'contexts':CONTEXTS,'targets':targets}
class CechTests(unittest.TestCase):
    def test_two_maps_are_not_conflated(self):
        c=m.certify(case([0,0,0,0,0,1]));self.assertEqual((c['incidence_rank'],c['delta0_rank'],c['delta0_augmented_rank']),(5,8,9));self.assertEqual(c['h1_dimension'],1)
    def test_all_global_assignments_reject_mermin(self):
        masks=[sum(1<<r for r in c) for c in CONTEXTS]
        # Exhaustive independent truth table on all 512 global assignments.
        self.assertFalse(any(all(bin(g&a).count('1')%2==b for a,b in zip(masks,[0,0,0,0,0,1])) for g in range(512)))
    def test_actual_global_control(self):
        c=m.certify(case([0]*6));self.assertEqual(c['global_section'],[0]*9);self.assertEqual(c['delta0_rank'],c['delta0_augmented_rank']);self.assertEqual(c['obstruction_pairing'],0)
    def test_nonzero_consistent_targets_are_not_called_obstructed(self):
        p=case([1,0,0,1,0,0]);c=m.certify(p);g=c['global_section'];self.assertIsNotNone(g)
        self.assertTrue(all(sum(g[r] for r in ctx)%2==b for ctx,b in zip(CONTEXTS,p['targets'])))
    def test_malformed_cover_refused(self):
        c=case([0]*6);c['contexts']=[[0,0,2]]+CONTEXTS[1:]
        with self.assertRaises(ValueError):m.certify(c)
        with self.assertRaises(ValueError):m.rank([[True]],1)
if __name__=='__main__':unittest.main()
