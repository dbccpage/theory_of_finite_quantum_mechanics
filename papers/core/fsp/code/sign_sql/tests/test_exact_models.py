"""Adversarial replay of exact SQL Meron/Hubbard model constructions."""

from fractions import Fraction
from itertools import permutations
from pathlib import Path
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import exact_models as model


RING=[(0,1),(1,2),(2,3),(0,3)]


@pytest.mark.parametrize("value",[1.0,0.1,True,"1.0","1e2"])
def test_approximate_inputs_are_rejected(value):
    with pytest.raises((TypeError,ValueError)):
        model.rational(value)


def test_stepwise_rational_fold_exceeds_sqlite_integer_range():
    con=model.connection()
    large=1 << 100
    result=con.execute("SELECT qsum(value) FROM (SELECT ? value UNION ALL SELECT ? UNION ALL SELECT ?)",
                       (f"{large}/3",f"{-large}/3","5/15")).fetchone()[0]
    assert result=="1/3"


@pytest.mark.parametrize("repetitions,q",[(1,"3"),(2,"3"),(2,"5/3"),(2,"1")])
def test_real_meron_partition_replays_independent_transfer(repetitions,q):
    con=model.meron_database(4,repetitions,q)
    summary=model.meron_summary(con)
    assert summary["reconstruction"]
    assert summary["signed_partition"]==model.meron_transfer_trace(4,repetitions,q)
    assert con.execute("SELECT COUNT(*) FROM meron_orbit WHERE merons%2<>0").fetchone()[0]==0
    assert con.execute("SELECT COUNT(*) FROM meron_orbit WHERE qsign(reduced_weight)<0").fetchone()[0]==0


def test_meron_cancellation_and_observable_are_nontrivial():
    con=model.meron_database()
    summary=model.meron_summary(con)
    assert summary["negative_configurations"]==192
    assert summary["signed_partition"]=="912"
    assert summary["absolute_partition"]=="1296"
    assert summary["average_sign"]=="19/27"
    assert summary["staggered_square_numerator"]==summary["improved_staggered_square_numerator"]=="36864"
    # Two-meron orbits have zero denominator but can have nonzero observable numerator.
    assert con.execute("SELECT COUNT(*) FROM meron_orbit o JOIN meron_squared_orbit a ON a.gid=o.gid WHERE o.merons=2 AND qsign(a.numerator)>0").fetchone()[0]>0


@pytest.mark.parametrize("corruption",["sign","weight","missing"])
def test_meron_certificate_rejects_corrupted_orbit(corruption):
    con=model.meron_database()
    if corruption=="sign":
        con.execute("UPDATE meron_configuration SET sign=-sign WHERE gid=0 AND mask=3")
        assert model.meron_summary(con)["invalid_characters"]>0
    elif corruption=="weight":
        con.execute("UPDATE meron_configuration SET weight='2' WHERE gid=0 AND mask=3")
        assert model.meron_summary(con)["unequal_orbit_weights"]==1
    else:
        con.execute("DELETE FROM meron_configuration WHERE gid=0 AND mask=3")
        assert model.meron_summary(con)["incomplete_orbits"]==1
    assert not model.meron_summary(con)["reconstruction"]


def test_meron_input_scope_is_enforced():
    for args in [(3,2,3),(4,0,3),(4,4,3),(4,2,"1/2")]:
        with pytest.raises(ValueError):
            model.meron_database(*args)


def test_meron_cardinality_does_not_admit_an_out_of_domain_orientation():
    con=model.meron_database()
    con.execute("UPDATE meron_configuration SET mask=19 WHERE gid=0 AND mask=3")
    summary=model.meron_summary(con)
    assert not summary["reconstruction"]
    assert summary["orientation_key_defects"]==2


def test_meron_cannot_coherently_delete_a_declared_graph():
    con=model.meron_database()
    for table in ("meron_configuration","meron_state","meron_orientation","meron_component","meron_edge","meron_graph"):
        con.execute(f"DELETE FROM {table} WHERE gid=1")
    summary=model.meron_summary(con)
    assert not summary["reconstruction"]
    assert summary["graphs"]==255
    assert summary["model_relation_defects"]["meron_graph"]==1


def test_meron_cannot_coherently_change_declared_weights_to_negative():
    con=model.meron_database()
    con.execute("UPDATE meron_graph SET weight='-1' WHERE gid=0")
    con.execute("UPDATE meron_configuration SET weight='-1' WHERE gid=0")
    summary=model.meron_summary(con)
    assert not summary["reconstruction"]
    assert "meron_graph" in summary["model_relation_defects"]


