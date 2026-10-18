r"""
Tests for consolidated lift package (emergence, algebra_lift, forced_lift, lift, classical_quantum_lift, row_sparsity_descent).

AuthorityEffect: None.
"""

from omega_engine.crates.lift import (
    StructureDerived,
    LiftRequired,
    RefusedFormalism,
    FormalismEmergenceEngine,
    BinaryOperation,
    check_associativity,
    AlgebraLiftOperator,
    ForcedLift,
    verify_forced_lift,
    LiftRequest,
    LiftLicense,
    CheckedLiftLicense,
    verify_lift_contract,
)


def test_formalism_emergence():
    engine = FormalismEmergenceEngine()
    engine.register_resolver("Algebra", lambda state, act: isinstance(state, StructureDerived))
    
    op = BinaryOperation([0, 1], {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0})
    lift_op = AlgebraLiftOperator(op)
    
    res = lift_op("witness")
    assert isinstance(res, StructureDerived)
    assert engine.resolve(lift_op, "witness", "Algebra")


def test_algebra_lift_associativity_check():
    # Associative operation (addition mod 2)
    op = BinaryOperation([0, 1], {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0})
    is_assoc, failures = check_associativity(op)
    assert is_assoc
    assert not failures

    # Non-associative operation (subtraction mod 3)
    op_non = BinaryOperation([0, 1, 2], {(x, y): (x - y) % 3 for x in range(3) for y in range(3)})
    is_assoc_non, failures_non = check_associativity(op_non)
    assert not is_assoc_non
    assert len(failures_non) > 0


def test_forced_lift_verification():
    lift = ForcedLift(
        name="TestLift",
        lift_map=lambda s: s * 2,
        obstruction_resolver=lambda s: s == 4,
    )
    result = verify_forced_lift(lift, 2)
    assert result is True

    fail_result = verify_forced_lift(lift, 3)
    assert isinstance(fail_result, RefusedFormalism) or hasattr(fail_result, "reason")


