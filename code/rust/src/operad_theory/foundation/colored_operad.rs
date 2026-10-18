//! Foundation: Planar & Symmetric Coloured Operads.
//!
//! AuthorityEffect: None.

use std::collections::{HashMap, HashSet};
use serde::{Deserialize, Serialize};
use super::colour::{OperadColour, OperadSignature};
use super::operation::{Operation, OperationId, OperationKind};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum OperadVariant {
    Planar,
    Symmetric,
}

/// A planar multi-coloured operad with strictly ordered input slots.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlanarColoredOperad {
    pub name: String,
    pub is_closed_universe: bool,
    colours: HashSet<OperadColour>,
    generators: HashMap<String, Operation>,
}

impl PlanarColoredOperad {
    pub fn new(name: impl Into<String>, is_closed_universe: bool) -> Self {
        Self {
            name: name.into(),
            is_closed_universe,
            colours: HashSet::new(),
            generators: HashMap::new(),
        }
    }

    pub fn variant(&self) -> OperadVariant {
        OperadVariant::Planar
    }

    pub fn colours(&self) -> &HashSet<OperadColour> {
        &self.colours
    }

    pub fn operations(&self) -> &HashMap<String, Operation> {
        &self.generators
    }

    pub fn add_colour(&mut self, colour: OperadColour) -> OperadColour {
        self.colours.insert(colour.clone());
        colour
    }

    pub fn add_operation(&mut self, op: Operation) -> Result<(), String> {
        if self.generators.contains_key(op.op_id.as_str()) {
            return Err(format!(
                "Duplicate operation ID '{}' already exists in operad '{}'",
                op.op_id.as_str(),
                self.name
            ));
        }

        if self.is_closed_universe {
            for inp in op.inputs() {
                if !self.colours.contains(inp) {
                    return Err(format!(
                        "Operation '{}' references unadmitted input colour: {}",
                        op.op_id.as_str(),
                        inp.as_str()
                    ));
                }
            }
            if !self.colours.contains(op.output()) {
                return Err(format!(
                    "Operation '{}' references unadmitted output colour: {}",
                    op.op_id.as_str(),
                    op.output().as_str()
                ));
            }
        } else {
            for inp in op.inputs() {
                self.colours.insert(inp.clone());
            }
            self.colours.insert(op.output().clone());
        }

        self.generators.insert(op.op_id.as_str().to_string(), op);
        Ok(())
    }

    pub fn ensure_identities(&mut self) -> Vec<Operation> {
        let mut added = Vec::new();
        let sorted_colours: Vec<OperadColour> = {
            let mut c_vec: Vec<OperadColour> = self.colours.iter().cloned().collect();
            c_vec.sort();
            c_vec
        };
        for c in sorted_colours {
            let id_op = Operation::identity(c);
            if !self.generators.contains_key(id_op.op_id.as_str()) {
                self.generators.insert(id_op.op_id.as_str().to_string(), id_op.clone());
                added.push(id_op);
            }
        }
        added
    }

    pub fn partial_compose(&self, f: &Operation, g: &Operation, i: usize) -> Result<Operation, String> {
        if i >= f.arity() {
            return Err(format!("Insertion index i={} out of range [0, {})", i, f.arity()));
        }

        let target_input = &f.inputs()[i];
        if g.output() != target_input {
            return Err(format!(
                "Partial composition ill-typed: {} expects colour {} at position {}, but {} outputs {}",
                f.op_id.as_str(),
                target_input.as_str(),
                i,
                g.op_id.as_str(),
                g.output().as_str()
            ));
        }

        let mut new_inputs = f.inputs()[..i].to_vec();
        new_inputs.extend_from_slice(g.inputs());
        new_inputs.extend_from_slice(&f.inputs()[i + 1..]);

        let new_id = OperationId::new(format!("({}_o_{}_{})", f.op_id.as_str(), i, g.op_id.as_str()))?;

        Ok(Operation {
            op_id: new_id,
            signature: OperadSignature::new(new_inputs, f.output().clone()),
            kind: OperationKind::composite(format!("{}_o_{}_{}", f.op_id.as_str(), i, g.op_id.as_str())),
            is_equivariant: false,
            description: format!("Planar composition of {} and {} at slot {}", f.op_id.as_str(), g.op_id.as_str(), i),
        })
    }

    pub fn full_compose(&self, f: &Operation, args: &[Operation]) -> Result<Operation, String> {
        if args.len() != f.arity() {
            return Err(format!("Expected {} operations for full composition, got {}", f.arity(), args.len()));
        }

        let mut current = f.clone();
        for idx in (0..f.arity()).rev() {
            current = self.partial_compose(&current, &args[idx], idx)?;
        }
        Ok(current)
    }
}

/// A symmetric multi-coloured operad supporting lawful Sigma_n input permutations.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SymmetricColoredOperad {
    pub planar: PlanarColoredOperad,
}

impl SymmetricColoredOperad {
    pub fn new(name: impl Into<String>, is_closed_universe: bool) -> Self {
        Self {
            planar: PlanarColoredOperad::new(name, is_closed_universe),
        }
    }

    pub fn variant(&self) -> OperadVariant {
        OperadVariant::Symmetric
    }

    pub fn add_colour(&mut self, colour: OperadColour) -> OperadColour {
        self.planar.add_colour(colour)
    }

    pub fn add_operation(&mut self, op: Operation) -> Result<(), String> {
        self.planar.add_operation(op)
    }

    pub fn ensure_identities(&mut self) -> Vec<Operation> {
        self.planar.ensure_identities()
    }

    pub fn permute_operation(&mut self, op: &Operation, permutation: &[usize]) -> Result<Operation, String> {
        let perm_op = op.permute_inputs(permutation)?;
        self.planar.add_operation(perm_op.clone())?;
        Ok(perm_op)
    }
}
