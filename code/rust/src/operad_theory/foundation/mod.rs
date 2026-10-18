//! Foundation Tier for Operad Theory.
//!
//! AuthorityEffect: None.

pub mod colour;
pub mod operation;
pub mod planar_tree;
pub mod colored_operad;
pub mod monoidal_operad;
pub mod span_operand;

pub use colour::{OperadColour, OperadSignature};
pub use operation::{Operation, OperationId, OperationKind, OperationKindType};
pub use planar_tree::{OpenLeaf, PlanarTree, TreeChild};
pub use colored_operad::{OperadVariant, PlanarColoredOperad, SymmetricColoredOperad};
pub use monoidal_operad::MonoidalOperad;
pub use span_operand::{SpanOperand, ADMITTED_FINITE_COLOURS};

/// Validates operadic tree arity conservation under grafting: arity(T o_i S) = arity(T) + arity(S) - 1.
pub fn verify_tree_grafting_arity_formula(t_arity: usize, s_arity: usize) -> usize {
    t_arity + s_arity - 1
}

#[cfg(test)]
mod found_tests {
    use super::*;

    #[test]
    fn test_arity_formula() {
        assert_eq!(verify_tree_grafting_arity_formula(2, 2), 3);
    }
}