def test_meron_cannot_manufacture_a_positive_character_ensemble():
    con=model.meron_database()
    con.execute("UPDATE meron_configuration SET sign=1")
    summary=model.meron_summary(con)
    assert summary["invalid_characters"]==0
    assert not summary["reconstruction"]
    assert "meron_configuration" in summary["model_relation_defects"]


@pytest.mark.parametrize("mutation",[
    "DELETE FROM dq_field WHERE mask=0",
    "DELETE FROM dq_product WHERE mask=0 AND spin=0 AND i=0 AND j=0",
    "DELETE FROM dq_determinant WHERE mask=0 AND spin=0",
    "UPDATE dq_product SET mask=4 WHERE mask=0",
    "UPDATE dq_determinant SET spin=2 WHERE spin=0",
    "UPDATE dq_product SET i=3 WHERE i=0",
])
def test_auxiliary_certificate_rejects_missing_or_stale_relational_support(mutation):
    con=model.auxiliary_hubbard(2,[(0,1)],slices=1)
    con.execute(mutation)
    with pytest.raises(ValueError,match="support|key"):
        model.auxiliary_summary(con)


@pytest.mark.parametrize("table,column,where",[
    ("dq_product","i","mask=0 AND spin=0 AND i=0 AND j=0"),
    ("dq_product","j","mask=0 AND spin=0 AND i=0 AND j=0"),
    ("dq_product","mask","mask=0 AND spin=0 AND i=0 AND j=0"),
    ("dq_product","spin","mask=0 AND spin=0 AND i=0 AND j=0"),
    ("dq_determinant","mask","mask=0 AND spin=0"),
    ("dq_determinant","spin","mask=0 AND spin=0"),
    ("dq_parameter","sites","1=1"),
    ("dq_parameter","slices","1=1"),
    ("dq_parameter","attractive","1=1"),
])
@pytest.mark.parametrize("value",[None,0.5])
def test_auxiliary_certificate_rejects_null_or_nonintegral_keys(table,column,where,value):
    con=model.auxiliary_hubbard(2,[(0,1)],slices=1)
    con.execute(f"UPDATE {table} SET {column}=? WHERE {where}",(value,))
    with pytest.raises(ValueError,match="key columns"):
        model.auxiliary_summary(con)


@pytest.mark.parametrize("bonds,length",[(RING,4),([(0,1),(0,2),(0,3)],6)])
def test_hubbard_configuration_cycles_reconstruct_negative_gauge_holonomy(bonds,length):
    con=model.occupation_hubbard(4,bonds,2,1,interaction="4")
    result=model.gauge_obstruction(con)
    assert not result["diagonal_sign_gauge"]
    path=result["negative_cycle"]
    assert len(path)==length+1 and path[0]==path[-1]
    sign=1
    for source,target in zip(path,path[1:]):
        sign*=-con.execute("SELECT qsign(value) FROM hubbard_hamiltonian WHERE source=? AND target=?",(source,target)).fetchone()[0]
    assert sign==-1
    # This is an interacting two-spin sector; both zero and nonzero U diagonals occur.
    assert {value for value, in con.execute("SELECT DISTINCT value FROM hubbard_hamiltonian WHERE source=target")}=={"0","4"}


def test_open_chain_gauge_reconstructs_every_edge():
    con=model.occupation_hubbard(4,[(0,1),(1,2),(2,3)],2,1)
    result=model.gauge_obstruction(con)
    assert result["diagonal_sign_gauge"]
    gauge=dict(result["gauge"])
    for source,target,value in con.execute("SELECT * FROM hubbard_hamiltonian WHERE source<>target"):
        assert gauge[source]*model.rational(value)*gauge[target]<=0


@pytest.mark.parametrize("bonds",[RING,[(0,1),(0,2),(0,3)],[(0,1),(1,2),(2,3)]])
def test_sql_hubbard_obstruction_agrees_with_independent_sign_normal_form(bonds):
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
    from bqnf_sign_evaluator import normalize_sign_cochain
    con=model.occupation_hubbard(4,bonds,2,1)
    states=[state for state, in con.execute("SELECT state FROM hubbard_basis ORDER BY state")]
    index={state:i for i,state in enumerate(states)}
    edges=[];parities=[]
    for source,target,value in con.execute("SELECT source,target,value FROM hubbard_hamiltonian WHERE source<target"):
        edges.append((index[source],index[target]));parities.append(int(model.rational(value)>0))
    normal=normalize_sign_cochain(len(states),edges,parities)
    sql=model.gauge_obstruction(con)
    assert sql["diagonal_sign_gauge"]==(not any(normal.parities))


