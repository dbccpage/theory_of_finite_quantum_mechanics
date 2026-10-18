

class OperadExpectationTests(unittest.TestCase):
    def test_composition_and_linearity_on_arbitrary_exact_tables(self):
        law = [Q((i*7+11) % 31+1) for i in range(16)]
        law = [p/sum(law) for p in law]
        table = [[Q((i+1)*(j-2), i+j+3) for j in range(4)] for i in range(16)]
        left = bell.chsh_linear(bell.joint_expectation(law, table))
        right = sum(p*bell.chsh_linear(row) for p,row in zip(law,table))
        self.assertEqual(left, right)
        self.assertEqual(bell.joint_expectation(law,bell.response_products()), bell.certify_joint_law(law).correlators)
        self.assertEqual(bell.chsh_linear(bell.joint_expectation(law,bell.response_products())),bell.certify_joint_law(law).chsh)
        # Linearity alone does not import a bound for arbitrary response maps.
        self.assertEqual(bell.chsh_linear(bell.joint_expectation(law,[[2,2,2,2]]*16)),4)

    def test_generic_map_shape_and_exactness(self):
        for table in ([[1,1,1,1]]*15, [[1,1,1]]*16):
            with self.assertRaises(ValueError): bell.joint_expectation([Q(1,16)]*16,table)
        for bad in (True, 1.0, '1'):
            with self.assertRaises(TypeError): bell.chsh_linear([1,1,1,bad])
            with self.assertRaises(TypeError): bell.joint_expectation([Q(1,16)]*16,[[1,1,1,bad]]*16)

    def test_consumer_rejects_each_forged_field(self):
        from dataclasses import replace
        law = [Q(i,136) for i in range(1,17)]
        c = bell.certify_joint_law(law)
        bell.verify_joint_certificate(law,c)
        for field in ('chsh','positive_score_mass','negative_score_mass','lower_slack','upper_slack'):
            with self.assertRaises(ValueError): bell.verify_joint_certificate(law,replace(c,**{field:getattr(c,field)+1}))
        for j in range(4):
            vector = list(c.correlators);vector[j] += 1
            with self.assertRaises(ValueError): bell.verify_joint_certificate(law,replace(c,correlators=tuple(vector)))
        with self.assertRaises(TypeError): bell.verify_joint_certificate(law,replace(c,chsh=True))

    def test_all_vertices_and_rational_mixtures_through_consumer(self):
        for i in range(16):
            for j in range(16):
                for p in (Q(1,7),Q(2,5),Q(11,13)):
                    law=[Q(0)]*16;law[i]+=p;law[j]+=1-p
                    bell.verify_joint_certificate(law,bell.certify_joint_law(law))
