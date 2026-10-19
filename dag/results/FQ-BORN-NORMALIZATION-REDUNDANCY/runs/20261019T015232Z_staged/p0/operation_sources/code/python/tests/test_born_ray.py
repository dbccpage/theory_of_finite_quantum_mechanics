from fractions import Fraction as Q
import importlib,itertools
from pathlib import Path
import sys,types,unittest
package=types.ModuleType('staged_qm');package.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[package.__name__]=package
born=importlib.import_module('staged_qm.born_ray')


class BornRayTests(unittest.TestCase):
    def test_all_small_vectors_are_bound_to_actual_scalars_or_nonzero_minors(self):
        vectors=[v for v in itertools.product(range(4),repeat=3) if sum(v)]
        for left in vectors:
            for right in vectors:
                c=born.certify(left,right,Q(7,3));self.assertEqual(c['normalized'],c['normalized_twice']);self.assertEqual(c['normalized'],c['normalized_scaled'])
                if c['same_weight_ray']:
                    scale=Q(c['ray_scale']);self.assertGreater(scale,0);self.assertEqual(tuple(map(Q,right)),tuple(scale*x for x in left))
                else:
                    i,j=c['separating_minor']['indices'];value=right[i]*left[j]-left[i]*right[j]
                    self.assertEqual(Q(c['separating_minor']['value']),value);self.assertNotEqual(value,0)
    def test_zero_negative_and_nonpositive_scale_are_refused(self):
        for w in ([],[0,0],[-1,2]):
            with self.assertRaises(ValueError):born.normalize(w)
        for c in (0,-1):
            with self.assertRaises(ValueError):born.certify([1],[1],c)
    def test_floats_booleans_and_strings_are_refused(self):
        for x in (True,0.5,'1/2'):
            with self.assertRaises(TypeError):born.normalize([x,1])
    def test_arbitrary_precision_and_zero_coordinates(self):
        d=10**100+7;a=[0,Q(1,d),1];b=[0,Q(3,d),3]
        c=born.certify(a,b,Q(2,7));self.assertTrue(c['same_weight_ray']);self.assertEqual(c['ray_scale'],'3')
    def test_equal_born_weights_do_not_determine_an_amplitude_ray(self):
        a=[(1,0),(1,0)];b=[(1,0),(-1,0)]
        self.assertEqual(born.born_weights(a),born.born_weights(b));self.assertNotEqual(a[0][0]*b[1][0]-a[1][0]*b[0][0],0)


if __name__=='__main__':unittest.main()
