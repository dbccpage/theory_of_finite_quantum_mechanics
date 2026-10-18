
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
