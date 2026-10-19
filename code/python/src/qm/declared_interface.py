"""Exercise an explicitly admitted interface on real-rational two-state inputs.

These calculations do not derive the complex scalar field, Hilbert structure,
Born rule, tensor rule, channels, observer records or a time evolution.
"""
from fractions import Fraction as Q
from .pfp_exact import matrix,eye,transpose,multiply,add,scale,tensor,trace,is_psd
SLOTS=('scalar_field','inner_product','positive_states_and_effects','Born_trace','tensor','channels','unitary_step_and_time','observer_records')
def certify(admissions,rho,effect,kraus,unitary):
    if set(admissions)!=set(SLOTS) or any(type(v) is not str or not v.startswith('ADMITTED: ') for v in admissions.values()):raise ValueError('explicit admitted interface slots required')
    rho,effect,unitary=map(matrix,(rho,effect,unitary));ks=list(map(matrix,kraus))
    if any(len(a)!=2 or len(a[0])!=2 for a in [rho,effect,unitary]+ks) or not ks:raise ValueError('nonempty declared two-state matrices required')
    identity=eye(2);zero=scale(0,identity)
    if not is_psd(rho) or trace(rho)!=1:raise ValueError('positive trace-one state required')
    if not is_psd(effect) or not is_psd(add(identity,scale(-1,effect))):raise ValueError('effect must lie between zero and identity')
    completeness=zero;channel=zero
    for k in ks:
        completeness=add(completeness,multiply(transpose(k),k));channel=add(channel,multiply(multiply(k,rho),transpose(k)))
    if completeness!=identity:raise ValueError('Kraus trace-preservation hypothesis required')
    ustaru=multiply(transpose(unitary),unitary)
    if ustaru!=identity:raise ValueError('supplied unitary step required')
    evolved=multiply(multiply(unitary,rho),transpose(unitary));joint=tensor(rho,rho)
    arrays={'density':rho,'effect':effect,'kraus_completeness':completeness,'channel_density':channel,'unitary_star_unitary':ustaru,'evolved_density':evolved,'tensor_density':joint}
    scalars={'Born_weight':trace(multiply(rho,effect)),'unit_weight':trace(rho),'channel_trace':trace(channel),'evolved_trace':trace(evolved),'tensor_trace':trace(joint),'channel_Born_weight':trace(multiply(channel,effect))}
    return {'admissions':dict(admissions),'matrices':{k:[[str(x) for x in r] for r in a] for k,a in arrays.items()},'scalars':{k:str(v) for k,v in scalars.items()},'derivation_status':'ADMITTED_INTERFACE_EXERCISED_ONLY'}
