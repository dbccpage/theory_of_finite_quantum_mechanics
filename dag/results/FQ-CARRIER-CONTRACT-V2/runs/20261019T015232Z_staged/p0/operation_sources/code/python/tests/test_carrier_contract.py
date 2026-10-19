from fractions import Fraction as Q
import importlib,subprocess
from pathlib import Path
import sys,types,unittest
package=types.ModuleType('staged_qm');package.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[package.__name__]=package
carrier=importlib.import_module('staged_qm.carrier_contract');domain=importlib.import_module('staged_qm.domain.cyclotomic_tower')
def sample():return {'id':'n3','source_conductor':3,'intermediate_conductor':6,'target_conductor':120,'a':[Q(2),Q(1)],'b':[Q(1),Q(-1)]}
class CarrierTests(unittest.TestCase):
    def test_label_lcm_is_not_field_minimality(self):
        self.assertEqual(domain.CyclotomicTower.minimal_conductor([1,2,3,4,5,8,12]),120)
        self.assertEqual(domain.CyclotomicTower.minimal_conductor([2]),2)
        self.assertEqual(domain.CyclotomicElement.zeta(2).as_rational(),-1)
    def test_actual_norm_and_lift_composition(self):
        c=carrier.certify([{'target_id':1,'conductor':3}],[sample()])['samples'][0]
        self.assertEqual(c['embedded_coefficients'],c['via_intermediate_coefficients']);self.assertEqual(c['embedded_norm_coefficients'],c['norm_after_embedding'])
        self.assertEqual(c['embedded_sum'],c['sum_after_embedding']);self.assertEqual(c['embedded_product'],c['product_after_embedding'])
    def test_invalid_lift_is_refused_with_optimization(self):
        path=Path(domain.__file__)
        source='import importlib.util; s=importlib.util.spec_from_file_location("c",'+repr(str(path))+');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\ntry:m.CyclotomicElement.zeta(3).lift_to(4)\nexcept ValueError:print("refused")\nelse:raise RuntimeError("bad lift accepted")'
        child=subprocess.run([sys.executable,'-O','-c',source],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.assertEqual(child.returncode,0,child.stderr.decode());self.assertEqual(child.stdout.strip(),b'refused')
    def test_inexact_coefficients_are_refused(self):
        for x in (True,0.5,'1/2'):
            p=sample();p['a']=[x,Q(0)]
            with self.assertRaises(TypeError):carrier.certify([{'target_id':1,'conductor':3}],[p])
    def test_no_colimit_or_full_target_amplitude_promotion(self):
        c=carrier.certify([{'target_id':1,'conductor':3}],[sample()])
        self.assertFalse(c['declaration_boundary']['colimit_constructed']);self.assertFalse(c['declaration_boundary']['all_target_amplitudes_verified']);self.assertEqual(c['declaration_boundary']['Kronecker_Weber'],'DECLARED')
if __name__=='__main__':unittest.main()
