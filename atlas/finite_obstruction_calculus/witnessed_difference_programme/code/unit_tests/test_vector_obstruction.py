from fractions import Fraction

import pytest
from witnessed_difference.vector_obstruction import (
    source_three_node_example,
    triangle_vector_obstruction,
)


def test_source_three_node_vector_obstruction_is_recreated_exactly() -> None:
    result = source_three_node_example()
    assert result.circulation == (Fraction(1), Fraction(1))
    assert result.repair_potential == ((0, 0), (1, 0), (1, 1))
    assert result.residual == ((0, 0), (0, 0), (1, 1))
    assert result.l1_l1_minimum == 2
    assert result.l1_l2_minimum_squared == 2
    assert result.l1_l2_minimum_display == "1.414214"


def test_vector_obstruction_accepts_exact_scalars_and_refuses_wrong_shape() -> None:
    result = triangle_vector_obstruction((("1/2", 0), (0, Fraction(1, 2)), (0, 0)))
    assert result.l1_l1_minimum == 1
    assert result.l1_l2_minimum_squared == Fraction(1, 2)
    with pytest.raises(ValueError, match="three oriented"):
        triangle_vector_obstruction(((1, 0),))
    with pytest.raises(ValueError, match="two coordinates"):
        triangle_vector_obstruction(((1, 0, 0), (0, 1), (0, 0)))
    with pytest.raises(TypeError, match="exact"):
        triangle_vector_obstruction(((1.0, 0), (0, 1), (0, 0)))


def test_vector_obstruction_formats_large_exact_norm_without_float_overflow() -> None:
    large = 10**1000
    result = triangle_vector_obstruction(((large, 0), (0, 0), (0, 0)))
    assert result.l1_l2_minimum_squared == large * large
    assert result.l1_l2_minimum_display == f"{large}.000000"


# Executable finite evidence; AuthorityEffect: None.