def test_hop_sign_replays_two_car_operations():
    for state in range(1 << 6):
        for source in range(6):
            for target in range(6):
                if source==target or not ((state >> source)&1) or ((state >> target)&1):
                    continue
                annihilation=(-1)**((state & ((1 << source)-1)).bit_count())
                removed=state^(1 << source)
                creation=(-1)**((removed & ((1 << target)-1)).bit_count())
                assert model.hop_sign(state,source,target)==annihilation*creation


def test_bipartite_kinetic_exact_inverse_pairing():
    con=model.connection()
    matrix=model.kinetic_matrix(con,4,RING,"3/2")
    assert matrix==list(map(list,zip(*matrix)))
    eta=[1,-1,1,-1]
    inverse=[[eta[i]*matrix[i][j]*eta[j] for j in range(4)] for i in range(4)]
    product=model.sql_matrix_product(con,matrix,inverse)
    assert product==[[Fraction(i==j) for j in range(4)] for i in range(4)]


def test_half_filled_hubbard_all_fields_have_paired_determinants():
    con=model.auxiliary_hubbard(4,RING)
    summary=model.auxiliary_summary(con)
    assert summary["fields"]==256
    assert summary["pairing_verified"]
    assert summary["negative_fields"]==0
    assert summary["average_sign"]=="1"
    assert summary["particle_number_expectation"]=="4"


def test_attractive_frustrated_doped_hubbard_is_a_square():
    con=model.auxiliary_hubbard(3,[(0,1),(1,2),(0,2)],fugacity="3/2",attractive=True)
    summary=model.auxiliary_summary(con)
    assert summary["fields"]==64 and summary["pairing_verified"]
    assert summary["average_sign"]=="1"


@pytest.mark.parametrize("attractive",[False,True])
def test_hs_sum_replays_full_fock_transfer_including_charge_prefactor(attractive):
    con=model.auxiliary_hubbard(2,[(0,1)],fugacity="3/2",attractive=attractive)
    summary=model.auxiliary_summary(con)
    sql=summary["determinant_sum"]
    direct=model.hubbard_transfer_trace(2,[(0,1)],fugacity="3/2",attractive=attractive)
    assert sql==direct
    number=model.hubbard_transfer_trace(2,[(0,1)],fugacity="3/2",attractive=attractive,number_numerator=True)
    assert summary["particle_number_numerator"]==number
    assert model.rational(summary["particle_number_expectation"])==model.rational(number)/model.rational(direct)


@pytest.mark.parametrize("sites,bonds,z,mask",[(4,RING,"2",15721),(3,[(0,1),(1,2),(0,2)],"1",1281)])
def test_negative_hubbard_fields_have_independently_replayed_determinants(sites,bonds,z,mask):
    con=model.auxiliary_hubbard(sites,bonds,4,"2","8",z,field_masks=[mask])
    summary=model.auxiliary_summary(con)
    assert summary["field_coverage"]=="selected fields only"
    assert summary["full_ensemble_average_sign"] is None
    assert summary["selected_subset_average_sign"]=="-1"
    assert summary["negative_fields"]==1
    for spin in (0,1):
        matrix=[[Fraction(0) for _ in range(sites)] for _ in range(sites)]
        for i,j,value in con.execute("SELECT i,j,value FROM dq_product WHERE spin=?",(spin,)):
            matrix[i][j]=model.rational(value)+(i==j)
        independent=Fraction(0)
        for perm in permutations(range(sites)):
            term=Fraction((-1)**sum(perm[i]>perm[j] for i in range(sites) for j in range(i+1,sites)))
            for i,j in enumerate(perm):
                term*=matrix[i][j]
            independent+=term
        stored=con.execute("SELECT value FROM dq_determinant WHERE spin=?",(spin,)).fetchone()[0]
        assert independent==model.rational(stored)


@pytest.mark.parametrize("kwargs",[{"hs":0.5},{"hs":"1/2"},{"fugacity":0},{"field_masks":[1,1]},{"field_masks":[256]},{"field_masks":[]}])
def test_auxiliary_inputs_reject_unsupported_parameters(kwargs):
    with pytest.raises((TypeError,ValueError)):
        model.auxiliary_hubbard(4,RING,**kwargs)


def test_duplicate_hopping_bond_is_not_silently_double_counted():
    with pytest.raises(ValueError):
        model.occupation_hubbard(2,[(0,1),(1,0)],1,1)
