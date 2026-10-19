"""Finite conductor inventory and actual selected cyclotomic lift compositions.

The colimit and Kronecker-Weber input remain declarations. A finite sample of
field elements does not verify every amplitude in the 23 source target systems.
"""
from fractions import Fraction as Q
from .domain.cyclotomic_tower import CyclotomicElement,cyclotomic_polynomial_coeffs,CyclotomicTower


def certify(targets,samples):
    ids=[t['target_id'] for t in targets]
    if len(set(ids))!=len(ids) or any(type(i) is not int for i in ids):raise ValueError('distinct integer target IDs required')
    conductors=[t['conductor'] for t in targets];lcm=CyclotomicTower.minimal_conductor(conductors)
    results=[]
    for sample in samples:
        n,mid,target=sample['source_conductor'],sample['intermediate_conductor'],sample['target_conductor']
        if any(type(x) is not int or x<1 for x in (n,mid,target)) or mid%n or target%mid:raise ValueError('directed divisibility chain required')
        values=[]
        for coefficients in (sample['a'],sample['b']):
            if any(type(x) not in (int,Q) for x in coefficients):raise TypeError('exact rational coefficients required')
            if len(coefficients)!=len(cyclotomic_polynomial_coeffs(n))-1:raise ValueError('full source power-basis vector required')
            values.append(CyclotomicElement(n,coefficients))
        a,b=values;ea=a.lift_to(target);eb=b.lift_to(target);via=a.lift_to(mid).lift_to(target);norm=a.born_weight();enorm=norm.lift_to(target);norm_after=ea.born_weight()
        arrays={'source_coefficients':a.coeffs,'conjugate_coefficients':a.conjugate().coeffs,'norm_coefficients':norm.coeffs,
                'embedded_coefficients':ea.coeffs,'via_intermediate_coefficients':via.coeffs,'embedded_norm_coefficients':enorm.coeffs,
                'norm_after_embedding':norm_after.coeffs,'embedded_sum':(a+b).lift_to(target).coeffs,'sum_after_embedding':(ea+eb).coeffs,
                'embedded_product':(a*b).lift_to(target).coeffs,'product_after_embedding':(ea*eb).coeffs,
                'embedded_conjugate':a.conjugate().lift_to(target).coeffs,'conjugate_after_embedding':ea.conjugate().coeffs}
        if ea.coeffs!=via.coeffs or enorm.coeffs!=norm_after.coeffs or not norm.is_real():raise ArithmeticError('finite lift/norm identity failed')
        results.append({'id':sample['id'],'source_conductor':n,'intermediate_conductor':mid,'target_conductor':target,
                        'source_polynomial':cyclotomic_polynomial_coeffs(n),'target_polynomial':cyclotomic_polynomial_coeffs(target),
                        **{key:list(map(str,value)) for key,value in arrays.items()}})
    return {'inventory_target_ids':ids,'inventory_conductors':conductors,'distinct_conductors':sorted(set(conductors)),
            'label_lcm':lcm,'samples':results,'declaration_boundary':{'colimit_constructed':False,'Kronecker_Weber':'DECLARED','field_minimality_proved':False,'all_target_amplitudes_verified':False}}
