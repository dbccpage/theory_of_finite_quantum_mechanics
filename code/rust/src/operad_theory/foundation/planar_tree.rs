
use std::fmt;
use sha2::{Digest, Sha256};
use serde::{Deserialize, Serialize};
use super::colour::OperadColour;
use super::operation::Operation;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct OpenLeaf {
    pub colour: OperadColour,
}

impl OpenLeaf {
    pub fn new(colour: OperadColour) -> Self {
        Self { colour }
    }
}

impl fmt::Display for OpenLeaf {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Leaf({})", self.colour)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum TreeChild {
    Leaf(OpenLeaf),
    Subtree(PlanarTree),
}

impl TreeChild {
    pub fn output_colour(&self) -> &OperadColour {
        match self {
            Self::Leaf(l) => &l.colour,
            Self::Subtree(t) => t.output_colour(),
        }
    }

    pub fn arity(&self) -> usize {
        match self {
            Self::Leaf(_) => 1,
            Self::Subtree(t) => t.arity(),
        }
    }

    pub fn term_hash(&self) -> String {
        match self {
            Self::Leaf(l) => format!("leaf:{}", l.colour.as_str()),
            Self::Subtree(t) => format!("sub:{}", t.term_hash()),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PlanarTree {
    pub root: Operation,
    pub children: Vec<TreeChild>,
}

impl PlanarTree {
    pub fn new(root: Operation, children: Option<Vec<TreeChild>>) -> Result<Self, String> {
        let actual_children = match children {
            None => root
                .inputs()
                .iter()
                .map(|c| TreeChild::Leaf(OpenLeaf::new(c.clone())))
                .collect(),
            Some(ch) => {
                if ch.len() != root.arity() {
                    return Err(format!(
                        "PlanarTree children count {} != root operation arity {}",
                        ch.len(),
                        root.arity()
                    ));
                }
                for (idx, child) in ch.iter().enumerate() {
                    let expected = &root.inputs()[idx];
                    if child.output_colour() != expected {
                        return Err(format!(
                            "Child colour mismatch at slot {}: expected {}, got {}",
                            idx,
                            expected.as_str(),
                            child.output_colour().as_str()
                        ));
                    }
                }
                ch
            }
        };

        Ok(Self {
            root,
            children: actual_children,
        })
    }

    pub fn corolla(operation: Operation) -> Self {
        let children: Vec<TreeChild> = operation
            .inputs()
            .iter()
            .map(|c| TreeChild::Leaf(OpenLeaf::new(c.clone())))
            .collect();
        Self {
            root: operation,
            children,
        }
    }

    pub fn arity(&self) -> usize {
        self.children.iter().map(|ch| ch.arity()).sum()
    }

    pub fn output_colour(&self) -> &OperadColour {
        self.root.output()
    }

    pub fn term_hash(&self) -> String {
        let mut parts = vec![self.root.op_id.as_str().to_string()];
        for ch in &self.children {
            parts.push(ch.term_hash());
        }
        let mut hasher = Sha256::new();
        hasher.update(parts.join(";").as_bytes());
        let digest = hex::encode(hasher.finalize());
        format!("tree_{}", &digest[..16])
    }

    pub fn graft(&self, slot_index: usize, subtree: PlanarTree) -> Result<PlanarTree, String> {
        if slot_index >= self.children.len() {
            return Err(format!(
                "Root slot index {} out of range [0, {})",
                slot_index,
                self.children.len()
            ));
        }

        let expected_colour = &self.root.inputs()[slot_index];
        if subtree.output_colour() != expected_colour {
            return Err(format!(
                "Cannot graft subtree into slot {}: expected output colour {}, got {}",
                slot_index,
                expected_colour.as_str(),
                subtree.output_colour().as_str()
            ));
        }

        let mut new_children = self.children.clone();
        new_children[slot_index] = TreeChild::Subtree(subtree);
        Ok(PlanarTree {
            root: self.root.clone(),
            children: new_children,
        })
    }
}
