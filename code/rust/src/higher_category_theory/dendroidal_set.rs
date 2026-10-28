
use std::collections::{BTreeMap, HashMap, HashSet};

use engine_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};

use crate::error::{reserve_exact, HigherCategoryError};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TreeEdge {
    pub id: String,
    pub colour: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TreeVertex {
    pub id: String,
    pub inputs: Vec<String>,
    pub output: String,
    pub operation_id: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PlanarTree {
    pub id: String,
    pub vertices: Vec<TreeVertex>,
    pub edges: Vec<TreeEdge>,
    pub root_edge: String,
    pub leaf_edges: Vec<String>,
    pub inner_edges: Vec<String>,
}

impl PlanarTree {
    pub fn corolla(
        id: &str,
        operation_id: &str,
        input_colours: &[&str],
        output_colour: &str,
        limits: &OperationLimits,
    ) -> Result<Self, HigherCategoryError> {
        let mut edges = Vec::new();
        reserve_exact(&mut edges, input_colours.len() + 1, limits)?;

        let mut leaf_edges = Vec::new();
        reserve_exact(&mut leaf_edges, input_colours.len(), limits)?;

        for (idx, &c) in input_colours.iter().enumerate() {
            let edge_id = format!("{}_in_{}", id, idx);
            edges.push(TreeEdge {
                id: edge_id.clone(),
                colour: c.to_string(),
            });
            leaf_edges.push(edge_id);
        }

        let root_edge_id = format!("{}_root", id);
        edges.push(TreeEdge {
            id: root_edge_id.clone(),
            colour: output_colour.to_string(),
        });

        let mut vertices = Vec::new();
        reserve_exact(&mut vertices, 1, limits)?;
        vertices.push(TreeVertex {
            id: format!("{}_v0", id),
            inputs: leaf_edges.clone(),
            output: root_edge_id.clone(),
            operation_id: Some(operation_id.to_string()),
        });

        Ok(PlanarTree {
            id: id.to_string(),
            vertices,
            edges,
            root_edge: root_edge_id,
            leaf_edges,
            inner_edges: Vec::new(),
        })
    }

    pub fn graft_two_corollas(
        id: &str,
        lower: &PlanarTree,
        upper: &PlanarTree,
        graft_index: usize,
        limits: &OperationLimits,
    ) -> Result<Self, HigherCategoryError> {
        if graft_index >= lower.leaf_edges.len() {
            return Err(HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("graft_index < {}", lower.leaf_edges.len()),
                found: format!("{}", graft_index),
            });
        }

        let lower_graft_edge_id = &lower.leaf_edges[graft_index];
        let lower_edge = lower
            .edges
            .iter()
            .find(|e| &e.id == lower_graft_edge_id)
            .ok_or_else(|| HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("lower edge '{}' exists", lower_graft_edge_id),
                found: "not found".to_string(),
            })?;

        let upper_root_edge = upper
            .edges
            .iter()
            .find(|e| e.id == upper.root_edge)
            .ok_or_else(|| HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("upper root edge '{}' exists", upper.root_edge),
                found: "not found".to_string(),
            })?;

        if lower_edge.colour != upper_root_edge.colour {
            return Err(HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!(
                    "matching graft edge colours: lower '{}' == upper '{}'",
                    lower_edge.colour, upper_root_edge.colour
                ),
                found: format!("{} != {}", lower_edge.colour, upper_root_edge.colour),
            });
        }

        let inner_edge_id = format!("{}_inner_e", id);
        let mut edges = Vec::new();
        let total_edges = lower.edges.len() + upper.edges.len() - 1;
        reserve_exact(&mut edges, total_edges, limits)?;

        let mut leaf_edges = Vec::new();
        let total_leaves = lower.leaf_edges.len() + upper.leaf_edges.len() - 1;
        reserve_exact(&mut leaf_edges, total_leaves, limits)?;

        for (idx, e_id) in lower.leaf_edges.iter().enumerate() {
            if idx == graft_index {
                continue;
            }
            let edge = lower.edges.iter().find(|e| &e.id == e_id).unwrap();
            edges.push(edge.clone());
            if idx < graft_index {
                leaf_edges.push(edge.id.clone());
            }
        }

        for e_id in &upper.leaf_edges {
            let edge = upper.edges.iter().find(|e| &e.id == e_id).unwrap();
            edges.push(edge.clone());
            leaf_edges.push(edge.id.clone());
        }

        for (idx, e_id) in lower.leaf_edges.iter().enumerate() {
            if idx > graft_index {
                let edge = lower.edges.iter().find(|e| &e.id == e_id).unwrap();
                leaf_edges.push(edge.id.clone());
            }
        }

        let root_edge = lower.edges.iter().find(|e| e.id == lower.root_edge).unwrap();
        edges.push(root_edge.clone());

        edges.push(TreeEdge {
            id: inner_edge_id.clone(),
            colour: lower_edge.colour.clone(),
        });

        let mut vertices = Vec::new();
        reserve_exact(&mut vertices, 2, limits)?;

        let mut lower_v_inputs = lower.vertices[0].inputs.clone();
        lower_v_inputs[graft_index] = inner_edge_id.clone();
        vertices.push(TreeVertex {
            id: format!("{}_v_bot", id),
            inputs: lower_v_inputs,
            output: root_edge.id.clone(),
            operation_id: lower.vertices[0].operation_id.clone(),
        });

        vertices.push(TreeVertex {
            id: format!("{}_v_top", id),
            inputs: upper.vertices[0].inputs.clone(),
            output: inner_edge_id.clone(),
            operation_id: upper.vertices[0].operation_id.clone(),
        });

        let mut inner_edges = Vec::new();
        reserve_exact(&mut inner_edges, 1, limits)?;
        inner_edges.push(inner_edge_id);

        let tree = PlanarTree {
            id: id.to_string(),
            vertices,
            edges,
            root_edge: root_edge.id.clone(),
            leaf_edges,
            inner_edges,
        };

        tree.validate_tree_acyclicity()?;
        Ok(tree)
    }

    pub fn contract_inner_edge(
        &self,
        inner_edge_id: &str,
        limits: &OperationLimits,
    ) -> Result<Self, HigherCategoryError> {
        if !self.inner_edges.iter().any(|e| e == inner_edge_id) {
            return Err(HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("edge '{}' to be an inner edge", inner_edge_id),
                found: "not an inner edge".to_string(),
            });
        }

        let lower_v = self
            .vertices
            .iter()
            .find(|v| v.inputs.iter().any(|i| i == inner_edge_id))
            .ok_or_else(|| HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("vertex receiving inner edge '{}'", inner_edge_id),
                found: "not found".to_string(),
            })?;

        let upper_v = self
            .vertices
            .iter()
            .find(|v| v.output == inner_edge_id)
            .ok_or_else(|| HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("vertex emitting inner edge '{}'", inner_edge_id),
                found: "not found".to_string(),
            })?;

        let mut merged_inputs = Vec::new();
        reserve_exact(
            &mut merged_inputs,
            lower_v.inputs.len() + upper_v.inputs.len() - 1,
            limits,
        )?;

        for inp in &lower_v.inputs {
            if inp == inner_edge_id {
                for u_inp in &upper_v.inputs {
                    merged_inputs.push(u_inp.clone());
                }
            } else {
                merged_inputs.push(inp.clone());
            }
        }

        let mut remaining_inner_edges = Vec::new();
        reserve_exact(
            &mut remaining_inner_edges,
            self.inner_edges.len().saturating_sub(1),
            limits,
        )?;
        for e in &self.inner_edges {
            if e != inner_edge_id {
                remaining_inner_edges.push(e.clone());
            }
        }

        let mut remaining_edges = Vec::new();
        reserve_exact(
            &mut remaining_edges,
            self.edges.len().saturating_sub(1),
            limits,
        )?;
        for e in &self.edges {
            if e.id != inner_edge_id {
                remaining_edges.push(e.clone());
            }
        }

        let mut vertices = Vec::new();
        reserve_exact(&mut vertices, 1, limits)?;
        vertices.push(TreeVertex {
            id: format!("{}_merged", self.id),
            inputs: merged_inputs,
            output: lower_v.output.clone(),
            operation_id: None,
        });

        Ok(PlanarTree {
            id: format!("{}_contracted", self.id),
            vertices,
            edges: remaining_edges,
            root_edge: self.root_edge.clone(),
            leaf_edges: self.leaf_edges.clone(),
            inner_edges: remaining_inner_edges,
        })
    }

    pub fn contracted_boundary_colours(
        &self,
        inner_edge_id: &str,
    ) -> Result<(Vec<String>, String), HigherCategoryError> {
        let (lower_inputs, lower_output, upper_inputs) = {
            let lower_v = self
                .vertices
                .iter()
                .find(|v| v.inputs.iter().any(|inp| inp == inner_edge_id))
                .ok_or_else(|| HigherCategoryError::DendroidalBoundaryMismatch {
                    expected: format!("vertex receiving inner edge '{}'", inner_edge_id),
                    found: "not found".to_string(),
                })?;
            let upper_v = self
                .vertices
                .iter()
                .find(|v| v.output == inner_edge_id)
                .ok_or_else(|| HigherCategoryError::DendroidalBoundaryMismatch {
                    expected: format!("vertex emitting inner edge '{}'", inner_edge_id),
                    found: "not found".to_string(),
                })?;
            (lower_v.inputs.clone(), lower_v.output.clone(), upper_v.inputs.clone())
        };

        let colour_of = |edge_id: &str| -> Result<String, HigherCategoryError> {
            self.edges
                .iter()
                .find(|edge| edge.id == edge_id)
                .map(|edge| edge.colour.clone())
                .ok_or_else(|| HigherCategoryError::DendroidalBoundaryMismatch {
                    expected: format!("edge '{}' exists", edge_id),
                    found: "not found".to_string(),
                })
        };

        let mut inputs = Vec::new();
        for inp in &lower_inputs {
            if inp == inner_edge_id {
                for upper_inp in &upper_inputs {
                    inputs.push(colour_of(upper_inp)?);
                }
            } else {
                inputs.push(colour_of(inp)?);
            }
        }
        let output = colour_of(&lower_output)?;
        Ok((inputs, output))
    }

    pub fn validate_tree_acyclicity(&self) -> Result<(), HigherCategoryError> {
        let mut visited = HashSet::new();
        let mut on_path = HashSet::new();

        fn dfs(
            v_id: &str,
            tree: &PlanarTree,
            visited: &mut HashSet<String>,
            on_path: &mut HashSet<String>,
        ) -> Result<(), HigherCategoryError> {
            visited.insert(v_id.to_string());
            on_path.insert(v_id.to_string());

            let v = tree.vertices.iter().find(|x| x.id == v_id).unwrap();
            for inp_edge in &v.inputs {
                if let Some(child_v) = tree.vertices.iter().find(|x| &x.output == inp_edge) {
                    if on_path.contains(&child_v.id) {
                        return Err(HigherCategoryError::TreeCycleViolation {
                            details: format!(
                                "Cycle detected between vertex '{}' and '{}'",
                                v_id, child_v.id
                            ),
                        });
                    }
                    if !visited.contains(&child_v.id) {
                        dfs(&child_v.id, tree, visited, on_path)?;
                    }
                }
            }
            on_path.remove(v_id);
            Ok(())
        }

        for v in &self.vertices {
            if !visited.contains(&v.id) {
                dfs(&v.id, self, &mut visited, &mut on_path)?;
            }
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TreeInnerHorn {
    pub tree: PlanarTree,
    pub inner_edge: String,
    pub outer_face_top_op: String,
    pub outer_face_bot_op: String,
}

impl TreeInnerHorn {
    pub fn new(
        tree: PlanarTree,
        inner_edge: &str,
        top_op: &str,
        bot_op: &str,
    ) -> Result<Self, HigherCategoryError> {
        if !tree.inner_edges.iter().any(|e| e == inner_edge) {
            return Err(HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("inner edge '{}' to exist in tree", inner_edge),
                found: "not an inner edge".to_string(),
            });
        }
        if tree.vertices.len() != 2 {
            return Err(HigherCategoryError::DendroidalBoundaryMismatch {
                expected: "2 vertices for minimal inner horn".to_string(),
                found: format!("{} vertices", tree.vertices.len()),
            });
        }
        Ok(TreeInnerHorn {
            tree,
            inner_edge: inner_edge.to_string(),
            outer_face_top_op: top_op.to_string(),
            outer_face_bot_op: bot_op.to_string(),
        })
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DendroidalSet {
    pub colours: Vec<String>,
    pub operations: HashMap<String, (Vec<String>, String)>,
    pub comp_table: HashMap<(String, String, usize), String>,
}

impl DendroidalSet {
    pub fn new(limits: &OperationLimits) -> Result<Self, HigherCategoryError> {
        let mut colours = Vec::new();
        reserve_exact(&mut colours, 0, limits)?;
        Ok(DendroidalSet {
            colours,
            operations: HashMap::new(),
            comp_table: HashMap::new(),
        })
    }

    pub fn add_colour(&mut self, c: &str, limits: &OperationLimits) -> Result<(), HigherCategoryError> {
        if !self.colours.iter().any(|x| x == c) {
            reserve_exact(&mut self.colours, 1, limits)?;
            self.colours.push(c.to_string());
        }
        Ok(())
    }

    pub fn add_operation(
        &mut self,
        op_id: &str,
        inputs: &[&str],
        output: &str,
        limits: &OperationLimits,
    ) -> Result<(), HigherCategoryError> {
        if self.operations.len() >= limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.operations.len() + 1,
                limit: limits.max_cells,
            });
        }
        for inp in inputs {
            if !self.colours.iter().any(|c| c == inp) {
                return Err(HigherCategoryError::ZeroCellNotFound { id: inp.to_string() });
            }
        }
        if !self.colours.iter().any(|c| c == output) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: output.to_string() });
        }
        let inps: Vec<String> = inputs.iter().map(|s| s.to_string()).collect();
        self.operations.insert(op_id.to_string(), (inps, output.to_string()));
        Ok(())
    }

    pub fn register_operadic_composition(
        &mut self,
        lower_op: &str,
        upper_op: &str,
        graft_index: usize,
        composite_op: &str,
    ) -> Result<(), HigherCategoryError> {
        let (lower_inps, lower_out) = self
            .operations
            .get(lower_op)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: lower_op.to_string() })?;
        let (upper_inps, upper_out) = self
            .operations
            .get(upper_op)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: upper_op.to_string() })?;
        let (comp_inps, comp_out) = self
            .operations
            .get(composite_op)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: composite_op.to_string() })?;

        if graft_index >= lower_inps.len() {
            return Err(HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("graft_index < {}", lower_inps.len()),
                found: format!("{}", graft_index),
            });
        }
        if &lower_inps[graft_index] != upper_out {
            return Err(HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("lower input '{}' == upper output '{}'", lower_inps[graft_index], upper_out),
                found: format!("{} != {}", lower_inps[graft_index], upper_out),
            });
        }
        if comp_out != lower_out {
            return Err(HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("composite output '{}' == lower output '{}'", comp_out, lower_out),
                found: format!("{} != {}", comp_out, lower_out),
            });
        }

        let mut expected_inputs = Vec::with_capacity(lower_inps.len() + upper_inps.len() - 1);
        expected_inputs.extend(lower_inps[..graft_index].iter().cloned());
        expected_inputs.extend(upper_inps.iter().cloned());
        expected_inputs.extend(lower_inps[graft_index + 1..].iter().cloned());
        if comp_inps != &expected_inputs {
            return Err(HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("composite inputs {:?}", expected_inputs),
                found: format!("{:?}", comp_inps),
            });
        }

        self.comp_table.insert(
            (lower_op.to_string(), upper_op.to_string(), graft_index),
            composite_op.to_string(),
        );
        Ok(())
    }

    pub fn fill_dendroidal_inner_horn(
        &self,
        horn: &TreeInnerHorn,
    ) -> Result<String, HigherCategoryError> {
        let lower_v = horn
            .tree
            .vertices
            .iter()
            .find(|v| v.inputs.iter().any(|i| i == &horn.inner_edge))
            .ok_or_else(|| HigherCategoryError::DendroidalBoundaryMismatch {
                expected: format!("lower vertex connected to inner edge '{}'", horn.inner_edge),
                found: "not found".to_string(),
            })?;

        let graft_idx = lower_v
            .inputs
            .iter()
            .position(|i| i == &horn.inner_edge)
            .unwrap();

        let key = (
            horn.outer_face_bot_op.clone(),
            horn.outer_face_top_op.clone(),
            graft_idx,
        );

        let composite = self
            .comp_table
            .get(&key)
            .ok_or_else(|| HigherCategoryError::DendroidalMissingFaceMismatch {
                expected: format!(
                    "Operadic composite for lower='{}', upper='{}' at index {}",
                    horn.outer_face_bot_op, horn.outer_face_top_op, graft_idx
                ),
                found: "unregistered in dendroidal set".to_string(),
            })?;

        Ok(composite.clone())
    }

    pub fn verify_dendroidal_inner_horn_property(
        &self,
        horn: &TreeInnerHorn,
    ) -> Result<bool, HigherCategoryError> {
        let composite_id = self.fill_dendroidal_inner_horn(horn)?;
        let (comp_inps, comp_out) = self.operations.get(&composite_id).ok_or_else(|| {
            HigherCategoryError::DendroidalMissingFaceMismatch {
                expected: format!("operation '{}' registered on the dendroidal set", composite_id),
                found: "absent from operations".to_string(),
            }
        })?;
        let (expected_inputs, expected_output) =
            horn.tree.contracted_boundary_colours(&horn.inner_edge)?;
        if comp_inps != &expected_inputs || comp_out != &expected_output {
            return Err(HigherCategoryError::DendroidalMissingFaceMismatch {
                expected: format!("inputs {:?} output {}", expected_inputs, expected_output),
                found: format!("inputs {:?} output {}", comp_inps, comp_out),
            });
        }
        Ok(true)
    }

    pub fn content_hash(&self) -> String {
        use sha2::{Digest, Sha256};
        let mut hasher = Sha256::new();
        hasher.update(b"DendroidalSet::v1::");
        let mut sorted_colours = self.colours.clone();
        sorted_colours.sort();
        for c in sorted_colours {
            hasher.update(c.as_bytes());
            hasher.update(b";");
        }
        let sorted_ops: BTreeMap<_, _> = self.operations.iter().collect();
        for (id, (inps, out)) in sorted_ops {
            hasher.update(id.as_bytes());
            hasher.update(b"->");
            for inp in inps {
                hasher.update(inp.as_bytes());
                hasher.update(b",");
            }
            hasher.update(b":");
            hasher.update(out.as_bytes());
            hasher.update(b";");
        }
        let sorted_comp: BTreeMap<_, _> = self.comp_table.iter().collect();
        for ((bot, top, idx), comp) in sorted_comp {
            hasher.update(format!("{}_o_{}_{}=={};", bot, idx, top, comp).as_bytes());
        }
        format!("sha256:{:x}", hasher.finalize())
    }
}
